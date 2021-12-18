import bpy
import bmesh
import addon_utils
from ..config import Config
from mathutils import Vector
from importlib import import_module
from ..FaceMeshTracking import get_initial_landmarks, add_landmark_empties, add_group_empty, transform_landmarks, get_num_of_armatures, get_name_of_object

class FFMOCAP_OT_initiate_face(bpy.types.Operator):
    """Initiale Facial Armature"""
    bl_idname = Config.operator_initiate_face_idname
    bl_label = "FFMoCap Initiate Face Operator"

    def execute(self, context):
        addon = bpy.context.preferences.addons.get('rigify')
        np = import_module('numpy')

        if not addon:
            # Rigify requires default_set=True
            addon_utils.enable('rigify', default_set=True)

        get_num_of_armatures()

        bpy.ops.object.armature_human_metarig_add()
        arm = bpy.context.active_object
        Config.num_armatures += 1
        arm.name = get_name_of_object(Config.armature_prefix)
        
        return {'FINISHED'}