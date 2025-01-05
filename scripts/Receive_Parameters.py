import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

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

def get_parameters_data(params_path):
    """
    :param params_path: <string> path to read the file
    returns: a dictionary with the lines taken from the parameters file
    """
    parameters = extract_parameters_data(params_path)
    parameters_dict = {
        "i_folder_path": parameters[0].strip(),
        "i_file_name": parameters[1].strip(),
        "o_folder_path": parameters[2].strip(),
        "o_file_name": parameters[3].strip(),
        "represent_type": parameters[4].strip(),
        "o_file_type": parameters[5].strip(),
        "str_is_ionic": parameters[6].strip(),
        "str_unit_cell": parameters[7].strip(),
        "str_ion_input_list": parameters[8].strip(),
        "str_is_animation": parameters[9].strip(),
        "str_ionic_cell": f"({parameters[6].strip()}_{parameters[7].strip()})" #still not sure why i need this
    }
    return parameters_dict
    
#params_path = "C:\\Documents\\Gaussian-2-Blender\\scripts\\parameters.txt"