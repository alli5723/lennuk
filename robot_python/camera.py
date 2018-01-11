
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
        self.cap = cv2.VideoCapture(1)
        self.hsv = None
        self.robot_state = "ball search"
        #These should be in their own AI module, but let's keep them here for now.
        self.balls = None
        self.basket = None


    """receives the camera image each frame and does the basic hsv conversion to prepare for comparisons and such"""
    def receive_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 180)
            frame = imutils.resize(frame, width=600)
            self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    """Takes a tuple of tuples color ((hLow, sLow, vLow), (hHigh, sHigh, vHigh)) and returns contours"""
    def get_contours(self, colorbound):
        lower, upper = colorbound
        mask = cv2.inRange(self.hsv, lower, upper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None,iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None,iterations=3)
        cv2.imshow("window", mask)
        objContour, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if objContour == []: return []
        areaArray = []
        for c in objContour:
            area = cv2.contourArea(c)
            areaArray.append(area)
        sortedObjs = (sorted(zip(areaArray, objContour), key=lambda x: x[0], reverse=True))
        return sortedObjs
        #returns a list of tuples (area, contour), sorted by largest areas first

    """Takes list of balls from class and outputs radius and centre of the largest one(temp)"""
    def get_horizontal_ball_positions(self):
        centre_ball = []
        largest_ball = self.balls[0][1]
        moments_b = cv2.moments(largest_ball)
        centre_ball.append(int(moments_b['m10'] / moments_b['m00']))
        centre_ball.append(int(moments_b['m01'] / moments_b['m00']))
        cv2.circle(self.hsv, (centre_ball[0], centre_ball[1]), 3, (0, 0, 0), -1)
        x, y, w, h = cv2.boundingRect(largest_ball)
        cv2.drawContours(self.hsv, largest_ball, -1, (0, 165, 255), 2)

        # Kerttu: calculating the radius for the ball by taking two extreme points from the contour: left and right
        ball_radius_calculated = int(math.sqrt(math.pow(
            tuple(largest_ball[largest_ball[:, :, 0].argmin()][0])[0] - tuple(largest_ball[largest_ball[:, :, 0].argmax()][0])[0],
            2) + math.pow(
            tuple(largest_ball[largest_ball[:, :, 0].argmin()][0])[1] - tuple(largest_ball[largest_ball[:, :, 0].argmax()][0])[1],
            2)) / 2)

        ball_radius = ball_radius_calculated
        return ball_radius, centre_ball[0]

    def search_for_ball(self):
        self.communication.sendCommand(10, 10, 10) 

    def search_for_basket(self):
        self.communication.sendCommand(0, 10, 0)

    """misplaced AI method, should use function assigning at the class instead... something to worry abt later"""
    def take_decision(self):
        if self.robot_state == "ball search":
            """ state: no balls in sight, no balls in thrower(by inference)
            action: spin around until you find it """
            if self.balls == []:
                print("no balls found yet")
                self.search_for_ball()
            else: 
                self.robot_state = "ball found"

        if self.robot_state == "ball found":
            """ state: ball(s) seen, no balls in thrower(by inference)
            action: calculate position then go towards it """
            if self.balls == []:
                self.robot_state = "ball search"
                return
            for a_c_tuple in self.balls:
            #remember self.balls is in the form [(area, contour)]
            #regardless of whether there is a larger ball in sight, if there's one very close to the thrower
            #(meaning, very close to the bottom of the camera frame), it will switch into basket search mode.
                x, y, w, h = cv2.boundingRect(a_c_tuple[1])
                if y < 10 and h < 25:
                    """BALL IS VERY NEAR THROWER!!"""
                    self.robot_state = "basket search"
                    break

            largest_radius, largest_centre = self.get_horizontal_ball_positions()
            self.move_towards_ball(largest_radius, largest_centre)

        if self.robot_state == "basket search":
            """ state: balls seen or not, basket not seen, ball in thrower
            action: look for basket (for now, only spinning around). When 
            basket is found and in optimal position, throw the ball and move to ball search"""
            self.search_for_basket()
            if self.basket:
                self.get_basket_position()
                """BIG TODO: Here I should get basket position, look for it if not available, and move into position for a shot otherwise. Once the shot is made, return to ball search."""



    def move_towards_ball(self, radius, centre):
        #centre: 300 is the center of the frame, 600 is the right edge, 0 is the left edge
        #note that this is because we resize the frame to 600 width in receive_image
            if centre > 340:
                self.communication.sendCommand(15,15,15)
              #  print("RIGHT")

            # turn left
            elif centre < 260:
                self.communication.sendCommand(-15, -15, -15)
              #  print("LEFT")

            # go forward
            elif radius < 30:
                self.communication.sendCommand(-30, 0, 30)
              #  print("FORWARD, FAST")

            elif radius > 30:
                self.communication.sendCommand(-20, 0, 20)
             #   print("FORWARD, SLOW")

    """Main loop, gets looped in main.py"""
    def main_loop(self):
        self.receive_image()
        self.balls = self.get_contours(GREEN_BOUNDARIES)#list of tuples
        self.basket = self.get_contours(BLUE_BOUNDARIES)#just a contour, or empty if there's nothing
        if self.basket: self.basket = self.basket[0][1]
        #first, takes in information from the camera and extracts boundaries for balls and basket
        cv2.imshow("hsv", self.hsv)

        self.take_decision()
        cv2.waitKey(5)

            
