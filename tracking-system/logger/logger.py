import requests
import json
import serial
import time


ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
    raw_data = ser.readline()
    if(raw_data[0:1] == '--'):
        print(raw_data)
    else:
        raw = raw_data.strip().split(',')
        try:
            url = 'http://192.168.1.131:8080/log'
            payload = {
                'timestamp': json.dumps(raw[0]),
                'latitude': json.dumps(float(raw[1])),
                'longitude': json.dumps(float(raw[2])),
                'ax': json.dumps(int(raw[3])),
                'ay': json.dumps(int(raw[4])),
                'az': json.dumps(int(raw[5])),
                'gx': json.dumps(int(raw[6])),
                'gy': json.dumps(int(raw[7])),
                'gz': json.dumps(int(raw[8]))
            }
            headers = {'content-type': 'application/json'}
            r = requests.post(url, data=payload, headers=headers)
            print("%s,%s,%s,%s,%s,%s -- %d"
                  % (raw[0], raw[1], raw[2], raw[3], raw[4], raw[5], r.status_code))
        except:
            print("-- Failed")
    time.sleep(1)
