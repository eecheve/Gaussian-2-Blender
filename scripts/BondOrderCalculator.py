import os
import json
import numpy as np
from typing import List
from typing import Sequence

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

    def get_bond_length_from_coordinates(self, pos1: List[float], pos2: List[float]) -> float:
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

    def calculate_bond_order_threshold(distance:float, references: List[float]) -> List[float]:
        """
        Checks the possible bond distances available for single, double, and triple bonds between two specified bonds

        :param references: (List[float]) The three bond length values (can be NA values if a bond is not found)

        :return: (List[float]) The three threshold values: distance + 10% distance for single bond, and midpoints for double an triple bonds if they exist
        """
        t1 = None
        t2 = None
        t3 = None
        if references[0] is not None:
            t1 = (references[0] * 1.15) #first entry is a 15% leeway for single bond distance
        if references[1] is not None:
            t2 = (references[0] + references[1])/2 #second entry is the midpoint between single and double bond
        if references[2] is not None:
            t3 = (references[1] + references[2])/2 #third entry is the midpoint between triple and double bond
        return [t1, t2, t3]
    
    def compare_distance_to_thresholds(self, distance:float, thresholds: List[float]) -> float:
        """
        Classify bond order based on distance and thresholds

        :return: (int) bond order (None means no bond)
        """
        t_single, t_double, t_triple = thresholds

        if t_triple is not None and distance < t_triple: # Triple bond
            return 3
        
        if t_double is not None and distance < t_double * 0.97: # Double bond 
            return 2
        
        if t_double is not None and t_single is not None:
            arom_lower = t_double * 0.97
            arom_upper = t_double * 1.03
            if arom_lower <= distance < arom_upper:
                return 1.5

        if t_single is not None and distance <= t_single: # Single bond
            return 1

        return None # No bond
              
    def get_bond_order_from_coordinates(self, atom1:str, atom2:str, pos1:Sequence[float], pos2:Sequence[float]):
        """
        Determine the bond order based on the distance between two atoms and their covalent radii.

        :param atom1: (str) The atomic symbol for the first atom.
        :param atom2: (str) The atomic symbol for the second atom.
        :param pos1: (tuple or list) The (x, y, z) coordinates of the first atom.
        :param pos2: (tuple or list) The (x, y, z) coordinates of the second atom.

        :return: (int) The bond order (1 for single, 2 for double, 3 for triple) or None if no bond order is found.
        """
        distance = self.get_bond_length_from_coordinates(pos1, pos2)
        references = self.get_covalent_lengths_for_atoms(atom1, atom2)
        thresholds = self.calculate_bond_order_threshold(references)
        bo = self.compare_distance_to_thresholds(distance, thresholds)
        #if bo is None:
        #    print(f"the distance between {atom1} and {atom2} is too long to render a bond in between")
        return bo

    #TO DEBUG
    # def run(self):
    #     print("**********************************")
        # print("----- C,C -----")
        # cc3 = self.get_bond_order_from_coordinates(atom1="C", atom2="C", pos1=[0,0,-0.597796393], pos2=[0,0,0.597796393])
        # cc2 = self.get_bond_order_from_coordinates(atom1="C", atom2="C", pos1=[-0.2511,0.0016,-0.0110], pos2=[1.0761,0.0016,-0.0090])
        # cc1 = self.get_bond_order_from_coordinates(atom1="C", atom2="C", pos1=[-0.000135749,-0.000316366,-0.753067743], pos2=[0.000135749,0.000316366,0.753067743])
        # print("should be 3:", cc3)
        # print("should be 2:", cc2)
        # print("should be 1:", cc1)
        # print("----- C,O -----")
        # co3 = self.get_bond_order_from_coordinates(atom1="C", atom2="O", pos1=[0,0,0], pos2=[0,0,1.13963257])
        # co2 = self.get_bond_order_from_coordinates(atom1="C", atom2="O", pos1=[0.2239,-0.2815,0.2846], pos2=[1.4875,-0.4601,0.2156])
        # print("should be 3:", co3)
        # print("should be 2:", co2)
        # print("----- C,N -----")
        # cn3 = self.get_bond_order_from_coordinates(atom1="C", atom2="N", pos1=[1.47140000,2.60590000,-0.53680000], pos2=[2.61960000,2.63730000,-0.52260000])
        # cn2 = self.get_bond_order_from_coordinates(atom1="C", atom2="N", pos1=[0.2239,-0.2815,0.2846], pos2=[1.4875,-0.4601,0.2156])
        # cn1 = self.get_bond_order_from_coordinates(atom1="C", atom2="N", pos1=[0.9707,1.1614,1.1860], pos2=[-0.0577,2.2053,1.1051])
        # print("should be 3:", cn3)
        # print("should be 2:", cn2)
        # print("should be 1:", cn1)

# TO DEBUG
# if __name__ == "__main__":
#      test = BondOrderCalculator()
#      test.run()