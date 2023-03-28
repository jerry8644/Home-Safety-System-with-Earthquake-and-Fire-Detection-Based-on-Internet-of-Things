import object_door
import SHT31
import bmp180
import Adafruit_DHT
import smoke_detect
import time
import RPi.GPIO as GPIO
PWM_FREQ =50
STEP = 15
SPICLK = 23#11
SPIMISO = 21#9
SPIMOSI = 19#10
SPICS = 24#8
class Room:
	def __init__(self, mq2_dpin_up, mq2_apin_up, mq2_dpin_down, mq2_apin_down, pir_sensor, dht11_pin, door_pin, button):#dht11 BCM
		self.mq2_dpin_up = mq2_dpin_up
		self.mq2_apin_up = mq2_apin_up
		if(mq2_dpin_down == None):
			self.mq2_dpin_down = 0
			self.mq2_apin_down = 0
		else:
			self.mq2_dpin_down = mq2_dpin_down
			self.mq2_apin_down = mq2_apin_down
		self.pir_sensor = pir_sensor
		self.dht11_pin = dht11_pin
		self.people_status = False #no people
		self.door_status = False #close
		# ~ self.temp_sht31 = 0
		# ~ self.humi_sht31 = 0
		# ~ self.temp_bmp180 = 0
		# ~ self.pressure = 0
		# ~ self.altitude = 0
		self.humi_dht11 = 0
		self.temp_dht11 = 0
		self.smoke_value_up = 0
		self.smoke_value_down = 0
		self.door_pin = door_pin
		self.button = button
		self.count = 0
		if(door_pin == None):
			self.pwm = 0
		else:
			self.pwm = GPIO.PWM(self.door_pin, PWM_FREQ)
			self.pwm.start(0)
		
	# ~ def Sht31(self):#temperature, humidity
		# ~ self.temp_sht31, self.humi_sht31= SHT31.temp_humi_value()
	
	def Dht11(self):#temperature, humidity
		DHT_SENSOR = Adafruit_DHT.DHT11
		self.humi_dht11 , self.temp_dht11= Adafruit_DHT.read_retry(DHT_SENSOR,self.dht11_pin)
		
	# ~ def Check_pir(self,channel):
		# ~ print("There are people in chen room")
		# ~ self.people_status = True
	
	# ~ def Detect_pir(self):
		# ~ GPIO.add_event_detect(self.pir_sensor, GPIO.RISING, self.Check_pir, bouncetime=1000)
	
	def Pir_value(self):
		input_value = GPIO.input(self.pir_sensor)
		return input_value
	
	# ~ def Pressure(self):
		# ~ self.temp_bmp180, self.pressure, self.altitude = bmp180.temp_pressure_altitude_value()
		

	def Smoke(self):
		COlevel=smoke_detect.readadc(self.mq2_apin_up, SPICLK, SPIMOSI, SPIMISO, SPICS)
		self.smoke_value_up = "%.2f"%((COlevel/1024.)*3.3)
		return self.smoke_value_up
		
	def __angle_to_duty_cycle(self,angle=0):
		cycle=(0.05*PWM_FREQ) + (0.19*PWM_FREQ*angle/180)
		return cycle    
   
	def Door_operation(self,channel):
		print("success")
		self.count = self.count+1
		if(self.count%2!=0):
			self.open_door()
		else:
			self.close_door()
			
	def Check_door(self):
		GPIO.add_event_detect(self.button, GPIO.FALLING, self.Door_operation, bouncetime=1000)
		
	def open_door(self):
		for angle in range(1,91,STEP):
			dc = self.__angle_to_duty_cycle(angle)
			self.pwm.ChangeDutyCycle(dc)
			time.sleep(0.03)
			print("open door")
			self.door_status = True
			
	def close_door(self):
		for angle in range(90,0,-(STEP)):
			dc=self.__angle_to_duty_cycle(angle)
			self.pwm.ChangeDutyCycle(dc)
			time.sleep(0.03)
			print("close door")
			self.door_status = False
            
	# ~ def button_value(self):
		# ~ input_value = GPIO.input(self.button)
		# ~ return input_value
        
		

