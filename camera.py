import threading
import cv2
import numpy as np

class Camera():
    def __init__(self):
        self.device = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.WIDTH, self.HEIGHT = 1280, 720
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)

        self.device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.device.set(cv2.CAP_PROP_FPS, 30)
        self.device.set(cv2.CAP_PROP_BUFFERSIZE, 1)


    def getFrame(self):
        ret, frame = self.device.read()
        return frame

    def getResolution(self):
        return self.WIDTH, self.HEIGHT


