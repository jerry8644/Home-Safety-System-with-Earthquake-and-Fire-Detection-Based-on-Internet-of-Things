#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
def read_card():
		print("Tag card")
		id, text = reader.read()
		if(id == 439328120783):
			print(id)
			print(text)
			return True
		else:
			print("None")
			return False


