from communication import CommunicationController


class RobotController:

    def __init__(self):
        # camera = CameraController()
        # camera.start()
        self.communication = CommunicationController()
        self.communication.listenToRefree()
        print("robot initialized")

    def Stop(self):
        self.communication.sendCommand(0, 0, 0, 1)
        print("Stop playing")

    def Play(self):
        self.communication.sendCommand(15, 15, 15, 1)
        print("Playing")

    def getBall(self):
        print("ball obtained")

    def hasBall(self):
        return False

    def searchBall(self):
        print("Searching for ball")