import bpy
import bmesh
from bpy_extras.object_utils import object_data_add
from ..config import Config
from mathutils import Vector

def add_landmark_empties(landmarks, createObject):
    if createObject:
        for i, v in enumerate(landmarks):
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=v)
            empty = bpy.context.active_object
            empty.name = Config.empties_prefix + str(i)
            empty.scale = (0.01, 0.01, 0.01)
    else:
        groupEmpty_loc = bpy.data.objects[Config.group_empty_name].location
        groupEmpty_first_loc = Config.group_empty_first_location
        for i, v in enumerate(landmarks):
            empty = bpy.data.objects[Config.empties_prefix + str(i)]
            loc = empty.location
            new_loc = Vector(v)
            # diff_loc = groupEmpty_loc - new_loc
            # print(diff_loc)
            empty.delta_location = new_loc
    
    bpy.ops.object.select_all(action='DESELECT')