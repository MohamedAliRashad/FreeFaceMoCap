import bpy
from ..config import Config
from mathutils import Vector
from .numArmatures import get_name_of_object


def add_landmark_empties(landmarks, empties_names, createObject=False):
    """
    Creates/Updates empties controlling the pose bones.

    Args:
    -----
    landmarks: list
        The locations of the empties.

    empties_names: list
        The empties names to create them or update their locations.

    createObject: boolean. Default: False.
        Whether to create new empties or updating their locations.

    Returns:
    -------
    empties:
        The created/updated empties controlling the pose bones.
    """

    if createObject:
        Config.empties_names = empties_names
    empties = []
    for name, loc in zip(Config.empties_names, landmarks):
        if createObject:
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=Vector(loc))
            empty = bpy.context.active_object
            empty.name = get_name_of_object(
                Config.empties_prefix) + '_' + str(name)
            empty.scale = (0.01, 0.01, 0.01)
        else:
            empty = bpy.data.objects[get_name_of_object(
                Config.empties_prefix) + '_' + str(name)]
            empty.location = Vector(loc)
        empties.append(empty)

    return empties


def add_head_empty(rig):
    """
    Creates an empty of the 'head' pose bone.

    Args:
    -----
    rig:
        The rig object.

    Returns:
    -------
    empty:
        The created empty of the 'head' pose bone.
    """

    m_w_eye = rig.convert_space(pose_bone=rig.pose.bones['eye.R'],
                                matrix=rig.pose.bones['eye.R'].matrix,
                                from_space='POSE',
                                to_space='WORLD')

    y_eye = m_w_eye.translation[1]

    m_w = rig.convert_space(pose_bone=rig.pose.bones['head'],
                            matrix=rig.pose.bones['head'].matrix,
                            from_space='POSE',
                            to_space='WORLD')

    head_loc = m_w.translation
    head_loc[1] += y_eye
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=Vector(head_loc))
    empty = bpy.context.active_object
    empty.name = get_name_of_object(Config.empties_prefix) + '_head'
    empty.scale = (0.01, 0.01, 0.01)

    Config.head_loc = head_loc
    return empty
