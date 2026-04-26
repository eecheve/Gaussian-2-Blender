import bpy
import bmesh
from mathutils import Vector
import math
import importlib
import Primitives
importlib.reload(Primitives)


def compute_lattice_vectors(bound_box_points):
    origin = Vector(bound_box_points[0])
    a1 = Vector(bound_box_points[1]) - origin
    a2 = Vector(bound_box_points[2]) - origin
    a3 = Vector(bound_box_points[3]) - origin
    return origin, a1, a2, a3


def compute_reciprocal_vectors(a1, a2, a3):
    V = a1.dot(a2.cross(a3))
    if abs(V) < 1e-10:
        raise ValueError("Unit cell volume is zero — lattice vectors are coplanar.")
    b1 = a2.cross(a3) / V
    b2 = a3.cross(a1) / V
    b3 = a1.cross(a2) / V
    return b1, b2, b3


def compute_miller_normal(h, k, l, b1, b2, b3):
    g_hkl = h * b1 + k * b2 + l * b3
    if g_hkl.length < 1e-10:
        raise ValueError(f"Miller indices ({h},{k},{l}) produce a zero normal vector.")
    return g_hkl.normalized()


def compute_plane_anchor(h, k, l, origin, a1, a2, a3):
    if h != 0:
        return origin + a1 / h
    elif k != 0:
        return origin + a2 / k
    elif l != 0:
        return origin + a3 / l
    else:
        raise ValueError("At least one Miller index must be non-zero.")


def compute_unit_cell_corners(origin, a1, a2, a3):
    """
    Computes all 8 corners of the unit cell parallelepiped.
    Bit masking maps index 0-7 to the 8 combinations of (0/1)*a1, (0/1)*a2, (0/1)*a3.
    """
    corners = []
    for i in range(8):
        corner = origin.copy()
        if i & 1: corner += a1
        if i & 2: corner += a2
        if i & 4: corner += a3
        corners.append(corner)
    return corners


PARALLELEPIPED_EDGES = [
    (0, 1), (0, 2), (0, 4),
    (1, 3), (1, 5),
    (2, 3), (2, 6),
    (3, 7),
    (4, 5), (4, 6),
    (5, 7), (6, 7)
]


def intersect_plane_with_edges(corners, normal, anchor, tolerance=1e-8):
    """
    Finds intersection points of the (hkl) plane with the 12 edges
    of the unit cell parallelepiped.

    The plane equation is: normal · (p - anchor) = 0
    For an edge from p0 to p1, parameterize as p(t) = p0 + t*(p1-p0),
    solve for t, keep if 0 <= t <= 1.
    """
    intersection_points = []

    for i, j in PARALLELEPIPED_EDGES:
        p0 = corners[i]
        p1 = corners[j]
        edge = p1 - p0

        denom = normal.dot(edge)
        if abs(denom) < tolerance:
            continue  # edge is parallel to plane

        t = normal.dot(anchor - p0) / denom
        if -tolerance <= t <= 1.0 + tolerance:
            point = p0 + t * edge
            intersection_points.append(point)

    return intersection_points


def sort_polygon_vertices(points, normal):
    """
    Sorts intersection points angularly around their centroid
    so the polygon face winds correctly.
    """
    if len(points) < 3:
        return points

    centroid = Vector((0, 0, 0))
    for p in points:
        centroid += p
    centroid /= len(points)

    # Build two orthogonal axes in the plane
    ref = points[0] - centroid
    if ref.length < 1e-10:
        ref = points[1] - centroid
    ref.normalize()
    perp = normal.cross(ref).normalized()

    def angle(p):
        v = p - centroid
        return math.atan2(v.dot(perp), v.dot(ref))

    return sorted(points, key=angle)


def build_mesh_from_polygon(vertices, name):
    """
    Creates a Blender mesh object from an ordered list of vertices,
    forming a single flat face.
    """
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    bm_verts = [bm.verts.new(v) for v in vertices]
    bm.faces.new(bm_verts)
    bm.to_mesh(mesh)
    bm.free()

    return obj


def assign_material_to_object(obj, mat_dict):
    mat = mat_dict.get("Yy")
    if mat:
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)
    else:
        print("MillerPlaneBuilder: 'Yy' material not found in mat_dict.")


def InstantiateMillerPlane(bound_box_points, h, k, l, mat_dict):
    """
    Renders a polygon clipped to the unit cell boundaries,
    oriented by Miller indices (hkl).

    :param bound_box_points: list of Vectors defining the unit cell corners
    :param h: Miller index h
    :param k: Miller index k
    :param l: Miller index l
    :param mat_dict: materials dictionary
    """
    if h == 0 and k == 0 and l == 0:
        print("MillerPlaneBuilder: all indices are zero, no plane will be rendered.")
        return

    print(f"MillerPlaneBuilder: rendering plane ({h} {k} {l})")

    origin, a1, a2, a3 = compute_lattice_vectors(bound_box_points)
    b1, b2, b3         = compute_reciprocal_vectors(a1, a2, a3)
    normal             = compute_miller_normal(h, k, l, b1, b2, b3)
    anchor             = compute_plane_anchor(h, k, l, origin, a1, a2, a3)
    corners            = compute_unit_cell_corners(origin, a1, a2, a3)

    print(f"  normal: {normal}")
    print(f"  anchor: {anchor}")

    intersection_points = intersect_plane_with_edges(corners, normal, anchor)

    if len(intersection_points) < 3:
        print(f"MillerPlaneBuilder: plane ({h}{k}{l}) does not intersect the unit cell.")
        return

    # Remove duplicate points that can appear at corners
    unique_points = []
    for p in intersection_points:
        if not any((p - q).length < 1e-6 for q in unique_points):
            unique_points.append(p)

    sorted_points = sort_polygon_vertices(unique_points, normal)
    print(f"  polygon vertices: {len(sorted_points)}")

    plane_name = f"MillerPlane_{h}{k}{l}"
    obj = build_mesh_from_polygon(sorted_points, plane_name)
    assign_material_to_object(obj, mat_dict)

    print(f"MillerPlaneBuilder: plane '{plane_name}' instantiated successfully.")