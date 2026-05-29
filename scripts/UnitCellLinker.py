import bpy
import re
import itertools
import numpy as np
from BondOrderCalculator import BondOrderCalculator


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


def get_primitive_atoms(atoms_in_scene):
    """
    Filters atoms_in_scene to only the primitive-cell atoms — those without
    a Blender duplication suffix (i.e., no '.' in the name).

    :param atoms_in_scene: (dict) Full atom dict from collect_atoms_from_scene.
    :return: (dict) Subset containing only primitive-cell atoms.
    """
    return {name: pos for name, pos in atoms_in_scene.items() if '.' not in name}


def group_atom_instances(atoms_in_scene):
    """
    Groups all scene atom names by their base name — the part before the first '.'.
    For example, 'C01', 'C01.001', and 'C01.002' all map to base 'C01'.

    :param atoms_in_scene: (dict) Full atom dict from collect_atoms_from_scene.
    :return: (dict) {base_name (str): [list of instance names (str)]}
    """
    groups = {}
    for name in atoms_in_scene.keys():
        base = name.split('.')[0]
        groups.setdefault(base, []).append(name)
    return groups


def find_periodic_bond_types(primitive_atoms, lattice_vectors, calculator, tolerance_ratio=0.1):
    """
    Identifies inter-cell bond types by generating image positions of each
    primitive atom in all 26 neighboring cells and checking for bonds via
    BondOrderCalculator. Works entirely on the primitive cell — O(26 * n^2)
    where n is the number of atoms in the primitive cell.

    :param primitive_atoms: (dict) Primitive-cell atoms from get_primitive_atoms.
    :param lattice_vectors: (tuple) Three Cartesian lattice vectors (each array-like, length 3).
    :param calculator: (BondOrderCalculator) Instance used for bond detection.
    :param tolerance_ratio: (float) Not used here; reserved for consistency with downstream calls.
    :return: (list) Tuples of (atomA, atomB, bond_char, ref_dist) for each
             detected inter-cell bond type.
    """
    bond_order_map = {1: '-', 1.5: '%', 2: '=', 3: '#'}
    v1, v2, v3 = [np.array(v) for v in lattice_vectors]

    neighbor_offsets = [
        (i, j, k)
        for i, j, k in itertools.product([-1, 0, 1], repeat=3)
        if not (i == 0 and j == 0 and k == 0)
    ]

    periodic_bonds = []
    seen = set()
    items = list(primitive_atoms.items())

    for nameA, posA in items:
        elemA = re.match(r"([A-Za-z]+)", nameA).group(1)
        posA_arr = np.array(posA)

        for nameB, posB in items:
            elemB = re.match(r"([A-Za-z]+)", nameB).group(1)
            posB_arr = np.array(posB)

            for i, j, k in neighbor_offsets:
                posB_image = posB_arr + i * v1 + j * v2 + k * v3
                bond_order = calculator.get_bond_order_from_coordinates(
                    elemA, elemB, tuple(posA_arr), tuple(posB_image)
                )
                if bond_order is not None:
                    # Use a directed key so (A→B at +x) and (B→A at -x) are not duplicated
                    key = frozenset(((nameA, 0, 0, 0), (nameB, i, j, k)))
                    if key not in seen:
                        seen.add(key)
                        ref_dist = float(np.linalg.norm(posB_image - posA_arr))
                        bond_char = bond_order_map.get(bond_order)
                        periodic_bonds.append((nameA, nameB, bond_char, ref_dist))

    print(f"find_periodic_bond_types: {len(periodic_bonds)} inter-cell bond type(s) detected")
    return periodic_bonds


def find_replicated_bonds(periodic_bond_types, atoms_in_scene, atom_groups, tolerance_ratio=0.1):
    """
    For each inter-cell bond type, searches the replicated scene for all instance
    pairs whose distance matches the reference distance within tolerance.
    Same-copy pairs (instances sharing a Blender suffix) are skipped, as their
    intra-cell bonds were already created during replication.

    :param periodic_bond_types: (list) Output of find_periodic_bond_types.
    :param atoms_in_scene: (dict) Full atom dict from collect_atoms_from_scene.
    :param atom_groups: (dict) Output of group_atom_instances.
    :param tolerance_ratio: (float) Distance tolerance as a fraction of the reference distance.
    :return: (list) Tuples of (atomA_instance, atomB_instance, bond_char).
    """
    replicated_bonds = []
    seen = set()

    for nameA, nameB, bond_char, ref_dist in periodic_bond_types:
        baseA = nameA.split('.')[0]
        baseB = nameB.split('.')[0]
        tol = ref_dist * tolerance_ratio

        groupA = atom_groups.get(baseA, [])
        groupB = atom_groups.get(baseB, [])

        for instA in groupA:
            suffA = instA.split('.')[1] if '.' in instA else ''
            for instB in groupB:
                suffB = instB.split('.')[1] if '.' in instB else ''
                if suffA == suffB:       # same copy — bond already exists
                    continue
                key = frozenset((instA, instB))
                if key in seen:
                    continue
                posA = atoms_in_scene.get(instA)
                posB = atoms_in_scene.get(instB)
                if posA is None or posB is None:
                    continue
                d = (posB - posA).length
                if abs(d - ref_dist) <= tol:
                    replicated_bonds.append((instA, instB, bond_char))
                    seen.add(key)

    return replicated_bonds


def replicate_primitive_bonds(lattice_vectors, tolerance_ratio=0.1):
    """
    Main entry point for UnitCellLinker. Detects all inter-cell bonds in the
    replicated Blender scene using an image-atom approach on the primitive cell.

    Steps:
      1. Collect all atoms from the scene.
      2. Isolate the primitive-cell atoms (no Blender suffix).
      3. Generate images in all 26 neighboring cells; detect inter-cell bond types
         via BondOrderCalculator — no assumption about pre-existing bond pairs.
      4. Search replicated instances for pairs matching each bond type by distance.

    :param lattice_vectors: (tuple) Three Cartesian lattice vectors (each array-like, length 3),
                            typically unit_cell_points[1:4].
    :param tolerance_ratio: (float) Distance tolerance as a fraction of the reference distance.
                            Default 0.1.
    :return: (dict) {
               'atoms_in_scene': {name: Vector},
               'replicated_bonds': [(atomA, atomB, bond_char), ...]
             }
    """
    calculator = BondOrderCalculator()
    atoms_in_scene = collect_atoms_from_scene()
    primitive_atoms = get_primitive_atoms(atoms_in_scene)
    atom_groups = group_atom_instances(atoms_in_scene)

    periodic_bond_types = find_periodic_bond_types(
        primitive_atoms, lattice_vectors, calculator, tolerance_ratio
    )
    replicated_bonds = find_replicated_bonds(
        periodic_bond_types, atoms_in_scene, atom_groups, tolerance_ratio
    )
    return {"atoms_in_scene": atoms_in_scene, "replicated_bonds": replicated_bonds}