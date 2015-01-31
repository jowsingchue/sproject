from random import uniform
import requests
import json
import datetime
import time

while True:
    timestamp = datetime.datetime.now()
    flat = round(uniform(13, 14), 6)
    flon = round(uniform(100, 101), 6)

    url = 'http://192.168.1.131:8080/log'
    payload = {
        'timestamp': json.dumps(timestamp.isoformat()),
        'latitude': json.dumps(flat),
        'longitude': json.dumps(flon)
    }
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=payload, headers=headers)
    print("timestamp = %s\nlatitude = %f, longitude = %f, status = %d"
          % (timestamp, flat, flon, r.status_code))

    time.sleep(1)
