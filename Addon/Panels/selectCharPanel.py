import bpy
from ..config import Config
from .common import Common

class FFMOCAP_PT_select_character(Common, bpy.types.Panel):
    """Selecting Character Panel"""
    bl_label = "Selecting Character"
    bl_idname = Config.panel_select_charachter_idname

    def draw(self, context):
        layout = self.layout
        props = context.scene.selected_char_prop

        row = layout.row()
        if props.is_selected:
            row.operator(Config.operator_select_character_idname, text="Change Selection",
                            icon="SELECT_SET")
            row.operator(Config.operator_deselect_character_idname, text="Clear Selection",
                            icon="TRASH")
        else:
            row.operator(Config.operator_select_character_idname, text="Select Character",
                            icon="SELECT_SET")