import bpy
    
def ExportSceneAs_old(folder_path, file_name, file_type):
    file_path = folder_path + "\\" + file_name + file_type
    
    export_functions = {
        ".fbx": lambda: bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, bake_anim=True, embed_textures=True),
        ".dae": lambda: bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, apply_modifiers=True, 
                                                   selected=True, use_blender_profile=True, use_texture_copies=True),
        ".obj": lambda: bpy.ops.export_scene.obj(filepath=file_path, use_selection=True, use_materials=True),
        ".x3d": lambda: bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True),
        ".stl": lambda: bpy.ops.export_mesh.stl(filepath=file_path, use_selection=True)
    }
    
    if file_type in export_functions:
        bpy.ops.object.select_all(action='SELECT')
        export_functions[file_type]()
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("Invalid file type")
        
def ExportSceneAs(folder_path, file_name, file_type):  
    """
    Exports the scene as the specified file type while ensuring transparency is enabled.

    Parameters:
    folder_path (str): The directory where the file will be saved.
    file_name (str): The name of the exported file (without extension).
    file_type (str): The format of the exported file (e.g., ".fbx", ".dae", ".obj", ".x3d", ".stl").
    """

    # Enable film transparency for proper alpha handling
    bpy.context.scene.render.film_transparent = True  

    file_path = folder_path + "\\" + file_name + file_type

    export_functions = {
        ".fbx": lambda: bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, 
                                                  bake_anim=True, embed_textures=True, 
                                                  path_mode='COPY', use_active_collection=False),
        ".dae": lambda: bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, 
                                                  apply_modifiers=True, selected=True, 
                                                  use_blender_profile=True, use_texture_copies=True),
        ".obj": lambda: bpy.ops.export_scene.obj(filepath=file_path, use_selection=True, 
                                                 use_materials=True),
        ".x3d": lambda: bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True),
        ".stl": lambda: bpy.ops.export_mesh.stl(filepath=file_path, use_selection=True)
    }
    if file_type in export_functions:
        bpy.ops.object.select_all(action='SELECT')
        export_functions[file_type]()
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("Invalid file type")
        
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
    
#TO DEBUG
file_path = "C:\\Documents\\Gaussian-2-Blender\\output"
file_name = "methyl_xanthate_highlighted3"
file_type = ".fbx"

ExportSceneAs(folder_path=file_path, file_name=file_name, file_type=file_type)
    