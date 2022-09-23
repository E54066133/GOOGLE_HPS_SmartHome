"""
Implementation of Face Recogintion

Credict:
    A lot of code and concept of this implementation is from https://github.com/ageitgey/face_recognition
"""

from picamera import PiCamera
from picamera.array import PiRGBArray
import my_knn
import cv2
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import time



def loadTrain(train_dir):
    """
    Arg:
        train_dir: directory that contains a sub-directory for each known person, with its name.
        Structure:
            <train_dir>
            ├── <person1>
            │   ├── <somename1>.jpeg
            │   ├── <somename2>.jpeg
            │   ├── ...
            ├── <person2>
            │   ├── <somename1>.jpeg
            │   └── <somename2>.jpeg
            └── ...
    Return:
        en_faces(list):The enconding face of each image.
        names(list):The name of ecah image.
    """
    en_faces = []
    names = []
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                print("[WARNING] Image {} not suitable for training: {}".format(img_path, "Didn't find a face" \
                    if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                en_faces.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                names.append(class_dir)
    return en_faces, names

def putText_zh(img, text, xy, color, fontsize=20):
    fontpath = 'NotoSansTC-Regular.otf'
    font = ImageFont.truetype(fontpath, fontsize)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    draw.text(xy, text, fill=color, font=font)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

if __name__ == "__main__":
    IS_TRAINED = True
    TRAIN_DIR = "retrain"
    KNN_DIR = "my_knn_model.clf"
    
    model = my_knn.FRKNN(n_neighbors=4)
    if IS_TRAINED == False:
        #Loading training dataset
        print("No exist KNN model!")
        print("Collecting data")
        en_faces, names = loadTrain(TRAIN_DIR)
        #Training KNN classifier
        s_time = time.time()
        print("Training")
        model.fit(en_faces, names)
        model.save(KNN_DIR)
        f_time = time.time()
        take = f_time-s_time
        print("Training complete! Took:", take, "s")
        IS_TRAINED = True
    else:
        model.load(KNN_DIR)

    # used to calculate FPS
    prev_frame_time = 0
    new_frame_time = 0

    # Get a reference to webcam #0 (the default one)
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    
    process_this_frame = True
    while True:
        # Grab a single frame of video
        

        # RGB color (which face_recognition uses)
        camera.capture(rawCapture, format='bgr')
        image = rawCapture.array
        #Predic
        predictions = model.predict(image, 0.4)

        # Display the results
        for name, (top, right, bottom, left) in predictions:

            # Draw a box around the face
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(image, (left, bottom), (right, bottom +25), (0, 0, 255), cv2.FILLED)
            #font = cv2.FONT_HERSHEY_DUPLEX
            image = putText_zh(image, name, (left + 6, bottom ), (255, 255, 255))
            #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        #for FPS
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = str(int(fps))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

        # Display the resulting image
        cv2.imshow('Video', image)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()






