import bpy
from ..config import Config

class FFMOCAP_OT_deselect_character(bpy.types.Operator):
    """Tooltip"""
    bl_idname = Config.operator_deselect_character_idname
    bl_label = "FFMoCap Clear Character Selection Operator"

    def execute(self, context):
        props = context.scene.selected_char_prop
        props.selected_char = None
        props.is_selected = False
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}