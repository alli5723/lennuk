import serial
from settings import *
class CommunicationController:
    def __init__(self):
        global board
        board = serial.Serial(ROBOT_SERIAL, BAUDRATE, serial.EIGHTBITS, timeout=0)
        self.count = 0
        print("Communication controller")
        self.serialChannel = board
        self.CharCounter = 0
        self.initChar = 'a'
        self.listening = False
        self.respond = False
        self.kill_received = False
        self.game_state = False
        self.playingField = 'Z'
        self.robotID = 'Y'
        self.allRobotsChar = 'X'

    def sendCommand(self, right, back, left, pid):
        self.count += 1
        if self.count >= BUFFER_RESET_BOUND:
            board.reset_output_buffer()
            board.reset_input_buffer()
        #format:
        #sd:BACKWHEEL:RIGHTWHEEL:LEFTWHEEL:pid\n
        command = ":".join(("sd", str(back), str(right), str(left), str(pid), '\n'))
        print(command)
        if board.is_open:
            board.write(command.encode())

    # def listenToRefree(self):
    #     # print(board.readline())
    #     if board.is_open:
    #         refree_msg = board.read()
    #         print(refree_msg)
    #         board.write(ack.encode())
    #     else:
    #         print("board is not open")


    def write_ack_string(self):
        print("playingField: " + self.initChar + self.playingField + self.robotID + ack)
        print("intChar: " + (
        self.initChar + self.playingField + self.robotID  + ack).encode())
        message = ("rf:"+self.initChar + self.playingField + self.robotID  + ack + "\n").encode()
        print("message: " + message)
        self.serialChannel.write(message)

    def game_status(self):
        return self.game_state

    def listenToRefree(self):
        # print("ok")
        # while not self.kill_received:
        # self.CharCounter += 1
        char_signal = board.read()
        # print(char_signal)
        if char_signal == self.initChar:
            self.CharCounter = 0
            self.listening = True
            return #continue
        if not self.listening:
            return #continue  # wait for next a
        if self.CharCounter == 1 and char_signal != self.playingField:
            self.listening = False
        if self.CharCounter == 2 and char_signal != self.robotID  and char_signal != self.allRobotsChar:
            self.listening = False
        if self.CharCounter == 2 and char_signal == self.robotID :
            self.respond = True
        if self.CharCounter == 2 and char_signal == self.allRobotsChar:
            self.respond = False
        if self.CharCounter == 2 and self.listening:
            msg = ""
            for self.CharCounter in range(3, 12):
                char_signal = self.serialChannel.read()
                print(char_signal)
                if char_signal == self.initChar:
                    self.CharCounter = 0
                    break
                if char_signal == "-":
                    self.listening = False
                    break
                msg += char_signal
                if msg in ["START", "STOP"]:
                    print(msg)
                    if self.respond:
                        self.write_ack_string()

                    if msg == "START":
                        self.game_state = True
                    else:
                        self.sendCommand(0, 0, 0, 1)
                        self.game_state = False
