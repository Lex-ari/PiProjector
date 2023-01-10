import cv2
import time
import numpy as np
import keyboard
import time
import camera

# Camera Initialization
vid = camera.Camera()

calibrationTemplate = cv2.imread(r"C:\Users\amari\Desktop\PiProjector\Template-01.png")
cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("Projector", calibrationTemplate)
blackDisplay = np.zeros((1080, 1920, 3), np.uint8)

#Begin Calibration
while True:
    cv2.imshow("Projector", blackDisplay)
    cv2.waitKey(1)
    time.sleep(0.3)
    pictureNoTemplate = vid.getFrame()
    cv2.imshow("noTemplate", pictureNoTemplate)
    cv2.waitKey(1)
    cv2.imshow("Projector", calibrationTemplate)
    cv2.waitKey(1)
    time.sleep(0.3)
    pictureWithTemplate = vid.getFrame()
    cv2.imshow("WithTemplate", pictureWithTemplate)
    cv2.waitKey(1)
