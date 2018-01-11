import serial
from camera import CameraController


class RobotController:

    def __init__(self):
        camera = CameraController()
        camera.start()
        print("robot initialized")

    def getBall(self):
        print("ball obtained")

    def hasBall(self):
        return False

    def searchBall(self):
        print("Searching for ball")