import bpy
from ..config import Config

def get_num_of_faces_empties():
    empties = [obj for obj in bpy.data.objects if obj.name.startswith(Config.empties_prefix)]
    num_faces = 0
    if len(empties) == 0:
        return 0
    
    for empty in empties:
        if num_faces == int(empty.name[len(Config.empties_prefix) : len(Config.empties_prefix) + 3]):
            num_faces += 1

    return num_faces