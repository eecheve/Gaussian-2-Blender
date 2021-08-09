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

def Instantiate(is_ionic, represent_type, names_and_pos, materials_dict, connect_with_symbols,
                element_data, ion_data, ion_input, unit_cell):
    """manages the instantiation of all elements and/or ions from cartesian coordinates."""
    print("7: Instantiating geometries")
    if is_ionic == "0":
        if represent_type == "Ball-and-Stick":
            Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)
            Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict)
            
        elif represent_type == "Stick-only":
            Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)
            
        elif represent_type == "Van-der-Waals":
            Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict, van_der_waals=True)
        else:
            print("7: Error Instantiating geometries: unrecognized output type")            
    else:
        refined_ion_data = Ions.RemoveNonSpecifiedIons(ion_data, ion_input)
        
        print("7: getting ionic radii from input ...")
        Ions.GetIonDataFromInput(refined_ion_data, ion_input)
        
        refined_element_data = Ions.RemoveSpecifiedIonsFromElementDict(refined_ion_data, element_data)
        refined_element_positions = Ions.RemoveSpecifiedIonsFromElementDict(refined_ion_data, names_and_pos)
        ion_positions = Ions.GetIonPositions(names_and_pos, refined_ion_data)
                
        if represent_type == "Stick-only":
            Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols)
            
        elif represent_type == "Van-der-Waals":
            Primitives.InstantiateElementsFromDictionary(names_and_pos, element_data, materials_dict, van_der_waals=True)
            print("7: Ionic radii replaced with van der Waals radii")
            
        elif represent_type == "Ball-and-Stick":
            if refined_element_positions: #check if dictionary is not empty
                Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols, unit_cell)
                Primitives.InstantiateElementsFromDictionary(refined_element_positions, refined_element_data, materials_dict)
                if refined_ion_data:
                    Primitives.InstantiateIonsFromDictionary(ion_positions, ion_input, materials_dict)
            else: #dictionary is empty
                Primitives.InstantiateBondsFromConnectivity(names_and_pos, materials_dict, connect_with_symbols, unit_cell)
                if refined_ion_data:
                    Primitives.InstantiateIonsFromDictionary(ion_positions, ion_input, materials_dict)
        else:
            print("7: Error Instantiating geometries: unrecognized output type") 
    set_every_object_origin()
            
def set_every_object_origin():
    scene = bpy.context.scene
    mesh_objs = [o for o in scene.objects if o.type =='MESH']
    for ob in mesh_objs:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        #me = o.data
        #mw = o.matrix_world
        #origin = sum((v.co for v in me.vertices), Vector()) / len(me.vertices)
        #T = Matrix.Translation(-origin)
        #me.transform(T)
        #mw.translation = mw @ origin