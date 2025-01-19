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
    
import Primitives
import Ions

import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Ions)
importlib.reload(Primitives)

def handle_non_ionic(represent_type, names_and_pos, materials_dict, connect_with_symbols, element_data):
    def ball_and_stick():
        Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)
        Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict)

    def stick_only():
        Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)

    def van_der_waals():
        Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict, van_der_waals=True)

    # Dictionary mapping represent_type to corresponding functions
    representations = {
        "Ball-and-Stick": ball_and_stick,
        "Stick-only": stick_only,
        "Van-der-Waals": van_der_waals,
    }

    represent = representations.get(represent_type) #getting the corresponding function to use
    if represent: #if represent_type can find its corresponding function
        represent() #apply the corresponding function
    else:
        print("5: Error Instantiating geometries: unrecognized output type")

def handle_ionic(represent_type, names_and_pos, materials_dict, connect_with_symbols, element_data, ion_data, ion_input, unit_cell):
    refined_ion_data = Ions.RemoveNonSpecifiedIons(ion_data, ion_input)
    print("5: getting ionic radii from input ...")
    Ions.GetIonDataFromInput(refined_ion_data, ion_input)

    refined_element_data = Ions.RemoveSpecifiedIonsFromElementDict(refined_ion_data, element_data)
    refined_element_positions = Ions.RemoveSpecifiedIonsFromElementDict(refined_ion_data, names_and_pos)
    ion_positions = Ions.GetIonPositions(names_and_pos, refined_ion_data)

    def ball_and_stick():
        Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols, unit_cell)
        if refined_element_positions:
            Primitives.InstantiateElementsFromDictionary(refined_element_positions, refined_element_data, materials_dict)
        if refined_ion_data:
            Primitives.InstantiateIonsFromDictionary(ion_positions, ion_input, materials_dict)

    def stick_only():
        Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)

    def van_der_waals():
        Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict, van_der_waals=True)
        print("5: Ionic radii replaced with van der Waals radii")

    # Dictionary mapping represent_type to corresponding functions
    representations = {
        "Ball-and-Stick": ball_and_stick,
        "Stick-only": stick_only,
        "Van-der-Waals": van_der_waals,
    }

    represent = representations.get(represent_type) #getting the corresponding function to use
    if represent: #if represent_type can find its corresponding function
        represent() #apply the corresponding function
    else:
        print("5: Error Instantiating geometries: unrecognized output type")


def Instantiate(is_ionic, represent_type, names_and_pos, materials_dict, connect_with_symbols,
                element_data, ion_data, ion_input, unit_cell):
    """Manages the instantiation of all elements and/or ions from cartesian coordinates."""
    print("5: Instantiating geometries")

    if is_ionic == "0":
        handle_non_ionic(represent_type, names_and_pos, materials_dict, connect_with_symbols, element_data)
    else:
        handle_ionic(represent_type, names_and_pos, materials_dict, connect_with_symbols, element_data, ion_data, ion_input, unit_cell)

    set_every_object_origin()

            
def set_every_object_origin():
    """
    Sets the origin of all mesh objects in the current Blender scene to the geometric center (median) of each object.
    """
    scene = bpy.context.scene
    mesh_objs = [o for o in scene.objects if o.type =='MESH']
    for ob in mesh_objs:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')