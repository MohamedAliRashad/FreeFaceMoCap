import bpy
from ..config import Config
from .common import Common

class FFMOCAP_PT_initiate_facial_empties(Common, bpy.types.Panel):
    """Capturing Face Panel"""
    bl_label = "Initiate Facial Empties"
    bl_idname = Config.panel_initiate_facial_empties_idname

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator(Config.operator_initiate_facial_empties_idname, text="Initiate Face Empties",
                          icon="OUTLINER_OB_EMPTY")
        row.operator(Config.operator_confirm_face_location_update_idname, text="Confirm New Location",
                          icon="CHECKMARK")
        
        # row = layout.row()
        
        # row = layout.row()
        # split = row.split(factor=0.5)

        # col1 = split.column()
        # col2 = split.column()

        # col1.label(text='')
        # col2.operator(Config.operator_confirm_face_location_update_idname, text="Confirm New Location",
        #                   icon="CHECKMARK")