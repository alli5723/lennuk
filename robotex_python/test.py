import numpy as np
import cv2
import imutils
import math
import time

BLUE_BOUNDARIES = ((82, 199, 105), (144, 255, 255))
VIDEO_DEVICE = 0
cap = cv2.VideoCapture(VIDEO_DEVICE)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        frame = cv2.flip(frame,180)
        frame = imutils.resize(frame, width=600)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # loop over the boundaries
        # for (lower, upper) in ballBoundaries:
        basketLower, basketUpper = BLUE_BOUNDARIES

        mask = cv2.inRange(hsv, basketLower, basketUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        basketContour, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        areaArray = []
        for c in basketContour:
            area = cv2.contourArea(c)
            print(area)
            areaArray.append(area)
        bc_b = (sorted(zip(areaArray, basketContour), key=lambda x: x[0], reverse=True))[0][1]
        # takes the largest contour
        print cv2.boundingRect(bc_b)

        cv2.imshow("window", frame)
        cv2.imshow("window2", mask)


        # ballContour, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

        #Ball not found yet

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:

        break

cap.release()
cv2.destroyAllWindows()


