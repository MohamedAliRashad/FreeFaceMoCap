from ..config import Config
from importlib import import_module
import bpy
from math import radians, acos
from mathutils import Euler, Vector
from .numArmatures import get_name_of_object


def rotate_head_with_axes():
    np = import_module('numpy')
    nose_new = bpy.data.objects.get(get_name_of_object(
        Config.empties_prefix) + '_nose')

    p1 = np.array(Config.nose_loc)
    p2 = np.array(nose_new.matrix_world.translation)
    head_loc = Config.head_loc

    head = bpy.data.objects.get(
        get_name_of_object(Config.empties_prefix) + '_head')

    shift = p2 - p1
    head.location = head_loc + Vector((shift * 10).tolist())

    # center = np.array(Config.group_loc)

    # def get_rotation(point1, point2, center):
    #     x = np.array([1, center[1]])
    #     v1 = point1 - center
    #     v2 = point2 - center

    #     x1 = angle_between(x, v1) * int(np.sign(point1[1]))
    #     x2 = angle_between(x, v2) * int(np.sign(point2[1]))

    #     return x1 - x2

    def unit_vector(vector):
        return vector / np.linalg.norm(vector)

    # def points_to_vectors(point1, point2, center):
    #     v1 = point1 - center
    #     v2 = point2 - center
    #     return v1, v2

    def angle_between(v1, v2):
        v1_u = unit_vector(v1)
        v2_u = unit_vector(v2)
        dot = np.dot(v1_u, v2_u)
        return np.arccos(np.dot(v1_u, v2_u))

    # p1_xz = np.array([p1[0], p1[2]])
    # p2_xz = np.array([p2[0], p2[2]])
    # center_xz = np.array([center[0], center[2]])
    # rot_y = get_rotation(p1_xz, p2_xz, center_xz)
    p1_init = np.array([Config.brow_l[0], Config.brow_l[2]])
    p2_init = np.array([Config.brow_r[0], Config.brow_r[2]])

    p1 = bpy.data.objects.get(get_name_of_object(
        Config.empties_prefix) + '_brow.T.L.001').matrix_world.translation
    p1 = [p1[0], p1[2]]

    p2 = bpy.data.objects.get(get_name_of_object(
        Config.empties_prefix) + '_brow.T.R.001').matrix_world.translation
    p2 = [p2[0], p2[2]]

    v1 = unit_vector(p2_init - p1_init)
    v2 = unit_vector(np.array(p2) - np.array(p1))

    rot_y = angle_between(v1, v2)

    sign = 1
    if p2[1] <= p1[1]:
        sign = -1

    head.rotation_euler.y = rot_y * sign
