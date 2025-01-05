import bpy
import sys
import os
from bpy import context, data
from math import radians, degrees
import mathutils
from Receive_Parameters import extract_parameters_data, get_parameters_data
import importlib

# Import necessary modules for reload
importlib_modules = [
    "Atom_Data", "Import_Data", "Refine_Data", "Refine_Elements", 
    "Create_Materials", "Primitives", "Export_Data", "Ions", 
    "Instantiate_Molecules", "Raw_Parameters", "Rig_Molecule", 
    "Animate", "Clear_Transforms", "Parent_Relations"
]

for module in importlib_modules:
    globals()[module] = importlib.import_module(module)
    importlib.reload(globals()[module])

class Main_Body(object):
    def __init__(self, i_folder_path, i_file_name, o_folder_path, o_file_name,
                 represent_type, o_file_type, str_ionic_cell, str_ion_input_list, str_is_animation):
        self.i_folder_path = i_folder_path
        self.i_file_name = i_file_name
        self.o_folder_path = o_folder_path
        self.o_file_name = o_file_name
        self.represent_type = represent_type
        self.o_file_type = o_file_type
        self.str_ionic_cell = str_ionic_cell
        self.str_ion_input_list = str_ion_input_list
        self.str_is_animation = str_is_animation
        
        self.coords = []
        self.number_of_elements = 0
        self.is_ionic=""
        self.unit_cell = []
        self.ion_input_list = []
        self.raw_coords = []
        self.raw_connect = []
        self.raw_key_frames = []
        
        self.names_and_pos = {}
        self.connect_with_symbols = []
        self.bond_list = []

    def Set_Raw_Parameters(self):
        #-------------------------------confirming parameters section-------------------------------------#
        print("0: input folder path is", self.i_folder_path)
        print("0: input file name is", self.i_file_name)
        print("0: output folder path is", self.o_folder_path)
        print("0: output file name is", self.o_file_name)
        print("0: representational model is", self.represent_type)
        print("0: output type is", self.o_file_type)
        print("0: ion and unit cell is", self.str_ionic_cell)
        print("0: ion list is", self.str_ion_input_list)
        print("0: is animation is", self.str_is_animation)    
        #-------------------------------import data section-----------------------------------------------#
        #Extracts information from the .com file and produces two lists: one for coordinates and atom type, and other for connectivity.
        print("1: Reading .com file ...")
        
        raw_coords_connect = Raw_Parameters.Set_Raw_Parameters_Convert(self.i_folder_path, self.i_file_name)
        self.raw_coords = raw_coords_connect[0]
        self.raw_connect = raw_coords_connect[1]
        
        if self.str_is_animation == "0":
            raw_coords_connect = Raw_Parameters.Set_Raw_Parameters_Convert(self.i_folder_path, self.i_file_name)
            self.raw_coords = raw_coords_connect[0]
            self.raw_connect = raw_coords_connect[1]
        #else:
        #    raw_coords_connect = Raw_Parameters.Set_Raw_Parameters_Animate()
        #    self.raw_coords = raw_coords_connect[0]
        #    self.raw_connect = raw_coords_connect[1]
        #    self.raw_key_frames = raw_coords_connect[2]
        
    def Extract_Data(self):
        print("2: Refining extracted data ...")
        self.coords = Refine_Data.RefineCoordList(self.raw_coords)
        self.number_of_elements = len(self.coords)

        ionic_cell=Refine_Data.rebuild_list(self.str_ionic_cell)
        ionic_cell = Refine_Data.make_tuple_in_list(ionic_cell)
        self.is_ionic = ionic_cell[0][0]
        self.unit_cell = ionic_cell[0][1]

        self.ion_input_list = Refine_Data.rebuild_list(self.str_ion_input_list)
        self.ion_input_list = Refine_Data.make_tuple_in_list(self.ion_input_list)

        print("2.1: number of elements in molecule is: ", self.number_of_elements)
        connect = Refine_Data.RefineConnectivity(self.raw_connect)
        self.connect_with_symbols = Refine_Data.AddElementSymbolsToConnecrivityList(connect, self.coords, self.number_of_elements)
    
    def Build_Molecule(self):
        #-----------------------------refine elemens section----------------------------------------------#
        print("3: Checking present elements ...")
        self.names_and_pos = Refine_Elements.CreateDictionaryWithNamesAndPositions(self.coords, self.number_of_elements) #supports up to 999 elements
        elements_present = Refine_Elements.GetElementsPresentInMolecule(self.coords)
        print("3.1: elements present are", elements_present)
        element_data = Refine_Elements.GetDataForExistingElements(elements_present, Atom_Data.Elements)
        ion_data = Refine_Elements.GetDataForExistingElements(elements_present, Atom_Data.IonicRadii)
        #----------------------------get ion specifications section---------------------------------------_
        print("4: Checking for present ion specifications ...")
        if self.ion_input_list: #checking if list is not empty
            print("4.1: ion_input_list is not empty")
            ion_input = Ions.CreateIonDataFromInput(self.ion_input_list)
        
        else:
            print("4: There are no ions with charge, coordination and spin specified")
            ion_input = []
        #----------------------------instantiate primitives section---------------------------------------#
        print("5: Creating and assigning materials ...")
        materials_dict = Create_Materials.CreateAndAssignMaterials(element_data)
        
        Instantiate_Molecules.Instantiate(self.is_ionic, self.represent_type, self.names_and_pos, 
                                materials_dict, self.connect_with_symbols, element_data, ion_data, ion_input, self.unit_cell)
                                          
    def Manage_Parent_Relations(self):
        Parent_Relations.Manage_Parent_Relations(self.names_and_pos, self.connect_with_symbols)
    
    def Reset_Transforms(self):    
        self.bond_list = Clear_Transforms.get_bond_obj_list()
        print("6.1: Applying bond transforms")
        Clear_Transforms.Apply_Bond_Transforms(self.bond_list)#<------- might be a source of problems in animation...
        print("6.2: Applying element transforms")
        Clear_Transforms.Apply_Element_Transforms(self.names_and_pos)
    
    def Rig_Molecule(self):
        print("7: Rigging molecule ...")
        Rig_Molecule.Rig_Molecule(self.o_file_name, self.names_and_pos, self.connect_with_symbols, self.bond_list)
        
    def Animate(self):
        print("8: Animating molecule ...")
        Animate.Animate(self.o_file_name, self.names_and_pos, self.raw_key_frames, self.connect_with_symbols)
        
    def Export(self):
        #------------------------export as something section----------------------------------------------#
        print("9: Exporting the results ...")
        Export_Data.ExportSceneAs(self.o_folder_path, self.o_file_name, self.o_file_type)
        
    def ExportForAnimation(self):
        print("9: Exporting the results ...")
        Export_Data.ExportForAnimation(self.names_and_pos, self.bond_list, self.o_folder_path, self.o_file_name, self.o_file_type)
    
if __name__ == "__main__":
    params_data = get_parameters_data("C:\\Documents\\Gaussian-2-Blender\\scripts\\parameters.txt")
    main_body_instance = Main_Body(params_data["i_folder_path"],
                                   params_data["i_file_name"],
                                   params_data["o_folder_path"],
                                   params_data["o_file_name"],
                                   params_data["represent_type"],
                                   params_data["o_file_type"],
                                   params_data["str_ionic_cell"],
                                   params_data["str_ion_input_list"],
                                   params_data["str_is_animation"])
    main_body_instance.Set_Raw_Parameters()
    main_body_instance.Extract_Data()
    main_body_instance.Build_Molecule()
    main_body_instance.Export()