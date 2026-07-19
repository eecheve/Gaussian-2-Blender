import bpy


def clear_scene():
    """
    Removes every object from the current scene except cameras and lights,
    then purges any mesh data left orphaned by that removal.

    Used at the start of each growth-cell export in Main_Body so every
    supercell is built from a clean slate instead of piling up on top of
    objects left behind by the previous export - which would otherwise
    get auto-suffixed by Blender (e.g. 'C01.001') and break the
    primitive-vs-replica name bookkeeping that UnitCellLinker,
    BoundBoxBuilder, and UnitCellReplicator rely on.

    :return: None
    """
    objects_to_remove = [
        obj for obj in bpy.context.scene.objects
        if obj.type not in {"CAMERA", "LIGHT"}
    ]

    for obj in objects_to_remove:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"clear_scene: removed {len(objects_to_remove)} object(s)")
    _purge_orphaned_meshes()


def _purge_orphaned_meshes():
    """
    Removes mesh datablocks left with zero users after clear_scene() runs,
    so repeated export cycles don't accumulate unused data in the .blend
    file.

    :return: None
    """
    orphaned = [mesh for mesh in bpy.data.meshes if mesh.users == 0]
    for mesh in orphaned:
        bpy.data.meshes.remove(mesh)
