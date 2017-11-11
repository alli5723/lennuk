from camera import CameraController
from refree import RefreeController
from robot import RobotController

refree = RefreeController()
camera = CameraController()
robot = RobotController()

refree.whatsUp()
camera.start()
robot.start()
