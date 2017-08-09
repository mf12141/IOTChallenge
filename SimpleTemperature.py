#!/usr/bin/python

import sys
import Adafruit_DHT
import time
import config

def getLine(array):
    return str(sum(array) / float(len(array))) + "," + str(min(array)) + "," + str(max(array))

sensor = Adafruit_DHT.DHT11
gpio = config.pin_temp

h = []
t = []

count = 5
date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

print(date + ": ")

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

# Un-comment the line below to convert the temperature to Fahrenheit.
temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}F  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)