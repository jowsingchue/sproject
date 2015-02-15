import requests
import json
import serial


ser = serial.Serial('/dev/ttyACM0', 115200)
# ser = serial.Serial('/dev/tty.usbmodem1421', 115200)

payload = []

# wait for the first valid data
while True:
    raw_data = ser.readline()
    if(raw_data[0:2] == '++'):
        payload = []
        raw = raw_data[2:].strip().split(',')
        payload = [
            raw[0],
            '%.6f' % float(raw[1]),
            '%.6f' % float(raw[2])]
        break;


while True:
    raw_data = ser.readline()
    if(raw_data[0:2] != '++'):
        raw = raw_data.strip().split(',')
        try:
            if (raw[5]):
                payload.append(raw)
        except:
            pass
    else:
        try:
            url = 'http://192.168.1.122:8080/log'
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            print(r.status_code)
        except:
            print("Failed")

        payload = []
        raw = raw_data[2:].strip().split(',')
        payload = [
            raw[0],
            '%.6f' % float(raw[1]),
            '%.6f' % float(raw[2])]

#     # time.sleep(1)
