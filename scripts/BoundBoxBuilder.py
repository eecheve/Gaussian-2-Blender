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
