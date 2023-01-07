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
blackDisplay = np.zeros((1920, 1080, 3), np.uint8)
cv2.imshow("Projector", blackDisplay)

#Begin Calibration
calibrationTemplate = cv2.imread(r"C:\Users\amari\Desktop\PiProjector\Template-01.png")
w = calibrationTemplate.shape[1]
h = calibrationTemplate.shape[0]

while True:
    #https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    #New strategy: Take 2 pictures, 1 with and 1 without template, then compare values

    time.sleep(0.3)
    ret, pictureNoTemplate = vid.read()
    cv2.imshow("Projector", calibrationTemplate)
    cv2.waitKey(1)
    time.sleep(0.3)
    ret, pictureWithTemplate = vid.read()
    cv2.imshow("Projector", blackDisplay)
    
    
    diff = cv2.absdiff(pictureNoTemplate, pictureWithTemplate)
    mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    threshold = 10  #if abs diff is greater than 10 for each value, then pixel becomes part of the mask.
    imagemask = mask > threshold

    output = np.zeros_like(pictureWithTemplate, np.uint8)
    output[imagemask] = pictureWithTemplate[imagemask]
    cv2.imshow("Difference", output)

    # Color masking to prevent image changes that aren't green
    output_hsv = cv2.cvtColor(output, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 0, 0], dtype = "uint8")
    upper_green = np.array([80, 255, 255], dtype = "uint8")
    greenColorMask = cv2.inRange(output_hsv, lower_green, upper_green)
    cv2.imshow("Mask", greenColorMask)

    # Finding Center of mask https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
    ret, binaryMask = cv2.threshold(greenColorMask, 127, 255, 0)
    moment = cv2.moments(binaryMask)
    if moment["m00"] > 0:
        cX = int(moment["m10"] / moment["m00"])
        cY = int(moment["m01"] / moment["m00"])
        cv2.circle(pictureWithTemplate, (cX, cY), 5, (0, 0, 255), -1)
    cv2.imshow("Prediction", pictureWithTemplate)

    if cv2.waitKey(1) == ord('q'):
            break


cv2.destroyAllWindows()