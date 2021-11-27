import bpy
from ..config import Config

class FFMOCAP_OT_select_character(bpy.types.Operator):
    """Tooltip"""
    bl_idname = Config.operator_select_character_idname
    bl_label = "FFMoCap Selecting Character Operator"

    def execute(self, context):
        selected = context.selected_objects

        if len(selected) == 0:
            self.report({'WARNING'}, 'Please select the character before clicking this button.')
        
        elif len(selected) > 1:
            self.report({'WARNING'}, 'Please select only one character.')
        
        else:
            bpy.ops.view3d.view_selected()
            bpy.ops.object.editmode_toggle()
            props = context.scene.selected_char_prop
            props.selected_char = selected[0]
            props.is_selected = True

        return {'FINISHED'}