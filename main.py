# -*- coding: utf-8 -*-
import cv2
import datetime as dt
import os
from time import sleep

from theta_shutter import theta_api


# make dir path
save_dir = './saved_dir'

theta_img_path = os.path.join(save_dir, 'theta_img')
webcam_img_path = os.path.join(save_dir, 'webcam_img')

if not os.path.exists(save_dir):
    os.makedirs(theta_img_path)
    os.makedirs(webcam_img_path)

# set features for face-detect
cascPath = './facedetect_features/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# initialize
video_capture = cv2.VideoCapture(0)
anterior = 0
shot_dense = 0.5
considerable_frames = 60
prev_faces = []
prev_shot = None
img_ratio = 3
dead_time = 3

while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    _, org_frame = video_capture.read()
    shape = org_frame.shape

    frame = cv2.resize(org_frame, (int(shape[1]/img_ratio), int(shape[0]/img_ratio)))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect face
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(int(30/img_ratio), int(30/img_ratio))
    )
    print(prev_faces)

    if prev_shot is None or (dt.datetime.now() - prev_shot).seconds > dead_time:
        prev_faces.append(len(faces))
        if len(prev_faces) > considerable_frames:
            drops = len(prev_faces) - considerable_frames
            prev_faces = prev_faces[drops:]
        dense = sum([1 for i in prev_faces if i > 0]) / float(len(prev_faces))

        if len(prev_faces) >= considerable_frames and dense >= shot_dense:
            print('shot', str(dt.datetime.now()))
            save_fig_name = os.path.join(webcam_img_path, '{}.jpg'.format(dt.datetime.now()))
            #cv2.imwrite(save_fig_name, org_frame)

            # take theta photo
            theta_api(theta_img_path)

            prev_faces = []
            prev_shot = dt.datetime.now()

    # visualize detected area
    for (x, y, w, h) in faces:
        x_ = x*img_ratio
        y_ = y*img_ratio
        x_w_ = (x+w)*img_ratio
        y_h_ = (y+h)*img_ratio
        cv2.rectangle(org_frame, (x_, y_), (x_w_, y_h_), (0, 255, 0), 2)

    # push 'q' to stop process
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # show real-time capturing
    cv2.imshow('Video', org_frame)

# finish process
video_capture.release()
cv2.destroyAllWindows()
