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

width = 1920 
height = 1080

x_offset = int((width - f.shape[1]) / 2)
y_offset = int((height - f.shape[0]) / 2)

ratio = float(f.shape[1]) / f.shape[0]
scale = 1

while True:
    time.sleep(0.1)
    ret, img = vid.read()
    
    
    
    if keyboard.is_pressed("up arrow"): y_offset -= 10
    if keyboard.is_pressed("down arrow"): y_offset += 10
    if keyboard.is_pressed("right arrow"): x_offset += 10
    if keyboard.is_pressed("left arrow"): x_offset -= 10
    if keyboard.is_pressed("i"): scale += 0.01
    if keyboard.is_pressed("k"): scale -= 0.01

    display = np.zeros((height, width, 3), np.uint8) #empty
    img = cv2.resize(img, (0,0), fx=scale, fy=scale)

    #https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv
    def overlay_image(background, overlay, x, y):
        # Handling cases
        # Img is fully enclosed in frame = overlay corners and use background offsets
        # Img is negative to the left = Render from offset in overlay and start on 0 for background
        # Img is far to the right = Overlay corners to edge offset, background start left corner to max resolution

        #Handling regions of background to replace with overlay
        y1, y2 = max(0, y), min(background.shape[0], y + overlay.shape[0])
        x1, x2 = max(0, x), min(background.shape[1], x + overlay.shape[1])

        #Handling region of the overlay to display (and not render outside of frame)
        y1o, y2o = max(0, -y), min(overlay.shape[0], background.shape[0] - y)   
        x1o, x2o = max(0, -x), min(overlay.shape[1], background.shape[1] - x)

        #If out of frame
        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return
        
        background[y1 : y2 , x1 : x2] = overlay[y1o : y2o , x1o : x2o]
    
    overlay_image(display, img, x_offset, y_offset)
    cv2.imshow("Projector", display)

    if cv2.waitKey(1) == ord('q'):
            break



