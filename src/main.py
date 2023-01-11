import cv2
import time
import numpy as np
import keyboard
import time
import camera
import display
import calibration
import os

camera = camera.C920()
projector = display.Display(camera)
while True:
    calibration.doCalibration(camera, projector)
    time.sleep(0.1)
    