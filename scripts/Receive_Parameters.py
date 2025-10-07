import bpy
import sys
import os
import json

# Ensure the script directory is in the system path
dir = os.path.dirname(bpy.data.filepath)
if dir not in sys.path:
    sys.path.append(dir)

def load_json_config(json_path):
    """
    Loads and parses the JSON configuration file.

    :param json_path: (str) Path to the JSON config file.
    :return: (dict) Parsed configuration dictionary.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON configuration file not found at: {json_path}")

    with open(json_path, 'r') as f:
        config = json.load(f)
    return config

def get_parameters_data(json_path):
    """
    Retrieves parameters from the JSON config and returns them in a flat dictionary.

    :param json_path: (str) Path to the JSON config file.
    :return: (dict) Dictionary with flattened and renamed keys for Blender use.
    """
    config = load_json_config(json_path)

    parameters_dict = {
        "i_file_type": config["input"]["type"],
        "i_folder_path": config["input"]["paths"],
        "i_file_name": config["input"]["names"],
        "o_folder_path": config["output"]["path"],
        "o_file_name": config["output"]["name"],
        "represent_type": config["model"]["type"],
        "o_file_type": config["output"]["type"],
        "str_is_ionic": str(config["flags"]["is_ionic"]),
        "str_unit_cell": str(config["flags"]["unit_cell"]),
        "str_ion_input_list": config["ions"],
        "is_animation": config["flags"]["is_anim"],
        "str_ionic_cell": f"({config['flags']['is_ionic']}_{config['flags']['unit_cell']})",
        "atom_hl_list": config["highlight"]["atoms"],
        "bond_hl_list": config["highlight"]["bonds"],
        "forced_bonds_list": config["forced_bonds"],
        "animation_frames": config["animation_frames"]
    }

    return parameters_dict