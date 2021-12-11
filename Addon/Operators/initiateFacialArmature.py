import bpy
import bmesh
import addon_utils
from ..config import Config
from mathutils import Vector

def add_armature():
    bpy.ops.object.armature_add()
    arm = bpy.context.active_object
    arm.name = 'FFMoCap_Armature'
    Config.num_face_armatures += 1


class FFMOCAP_OT_initiate_facial_armature(bpy.types.Operator):
    """Initiale Facial Armature"""
    bl_idname = Config.operator_initiate_facial_armature_idname
    bl_label = "FFMoCap Initiate Facial Armature Operator"

    def execute(self, context):
        addon = bpy.context.preferences.addons.get('rigify')

        if not addon:
            # Rigify requires default_set=True
            addon_utils.enable('rigify', default_set=True)
        
        add_armature()
        arm_objs = []
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("FFMoCap_Armature"):
                arm_objs.append(obj)
        
        arm_obj = None
        if Config.num_face_armatures == 0:
            self.report({'ERROR'}, 'Error adding face armature.')
            return {'CANCELLED'}

        elif Config.num_face_armatures == 1:
            arm_idx = None
            for a in arm_objs:
                if a.name == 'FFMoCap_Armature':
                    arm_idx = arm_objs.index(a)
            arm_obj = arm_objs[arm_idx]

        else:
            arm_idx = None
            for a in arm_objs:
                if a.name == f'FFMoCap_Armature.{str(Config.num_face_armatures - 1).zfill(3)}':
                    arm_idx = arm_objs.index(a)
            arm_obj = arm_objs[arm_idx]
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')

        for bone in arm_obj.data.edit_bones:
            bone.select = True

        bpy.ops.armature.delete()
        bpy.ops.armature.metarig_sample_add(metarig_type= 'faces.super_face')

        bpy.ops.object.mode_set(mode='OBJECT')

        bpy.ops.pose.rigify_generate()
        rig_objs = []
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("rig"):
                rig_objs.append(obj)

        rig_obj = rig_objs[-1]
        if Config.num_face_armatures == 1:
            rig_obj.name = 'FFMoCap_RIG'
        else:
            rig_obj.name = 'FFMoCap_RIG.'+str(Config.num_face_armatures - 1).zfill(3)
        
        return {'FINISHED'}