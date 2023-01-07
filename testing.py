import cv2
import time
import numpy as np
import keyboard
import time

# Camera Initialization
vid = cv2.VideoCapture(0)
ret = False
while not ret:
    ret, f = vid.read()
    if ret and np.sum(f.flatten()) == 0:
        ret = False

calibrationTemplate = cv2.imread(r"C:\Users\amari\Desktop\PiProjector\Template-01.png")
cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("Projector", calibrationTemplate)

#Begin Calibration


while True:
    ret, img = vid.read()
    output_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 0, 50], dtype = "uint8")
    upper_green = np.array([80, 255, 255], dtype = "uint8")


    greenColorMask = cv2.inRange(output_hsv, lower_green, upper_green)
    cv2.imshow("Mask", greenColorMask)


    if cv2.waitKey(1) == ord('q'):
            break