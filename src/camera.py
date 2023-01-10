from threading import Thread
import cv2
import numpy as np
import time

class Camera(Thread):
    def __init__(self):
        self.device = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.WIDTH, self.HEIGHT = 0, 0
        self.frame = np.zeros((self.HEIGHT, self.WIDTH, 3), np.uint8)

        #https://stackoverflow.com/questions/55099413/python-opencv-streaming-from-camera-multithreading-timestamps
        self.thread = Thread(target = self.update, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def update(self):
        while True:
            self.status, self.frame = self.device.read()
            time.sleep(0.1)

    def getFrame(self):
        if self.frame is not None:
            return self.frame

    def getResolution(self):
        return self.WIDTH, self.HEIGHT

class C920(Camera):
    def __init__(self):
        self.device = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        self.WIDTH, self.HEIGHT = 1280, 720
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        #self.device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.device.set(cv2.CAP_PROP_FPS, 30)
        self.device.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.device.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        self.device.set(cv2.CAP_PROP_EXPOSURE, -4) #affected if device set to MJPG
        self.frame = np.zeros((self.HEIGHT, self.WIDTH, 3), np.uint8)

        self.thread = Thread(target = self.update, args=())
        self.thread.daemon = True
        self.thread.start()