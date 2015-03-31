import requests
import json
import serial
import time

import random
import datetime

# ser = serial.Serial('/dev/ttyACM0', 115200)



while True:
    try:
        # create dummy data
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        latitude = round(random.uniform(1.5, 1.9), 5)
        longitude = round(random.uniform(1.5, 1.9), 5)

        payload = [timestamp, latitude, longitude]

        for i in range(0, 5):
            imu = [
                random.randint(-16000, 16000),
                random.randint(-16000, 16000),
                random.randint(-16000, 16000),
                random.randint(-16000, 16000),
                random.randint(-16000, 16000),
                random.randint(-16000, 16000)]
            payload.append(imu)
        payload = json.dumps(payload)

        # send
        url = 'http://183.90.171.55:8080/log' # AMR server
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=payload, headers=headers)

        print(payload)
        print("%d"
              % (r.status_code))
    except:
        print("-- Failed")
    time.sleep(1)
    # break
