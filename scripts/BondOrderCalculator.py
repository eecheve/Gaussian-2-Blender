import os
import json
import numpy as np

class BondOrderCalculator():
    def __init__(self):
        self.covalent_radii_json = self.initialize_covalent_radii()

    def initialize_covalent_radii(self):
        """
        Loads covalent radii data from a JSON file.
        The file is located in the 'external_data' directory, relative to the 
        script's location.

        :return: (dict{str:float}) Covalent radii data.
        """
        script_dir = os.path.dirname(__file__) # Get the directory of the current script
        json_file_path = os.path.join(script_dir, '..', 'external_data', 'covalent_radii.json') # Construct the path to the JSON file
        with open(json_file_path, 'r') as json_file:
            return json.load(json_file)

    def get_covalent_lengths_for_atoms(self, atom1, atom2):
        """
        Retrieve and sum the covalent radii values for the given atoms.

        :param atom1: (str) The atomic symbol for the first atom.
        :param atom2: (str) The atomic symbol for the second atom.

        :returns: ([float, float, float]) A list containing the summed covalent radii values for single, double, and triple bonds.
                 If any value is '-', it will be represented as None in the result.
        """
        # Read the json variable and search for the string atom1 (or atom2)
        list1 = self.covalent_radii_json.get(atom1, [None, None, None])
        list2 = self.covalent_radii_json.get(atom2, [None, None, None])

        result = []
        for val1, val2 in zip(list1, list2): # Add the values from list1 and list2
            if val1 == '-' or val2 == '-':
                result.append(None)
            else:
                result.append(val1 + val2 if val1 is not None and val2 is not None else None)

        return result

    def get_bond_length_from_coordinates(self, pos1, pos2):
        """
        Calculate the distance between two points in Cartesian space.

        :param pos1: ([float, float, float]) The (x, y, z) coordinates of the first point.
        :param pos2: ([float, float, float]) The (x, y, z) coordinates of the second point.
        :return: (float) The distance between the two points.
        """
        r1 = np.array(pos1)
        r2 = np.array(pos2)
        v = r2 - r1
        return np.linalg.norm(v)

    def get_bond_order_from_coordinates(self, atom1, atom2, pos1, pos2, threshold=0.1):
        """
        Determine the bond order based on the distance between two atoms and their covalent radii.

        :param atom1: (str) The atomic symbol for the first atom.
        :param atom2: (str) The atomic symbol for the second atom.
        :param pos1: (tuple or list) The (x, y, z) coordinates of the first atom.
        :param pos2: (tuple or list) The (x, y, z) coordinates of the second atom.
        :param threshold: (float) The threshold value to determine the bond order.

        :return: (int) The bond order (1 for single, 2 for double, 3 for triple) or None if no bond order is found.
        """
        distance = self.get_bond_length_from_coordinates(pos1, pos2)
        references = self.get_covalent_lengths_for_atoms(atom1, atom2)

        
        # Check for intermediate bond order (1.5)
        if references[0] is not None and references[1] is not None: #if each atoms has info for single and double bonds
            avg_1_2 = (references[0] + references[1]) / 2 #getting the average between single and double
            if abs(distance - avg_1_2) < threshold: #if the average +- distance is smaller than threshold
                return 1.5 #assign aromatic bond order

        # Check for other bond orders
        for i, ref in enumerate(references):
            if ref is not None and abs(ref - distance) < threshold:
                return i + 1  # Return the bond order (1 for single, 2 for double, 3 for triple)

        print(f"get_bond_order_from_coordinates error: the distance between {atom1} and {atom2} is too long to render a bond in between")
        return None  # Return None if no bond order is found

    #TO DEBUG
    #def run(self):
    #    bond_order = self.get_bond_order_from_coordinates(atom1="C", atom2="H", pos1=[0,0,0], pos2=[0.00000,0.00000,1.08900])
    #    print(bond_order)

# TO DEBUG
#if __name__ == "__main__":
#     test = BondOrderCalculator()
#     test.run()