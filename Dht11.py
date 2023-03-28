import Adafruit_DHT
import RPi.GPIO as GPIO

DHT_SENSOR = Adafruit_DHT.DHT11
#BCM
class DHT11:
	def __init__(self,CONTROL_PIN):
		self.CONTROL_PIN = CONTROL_PIN


	def value(self):
		humidity, temperature= Adafruit_DHT.read_retry(DHT_SENSOR,self.CONTROL_PIN)
		return humidity, temperature		


