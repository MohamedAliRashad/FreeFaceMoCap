import bpy
from ..config import Config

def get_num_of_armatures():
    num = 0
    for obj in bpy.context.scene.objects:
        if 'Armature' in obj.name:
            num += 1

    Config.num_armatures = num

def get_name_of_object(prefix):
    return prefix + str(Config.num_armatures).zfill(3)
