import cv2
import numpy as np

VIDEO_DEVICE = 0
GREEN = ((39, 168, 131), (75, 251, 241))
cap = cv2.VideoCapture(VIDEO_DEVICE)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower, upper = GREEN
        mask = cv2.inRange(frame, lower, upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None,iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None,iterations=2)
        cv2.imshow("win", mask)
        cv2.waitKey(5)





