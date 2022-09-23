import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition

class FRKNN:
    """
    Face recognition with KNN.
    """
    def __init__(self, n_neighbors=3, knn_algo='ball_tree') -> None:
        self.knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, \
            algorithm=knn_algo, weights='distance')

    def fit(self, x, y):
        self.knn_clf.fit(x, y)

    def predict(self, image, distance_threshold=0.6):
        """
        Args:
            image: need in RGB format
            distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
            of mis-classifying an unknown person as a known one.
        Return:
            a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
        """
        X_face_locations = face_recognition.face_locations(image)
        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            return []
        faces_encodings = face_recognition.face_encodings(image, known_face_locations=X_face_locations)
        # Use the KNN model to find the best matches for the test face
        closest_distances = self.knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(self.knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


    def load(self, PATH):
        with open(PATH, 'rb') as f:
            self.knn_clf = pickle.load(f)

    def save(self, PATH):
        with open(PATH, 'wb') as f:
            pickle.dump(self.knn_clf, f)
