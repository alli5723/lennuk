import serial
import time
from common import *
from settings import *

class RefreeController:
    
    def __init__(self, camera):
        self.my_ident = 'OZ'
        self.owner = camera
        print("Robot will listen to refree")
    
    def whatsUp(self):
        with self.owner.communication.board as s:

            print("Robot listening to refree")
            if s.readable():
                tdata = s.read()           # Wait forever for anything
            else: return
            time.sleep(0.01)              # Sleep (or inWaiting() doesn't give the correct value)
            data_left = s.inWaiting()  # Get the number of characters ready to be read
            tdata += s.read(data_left) # Do the read and combine it with the first character

            cmd = tdata.decode()[5:17]

            ident = cmd[1:3]

            print("Recieved: " + tdata.decode())

            print("Identiy: " + ident)

            req = cmd.split("-")[0][3:]

            print("Command: " + req)

            if ident == self.my_ident:
                ROBOT_STATE.STOP = False
                print("Identity match, sending ACK")

                s.write(str.encode("rf:a" + self.my_ident + "ACK------\n"))

                print("rf:a"+ self.my_ident + "ACK------\n")

                print()
