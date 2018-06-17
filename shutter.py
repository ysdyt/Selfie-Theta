# -*- coding: utf-8 -*-
import cv2
import sys
import datetime as dt
import time
from time import sleep


cascPath = './haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# initialize
video_capture = cv2.VideoCapture(0)
anterior = 0
shot_dense = 0.5
considerable_frames = 20
prev_faces = []
prev_shot = None


while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    ret, org_frame = video_capture.read()
    
    shape = org_frame.shape

    ratio = 3

    frame = cv2.resize(org_frame, (shape[1]/ratio,shape[0]/ratio))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect face
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30/ratio, 30/ratio)
    )
    print prev_faces, prev_shot

    if prev_shot is None or (dt.datetime.now() - prev_shot).seconds > 3:
        prev_faces.append(len(faces))
        if len(prev_faces) > considerable_frames:
            drops = len(prev_faces) - considerable_frames
            prev_faces = prev_faces[drops:]
        dense = sum([1 for i in prev_faces if i > 0]) / float(len(prev_faces))

        if len(prev_faces) >= considerable_frames and dense >= shot_dense:
            print 'shot',str(dt.datetime.now())
            save_fig_name = '/home/pi/face_detect/save_fig/{}.jpg'.format(dt.datetime.now())
            cv2.imwrite(save_fig_name,org_frame)
            
            print 'hogeeeeeeeeeeeee'

            prev_faces = []
            prev_shot = dt.datetime.now()

    # 顔検出領域を四角で囲む
    for (x, y, w, h) in faces:
        x_ = x*ratio
        y_ = y*ratio
        x_w_ = (x+w)*ratio
        y_h_ = (y+h)*ratio
        cv2.rectangle(org_frame, (x_, y_), (x_w_, y_h_), (0, 255, 0), 2)

    # 'q'を押したら検出処理を終える
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # 接続しているモニターにリアルタイムで画像を描写する（カメラで撮っている動画を表示する）
    cv2.imshow('Video', org_frame)

# 全てが完了したらプロセスを終了
video_capture.release()
cv2.destroyAllWindows()
