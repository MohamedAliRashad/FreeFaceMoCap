from importlib import import_module
import bpy
from ..config import Config
import json
import csv

def get_cluster_facial_landmarks(landmarks, distances):
    np = import_module('numpy')
    n = len(landmarks)
    weights = []
    for i, dist in enumerate(distances):
        if dist <= 1e-8:
            return np.array(landmarks[i])
        else:
            weights.append(1 / dist)

    location = np.zeros((3))
    for landmark, weight in zip(landmarks, weights):
        landmark = np.array(landmark) * weight
        location += landmark

    location = location / sum(weights)
    return location

def transform_landmarks(landmarks, armature, initial= True):
    np = import_module('numpy')
    results = None
    with open('results.json', 'r') as f:
        results = json.load(f)

    landmarks = np.array(landmarks)
    
    if armature is None:
        armature_points = Config.armature_points
    else:
        armature_points = np.array(armature)

    if initial:
        Config.armature_points = armature_points

    # ROTATING
    def rotate_x(points, angle):
        theta = (angle/180.) * np.pi
        rot_matrix = np.array([[1,               0,                 0],
                                [0,np.cos(theta), -np.sin(theta)], 
                                [0,np.sin(theta),  np.cos(theta)]])
        for i,point in enumerate(points):
            points[i,:] = point @ rot_matrix
        
        return points
    
    def rotate_y(points, angle):
        theta = (angle/180.) * np.pi
        rot_matrix = np.array([[np.cos(theta),0,np.sin(theta)],
                                [0               ,1,               0], 
                                [-np.sin(theta),0,np.cos(theta)]])
        for i,point in enumerate(points):
            points[i,:] = point @ rot_matrix
        
        return points
    
    def rotate_z(points, angle):
        theta = (angle/180.) * np.pi
        rot_matrix = np.array([[np.cos(theta),-np.sin(theta),0],
                                [np.sin(theta),np.cos(theta),0], 
                                [0               ,0               ,1]])
        for i,point in enumerate(points):
            points[i,:] = point @ rot_matrix
        
        return points

    landmarks = rotate_x(landmarks, -90)
    landmarks = rotate_z(landmarks, 180)
    landmarks = rotate_y(landmarks, 180)

    # SCALING
    x_scale_armature = np.max(armature_points[:,0]) - np.min(armature_points[:,0])
    y_scale_armature = np.max(armature_points[:,1]) - np.min(armature_points[:,1])
    z_scale_armature = np.max(armature_points[:,2]) - np.min(armature_points[:,2]) + 0.013

    x_scale_landmarks = np.max(landmarks[:,0]) - np.min(landmarks[:,0])
    y_scale_landmarks = np.max(landmarks[:,1]) - np.min(landmarks[:,1])
    z_scale_landmarks = np.max(landmarks[:,2]) - np.min(landmarks[:,2])

    landmarks[:,0] = (landmarks[:,0] * x_scale_armature) / x_scale_landmarks
    landmarks[:,1] = (landmarks[:,1] * y_scale_armature) / y_scale_landmarks
    landmarks[:,2] = (landmarks[:,2] * z_scale_armature) / z_scale_landmarks

    # SHIFTING
    min_x_arm, min_y_arm, min_z_arm = np.min(armature_points[:,0]), np.min(armature_points[:,1]), np.min(armature_points[:,2])
    min_x_lm, min_y_lm, min_z_lm = np.min(landmarks[:,0]), np.min(landmarks[:,1]), np.min(landmarks[:,2])

    landmarks[:,0] += min_x_arm - min_x_lm
    landmarks[:,1] += min_y_arm - min_y_lm
    landmarks[:,2] += min_z_arm - min_z_lm + 0.013

    new_armature_points = []
    for point in results:
        new_armature_points.append(get_cluster_facial_landmarks(landmarks[np.array([int(i) for i in point.keys()])], point.values()))
    
    modifiers = []
    with open('modifiers.csv', 'r') as f:
        r = csv.reader(f, delimiter=',')
        for row in r:
            modifiers.append(row)

    modifiers = np.array(modifiers).astype(np.float64)

    new_armature_points = np.array(new_armature_points) + np.array(modifiers)
    return new_armature_points

# def transform_landmarks(landmarks, armature, initial= True):
#     np = import_module('numpy')
#     landmarks = np.array(landmarks)

#     if initial:
#         armature_points = np.array(armature)
#         Config.initial_landmarks = landmarks
#         W = armature_points.dot(np.linalg.inv(landmarks.T.dot(landmarks)).dot(landmarks.T))
#         landmarks = W@landmarks
#         Config.armature_points = armature_points

#         return landmarks
    
#     else:
#         initial_landmarks = Config.initial_landmarks
#         initial_landmarks = np.append(initial_landmarks, np.ones((initial_landmarks.shape[0], 1)), axis= 1)
#         landmarks = np.append(landmarks, np.ones((landmarks.shape[0], 1)), axis= 1)

#         W_land = (np.linalg.inv(initial_landmarks.T.dot(initial_landmarks))).dot(initial_landmarks.T).dot(landmarks)

#         armature_points = np.append(Config.armature_points, np.ones((Config.armature_points.shape[0], 1)), axis= 1)

#         new_armature_points = armature_points@W_land

#         Config.armature_points = new_armature_points[:, :3]
#         Config.initial_landmarks = landmarks[:, :3]
        
#         return new_armature_points[:, :3]

# def transform_landmarks2(landmarks, armature, initial = True):
#         np = import_module('numpy')
#         landmarks = np.array(landmarks)
#         armature_points = np.array(armature)
        
#         #ROTATING
#         # def rotate_x(points, angle):
#         #     theta = (angle/180.) * np.pi
#         #     rot_matrix = np.array([[1,               0,                 0],
#         #                             [0,np.cos(theta), -np.sin(theta)], 
#         #                             [0,np.sin(theta),  np.cos(theta)]])
#         #     for i,point in enumerate(points):
#         #         points[i,:] = point @ rot_matrix
            
#         #     return points
        
#         # def rotate_y(points, angle):
#         #     theta = (angle/180.) * np.pi
#         #     rot_matrix = np.array([[np.cos(theta),0,np.sin(theta)],
#         #                             [0               ,1,               0], 
#         #                             [-np.sin(theta),0,np.cos(theta)]])
#         #     for i,point in enumerate(points):
#         #         points[i,:] = point @ rot_matrix
            
#         #     return points
        
#         # def rotate_z(points, angle):
#         #     theta = (angle/180.) * np.pi
#         #     rot_matrix = np.array([[np.cos(theta),-np.sin(theta),0],
#         #                             [np.sin(theta),np.cos(theta),0], 
#         #                             [0               ,0               ,1]])
#         #     for i,point in enumerate(points):
#         #         points[i,:] = point @ rot_matrix
            
#         #     return points

#         # landmarks = rotate_x(landmarks, -90)
#         # landmarks = rotate_z(landmarks, 180)
#         # landmarks = rotate_y(landmarks, 180)

#         # # SCALING
#         # x_scale_armature = np.max(armature_points[:,0]) - np.min(armature_points[:,0])
#         # y_scale_armature = np.max(armature_points[:,1]) - np.min(armature_points[:,1])
#         # z_scale_armature = np.max(armature_points[:,2]) - np.min(armature_points[:,2])

#         # x_scale_landmarks = np.max(landmarks[:,0]) - np.min(landmarks[:,0])
#         # y_scale_landmarks = np.max(landmarks[:,1]) - np.min(landmarks[:,1])
#         # z_scale_landmarks = np.max(landmarks[:,2]) - np.min(landmarks[:,2])

#         # landmarks[:,0] = (landmarks[:,0] * x_scale_armature) / x_scale_landmarks
#         # landmarks[:,1] = (landmarks[:,1] * y_scale_armature) / y_scale_landmarks
#         # landmarks[:,2] = (landmarks[:,2] * z_scale_armature) / z_scale_landmarks

#         # min_x_arm, min_y_arm, min_z_arm = np.min(armature_points[:,0]), np.min(armature_points[:,1]), np.min(armature_points[:,2])
#         # min_x_lm, min_y_lm, min_z_lm = np.min(landmarks[:,0]), np.min(landmarks[:,1]), np.min(landmarks[:,2])

#         # landmarks[:,0] += min_x_arm - min_x_lm
#         # landmarks[:,1] += min_y_arm - min_y_lm
#         # landmarks[:,2] += min_z_arm - min_z_lm
        
#         if initial:
#             W = (armature_points).dot(np.linalg.inv(landmarks.T.dot(landmarks)).dot(landmarks.T))
#             landmarks = W@landmarks
#             Config.initial_landmarks = landmarks
        
#         else:
#             shift = landmarks - Config.initial_landmarks
#             min_x_arm = np.min(armature_points[:,0]) + np.min(shift[:, 0])
#             min_y_arm = np.min(armature_points[:,1]) + np.min(shift[:, 1])
#             min_z_arm = np.min(armature_points[:,2]) + np.min(shift[:, 2])

#             min_x_lm, min_y_lm, min_z_lm = np.min(landmarks[:,0]), np.min(landmarks[:,1]), np.min(landmarks[:,2])

#             landmarks[:,0] += min_x_arm - min_x_lm
#             landmarks[:,1] += min_y_arm - min_y_lm
#             landmarks[:,2] += min_z_arm - min_z_lm

#         # SHIFTING
        
#         #     Config.transformation_matrix = W   
#         #     Config.new_armature = armature_points

#         # else:
#         #     W = Config.transformation_matrix
#         #     armature_points = Config.new_armature
#         #     W_shift = W@shift
#         #     # print(armature_points[0])
#         #     # new_arm = np.linalg.inv(W.T.dot(W)).dot(W.T).dot(armature_points)
#         #     # new_arm -= shift

#         #     armature_points = W_shift
#         #     print(armature_points[0])

#         #     W = armature_points.dot(np.linalg.inv(landmarks.T.dot(landmarks)).dot(landmarks.T))
#         #     Config.transformation_matrix = W        
#         #     Config.new_armature = armature_points
#         #     landmarks = W@landmarks

#         return landmarks