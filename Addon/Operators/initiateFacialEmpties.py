from csv import reader as csv_reader
import bpy
import bmesh
from ..config import Config
from ..FaceMeshTracking import get_initial_landmarks, add_landmark_empties, add_group_empty
from importlib import import_module

class FFMOCAP_OT_initiate_facial_empties(bpy.types.Operator):
    """Initiale Facial Empties"""
    bl_idname = Config.operator_initiate_facial_empties_idname
    bl_label = "FFMoCap Initiate Facial Empties Operator"

    def execute(self, context):
        np = import_module('numpy')
        landmarks = get_initial_landmarks()
        props = context.scene.face_transformation_matrix
        props.num_landmarks = len(landmarks)
        add_landmark_empties(landmarks, createObject= True)
        # add_group_empty(context)
        return {'FINISHED'}