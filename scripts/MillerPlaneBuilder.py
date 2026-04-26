import bpy
from mathutils import Vector
import math

import importlib
import Primitives
importlib.reload(Primitives)


def compute_lattice_vectors(bound_box_points):
    """
    Extracts the three lattice vectors from the bounding box points.
    bound_box_points[0] is the origin.
    bound_box_points[1], [2], [3] are the three adjacent corners.
    """
    origin = Vector(bound_box_points[0])
    a1 = Vector(bound_box_points[1]) - origin
    a2 = Vector(bound_box_points[2]) - origin
    a3 = Vector(bound_box_points[3]) - origin
    return origin, a1, a2, a3


def compute_reciprocal_vectors(a1, a2, a3):
    """
    Computes the reciprocal lattice vectors b1, b2, b3.
    Uses the crystallographic definition scaled by unit cell volume.
    """
    V = a1.dot(a2.cross(a3))
    if abs(V) < 1e-10:
        raise ValueError("Unit cell volume is zero — lattice vectors are coplanar.")
    b1 = a2.cross(a3) / V
    b2 = a3.cross(a1) / V
    b3 = a1.cross(a2) / V
    return b1, b2, b3


def compute_miller_normal(h, k, l, b1, b2, b3):
    """
    Computes the normal vector to the (hkl) plane.
    g_hkl = h*b1 + k*b2 + l*b3
    """
    g_hkl = h * b1 + k * b2 + l * b3
    if g_hkl.length < 1e-10:
        raise ValueError(f"Miller indices ({h},{k},{l}) produce a zero normal vector.")
    return g_hkl.normalized()


def compute_plane_anchor(h, k, l, origin, a1, a2, a3):
    """
    Computes the anchor point of the (hkl) plane using the intercept definition.
    The plane intercepts a1/h, a2/k, a3/l — uses the first non-zero index.
    """
    if h != 0:
        return origin + a1 / h
    elif k != 0:
        return origin + a2 / k
    elif l != 0:
        return origin + a3 / l
    else:
        raise ValueError("At least one Miller index must be non-zero.")


def compute_plane_size(a1, a2, a3):
    """
    Estimates a reasonable plane size based on the unit cell dimensions.
    Uses the longest lattice vector as the reference size.
    """
    return max(a1.length, a2.length, a3.length) * 1.5


def rotation_from_z_to_normal(normal):
    """
    Computes the Euler rotation needed to align Blender's default plane
    (whose normal is Z) with the target normal vector.
    """
    z_axis = Vector((0, 0, 1))
    angle = z_axis.angle(normal)
    axis = z_axis.cross(normal)

    if axis.length < 1e-10:
        # normal is parallel or anti-parallel to Z
        if normal.dot(z_axis) > 0:
            return (0.0, 0.0, 0.0)  # already aligned
        else:
            return (math.pi, 0.0, 0.0)  # flip 180 degrees around X

    axis.normalize()
    rotation_matrix = axis.to_track_quat('Z', 'Y').to_euler()
    # Use mathutils rotation matrix from axis-angle instead
    import mathutils
    q = mathutils.Quaternion(axis, angle)
    return q.to_euler()


def InstantiateMillerPlane(bound_box_points, h, k, l, mat_dict):
    """
    Renders a semi-transparent plane oriented by Miller indices (hkl).

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
    b1, b2, b3 = compute_reciprocal_vectors(a1, a2, a3)
    normal = compute_miller_normal(h, k, l, b1, b2, b3)
    anchor = compute_plane_anchor(h, k, l, origin, a1, a2, a3)
    size = compute_plane_size(a1, a2, a3)
    euler = rotation_from_z_to_normal(normal)

    print(f"  normal: {normal}")
    print(f"  anchor: {anchor}")
    print(f"  size:   {size}")

    bpy.ops.mesh.primitive_plane_add(
        size=size,
        enter_editmode=False,
        location=anchor
    )

    plane_obj = bpy.context.active_object
    plane_obj.name = f"MillerPlane_{h}{k}{l}"
    plane_obj.rotation_euler = euler

    # Assign material
    mat = mat_dict.get("Yy")
    if mat:
        if plane_obj.data.materials:
            plane_obj.data.materials[0] = mat
        else:
            plane_obj.data.materials.append(mat)
    else:
        print("MillerPlaneBuilder: 'Yy' material not found in mat_dict.")