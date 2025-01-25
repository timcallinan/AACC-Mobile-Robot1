# This program takes an image using L1_camera, applies filters with openCV, and returns
# a color target if located in the image.  The target parameters are (x,y,radius).
# This program requires that opencv2 is installed for python3.

# Import internal programs:
import L1_camera as cam

# Import external programs:
import cv2          # computer vision
import numpy as np  # for handling matrices
import time         # for keeping time

# Define global parameters
img_width = cam.width                         # image width in pixels
color_range = ((0, 150, 150), (15, 255, 255))  # This color range defines the color target
printFlag = True                              # use this variable to reduce print statements

def colorTarget(color_range=((0, 0, 0), (255, 255, 255))): # function defaults to open range if no range is provided
    image = cam.newImage()
    if filter == 'RGB':
        image_hsv = image.copy()
    else:
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)    # convert to hsv colorspace

    thresh = cv2.inRange(image_hsv, color_range[0], color_range[1])
    kernel = np.ones((5, 5), np.uint8)                                      # apply a blur function
    mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)                 # Apply blur
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)                  # Apply blur 2nd iteration

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE)[-2]                        # generates number of contiguous "1" pixels
    if len(cnts) > 0:                                           # begin processing if there are "1" pixels discovered
        c = max(cnts, key=cv2.contourArea)                      # return the largest target area
        ((x, y), radius) = cv2.minEnclosingCircle(c)            # get properties of circle around shape
        targ = np.array([int(x), int(y),                        # return x, y, radius, of target 
                round(radius, 1)])

        # Add tracking dot and circle to target in the original image
        xc = int(x)
        yc = int(y)
        rc = int(radius)
        cv2.circle(image, (xc,yc), 5, (0,0,255), -1)
        cv2.circle(image, (xc,yc), rc, (0,255,0), 2)

        # Display images
        #print("colorTarget images\n")
        cv2.namedWindow('camera')
        cv2.namedWindow('hsv')
        cv2.namedWindow('threshold')
        cv2.namedWindow('blurred')
        windowShift = 700
        cv2.moveWindow('camera', windowShift  * 0, 10) # upper left
        cv2.moveWindow('hsv', windowShift * 1, 10)  # next to the right
        cv2.moveWindow('threshold', windowShift * 2, 10) # Next right
        cv2.moveWindow('blurred', windowShift * 3, 10)
        cv2.imshow('camera', image)
        cv2.imshow('hsv', image_hsv)
        cv2.imshow('threshold', thresh)
        cv2.imshow('blurred', mask)

        return targ

    else:
        return np.array([None, None, 0])

def getAngle(x):                         # check deviation of target from center (fraction of screen)
    if x is not None:
        ratio = x / img_width            # divide by pixels in width
        offset_x = -2*(ratio - 0.5)      # offset to center of image.  Now, positive = left, negative = right
        offset_x = round(offset_x,1)     # perform rounding
        return (offset_x)
    else:
        return None

# THIS SECTION ONLY RUNS IF THE PROGRAM IS CALLED DIRECTLY
if __name__ == "__main__":
    while True:
        target = colorTarget(color_range) # generate a target
        x = target[0]
        if x is None:
            if printFlag == True : print("no target located.") 
            printFlag = False
        else:
            x_offset = getAngle(x)
            print("target x, y, radius:", target[0], target[1], target[2], '\t' "x_offset: ", x_offset)
            printFlag = True
        if cv2.pollKey() & 0XFF ==ord('q'):
            break
