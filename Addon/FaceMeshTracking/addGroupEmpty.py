import bpy
from mathutils import Vector
from math import radians
from ..config import Config
from .numArmatures import get_name_of_object


def add_group_empty(empties):
    """
    Creates a parent cube empty of the previously created empties.

    Args:
    -----
    empties:
        The created empties controlling the pose bones.

    Returns:
    -------
    None
    """
    num = len(empties)
    location = sum([empty.matrix_world.translation for empty in empties if not empty.name.endswith(
        '_head')], Vector()) / num
    if Config.group_loc is None:
        Config.group_loc = location

    if not get_name_of_object(Config.group_empty_prefix) in bpy.data.objects:
        bpy.ops.object.empty_add(type='CUBE', location=location)
        group_empty = bpy.context.active_object
        group_empty.name = get_name_of_object(Config.group_empty_prefix)
        group_empty.scale = tuple(
            Config.group_empty_initial_scale for _ in range(3))

    else:
        group_empty = bpy.data.objects[get_name_of_object(
            Config.group_empty_prefix)]
        group_empty.location = location

    # group_empty.hide_set(True)
    bpy.ops.object.select_all(action='DESELECT')

    for empty in empties:
        empty.parent = group_empty
        empty.matrix_parent_inverse = group_empty.matrix_world.inverted()
