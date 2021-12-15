import bpy
from ..config import Config
from ..FaceMeshTracking import get_initial_landmarks, add_landmark_empties, add_group_empty
from mathutils import Vector
import json

def get_cluster_facial_landmarks(landmarks, distances):
    n = len(landmarks)
    weights = []
    for i, dist in enumerate(distances):
        if dist <= 1e-8:
            return Vector(landmarks[i])

        weights.append(1 / dist)
    
    location = Vector()
    for landmark, weight in zip(landmarks, weights):
        landmark = Vector(landmark) * weight
        location += landmark

    location = location / sum(weights)
    return location

class FFMOCAP_OT_initiate_facial_empties(bpy.types.Operator):
    """Initiale Facial Empties"""
    bl_idname = Config.operator_initiate_facial_empties_idname
    bl_label = "FFMoCap Initiate Facial Empties Operator"

    def execute(self, context):
        initial_landmarks = get_initial_landmarks()

        clusters =None     
        with open('facialLandmarksClusteredv2.json', 'r') as f:
            clusters = json.load(f)
        
        cluster_landmarks = []
        for cluster in clusters:
            idxs = list(map(int, cluster.keys()))
            distances = list(cluster.values())
            cluster_points = []
            for idx in idxs:
                try:
                    initial_point = initial_landmarks[idx]
                except Exception:
                    initial_point = None

                if not initial_point is None:
                    cluster_points.append(initial_point)

            cluster_landmarks.append(get_cluster_facial_landmarks(cluster_points, distances))

        props = context.scene.face_transformation_matrix
        props.num_landmarks = len(cluster_landmarks)
        add_landmark_empties(cluster_landmarks, createObject= True)
        add_group_empty(context)

        return {'FINISHED'}