from ctypes import windll, Structure, c_long, byref
import time
import mss
import cv2
import numpy as np
import pyautogui



class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

def lmb_click():
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()

# 1024x768 windowed on 1920x1080 monitor
# mon = {"top": 156, "left": 448, "width": 1024, "height": 768}

title = "Fishing Bot"
sct = mss.mss()

print ("STARTING after 15 seconds, please adjust your rod!")
time.sleep(15)
print ("Started!")

lmb_click()
print ("Rod dropped!")
last_time = time.time()


while True:     # what bot sees
    if time.time() - last_time < 2:
        continue

    cur = queryMousePosition()
    mon = {"top": cur['y'] - 50, "left": cur['x'] - 50, "width": 100, "height": 100}
    img = np.asarray(sct.grab(mon))

    # create hsv
    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # create brown mask
    brown_lower = np.array([10, 0, 0], np.uint8) 
    brown_upper = np.array([20, 255, 255], np.uint8) 
    brown_mask = cv2.inRange(hsvFrame, brown_lower, brown_upper) 
    res = cv2.bitwise_and(img, img, mask = brown_mask)
    
    # check for brown color
    is_brown = np.sum(brown_mask)
    if is_brown:
        pass
    else:
        print ("Catch!")
        time.sleep(0.3)
        lmb_click()

        time.sleep(1.0)
        print ("New rod dropped!")
        lmb_click()

        last_time = time.time()

    cv2.imshow(title, img)        # what bot sees before masking
    cv2.imshow('res', res)        # what bot sees after masking  
    
    if cv2.waitKey(5) & 0xFF == 27:
        break

cv2.destroyAllWindows()