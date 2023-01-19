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

        # Layers: 
        # 0 = Background
        # 1 = CameraView
        # 2 = Template Matching Mask
        # 3 = Subtraction Mask
        self.layers = [self.blank, self.camera.getFrame(), None, None]
        # Threading
        self.thread = Thread(target = self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    #
    # Blends all layers of image to show as one image under "Projector" window.
    #
    def update(self):
        while True:
            compressedDisplay = self.layers[0].copy()
            
            self.__updateCameraAndMask(compressedDisplay, showMask = True)
            #self.__updateSubtractionMask(compressedDisplay)

            cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Projector", compressedDisplay)
            
            cv2.waitKey(1)
            time.sleep(0.1)
    
    #
    # Retrieves a frame from camera and resizes it into the compressedDisplay
    # showMask = True in order to see template matching boxes, prediction center, and correlation coefficients.
    #
    def __updateCameraAndMask(self, compressedDisplay, showMask):
        self.layers[1] = self.camera.getFrame()
        if showMask and self.layers[2] is not None: 
            self.layers[1] = cv2.add(self.layers[1], self.layers[2]) 
        cameraView = cv2.resize(self.layers[1], (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
        compressedDisplay[self.CAMERA_Y_OFFSET : self.CAMERA_Y_OFFSET + self.CAMERA_HEIGHT, self.CAMERA_X_OFFSET : self.CAMERA_X_OFFSET + self.CAMERA_WIDTH] = cameraView
    
    #
    # Shows subtraction mask and resizes it into compressedDispaly.
    #
    def __updateSubtractionMask(self, compressedDisplay):
        if self.layers[3] is not None:
            subtractionMask = cv2.resize(self.layers[3], (self.CAMERA_WIDTH, self.CAMERA_HEIGHT))
            cv2.rectangle(subtractionMask, (0, 0), (self.CAMERA_WIDTH, self.CAMERA_HEIGHT), (255, 255, 255), 2)
            merged_subtraction_mask = cv2.merge((subtractionMask, subtractionMask, subtractionMask))
            compressedDisplay[self.CAMERA_Y_OFFSET : self.CAMERA_Y_OFFSET + self.CAMERA_HEIGHT, 150 : 150 + self.CAMERA_WIDTH] = merged_subtraction_mask

    #
    # Changes fullscreen background to blank or different types of template by name.
    #
    def changeBackground(self, templateName):
        if templateName == "Template-01": self.layers[0] = cv2.imread(self.TEMPLATE_PATH + "Template-01.png")
    
        elif templateName == "Blank": self.layers[0] = self.blank.copy()
    
    def getResolution(self):
        return self.WIDTH, self.HEIGHT

    #
    # Updates mask that is used in lower-right mini camera view and tracking
    #
    def updateCameraMask(self, mask, center_coord):
        y_intersect, x_intersect = center_coord
        mask_with_prediction = cv2.circle(mask, (x_intersect, y_intersect), 50, (255, 0, 0), 5)
        self.layers[2] = mask

    def updateCameraSubtraction(self, mask):
        self.layers[3] = mask
    
