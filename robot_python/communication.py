import serial
from settings import *
class CommunicationController:
    def __init__(self):
        global board
        board = serial.Serial(ROBOT_SERIAL, BAUDRATE, serial.EIGHTBITS, timeout=0)
        self.count = 0
        print("Communication controller")

    def sendCommand(self, right, back, left):
        self.count += 1
        if self.count >= BUFFER_RESET_BOUND:
            board.reset_output_buffer()
            board.reset_input_buffer()
            self.count = 0
        #format:
        #sd:BACKWHEEL:RIGHTWHEEL:LEFTWHEEL\n
        command = ":".join(("sd", str(right), str(left), str(back) ))
        if board.is_open:
            board.write(command + '\n')
        # print(command)

    def throwBall(self, value):
        if board.is_open:
            command = ":".join(("d",str(value)))
            print(command)
            board.write(command + '\r\n')
            print("Throw")
        else:
            print("No board")
