from time import sleep
from importlib import import_module
import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from ..config import Config
from ..FaceMeshTracking import plot_mesh, add_landmark_empties, add_group_empty

class FFMOCAP_OT_capture_face(bpy.types.Operator, AddObjectHelper):
    """Tooltip"""
    bl_idname = Config.operator_capture_face_idname
    bl_label = "FFMoCap Capture Operator"

    scale: bpy.props.FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    _timer = None
    _cap  = None
    stop = False

    src = None
    drawing = False

    frame = None
    results = None
    fps = False

    # Webcam resolution:
    width = 640
    height = 480

    cv2 = None
    mp = None

    def init_camera(self):
        if Config.are_dependancies_installed:
            self.np = import_module('numpy')
            self.cv2 = import_module('cv2')
            self.mp = import_module('mediapipe')
            self.mp_face_mesh = self.mp.solutions.face_mesh
        if self._cap is None:
            self._cap = self.cv2.VideoCapture(self.src)
            self._cap.set(self.cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self._cap.set(self.cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self._cap.set(self.cv2.CAP_PROP_BUFFERSIZE, 1)
            sleep(1.0)

    def stop_playback(self, scene):
        print(format(scene.frame_current) + " / " + format(scene.frame_end))
        if scene.frame_current == scene.frame_end:
            bpy.ops.screen.animation_cancel(restore_frame=False)    

    def execute(self, context):
        props = context.scene.ffmocap_props
        self.src = int(props.video_sources_enum)
        self.drawing = props.show_mesh_on_real_face
        if props.show_fps:
            self.fps = True

        bpy.app.handlers.frame_change_pre.append(self.stop_playback)
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        self.init_camera()
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        self.cv2.destroyAllWindows()
        self._cap.release()
        self._cap = None
    
    def modal(self, context, event):
        if (event.type in {'ESC'}) or self.stop == True:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            with self.mp_face_mesh.FaceMesh(
                max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
            ) as face_mesh:
                _, self.frame = self._cap.read()
                self.frame = self.cv2.flip(self.frame, 1)
                self.frame.flags.writeable = False
                self.frame = self.cv2.cvtColor(self.frame, self.cv2.COLOR_BGR2RGB)
                results = face_mesh.process(self.frame)
                if results.multi_face_landmarks:
                    if self.drawing:
                        self.frame = plot_mesh(results, self.frame)
                    landmarks = results.multi_face_landmarks[0].landmark
                    self.results = self.np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks])
                video_fps = 0
                # Get FPS
                if self.fps:
                    video_fps = self._cap.get(self.cv2.CAP_PROP_FPS)
            # Show camera image in a window                     
            img = self.cv2.cvtColor(self.frame, self.cv2.COLOR_BGR2RGB)
            self.cv2.putText(img, f'FPS: {int(video_fps)}', (10,30), self.cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            self.cv2.imshow("Face Mesh Image", img)
            self.cv2.waitKey(1)

            add_landmark_empties(self.results, matrix= context.scene.face_transformation_matrix.matrix)
            
            # add_group_empty(context)

        return {'PASS_THROUGH'}