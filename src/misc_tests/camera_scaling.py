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

width = 1920 * 8
height = 1080 * 8

x_offset = int((width - f.shape[1]) / 2)
y_offset = int((height - f.shape[0]) / 2)

ratio = float(f.shape[1]) / f.shape[0]
scale = 1

while True:
    time.sleep(0.001)
    ret, img = vid.read()
    
    
    
    if keyboard.is_pressed("up arrow"): y_offset -= 10
    if keyboard.is_pressed("down arrow"): y_offset += 10
    if keyboard.is_pressed("right arrow"): x_offset += 10
    if keyboard.is_pressed("left arrow"): x_offset -= 10
    if keyboard.is_pressed("i"): scale += 0.01
    if keyboard.is_pressed("k"): scale -= 0.01

    display = np.zeros((height, width, 3), np.uint8) #empty
    img = cv2.resize(img, (0,0), fx=scale, fy=scale)

    #https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
    #https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv
    display[y_offset : y_offset + img.shape[0], x_offset : x_offset + img.shape[1]] = img
    output = display[int((height - 1080) / 2): int((height + 1080) / 2), int((width - 1920) / 2): int((width + 1920) / 2)]
    cv2.imshow("Projector", output)

    if cv2.waitKey(1) == ord('q'):
            break



