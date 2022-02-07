#Load libraries
import RPi.GPIO as GPIO
from RPLCD import i2c
from time import sleep

#set GPIO to BCM mode - pins using GPIO names
GPIO.setmode(GPIO.BCM)

#Configure blinking sequence variables and set count to zero
blinkCount = 3
count = 0

#Create class for LEDs so mutliple properties can be assigned
class led:
    def __init__(self, color, pin):
        self.color = color
        self.pin = pin


#Configure GPIO pin number constants
LEDPinRED = led("RED", 22)
LEDPinBLUE = led("BLUE", 19)
LEDPinGREEN = led("GREEN", 5)
BUZZERPin = 17
Motor1 = 18
Motor2 = 6

#Configure LCD constants
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27
port = 1

#Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

#clear LCD from previous run
lcd.close(clear=True)
lcd.backlight_enabled = False

#Set up GPIO pins for lights and buzzer
GPIO.setup(LEDPinRED.pin, GPIO.OUT)
GPIO.setup(LEDPinBLUE.pin, GPIO.OUT)
GPIO.setup(LEDPinGREEN.pin, GPIO.OUT)
GPIO.setup(BUZZERPin, GPIO.OUT)
GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)

#Create array of lights
lights = [LEDPinRED,LEDPinBLUE,LEDPinGREEN]

#Create function to turn light on, signal with buzzer and notify on screen and on the LCD
def lightbuzzerlcd():
    for light in lights:
        lcd.backlight_enabled = True
        lcd.close(clear=True)
        GPIO.output(light.pin, True)
        print (light.color + " LED ON")
        lcd.clear()
        lcd.write_string(light.color + " LED ON")
        sleep (3)
        GPIO.output(light.pin , False)
        print (light.color + " LED OFF")
        lcd.clear()
        lcd.write_string(light.color + " LED OFF")
        GPIO.output(BUZZERPin,1)
        sleep(.05)
        GPIO.output(BUZZERPin,0)
    
#Main
try:
    lcd.backlight_enabled = True
    lcd.close(clear=True)
    lcd.write_string('Hello')
    print ("Hello")
    sleep (3)
    lcd.clear()
    lcd.write_string('Motor going forward')
    GPIO.output (Motor1, GPIO.LOW)
    GPIO.output (Motor2, GPIO.HIGH)
    sleep (1)
    GPIO.output (Motor1, GPIO.LOW)
    GPIO.output (Motor2, GPIO.LOW)
    sleep (3)
    lcd.clear()
    lcd.write_string('Motor going backward')
    GPIO.output (Motor1, GPIO.LOW)
    GPIO.output (Motor2, GPIO.HIGH)
    sleep (1)
    GPIO.output (Motor1, GPIO.LOW)
    GPIO.output (Motor2, GPIO.LOW)
    sleep (3)
    while count < blinkCount:
        lightbuzzerlcd()
        count += 1
    lcd.clear()    
    lcd.write_string('Goodbye')
    print ("Goodbye")
    sleep (5)
finally:
    GPIO.cleanup()
    lcd.close(clear=True)
    lcd.backlight_enabled = False
