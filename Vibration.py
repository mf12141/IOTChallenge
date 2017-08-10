# This section is for remote debugging from Eclipse on my PC
"""
import sys
sys.path.append(r'/home/pi/Public/Projects/Elevator')
import pydevd
from pydevd_file_utils import setup_client_server_paths
MY_PATHS_FROM_ECLIPSE_TO_PYTHON = [
    ('/Users/i010317/eclipse-workspace/RemoteSystemsTempFiles/192.168.1.67/home/pi/Public/Projects/Elevator', '/home/pi/Public/Projects/Elevator'),
]
setup_client_server_paths(MY_PATHS_FROM_ECLIPSE_TO_PYTHON)
pydevd.settrace('192.168.1.64') # replace IP with address 
                                # of Eclipse host machine
"""
# all configuration settings come from config.py
try:
    import config
except ImportError:
    print("File config.py is missing - it must be configured to use this test!"); exit();
    
#debug_communication=1
debug_communication=0

import urllib3
import time
import json

import sys
import signal

import RPi.GPIO as GPIO
import math as m

class VibrationSensor(object):
    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback, bouncetime=1)
        self.count = 0

    def callback(self , pin):
        self.count += 1


class TrafficLightSensor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #Broadcom pin-numbering scheme.  This uses the pin numbers that match the pin numbers on the Pi Traffic Light
        GPIO.setup(config.pin_traffic_light_red,GPIO.OUT)  # Red LED pin set as output
        GPIO.setup(config.pin_traffic_light_yellow,GPIO.OUT)  # Yellow LED pin set as output
        GPIO.setup(config.pin_traffic_light_green,GPIO.OUT) # Green LED pin set as output

    def LedOn(self,led):
        GPIO.output(led, 1)

    def LedOff(self,led):
        GPIO.output(led, 0)

def main():
    '''****************************************************************************************
                       HCP services Variables
    ****************************************************************************************'''
    try:
        urllib3.disable_warnings()
    except:
        print("urllib3.disable_warnings() failed - get a recent enough urllib3 version to avoid potential InsecureRequestWarning warnings! Can and will continue though.")
    
    # use with or without proxy
    if (config.proxy_url == ''):
        http = urllib3.PoolManager()
    else:
        http = urllib3.proxy_from_url(config.proxy_url)
        
    headers = urllib3.util.make_headers(user_agent=None)
    headers['Authorization'] = 'Bearer ' + config.oauth_credentials_for_device
    headers['Content-Type'] = 'application/json;charset=utf-8'
    url='https://iotmms' + config.hcp_account_id + config.hcp_landscape_host + '/com.sap.iotservices.mms/v1/api/http/data/'+ str(config.device_id)

    vSensor = VibrationSensor(config.pin_vibration)
    tlSensor = TrafficLightSensor()
    loopCount = 0
    try:
        while True:
            time.sleep(1)
            value = vSensor.count;
            if (loopCount == 60 or value >=100):
                loopCount = 0
                send_to_hcp(http, url, headers, value)
                poll_from_hcp(http, url, headers, tlSensor)
            else:
                loopCount += 1
            print(value)
            if (value >=100):
                tlSensor.LedOn(config.pin_traffic_light_yellow)
            else:
                tlSensor.LedOff(config.pin_traffic_light_yellow)
            vSensor.count = 0

    except KeyboardInterrupt:
        GPIO.cleanup()
    
def send_to_hcp(http, url, headers, value):
    timestamp=int(time.time())
    additionalData='Sample additional data'
    body='{"mode":"async", "messageType":"' + str(config.message_type_vibration) + '", "messages":[{"timestamp":"' + str(timestamp) + '", "level":"' + str(value) + '", "additionalData":"' + str(additionalData) + '"}]}'
    # print(body)
    r = http.urlopen('POST', url, body=body, headers=headers)
    if (debug_communication == 1):
        print("send_to_hcp():" + str(r.status))
        print(r.data)

def poll_from_hcp(http, url, headers, tlSensor):
    global msg_string

    r = http.urlopen('GET', url, headers=headers)
    if (debug_communication == 1):
        print("poll_from_hcp():" + str(r.status))
        print(r.data)
    json_string='{"all_messages":'+(r.data).decode("utf-8")+'}'
    # print(json_string)

    try:
        json_string_parsed=json.loads(json_string)
        # print(json_string_parsed)
        # take care: if multiple messages arrive in 1 payload - their order is last in / first out - so we need to traverse in reverese order
        try:
            messages_reversed=reversed(json_string_parsed["all_messages"])
            for single_message in messages_reversed:
                # print(single_message)
                payload=single_message["messages"][0]
                action=payload["action"]
                target=payload["target"]
                # print(opcode)
                # print(operand)
                # now do things depending on the opcode
                if (action == "ON"):
                    tlSensor.LedOn(int(target))
                else:
                    if (action == "OFF"):
                        tlSensor.LedOff(int(target))
                msg_string=payload["additionalData"]
                print(msg_string)
        except TypeError:
            print("Problem decoding the message " + (r.data).decode("utf-8") + " retrieved with poll_from_hcp()! Can and will continue though.")
    except ValueError:
        print("Problem decoding the message " + (r.data).decode("utf-8") + " retrieved with poll_from_hcp()! Can and will continue though.")

if __name__ == '__main__':
    main()