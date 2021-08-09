import bpy

def Apply_Bond_Transforms(bond_list):
    for bond in bond_list:
        bpy.context.view_layer.objects.active = bond
        bond.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
    bpy.ops.object.select_all(action='DESELECT')

def Apply_Element_Transforms(names_and_pos):
    for elem_name in names_and_pos:
        elem_obj = bpy.context.scene.objects[elem_name]
        bpy.context.view_layer.objects.active = elem_obj
        elem_obj.select_set(True)
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
    bpy.ops.object.select_all(action='DESELECT')
    
def get_bond_obj_list():
    l = []
    scene = bpy.context.scene
    mesh_objs = [o for o in scene.objects if o.type =='MESH']
    for ob in mesh_objs:
        if "-" in ob.name or "=" in ob.name or "#" in ob.name:
            l.append(ob)
    return l