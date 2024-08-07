


from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        while True:
            ret, frame = self.video.read()
            if not ret:
                continue
            
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Perform face detection
            results = self.face_detection.process(frame_rgb)
            
            # Draw face detections on the frame
            if results.detections:
                for detection in results.detections:
                    self.mp_drawing.draw_detection(frame, detection)
            
            # Convert frame back to BGR format for OpenCV
            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            
            # Encode the frame in JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame_bgr)
            
            if not ret:
                continue
            
            # Yield the frame in bytes
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('desktop-2.html')

def gen(camera):
    for frame in camera.get_frame():
        yield frame

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
# # from flask import Flask, render_template

# # app = Flask(__name__)

# # @app.route('/')
# # def index():
# #     return render_template('desktop-2.html')

# # if __name__ == '__main__':
# #     app.run(debug=True)

# # import cv2
# # from time import time
# # import pickle as pk
# # import mediapipe as mp
# # import pandas as pd
# # import pyttsx4
# # import multiprocessing as mtp
# # from recommendations import check_pose_angle
# # from landmarks import extract_landmarks
# # from calc_angles import rangles

# # class YogaPoseDetector:
# #     def __init__(self):
# #         self.cam = self.init_cam()
# #         self.model = pk.load(open(r'C:\research_paper\research paper\yoga-pose-detection-correction-main\models\poses.model', "rb"))
# #         self.cols, self.landmarks_points_array = self.init_dicts()
# #         self.angles_df = pd.read_csv(r'C:\research_paper\research paper\yoga-pose-detection-correction-main\csv_files\poses_angles.csv')
# #         self.mp_drawing = mp.solutions.drawing_utils
# #         self.mp_pose = mp.solutions.pose
# #         self.tts_q = mtp.JoinableQueue()
# #         self.tts_proc = mtp.Process(target=self.tts, args=())
# #         self.tts_proc.start()
# #         self.tts_last_exec = time() + 5

# #     def init_cam(self):
# #         cam = cv2.VideoCapture(0)
# #         cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# #         cam.set(cv2.CAP_PROP_FOCUS, 360)
# #         cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
# #         cam.set(cv2.CAP_PROP_SHARPNESS, 125)
# #         cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# #         cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# #         return cam

# #     def init_dicts(self):
# #         landmarks_points = {
# #             "nose": 0,
# #             "left_shoulder": 11, "right_shoulder": 12,
# #             "left_elbow": 13, "right_elbow": 14,
# #             "left_wrist": 15, "right_wrist": 16,
# #             "left_hip": 23, "right_hip": 24,
# #             "left_knee": 25, "right_knee": 26,
# #             "left_ankle": 27, "right_ankle": 28,
# #             "left_heel": 29, "right_heel": 30,
# #             "left_foot_index": 31, "right_foot_index": 32,
# #         }
# #         landmarks_points_array = {
# #             "left_shoulder": [], "right_shoulder": [],
# #             "left_elbow": [], "right_elbow": [],
# #             "left_wrist": [], "right_wrist": [],
# #             "left_hip": [], "right_hip": [],
# #             "left_knee": [], "right_knee": [],
# #             "left_ankle": [], "right_ankle": [],
# #             "left_heel": [], "right_heel": [],
# #             "left_foot_index": [], "right_foot_index": [],
# #         }
# #         col_names = []
# #         for i in range(len(landmarks_points.keys())):
# #             name = list(landmarks_points.keys())[i]
# #             col_names.append(name + "_x")
# #             col_names.append(name + "_y")
# #             col_names.append(name + "_z")
# #             col_names.append(name + "_v")
# #         cols = col_names.copy()
# #         return cols, landmarks_points_array

# #     def tts(self):
# #         engine = pyttsx4.init()
# #         while True:
# #             objects = self.tts_q.get()
# #             if objects is None:
# #                 break
# #             message = objects[0]
# #             engine.say(message)
# #             engine.runAndWait()
# #         self.tts_q.task_done()

# #     def cv2_put_text(self, image, message):
# #         cv2.putText(
# #             image,
# #             message,
# #             (50, 50),
# #             cv2.FONT_HERSHEY_SIMPLEX,
# #             2,
# #             (255, 0, 0),
# #             5,
# #             cv2.LINE_AA
# #         )

# #     def destory(self):
# #         cv2.destroyAllWindows()
# #         self.cam.release()
# #         self.tts_q.put(None)
# #         self.tts_q.close()
# #         self.tts_q.join_thread()
# #         self.tts_proc.join()

# #     def detect_yoga_pose(self):
# #         result, image = self.cam.read()
# #         flipped = cv2.flip(image, 1)
# #         resized_image = cv2.resize(
# #             flipped,
# #             (640, 360),
# #             interpolation=cv2.INTER_AREA
# #         )
# #         key = cv2.waitKey(1)
# #         if key == ord("q"):
# #             self.destory()
# #             return "Camera destroyed"
# #         if result:
# #             err, df, landmarks = extract_landmarks(
# #                 resized_image,
# #                 self.mp_pose,
# #                 self.cols
# #             )
# #             if err == False:
# #                 prediction = self.model.predict(df)
# #                 probabilities = self.model.predict_proba(df)
# #                 self.mp_drawing.draw_landmarks(
# #                     flipped,
# #                     landmarks,
# #                     self.mp_pose.POSE_CONNECTIONS
# #                 )
# #                 if probabilities[0, prediction[0]] > 0.85:
# #                     self.cv2_put_text(
# #                         flipped,
# #                         self.get_pose_name(prediction[0])
# #                     )
# #                     angles = rangles(df, self.landmarks_points_array)
# #                     suggestions = check_pose_angle(
# #                         prediction[0], angles, self.angles_df)
# #                     if time() > self.tts_last_exec:
# #                         self.tts_q.put([
# #                             suggestions[0]
# #                         ])
# #                         self.tts_last_exec = time() + 5
# #                 else:
# #                     self.cv2_put_text(
# #                         flipped,
# #                         "No Pose Detected"
# #                     )
# #             cv2.imshow("Frame", flipped)
# #             return "Pose detected"

# #     def get_pose_name(self, index):
# #         names = {
# #             0: "downdog",
# #             1:"goddess",
# #             2:"padmasana",
# #             3:"phalakasana",
# #             4:"virabhadrasana ii",
# #             5:"vriksasana"
# #         }
# #         return str(names[index])

# # # Usage in Flask app
# # from flask import Flask, render_template, Response

# # app = Flask(__name__)
# # pose_detector = YogaPoseDetector()

# # @app.route('/')
# # def index():
# #     return render_template('index.html')  # Assuming you have an index.html file

# # def gen():
# #     while True:
# #         frame = pose_detector.detect_yoga_pose()
# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# # @app.route('/video_feed')
# # def video_feed():
# #     return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# # if __name__ == '__main__':
# #     app.run(debug=True)
# from flask import Flask, render_template, Response
# from camera import VideoCamera
# app = Flask(__name__)

#                                                                #render home.html

# @app.route('/')
# def index():
#     return render_template('index.html')                                                                   #render index.html



# @app.route('/video_frame')
# def gen(camera):
#     while True:
#         frame =VideoCamera.get_frame(camera)  
#                                                                     #call get_frame() function from camera
#         yield (b'--frame\r\n'                                                   #also shows image in bytes format to normal format ;)
#                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         return frame,camera.video
    
# # def video_feed():
# #     return Response(gen(VideoCamera()),
# #                     mimetype='multipart/x-mixed-replace; boundary=frame')       #mimetype is for the browser, we are basically letting browser what type of file it is


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='5000', debug=True)
