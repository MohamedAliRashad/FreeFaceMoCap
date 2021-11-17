import cv2
import mediapipe as mp
import time
from threading import Thread
import numpy as np
from pathlib import Path
import utils

class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = time.time()
        return self

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return self._end - self._start

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()

    def stop(self):
        # indicate that the thread should be stopped
        self._end = time.time()


class MediapipeStream:
    def __init__(self, src=0, fps=True, drawing=True):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.mp_face_mesh = mp.solutions.face_mesh
        self.drawing = drawing

        if self.stream is None or not self.stream.isOpened():
            print("Warning: unable to open video source: {}".format(src))
            return

        # initialize frame and the results state
        self.frame = None
        self.results = None

        if fps:
            self.fps = FPS()
        else:
            self.fps = None

        # flag to tell the thread when to stop
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        time.sleep(2)
        if self.fps:
            self.fps.start()
        return self

    def update(self):
        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as face_mesh:
            # keep looping infinitely until the thread is stopped
            while self.stream.isOpened():
                # if the thread indicator variable is set, stop the thread
                if self.stopped:
                    return
                # otherwise, read the next frame from the stream
                _, self.frame = self.stream.read()
                
                self.frame.flags.writeable = False
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(self.frame)
                if self.drawing:
                    self.frame = utils.plot_mediapipe(results, self.frame)
                self.results = np.array([[landmark.x, landmark.y, landmark.z] for landmark in results.multi_face_landmarks[0].landmark])

                # update the fps counter
                if self.fps:
                    self.fps.update()

    def read_landmarks_only(self):
        # return the landmarks most recently read
        return self.results

    def read_all(self):
        # return the frame and landmarks most recently read
        return self.frame, self.results

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        time.sleep(0.1)
        self.stream.release()
        if self.fps:
            self.fps.stop()
            print("Approximate fps: {}".format(self.fps.fps()))


class FaceMeshTracking(object):
    mp_face_mesh = mp.solutions.face_mesh

    def __init__(self, camera_num=2, save_path=Path(__file__).parents[1] / "output"):
        self.cap = cv2.VideoCapture(camera_num)
        self.save_path = save_path
        self.save_path.mkdir(parents=True, exist_ok=True)

    def live(self):
        idx = len(list(self.save_path.glob("*")))
        with self.mp_face_mesh.FaceMesh(
            max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as face_mesh:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)

                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_face_landmarks:
                    image = utils.plot_opencv(results, image)

                # Flip the image horizontally for a selfie-view display.
                cv2.imshow("MediaPipe Face Mesh", cv2.flip(image, 1))
                # cv2.imshow("MediaPipe Face Mesh", image)
                key = cv2.waitKey(5)
                if key == ord("s"):
                    image_path = self.save_path / f"{str(idx).zfill(2)}.png"
                    cv2.imwrite(str(image_path), image)
                    idx += 1
                    print(f"image number {idx} was captured!")
                if key & 0xFF == ord("q"):  # 27:
                    break
                
        self.cap.release()

    def run(self, images):
        num_images = len(list(self.save_path.glob("*")))
        if not isinstance(images, list):
            images = [images]
        # drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        with self.mp_face_mesh.FaceMesh(
            static_image_mode=True, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5
        ) as face_mesh:
            for idx, file in enumerate(images):
                image = cv2.imread(file)
                # Convert the BGR image to RGB before processing.
                results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                # Print and draw face mesh landmarks on the image.
                if not results.multi_face_landmarks:
                    continue
                annotated_image = image.copy()

                annotated_image = utils.plot_opencv(results, annotated_image)
                image_path = self.save_path / f"{str(idx+num_images).zfill(2)}.png"
                print(image_path)
                cv2.imwrite(str(image_path), annotated_image)

if __name__ == "__main__":
    # face = FaceMeshTracking()
    # face.live()

    stream = MediapipeStream(src=2, fps=False)
    stream.start()
    while True:
        frame, landmarks = stream.read_all()
        print(landmarks[:,-1])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.imshow("MediaPipe Face Mesh", frame)
        if cv2.waitKey(5) & 0xFF == ord("q"):  # 27:
            stream.stop()
            break
