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

cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)