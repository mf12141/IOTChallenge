#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import math as m
import config 

class Sw40(object):
    """docstring for Senal"""
    def __init__(self, pin , led):
        self.led = led
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led,GPIO.OUT)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback, bouncetime=1)
        self.count = 0

    def callback(self , pin):
        self.count += 1

    def LedOn(self):
        GPIO.output(self.led , 1)

    def LedOff(self):
        GPIO.output(self.led , 0)








def main():
    sensor = Sw40(config.pin_vibration,config.pin_traffic_light_yellow)
    try:
        while True:

            time.sleep(1)
            print(sensor.count);
            if sensor.count >=100:
                sensor.LedOn()
            else:
                sensor.LedOff()
            sensor.count = 0



    except KeyboardInterrupt:
        GPIO.cleanup()



if __name__ == '__main__':
    main()