import RPi.GPIO as GPIO
import time
#BCM
SPICLK = 23#11
SPIMISO = 21#9
SPIMOSI = 19#10
SPICS = 24#8

chih_mq2_dpin = 16#23
chih_mq2_apin = 4#channel

living_mq2_dpin = 7#4
living_mq2_apin = 2#channel

out_mq2_dpin = 29#5
out_mq2_apin = 1#channel

chen_mq2_dpin = 37#26
chen_mq2_apin = 0#channel
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler

#port init
def init():
         GPIO.setwarnings(False)
         GPIO.cleanup()			#clean up at the end of your script
         GPIO.setmode(GPIO.BOARD)		#to specify whilch pin numbering system
         # set up the SPI interface pins
         GPIO.setup(SPIMOSI, GPIO.OUT)
         GPIO.setup(SPIMISO, GPIO.IN)
         GPIO.setup(SPICLK, GPIO.OUT)
         GPIO.setup(SPICS , GPIO.OUT)
         GPIO.setup(out_mq2_dpin ,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
         GPIO.setup(chen_mq2_dpin ,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
         GPIO.setup(chih_mq2_dpin ,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
         GPIO.setup(living_mq2_dpin ,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

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

                        


