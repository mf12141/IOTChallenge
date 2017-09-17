'''Measure the distance or depth with an HCSR04 Ultrasonic sound
sensor and a Raspberry Pi.  Imperial and Metric measurements are available'''

# Al Audet
# MIT License

import time
import math
import json
import requests

#DEVICE_ID=1247
#DEVICE_ID=1468
DEVICE_ID="74:da:38:56:03:f0"
#MEASURE_ID=1506
#MEASURE_ID=100
URL = 'https://trial.canary.cp.iot.sap/iot/gateway/rest/measures/'
#URL = 'https://trial.canary.cp.iot.sap:8883/measures/'
valid = True
if(valid):
    raw_data = {}
    raw_data['logNodeAddr'] = 2
    raw_data['profileId'] = 48
    raw_data['values'] = []
    raw_data['values'].append("30")
    raw_data['values'].append("28")
    raw_data['measureIds'] = []
    raw_data['measureIds'].append(100)
    raw_data['measureIds'].append(101)
#    data = json.dumps({
#        'measureIds': [100,101],
#        'values': ['{}'.format(val)],
#        'logNodeAddr':3  })
    data = json.dumps(raw_data)
    print(data)

    headers = {'Content-type': 'application/json'}

    try:
#        r = requests.post(URL + str(DEVICE_ID),
#                        data=data,
#                        headers=headers,
#                        cert=('./certificates/client.pem'),verify=False)
        r = requests.post(URL + str(DEVICE_ID),
                        data=data,
                        headers=headers,
                        cert=('./certificates/client.crt.pem','./certificates/client.key.pem'),verify=False)

        if r.status_code == 200:
                print('Sent data successfully')
        else:
                print('===== Error sending data =====')
                print('==> HTTP Response: ', r.status_code)
                print('==> HTTP Content:', r.content)

    except requests.exceptions.RequestException as e:
        print(str(e))