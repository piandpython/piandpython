#Load libraries
import RPi.GPIO as GPIO
from RPLCD import i2c
from time import sleep

#set GPIO to BCM mode - pins using GPIO names
GPIO.setmode(GPIO.BCM)

#Configure blinking sequence variables and set count to zero
blinkCount = 3
count = 0
timer=10

#Create class for LEDs so mutliple properties can be assigned
class led:
    def __init__(self, color, pin):
        self.color = color
        self.pin = pin


#Configure GPIO pin number constants
LEDPinRED = led("RED", 22)
LEDPinBLUE = led("BLUE", 19)
LEDPinGREEN = led("GREEN", 5)
button = 18
BUZZERPin = 17

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
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button with the initial state HIGH
GPIO.setup(BUZZERPin, GPIO.OUT)


#Create array of lights
lights = [LEDPinRED,LEDPinBLUE,LEDPinGREEN]

#button state to 0
state = 0

try:
    lcd.backlight_enabled = True
    lcd.close(clear=True)
    lcd.write_string('Hello')
    print ("Hello")
    print (timer)
    sleep (3)
    lcd.clear()
    lcd.write_string('Dont press the button!')
    while True:
        if GPIO.input (button) == GPIO.LOW:
            lcd.clear()
            lcd.write_string('You pressed the button!')
            sleep(1)
            while (timer > 0):
                lcd.clear()
                lcdtime=str(timer)
                lcd.write_string(lcdtime)
                timer -= 1
                sleep(1)
            lcd.clear()
            lcd.write_string("Boom!")
            GPIO.output(BUZZERPin,1)
            sleep(5)
            GPIO.output(BUZZERPin,0)
            lcd.clear()
            sleep(1)
            timer=10
            lcd.write_string('Dont press the button!')
finally:
    GPIO.cleanup()
    lcd.close(clear=True)
    lcd.backlight_enabled = False
        
        
        