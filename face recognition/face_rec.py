"""
Implementation of Face Recogintion

Credict:
    A lot of code and concept of this implementation is from https://github.com/ageitgey/face_recognition
"""

import my_knn
import cv2
import os
import numpy as np
import time
import my_common_functions as com
import keyboard
import socket
import threading
from picamera import PiCamera

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
# Port to listen on (non-privileged ports are > 1023)
PORT_TRAIN = 5432
PORT_CAPTURE = 4321


TRAIN_DIR = "retrain"
KNN_DIR = "my_knn_model.clf"

#The varible for the first iteration and need to load model.
first_start = True
re_train = False
capture = False
finish_capture = False
names = os.listdir(TRAIN_DIR)
names.extend(["unknown", None])
det_names = [None]*5
threshold = 2
#Pointer for average list.
pointer = 0
final = False
def train_control():
    global re_train
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_TRAIN))
        s.listen()
        while True:
            conn, addr = s.accept()

            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                #Reduntant!
                if data == b'ReTrain':
                    re_train = True
                    conn.send(b"Retraining Model")

def capture_control():
    global capture
    global finish_capture
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT_CAPTURE))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                #Reduntant!
                if data == b'Capture':
                    capture = True
                    while not finish_capture:
                        pass
                    finish_capture = False
                    conn.sendall(b"finish capture")



if __name__ == "__main__":
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    t1 = threading.Thread(target=train_control)
    t2 = threading.Thread(target=capture_control)
    t1.start()
    t2.start()
    print("start")
    while True:
        if re_train:
            model = my_knn.FRKNN(n_neighbors=4)
            #Loading training dataset
            names = os.listdir(TRAIN_DIR)
            names.append("unknown")
            print("Retraining!")
            s_time = time.time()
            print("Collecting data")
            en_faces, names = com.loadTrain(TRAIN_DIR)
            #Training KNN classifier
            print("Training")
            model.fit(en_faces, names)
            model.save(KNN_DIR)
            print("Training complete!")
            print("Took:", time.time()-s_time, "s")
            re_train = False
        elif first_start:
            model = my_knn.FRKNN(n_neighbors=4)
            #The first time need to load the model
            model.load(KNN_DIR)
            first_start = False

        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        if capture == True:
            if os.path.exists("capture.png"):
                os.remove("capture.png")
                os.remove("capture_small.png")
            cv2.imwrite("capture.png", frame)
            small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
            cv2.imwrite("capture_small.png", small_frame)
            capture = False
            finish_capture = True

        # Only process every other frame of video to save time
        #if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        #small_frame = frame
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        #Predic
        predictions = model.predict(rgb_small_frame, 0.35)

        #process_this_frame = not process_this_frame

        #Processing detected names
        if len(predictions) == 1:
            det_names[pointer] = predictions[0][0]
                    
        else:
            det_names[pointer] = None
        with open('person_detected.txt', 'w+') as f:
            for name in names:
                if det_names.count(name) > threshold:
                    f.write(str(name))
                    if name != None:
                        print(name)

        if pointer == 4:
            pointer = 0
        else:
            pointer += 1

        # if key 'q' is pressed
        #if keyboard.is_pressed('q'):
        #    print('You Pressed Q Key! Finish Program')
        #    break  # finishing the loop

# Release handle to the webcam
video_capture.release()
final = True






