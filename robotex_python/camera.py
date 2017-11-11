import numpy as np
import cv2
import imutils
import math
import time
from settings import *
from common import *
from communication import CommunicationController

class CameraController:
    def __init__(self):
        self.communication = CommunicationController()
        self.count = 0
        self.debugcount = 0
        print("Camera Started")

    def evaluate(self, objectContour, frame):
        areaArray = []
        if len(objectContour) > 0 and not ROBOT_STATE.STOP :
            ROBOT_WITH_BALL.SEEN_BALL = True
            ROBOT_WITH_BALL.FOLLOW_BALL = True
            for i, c in enumerate(objectContour):
                area = cv2.contourArea(c)
                areaArray.append(area)
            bc_b = (sorted(zip(areaArray, objectContour), key=lambda x: x[0], reverse=True))[0][1]

            centre_ball = []
            moments_b = cv2.moments(bc_b)
            centre_ball.append(int(moments_b['m10'] / moments_b['m00']))
            centre_ball.append(int(moments_b['m01'] / moments_b['m00']))
            cv2.circle(frame, (centre_ball[0], centre_ball[1]), 3, (0, 0, 0), -1)

            x, y, w, h = cv2.boundingRect(bc_b)
            cv2.drawContours(frame, bc_b, -1, (0, 165, 255), 2)

            # Kerttu: calculating the radius for the ball by taking two extreme points from the contour: left and right
            ball_radius_calculated = int(math.sqrt(math.pow(
                tuple(bc_b[bc_b[:, :, 0].argmin()][0])[0] - tuple(bc_b[bc_b[:, :, 0].argmax()][0])[0],
                2) + math.pow(
                tuple(bc_b[bc_b[:, :, 0].argmin()][0])[1] - tuple(bc_b[bc_b[:, :, 0].argmax()][0])[1],
                2)) / 2)

            ball_radius = ball_radius_calculated
            # print(ball_radius)
            if (centre_ball[0] > 330) and (ball_radius < 18):
                self.communication.sendCommand(15,15,15,1)

            if (centre_ball[0] > 330) and (ball_radius >= 18):
                self.communication.sendCommand(15, 15, 15, 1)

            # turn left
            if (centre_ball[0] < 230) and (ball_radius < 18):
                self.communication.sendCommand(-15, -15, -15, 1)

            if (centre_ball[0] < 230) and (ball_radius >= 18):
                self.communication.sendCommand(-15, -15, -15, 1)

            # go forward
            if (centre_ball[0] > 230) and (centre_ball[0] < 330) and ball_radius < 18:
                if(ball_radius < 10):
                    time.sleep(0.05)
                    ROBOT_WITH_BALL.HAS_BALL = True
                    ROBOT_STATE.SEARCH_BASKET = True
                #     self.communication.throwBall(200)
                # print("Ball radius is " + str(ball_radius))
                self.communication.sendCommand(-30, 0, 30, 1)
            # self.communication.throwBall(120)

            if (centre_ball[0] > 230) and (centre_ball[0] < 330) and ball_radius > 18:
                self.communication.sendCommand(-20, 0, 20, 1)


    def start(self):
        cap = cv2.VideoCapture(VIDEO_DEVICE)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame,180)
                frame = imutils.resize(frame, width=600)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                ballBoundaries = [ GREEN_BOUNDARIES, ORANGE_BOUNDARIES ]

                # loop over the boundaries
                # for (lower, upper) in ballBoundaries:
                lower, upper = GREEN_BOUNDARIES
                basketLower, basketUpper = BLUE_BOUNDARIES

                mask = cv2.inRange(hsv, lower, upper)
                mask = cv2.erode(mask, None, iterations=2)
                mask = cv2.dilate(mask, None, iterations=2)
                cv2.imshow("window", frame)
                

                ballContour, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

                #Ball not found yet
                if len(ballContour) == 0 and not ROBOT_STATE.STOP:
                    ROBOT_WITH_BALL.SEEN_BALL = False
                    self.communication.sendCommand(10, 10, 10, 1)
                    # self.communication.throwBall(0)
                # else:
                    # print("Robot is potentially paused")
                if not ROBOT_STATE.SEARCH_BASKET:
                    self.evaluate(ballContour, frame)
                else:
                    mask2 = cv2.inRange(hsv, basketLower, basketUpper)
                    mask2 = cv2.erode(mask2, None, iterations=2)
                    mask2 = cv2.dilate(mask2, None, iterations=2)
                    cv2.imshow("window2", mask2)

                    basketContour, hierarchy = cv2.findContours(mask2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

                    if len(basketContour) == 0 and ROBOT_STATE.SEARCH_BASKET:
                        self.communication.sendCommand(0, 10, 0, 1)

                    self.evaluateBasket(basketContour, frame)
                        

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def camprint(self, x, y, w, h):
        if self.debugcount > 20:
            print("width is " + str(x) + " > " + str(y) + " > "  + str(w) + " > " + str(h))
            self.debugcount = 0
        else:
            self.debugcount += 1
        

    def evaluateBasket(self, objectContour, frame):
        areaArray = []
        if len(objectContour) > 0 and not ROBOT_STATE.STOP :
            # print("Now we need a vasket")
            ROBOT_WITH_BALL.SEEN_BALL = True
            ROBOT_WITH_BALL.FOLLOW_BALL = True
            for i, c in enumerate(objectContour):
                area = cv2.contourArea(c)
                areaArray.append(area)
            bc_b = (sorted(zip(areaArray, objectContour), key=lambda x: x[0], reverse=True))[0][1]

            centre_basket = []
            moments_b = cv2.moments(bc_b)
            centre_basket.append(int(moments_b['m10'] / moments_b['m00']))
            centre_basket.append(int(moments_b['m01'] / moments_b['m00']))
            cv2.circle(frame, (centre_basket[0], centre_basket[1]), 3, (0, 0, 0), -1)

            x, y, w, h = cv2.boundingRect(bc_b)
            cv2.drawContours(frame, bc_b, -1, (0, 165, 255), 2)

            self.camprint(x, y, w, h)

            # Kerttu: calculating the radius for the ball by taking two extreme points from the contour: left and right
            basket_radius_calculated = int(math.sqrt(math.pow(
                tuple(bc_b[bc_b[:, :, 0].argmin()][0])[0] - tuple(bc_b[bc_b[:, :, 0].argmax()][0])[0],
                2) + math.pow(
                tuple(bc_b[bc_b[:, :, 0].argmin()][0])[1] - tuple(bc_b[bc_b[:, :, 0].argmax()][0])[1],
                2)) / 2)

            basket_radius = basket_radius_calculated
            # print(basket_radius)
            if (centre_basket[0] > 330) and (basket_radius < 18):
                self.communication.sendCommand(15,15,15,1)

            if (centre_basket[0] > 330) and (basket_radius >= 18):
                self.communication.sendCommand(15, 15, 15, 1)

            # turn left
            if (centre_basket[0] < 230) and (basket_radius < 18):
                self.communication.sendCommand(-15, -15, -15, 1)

            if (centre_basket[0] < 230) and (basket_radius >= 18):
                self.communication.sendCommand(-15, -15, -15, 1)

            # go forward
            # print("Basket radius is " + str(basket_radius))
            if (centre_basket[0] > 230) and (centre_basket[0] < 330) and basket_radius < 18:
                if(basket_radius < 3):
                    time.sleep(0.05)
                    ROBOT_WITH_BALL.HAS_BALL = True
                    ROBOT_STATE.SEARCH_BASKET = True
                #     self.communication.throwBall(200)
                # print("Basket radius is " + str(basket_radius))
                self.communication.sendCommand(-30, 0, 30, 1)
            # self.communication.throwBall(120)

            if (centre_basket[0] > 230) and (centre_basket[0] < 330) and basket_radius > 18:
                self.communication.sendCommand(-20, 0, 20, 1)