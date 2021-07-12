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
    note: supports up to 99 elements.
    """
    dict = {}
    if number_of_elements < 100:
        for i in range(len(list)):
            if i < 9:
                name = list[i][0] + '0' + str(i+1)
            else:
                name = list[i][0] + str(i+1)
            x = list[i][1]
            y = list[i][2]
            z = list[i][3]
            dict[name] = mathutils.Vector((x,y,z))
        return dict
    elif number_of_elements < 1000:
        for i in range(len(list)):
            if i < 9:
                name = list[i][0] + '00' + str(i+1)
            elif i < 99:
                name = list[i][0] + '0' + str(i+1)
            else:
                name = list[i][0] + str(i+1)
            x = list[i][1]
            y = list[i][2]
            z = list[i][3]
            dict[name] = mathutils.Vector((x,y,z))
        return dict
    else:
        print("@Refine_Elements: Too many atoms, cannot process")
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

def RemoveNonSpecifiedIons(ion_dict, ionInputList):
    """
    input: ion_dict <dictionary>: contains the symbols and possible ion radii for all present elements,
    input: ionInputList <list>(string, string, string, string): list of ions with custom properties
    summary: removes from the ion dictionary the elements that were not specified in input list
    output: smaller dictionary
    error output: prints out an error if input list contains an ion non present in dictionary
    """
    d = {}
    for ion in ion_dict:
        for entry in ionInputList:
            if entry[0] in ion_dict:
                if entry[0] == ion:
                    d[ion] = ion_dict.get(ion)
            else:
                print("Error: specified ion for",entry[0],"is not present in molecule, specification will be ignored")
    return d

def RemoveSpecifiedIonsFromElementDict(ion_dict, element_dict):
    """
    input: ion_dict <dictionary>: contains the symbols and the possible radii for specified elements,
    input: element_dict <dictionary>: dictionary off all elements present
    summary: removes specified ions from dict of all elements present
    output: smaller dictionary
    """
    d = {}
    for element in element_dict:
        for ion in ion_dict:
            if ion == element:
                continue
            else:
                d[element] = element_dict.get(element)
    return d