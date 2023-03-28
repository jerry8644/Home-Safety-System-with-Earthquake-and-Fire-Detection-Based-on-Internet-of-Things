import RPi.GPIO as GPIO
import sys
import smbus2
import time
sys.modules['smbus'] = smbus2
pir_sensor = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sensor, GPIO.IN, GPIO.PUD_DOWN)
def pir_checked(channel):
	print("test")
try:
	GPIO.add_event_detect(pir_sensor, GPIO.RISING, pir_checked, bouncetime=1000)	
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()
# enter smoke code
# ~ class pir:
	# ~ def __init__(self, pir_sensor):
		# ~ self.pir_sensor = pir_sensor
