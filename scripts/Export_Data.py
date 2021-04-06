import bpy

def ExportSceneAs(folder_path, file_name, file_type): #https://docs.blender.org/api/current/bpy.ops.export_scene.html
    file_path = folder_path + "\\" + file_name + file_type
    if file_type == ".fbx":
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True)
        bpy.ops.object.select_all(action='DESELECT')
    elif file_type == ".dae": #currently, materials not saved using this settings.
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, apply_modifiers=True, selected=True, use_blender_profile=True)
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