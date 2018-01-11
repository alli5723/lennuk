import numpy as np
import cv2
import imutils
import math
import time
import serial

s = serial.Serial("/dev/ttyACM0")

def shoot(power):
    s.write("d:" + str(power) + "\n")
    time.sleep(0.1)
    s.write("sd:-20:20:0\n")

#PINK_BOUNDARIES = ((12, 170, 93), (29, 252, 151))
#VIDEO_DEVICE = 0
#cap = cv2.VideoCapture(VIDEO_DEVICE)
#while(cap.isOpened()):
#    ret, frame = cap.read()
#    if ret:
#        frame = cv2.flip(frame,180)
#        frame = imutils.resize(frame, width=600)
#        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


#        # loop over the boundaries
#        # for (lower, upper) in ballBoundaries:
#        basketLower, basketUpper = PINK_BOUNDARIES

#        mask = cv2.inRange(hsv, basketLower, basketUpper)

#        basketContour, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#        areaArray = []
#        try:
#            for c in basketContour:
#                area = cv2.contourArea(c)
#                # print(area)
#                areaArray.append(area)
#            bc_b = (sorted(zip(areaArray, basketContour), key=lambda x: x[0], reverse=True))[0][1]
#            # takes the largest contour
#            x, y, w, h = cv2.boundingRect(bc_b)
#            print "x:", x, "y:", y, "w:", w, "h:", h
#        except:
#            pass

#        # cv2.imshow("window", frame)
#        # cv2.imshow("window2", mask)


#        # ballContour, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

#        #Ball not found yet

#        if cv2.waitKey(1) & 0xFF == ord('q'):
#            break
#    else:

#        break

#cap.release()
#cv2.destroyAllWindows()


