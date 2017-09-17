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
    import config4
except ImportError:
    print("File config4.py is missing - it must be configured to use this test!") 
    exit()
    
#debug_communication=1
debug_communication=0

import urllib3
import time
import json

import sys
import signal

import RPi.GPIO as GPIO
import math

import paho.mqtt.client as mqtt
import ssl

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import Adafruit_DHT

class LightSensor(object):
    def __init__(self):
        self.measure = config4.measure_light_sensor
        self.mcp = Adafruit_MCP3008.MCP3008(clk=config4.pin_analog_spiclk, cs=config4.pin_analog_spics, 
                                   miso=config4.pin_analog_spimiso, mosi=config4.pin_analog_spimosi)
        
    def getValue(self):
        return self.mcp.read_adc(config4.light_sensor_analog_register)

class VibrationSensor(object):
    def __init__(self):
        self.measure = config4.measure_vibration_sensor
        self.pin = config4.pin_vibration
        self.count = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.callback, bouncetime=1)

    def callback(self, pin):
        self.count += 1

    def getValue(self):
        h_count = self.count
        self.count = 0
        return h_count

class DistanceSensor(object):
    def __init__(self,
                 temperature=20,
                 unit='metric',
                 round_to=1
                 ):
        self.measure = config4.measure_distance_sensor
        self.trig_pin = config4.pin_ultrasonic_dist_trig
        self.echo_pin = config4.pin_ultrasonic_dist_echo
        self.temperature = temperature
        self.unit = unit
        self.round_to = round_to
               
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def raw_distance(self, sample_size=11, sample_wait=0.1):
        '''Return an error corrected unrounded distance, in cm, of an object
        adjusted for temperature in Celcius.  The distance calculated
        is the median value of a sample of `sample_size` readings.
        Speed of readings is a result of two variables.  The sample_size
        per reading and the sample_wait (interval between individual samples).
        Example: To use a sample size of 5 instead of 11 will increase the
        speed of your reading but could increase variance in readings;
        value = sensor.Measurement(trig_pin, echo_pin)
        r = value.raw_distance(sample_size=5)
        Adjusting the interval between individual samples can also
        increase the speed of the reading.  Increasing the speed will also
        increase CPU usage.  Setting it too low will cause errors.  A default
        of sample_wait=0.1 is a good balance between speed and minimizing
        CPU usage.  It is also a safe setting that should not cause errors.
        e.g.
        r = value.raw_distance(sample_wait=0.03)
        '''

        if self.unit == 'imperial':
            self.temperature = (self.temperature - 32) * 0.5556
        elif self.unit == 'metric':
            pass
        else:
            raise ValueError(
                'Wrong Unit Type. Unit Must be imperial or metric')

        speed_of_sound = 331.3 * math.sqrt(1+(self.temperature / 273.15))
        sample = []
        # setup input/output pins
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        """

        for distance_reading in range(sample_size):
            GPIO.output(self.trig_pin, GPIO.LOW)
            time.sleep(sample_wait)
            GPIO.output(self.trig_pin, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_pin, False)
            echo_status_counter = 1
            
            while GPIO.input(self.echo_pin) == 0:
                if echo_status_counter < 1000:
                    sonar_signal_off = time.time()
                    echo_status_counter += 1
                else:
                    raise SystemError('Echo pulse was not received')
            while GPIO.input(self.echo_pin) == 1:
                sonar_signal_on = time.time()
            time_passed = sonar_signal_on - sonar_signal_off
            distance_cm = time_passed * ((speed_of_sound * 100) / 2)
            sample.append(distance_cm)
        sorted_sample = sorted(sample)
        """
        # Only cleanup the pins used to prevent clobbering
        # any others in use by the program
        GPIO.cleanup((self.trig_pin, self.echo_pin))
        """
        return sorted_sample[sample_size // 2]

    def depth_metric(self, median_reading, hole_depth):
        '''Calculate the rounded metric depth of a liquid. hole_depth is the
        distance, in cm's, from the sensor to the bottom of the hole.'''
        return round(hole_depth - median_reading, self.round_to)

    def depth_imperial(self, median_reading, hole_depth):
        '''Calculate the rounded imperial depth of a liquid. hole_depth is the
        distance, in inches, from the sensor to the bottom of the hole.'''
        return round(hole_depth - (median_reading * 0.394), self.round_to)

    def distance_metric(self, median_reading):
        '''Calculate the rounded metric distance, in cm's, from the sensor
        to an object'''
        return round(median_reading, self.round_to)

    def distance_imperial(self, median_reading):
        '''Calculate the rounded imperial distance, in inches, from the sensor
        to an oject.'''
        return round(median_reading * 0.394, self.round_to)
    
    def getValue(self):
        return self.raw_distance()

class SmokeSensor(object): 
    def __init__(self):
        self.measure = config4.measure_smoke_sensor
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)        #to specify whilch pin numbering system
        # set up the SPI interface pins
        GPIO.setup(config4.pin_analog_spimosi, GPIO.OUT)
        GPIO.setup(config4.pin_analog_spimiso, GPIO.IN)
        GPIO.setup(config4.pin_analog_spiclk, GPIO.OUT)
        GPIO.setup(config4.pin_analog_spics, GPIO.OUT)
        GPIO.setup(config4.pin_smoke_digital,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

    #read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(cspin, True)    

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

    def getValue(self):
        COlevel=self.readadc(config4.pin_smoke_analog, config4.pin_analog_spiclk, 
                        config4.pin_analog_spimosi, config4.pin_analog_spimiso, 
                        config4.pin_analog_spics)
        if GPIO.input(config4.pin_smoke_digital):
             return "0"
        else:
             return str("%.2f"%((COlevel/1024.)*3.3))

class TemperatureSensor(object):
    def __init__(self):
        self.measure = config4.measure_temperature_sensor
        self.measure_humidity = config4.measure_humidity_sensor

    def getValue(self):
        self.humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, config4.pin_temp)
        return temperature
    
    def getHumidity(self):
        return self.humidity
    
class TrafficLightSensor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #Broadcom pin-numbering scheme.  This uses the pin numbers that match the pin numbers on the Pi Traffic Light
        GPIO.setup(config4.pin_traffic_light_red,GPIO.OUT)  # Red LED pin set as output
        GPIO.setup(config4.pin_traffic_light_yellow,GPIO.OUT)  # Yellow LED pin set as output
        GPIO.setup(config4.pin_traffic_light_green,GPIO.OUT) # Green LED pin set as output

    def LedOn(self,led):
        GPIO.output(led, 1)

    def LedOff(self,led):
        GPIO.output(led, 0)

class InterfaceWithCloud(object):
    def __init__(self):
        self.client = mqtt.Client(client_id=config4.device_mac_address)
        self.client.tls_set(config4.path_to_landscape_certificate, 
               certfile=config4.path_to_certificate, 
               keyfile=config4.path_to_private_key, 
               cert_reqs=ssl.CERT_REQUIRED, 
               tls_version=ssl.PROTOCOL_SSLv23, 
               ciphers=None)
        
    def on_connect_broker(self,client, userdata, flags, rc):
        print("Connected to MQTT broker with result code " + str(rc))
        
    def connect(self):
        self.client.on_connect = self.on_connect_broker
        self.client.connect(config4.cloud_system,config4.cloud_system_port_mqtt)
        self.client.loop_start()
        
    def publish(self,payload):
        print("trying to publish")
        publish_topic=config4.cloud_system_url_extension + config4.device_mac_address
        result=self.client.publish(publish_topic, payload, qos=0)
        print(result)
        
class SensorSet(object):
    def __init__(self):
        self.oVibration = VibrationSensor()
        self.oLight = LightSensor()
        self.oTemperature = TemperatureSensor()
        self.oDistance = DistanceSensor()
        self.oSmoke = SmokeSensor()
        self.oTrafficLight = TrafficLightSensor()   
        
    def get_message(self):
        time.sleep(config4.pause_interval_message)
        raw_data = {}
        raw_data['logNodeAddr'] = config4.cloud_system_log_node_addr
        raw_data['profileId'] = config4.cloud_system_profile_id
        raw_data['measureIds'] = []
        raw_data['values'] = []
        raw_data['measureIds'].append(self.oLight.measure)
        raw_data['values'].append(self.oLight.getValue())
        raw_data['measureIds'].append(self.oTemperature.measure)
        raw_data['values'].append(self.oTemperature.getValue())
        raw_data['measureIds'].append(self.oTemperature.measure_humidity)
        raw_data['values'].append(self.oTemperature.getHumidity())
        raw_data['measureIds'].append(self.oDistance.measure)
        raw_data['values'].append(self.oDistance.getValue())
        raw_data['measureIds'].append(self.oSmoke.measure)
        raw_data['values'].append(self.oSmoke.getValue())
        raw_data['measureIds'].append(self.oVibration.measure)
        raw_data['values'].append(self.oVibration.getValue())
        data = json.dumps(raw_data)
        print(data)
        return data

def main():
    '''****************************************************************************************
                       HCP services Variables
    ****************************************************************************************'''
    oInterface = InterfaceWithCloud()
    oInterface.connect()
    oSensorSet = SensorSet()
    try:
        while True:
            time.sleep(config4.pause_interval_detection)
            message = oSensorSet.get_message()
            print(message)
            oInterface.publish(message);

    except KeyboardInterrupt:
        GPIO.cleanup()
    
if __name__ == '__main__':
    main()