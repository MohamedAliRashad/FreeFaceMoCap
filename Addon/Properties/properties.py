import bpy
from ..config import Config

def update_cameras(self, context):
    return [(str(i), f'Camera Source {i + 1}', '') for i in range(Config.number_of_available_cameras)]

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

class SelectCharProp():
    selected_char = None
    is_selected = False

class SelectPointsProp():
    points = ['Chin', 'Left_Mouth', 'Right_Mouth', 'Nose', 'Left_Eye_Point_1', 'Left_Eye_Point_2', 'Right_Eye_Point_1', 'Right_Eye_Point_2']
    points_pos = [None for _ in range(len(points))]
    points_selected = [False for _ in range(len(points))]