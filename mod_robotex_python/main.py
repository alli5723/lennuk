
from camera import CameraController
import time
from refree import RefreeController
from settings import ROBOT_ID, FIELD_ID
# from robot import RobotController

# def get_rf_signal():



camera = CameraController()
#camera.robot_state = "stop"

while not camera.communication.board.is_open:
    time.sleep(1)

# camera.refree = RefreeController(camera)

while camera.cap.isOpened():
    camera.main_loop()

    if camera.robot_state == "stop":
        time.sleep(1)

    if camera.communication.board.readable():
        time.sleep(0.01)
        tdata = camera.communication.board.read()
        data_left = camera.communication.board.inWaiting()  # Get the number of characters ready to be read
        tdata += camera.communication.board.read(data_left) # Do the read and combine it with the first character

        if tdata:
            oursignal="a" + FIELD_ID + ROBOT_ID
            allsignal="a" + FIELD_ID + "X"
            if oursignal in tdata or allsignal in tdata:
                if "STOP" in tdata:
                    camera.robot_state = "stop"
                    camera.communication.board.write("rf:a" + FIELD_ID + ROBOT_ID + "ACK------\n")                
                elif "START" in tdata:
                    camera.robot_state = "ball search"
                    camera.communication.board.write("rf:a" + FIELD_ID + ROBOT_ID + "ACK------\n")                
                elif "PING" in tdata:
                    camera.communication.board.write("rf:a" + FIELD_ID + ROBOT_ID + "ACK------\n")                


    # camera.refree.whatsUp()
# robot = RobotController()

# robot.start()
