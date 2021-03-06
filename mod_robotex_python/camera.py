
import numpy as np
import cv2
import imutils
import math
import time
from settings import *
from common import *
from communication import CommunicationController
from speedgen import get_speeds

class CameraController:
    def __init__(self):
        self.communication = CommunicationController()
        self.cap = cv2.VideoCapture(VIDEO_DEVICE)
        self.hsv = None
        self.robot_state = "ball search"
        #These should be in their own AI module, but let's keep them here for now.
        self.balls = None
        self.basket = None
        self.currentbasket = CURRENT_BASKET_TARGET
        self.launchercount = 0

    @property
    def basket_in_position(self):
        if self.basket == []: return False
        
        x, y, w, h = cv2.boundingRect(self.basket)
        #basket should always be pretty much rectangular and not rotated, so the bounding rect is a good enough approx.
        #y+h = 449 if the basket is touching the top of the camera frame 
        horizontal_middle = x+y/2
        if horizontal_middle < 340 and horizontal_middle > 260 and h < 85 and h > 75:
            return True
        else:
            return False


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
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, None,iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, None,iterations=2)
        _, objContour, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
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
        self.communication.sendCommand(1, 15, 2)

    def take_decision(self):
        if self.robot_state == "ball search":
            """ state: no balls in sight, no balls in thrower(by inference)
            action: spin around until you find it """
            if self.balls == []:
                self.search_for_ball()
            else: 
                self.robot_state = "ball found"

        if self.robot_state == "ball found":
            """ state: ball(s) seen, no balls in thrower(by inference)
            action: calculate position then go towards it """
            if self.balls == []:
                self.robot_state = "ball search"
                return
            largest_radius, largest_centre = self.get_horizontal_ball_positions()
            for a_c_tuple in self.balls:
            #remember self.balls is in the form [(area, contour)]
            #regardless of whether there is a larger ball in sight, if there's one very close to the thrower
            #(meaning, very close to the bottom of the camera frame), it will switch into basket search mode.
                x, y, w, h = cv2.boundingRect(a_c_tuple[1])
                center_x = largest_centre
                center_y = y+h/2
                print center_x, center_y

                if (center_x > 330) and (largest_radius < 18):
                    self.communication.sendCommand(15,15,15)

                if (center_x > 330) and (largest_radius >= 18):
                    self.communication.sendCommand(15, 15, 15)

                # turn left
                if (center_x < 230) and (largest_radius < 18):
                    self.communication.sendCommand(-15, -15, -15)

                if (center_x < 230) and (largest_radius >= 18):
                    self.communication.sendCommand(-15, -15, -15)

                # go forward
                if (center_x > 230) and (center_x < 330) and largest_radius < 18:
                    self.communication.sendCommand(-30, 0, 30)

                if (center_x > 230) and (center_x < 330) and largest_radius > 18:
                    self.communication.sendCommand(-20, 0, 20)

                if largest_radius >= 22 and 240 <= largest_centre <= 305:
                    self.communication.sendCommand(0, 0, 0)
                    self.robot_state = "basket search"
                    return
                # if largest_radius >= 22 and 240 <= largest_centre <= 305:
                #     self.communication.sendCommand(0, 0, 0)
                #     self.robot_state = "basket search"
                #     return
                # elif center_y <= 8 and 240 <= largest_centre <= 305:
                #     self.communication.sendCommand(8, 0, -8)
                #     print "back"
                #     time.sleep(0.9)

            print("radius of largest:", largest_radius)
            if largest_radius <= 0:
                self.robot_state = "ball search"
                return
            x, y, w, h = cv2.boundingRect(self.balls[0][1])
            self.move_towards_ball(largest_radius, largest_centre, y)
        print(self.robot_state)

        if self.robot_state == "basket search":
            """ state: balls seen or not, basket not seen, ball in thrower
            action: look for basket (for now, only spinning around). When 
            basket is found and in optimal position, throw the ball and move to ball search"""
            # if self.basket != [] and cv2.contourArea(self.basket) > 50:
            #     self.robot_state = "basket found"
            #     return
            self.search_for_basket()
            if self.basket != [] and cv2.contourArea(self.basket) > 200:
                self.robot_state = "basket found"

        if self.robot_state == "basket found":
            if self.basket == []:
                self.robot_state = "basket search"
                return
            else:
                x, y, w, h = cv2.boundingRect(self.basket)
                # if h < 70 and self.currentbasket == BLUE_BOUNDARIES:
                #     self.currentbasket = PINK_BOUNDARIES
                #     return
                # if h < 70 and self.currentbasket == PINK_BOUNDARIES:
                #     self.currentbasket = BLUE_BOUNDARIES
                #     return
                center_x = x + w/2
                if self.balls == []:
                    self.robot_state = "ball search"
                    return
                _, largest_centre = self.get_horizontal_ball_positions()

                if 260 <  center_x < 290:
                    print "basket in middle"
                    # if h < 70:
                    #     self.communication.sendCommand(-25, 0, 25)
                    #     return
                    self.shoot_ball()
                    self.robot_state = "ball search"
                elif center_x >= 300:
                    self.communication.sendCommand(1, 10, 2)
                else:
                    self.communication.sendCommand(-1, 10, -2)

    def get_throw_power(self):
        power = 0
        #if self.basket == []:
            #if by mistake there's no basket when the ball is thrown, throw at an arbitrary mid-range power
        #    return power
        unused1, unused2, unused3, h = cv2.boundingRect(self.basket)
        print "h:", h

        # power = 219 -0.605 * h + 0.0015 * h**2
        # power = math.ceil(power)

        if h > 196:
            power = 162    
        elif h > 190:
            power = 164
        elif h > 179:
            power = 165
        elif h > 170:
            power = 166
        elif h > 160:
            power = 166
        elif h > 150:
            power = 167
        elif h > 140: 
            power = 168
        elif h > 120:
            power = 170
        elif h > 115:
            power = 172
        elif h > 105:
            power = 174
        elif h <= 105:
            power = 179

        print "power:", power

        return power



    def shoot_ball(self):
        power = self.get_throw_power()
        self.communication.shoot_ball(power)
        time.sleep(0.1)
        self.communication.sendCommand(-20, 0, 20)
        time.sleep(0.8)
        self.communication.shoot_ball(1)


    def move_towards_ball(self, radius, centre, y):
        #centre: 300 is the center of the frame, 600 is the right edge, 0 is the left edge
        #note that this is because we resize the frame to 600 width in receive_image
        if centre > 300:
            if radius <=8:
                turnspeed = max(radius, 4 )
            elif y <= 30: 
                turnspeed = 4
            else:
                turnspeed = 12
            print("RIGHT, FAR")
            self.communication.sendCommand(turnspeed,turnspeed,turnspeed)

        # turn left
        elif centre < 260:
            if radius <=12:
                turnspeed = min(radius, 5)
            elif y <= 30: 
                turnspeed = 4
            else:
                turnspeed = 12
            print("LEFT, FAR")
            self.communication.sendCommand(-turnspeed,-turnspeed,-turnspeed)

        # go forward
        elif radius < 12:
            self.communication.sendCommand(-30, 0, 30)
            print("FORWARD, FAST")

        elif 20 > radius >= 12 :
            self.communication.sendCommand(-10, 0, 10)
            print("FORWARD, SLOW")

        elif radius > 20:
            self.communication.sendCommand(-5, 0, 5)


    """Main loop, gets looped in main.py"""
    def main_loop(self):
        self.receive_image()
        self.balls = self.get_contours(GREEN)#list of tuples
        self.basket = self.get_contours(CURRENT_BASKET_TARGET)#just a contour, or empty if there's nothing
        # if not self.basket:
        #     self.basket = self.get_contours(PINK_BOUNDARIES)
        if self.basket: self.basket = self.basket[0][1]
        #first, takes in information from the camera and extracts boundaries for balls and basket
        cv2.imshow("hsv", self.hsv)
        
        self.take_decision()
        cv2.waitKey(5)
