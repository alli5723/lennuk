
from camera import CameraController
# from refree import RefreeController
# from robot import RobotController

camera = CameraController()
while camera.cap.isOpened():
    camera.main_loop()
# refree = RefreeController()
# robot = RobotController()

# refree.whatsUp()
# robot.start()
