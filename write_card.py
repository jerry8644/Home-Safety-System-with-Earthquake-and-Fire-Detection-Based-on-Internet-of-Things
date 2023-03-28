#!/usr/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
def write():
		text = input('New data:')
		print("Now place your tag to write")
		reader.write(text)
		print("Written")


write()
GPIO.cleanup()
