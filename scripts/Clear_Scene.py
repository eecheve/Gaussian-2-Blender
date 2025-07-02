import bpy

def clear_scene():
    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select and delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # Remove all meshes, materials, cameras, lights, etc.
    data_blocks = [
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.curves,
        bpy.data.textures,
        bpy.data.images,
        bpy.data.armatures,
        bpy.data.collections
    ]

    for block in data_blocks:
        for item in block:
            block.remove(item, do_unlink=True)

    print("Scene cleared: all objects, meshes, materials, and data blocks removed.")
    
    
clear_scene()
