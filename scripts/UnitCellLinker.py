import bpy
from mathutils import Vector


def collect_atoms_from_scene():
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


def get_bond_reference_distances(connect_with_symbols, atoms_in_scene):
    reference_bonds = []
    for atomA, atomB, bond_char in connect_with_symbols:
        posA = atoms_in_scene.get(atomA)
        posB = atoms_in_scene.get(atomB)
        if posA is None or posB is None:
            continue
        d0 = (posB - posA).length
        reference_bonds.append((atomA, atomB, bond_char, d0))
    return reference_bonds


def group_atom_instances(atoms_in_scene):
    groups = {}
    for name in atoms_in_scene.keys():
        base = name.split('.')[0]
        groups.setdefault(base, []).append(name)
    return groups


def find_replicated_bonds(reference_bonds, atoms_in_scene, atom_groups, tolerance_ratio=0.1):
    replicated_bonds = []
    seen = set()

    print(f"\n--- find_replicated_bonds DEBUG ---")
    print(f"Total atoms in scene: {len(atoms_in_scene)}")
    print(f"Atom groups: {atom_groups}")
    print(f"Reference bonds: {reference_bonds}")

    for atomA_base, atomB_base, bond_char, ref_dist in reference_bonds:
        tol = ref_dist * tolerance_ratio
        groupA = atom_groups.get(atomA_base, [])
        groupB = atom_groups.get(atomB_base, [])

        print(f"\nChecking primitive bond: {atomA_base}-{atomB_base}, ref_dist={ref_dist:.4f}, tol={tol:.4f}")
        print(f"  groupA: {groupA}")
        print(f"  groupB: {groupB}")

        for atomA in groupA:
            for atomB in groupB:
                if atomA == atomA_base and atomB == atomB_base:
                    continue
                key = frozenset((atomA, atomB))
                if key in seen:
                    continue
                posA = atoms_in_scene.get(atomA)
                posB = atoms_in_scene.get(atomB)
                if posA is None or posB is None:
                    continue
                d = (posB - posA).length
                print(f"  {atomA} - {atomB}: dist={d:.4f}, ref={ref_dist:.4f}, diff={abs(d-ref_dist):.4f}, tol={tol:.4f}, match={abs(d - ref_dist) <= tol}")
                if abs(d - ref_dist) <= tol:
                    replicated_bonds.append((atomA, atomB, bond_char))
                    seen.add(key)

    print(f"\nReplicated bonds found: {replicated_bonds}")
    print(f"--- END DEBUG ---\n")
    return replicated_bonds

def replicate_primitive_bonds(connect_with_symbols, primitive_positions=None, tolerance_ratio=0.1):
    atoms_in_scene = collect_atoms_from_scene()
    atom_groups = group_atom_instances(atoms_in_scene)
    reference_bonds = get_bond_reference_distances(connect_with_symbols, atoms_in_scene)
    replicated_bonds = find_replicated_bonds(reference_bonds, atoms_in_scene, atom_groups, tolerance_ratio)
    return {"atoms_in_scene": atoms_in_scene, "replicated_bonds": replicated_bonds}