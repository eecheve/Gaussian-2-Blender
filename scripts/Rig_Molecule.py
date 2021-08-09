import bpy
import sys
import os

from bpy import context
import math
from math import *
import mathutils

context = bpy.context

def Rig_Molecule(obj_name, names_and_pos, connect_list, bond_list):
    armat_obj = create_armature_obj(obj_name, names_and_pos, connect_list)
    create_bond_hierarchy(armat_obj, connect_list, names_and_pos)
    set_armature_constraint(armat_obj)
    assign_weights_elements(names_and_pos)
    assign_weights_bonds(bond_list)

def join_meshes(obj_name):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.join()
    bpy.context.active_object.name = obj_name
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

def create_armature_obj(obj_name, names_and_pos, connect_list):
    print("7.1: creating armature")
    bpy.ops.object.armature_add(enter_editmode=True)
    armat_obj = bpy.context.active_object
    armat_obj.name = obj_name
    armat = armat_obj.data
    ebs = armat.edit_bones
    for connect in connect_list:
        name1 = connect[0]
        name2 = connect[1]
        type = connect[2]
        bond_name = name1 + type + name2
        #bond_name_alt = name1 + type + name2 + "-alt"
        bone = ebs.new(bond_name)
        #bone_alt = ebs.new(bond_name_alt)
        bone.head = names_and_pos[name1]
        bone.tail = names_and_pos[name2]
        #bone_alt.head = names_and_pos[name2]
        #bone_alt.tail = names_and_pos[name1]
    return armat_obj

def create_bond_hierarchy(armat_obj, connect_list, names_and_pos):
    print("7.2: renaming root bone")
    first_element = connect_list[0][0]
    first_location = names_and_pos[first_element]
    bpy.ops.object.mode_set(mode = 'EDIT')
    ebs = armat_obj.data.edit_bones
    root = None
    for eb in ebs:
        print("currently at", eb.name)
        if eb.name == "Bone":
            root = eb
            print("renaming to", first_element)
            eb.name = first_element
            eb.head = first_location #<--------------------------------
            eb.tail = first_location + mathutils.Vector([0,1,0])
        else:
            if root is not None:
                eb.parent = root   
    bpy.ops.object.mode_set(mode = 'OBJECT')
    
def set_armature_constraint(armature_obj):
    print("7.3: setting armature constraints")
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.context.view_layer.objects.active = armature_obj
    armature_obj.select_set(True)
    bpy.ops.object.parent_set(type='ARMATURE_NAME')
    
def assign_weights_elements(names_and_pos):
    print("7.4: assigning weights for elements")
    for e_name in names_and_pos:
        elem_obj = bpy.context.scene.objects[e_name]
        vgs = elem_obj.vertex_groups
        verts = elem_obj.data.vertices
        vert_list = get_verts_indices(verts)
        for vg in vgs:
            if e_name in vg.name:
                print("7.4.1: assigning", vg.name, "for", e_name)
                vg.add(vert_list, 1.0, 'REPLACE')
                break
                #if "alt" not in vg.name:
                #    vg.add(vert_list, 1.0, 'REPLACE')
                #else:
                #    vg.add(vert_list, 1.0, 'REPLACE')
                #    break
            
def get_verts_indices(verts):
    l = []
    for vert in verts:
        index = vert.index
        l.append(index)
    return l

def assign_weights_bonds(bond_list):
    print("7.5: assigning weights for bonds")
    for bond in bond_list:
        vgs = bond.vertex_groups
        verts = bond.data.vertices
        vert_list = get_verts_indices(verts)
        for vg in vgs:
            if bond.name in vg.name:
                print("7.5.1: assigning weight for", vg.name, "to", bond.name)
                if "alt" not in vg.name:
                    vg.add(vert_list, 1.0, 'REPLACE')
                else:
                    vg.add(vert_list, 1.0, 'REPLACE')
                    break
