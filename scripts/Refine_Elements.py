import bpy
from bpy import context
import math
from math import *
import mathutils

def GetElementsPresentInMolecule(list):
    """
    input: list of elements and their xyz coordinates (as string values)
    summary: checks for first value of each entry in list, if symbol present, skip
    output: a list of all the elements present (no repeats)
    """
    l = []
    for entry in list:
        if entry[0] not in l:
            l.append(entry[0])
    return l

def CreateDictionaryWithNamesAndPositions(list, number_of_elements):
    """
    input: list where each row has 4 items: name, and xyz coordinates.
    summary: creates a dictionary, assigns a number to each element, converts xyz into vector
    output: key -> Symbol+number (e.g. C01) value -> Vector3(xyz) !!If a dummy atom is present, is called "?s!!
    note: supports up to 999 elements.
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
    input: atom_dict <dictionary>: contains atom labels with symbols and index, connect_list <list>: list to update
    summary: before this, the connectivity list did not have indexes on their corresponding elements
    output: adds the indexes to the elements involved in specific bonds
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
    gets a smaller list of type <Atom_Data> only for the present elements
    """
    d = {}
    for element in list:
        if ref_dict.get(element):
            d[element] = ref_dict.get(element)
    return d