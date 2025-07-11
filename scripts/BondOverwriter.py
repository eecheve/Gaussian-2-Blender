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