import sys
import cv2
import numpy as np
import time
import imutils

#define function to recognize entities

def find_circles(frame, mask):

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None
    

    #find contours in the mask
    if len(contours)> 1:
        #find the largest contours
        c = max(contours, key = cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        #calculating center of detected
        center = (int (M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

        if radius > 10:
            #draw circle
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), 1)
        
    return center


def find_x_shape(frame, mask, x_shape_template):
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    for c in contours:
        # Approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        # Use shape matching to identify the "X" shape
        match = cv2.matchShapes(x_shape_template, approx, cv2.CONTOURS_MATCH_I1, 0.0)
        
        # If match is good enough (lower value means a better match)
        if match < 0.2:  # Adjust threshold as necessary
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            if radius > 10:
                cv2.drawContours(frame, [approx], -1, (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 0), 1)
                
            break
    
    return center

def create_x_shape_template():
    x_shape = np.array([
        [0, 0], [1, 1], [2, 0], [1, -1]
    ], dtype=np.int32)
    x_shape = x_shape.reshape((-1, 1, 2))
    return x_shape