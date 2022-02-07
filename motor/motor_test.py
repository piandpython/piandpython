#Load libraries
import RPi.GPIO as GPIO
from RPLCD import i2c
from time import sleep

MotorButton = 18
MotorRelay = 6

#set GPIO to BCM mode - pins using GPIO names
GPIO.setmode(GPIO.BCM)


GPIO.setup(MotorButton, GPIO.IN)
GPIO.setup(MotorRelay, GPIO.OUT)

#Turn motor off
GPIO.output (MotorRelay, GPIO.LOW)

try:
    while True:
        
        if GPIO.input (MotorButton) == GPIO.LOW:
            print ("Button Push")
            GPIO.output (MotorRelay, GPIO.HIGH)
        if GPIO.input (MotorButton) == GPIO.HIGH:
            print ("Button Release")
            GPIO.output (MotorRelay, GPIO.LOW)
            
        
finally:
    GPIO.cleanup()