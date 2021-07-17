import bpy
import sys
import os

from bpy import context
import math
from math import *
import mathutils

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Atom_Data

import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Atom_Data)

def CreateIonDataFromInput(ionInputList):
    """
    input: ionInputList <list>(string, string, string, string): list of ions to specify and their properties
    summary: takes values in each entry of the ionInputList and makes a IonDataDict
    output: dictionary<string, Ionic>: dict of Ionic class wich contains info with no radius value
    """
    d = {}
    for ionInput in ionInputList:
        symbol = ionInput[0]
        charge = int(ionInput[1])
        coordination = ionInput[2]
        d[symbol] = Atom_Data.Ionic(charge, coordination, 0.0)
    return d

def GetIonPositions(names_and_pos, ion_input):
    """
    input: names_and_pos dict<string, Vector3>: dictionary that contains the position of each labelled element present.
    input: ion_input dict<string, Ionic>: dict of Ionic class wich contains info with no radius value
    output: dict<string, Vector3>: refined dict with only the ions from the ion_input dict
    """
    d = names_and_pos.copy()
    for element_num in names_and_pos:
        element = ''.join([i for i in element_num if not i.isdigit()]) #removes int from string
        if element not in ion_input:
            del d[element_num]
    return d

def RemoveNonSpecifiedIons(ion_dict, ion_input):
    """
    input: ion_dict <dictionary>: contains the symbols and possible ion radii for all present elements,
    input: ion_input dict<string, Ionic>: dict of Ionic class wich contains info with no radius value
    summary: removes from the ion dictionary the elements that were not specified in input list
    output: smaller dictionary
    error output: prints out an error if input list contains an ion non present in dictionary
    error output: prints out an error if ion_input is empty
    """
    d = {}
    for ion_num in ion_dict:
        ion = ''.join([i for i in ion_num if not i.isdigit()]) #removes int from string
        if not ion_input:
            print("Error: no ion specification received")
            return ion_dict
        else:
            for entry in ion_input:
                if entry in ion_dict:
                    if entry == ion:
                        d[ion] = ion_dict.get(ion)
                else:
                    print("Error: specified ion for",entry,"is not present in molecule, specification will be ignored")
    return d

def RemoveSpecifiedIonsFromElementDict(ion_dict, element_dict):
    """
    input: ion_dict <dictionary>: contains the symbols and the possible radii for specified elements,
    input: element_dict <dictionary>: dictionary off all elements present
    summary: removes specified ions from dict of all elements present
    output: smaller dictionary
    """
    d = element_dict.copy()
    for element_num in element_dict:
        element = ''.join([i for i in element_num if not i.isdigit()]) #removes int from string
        if element in ion_dict:
            del d[element_num]
    if len(d) == len(element_dict):
        print("5: none of the specified ions is present in the molecule")
    return d

def GetIonDataFromInput(ion_data_dict, ion_input):
    """
    input: ion_dict <dictionary>: contains the symbols and possible ionic radii for elements of interest
    input: ion_input dict<string, Ionic>: dict of Ionic class wich contains info with no radius value
    summary: gets the correct ionic radii data set from the ionInputList for each element in ion_dict
    output: dictionary<string, float>: Element symbol and their ionic radius
    """
    for ion in ion_input:
        symbol = ion
        charge = ion_input[ion].charge
        coordination = ion_input[ion].coordination
        for key in ion_data_dict:
            ion_data_list = ion_data_dict[key]
            for ion_data in ion_data_list:
                if ion_data.charge == charge and ion_data.coordination == coordination:
                    ion_input[ion].set_radius(ion_data.radius)

    
    
            


