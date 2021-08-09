import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import Main_Body

import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Main_Body)

#--------------------------------FOR DEBUGGING------------------------------------------------------------------------
#i_folder_path="C:\\Users\\eecheve\\Documents\\BlenderScripts\\ReadMolecules\\Blender-Gaussian-Bridge\\input_examples\\minerals"
#i_file_name="halite.com"
#o_folder_path="C:\\Users\\eecheve\\Documents\\BlenderScripts\\ReadMolecules\\Blender-Gaussian-Bridge\\output"
#o_file_name="halite"
#represent_type="Ball-and-Stick"
#o_file_type=".fbx"
#str_is_ionic="1"
#str_unit_cell="0"
#str_ion_input_list="(Na_1_VI)_(Cl_-1_VI)"
#str_is_animation="0"
#str_ionic_cell = "(" + str_is_ionic + "_" + str_unit_cell + ")"
#----------------------------------------------------------------------------------------------------------------------

#-------------------------WHEN USING UI-----------------------------------------------------------------------------
def extract_parameters_data(params_path):
    """
    path: <string> path to read the file
    returns: a list of data. Each entry corresponds to a line in the file to read
    """
    l = []
    with open(params_path, 'r') as f:
        content = f.readlines()
    for line in content:
        print(line)
        stripped = line.strip()
        print(stripped)
        l.append(stripped)
    return l

parameters = extract_parameters_data(dir + "\\parameters.txt")

i_folder_path=parameters[0].strip()
i_file_name=parameters[1].strip()
o_folder_path=parameters[2].strip()
o_file_name=parameters[3].strip()
represent_type=parameters[4].strip()
o_file_type=parameters[5].strip()
str_is_ionic=parameters[6].strip()
str_unit_cell=parameters[7].strip()
str_ion_input_list=parameters[8].strip()
#str_is_animation=parameters[9].strip()
str_ionic_cell = "(" + str_is_ionic + "_" + str_unit_cell + ")"
#----------------------------------------------------------------------------------------------------------------
main_body = Main_Body.Main_Body(i_folder_path, i_file_name, o_folder_path, o_file_name, 
                                represent_type, o_file_type, str_ionic_cell, str_ion_input_list)#,
                                #str_is_animation)
                                
main_body.Set_Raw_Parameters()
main_body.Extract_Data()
main_body.Build_Molecule()
main_body.Export()

#--------------------------------------------------------------------------------------------------------
# FOR FUTURE DEVELOPMENT: ANIMATION PART DID NOT CUT FOR DEADLINE
#--------------------------------------------------------------------------------------------------------
#if str_is_animation == "0":
#    main_body.Build_Molecule()
#    main_body.Export()
#else:
#    main_body.Build_Molecule()
#    main_body.Reset_Transforms()
#    main_body.Rig_Molecule()
#    main_body.Animate()
#    main_body.ExportForAnimation()