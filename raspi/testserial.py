import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200)
while 1 :
    print(ser.readline())
    # time.sleep(1) # delays for 1 seconds
