import bpy
import sys
import os
import re

import math
from math import *
import mathutils

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
    
def clear_all_animations():
    """
    Removes all keyframes for all objects in the scene
    """
    context = bpy.context
    for ob in context.scene.objects:
        ob.animation_data_clear()
    all_actions = bpy.data.actions
    for action in all_actions:
        bpy.data.actions.remove(action)

def separate_elements_from_bonds():
    """
    Goes over all objects in the scene and separates them into elements or bonds
    return: a tuple (element_list, bond_list)
    """
    context = bpy.context
    elements = []
    bonds = []
    for ob in context.scene.objects:
        if '-' in ob.name or '=' in ob.name or '_' in ob.name:
            bonds.append(ob)
        else:
            elements.append(ob)
    return (elements, bonds)

def filter_bond_list_by_type(bond_list):
    dashed_bonds = []
    single_bonds = []
    arom_bonds = []
    double_bonds = []
    triple_bonds = []
    for bond in bond_list:
        if '_' in bond.name:
            dashed_bonds.append(bond)
        elif '-' in bond.name and '=' not in bond.name:
            single_bonds.append(bond)
        elif '-' in bond.name and '=' in bond.name:
            arom_bonds.append(bond)
        elif '=' in bond.name and '-' not in bond.name:
            double_bonds.append(bond)
        elif '#' in bond.name:
            triple_bonds.append(bond)
        else:
            print("ERROR: filtering bonds has a non-resolved case")
    return dashed_bonds, single_bonds, arom_bonds, double_bonds, triple_bonds

def insert_keyframes_to_all(number_of_frames):
    """
    Inserts a number_of_frames, separated by 10 frames to all objects in the scene
    """
    context = bpy.context
    for i in range(0,number_of_frames):
        for ob in context.scene.objects: #looping through all objects in the scene
            ob.keyframe_insert(data_path="location", frame=i*10)
            
def update_keyframe_locations(target, extra_frames_nmbr, step_size, locations):
    """
    target: the object to change its location
    extra_frames_nmbr: <int> number of frames additional from the initial geometry
    locations: list of locations for the target object for each frame to modify 
    """
    target.keyframe_insert(data_path="location", frame=0) #first keyframe is the first location
    for i in range(extra_frames_nmbr - 1):
        target.location = locations[i]
        target.keyframe_insert(data_path="location", frame=(i+1)*step_size)
        
def update_keyframe_rotations(target, extra_frames_nmbr, step_size, normals):
    target.keyframe_insert(data_path="rotation_euler", frame=0)
    for i in range(extra_frames_nmbr - 1):
        try:
            phi = math.atan2(normals[i].y, normals[i].x)
        except ValueError:
            phi = math.pi / 2
        try:
            theta = math.acos(normals[i].z/normals[i].magnitude)
        except ValueError:
            theta = 0
        target.rotation_euler[1] = theta
        target.rotation_euler[2] = phi
        target.keyframe_insert(data_path="rotation_euler", frame=(i+1)*step_size)
        
def ExtractDataFromFile(path):
    """
    path: <string> path to read the file
    returns: a list of data. Each entry corresponds to a line in the file to read
    """
    l = []
    with open(path) as f:
        content = f.readlines()
        for line in content:
            # store the line as list in file_data
            l.append(line.split())
    return l

def refine_anim_data(raw_anim_data):
    l = []
    #total_coordinates = extra_frames_nmbr * 3
    for data_point in raw_anim_data:
        m = []
        m.append(data_point[0])
        x1 = float(data_point[1])
        y1 = float(data_point[2])
        z1 = float(data_point[3])
        x2 = float(data_point[4])
        y2 = float(data_point[5])
        z2 = float(data_point[6])
        v1 = mathutils.Vector((x1,y1,z1))
        v2 = mathutils.Vector((x2,y2,z2))
        m.append([v1,v2])
        l.append(m)
    return l

def get_bond_locations(bond_name, anim_data, type):
    l = []
    components = bond_name.split(type) #getting the elements involved in the bond
    for data_point in anim_data:
        #comparing the elements in the bond with the keyframe locations
        if data_point[0] == components[0]:
            r1 = data_point[1] #vector located at one end of the bond
        elif data_point[0] == components[1]:
            r2 = data_point[1] #vector located at the other end of the bond
        else:
            continue
    #finding center of mass for each bond location
    for i in range(len(anim_data[0][1])):
        v_i = (r1[i] + r2[i])/2 #average position between the two elements
        l.append(v_i) #adding average position to the list
    return l

def get_bond_normals(bond_name, anim_data, type):
    n = []
    components = bond_name.split(type) #getting the elements involved in the bond
    for data_point in anim_data:
        #comparing the elements in the bond with the keyframe locations
        if data_point[0] == components[0]:
            r1 = data_point[1] #vector located at one end of the bond
        elif data_point[0] == components[1]:
            r2 = data_point[1] #vector located at the other end of the bond
        else:
            continue
    #finding normal vector for each bond
    for i in range(len(anim_data[0][1])):
        n_i = r2[i] - r1[i] #!!! possible bug source, the bond might rotate 180 degrees!!!!!!
        n.append(n_i)
    return n    
            
def animate_elements_from_anim_data(anim_data, step_size=10, extra_frames=3):
    for data_point in anim_data:
        current_obj = bpy.data.objects[data_point[0]] #getting the current element in animation data
        update_keyframe_locations(target=current_obj, extra_frames_nmbr=extra_frames, step_size=step_size, locations=data_point[1])

def animate_bonds_by_type_list(bond_type_list, anim_data, bond_type, step_size=10, extra_frames=3):
    if len(bond_type_list) != 0:
        for bond in bond_type_list:
            bond_locations = get_bond_locations(bond.name, anim_data, bond_type)
            bond_normals = get_bond_normals(bond.name, anim_data, bond_type)
            update_keyframe_locations(target=bond, extra_frames_nmbr=extra_frames, step_size=step_size, locations=bond_locations)
            update_keyframe_rotations(target=bond, extra_frames_nmbr=extra_frames, step_size=step_size, normals=bond_normals)
    else:
        print("there are no bonds of type", bond_type)    
        return
    
def animate(anim_data, bond_list):
    #filtering bond types from bond_list
    dashed_bonds = filter_bond_list_by_type(bond_list)[0]
    single_bonds = filter_bond_list_by_type(bond_list)[1]
    arom_bonds = filter_bond_list_by_type(bond_list)[2]
    double_bonds = filter_bond_list_by_type(bond_list)[3]
    triple_bonds = filter_bond_list_by_type(bond_list)[4]
    #animating elements
    animate_elements_from_anim_data(anim_data=anim_data, step_size=20, extra_frames=3) 
    #animating bonds
    animate_bonds_by_type_list(bond_type_list=dashed_bonds, anim_data=anim_data, bond_type='_', step_size=20, extra_frames=3)
    animate_bonds_by_type_list(bond_type_list=single_bonds, anim_data=anim_data, bond_type='-', step_size=20, extra_frames=3)
    animate_bonds_by_type_list(bond_type_list=arom_bonds, anim_data=anim_data, bond_type='-=', step_size=20, extra_frames=3)
    animate_bonds_by_type_list(bond_type_list=double_bonds, anim_data=anim_data, bond_type='=', step_size=20, extra_frames=3)
    animate_bonds_by_type_list(bond_type_list=triple_bonds, anim_data=anim_data, bond_type='#', step_size=20, extra_frames=3)
    
def assign_parent_to_objects(element_list, bond_list):
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    parent = bpy.data.objects['Empty'] #assigning parent
    parent.name = "TS" #renaming parent
    for element in element_list:
        element.parent = parent
    for bond in bond_list:
        bond.parent = parent    

raw_anim_data = ExtractDataFromFile(dir+"\\animation_frames.txt")
anim_data = refine_anim_data(raw_anim_data)
element_list = separate_elements_from_bonds()[0]
bond_list = separate_elements_from_bonds()[1]

#clear_all_animations()
animate(anim_data, bond_list)
#assign_parent_to_objects(element_list, bond_list)




#bpy.ops.nla.tracks_add(above_selected=True) #adds master nla track
#all_actions = bpy.data.actions
#for action in all_actions:
#    bpy.ops.nla.actionclip_add(action)

