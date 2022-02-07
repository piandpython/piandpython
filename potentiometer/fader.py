#Use potentiometer with ADS7830

import RPi.GPIO as GPIO
import time
#from pynput import keyboard
#must install ADCDevice module from https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Libs/Python-Libs
from ADCDevice import *

ledPin = 22
adc = ADS7830() # Define an ADCDevice class object
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin,GPIO.OUT)
p = GPIO.PWM(ledPin,1000)
p.start(0)

try:
    while True:       
        value = adc.analogRead(0) # read the ADC value of channel 0
        oldvoltage = value / 255.0 * 3.3 # calculate the voltage value
        voltage=round (oldvoltage,1)
        p.ChangeDutyCycle(voltage*30.1) # Mapping to PWM duty cycle
        print ('ADC Value : %d, Voltage : %.2f'%(value,voltage))
        time.sleep(0.03)

finally:
    adc.close()
    GPIO.cleanup()