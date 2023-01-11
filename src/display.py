import cv2
import time
import numpy as np
import keyboard
import time
import camera
import os
from threading import Thread

class Display(Thread):
    def __init__(self, camera):
        self.TEMPLATE_PATH = r"template_pictures\\"
        self.WIDTH, self.HEIGHT = 1920, 1080
        #cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # this breaks self.update in self.thread

        self.blank = np.zeros((self.HEIGHT, self.WIDTH, 3), np.uint8)
        
        self.camera = camera
        self.CAMERA_X_OFFSET, self.CAMERA_Y_OFFSET = 1344, 690
        self.CAMERA_WIDTH, self.CAMERA_HEIGHT = 426, 240

        # Layers: Background, CameraView, TrackingMask
        self.layers = [self.blank, self.camera.getFrame(), None, None]
        # Threading
        self.thread = Thread(target = self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    
    def update(self):
        while True:
            # Compress layers and imshow
            resultDisplay = self.layers[0]
            self.layers[1] = self.camera.getFrame()
            
            if self.layers[2] is not None: 
                self.layers[1] = cv2.add(self.layers[1], self.layers[2])

            '''
            if self.layers[3] is not None:
                white = np.zeros((720, 1280, 3), np.uint8)
                white[self.layers[3]] = (255, 255, 255)
                cv2.imshow("white", white)
                subtractionMask = cv2.resize(white, (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
                resultDisplay[self.CAMERA_Y_OFFSET : self.CAMERA_Y_OFFSET + self.CAMERA_HEIGHT, 576 : 576 + self.CAMERA_WIDTH] = subtractionMask
                cv2.imshow("subtraction", subtractionMask)
            '''
            
            cameraView = cv2.resize(self.layers[1], (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
            resultDisplay[self.CAMERA_Y_OFFSET : self.CAMERA_Y_OFFSET + self.CAMERA_HEIGHT, self.CAMERA_X_OFFSET : self.CAMERA_X_OFFSET + self.CAMERA_WIDTH] = cameraView
            cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Projector", resultDisplay)
            
            cv2.waitKey(5)
            time.sleep(0.1)
        
    def changeBackground(self, templateName):
        if templateName == "Template-01": self.layers[0] = cv2.imread(self.TEMPLATE_PATH + "Template-01.png")
    
        elif templateName == "Blank": self.layers[0] = self.blank.copy()
    
    def getResolution(self):
        return self.WIDTH, self.HEIGHT

    def updateCameraMask(self, mask):
        self.layers[2] = mask

    def updateCameraSubtraction(self, mask):
        self.layers[3] = mask
