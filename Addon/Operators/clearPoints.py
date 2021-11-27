import bpy
import bmesh
from ..config import Config

class FFMOCAP_OT_clear_face_points(bpy.types.Operator):
    """Tooltip"""
    bl_idname = Config.operator_clear_face_points_idname
    bl_label = "FFMoCap Clear All Points Operator"

    def execute(self, context):
        points_pos = context.scene.points_prop.points_pos
        points_selected = context.scene.points_prop.points_selected

        for i in range(len(points_pos)):
            points_pos[i] = None
            points_selected[i] = False

        return {'FINISHED'}