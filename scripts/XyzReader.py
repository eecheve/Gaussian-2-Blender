# adding this file path to Blender find directory because it was not finding BondOrderCalculator
#filepath = bpy.data.filepath
#dir = os.path.dirname(filepath)
#if not dir in sys.path:
#   sys.path.append(dir)

from BondOrderCalculator import BondOrderCalculator

class XyzReader():
    def __init__(self):
        self.calculator = BondOrderCalculator()

    def extract_coords_from_xyz_file(self, xyz_file_path):
        """
        Extracts atomic data from an XYZ file.

        Reads the file and returns lines with exactly four elements 
        (atom symbol and three coordinates).

        :param xyz_file_path (str): Path to the XYZ file.
        :returns: A list of lines with atom symbol and (x, y, z) coordinates.
        """
        coords = []
        with open(xyz_file_path, 'r') as f:
            for line in f:
                split_line = line.split()
                if len(split_line) == 4:
                    # Convert coordinates to float
                    atom = split_line[0]
                    coordinates = list(map(float, split_line[1:]))
                    coords.append([atom] + coordinates)
        return coords

    def assign_indices(self, raw_coords):
        """
        Returns:
        list: A list of lists with atomic symbols assigned a unique two-digit index.
        """
        for index, entry in enumerate(raw_coords, start=1):
            entry[0] = f"{entry[0]}{index:02d}"
        return raw_coords
    
    def obtain_all_bond_orders(self, raw_coordinates):
        """
        Computes bond orders for each unique pair of atoms using their coordinates.

        Returns:
        list: A list of tuples, where each tuple contains the atom pair, their coordinates,
              and the bond order (if any).
        """
        bond_orders = []
        bond_order_map = {1: '-', 2: '=', 3: '#'}
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