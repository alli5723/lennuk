class CommunicationController:
    def __init__(self):
        port = "COM4"
        baud = 9600
        global board
        # board = serial.Serial(port, baud, serial.EIGHTBITS, timeout=0)
        print("Communication controller")

    def sendCommand(self, left, right, back, pid):
        # if board.isOpen:
        #     board.write(command + '\n')
        print(left, right, back, pid)
