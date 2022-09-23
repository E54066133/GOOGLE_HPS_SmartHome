import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import os

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
