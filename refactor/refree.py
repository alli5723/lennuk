import serial

import time

my_ident = 'OZ'

 

with serial.Serial('/dev/ttyACM0') as s:

    while True:

        tdata = s.read()           # Wait forever for anything

        time.sleep(0.01)              # Sleep (or inWaiting() doesn't give the correct value)

        data_left = s.inWaiting()  # Get the number of characters ready to be read

        tdata += s.read(data_left) # Do the read and combine it with the first character

        cmd = tdata.decode()[5:17]

        ident = cmd[1:3]

        print("Recieved: " + tdata.decode())

        print("Identiy: " + ident)

        req = cmd.split("-")[0][3:]

        print("Command: " + req)

        if ident == my_ident:

            print("Identity match, sending ACK")

            s.write(str.encode("rf:a" + my_ident + "ACK------\n"))

            print("rf:a"+ my_ident + "ACK------\n")

        print()