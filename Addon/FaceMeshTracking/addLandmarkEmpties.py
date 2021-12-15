import bpy
import bmesh
from bpy_extras.object_utils import object_data_add
from ..config import Config
from mathutils import Vector
from importlib import import_module
from .getNumFacesEmpties import get_num_of_faces_empties

def add_landmark_empties(landmarks, createObject= False, matrix= None):
    if createObject:
        num_faces = get_num_of_faces_empties()
        for i, v in enumerate(landmarks):
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=Vector(v))
            empty = bpy.context.active_object
            empty.name = Config.empties_prefix + str(num_faces).zfill(3) + '_' + str(i)
            empty.scale = (0.01, 0.01, 0.01)
    else:
        np = import_module('numpy')
        w = np.array(matrix)
        D = np.array(landmarks)
        D = np.insert(D, 3, 1, axis= 1)
        Y = D.dot(w)
        Y = np.delete(Y, 3, axis= 1)
        for i, v in enumerate(Y):
            empty = bpy.data.objects[Config.empties_prefix + str(i)]
            empty.location = Vector(v)
    
    bpy.ops.object.select_all(action='DESELECT')