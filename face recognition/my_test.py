from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(rawCapture, format='bgr')
image = rawCapture.array

cv2.imshow("Image", image)
cv2.waitKey(0)
