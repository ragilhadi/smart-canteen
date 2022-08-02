import dlib
import cv2 as cv
import numpy as np

class FacialLandmark:
    def __init__(self):
        self.file_path = "assets/shape_predictor_68_face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.file_path)
        self.lk_params = dict(winSize=(70, 70),
                            maxLevel=50,
                            criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.003)
                            )
        self.optical_go = False
        self.frame_idx = 1
        self.detect_interval = 10
        self.message_text = 'Mendeteksi Wajah'
        self.prev_grey = None
        self.old_points_top_track = None
        self.points_top_track = None
        self.points_center_track = None
        self.points_bottom_track = None
        self.points_first_top = None
        self.points_first_center = None
        self.points_first_bottom = None
        self.command = 0

    def draw_landmarks(self, frame):
        img_gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        faces = self.detector(img_gray, 0)
        old_points_top = 0
        old_points_center = 0
        old_points_bottom = 0

        for face in faces:
                landmarks = self.predictor(img_gray, face)
                x0 = landmarks.part(19).x # Top
                y0 = landmarks.part(19).y
                x1 = landmarks.part(24).x
                y1 = landmarks.part(24).y

                center_x = landmarks.part(30).x  # Center
                center_y = landmarks.part(30).y

                bottom_x = landmarks.part(8).x  # Bottom
                bottom_y = landmarks.part(8).y

                top_x = (x0 + x1) // 2
                top_y = (y0 + y1) // 2
                old_points_top = np.array([[top_x, top_y]], dtype=np.float32)
                old_points_center = np.array([[center_x, center_y]], dtype=np.float32)
                old_points_bottom = np.array([[bottom_x, bottom_y]], dtype=np.float32)
                # trajectories = np.array([old_points_top, old_points_center, old_points_bottom], dtype=np.float32)

                cv.circle(frame, (top_x, top_y), 3, (0,255,0), 3)
                cv.circle(frame, (center_x, center_y), 3, (0, 255, 0), 3)
                cv.circle(frame, (bottom_x, bottom_y), 3, (0, 255, 0), 3)
                # cv.polylines(frame, [np.int32(trajectory) for trajectory in trajectories], False, (0, 255, 0))

        return frame, old_points_top, old_points_center, old_points_bottom

    def detection(self, frame):
        img_gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        faces = self.detector(img_gray, 0)
        self.command = 0
        
        if len(faces) == 1:
            self.message_text = 'Wajah Terdeteksi'
        elif len(faces) == 0:
            self.message_text = 'Tidak Mendeteksi Wajah'
        else:
            self.message_text = f'Terdeteksi {len(faces)} Wajah'
        
        drawing, points_top, points_center, points_bottom = self.draw_landmarks(frame)

        if self.optical_go == True:
            img0, img1 = self.prev_grey, img_gray
            new_points_top, _sts, _err = cv.calcOpticalFlowPyrLK(img0, img1, self.points_top_track, None, **self.lk_params)
            new_points_center, _sts, _err = cv.calcOpticalFlowPyrLK(img0, img1, self.points_center_track, None, **self.lk_params)
            new_points_bottom, _sts, _err = cv.calcOpticalFlowPyrLK(img0, img1, self.points_bottom_track, None, **self.lk_params)
            
            x_top, y_top = new_points_top.ravel()
            x_center, y_center = new_points_center.ravel()
            x_bottom, y_bottom = new_points_bottom.ravel()

            x_top_old, y_top_old = self.points_first_top.ravel()
            x_center_old, y_center_old = self.points_first_center.ravel()
            x_bottom_old, y_bottom_old = self.points_first_bottom.ravel()

            x_top_diff = x_top - x_top_old
            y_top_diff = y_top - y_top_old
            x_center_diff = x_center - x_center_old
            y_center_diff = y_center - y_center_old
            x_bottom_diff = x_bottom - x_bottom_old
            y_bottom_diff = y_bottom - y_bottom_old

            print(x_center_diff)

            if 20 > x_top_diff and 10 < x_top_diff and 20 > x_center_diff and 8 < x_center_diff and 20 > x_bottom_diff and 5 < x_bottom_diff:
                # self.message_text = f"Kepala Ke Kanan {x_top_diff}"
                self.command = 1
            elif -20 < x_top_diff and -10 > x_top_diff and -20 < x_center_diff and -8 > x_center_diff and -20 < x_bottom_diff and -5 > x_bottom_diff:
                # self.message_text = f"Kepala ke Kiri {x_top_diff}"
                self.command = -1
            elif 15 > y_top_diff and 8 < y_top_diff and 15 > y_center_diff and 6 < y_center_diff and 15 > y_bottom_diff and 3 < y_bottom_diff:
                # self.message_text = f"Kepala Ke Bawah {x_top_diff}"
                self.command = -10 #Down
            elif -15 < y_top_diff and -8 > y_top_diff and -15 < y_center_diff and -6 > y_center_diff and -15 < y_bottom_diff and -3 > y_bottom_diff:
                # self.message_text = f"Kepala Ke Atas {x_top_diff}"
                self.command = 10 # Up
            
        

        if self.frame_idx % self.detect_interval == 0:
            self.points_top_track = points_top        
            self.points_center_track = points_center
            self.points_bottom_track = points_bottom
            if len(faces) == 1:
                self.optical_go = True
                self.points_first_top = points_top  
                self.points_first_center = points_center
                self.points_first_bottom = points_bottom
            else:
                self.optical_go = False


        self.frame_idx += 1
        self.prev_grey = img_gray
        #self.old_points_top_track = points_top
            
        return drawing, self.message_text, self.command

    def opticalflow(self, img0, img1, points):
        new_points_top, status, error = cv.calcOpticalFlowPyrLK(img0, img1, points, None, **self.lk_params)
        print(f'points: {new_points_top} status: {status} error: {error}')

        