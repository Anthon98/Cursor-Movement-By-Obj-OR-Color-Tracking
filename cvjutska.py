print("started")

import cv2
import time
import win32api
import numpy as np

cap = cv2.VideoCapture(0)
tracker = cv2.TrackerMOSSE_create()
success, img = cap.read()
bbox = cv2.selectROI("Tracking",img,False)
tracker.init(img,bbox)

def drawBox(img,bbox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    print(x, y)

    #on center, its like 250 and y is 120
    #
    #250

    #250 and 120 should be center of: 1440/2 = 720 2560/2 = 1280 - 250 / 720 - 120

    #win32api.SetCursorPos((x*5,y*5))
    
    gg = 2560-(x*15+w)
    eg = 1440-(y*15+h)
    eg = y*15
    win32api.SetCursorPos((gg,eg))
    
    
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)

while True:
    #time.sleep(0.1)
    timer = cv2.getTickCount()
    success, img = cap.read()
    #fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    #cv2.

    success,bbox = tracker.update(img)


    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #definig the range of red color
    red_lower=np.array([136,87,111],np.uint8)
    red_upper=np.array([180,255,255],np.uint8)

    kernel = np.ones((5 ,5), "uint8")

    #finding the range of red,blue and yellow color in the image
    red=cv2.inRange(hsv, red_lower, red_upper)
    red=cv2.dilate(red, kernel)
    res=cv2.bitwise_and(img, img, mask = red)

    #Tracking the Red Color
    contours,hierarchy=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>300):
            
            x,y,w,h = cv2.boundingRect(contour)
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,255))

            #gg = 2560-(x*5+w)
            #eg = y*5
            #win32api.SetCursorPos((gg*2,eg*2))

    if success:
        drawBox(img,bbox)
    else:
        print("not tracking")

    cv2.imshow("Tracking",img)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break