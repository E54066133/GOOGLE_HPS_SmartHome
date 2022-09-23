import my_knn
import cv2
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
from PIL import ImageFont, ImageDraw, Image

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

def show_prediction_labels_on_image(img_path, predictions):
    """
    Shows the face recognition results visually.

    :param img_path: path to image to be recognized
    :param predictions: results of the predict function
    :return:
    """
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # There's a bug in Pillow where it blows up with non-UTF-8 text
        # when using the default bitmap font

        #name = name.encode("UTF-8")
        fontpath = 'NotoSansTC-Regular.otf'
        font = ImageFont.truetype(fontpath, 20)
        # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name, font= font)

        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255), font= font)

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    pil_image.show()

if __name__ == "__main__":
    IS_TRAINED = True
    TRAIN_DIR = "my_dataset/train"
    TEST_DIR = "my_dataset/test"
    KNN_DIR = "my_knn_model.clf"

    model = my_knn.FRKNN()
    if IS_TRAINED == False:
        #Loading training dataset
        print("No exist KNN model!")
        print("Collecting data")
        en_faces, names = loadTrain(TRAIN_DIR)
        #Training KNN classifier
        print("Training")
        model.fit(en_faces, names)
        model.save(KNN_DIR)
        print("Training complete!")
        IS_TRAINED = True
    else:
        model.load(KNN_DIR)

    for image_file in os.listdir(TEST_DIR):
        full_file_path = os.path.join(TEST_DIR, image_file)

        print("Looking for faces in {}".format(image_file))

        # Find all people in the image using a trained classifier model
        # Note: You can pass in either a classifier file name or a classifier model instance
        X_img = face_recognition.load_image_file(full_file_path)
        predictions = model.predict(X_img, 0.45)

        # Print results on the console
        for name, (top, right, bottom, left) in predictions:
            print("- Found {} at ({}, {})".format(name, left, top))

        # Display results overlaid on an image
        show_prediction_labels_on_image(os.path.join(TEST_DIR, image_file), predictions)







