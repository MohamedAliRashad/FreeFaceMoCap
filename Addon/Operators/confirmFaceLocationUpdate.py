from csv import reader as csv_reader
import bpy
import bmesh
from ..config import Config
from ..FaceMeshTracking import get_initial_landmarks, get_face_transformation_matrix
class FFMOCAP_OT_confirm_face_location_update(bpy.types.Operator):
    """Initiale Facial Empties"""
    bl_idname = Config.operator_confirm_face_location_update_idname
    bl_label = "FFMoCap confirm Face Location Update Operator"

    def execute(self, context):
        props = context.scene.face_transformation_matrix
        num_landmarks = props.num_landmarks
        first_empty = bpy.data.objects.get(Config.empties_prefix + str(0), None)

        if first_empty is None:
            self.report({'ERROR'}, 'Empties not initialized.')
            return {'CANCELLED'}
        
        initial_landmarks = get_initial_landmarks()
        new_landmarks = []
        for i in range(num_landmarks):
            new_location = list(bpy.data.objects[Config.empties_prefix + str(i)].location)
            new_landmarks.append(new_location)

        print(len(new_landmarks))
        w = get_face_transformation_matrix(initial_landmarks, new_landmarks)
        props.matrix = w
        print(props.matrix)
        return {'FINISHED'}