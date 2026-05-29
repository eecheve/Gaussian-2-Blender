import re
import bpy
from bpy import context
    
import Primitives
import importlib
importlib.reload(Primitives)

from mathutils import Vector

UNIT_CELL_EDGES = [
    (0, 1), (0, 2), (0, 3),
    (1, 4), (1, 5),
    (2, 4), (2, 6),
    (3, 5), (3, 6),
    (4, 7), (5, 7), (6, 7)
]

BBOX_NAME_PATTERN = re.compile(r'^\d+-\d+$')

def InstantiateBoundingBox(bound_box_points, mat_dict, radius=0.03):
    """
    Builds a parallelepiped (unit cell) wireframe from 8 corner points.
    """
    for i, j in UNIT_CELL_EDGES:
        origin = Vector(bound_box_points[i])
        end = Vector(bound_box_points[j])
        Primitives.InstantiateBondBetweenTwoPoints(
            origin,
            end,
            radius
        )
        Primitives.ModifyNamesAndMaterials(
            f"{i}-{j}",
            "Xx",
            mat_dict
        )

def ParentBoundingBoxToEmpty():
    """
    Collects all bounding box edge objects (named '{i}-{j}' with optional
    Blender instance suffixes) and parents them to a new Empty at the origin,
    preserving their world-space transforms.

    :return: (bpy.types.Object) The created Empty, or None if no objects were found.
    """
    bbox_objects = [
        obj for obj in bpy.context.scene.objects
        if obj.type == 'MESH' and BBOX_NAME_PATTERN.match(obj.name.split('.')[0])
    ]

    if not bbox_objects:
        print("ParentBoundingBoxToEmpty: no bounding box objects found")
        return None

    empty = bpy.data.objects.new("BoundingBox_Root", None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.location = (0, 0, 0)
    bpy.context.collection.objects.link(empty)

    for obj in bbox_objects:
        obj.parent = empty
        obj.matrix_parent_inverse = empty.matrix_world.inverted()

    print(f"ParentBoundingBoxToEmpty: parented {len(bbox_objects)} objects to BoundingBox_Root")
    return empty
