import bpy
import os
    
def ExportSceneAs(folder_path, file_name, file_type):
    file_path = folder_path + "\\" + file_name + file_type
    
    export_functions = {
        #".x3d": lambda: bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True), #NO LONGER SUPPORTED IN BLENDER4.1+
        ".fbx": lambda: bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, bake_anim=False, embed_textures=True),
        ".glb": lambda: bpy.ops.export_scene.gltf(filepath=file_path, use_selection=True,export_materials='EXPORT',
                                                    export_animations=False),
        ".dae": lambda: bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, apply_modifiers=True, 
                                                   selected=True, use_blender_profile=True, use_texture_copies=True),
        ".obj": lambda: bpy.ops.wm.obj_export(filepath=file_path, export_selected_objects=True, export_materials=True),
        ".stl": lambda: bpy.ops.wm.stl_export(filepath=file_path, export_selected_objects=True)
    }
    
    if file_type in export_functions:
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0] #setting the context for the export functionality
        export_functions[file_type]()
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("Invalid file type")
        
#TO DEBUG
#file_path = "C:\\Documents\\Gaussian-2-Blender\\output"
#file_name = "water_gltf"
#file_type = ".glb"
#ExportSceneAs(folder_path=file_path, file_name=file_name, file_type=file_type)