import bpy
import os
    
def ExportSceneAs(folder_path, file_name, file_type):
    """
    Exports the Blender scene to the specified file type.

    :param folder_path: (str) The path to the folder where the file will be saved.
    :param file_name: (str) The name of the file to be saved.
    :param file_type: (str) The type of file to export (e.g., .fbx, .glb, .dae, .obj, .stl, .usdz).
    :return: None
    """
    #file_path = folder_path + "\\" + file_name + file_type
    file_path = os.path.join(folder_path, file_name + file_type)

    export_functions = {
        #".x3d": lambda: bpy.ops.export_scene.x3d(filepath=file_path, use_selection=True), #NO LONGER SUPPORTED IN BLENDER4.1+
        ".fbx": lambda: bpy.ops.export_scene.fbx(filepath=file_path, use_selection=True, bake_anim=False, embed_textures=True),
        ".glb": lambda: bpy.ops.export_scene.gltf(filepath=file_path, use_selection=True,export_materials='EXPORT',
                                                    export_animations=False),
        ".dae": lambda: bpy.ops.wm.collada_export(filepath=file_path, filter_collada=True, apply_modifiers=True,
                                                   selected=True, use_blender_profile=True, use_texture_copies=True),
        ".obj": lambda: bpy.ops.wm.obj_export(filepath=file_path, export_selected_objects=True, export_materials=True),
        ".stl": lambda: bpy.ops.wm.stl_export(filepath=file_path, export_selected_objects=True),
        ".usdz": lambda: bpy.ops.wm.usd_export(
            filepath=file_path,
            selected_objects_only=True,
            export_animation=False,
            evaluation_mode='RENDER',
            export_materials=True,
            export_textures_mode='NEW',
            export_uvmaps=True,
            export_normals=True,
            relative_paths=True,
            root_prim_path='/root',
        ),
    }

    if file_type in export_functions:
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[0] #setting the context for the export functionality
        export_functions[file_type]()
        bpy.ops.object.select_all(action='DESELECT')
    else:
        print("Invalid file type")


def ExportAnimationAs(folder_path, file_name, file_type):
    """
    Exports the current Blender scene - with its baked animation - to the
    specified file type. This is the animation-mode counterpart to
    ExportSceneAs: both build the output path from folder_path/file_name/
    file_type the same way, so Main_Body.Manage_Export can call either one
    without special-casing how the path gets built (previously this logic
    lived in Animate.py as export_animation(filepath), which took an
    already-joined path and left path-building to the caller instead).

    Unlike ExportSceneAs, this never calls select_all() first: every
    animated object needs to be included regardless of what's selected,
    which is why every exporter below is configured to export everything
    (use_selection=False / selected_objects_only=False) rather than just
    the current selection.

    Supports the same two animation formats Animate.py's baking step
    (bake_all_animations) bakes for: .fbx and .glb. .usdz is also
    supported here - USD natively carries its own time-sampled animation
    data and doesn't need the NLA-baking step .fbx/.glb rely on, so
    export_animation=True is enough to have Blender write out every frame
    in the scene's frame range that Animate.py already set up.

    :param folder_path: (str) The path to the folder where the file will be saved.
    :param file_name: (str) The name of the file to be saved.
    :param file_type: (str) The type of file to export (.fbx, .glb, or .usdz).
    :return: None
    """
    file_path = os.path.join(folder_path, file_name + file_type)

    # Use a dispatch table so adding formats is a one-liner.
    exporters = {
        ".fbx": lambda: bpy.ops.export_scene.fbx(
            filepath=file_path,
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
        ),

        ".glb": lambda: bpy.ops.export_scene.gltf(
            filepath=file_path,
            export_format='GLB',
            use_selection=False,
            export_animations=True,
            export_animation_mode='NLA_TRACKS',
            export_materials='EXPORT',
            export_apply=True,
            export_force_sampling=True
        ),

        ".usdz": lambda: bpy.ops.wm.usd_export(
            filepath=file_path,
            selected_objects_only=False,
            export_animation=True,
            evaluation_mode='RENDER',
            export_materials=True,
            export_textures_mode='NEW',
            export_uvmaps=True,
            export_normals=True,
            relative_paths=True,
            root_prim_path='/root',
        ),
    }

    try:
        export_fn = exporters.get(file_type)
        if export_fn is None:
            print(f"Unsupported animation export format: {file_type}")
            return

        result = export_fn()  # returns {'FINISHED'} | {'CANCELLED'}
        if {'FINISHED'} in (result if isinstance(result, set) else {result}):
            print(f"Animation successfully exported to {file_path}")
        else:
            print(f"Export operator returned {result} for {file_path}")

    except PermissionError as e:
        print(f"Permission error: Unable to export animation to {file_path}. {str(e)}")
    except Exception as e:
        print(f"An error occurred while exporting animation to {file_path}: {str(e)}")

#TO DEBUG
#file_path = "C:\\Documents\\Gaussian-2-Blender\\output"
#file_name = "water_gltf"
#file_type = ".glb"
#ExportSceneAs(folder_path=file_path, file_name=file_name, file_type=file_type)