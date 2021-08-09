import bpy

def ExportSceneAs(folder_path, file_name, file_type): #https://docs.blender.org/api/current/bpy.ops.export_scene.html
    file_path = folder_path + "\\" + file_name + file_type
    if file_type == ".fbx":
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, bake_anim=True)
        bpy.ops.object.select_all(action='DESELECT')
    elif file_type == ".dae": #currently, materials not saved using this settings.
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, apply_modifiers=True, 
                                  selected=True, use_blender_profile=True, use_texture_copies=True) #use_textures_copies added
        bpy.ops.object.select_all(action='DESELECT')
    elif file_type == ".obj":
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.obj(filepath=file_path, use_selection=True, use_materials=True)
        bpy.ops.object.select_all(action='DESELECT')
    elif file_type == ".x3d":
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True)
        bpy.ops.object.select_all(action='DESELECT')
    elif file_type == ".stl":
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_mesh.stl(filepath=file_path, use_selection=True) #https://docs.blender.org/api/current/bpy.ops.export_mesh.html
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("invalid file type")
        
def ExportForAnimation(names_and_pos, bond_list, folder_path, file_name, file_type):
    file_path = folder_path + "\\" + file_name + file_type
    for elem_name in names_and_pos:
        elem_obj = bpy.context.scene.objects[elem_name]
        elem_obj.select_set(True)
    for bond_obj in bond_list:
        bond_obj.select_set(True)
    armat_obj = bpy.context.scene.objects[file_name]
    armat_obj.select_set(True)
    bpy.context.view_layer.objects.active = armat_obj
    bpy.ops.object.posemode_toggle()
    bpy.ops.export_scene.fbx(filepath=file_path, 
                             use_selection=True,
                             apply_unit_scale=True,
                             add_leaf_bones=False,
                             use_armature_deform_only=True,
                             bake_anim=True,
                             bake_space_transform=True) 
    #bpy.ops.object.select_all(action='DESELECT')
    