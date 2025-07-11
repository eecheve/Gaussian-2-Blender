from BondOrderCalculator import BondOrderCalculator

class XyzReader():
    def __init__(self):
        self.calculator = BondOrderCalculator()

    def extract_coords_from_xyz_file(self, xyz_file_path):
        """
        Extracts the first set of atomic coordinates from an XYZ file, whether it's a single-molecule
        or a trajectory file.

        :param xyz_file_path: (str) Path to the XYZ file.
        :return: A list of [atom, x, y, z] entries for the first set of coordinates.
        """
        coords = []
        with open(xyz_file_path, 'r') as f:
            lines = f.readlines()

        if not lines:
            return coords  # Empty file

        try:
            num_atoms = int(lines[0].strip())
        except ValueError:
            raise ValueError("First line of the file must be the number of atoms.")

        # Ensure there are enough lines for at least one full set
        if len(lines) < num_atoms + 2:
            raise ValueError("File does not contain enough lines for one full coordinate set.")

        # Extract the first set of coordinates
        for line in lines[2:2 + num_atoms]:
            split_line = line.split()
            if len(split_line) == 4:
                atom = split_line[0]
                coords.append([atom] + list(map(float, split_line[1:])))
        
        return coords


    def assign_indices(self, raw_coords):
        """
        Assigns unique two-digit indices to atomic symbols.

        :param raw_coords: (list) List of raw coordinates.
        :return: (list) A list of lists with atomic symbols assigned a unique two-digit index.
        """
        indexed_coords = []
        for index, entry in enumerate(raw_coords, start=1):
            new_entry = entry.copy()  # Copy the original entry to avoid modifying it
            new_entry[0] = f"{entry[0]}{index:02d}"
            indexed_coords.append(new_entry)
        return indexed_coords
    
    def obtain_all_bond_orders(self, raw_coordinates):
        """
        Computes bond orders for each unique pair of atoms using their coordinates.

        :param raw_coordinates: (list) List of raw coordinates.
        :return: (list) A list of tuples, where each tuple contains the atom pair, their coordinates, and the bond order (if any).
        """
        bond_orders = []
        bond_order_map = {1: '-', 1.5: '%', 2: '=', 3: '#'}
        coords_with_indices = self.assign_indices(raw_coordinates)
        num_atoms = len(coords_with_indices)
        for i in range(num_atoms):
            atom1, x1, y1, z1 = coords_with_indices[i]
            for j in range(i + 1, num_atoms):
                atom2, x2, y2, z2 = coords_with_indices[j]
                bond_order = self.calculator.get_bond_order_from_coordinates(
                    atom1[:-2], atom2[:-2], (float(x1), float(y1), float(z1)), (float(x2), float(y2), float(z2))
                )
                if bond_order is not None:
                    bond_order_char = bond_order_map.get(bond_order)
                    bond_orders.append((atom1, atom2, bond_order_char))
        return bond_orders
    
#if __name__ == "__main__":
#     test = XyzReader()
#     raw_coords = test.extract_coords_from_xyz_file(
#         "C:\\Documents\\Gaussian-2-Blender\\input_examples\\xyz_files\\2-cyano-2-aminoaceticacid.xyz")
#     all_bo = test.obtain_all_bond_orders(raw_coords)
#     print(all_bo)