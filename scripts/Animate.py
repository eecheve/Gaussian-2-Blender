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
        
def calculate_number_of_frames(anim_frames_path):
    """
    Calculates the number of frames from the animation data file.

    :param anim_frames_path (str): The file path to the animation frames data file.
    Returns: (int) The number of frames in the animation.
    """
    with open(anim_frames_path, 'r') as file:
        first_line = file.readline().strip()  # Read the first line
        parts = first_line.split() # Split the line into parts
        coordinates = parts[1:] # Remove the element identifier
        # The number of frames is the total number of coordinates divided by 3 (since each frame has 3 coordinates per element)
        num_frames = len(coordinates) / 3        
    return int(num_frames)

def separate_elements_from_bonds():
    """
    Separates objects in the scene into elements and bonds based on their names.
    Returns:
        tuple: A tuple containing a list of elements and a list of bonds.
    """
    context = bpy.context
    elements = []
    bonds = []
    for ob in context.scene.objects:
        if "_highlight" in ob.name:
            continue  # Skip objects that are highlights
        if '-' in ob.name or '=' in ob.name or '_' in ob.name or '#' in ob.name or '%' in ob.name:
            bonds.append(ob)
        else:
            elements.append(ob)
    return (elements, bonds)

def filter_bond_list_by_type(bond_list):
    """
    Filters bonds into categories based on their names.
    Args:
        bond_list (list): List of bond objects.
    Returns:
        tuple: A tuple containing lists of different types of bonds.
    """
    dashed_bonds = []
    single_bonds = []
    arom_bonds = []
    double_bonds = []
    triple_bonds = []
    for bond in bond_list:
        if '_' in bond.name:
            dashed_bonds.append(bond)
        elif '-' in bond.name:
            single_bonds.append(bond)
        elif '%' in bond.name:
            arom_bonds.append(bond)
        elif '=' in bond.name:
            double_bonds.append(bond)
        elif '#' in bond.name:
            triple_bonds.append(bond)
        else:
            print("ERROR: filtering bonds has a non-resolved case")
    return dashed_bonds, single_bonds, arom_bonds, double_bonds, triple_bonds

def insert_keyframes_to_all(number_of_frames, step_size=10):
    """
    Inserts keyframes for all objects in the scene at intervals of 10 frames.
    Args:
        number_of_frames (int): The total number of keyframes to insert.
        step_size (int): the spacing between each frame
    """
    context = bpy.context
    for i in range(0,number_of_frames):
        for ob in context.scene.objects: #looping through all objects in the scene
            ob.keyframe_insert(data_path="location", frame=i*step_size)
            
def update_keyframe_locations(target, step_size, locations):
    """
    Updates keyframe locations for a target object.
    Args:
        target (bpy.types.Object): The object to update.
        step_size (int): The interval between frames.
        locations (list): The locations for each frame (list of vectors).
    """
    target.location = locations[0]
    target.keyframe_insert(data_path="location", frame=0) #first keyframe is the first location
    for i in range(1, len(locations)):  # start from 1 since the 0th frame is already inserted
            target.location = locations[i]  # Set the location to the ith vector
            target.keyframe_insert(data_path="location", frame=(i) * step_size)
        
def update_keyframe_rotations(target, step_size, normals):
    """
    Updates keyframe rotations for a target object based on normals.
    Args:
        target (bpy.types.Object): The object to update.
        extra_frames_nmbr (int): The number of additional frames.
        step_size (int): The interval between frames.
        normals (list): The normal vectors for each frame.
    """
    target.keyframe_insert(data_path="rotation_euler", frame=0)
    for i, normal in enumerate(normals):
        try:
            phi = math.atan2(normal.y, normal.x)
        except ValueError:
            phi = math.pi / 2
        try:
            theta = math.acos(normal.z / normal.magnitude)
        except ValueError:
            theta = 0

        target.rotation_euler[1] = theta
        target.rotation_euler[2] = phi
        target.keyframe_insert(data_path="rotation_euler", frame=i * step_size)
        
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
    print("8.1: The data in animation_frames.txt was properly read")
    return l

def refine_anim_data(raw_anim_data):
    """
    Refines raw animation data into vectors.
    : param raw_anim_data (list): The raw animation data.
    Returns:
        list: A refined list of data points with vectors.
    """
    refined_data = []
    for data_point in raw_anim_data:
        element_identifier = data_point[0]
        vectors = []
        # Loop through the coordinate sets
        for i in range(1, len(data_point), 3):
            x = float(data_point[i])
            y = float(data_point[i + 1])
            z = float(data_point[i + 2])
            vector = mathutils.Vector((x, y, z))
            vectors.append(vector)
        refined_data.append([element_identifier] + vectors)
    print("8.2: The animation data was refined into numerical vectors")
    return refined_data

def get_bond_locations(bond_name, anim_data, type):
    """
    Calculates the center of mass for each bond location.
    Args:
        bond_name (str): The name of the bond.
        anim_data (list): The animation data.
        type (str): The bond type.
    Returns:
        list: The list of center locations for each bond.
    """
    """
    Calculates the center of mass for each bond location.
    Args:
        bond_name (str): The name of the bond.
        anim_data (list): The animation data.
        type (str): The bond type.
    Returns:
        list: The list of center locations for each bond.
    """
    print("Get bond locations is being called")
    l = []  # List to store center locations
    components = bond_name.split(type)  # Splitting bond_name to get the two atoms involved
    r1 = None
    r2 = None
    # Loop through anim_data to find vectors for the two components
    for data_point in anim_data:
        if data_point[0] == components[0]:
            r1 = [v for v in data_point[1:]]  # Extract all vectors for the first component
        elif data_point[0] == components[1]:
            r2 = [v for v in data_point[1:]]  # Extract all vectors for the second component

        if r1 is not None and r2 is not None:
            break  # Stop the loop when both r1 and r2 are found
    # Ensure both r1 and r2 are populated
    if r1 is None or r2 is None:
        raise ValueError("Bond components not found in the animation data.")
    # Calculate the center of mass for each corresponding pair of vectors in r1 and r2
    for i in range(len(r1)):  # Assuming r1 and r2 have the same number of vectors
        v_i = (r1[i] + r2[i]) / 2  # Calculate the center of mass
        l.append(v_i)  # Append the center of mass to the list
    print("bond locations are:", l)
    return l

def get_bond_normals(bond_name, anim_data, type): #<---------------------------------------------------------
    """
    Calculates the normal vector for each bond location.
    Args:
        bond_name (str): The name of the bond.
        anim_data (list): The animation data.
        type (str): The bond type.
    Returns:
        list: The list of normal vectors for the bond.
    """
    print("get bond normals is being called")
    n = []
    r1 = None
    r2 = None
    components = bond_name.split(type) #getting the elements involved in the bond
    for data_point in anim_data:
        #comparing the elements in the bond with the keyframe locations
        if data_point[0] == components[0]:
            r1 = [v for v in data_point[1:]]  # Extract all vectors for the first component
        elif data_point[0] == components[1]:
            r2 = [v for v in data_point[1:]]  # Extract all vectors for the second component
        if r1 is not None and r2 is not None:
            break  # Stop the loop when both r1 and r2 are found
    if r1 is None or r2 is None:
        raise ValueError("Bond components not found in the animation data.")
    #finding normal vector for each bond
    for i in range(len(r1)):  # Assuming r1 and r2 have the same number of vectors
        n_i = r2[i] - r1[i]  # Calculate the normal vector
        n.append(n_i)  # Append the normal vector to the list
    return n
            
def animate_elements_from_anim_data(anim_data, step_size=10):
    """
    Animates elements based on provided animation data.
    Args:
        anim_data (list): The animation data.
        step_size (int): The interval between frames.
        extra_frames (int): The number of additional frames.
    """
    print("11: elements are being animated")
    for data_point in anim_data:
        current_obj = bpy.data.objects[data_point[0]]  # Getting the current element in animation data
        locations = [v for v in data_point[1:]]  # Extract the vector list from the data_point
        update_keyframe_locations(target=current_obj, step_size=step_size, locations=locations)

def animate_bonds_by_type_list(bond_type_list, anim_data, bond_type, step_size=10):
    """
    Animates bonds based on their type and provided animation data.
    Args:
        bond_type_list (list): The list of bonds to animate.
        anim_data (list): The animation data.
        bond_type (str): The bond type.
        step_size (int): The interval between frames.
        extra_frames (int): The number of additional frames.
    """
    print("11: bonds are being animated")
    if len(bond_type_list) != 0:
        for bond in bond_type_list:
            print("animate_bonds_by_type: currently in bond: ", bond)
            bond_locations = get_bond_locations(bond.name, anim_data, bond_type)
            bond_normals = get_bond_normals(bond.name, anim_data, bond_type)
            update_keyframe_locations(target=bond, step_size=step_size, locations=bond_locations)
            update_keyframe_rotations(target=bond, step_size=step_size, normals=bond_normals)
    else:
        print("there are no bonds of type", bond_type)    
        return
    
def detect_bond_types(bond_list):
    """
    Extract the unique bond types from the bond list.
    :param bond_list (list): List of bpy.data.objects corresponding to the bonds in the molecule
    Returns a set of unique bonds in bond_list 
    """
    spacer_mapping = {'_': 0, '-': 1, '%': 2, '=': 3, '#': 4}
    detected_spacers = {}
    for bond in bond_list:
        bond_name = bond.name
        for spacer in spacer_mapping.keys():
            if spacer in bond_name:
                detected_spacers[spacer] = spacer_mapping[spacer]
                break  # Found the spacer, move to the next bond    
    return detected_spacers

def build_animations(anim_data, bond_list, bond_types, step_size, extra_frames, end_frame):
    """
    Animates elements and bonds based on the provided data.
    Args:
        anim_data (list): The animation data for elements.
        bond_list (list): The list of bonds to animate.
        bond_types (dict): A dictionary with all the unique bond types in the molecule
    """
    print("10: Animations are being built")
    print("10: build_animation() frame end should be:", end_frame)
    #specifying end frame
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = end_frame
    #animating elements
    animate_elements_from_anim_data(anim_data=anim_data, step_size=step_size) 
    #animating bonds
    for type, index in bond_types.items(): #iterating through the dictionary of bonds present in the molecule
        bond_type_list = filter_bond_list_by_type(bond_list)[index] #filtering bond types from bond list
        animate_bonds_by_type_list(bond_type_list=bond_type_list,
                                   anim_data=anim_data,
                                   bond_type=type,
                                   step_size=step_size)
    
def bake_all_animations(end_frame=40):
    """
    Bakes all animations for every object in the scene.
    """
    print("12: all animations were baked")
    bpy.ops.nla.bake(frame_start=0, frame_end=end_frame,
                     step=1, only_selected=False, visual_keying=True, 
                     clear_constraints=False, clear_parents=False, 
                     bake_types={'OBJECT'})
                     
def animate(anim_frames_path, step_size=20):
    """
    Animates elements and bonds in the scene based on the provided animation data.
    
    :param anim_frames_path (str): The file path to the animation frames data. 
    :param step_size (int): The number of frames between keyframes. Determines how frequently keyframes are inserted.
    :param number_of_frames (int): The total number of frames for the animation. 
    The function will:
        1. Extract animation data from the specified file.
        2. Refine the extracted data into a format suitable for animation.
        3. Separate elements and bonds in the scene and detect bond types.
        4. Set the end frame of the animation.
        5. Animate the elements and bonds using the extracted data.
        6. Bake the animation, which stores the keyframe data for all objects.
    """
    print("8: animation function is called")
    raw_anim_data = ExtractDataFromFile(anim_frames_path)
    anim_data = refine_anim_data(raw_anim_data)
    number_of_frames = calculate_number_of_frames(anim_frames_path)
    print("9: the number of frames is: ", number_of_frames)
    #element_list = separate_elements_from_bonds()[0]
    bond_list = separate_elements_from_bonds()[1]
    bond_types = detect_bond_types(bond_list)
    print("9: present bonds are: ", bond_types)
    end_frame = int((number_of_frames - 1)*step_size)
    print("9: the end frame is assigned to: ", end_frame)
    build_animations(anim_data, bond_list, bond_types, step_size, number_of_frames, end_frame)
    bake_all_animations(end_frame)

def export_animation(filepath):
    """
    Exports the animation to the given filepath.
    :param filepath: Path to save the exported file.
    """
    print("13: the export path is", filepath)
    try:
        bpy.ops.export_scene.fbx(filepath=filepath, 
                                 check_existing=True, 
                                 filter_glob="*.fbx", 
                                 use_selection=False, 
                                 global_scale=1.0, 
                                 apply_unit_scale=True, 
                                 bake_anim=True, 
                                 bake_anim_use_all_bones=False, 
                                 bake_anim_use_nla_strips=False, 
                                 bake_anim_use_all_actions=False, 
                                 bake_anim_force_startend_keying=True, 
                                 bake_anim_step=1.0, 
                                 bake_anim_simplify_factor=0.0, 
                                 use_mesh_modifiers=True)
        print(f"Animation exported to {filepath}")
    except PermissionError as e:
        print(f"Permission error: Unable to export animation to {filepath}. {str(e)}")
    except Exception as e:
        print(f"An error occurred while exporting animation to {filepath}: {str(e)}")


    
# TO DEBUG
#raw_anim_data = ExtractDataFromFile(dir+"\\animation_frames.txt")
#number_of_frames = calculate_number_of_frames(dir+"\\animation_frames.txt")
#export_path = ("C:\\Documents\\Gaussian-2-Blender\\output\\water.fbx")
#anim_data = refine_anim_data(raw_anim_data)
#element_list = separate_elements_from_bonds()[0]
#bond_list = separate_elements_from_bonds()[1]
#bond_types = detect_bond_types(bond_list)
#end_frame = (number_of_frames - 1)*20
#build_animations(anim_data, bond_list, bond_types, 20, number_of_frames, end_frame)
#bake_all_animations(anim_length)
#export_animation(export_path)

#clear_all_animations()