from robot import RobotController

robot = RobotController()
try:
    while True:
        #run app
        if(not robot.hasBall()):
            print("no ball yet")
        else:
            robot.getBall(robot.ball())
except Exception as ex:
    print(ex)