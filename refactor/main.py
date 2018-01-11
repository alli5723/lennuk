from robot import RobotController
from camera import CameraController
from communication import CommunicationController

# game_status = True
# robot = RobotController()
# camera = CameraController()
# camera.open()

try:
    communication = CommunicationController()
    while True:
        communication.sendCommand(15, 15, 15, 1)
        # #run app
        # if not game_status:
        #     robot.Stop()
        # else:
        #     robot.Play()

        # # if(not robot.hasBall()):
        # #     noball = True
        # # else:
        # #     robot.getBall(robot.ball())
except Exception as ex:
    robot = RobotController()
    print(ex)