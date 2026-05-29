import bpy

from typing import Iterable
from bpy.types import Object
from mathutils import Vector

def parent_atoms_and_bonds_to_empty_object(objects_in_scene: Iterable[Object]) -> Object:
    """
    Expects Blender objects representing atoms, bonds, or other scene geometry.
    Cameras and lights should be filtered out by the caller.
    """
    # --- Create the Empty object ---
    empty = bpy.data.objects.new(name="UnitCell_Root", object_data=None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 1.0

    # Link the Empty to the active collection
    bpy.context.collection.objects.link(empty)

    # --- Parent objects ---
    for obj in objects_in_scene:
        if obj is empty:
            continue  # safety guard
        obj.parent = empty

    return empty


def replicate_and_translate_cell(cell: Object, direction: Vector) -> Object:
    """
    Duplicates a unit-cell root Empty and all its children,
    translates the duplicate by `direction`, and returns the new root.
    """
    # NOTE: Assumes a flat hierarchy (no nested children).
    # If nested objects are introduced later, this must become recursive.
    if cell.type != 'EMPTY':
        raise TypeError("replicate_and_translate_cell expects an Empty object as root")

    # --- Duplicate the root Empty ---
    new_cell = cell.copy()
    new_cell.data = None  # empties have no data, but explicit is good practice
    bpy.context.collection.objects.link(new_cell)

    # --- Duplicate and re-parent children ---
    for child in cell.children:
        new_child = child.copy()
        new_child.data = child.data.copy() if child.data else None
        bpy.context.collection.objects.link(new_child)
        new_child.parent = new_cell

        # Preserve transforms relative to parent
        new_child.matrix_parent_inverse = new_cell.matrix_world.inverted()

    # --- Translate the duplicated cell ---
    new_cell.location += direction

    return new_cell

def delete_unit_cell_roots() -> int:
    """
    Removes all Empty objects created as unit-cell replication roots
    (named 'UnitCell_Root' and Blender-suffixed copies thereof).
    Should be called after flatten_scene_hierarchy, once parenting is no longer needed.

    :return: (int) Number of Empty objects removed.
    """
    roots = [
        obj for obj in bpy.context.scene.objects
        if obj.type == 'EMPTY' and obj.name.split('.')[0] == 'UnitCell_Root'
    ]

    for obj in roots:
        bpy.data.objects.remove(obj, do_unlink=True)

    print(f"delete_unit_cell_roots: removed {len(roots)} empty root(s)")
    return len(roots)

def flatten_scene_hierarchy() -> None:
    """
    Clears all parent relationships in the scene while preserving
    world-space transforms, leaving a flat hierarchy of mesh objects.
    """
    bpy.ops.object.select_all(action='DESELECT')
    
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    for obj in meshes:
        obj.select_set(True)
    
    if not meshes:
        return
    
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
    bpy.ops.object.select_all(action='DESELECT')
