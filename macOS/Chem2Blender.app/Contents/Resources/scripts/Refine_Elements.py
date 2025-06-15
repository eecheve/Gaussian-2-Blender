import bpy
from bpy import context
import math
from math import *
import mathutils

def GetElementsPresentInMolecule(list):
    """
    Checks for the presence of elements in the molecule and returns a list of unique elements.

    :param list: (list) List of elements and their xyz coordinates (as string values).
    :return: (list) A list of all the elements present (no repeats).
    """
    l = []
    for entry in list:
        if entry[0] not in l:
            l.append(entry[0])
    return l

def CreateDictionaryWithNamesAndPositions(list, number_of_elements):
    """
    Creates a dictionary with element names and their positions.

    :param list: (list) Each row has 4 items: name, and xyz coordinates.
    :param number_of_elements: (int) Number of elements.
    :return: (dict) Dictionary with keys as Symbol+number (e.g., C01) and values as Vector3(xyz).
    """
    if number_of_elements > 999:
        print("@Refine_Elements: Too many atoms, cannot process")
        return {}

    dict = {}
    digits = 3 if number_of_elements >= 100 else 2

    for i, (name, x, y, z) in enumerate(list):
        formatted_index = f"{i+1:0{digits}}"
        element_name = f"{name}{formatted_index}"
        dict[element_name] = mathutils.Vector((x, y, z))
    return dict
            
def AddAtomLabelsToConnectList(atom_dict, connect_list): #<----------------- source of bugs, I think!!!!!
    """
    Adds atom labels with symbols and indexes to the connectivity list.

    :param atom_dict: (dict) Contains atom labels with symbols and indexes.
    :param connect_list: (list) List to update.
    :return: None
    """
    for key in atom_dict:
        key_num = int(''.join(filter(str.isdigit, key))) #removes char from string
        for line in connect_list:
            if line[0] == key_num:
                line[0] = key
            elif line[1] == key_num:
                line[1] = key
                
def GetDataForExistingElements(list, ref_dict):
    """
    Gets a smaller list of type <Atom_Data> only for the present elements.

    :param list: (list) List of elements present.
    :param ref_dict: (dict) Reference dictionary with element data.
    :return: (dict) Dictionary with data for the present elements.
    """
    d = {}
    for element in list:
        if ref_dict.get(element):
            d[element] = ref_dict.get(element)
    return d