import bpy
import bmesh
import addon_utils
from ..config import Config
from mathutils import Vector
from importlib import import_module
from ..FaceMeshTracking import get_initial_landmarks, add_landmark_empties, add_group_empty, transform_landmarks, \
    get_face_bones, add_head_empty, get_num_of_armatures, get_name_of_object


class FFMOCAP_OT_generate_rig(bpy.types.Operator):
    """Initiale Facial Armature"""
    bl_idname = Config.operator_generate_rig_idname
    bl_label = "FFMoCap Generate Rig Operator"

    def execute(self, context):
        get_num_of_armatures()

        arm_obj = None
        if Config.num_armatures == 0:
            self.report({'ERROR'}, 'Please create a new armature first.')
            return {'CANCELLED'}

        else:
            arm_obj = bpy.data.objects.get(
                get_name_of_object(Config.armature_prefix))

        bpy.ops.pose.rigify_generate()
        rig_obj = context.active_object
        rig_obj.name = get_name_of_object(Config.rig_prefix)
        rig = rig_obj.data
        rig.name = get_name_of_object(Config.rig_data_prefix)
        bpy.data.collections.get(
            "WGTS_rig").name = get_name_of_object("WGTS_rig_")

        used_bones = get_face_bones()
        # arm_obj.hide_set(True)

        # bpy.ops.object.mode_set(mode='POSE')
        rig.layers = [True] * 4 + [False] * (len(rig.layers) - 4)

        pose_bones_locations = []
        pose_bones_names = []

        for bone in rig_obj.pose.bones:
            if bone.name in used_bones:
                m_w = rig_obj.convert_space(pose_bone=bone,
                                            matrix=bone.matrix,
                                            from_space='POSE',
                                            to_space='WORLD')
                if bone.name == 'nose':
                    Config.nose_loc = m_w.translation
                elif bone.name == 'brow.T.R.001':
                    Config.brow_r = m_w.translation
                elif bone.name == 'brow.T.L.001':
                    Config.brow_l = m_w.translation
                pose_bones_names.append(bone.name)
                pose_bones_locations.append(m_w.translation)

        bpy.ops.object.mode_set(mode='OBJECT')

        landmarks = transform_landmarks(
            get_initial_landmarks(), pose_bones_locations)
        empties = add_landmark_empties(
            landmarks, pose_bones_names, createObject=True)
        head_empty = add_head_empty(rig_obj)
        empties.append(head_empty)
        add_group_empty(empties)

        for empty in empties:
            bone_name = empty.name.split('_')[-1]
            bone = rig_obj.pose.bones.get(bone_name)
            if bone_name == 'head':
                constraint2 = bone.constraints.new('TRACK_TO')
                constraint2.target = empty
                constraint2.track_axis = 'TRACK_Z'

                constraint1 = bone.constraints.new('COPY_ROTATION')
                constraint1.target = empty
                constraint1.mix_mode = 'REPLACE'
                constraint1.euler_order = 'XYZ'
                constraint1.use_x = False
                constraint1.use_z = False

            else:
                constraint = bone.constraints.new('COPY_LOCATION')
                constraint.target = empty
                constraint.use_y = False

        return {'FINISHED'}
