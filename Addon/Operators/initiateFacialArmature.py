import bpy
import bmesh
import addon_utils
from ..config import Config
from mathutils import Vector
from ..FaceMeshTracking import add_landmark_empties, add_group_empty

def add_armature():
    bpy.ops.object.armature_add()
    arm = bpy.context.active_object
    arm.name = 'FFMoCap_Armature'
    # arm.location = Vector((0, 0, 1))
    Config.num_faces += 1

def get_num_of_faces():
    num = 0
    for obj in bpy.context.scene.objects:
        if 'Armature' in obj.name:
            num += 1
    
    Config.num_faces = num

class FFMOCAP_OT_initiate_facial_armature(bpy.types.Operator):
    """Initiale Facial Armature"""
    bl_idname = Config.operator_initiate_facial_armature_idname
    bl_label = "FFMoCap Initiate Facial Armature Operator"

    def execute(self, context):
        addon = bpy.context.preferences.addons.get('rigify')

        if not addon:
            # Rigify requires default_set=True
            addon_utils.enable('rigify', default_set=True)
        
        get_num_of_faces()
        
        add_armature()
        arm_objs = []
        for obj in bpy.context.scene.objects:
            if obj.name.startswith("FFMoCap_Armature"):
                arm_objs.append(obj)
        
        arm_obj = None
        if Config.num_faces == 0:
            self.report({'ERROR'}, 'Error adding face armature.')
            return {'CANCELLED'}

        elif Config.num_faces == 1:
            arm_idx = None
            for a in arm_objs:
                if a.name == 'FFMoCap_Armature':
                    arm_idx = arm_objs.index(a)
            arm_obj = arm_objs[arm_idx]

        else:
            arm_idx = None
            for a in arm_objs:
                if a.name == f'FFMoCap_Armature.{str(Config.num_faces - 1).zfill(3)}':
                    arm_idx = arm_objs.index(a)
            arm_obj = arm_objs[arm_idx]
        
        del arm_objs

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')

        for bone in arm_obj.data.edit_bones:
            bone.select = True

        bpy.ops.armature.delete()
        bpy.ops.armature.metarig_sample_add(metarig_type= 'faces.super_face')

        bones_locations = []
        unused_bones = ['teeth.T', 'teeth.B', 'tongue', 'tongue.001', 'tongue.002', 'ear.L', 'ear.L.001', 'ear.L.002',
                        'ear.L.003', 'ear.L.004', 'ear.R', 'ear.R.001', 'ear.R.002', 'ear.R.003', 'ear.R.004', 'face', 'jaw']
        for bone in arm_obj.data.edit_bones:
            if not bone.name in unused_bones:
                bones_locations.append(tuple(arm_obj.location + bone.tail))
                bones_locations.append(tuple(arm_obj.location + bone.head))

        new_bone_locations = list(set(bones_locations))

        bpy.ops.object.mode_set(mode='OBJECT')

        add_landmark_empties(new_bone_locations, createObject= True)
        add_group_empty(context)
        # bpy.ops.pose.rigify_generate()
        # rig_objs = []
        # for obj in bpy.context.scene.objects:
        #     if obj.name.startswith("rig"):
        #         rig_objs.append(obj)

        # rig_obj = rig_objs[-1]
        # del rig_objs

        # if Config.num_faces == 1:
        #     rig_obj.name = 'FFMoCap_RIG'
        # else:
        #     rig_obj.name = 'FFMoCap_RIG.'+str(Config.num_faces - 1).zfill(3)
        
        return {'FINISHED'}