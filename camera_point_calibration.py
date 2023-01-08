import cv2
import time
import numpy as np
import keyboard
import time

# Camera Initialization
vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
WIDTH, HEIGHT = 1280, 720
vid.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
vid.set(cv2.CAP_PROP_FPS, 30)

ret = False
while not ret:
    ret, f = vid.read()
    if ret and np.sum(f.flatten()) == 0:
        ret = False

cv2.namedWindow("Projector", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
blackDisplay = np.zeros((1080, 1920, 3), np.uint8)
cv2.imshow("Projector", blackDisplay)

#Begin Calibration
calibrationTemplate = cv2.imread(r"C:\Users\amari\Desktop\PiProjector\Template-01.png")
#calibrationTemplate = cv2.resize(calibrationTemplate, (960, 540))
w = calibrationTemplate.shape[1]
h = calibrationTemplate.shape[0]
while True:
    #https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    #New strategy: Take 2 pictures, 1 with and 1 without template, then compare values

    number_comparison_frames = 5
    #calibration_images = np.empty(number_comparison_frames, dtype=object) 

    blended_mask = np.zeros((HEIGHT, WIDTH, 1), np.uint8)
    blended_mask[:] = 255
    for i in range (number_comparison_frames):
        cv2.imshow("Projector", blackDisplay)
        cv2.waitKey(1)
        ret, pictureNoTemplate = vid.read()
        time.sleep(0.2)
        cv2.imshow("Projector", calibrationTemplate)
        cv2.waitKey(1)
        ret, pictureWithTemplate = vid.read()
        time.sleep(0.2)
        
        diff = cv2.absdiff(pictureNoTemplate, pictureWithTemplate)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        threshold = 30  #if abs diff is greater than 10 for each value, then pixel becomes part of the mask.
        imagemask = mask > threshold
        
        new_blended_mask = np.zeros_like(blended_mask, np.uint8)
        new_blended_mask[imagemask] = blended_mask[imagemask]
        blended_mask = new_blended_mask

        '''
        output = np.zeros_like(pictureWithTemplate, np.uint8)
        output[imagemask] = pictureWithTemplate[imagemask]
        cv2.imshow("Difference", output)
        '''
    #cv2.imshow("mask", blended_mask)
    
    
    #output_gray = cv2.cvtColor(blended_mask, cv2.COLOR_BGR2GRAY)
    # Finding Center of mask https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
    ret, binaryMask = cv2.threshold(blended_mask, 127, 255, 0)
    moment = cv2.moments(binaryMask)
    if moment["m00"] > 0:
        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])
        cv2.circle(pictureWithTemplate, (cX, cY), 5, (255, 0, 0), -1)
    
    blended_mask = cv2.resize(blended_mask, (960, 540))
    cv2.imshow("mask", blended_mask)
    pictureWithTemplate = cv2.resize(pictureWithTemplate, (960, 540))
    cv2.imshow("Prediction", pictureWithTemplate)
    
    if cv2.waitKey(1) == ord('q'):
            break


cv2.destroyAllWindows()