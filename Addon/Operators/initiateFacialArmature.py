import bpy
import bmesh
import addon_utils
from ..config import Config
from mathutils import Vector

def add_armature():
    bpy.ops.object.armature_add()
    arm = bpy.context.active_object
    arm.name = 'FFMoCap_Armature'


class FFMOCAP_OT_initiate_facial_armature(bpy.types.Operator):
    """Initiale Facial Armature"""
    bl_idname = Config.operator_initiate_facial_armature_idname
    bl_label = "FFMoCap Initiate Facial Armature Operator"

    def execute(self, context):
        addon = bpy.context.preferences.addons.get('rigify')

        if not addon:
            # Rigify requires default_set=True
            addon_utils.enable('rigify', default_set=True)
        
        is_arm_found = False
        try:
            bpy.data.objects['FFMoCap_Armature']
            is_arm_found = True
        except Exception:
            is_arm_found = False

        if is_arm_found:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.data.objects['FFMoCap_Armature'].select_set(True)
            bpy.ops.object.delete()
            add_armature()

        else:
            add_armature()
        
        arm_obj = bpy.data.objects['FFMoCap_Armature']
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')

        for bone in arm_obj.data.edit_bones:
            bone.select = True

        bpy.ops.armature.delete()
        bpy.ops.armature.metarig_sample_add(metarig_type= 'faces.super_face')

        # arm_obj.location += Vector((0, 0, 1))
        arm_obj.scale = (2.5, 2.5, 2.5)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}