import cv2
import time
import numpy as np
import keyboard
import time
import camera
import display
import os

TEMPLATE_PATH = r"template_pictures\\"

def doCalibration(camera, display):
    # Do Camer
    blended_mask = getSubtractedFrames(camera, display, 3, 10)
    display.updateCameraSubtraction(blended_mask)

    foundArea = getTemplateMatching(camera, blended_mask)
    display.updateCameraMask(foundArea)


def getSubtractedFrames(camera, display, number_comparison_frames, threshold):
    #https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    #New strategy: Take 2 pictures, 1 with and 1 without template, then compare values
    CAMERA_WIDTH, CAMERA_HEIGHT = camera.getResolution()
    blended_mask = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 1), np.uint8)
    blended_mask[:] = 255
    for i in range (number_comparison_frames):
        display.changeBackground("Blank")
        time.sleep(0.3)
        pictureNoTemplate = camera.getFrame()
        display.changeBackground("Template-01")
        time.sleep(0.3)
        pictureWithTemplate = camera.getFrame()
        
        diff = cv2.absdiff(pictureNoTemplate, pictureWithTemplate)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        imagemask = mask > threshold #if abs diff is greater than 10 for each value, then pixel becomes part of the mask.
        
        new_blended_mask = np.zeros_like(blended_mask, np.uint8)
        new_blended_mask[imagemask] = blended_mask[imagemask]
        blended_mask = new_blended_mask
    return blended_mask

def getTemplateMatching(camera, blended_mask):
    #template matching https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
    # use blended_mask as recent
    #multi scale template matching https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
    CAMERA_WIDTH, CAMERA_HEIGHT = camera.getResolution()
    template_to_match = cv2.imread(TEMPLATE_PATH + r"CornerPiece.png")
    template_to_match = cv2.cvtColor(template_to_match, cv2.COLOR_BGR2GRAY)
    ret, template_to_match = cv2.threshold(template_to_match, 127, 255, cv2.THRESH_BINARY)
    template_width, template_height = template_to_match.shape[::-1]
    return_edge_mask = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), np.uint8)
    for corner in range(4):
        rotated_template_to_match = template_to_match.copy()
        text = "TL"
        if corner == 1: 
            rotated_template_to_match = cv2.rotate(rotated_template_to_match, cv2.ROTATE_90_CLOCKWISE)
            text = "TR"
        elif corner == 2: 
            rotated_template_to_match = cv2.rotate(rotated_template_to_match, cv2.ROTATE_180)
            text = "BR"
        elif corner == 3: 
            rotated_template_to_match = cv2.rotate(rotated_template_to_match, cv2.ROTATE_90_COUNTERCLOCKWISE)
            text = "BL"
        found = None
        max_val = 0
        scaled_width = 1
        scaled_height = 1
        for scale in np.linspace(0.3, 1.0, 20)[::-1]:
            # Resize
            scaled_width = template_width * scale
            scaled_height = template_height * scale
            resized_template = cv2.resize(rotated_template_to_match, (int(scaled_width), int(scaled_height)))
            res = cv2.matchTemplate(blended_mask, resized_template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if found is None or max_val > found[0]:
                found = (max_val, max_loc, scale)
        if found is not None:
            top_left = found[1]
            bottom_right = (int(top_left[0] + template_width * found[2]), int(top_left[1] + template_height * found[2]))
            cv2.rectangle(return_edge_mask, top_left, bottom_right, (255, 255, 255), 2)
            cv2.putText(return_edge_mask, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(return_edge_mask, str(found[0])[0:4], bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return return_edge_mask



    #output_gray = cv2.cvtColor(blended_mask, cv2.COLOR_BGR2GRAY)
    # Finding Center of mask https://learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
    '''
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
    '''