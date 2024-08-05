import sys
import cv2
import numpy as np
import time
import imutils
import serial
import math
from matplotlib import pyplot as plt

import HSV_Strategy as hsv
import shape_recognition as shape
import triangulation as tri


#connect to serial
ser = serial.Serial('COM10',115200 , timeout=1)
time.sleep(2)

cap_left = cv2.VideoCapture(0)
cap_right = cv2.VideoCapture(2)

#setting image resolution
image_width = 640
image_height = 640

cap_left.set(3, image_width)
cap_left.set(4, image_height)

cap_right.set(3, image_width)
cap_right.set(4, image_height)

framerate = 30

B = 60 #distance between cameras(cm)
f = 6 #focal length of camera's lense(mm)

alpha = 90 #FOV horizontal


#define function for sending angle value
def send_angle(x_detected):
    if(x_detected >= image_width/2):
        x_detected = x_detected - image_width/2
        sector = 1
    else:
        x_detected = image_width/2 - x_detected
        sector = -1
    angle = int((alpha/2)-sector*x_detected*alpha/image_width)
    ser.write(str(angle).encode())
    print(f"Sent: vertical {angle}")


#starting loop 
count = -1
k = 0

while(True):
    count+=1
     
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()
     
    if ret_left == False or ret_right == False:
        break
    
    else:
        mask_left = hsv.add_HSV_filter(frame_left, 0)
        mask_right = hsv.add_HSV_filter(frame_right, 1)
        
        res_left = cv2.bitwise_and(frame_left, frame_left, mask = mask_left)
        res_right = cv2.bitwise_and(frame_right, frame_right, mask = mask_right)
        
        circles_left = shape.find_circles(frame_left, mask_left)
        circles_right = shape.find_circles(frame_right, mask_right)
        
        if np.all(circles_right) == None or np.all(circles_left) == None:
            cv2.putText(frame_right, "no detection", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            cv2.putText(frame_left, "no detection", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
        else:
            depth = tri.find_depth(circles_right, circles_left, frame_right, frame_left, B, f, alpha)
            cv2.putText(frame_left, "detected", (75,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
            cv2.putText(frame_right, "detected", (75,50), cv2. FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0),2)
            cv2.putText(frame_left, "distance: " + str(round(depth, 3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 0)
            if(k > 50):
                #send angle between
                send_angle(circles_left[0])
                k = 0
            cv2.putText(frame_right, "distance: " + str(round(depth, 3)), (200,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124,252,0), 2)
        
        cv2.imshow("frame_left", frame_left)
        cv2.imshow("frame_right", frame_right)
        cv2.imshow("mask_left", mask_left)
        cv2.imshow("mask_right", mask_right)
        k+=1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#drop image capturing
cap_left.release()
cap_right.release()

cv2.destroyAllWindows()

