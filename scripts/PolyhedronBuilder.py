import bpy
import bmesh
import re
from mathutils import Vector


# --------------------------------------------------------------------------- #
#  Scene helpers                                                               #
# --------------------------------------------------------------------------- #

def collect_atoms_from_scene():
    """
    Scans the active Blender scene and returns all mesh objects identified as atoms.
    Atoms are recognised by having at least one letter and one digit in their name,
    and by containing none of the bond-character symbols.

    :return: (dict) {atom_name (str): world-space position (Vector)}
    """
    BOND_NAME_CHARS = {'_', '-', '=', '#', '%'}
    atoms = {}
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        if any(c in obj.name for c in BOND_NAME_CHARS):
            continue
        has_letter = any(c.isalpha() for c in obj.name)
        has_digit  = any(c.isdigit() for c in obj.name)
        if not (has_letter and has_digit):
            continue
        atoms[obj.name] = obj.matrix_world.translation.copy()
    return atoms


def get_element(atom_name):
    """
    Extracts the bare element symbol from an atom name by stripping
    the Blender instance suffix and numeric index.
    Examples: 'Fe07' -> 'Fe', 'V03.001' -> 'V'.

    :param atom_name: (str) Full atom name from the scene.
    :return: (str) Element symbol.
    """
    base = atom_name.split('.')[0]
    match = re.match(r"([A-Za-z]+)", base)
    return match.group(1) if match else None


def get_neighbors(center_name, connect_with_symbols, atoms_in_scene):
    """
    Returns all neighbor atom names for the given center instance.
    For replicated instances (names containing '.'), intra-cell bonds are
    derived from the primitive's bonds by mapping the suffix, since those
    bonds are never explicitly added to connect_with_symbols.

    :param center_name: (str) Full name of the center atom instance.
    :param connect_with_symbols: (list) Tuples of (atomA, atomB, bond_char).
    :param atoms_in_scene: (dict) All atoms currently in the scene.
    :return: (list) Names of all neighbor atoms present in the scene.
    """
    neighbors = set()

    # Direct lookup — catches primitive intra-cell bonds and all inter-cell bonds
    for atomA, atomB, _ in connect_with_symbols:
        if atomA == center_name:
            neighbors.add(atomB)
        elif atomB == center_name:
            neighbors.add(atomA)

    # For replicated instances, intra-cell bonds don't exist in connect_with_symbols.
    # Derive them from the primitive's intra-cell bonds by applying the same suffix.
    if '.' in center_name:
        primitive = center_name.split('.')[0]       # e.g. 'V01'
        suffix    = center_name.split('.', 1)[1]    # e.g. '001'

        for atomA, atomB, _ in connect_with_symbols:
            if '.' in atomA or '.' in atomB:
                continue  # skip inter-cell bonds, only want primitive intra-cell
            if atomA == primitive:
                mapped = atomB + '.' + suffix
                if mapped in atoms_in_scene:
                    neighbors.add(mapped)
            elif atomB == primitive:
                mapped = atomA + '.' + suffix
                if mapped in atoms_in_scene:
                    neighbors.add(mapped)

    return [n for n in neighbors if n in atoms_in_scene]


def build_convex_hull_mesh(vertices, name):
    """
    Creates a Blender mesh object from a set of points using bmesh's
    convex hull operator. The result is the outer shell of the polyhedron
    formed by the given vertices.

    :param vertices: (list) List of Vector positions (the neighbor atom positions).
    :param name: (str) Name for the new Blender object.
    :return: (bpy.types.Object) The created mesh object, or None if hull failed.
    """
    if len(vertices) < 3:
        print(f"PolyhedronBuilder: '{name}' has fewer than 3 neighbors — skipping.")
        return None

    bm = bmesh.new()
    bm_verts = [bm.verts.new(v) for v in vertices]

    try:
        result = bmesh.ops.convex_hull(bm, input=bm_verts)
    except Exception as e:
        print(f"PolyhedronBuilder: convex hull failed for '{name}': {e}")
        bm.free()
        return None

    # Remove geometry that ended up inside the hull (unused verts/edges)
    geom_interior = result.get("geom_interior", [])
    for elem in geom_interior:
        if isinstance(elem, bmesh.types.BMVert):
            bm.verts.remove(elem)

    mesh = bpy.data.meshes.new(name)
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm.to_mesh(mesh)
    bm.free()

    return obj


def assign_material(obj, element, mat_dict, alpha=0.3):
    """
    Creates a node-based transparent material derived from the center element's
    diffuse color and assigns it to the polyhedron object.

    :param obj: (bpy.types.Object) The polyhedron mesh object.
    :param element: (str) Element symbol of the center atom.
    :param mat_dict: (dict) Materials dictionary keyed by element symbol.
    :param alpha: (float) Transparency — 0.0 fully transparent, 1.0 opaque.
    :return: None
    """
    original = mat_dict.get(element)
    if not original:
        print(f"PolyhedronBuilder: no material found for '{element}' in mat_dict.")
        return

    mat_name = f"{element}_polyhedron_mat"
    poly_mat = bpy.data.materials.get(mat_name)

    if poly_mat is None:
        poly_mat = bpy.data.materials.new(name=mat_name)
        poly_mat.use_nodes = True
        poly_mat.blend_method = 'BLEND'

        r, g, b, _ = original.diffuse_color
        bsdf = poly_mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
            bsdf.inputs["Alpha"].default_value = alpha

    obj.data.materials.append(poly_mat)


def BuildPolyhedra(polyhedra_centers, connect_with_symbols, mat_dict):
    """
    Builds coordination polyhedra for every instance of each specified
    center element type. For each center atom, the positions of its bonded
    neighbors are used as vertices of a convex hull mesh.

    Guards:
      - Does nothing if polyhedra_centers is empty.
      - Skips individual center atoms with fewer than 3 neighbors.

    :param polyhedra_centers: (list) Element symbols to treat as centers,
                              e.g. ['V', 'Fe']. Empty list = do nothing.
    :param connect_with_symbols: (list) Full connectivity list of
                                 (atomA, atomB, bond_char) tuples, including
                                 inter-cell bonds from Link_Unit_Cells.
    :param mat_dict: (dict) Materials dictionary keyed by element symbol.
    :return: None
    """
    if not polyhedra_centers:
        print("PolyhedronBuilder: no center atoms specified — skipping.")
        return

    center_set = set(polyhedra_centers)
    atoms_in_scene = collect_atoms_from_scene()

    built = 0
    skipped_too_few_neighbors = 0
    for atom_name, atom_pos in atoms_in_scene.items():
        element = get_element(atom_name)
        if element not in center_set:
            continue

        neighbor_names = get_neighbors(atom_name, connect_with_symbols, atoms_in_scene)
        neighbor_positions = [
            atoms_in_scene[n] for n in neighbor_names if n in atoms_in_scene
        ]

        if len(neighbor_positions) < 3:
            skipped_too_few_neighbors += 1
            continue

        poly_name = f"{atom_name}_polyhedron"
        obj = build_convex_hull_mesh(neighbor_positions, poly_name)
        if obj:
            assign_material(obj, element, mat_dict)
            built += 1

    print(f"PolyhedronBuilder: {built} polyhedron/a instantiated "
          f"({skipped_too_few_neighbors} center atom(s) skipped for having fewer than 3 neighbors).")