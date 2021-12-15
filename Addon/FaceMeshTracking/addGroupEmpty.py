import bpy
from mathutils import Vector
from math import radians
from ..config import Config
from .getNumFacesEmpties import get_num_of_faces_empties

def add_group_empty(context):
    num_faces = get_num_of_faces_empties()
    empties = [obj for obj in bpy.data.objects if obj.name.startswith(Config.empties_prefix + str(num_faces - 1).zfill(3))]
    n = len(empties)
    location = sum([empty.matrix_world.translation for empty in empties], Vector()) / n

    if not Config.group_empty_name in bpy.data.objects:
        bpy.ops.object.empty_add(type='CUBE', location= location)
        groupEmpty = bpy.context.active_object
        groupEmpty.name = Config.group_empty_name + '_' + str(num_faces - 1)
        groupEmpty.scale = tuple(Config.group_empty_initial_scale for _ in range(3))

    else:
        groupEmpty = bpy.data.objects[Config.group_empty_name]
        groupEmpty.location = location

    bpy.ops.object.select_all(action='DESELECT')
    
    for empty in empties:
        empty.parent = groupEmpty
        empty.matrix_parent_inverse = groupEmpty.matrix_world.inverted()