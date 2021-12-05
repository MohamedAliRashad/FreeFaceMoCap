import bpy
from ..config import Config
from .common import Common

class FFMOCAP_PT_select_face_points(Common, bpy.types.Panel):
    """Selecting Face Points Panel"""
    bl_label = "Selecting Face Points"
    bl_idname = Config.panel_select_face_points_idname
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ffmocap_props = scene.ffmocap_props

        points = scene.points_prop.points
        points_selected = scene.points_prop.points_selected
        points_pos = scene.points_prop.points_pos

        for i, point in enumerate(points):        
            row = layout.row()
            row.label(text= point.replace('_', ' '))
            if points_selected[i]:
                row.label(text= str(points_pos[i]))
                op = row.operator(Config.operator_select_face_points_idname, text="Change Point",
                                icon="VERTEXSEL")
                op2 = row.operator(Config.operator_deselect_face_points_idname, text="Clear Point",
                                icon="TRASH") 
                op2.id = i
            else:
                op = row.operator(Config.operator_select_face_points_idname, text="Select Point",
                                icon="VERTEXSEL")
            op.id = i
        
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator(Config.operator_clear_face_points_idname, text= 'Clear All Points', icon= 'TRASH')
        row.operator(Config.operator_apply_face_points_idname, text= 'Apply', icon= 'CHECKMARK')
