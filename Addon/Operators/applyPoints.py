import bpy
import bmesh
from ..config import Config

class FFMOCAP_OT_apply_face_points(bpy.types.Operator):
    """Tooltip"""
    bl_idname = Config.operator_apply_face_points_idname
    bl_label = "FFMoCap Apply Points Operator"

    def execute(self, context):
        points_pos = context.scene.points_prop.points_pos

        for point in points_pos:
            if point is None:
                self.report({'ERROR'}, 'Select all points before you can apply them!')
                return {'FINISHED'}
        
        # Add next step here!
        print('Applied')

        return {'FINISHED'}