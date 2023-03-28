import object_door
import SHT31
import Adafruit_DHT
import smoke_detect
import time
import RPi.GPIO as GPIO

PWM_FREQ =500
STEP = 15
SPICLK = 23#11
SPIMISO = 21#9
SPIMOSI = 19#10
SPICS = 24#8


class Room:
	def __init__(self, up_mq2_dpin, up_mq2_apin,down_mq2_dpin, down_mq2_apin, pir_sensor, dht11_pin, door_pin, button):#dht11 BCM
		self.up_mq2_dpin = up_mq2_dpin
		self.up_mq2_apin = up_mq2_apin	
		self.dht11_pin = dht11_pin
		self.people_status = False #no people
		self.door_status = False #close
		self.fire_status_up=0
		self.fire_status_down=0
		self.temp_sht31 = 0
		self.humi_sht31 = 0
		self.humi_dht11 = 0
		self.temp_dht11 = 0
		self.smoke_value_up = 0
		self.smoke_value_down = 0
		# ~ self.temp_bmp180 = 0
		# ~ self.pressure = 0
		# ~ self.altitude = 0
		self.door_pin = door_pin
		self.button = button
		self.count = 0
		if(door_pin == None):
			self.pwm = 0
		else:
			self.pwm = GPIO.PWM(self.door_pin, PWM_FREQ)
			self.pwm.start(0)
		if (pir_sensor==None):
			self.pir_sensor=0
		else:
			self.pir_sensor = pir_sensor
			
		if(down_mq2_dpin==None):
			self.down_mq2_dpin = 0
			self.down_mq2_apin = 0
		else:
			self.down_mq2_dpin = down_mq2_dpin
			self.down_mq2_apin = down_mq2_apin
	
	def Sht31(self):#temperature, humidity
		self.temp_sht31, self.humi_sht31= SHT31.temp_humi_value()
		self.temp_sht31 = round(self.temp_sht31, 2)
		self.humi_sht31 = round(self.humi_sht31, 2)
	
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
		if input_value == 0:
			self.people_status = False
		else:
			self.people_status = True
	
	def Pressure(self):
		self.temp_bmp180, self.pressure, self.altitude = bmp180.temp_pressure_altitude_value()
		

	def Smoke(self):
		COlevel_up=smoke_detect.readadc(self.up_mq2_apin, SPICLK, SPIMOSI, SPIMISO, SPICS)
		COlevel_down=smoke_detect.readadc(self.down, SPICLK, SPIMOSI, SPIMISO, SPICS)
		self.smoke_value_up = "%.2f"%((COlevel_up/1024.)*3.3)
		self.smoke_value_down = "%.2f"%((COlevel_down/1024.)*3.3)
		
	def __angle_to_duty_cycle(self,angle=0):
		cycle=(0.05*PWM_FREQ) + (0.19*PWM_FREQ*angle/180)
		return cycle    
	
	def Door_operation(self,channel):
		print("Press button")
		if self.door_status == True:
			self.close_door()
		else:
			self.open_door()
			
	def Check_door(self):
		GPIO.add_event_detect(self.button, GPIO.FALLING, self.Door_operation, bouncetime=2000)
		
	def open_door(self):
		for angle in range(0,91,STEP):
			dc = self.__angle_to_duty_cycle(angle)
			self.pwm.ChangeDutyCycle(dc)
			time.sleep(0.03)
		print("open door")
		self.door_status = True
			
	def close_door(self):
		for angle in range(90,-1,-(STEP)):
			dc=self.__angle_to_duty_cycle(angle)
			self.pwm.ChangeDutyCycle(dc)
			time.sleep(0.03)
		print("close door")
		self.door_status = False
	
	def Get_fire(self):
		self.fire_status_up = int(GPIO.input(self.up_mq2_dpin)==0)
		if self.down_mq2_dpin == 0:
			self.fire_status_down = 0
		else:
			self.previous_fire_status_down = self.fire_status_down
			self.fire_status_down = int(GPIO.input(self.down_mq2_dpin)==0)
        
		

