import serial
from settings import *
class CommunicationController:
    def __init__(self):
        for n in range(5):
            try:
                self.board = serial.Serial("/dev/ttyACM" + str(n), BAUDRATE, serial.EIGHTBITS, timeout=0)
            except:
                continue
        self.board.reset_output_buffer()
        self.board.reset_input_buffer()
        self.count = 0
        print("Communication controller")

    def sendCommand(self, right, back, left):
        self.count += 1
        if self.count >= BUFFER_RESET_BOUND and self.board.is_open:
            self.board.reset_output_buffer()
            self.board.reset_input_buffer()
            self.count = 0
        #format:
        #sd:RIGHTWHEEL:LEFTWHEEL:BACKWHEEL\n
        command = ":".join(("sd", str(right), str(left), str(back)))
        if self.board.is_open:
            self.board.write(command + '\n')

        # print(command)


    def shoot_ball(self, value):
        if self.board.is_open:
            # command = ":".join(("d",str(value)))
            command = "d:" + str(value) + "\n"
            print(command)
            self.board.write(command)
            print("Throw")
        else:
            print("No board")
