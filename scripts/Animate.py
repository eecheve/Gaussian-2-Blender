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
    Determines the number of animation frames based on an input file.
    
    :param anim_frames_path: Path to the animation frames data file.
    :type anim_frames_path: str
    :return: Number of frames in the animation.
    :rtype: int
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
    Categorizes scene objects as elements or bonds based on naming conventions.
    
    :return: A tuple containing lists of elements and bonds.
    :rtype: tuple[list, list]
    """
    context = bpy.context
    elements = []
    bonds = []
    for ob in context.scene.objects:
        if "highlight" in ob.name:
            continue  # Skip objects that are highlights
        if '-' in ob.name or '=' in ob.name or '_' in ob.name or '#' in ob.name or '%' in ob.name:
            bonds.append(ob)
        else:
            elements.append(ob)
    return (elements, bonds)

def filter_bond_list_by_type(bond_list):
    """
    Categorizes bonds into different types based on naming conventions.
    
    :param bond_list: List of bond objects.
    :type bond_list: list
    :return: Tuple of categorized bond lists (dashed, single, aromatic, double, triple bonds).
    :rtype: tuple[list, list, list, list, list]
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
    Inserts location keyframes for all objects in the scene at specified frame intervals.
    
    :param number_of_frames: Total number of frames.
    :type number_of_frames: int
    :param step_size: Frame interval for keyframe insertion.
    :type step_size: int, optional
    """
    context = bpy.context
    for i in range(0,number_of_frames):
        for ob in context.scene.objects: #looping through all objects in the scene
            ob.keyframe_insert(data_path="location", frame=i*step_size)
            
def update_keyframe_locations(target, step_size, locations):
    """
    Updates and inserts keyframe locations for a target object.
    
    :param target: Object to update.
    :type target: bpy.types.Object
    :param step_size: Interval between frames.
    :type step_size: int
    :param locations: List of location vectors for keyframes.
    :type locations: list[mathutils.Vector]
    """
    target.location = locations[0]
    target.keyframe_insert(data_path="location", frame=0) #first keyframe is the first location
    for i in range(1, len(locations)):  # start from 1 since the 0th frame is already inserted
            target.location = locations[i]  # Set the location to the ith vector
            target.keyframe_insert(data_path="location", frame=(i) * step_size)
        
def update_keyframe_rotations_quaternion(target, step_size, normals):
    """
    Updates keyframe rotations for a target object using quaternion rotations based on normal vectors.

    :param target: Object to update.
    :type target: bpy.types.Object
    :param step_size: Interval between frames.
    :type step_size: int
    :param normals: List of normal vectors for each frame.
    :type normals: list[mathutils.Vector]
    """
    target.rotation_mode = 'QUATERNION'
    target.keyframe_insert(data_path="rotation_quaternion", frame=0)
    z_axis = mathutils.Vector((0, 0, 1))  # Default orientation

    for i, normal in enumerate(normals):
        if normal.length == 0:
            continue  # Skip zero-length vectors to avoid errors
        rotation_quat = z_axis.rotation_difference(normal)
        target.rotation_quaternion = rotation_quat
        target.keyframe_insert(data_path="rotation_quaternion", frame=i * step_size)

def update_keyframe_rotations(target, step_size, normals):
    """
    Updates keyframe rotations for a target object based on normals.

    :param target: Object to update.
    :type target: bpy.types.Object
    :param step_size: Interval between frames.
    :type step_size: int
    :param normals: List of normal vectors for each frame
    :type normals: list[mathutils.Vector]
    """
    # function not used in version 2025.7 I'm replacing it with the update_keyframe_rotations_quaternion version.
    # the quaternions function was written by a LLM, I don't understand it. I'm leaving the update_keyframe_rotations 
    # here to fall back in case things fall apart because I'm not using a function I 100% understand what is doing.
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
    Extracts data from a path and stores it as a list

    :param path: <string> path to read the file
    :returns: List[str] of data. Each entry corresponds to a line in the file to read
    """
    l = []
    with open(path) as f:
        content = f.readlines()
        for line in content:
            l.append(line.split()) # store the line as list in file_data
    print("8.1: The data in animation_frames.txt was properly read")
    return l

def refine_anim_data(raw_anim_data):
    """
    Converts raw animation data into numerical vectors.
    
    :param raw_anim_data: Raw animation data.
    :type raw_anim_data: list[list[str]]
    :return: Refined animation data with numerical vectors.
    :rtype: list[list]
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

    :param bond_name: The name of the bond.
    :type bond_name: str
    :param anim_data: The animation data.
    :type anim_data: List[str]
    :param type: The bond type.
    :type type: char
    :return: The list of center locations for each bond.
    :rtype: List[mathutils.Vector]
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

def get_bond_normals(bond_name, anim_data, type):
    """
    Calculates the normal vector for each bond location.

    :param bond_name: (str) The name of the bond.
    :param anim_data: (List[str]) The animation data.
    :param type: (str) The bond type.
    :return: The list of normal vectors for the bond.
    :rtype: List[Mathutils.Vector]
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
        n_i = (r2[i] - r1[i]).normalized()  # Calculate the normal vector
        n.append(n_i)  # Append the normal vector to the list
    return n
            
def animate_elements_from_anim_data(anim_data, step_size=10):
    """
    Animates elements based on provided animation data.
    
    :param anim_data: (List[str]) The animation data.
    :param step_size: (int) The interval between frames.
    :param extra_frames: (int) The number of additional frames.
    """
    print("11: elements are being animated")
    for data_point in anim_data:
        current_obj = bpy.data.objects[data_point[0]]  # Getting the current element in animation data
        locations = [v for v in data_point[1:]]  # Extract the vector list from the data_point
        update_keyframe_locations(target=current_obj, step_size=step_size, locations=locations)

def animate_bonds_by_type_list(bond_type_list, anim_data, bond_type, step_size=10):
    """
    Animates bonds based on their type and provided animation data.
    
    :param bond_type_list: (List[char]) The list of bonds to animate.
    :param anim_data: (List[str]) The animation data.
    :param bond_type: (char) The bond type.
    :param step_size: (int) The interval between frames.
    :param extra_frames: (int) The number of additional frames.
    """
    print("11: bonds are being animated")
    if len(bond_type_list) != 0:
        for bond in bond_type_list:
            print("animate_bonds_by_type: currently in bond: ", bond)
            bond_locations = get_bond_locations(bond.name, anim_data, bond_type)
            bond_normals = get_bond_normals(bond.name, anim_data, bond_type)
            update_keyframe_locations(target=bond, step_size=step_size, locations=bond_locations)
            update_keyframe_rotations_quaternion(target=bond, step_size=step_size, normals=bond_normals)
    else:
        print("there are no bonds of type", bond_type)    
        return
    
def detect_bond_types(bond_list):
    """
    Extract the unique bond types from the bond list.

    :param bond_list: (List[bpy.data.object]) objects corresponding to the bonds in the molecule
    :return: a set of unique bonds in bond_list 
    :rtype: List[char]
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
    Constructs animations for elements and bonds in the scene.
    
    :param anim_data: Processed animation data.
    :type anim_data: list[list]
    :param bond_list: List of bond objects.
    :type bond_list: list
    :param bond_types: Dictionary mapping bond symbols to indices.
    :type bond_types: dict
    :param step_size: Frame interval between keyframes.
    :type step_size: int
    :param end_frame: Last frame in the animation.
    :type end_frame: int
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
    
def bake_for_fbx(element_list, bond_list, end_frame):
    print("12: Starting baking fbx animations...")
    total_objects = len(element_list) + len(bond_list)
    print(f"12.1: Total objects to bake: {total_objects}")
    for obj in element_list + bond_list:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        print(f"12.2: Baking animation for object: {obj.name}")
        bpy.ops.nla.bake(
            frame_start=0, frame_end=end_frame,
            step=1, only_selected=True, visual_keying=True,
            clear_constraints=False, clear_parents=False,
            bake_types={'OBJECT'}
        )
    print("12.3: Baking complete!")

def force_nla_tracks_for_glb(objects):
    """
    Ensures that each object has its baked action pushed to an NLA track,
    which is required for GLB export to include animations.
    
    :param objects: List of objects to process
    """
    for obj in objects:
        if not obj.animation_data:
            obj.animation_data_create()
        
        action = obj.animation_data.action
        if action:
            # Create a new NLA track and push the action into it
            track = obj.animation_data.nla_tracks.new()
            track.name = f"{obj.name}_NLA"
            #strip = track.strips.new(action.name, action.frame_range[0], action)
            track.strips.new(action.name, int(action.frame_range[0]), action)
            print(f"Pushed action '{action.name}' to NLA track for object '{obj.name}'")
        else:
            print(f"No action found for object '{obj.name}'")


def bake_for_glb(element_list, bond_list, end_frame):
    print("12: Starting baking glb animations...")
    bpy.ops.object.select_all(action='DESELECT')
    for obj in element_list + bond_list:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = element_list[0] if element_list else bond_list[0]
    bpy.ops.nla.bake(
        frame_start=0, frame_end=end_frame,
        step=1, only_selected=True, visual_keying=True,
        clear_constraints=False, clear_parents=False,
        bake_types={'OBJECT'}
    )
    print("12.1: Baking complete!")

def bake_all_animations(element_list, bond_list, end_frame=40, mode=".fbx"):
    """
    Bakes all the animations in the scene.
    
    :param element_list: (List[bpy.data.object]) The list of elements present in the scene
    :param bond_list: (List[bpy.data.object]) The list of bonds present in the scene
    :param end_frame: (int) Optional. Determines the length of the animation
    """
    if mode==".fbx":
        bake_for_fbx(element_list, bond_list, end_frame)
    elif mode==".glb":
        bake_for_glb(element_list, bond_list, end_frame)
        force_nla_tracks_for_glb(element_list + bond_list)
    else:
        raise ValueError(f"Unsupported mode '{mode}'. Only '.fbx' and '.glb' are allowed.")
                    
def animate(anim_frames_path, mode=".fbx", step_size=20):
    """
    Orchestrates animation of molecular elements and bonds.
    
    :param anim_frames_path: Filepath of the animation data.
    :type anim_frames_path: str
    :param step_size: Frame interval between keyframes.
    :type step_size: int, optional
    """
    print("8: animation function is called")
    raw_anim_data = ExtractDataFromFile(anim_frames_path)
    anim_data = refine_anim_data(raw_anim_data)
    number_of_frames = calculate_number_of_frames(anim_frames_path)
    print("9: the number of frames is: ", number_of_frames)
    element_list = separate_elements_from_bonds()[0]
    bond_list = separate_elements_from_bonds()[1]
    bond_types = detect_bond_types(bond_list)
    print("9: present bonds are: ", bond_types)
    end_frame = int((number_of_frames - 1)*step_size)
    print("9: the end frame is assigned to: ", end_frame)
    build_animations(anim_data, bond_list, bond_types, step_size, number_of_frames, end_frame)
    bake_all_animations(element_list, bond_list, end_frame, mode=mode)

def export_animation(filepath):
    """
    Exports the current Blender scene as an animation to the specified file path.
    Supports .fbx and .glb formats.

    :param filepath: (str) Full path (including extension) where the animation will be saved.
    """
    print("Exporting animation to:", filepath)
    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext == ".fbx":
            bpy.ops.export_scene.fbx(
                filepath=filepath,
                check_existing=True,
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
                use_mesh_modifiers=True,
                embed_textures=True
            )

        elif ext == ".glb":
            bpy.ops.export_scene.gltf(
                filepath=filepath,
                export_format='GLB',
                use_selection=False,
                export_animations=True,
                export_materials='EXPORT',
                export_apply=True,
                export_force_sampling=True
            )

        else:
            print(f"Unsupported animation export format: {ext}")
            return

        print(f"Animation successfully exported to {filepath}")

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
#bake_all_animations(element_list, bond_list, end_frame)
#export_animation(export_path)

#clear_all_animations()