from robot import RobotController
from communication import CommunicationController

try:
    robot = RobotController()
    while True:
        #run app
        if(not robot.hasBall()):
            noball = True
        else:
            robot.getBall(robot.ball())
except Exception as ex:
    robot = RobotController()
    print(ex)