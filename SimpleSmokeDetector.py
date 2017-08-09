import RPi.GPIO as GPIO
import time
import config

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()            #clean up at the end of your script
         GPIO.setmode(GPIO.BCM)        #to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(config.pin_analog_spimosi, GPIO.OUT)
         GPIO.setup(config.pin_analog_spimiso, GPIO.IN)
         GPIO.setup(config.pin_analog_spiclk, GPIO.OUT)
         GPIO.setup(config.pin_analog_spics, GPIO.OUT)
         GPIO.setup(config.pin_smoke_digital,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
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
#main ioop
def main():
         init()
         print"Please wait..."
         time.sleep(20)
         while True:
                  COlevel=readadc(config.pin_smoke_analog, config.pin_analog_spiclk, config.pin_analog_spimosi, config.pin_analog_spimiso, config.pin_analog_spics)

                  if GPIO.input(config.pin_smoke_digital):
                           print("No Smoke Detected")
                           time.sleep(0.5)
                  else:
                           print("Smoke Detected")
                           print"Current Gas AD value = " +str("%.2f"%((COlevel/1024.)*3.3))+" V"
                           time.sleep(0.5)

if __name__ =='__main__':
         try:
                  main()
                  pass
         except KeyboardInterrupt:
                  pass

GPIO.cleanup()