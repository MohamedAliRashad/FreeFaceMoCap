import bpy
from ..config import Config

def update_cameras(self, context):
    return [(str(i), f'Camera Source {i + 1}', '') for i in Config.available_cameras]

class FFMOCAPProperties(bpy.types.PropertyGroup):
    show_mesh_on_real_face: bpy.props.BoolProperty(
                    name="Show mesh on face",
                    description="",
                    default = False
                    )

    show_fps: bpy.props.BoolProperty(
                    name="Show FPS",
                    description="",
                    default = False
                    )
    
    video_sources_enum: bpy.props.EnumProperty(
                    name= '',
                    description= 'Select an option',
                    items = update_cameras,
                )

class FaceTransformationMatrix():
    armature_points = None






