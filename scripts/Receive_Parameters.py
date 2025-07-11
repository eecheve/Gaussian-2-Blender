import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

def extract_parameters_data(params_path):
    """
    Extracts data from a parameters file.

    :param params_path: (str) Path to the parameters file.
    :return: (list) A list of data, each entry corresponding to a line in the file.
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
    Retrieves parameters data from a file and returns it as a dictionary.

    :param params_path: (str) Path to the parameters file.
    :return: (dict) A dictionary with the lines taken from the parameters file.
    """
    parameters = extract_parameters_data(params_path)
    parameters_dict = {
        "i_file_type": parameters[0].strip(),
        "i_folder_path": parameters[1].strip(),
        "i_file_name": parameters[2].strip(),
        "o_folder_path": parameters[3].strip(),
        "o_file_name": parameters[4].strip(),
        "represent_type": parameters[5].strip(),
        "o_file_type": parameters[6].strip(),
        "str_is_ionic": parameters[7].strip(),
        "str_unit_cell": parameters[8].strip(),
        "str_ion_input_list": parameters[9].strip(),
        "str_is_animation": parameters[10].strip(),
        "str_ionic_cell": f"({parameters[7].strip()}_{parameters[8].strip()})", #don't remember why i need this
        "atom_hl_list": parameters[11].strip(),
        "bond_hl_list": parameters[12].strip(),
        "forced_bonds_list": parameters[13].strip()
    }
    return parameters_dict