import serial
import time

now = time.time()
future = now + 10
count = 0

# ser = serial.Serial('/dev/tty.usbmodem1421', 115200)
ser = serial.Serial('/dev/ttyACM0', 115200)

while time.time() < future:
    raw_data = ser.readline()
    # print(raw_data,count)
    if ( raw_data ):
        count += 1
    pass

print(count)

### 6 values 10 second
# read by mac = 2742
# read by mac = 2750
# read by mac = 2743
# read by mac = 2752
# read by mac = 2753
# read by raspi = 924

### 1 value 10 seconds
# read by mac = 6356
# read by raspi = 5224