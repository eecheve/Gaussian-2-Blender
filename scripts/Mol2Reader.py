import re
from BondOrderCalculator import BondOrderCalculator

class Mol2Reader():
    def __init__(self):
        self.calculator = BondOrderCalculator()

    def extract_coords_from_mol2_file(self, mol2_file_path):
        """
        Extracts atomic symbols and 3D coordinates from the @<TRIPOS>ATOM section of a .mol2 file.

        :param mol2_file_path: (str) Path to the .mol2 file.
        :return: (list) A list of lists, each containing an atom symbol and its x, y, z coordinates.
        """
        coords = []
        with open(mol2_file_path, 'r') as f:
            lines = f.readlines()
            atom_section = False
            for line in lines:
                if line.startswith("@<TRIPOS>ATOM"):
                    atom_section = True
                    continue
                elif line.startswith("@<TRIPOS>"):
                    atom_section = False
                if atom_section:
                    parts = line.split()
                    if len(parts) >= 6:
                        #atom = parts[1]
                        raw_atom = parts[1] # Remove digits from atom name
                        atom = re.sub(r"\d+", "", raw_atom)
                        x, y, z = map(float, parts[2:5])
                        coords.append([atom, x, y, z])
        return coords

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
            #new_entry[0] = f"{entry[0]}{index:02d}"
            new_entry[0] = f"{entry[0]}{index:0{digits}d}" #to account for molecules between 100 and 999 atoms
            indexed_coords.append(new_entry)
        return indexed_coords

    def obtain_all_bond_orders2(self, raw_coordinates):
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
    
    def obtain_all_bond_orders(self, raw_coordinates, mol2_file_path):
        """
        Extracts bond connections and bond orders from the @<TRIPOS>BOND section of a .mol2 file.

        :param raw_coordinates: (list) List of atoms with their coordinates.
        :param mol2_file_path: (str) Path to the .mol2 file.
        :return: (list) A list of tuples with atom pairs and their bond order symbol (e.g., '-', '=', '#').
        """
        bond_orders = []
        bond_order_map = {'1': '-', '2': '=', '3': '#', 'ar': '%'}

        coords_with_indices = self.assign_indices(raw_coordinates)
        atom_index_map = {i + 1: atom[0] for i, atom in enumerate(coords_with_indices)}

        with open(mol2_file_path, 'r') as f:
            lines = f.readlines()
            bond_section = False
            for line in lines:
                if line.startswith("@<TRIPOS>BOND"):
                    bond_section = True
                    continue
                elif line.startswith("@<TRIPOS>") and bond_section:
                    break
                if bond_section:
                    parts = line.split()
                    if len(parts) >= 4:
                        origin = int(parts[1])
                        target = int(parts[2])
                        bond_type = parts[3]
                        bond_symbol = bond_order_map.get(bond_type, '-')
                        atom1 = atom_index_map.get(origin)
                        atom2 = atom_index_map.get(target)
                        if atom1 and atom2:
                            bond_orders.append((atom1, atom2, bond_symbol))
        return bond_orders
