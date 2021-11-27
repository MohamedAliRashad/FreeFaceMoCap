import bpy
from ..config import Config
from ..utils import get_number_of_cams
from .common import Common

class FFMOCAP_PT_capture_face(Common, bpy.types.Panel):
    """Capturing Face Panel"""
    bl_label = "Capturing Face"
    bl_idname = Config.panel_capture_charachter_idname

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        ffmocap_props = scene.ffmocap_props
        
        row = layout.row()
        # ffmocap_props.video_sources_enum.items = [(str(i), f'Camera Source {i + 1}', '') for i in range(Config.number_of_available_cameras)]
        # print(ffmocap_props.video_sources_enum)
        row.prop(data= ffmocap_props, property= 'video_sources_enum', text= f'Choose a webcam to use')
        
        row = layout.row()
        row.prop(ffmocap_props, 'show_mesh_on_real_face', text= 'Show mesh on the real face')
        row.prop(ffmocap_props, 'show_fps', text= 'Show FPS')

        row = layout.row()
        row.operator(Config.operator_capture_face_idname, text="Capture My Face",
                          icon="OUTLINER_OB_CAMERA")