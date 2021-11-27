import bpy
from ..config import Config
from .common import Common

class FFMOCAP_PT_no_camera_found(Common, bpy.types.Panel):
    """No Camera Found Panel"""
    bl_label = "No Camera Found"
    bl_idname = Config.panel_no_camera_idname

    @classmethod
    def poll(self, context):
        return Config.are_dependancies_installed and Config.number_of_available_cameras == 0

    def draw(self, context):
        layout = self.layout

        layout.alert = True
        lines = [
                    'Warning! There is no camera detected in your system.',
                    'Please check that you successfully setup the camera then restart blender.'
                ]
        for i, line in enumerate(lines):
            if i == 0:
                layout.label(text= line, icon= 'X')
            else:
                layout.label(text= line)