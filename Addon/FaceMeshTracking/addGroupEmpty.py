import bpy
from mathutils import Vector
from math import radians
from ..config import Config

def add_group_empty(context):
    empties = [obj for obj in bpy.data.objects if obj.name.startswith(Config.empties_prefix)]
    n = len(empties)
    location = sum([empty.matrix_world.translation for empty in empties], Vector()) / n
    diff_loc = location - context.scene.cursor.location

    if not Config.group_empty_name in bpy.data.objects:
        bpy.ops.object.empty_add(type='CUBE', location= location)
        groupEmpty = bpy.context.active_object
        groupEmpty.name = Config.group_empty_name
        groupEmpty.scale = (0.5, 0.5, 0.5)
        Config.group_empty_first_location = diff_loc
    else:
        groupEmpty = bpy.data.objects[Config.group_empty_name]
        # groupEmpty.delta_location = location
        groupEmpty.location = location
        

    bpy.ops.object.select_all(action='DESELECT')
    
    for empty in empties:
        empty.parent = groupEmpty
        empty.matrix_parent_inverse = groupEmpty.matrix_world.inverted()

    # groupEmpty.location = context.scene.cursor.location
    # groupEmpty.location -= diff_loc
    # groupEmpty.rotation_euler = (radians(-90), 0, radians(90))
    # groupEmpty.delta_scale = (1, 1, 1)
