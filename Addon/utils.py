import cv2
import mediapipe as mp

def plot_mediapipe(results, image, thickness=1, circle_radius=1):

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh
    drawing_spec = mp_drawing.DrawingSpec(thickness=thickness, circle_radius=circle_radius)

    for face_landmarks in results.multi_face_landmarks:

        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
        )
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
        )
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
        )
    return image

def plot_opencv(results, image, text=False):

    for face in results.multi_face_landmarks:
        for i, landmark in enumerate(face.landmark):
            x = landmark.x
            y = landmark.y

            shape = image.shape
            relative_x = int(x * shape[1])
            relative_y = int(y * shape[0])

            cv2.circle(image, (relative_x, relative_y), radius=1, color=(255, 0, 0), thickness=1)
            if text:
                cv2.putText(
                    image,
                    str(i),
                    (relative_x, relative_y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.3,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
    return image
