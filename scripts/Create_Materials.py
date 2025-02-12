import bpy
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
import Atom_Data

import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Atom_Data)

def CreateAndAssignMaterials(ref_dict):
    """
    Instantiates the materials for the elements present in the molecule.

    :param ref_dict: (dict) Dictionary of elements present in the molecule and their data.
    :return: (dict) Dictionary of created materials.
    """
    d = {}
    for key in ref_dict:
        d[key] = AssignMaterial(key, ref_dict.get(key).get_color())
    d["Xx"] = AssignMaterial("Xx", Atom_Data.Elements.get("Xx").get_color())
    return d
    

def AssignMaterial(material_name, material_color):
    """
    Creates a material if it does not exist and assigns its name and diffuse color.

    :param material_name: (str) Name of the material.
    :param material_color: (tuple) RGBA values for the material.
    :return: (bpy.types.Material) The created or existing material.
    """
    assignment = bpy.data.materials.get(material_name)
    if assignment is None:
        assignment = bpy.data.materials.new(name=material_name)
        assignment.diffuse_color = material_color
    return assignment

def RemoveAllMaterialsAndMeshes():
    """
    Removes all materials and meshes from the Blender scene.

    :return: None
    """
    # Remove all materials
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)
    # Remove all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
        
RemoveAllMaterialsAndMeshes()