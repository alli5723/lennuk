import serial
from settings import *
class CommunicationController:
    def __init__(self):
        global board
        board = serial.Serial(ROBOT_SERIAL, BAUDRATE, serial.EIGHTBITS, timeout=0)
        self.count = 0
        print("Communication controller")

    def sendCommand(self, right, back, left, pid):
        self.count += 1
        if self.count >= BUFFER_RESET_BOUND:
            board.reset_output_buffer()
            board.reset_input_buffer()
        #format:
        #sd:BACKWHEEL:RIGHTWHEEL:LEFTWHEEL:pid\n
        command = ":".join(("sd", str(back), str(right), str(left), str(pid)))
        if board.is_open:
            board.write(command + '\n')
        print(command)
