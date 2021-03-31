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
import Import_Data
import Refine_Data
import Refine_Elements
import Create_Materials
import Primitives
import Export_Data

#Please contact eecheve@ncsu.edu if you plan to extend this program's functionality 
import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Atom_Data)
importlib.reload(Import_Data)
importlib.reload(Refine_Data)
importlib.reload(Refine_Elements)
importlib.reload(Create_Materials)
importlib.reload(Primitives)
importlib.reload(Export_Data)

#--------------------------confirming parameters section------------------------------------------#
argv = sys.argv
argv = argv[argv.index("--") + 1:]

i_folder_path = argv[0]
i_file_name = argv[1]
o_folder_path = argv[2]
o_file_name = argv[3]
represent_type = argv[4]
o_file_type = argv[5]

print("0: input folder path is", i_folder_path)
print("0: input file name is", i_file_name)
print("0: output folder path is", o_folder_path)
print("0: output file name is", o_file_name)
print("0: representational model is", represent_type)
print("0: output type is", o_file_type)

#-------------------------------import data section-----------------------------------------------#
#Extracts information from the .com file and produces two lists: one for coordinates and atom type, and other for connectivity.
print("1: Reading .com file ...")
file_path = i_folder_path + "\\" + i_file_name

raw_data = Import_Data.ExtractDataFromFile(file_path)
raw_data = Import_Data.FilterOutExtraInformation('above', 2, 1, raw_data) #removes everything above the second line break +1 line, from the raw_data
raw_data = Import_Data.FilterOutExtraInformation('below', 2, 1, raw_data) #raw coords and connectivity.

print("2: Extracting information from .com file ...")
raw_coords = Import_Data.FilterOutExtraInformation('below', 1, 1, raw_data)
raw_connect = Import_Data.FilterOutExtraInformation('above', 1, 0, raw_data)

#-----------------------------refine data section-------------------------------------------------#
print("3: Refining extracted data ...")
coords = Refine_Data.RefineCoordList(raw_coords)
number_of_elements = len(coords)
print("3: numbet of elements in molecule is: ", number_of_elements)
connect = Refine_Data.RefineConnectivity(raw_connect)
connect_with_symbols = Refine_Data.AddElementSymbolsToConnecrivityList(connect, coords, number_of_elements)

#-----------------------------refine elemens section----------------------------------------------#
print("4: Checking present elements ...")
names_and_pos = Refine_Elements.CreateDictionaryWithNamesAndPositions(coords, number_of_elements) #supports up to 999 elements
elements_present = Refine_Elements.GetElementsPresentInMolecule(coords)
print("4: elements present are", elements_present)
element_data = Refine_Elements.GetDataForExistingElements(elements_present, Atom_Data.Elements)

#----------------------------instantiate primitives section---------------------------------------#
print("5: Instantiating geometries ...")
materials_dict = Create_Materials.CreateAndAssignMaterials(element_data)

if represent_type == "Ball-and-Stick":
    Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)
    Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict)
    
elif represent_type == "Stick-only":
    Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)
    
elif represent_type == "Van-der-Waals":
    Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict, van_der_waals=True)
else:
    print("5: Error Instantiating geometries: unrecognized output type")

#------------------------export as something section----------------------------------------------#
print("6: Exporting the results ...")
Export_Data.ExportSceneAs(o_folder_path, o_file_name, o_file_type)