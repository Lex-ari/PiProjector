import cv2
import time
import numpy as np
import camera

# Camera Initialization
vid = cv2.VideoCapture(1)
ret = False
while not ret:
    ret, f = vid.read()
    if ret and np.sum(f.flatten()) == 0:
        ret = False

# Optical Flow
# Guide: https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
# ShiTomasi Corner Detection
feature_params = dict(
    maxCorners = 4,
    qualityLevel = 0.001,
    minDistance = 200,
    blockSize = 7
)
# Lucas Kanade Optical Flow
lk_params = dict(
    winSize = (15, 15),
    maxLevel = 2,
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

# Random Colors
color = np.random.randint(0, 255, (1000, 3))

# First Frame Corners
ret, old_frame = vid.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
ogpoints = p0.copy()

# Mask image
mask = np.zeros_like(old_frame)

# IO
translation = np.zeros(shape=(3, 3))
setestimation = np.zeros(shape=(3, 3))
ret, img = vid.read()
originalImage = img
j = 0
while True:
    #p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    
    #Iteration
    j += 1
    time.sleep(0.01)
    
    ret, img = vid.read()
    if not ret:
        continue

    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calc optical Flow
    #Parameters: Past image, Present image, Previous points, next points,
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    # Perpsective Transform
    perspectiveTransform = cv2.getPerspectiveTransform(p1, ogpoints)
    print("Transform Matrix")
    print('\n')
    print('\n'.join([' '.join(['{:10.2f}'.format(float) for float in row]) for row in perspectiveTransform]))
    ir2 = cv2.warpPerspective(img, perspectiveTransform,(img.shape[1], img.shape[0]))
    cv2.imshow("warp", ir2)

    overlayOut = cv2.addWeighted(originalImage, 0.7, ir2, 0.5, 0)
    cv2.imshow("overlayed", overlayOut)


    # Selecting Good Points
    if p1 is not None:
        good_new = p1[st==1]    #Checking if status = 1, successful optical flow
        good_old = p0[st==1]
    
    # Track Drawing
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(img, (int(a), int(b)), 5, color[i].tolist(), -1)
    img = cv2.add(frame, mask)
    cv2.imshow('frame',img)

    # Update Optical Flow Frames
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

    
    if cv2.waitKey(1) == ord('q'):
        break

time.sleep(100)

#https://www.cse.psu.edu/~rtc12/CSE486/lecture23_6pp.pdf
#https://docs.opencv.org/4.0.0/d9/d0c/group__calib3d.html#gad767faff73e9cbd8b9d92b955b50062d