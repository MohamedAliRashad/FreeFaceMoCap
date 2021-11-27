import bpy
import bmesh
from ..config import Config

class FFMOCAP_OT_deselect_face_points(bpy.types.Operator):
    """Tooltip"""
    bl_idname = Config.operator_deselect_face_points_idname
    bl_label = "FFMoCap Clear Face Points Selection Operator"

    id: bpy.props.IntProperty(default=0)

    def execute(self, context):
        points_pos = context.scene.points_prop.points_pos
        points_selected = context.scene.points_prop.points_selected

        points_pos[self.id] = None
        points_selected[self.id] = False
        return {'FINISHED'}