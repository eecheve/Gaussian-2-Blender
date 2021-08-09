import bpy

def Manage_Parent_Relations(names_and_pos, connect_with_symbols):
    root = connect_with_symbols[0][0]
    root_obj = bpy.context.scene.objects[root]
    for connect in connect_with_symbols:
        bond = connect[0] + connect[2] + connect[1]
        bond_obj = bpy.context.scene.objects[bond]
        elem_obj = bpy.context.scene.objects[connect[1]]
        bond_obj.parent = elem_obj
        elem_obj.parent = root_obj