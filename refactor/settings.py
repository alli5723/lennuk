ORANGE_BOUNDARIES = ((0, 102, 150), (27, 255, 255))
GREEN_BOUNDARIES = ((47, 82, 44), (80, 205, 172))
VIDEO_DEVICE = 0
ROBOT_SERIAL = "/dev/ttyS0" # "/dev/cu.usbmodem1411" ///ttyACM0
BAUDRATE = 19200
BUFFER_RESET_BOUND = 25
ack = "ACK-----"

robotID = "A"
fieldID = "K"


#dmesg | egrep --color 'serial|ttyS'
#cu -l /dev/ttyS0 -s 19200