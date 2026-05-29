import re
import bpy

def parse_connection_string(connect_list_string):
    """Splits the input string into a list of cleaned connection entries."""
    return [conn.strip() for conn in connect_list_string.split(';') if conn.strip()]

def build_atom_identity_map(coords):
    """
    Builds a map of atom indices to their element symbols from a list of raw coordinates.

    :param coords: (list) List of [element, x, y, z] entries.
    :return: (dict) Dictionary mapping index strings to element symbols, e.g., {'01': 'C', '02': 'O'}
    """
    identity_map = {}
    for i, entry in enumerate(coords, start=1):
        symbol = entry[0]
        index = f"{i:02d}" # Two-digit index
        identity_map[index] = symbol
    return identity_map

def build_connection_lookup(connect_with_symbols):
    """Creates a dictionary of existing connections using unordered atom pairs as keys."""
    return {frozenset((a, b)): (a, b, bond) for a, b, bond in connect_with_symbols}

def parse_connection_entry(conn):
    """
    Parses a connection entry like 'Fe07-Cl25' into atom1, bond, atom2.
    Assumes bond is a single character.
    """
    for i, char in enumerate(conn):
        if char in "-=#_%":
            atom1 = conn[:i]
            bond = conn[i]
            atom2 = conn[i+1:]
            return atom1, bond, atom2
    raise ValueError(f"Invalid connection format: {conn}")

def validate_atom_identity(atom_label, identity_map):
    """Validates that the atom exists and matches the expected symbol."""
    symbol = ''.join(filter(str.isalpha, atom_label))
    index = ''.join(filter(str.isdigit, atom_label))
    if index not in identity_map:
        raise ValueError(f"Atom index {index} not found in molecule.")
    if identity_map[index] != symbol:
        raise ValueError(f"Atom identity mismatch: expected {identity_map[index]}, got {symbol}.")

def overwrite_connectivity(connect_list_string, connect_with_symbols, coords):
    """
    Updates or appends bond connections based on a user-defined string.
    Validates that atom indices and identities match the current molecule.

    :param connect_list_string: (str) e.g., "Fe07-Cl25; C03=C07"
    :param connect_with_symbols: (list) Existing connectivity list
    :return: (list) Updated connectivity list
    """
    if not connect_list_string.strip():
        return connect_with_symbols

    new_connections = parse_connection_string(connect_list_string)
    if not new_connections:
        return connect_with_symbols

    atom_identity_map = build_atom_identity_map(coords)
    existing_connections = build_connection_lookup(connect_with_symbols)

    for conn in new_connections:
        atom1, bond, atom2 = parse_connection_entry(conn)
        validate_atom_identity(atom1, atom_identity_map)
        validate_atom_identity(atom2, atom_identity_map)

        key = frozenset((atom1, atom2))
        existing_connections[key] = (atom1, atom2, bond)

    print("optional step: overwriting conectivity list")
    return list(existing_connections.values())

# def delete_forbidden_bonds_from_scene(connect_list_string):
#     """
#     Parses the connection override string for no-bond entries (bond character '~'),
#     resolves each entry to its bare element pair by stripping numeric indices and
#     Blender instance suffixes, then deletes every matching bond object from the scene.

#     Works for both type-level ('Fe~Fe') and instance-level ('Fe07~Fe12') entries —
#     both are resolved to element pairs, so deletion is always type-wide.

#     :param connect_list_string: (str) Semicolon-separated connection rules, e.g. "Fe~Fe; C07~N03".
#     :return: (int) Number of bond objects removed from the scene.
#     """
#     BOND_NAME_CHARS = {'_', '-', '=', '#', '%'}

#     def bare_element(atom_label):
#         """Strip Blender suffix (.001) and numeric index, leaving only the element symbol."""
#         base = atom_label.split('.')[0]          # drop .001, .002, etc.
#         match = re.match(r"([A-Za-z]+)", base)
#         return match.group(1) if match else None

#     # Collect forbidden element pairs from '~' entries
#     forbidden_pairs = set()
#     for conn in parse_connection_string(connect_list_string):
#         try:
#             atom1, bond, atom2 = parse_connection_entry(conn)
#         except ValueError:
#             continue
#         if bond != '~':
#             continue
#         elem1 = bare_element(atom1)
#         elem2 = bare_element(atom2)
#         if elem1 and elem2:
#             forbidden_pairs.add(frozenset((elem1, elem2)))

#     if not forbidden_pairs:
#         return 0

#     # Delete every bond object whose endpoint elements form a forbidden pair
#     count = 0
#     for obj in list(bpy.context.scene.objects):
#         if obj.type != 'MESH':
#             continue
#         bond_char = next((c for c in BOND_NAME_CHARS if c in obj.name), None)
#         if bond_char is None:
#             continue
#         parts = obj.name.split(bond_char, 1)
#         if len(parts) != 2:
#             continue
#         elem1 = bare_element(parts[0])
#         elem2 = bare_element(parts[1])
#         if elem1 and elem2 and frozenset((elem1, elem2)) in forbidden_pairs:
#             bpy.data.objects.remove(obj, do_unlink=True)
#             count += 1

#     print(f"delete_forbidden_bonds_from_scene: removed {count} bond object(s)")
#     return count

def delete_forbidden_bonds_from_scene(custom_bond_thresholds):
    """
    Reads custom threshold rules with bond order 0, then deletes every bond
    object from the scene whose endpoint element types match a forbidden pair.

    :param custom_bond_thresholds: (list) Dicts from get_custom_thresholds(),
                                   each with 'atom_pair' and 'bond_order'.
    :return: (int) Number of bond objects removed from the scene.
    """   
    BOND_NAME_CHARS = {'_', '-', '=', '#', '%'}

    def bare_element(atom_label):
        base = atom_label.split('.')[0]
        match = re.match(r"([A-Za-z]+)", base)
        return match.group(1) if match else None

    forbidden_pairs = {
        frozenset(rule["atom_pair"])
        for rule in (custom_bond_thresholds or [])
        if rule.get("bond_order") == 0
    }

    if not forbidden_pairs:
        return 0

    count = 0
    for obj in list(bpy.context.scene.objects):
        if obj.type != 'MESH':
            continue
        bond_char = next((c for c in BOND_NAME_CHARS if c in obj.name), None)
        if bond_char is None:
            continue
        parts = obj.name.split(bond_char, 1)
        if len(parts) != 2:
            continue
        elem1 = bare_element(parts[0])
        elem2 = bare_element(parts[1])
        if elem1 and elem2 and frozenset((elem1, elem2)) in forbidden_pairs:
            bpy.data.objects.remove(obj, do_unlink=True)
            count += 1

    print(f"delete_forbidden_bonds_from_scene: removed {count} bond object(s)")
    return count

def get_forbidden_type_pairs(custom_bond_thresholds):
    """
    Extracts element type pairs designated as bond order 0 from the
    custom threshold rules.

    :param custom_bond_thresholds: (list) Rules from get_custom_thresholds(),
                                   each a dict with 'atom_pair' and 'bond_order'.
    :return: (set) Frozensets of element symbol pairs, e.g. {frozenset({'V', 'V'})}.
    """
    return {
        frozenset(rule["atom_pair"])
        for rule in (custom_bond_thresholds or [])
        if rule.get("bond_order") == 0
    }

def remove_forbidden_bonds_from_connectivity(connect_with_symbols, forbidden_type_pairs):
    """
    Filters connect_with_symbols, removing any entry whose atom type pair
    is in forbidden_type_pairs.

    :param connect_with_symbols: (list) Connectivity list of (atomA, atomB, bond_char) tuples.
    :param forbidden_type_pairs: (set) Output of get_forbidden_type_pairs.
    :return: (list) Filtered connectivity list.
    """
    filtered = []
    for atomA, atomB, bond_char in connect_with_symbols:
        elem1 = re.match(r"([A-Za-z]+)", atomA.split('.')[0]).group(1)
        elem2 = re.match(r"([A-Za-z]+)", atomB.split('.')[0]).group(1)
        if frozenset((elem1, elem2)) not in forbidden_type_pairs:
            filtered.append((atomA, atomB, bond_char))
    return filtered