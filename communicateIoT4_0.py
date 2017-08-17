'''Measure the distance or depth with an HCSR04 Ultrasonic sound
sensor and a Raspberry Pi.  Imperial and Metric measurements are available'''

# Al Audet
# MIT License

import time
import math
import json
import requests

#DEVICE_ID=1247
DEVICE_ID="b8:27:eb:d3:be:38"
MEASURE_ID=1506
URL = 'https://trial.canary.cp.iot.sap/iot/gateway/rest/measures/'
valid = True
if(valid):
    val = 100
    data = json.dumps({
        'measureIds': [MEASURE_ID],
        'values': ['{}'.format(val)],
        'logNodeAddr':3  })

    headers = {'Content-type': 'application/json'}

    try:
        r = requests.post(URL + str(DEVICE_ID),
                        data=data,
                        headers=headers,
                        cert=('./certificatesIoT/client.pem'),verify=False)

        if r.status_code == 200:
                print('Sent data weather data distance: {}'.format(val))
        else:
                print('===== Error sending data =====')
                print('==> HTTP Response: ', r.status_code)
                print('==> HTTP Content:', r.content)

    except requests.exceptions.RequestException as e:
        print(str(e))
