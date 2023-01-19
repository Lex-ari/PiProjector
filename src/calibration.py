import cv2
import time
import numpy as np
import keyboard
import time
import camera
import display
import os

TEMPLATE_PATH = r"template_pictures\\"

#
# Method to be called outside to handle calibration methods, such as image subtraction and template matching.
#
def doCalibration(camera, display):
    # Do Camer
    blended_mask = getSubtractedFrames(camera, display, 3, 10)
    display.updateCameraSubtraction(blended_mask)

    edge_mask, corners = getTemplateMatching(camera, blended_mask)
    y_center, x_center = getCenterCoordinates(camera, corners)
    display.updateCameraMask(edge_mask, (y_center, x_center))
    

#
# Takes a picture without and with the template, subtracts anything that is similar (using a threshold) so that differences show.
# Repeats number_comparison_frames times. Takes differences of each group for one final blended_mask
# Returns a matrix with shape CAMERA_HEIGHT, CAMERA_WIDTH, 1.
#
def getSubtractedFrames(camera, display, number_comparison_frames, threshold):
    #https://stackoverflow.com/questions/27035672/cv-extract-differences-between-two-images
    #New strategy: Take 2 pictures, 1 with and 1 without template, then compare values
    CAMERA_WIDTH, CAMERA_HEIGHT = camera.getResolution()
    blended_mask = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 1), np.uint8)
    blended_mask[:] = 255
    for i in range (number_comparison_frames):
        display.changeBackground("Blank")
        time.sleep(0.5)
        pictureNoTemplate = camera.getFrame()
        display.changeBackground("Template-01")
        time.sleep(0.5)
        pictureWithTemplate = camera.getFrame()

        
        diff = cv2.absdiff(pictureNoTemplate, pictureWithTemplate)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        imagemask = mask > threshold #if abs diff is greater than 10 for each value, then pixel becomes part of the mask.
        
        new_blended_mask = np.zeros_like(blended_mask, np.uint8)
        new_blended_mask[imagemask] = blended_mask[imagemask]
        blended_mask = new_blended_mask
    return blended_mask

#
# Uses scaling template matching 4 times to get corners of blended_mask.
# Assumes that the image projected is reasonably fixed and not skewed at an angle.
# Camera and Blended_mask should have same resolution.
# Access to CornerPiece.png required.
# Returns mask and array of size 4 of the end coordinates in [y, x]. Assumes Camera Resolution.
#
def getTemplateMatching(camera, blended_mask):
    #template matching https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html
    # use blended_mask as recent
    #multi scale template matching https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/
    CAMERA_WIDTH, CAMERA_HEIGHT = camera.getResolution()

    template_to_match = cv2.imread(TEMPLATE_PATH + r"CornerPiece.png")  # Template should be 200 x 200 size. Actual corner is 150 x 150
    template_to_match = cv2.cvtColor(template_to_match, cv2.COLOR_BGR2GRAY)
    ret, template_to_match = cv2.threshold(template_to_match, 127, 255, cv2.THRESH_BINARY)
    template_height, template_width = template_to_match.shape[::-1]

    return_edge_mask = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), np.uint8)
    coordinate_edges = [(0, 0), (0, 0), (0, 0), (0, 0)]
    scale


    for corner in range(4):
        rotated_template_to_match = template_to_match.copy()
        text = "TL"
        offset = (25, 25) # Y, X
        if corner == 1: 
            rotated_template_to_match = cv2.rotate(rotated_template_to_match, cv2.ROTATE_90_CLOCKWISE)
            text = "TR"
            offset = (25, 175)
        elif corner == 2: 
            rotated_template_to_match = cv2.rotate(rotated_template_to_match, cv2.ROTATE_180)
            text = "BR"
            offset = (175, 175)
        elif corner == 3: 
            rotated_template_to_match = cv2.rotate(rotated_template_to_match, cv2.ROTATE_90_COUNTERCLOCKWISE)
            text = "BL"
            offset = (175, 25)
        
        found = None
        max_val = 0
        scaled_width = 1
        scaled_height = 1

        for scale in np.linspace(0.3, 1.0, 20)[::-1]:
            # Resize
            scaled_width = template_width * scale
            scaled_height = template_height * scale
            resized_template = cv2.resize(rotated_template_to_match, (int(scaled_height), int(scaled_width)))
            res = cv2.matchTemplate(blended_mask, resized_template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if found is None or max_val > found[0]:
                found = (max_val, max_loc, scale)
        
        if found is not None:
            max_val, max_loc, scale = found
            top_left = max_loc # X, Y
            bottom_right = (int(top_left[0] + template_width * found[2]), int(top_left[1] + template_height * found[2]))
            cv2.rectangle(return_edge_mask, top_left, bottom_right, (255, 255, 255), 2)
            cv2.putText(return_edge_mask, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(return_edge_mask, str(max_val)[0:4], bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            coordinate_edges[corner] = (top_left[1] + int(offset[0] * scale), top_left[0] + int(offset[1] * scale)) # Convert Y, X

            #cv2.circle(return_edge_mask, (top_left[0] + int(offset[1] * scale), top_left[1] + int(offset[0] * scale)), 5, (0, 0, 255), 2)

    return return_edge_mask, coordinate_edges

#
# Gets the center coordinate using diagonals
# Returns integers y_intersect, x_intersect
# Assumes Camera Resolution
# coordinate_edges_array is assumed [TL, TR, BR, BL]
# Each coordinate is (Y, X)
# Note that (0, 0) dictates Top Left corner of screen. Y increases going down respective of camera footage. Should not make a difference.
#
#
def getCenterCoordinates(camera, coordinate_edges_array):
    CAMERA_WIDTH, CAMERA_HEIGHT = camera.getResolution()
    TL, TR, BR, BL = coordinate_edges_array

    slope_diagonal_TLBR = float(TL[0] - BR[0]) / float(TL[1] - BR[1])   # Should be positive slope  (reversed since y incr going down)
    offset_TLBR = TL[0] - slope_diagonal_TLBR * TL[1]
    slope_diagonal_BLTR = float(TR[0] - BL[0]) / float(TR[1] - BL[1])   # Shold be negative slope   (going up)
    offset_BLTR = BL[0] - slope_diagonal_BLTR * BL[1]

    # (m2 - m1)x = b1 - b2
    x_intersect = int(float(offset_TLBR - offset_BLTR) / float(slope_diagonal_BLTR - slope_diagonal_TLBR))
    y_intersect = int(slope_diagonal_TLBR * x_intersect + offset_TLBR)
    
    return y_intersect, x_intersect



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