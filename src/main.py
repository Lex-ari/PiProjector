import cv2
import time
import numpy as np
import keyboard
import time
import camera
import display
import os

camera = camera.C920()
projector = display.Display(camera)
projector.changeBackground("Template-01.png")
while True:
    projector.changeBackground("Template-01.png")
    time.sleep(0.1)
    projector.changeBackground("Blank")
    time.sleep(0.1)