import bpy
from ..config import Config
from .common import Common

class FFMOCAP_PT_initiate_face(Common, bpy.types.Panel):
    """Capturing Face Panel"""
    bl_label = "Initiate Facial Empties"
    bl_idname = Config.panel_initiate_face_idname

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator(Config.operator_initiate_face_idname, text="Create a New Armature",
                          icon="OUTLINER_OB_ARMATURE")
        
        row = layout.row()
        row.label(text= 'Align the armature to your character.')

        row = layout.row()
        row.operator(Config.operator_generate_rig_idname, text="Generate Rig",
                          icon="OUTLINER_OB_ARMATURE")
