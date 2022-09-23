"""
Implementation of Face Recogintion

Credict:
    A lot of code and concept of this implementation is from https://github.com/ageitgey/face_recognition
"""

import my_knn
import cv2
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import time
import my_common_functions as com


if __name__ == "__main__":
    IS_TRAINED = True
    TRAIN_DIR = "my_dataset/train"
    KNN_DIR = "my_knn_model.clf"

    model = my_knn.FRKNN(n_neighbors=4)
    if IS_TRAINED == False:
        #Loading training dataset
        print("No exist KNN model!")
        s_time = time.time()
        print("Collecting data")
        en_faces, names = com.loadTrain(TRAIN_DIR)
        #Training KNN classifier
        print("Training")
        model.fit(en_faces, names)
        model.save(KNN_DIR)
        print("Training complete!")
        print("Took:", time.time()-s_time, "s")
        IS_TRAINED = True
    else:
        model.load(KNN_DIR)

    # used to calculate FPS
    prev_frame_time = 0
    new_frame_time = 0

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frame = cv2.rotate(frame, cv2.ROTATE_180)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            #Predic
            predictions = model.predict(rgb_small_frame, 0.45)

        process_this_frame = not process_this_frame

        # Display the results
        for name, (top, right, bottom, left) in predictions:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom +25), (0, 0, 255), cv2.FILLED)
            #font = cv2.FONT_HERSHEY_DUPLEX
            frame = com.putText_zh(frame, name, (left + 6, bottom ), (255, 255, 255))
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        #for FPS
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = str(int(fps))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, fps, (7, 70), font, 2, (100, 255, 0), 3, cv2.LINE_AA)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()






