import RPi.GPIO as GPIO
import time
# ~ GPIO.setmode(GPIO.BCM)

class Door:
    def __init__(self, pwm, CONTROL_PIN, PWM_FREQ, button):
        self.pwm = pwm
        self.CONTROL_PIN = CONTROL_PIN
        self.button = button
        self.count = 0
        self.step = 15
        self.pwm_freq = PWM_FREQ
        
    def __angle_to_duty_cycle(self,angle=0):
        cycle=(0.05*self.pwm_freq) + (0.19*self.pwm_freq *angle/180)
        return cycle    
    
    def open_door(self, pwm):
        for angle in range(1,91,self.step):
            dc = self.__angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.03)
            print(1)
            
    def close_door(self, pwm):
        for angle in range(90,0,-(self.step)):
            dc=self.__angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.03)
            
    def button_value(self):
        input_value = GPIO.input(self.button)
        return input_value
        

