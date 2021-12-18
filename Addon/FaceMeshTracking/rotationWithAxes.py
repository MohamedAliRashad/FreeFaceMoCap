from ..config import Config
from importlib import import_module
import bpy
from math import radians, acos
from mathutils import Euler, Vector
from .numArmatures import get_name_of_object

def rotate_head_with_axes():
    np = import_module('numpy')

    p1 = np.array(Config.nose_loc)
    p2 = np.array(bpy.data.objects.get(get_name_of_object(Config.empties_prefix) + '_nose').matrix_world.translation)
    head_loc = Config.head_loc

    head = bpy.data.objects.get(get_name_of_object(Config.empties_prefix) + '_head')

    shift = p2 - p1
    head.location = head_loc + Vector((shift * 10).tolist())

    # p1 = np.array(Config.lip_bottom_loc)
    # p2 = np.array(bpy.data.objects.get(get_name_of_object(Config.empties_prefix) + '_lip.B').matrix_world.translation)
    # jaw = Config.jaw_master
    # shift = p2 - p1
    # jaw.location = Config.jaw_master_loc + Vector((shift * 0.1).tolist())

    # def unit_vector(vector):
    #     return vector / np.linalg.norm(vector)

    # def angle_between(v1, v2):
    #     v1_u = unit_vector(v1)
    #     v2_u = unit_vector(v2)
    #     dot = np.dot(v1_u, v2_u)
    #     # cross = np.cross(v1_u, v2_u)
    #     sign = (v1_u[0] * v2_u[1] - v1_u[1] * v2_u[0])
    #     if sign < 0:
    #         sign = -1
    #     else:
    #         sign = 1
    #     return np.arccos(np.dot(v1_u, v2_u)) * sign

    # def points_to_vectors(center_point, p1, p2):
    #     return p1 - center_point, p2 - center_point
    
    # p1_xy = np.array([p1[0], p1[1]])
    # p2_xy = np.array([p2[0], p2[1]])
    # center_xy = np.array([center[0], center[1]])
    # v1, v2 = points_to_vectors(center_xy, p1_xy, p2_xy)
    # rot_z = angle_between(v1, v2)
    
    # p1_xz = np.array([p1[0], p1[2]])
    # p2_xz = np.array([p2[0], p2[2]])
    # center_xz = np.array([center[0], center[2]])
    # v1, v2 = points_to_vectors(center_xz, p1_xz, p2_xz)
    # rot_y = angle_between(v1, v2)
    
    # p1_yz = np.array([p1[1], p1[2]])
    # p2_yz = np.array([p2[1], p2[2]])
    # center_yz = np.array([center[1], center[2]])
    # v1, v2 = points_to_vectors(center_yz, p1_yz, p2_yz)
    # rot_x = angle_between(v1, v2)

    # print('X: ', np.rad2deg(rot_x), 'Y: ', np.rad2deg(rot_y), 'Z: ', np.rad2deg(rot_z))

    # head.rotation_euler = Euler((rot_x, rot_y, rot_z), 'XYZ')
