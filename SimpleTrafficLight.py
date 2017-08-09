# This section is for remote debugging from Eclipse on my PC
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

# This is the start of the actual program
import os
import time
import RPi.GPIO as gpio
import config
# Pin Setup:
gpio.setmode(gpio.BCM)  #Broadcom pin-numbering scheme.  This uses the pin numbers that match the pin numbers on the Pi Traffic Light
gpio.setup(config.pin_traffic_light_red,gpio.OUT)  # Red LED pin set as output
gpio.setup(config.pin_traffic_light_yellow,gpio.OUT)  # Yellow LED pin set as output
gpio.setup(config.pin_traffic_light_green,gpio.OUT)
# Set the pin HIGH
gpio.output(config.pin_traffic_light_red, True)  # Turns on the Red Light
time.sleep(1)
gpio.output(config.pin_traffic_light_yellow, True)
time.sleep(1)
gpio.output(config.pin_traffic_light_green, True)
time.sleep(1)
gpio.output(config.pin_traffic_light_red, False)
time.sleep(1)
gpio.output(config.pin_traffic_light_yellow, False)
time.sleep(1)
gpio.output(config.pin_traffic_light_green, False)
 # GPIO.setup(10, GPIO.OUT) # Yellow LED
 # GPIO.setup(11, GPIO.OUT) # Green LED pin as output
