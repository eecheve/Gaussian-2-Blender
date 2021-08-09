import bpy
import sys
import os
import re

from bpy import context
import math
from math import *
import mathutils

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import Refine_Data

#Please contact eecheve@ncsu.edu if you plan to extend this program's functionality 
import importlib #<-- for end user in case they want to add functionality. 
importlib.reload(Refine_Data)

##NOTE FOR FURTHER DEVELOPMENT: ANIMATE FUNCTIONALITY DID NOT WORK. TWO POSSIBLE PROBLEMS:
# 1. If bonds and elements are animated separately, the animation of each object is exported as an individual
#    animation instead of a merged thing.
# 2. If an armature is created, a whole animation can be made, but bond stretching is not currently working.

def Animate(obj_name, names_and_pos, raw_key_frames, connectivity):
    key_frames_lst = Refine_Data.refine_key_frames(raw_key_frames)
    key_frames_dict = Refine_Data.create_frames_dict(key_frames_lst)
    e_tail = create_empty_placeholder()
    ob = get_object_in_posemode(obj_name)
    #all_bones = get_pose_bones(ob)
    #n_bones = all_bones[0]
    #a_bones = all_bones[1]
    bones = ob.pose.bones #gets pose bone list reference <-------------
    bpy.ops.object.posemode_toggle()
    inverse_kinematics_with_index(ob, bones, 1, connectivity, key_frames_dict, e_tail)
    #switch_bone_directions(ob)
    #inverse_kinematics_with_index(ob, a_bones, 0, connectivity, key_frames_dict, e_tail)
    bpy.ops.object.posemode_toggle()
    bpy.context.scene.frame_set(0)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    e_tail.select_set(True)
    bpy.ops.object.delete()
    
def get_pose_bones(ob):
    normal_bones = []
    alt_bones = []
    all_bones = ob.pose.bones
    for bone in all_bones:
        if "-" in bone.name or "=" in bone.name or "#" in bone.name:
            if "alt" in bone.name:
                alt_bones.append(bone)
            else:
                normal_bones.append(bone)
    return normal_bones, alt_bones            

def inverse_kinematics_with_index(ob, bones, index, connectivity, key_frames_dict, e_tail):
    for bone in bones: #iterates through bone list
        print("currently at", bone.name)
        bone.rotation_mode = 'QUATERNION' #uses euler mode to rotate
        b_name = bone.name
        ob.data.bones.active = bone.bone #making bone the active bone in armature (from pose bone's bone)
        e_tail.location = mathutils.Vector([0,0,0]) #reseting empty location
        bone.keyframe_insert(data_path = "location", frame=0)
        bone.keyframe_insert(data_path = "rotation_quaternion", frame=0) #adds keyframe before rotating
        bone.keyframe_insert(data_path = "scale", frame=0)
        if "-" in b_name or "=" in b_name or "#" in b_name: #does not occur for root bone
            first = connectivity[0][0] #first element in connectivity list
            elements = re.findall(r"[\w']+", b_name) #splits into list by any special character
            elem = elements[index] #element located at the tail of the bond
            apply_ik_to_bone(bone, elem, key_frames_dict, e_tail)
        else:
            elem = bone.name #as it was asigned in the Rig_Molecule module
            #move_pose_bone(bone, elem, key_frames_dict) #if element is placed at bone head
            #apply_ik_to_bone(bone, elem, key_frames_dict, e_tail) #if element is placed at bone tail
            #ob.data.bones[b_name].use_deform = False #if the root bone is not used at all
        print("*************")
    
def move_pose_bone(bone, elem, key_frames_dict):
    elem_locs = key_frames_dict[elem]
    frame_value = 0
    for i in range(len(elem_locs)):
        print("root location was", bone.location)
        frame_value += 25
        bone.location = elem_locs[i]
        print("root location now is", bone.location)
        bone.keyframe_insert(data_path = "location", frame=frame_value)

def apply_ik_to_bone(bone, elem, key_frames_dict, e_tail):
    elem_locs = key_frames_dict[elem] #locations for each frame for element at the tail
    frame_value = 0
    for i in range(len(elem_locs)): #for i in range(len(2)):
        print("currently at frame", i)
        frame_value += 25
        move_bone_tail_to_constraint(bone, i, frame_value, e_tail, elem_locs)
    
def move_bone_tail_to_constraint(bone, i, frame_value, e_elem, elem_locs):
    constraint = bone.constraints.new('IK') #adding a temporal inverse kinematics constraint
    bpy.context.scene.frame_set(frame_value)
    e_elem.location = elem_locs[i] #moving tail to next frame location
    print("constraint target at", e_elem.location)
    print("bone tail was at", bone.tail)
    constraint.target = e_elem #setting tail empty as target to move bone's tail
    constraint.use_stretch = True
    bone.constraints.update() #applying constraint
    bpy.context.view_layer.update() #updating scene
    transform = bone.matrix.copy() #bone transform due to the constraint
    bone.constraints.remove(constraint) #removing temporary transform
    bone.constraints.update() #applying constraint removal
    bone.matrix = transform #updating bone's transform
    print("bone tail is now at", bone.tail)
    bone.keyframe_insert(data_path = "location", frame=frame_value)
    bone.keyframe_insert(data_path = "rotation_quaternion", frame=frame_value)
    bone.keyframe_insert(data_path = "scale", frame=frame_value)
    
def switch_bone_directions(ob):
    bpy.ops.object.posemode_toggle()
    bpy.ops.object.editmode_toggle()
    ebs = ob.data.edit_bones
    for eb in ebs:
        eb.select = True
        bpy.ops.armature.switch_direction()
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.posemode_toggle()

def create_empty_placeholder():
    e_tail = bpy.data.objects.new('e_tail', None) #empty placeholder for bone tail position
    bpy.context.scene.collection.objects.link(e_tail)
    return e_tail

def get_object_in_posemode(obj_name):    
    ob = bpy.context.scene.objects[obj_name] #Gets object by name
    bpy.context.view_layer.objects.active = ob #makes object the active object
    ob.select_set(True) #Selects active object
    bpy.ops.object.posemode_toggle() #toggles pose mode
    return ob

