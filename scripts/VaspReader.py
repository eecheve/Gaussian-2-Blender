import re
from BondOrderCalculator import BondOrderCalculator

class VaspReader():
    def __init__(self):
        self.calculator = BondOrderCalculator()

    
    def get_file_info_as_list(self, vasp_file_path, encoding='utf-8'):
        """Return a list of token lists, splitting each line on any whitespace."""
        with open(vasp_file_path, 'r', encoding=encoding) as f:
            return [line.strip().split() for line in f]
  
    def get_atoms_in_file(self, file_as_lines):
        """
        Extracts the identities and quantities of the atoms in the crystalline structure. 

        :param asp_file_path: (str) Path to the .vasp file.
        :return: (list) of the form [(atomicSimbol, numberOfAtomsOfTheType)]
        """
        atoms_in_file = []
        line_with_atoms = file_as_lines[5]
        line_with_quantities = file_as_lines[6]
        for i in range(0, len(line_with_atoms)):
                entry = (line_with_atoms[i], int(line_with_quantities[i]))
                atoms_in_file.append(entry)            
        return atoms_in_file
    
    def detect_coordinate_section(self, file_as_lines):
        """
        Determine the coordinate type ('direct' or 'cartesian') and the starting
        index for the coordinates block in a POSCAR/CONTCAR-like file.
        """
        # Ensure line 7 exists and is not empty
        if len(file_as_lines) <= 7 or not file_as_lines[7]:
            raise ValueError("Unexpected empty or missing line at index 7; "
                            "cannot determine coordinate section.")

        line7_first = file_as_lines[7][0].lower()

        # Case 1: "Selective Dynamics" present
        if line7_first.startswith("select"):  # e.g., "Selective" or "Selective_Dynamics"
            # Ensure the next line with coord type exists
            if len(file_as_lines) <= 8 or not file_as_lines[8]:
                raise ValueError("Missing coordinate type after 'Selective Dynamics'.")
            coord_type = file_as_lines[8][0].lower()
            start_idx = 9  # coordinates start after the coord type line
        else:
            # Case 2: Direct/Cartesian given directly on line 7
            coord_type = line7_first
            start_idx = 8  # coordinates start right after this line

        # Optional validation
        if coord_type not in ("direct", "cartesian"):
            raise ValueError(f"Unrecognized coordinate type: {coord_type!r} "
                            "(expected 'Direct' or 'Cartesian').")

        return coord_type, start_idx
    
    def get_coordinate_lines(self, atoms_in_file, file_as_lines):
        total_atoms = sum(count for _, count in atoms_in_file) # Get total number of atoms
        coord_type, start_idx = self.detect_coordinate_section(file_as_lines) # Detect coord type and starting index
        # Slice the coordinate block
        end_idx = start_idx + total_atoms
        coords = file_as_lines[start_idx:end_idx]
        return coords  
    
    def parse_xyz(self, tokens, convert_numbers=True):
            if len(tokens) < 3:
                raise ValueError(f"Coordinate row has fewer than 3 values: {tokens}")
            x, y, z = tokens[0], tokens[1], tokens[2]
            if convert_numbers:
                try:
                    x = float(x); y = float(y); z = float(z)
                except ValueError as e:
                    raise ValueError(f"Non-numeric coordinate encountered: {tokens}") from e
            return x, y, z

    def extract_coords_from_vasp_file(self, file_path):
        """
        Extract atomic symbols and 3D coordinates from a VASP POSCAR/CONTCAR-like file.
        Returns a list of rows: ["Symbol", x, y, z].
        """
        file_as_list = self.get_file_info_as_list(file_path)
        atoms_in_file = self.get_atoms_in_file(file_as_list)
        coords_list = self.get_coordinate_lines(atoms_in_file, file_as_list)
        coords_with_symbols = self.merge_atoms_and_coordinates(atoms_in_file, coords_list)
        return coords_with_symbols
    
    
    def merge_atoms_and_coordinates(self, atoms_in_file, coords_list):
        """
        Extracts atomic symbols and 3D coordinates from the @<TRIPOS>ATOM section of a .mol2 file.

        :param vasp_file_path: (str) Path to the .vasp file.
        :return: (list) A list of lists, each containing an atom symbol and its x, y, z coordinates.
        """
        coords_with_atoms = []
        
        # 1) Expand symbols by count: [("V",4),("H",4)] -> ["V","V","V","V","H","H","H","H"]
        symbol_sequence = []
        for symbol, count in atoms_in_file:
            symbol_sequence.extend([symbol] * int(count))

        total_atoms = len(symbol_sequence)
        if total_atoms != len(coords_list):
            raise ValueError(
                f"Atom count ({total_atoms}) does not match number of coordinate rows "
                f"({len(coords_list)})."
            )

        for i, row in enumerate(coords_list):
                symbol = symbol_sequence[i]
                x, y, z = self.parse_xyz(row)
                merged = [symbol, x, y, z]
                coords_with_atoms.append(merged)

        return coords_with_atoms

    def assign_indices(self, raw_coords):
        """
        Assigns unique two-digit indices to atomic symbols.

        :param raw_coords: (list) List of raw coordinates.
        :return: (list) A list of lists with atomic symbols assigned a unique two-digit index.
        """
        num_atoms = len(raw_coords)
        digits = 3 if num_atoms >= 100 else 2
        indexed_coords = []
        for index, entry in enumerate(raw_coords, start=1):
            new_entry = entry.copy()
            new_entry[0] = f"{entry[0]}{index:0{digits}d}" #to account for molecules between 100 and 999 atoms
            indexed_coords.append(new_entry)
        return indexed_coords

    def obtain_all_bond_orders(self, raw_coordinates):
        """
        Computes bond orders between all unique atom pairs using their coordinates.

        :param raw_coordinates: (list) List of atoms with their coordinates.
        :return: (list) A list of tuples with atom pairs and their bond order symbol (i.e., '-', '=', '#').
        """
        bond_orders = []
        bond_order_map = {1: '-', 1.5:'%',  2: '=', 3: '#'}
        coords_with_indices = self.assign_indices(raw_coordinates)
        num_atoms = len(coords_with_indices)
        for i in range(num_atoms):
            atom1, x1, y1, z1 = coords_with_indices[i]
            for j in range(i + 1, num_atoms):
                atom2, x2, y2, z2 = coords_with_indices[j]
                elem1 = re.match(r"([A-Za-z]+)", atom1).group(1) #regular expression to remove numerical indices from atom name
                elem2 = re.match(r"([A-Za-z]+)", atom2).group(1) #regular expression to remove numerical indices from atom name
                bond_order = self.calculator.get_bond_order_from_coordinates(
                    elem1, elem2, (float(x1), float(y1), float(z1)), (float(x2), float(y2), float(z2))
                )
                if bond_order is not None:
                    bond_order_char = bond_order_map.get(bond_order)
                    bond_orders.append((atom1, atom2, bond_order_char))
        return bond_orders