#libraries
import RPi.GPIO as GPIO
from RPLCD import i2c
from time import sleep

#set GPIO to BCM mode - pins using GPIO names
GPIO.setmode(GPIO.BCM)

#Configure blinking variables and set count to zero
blinkCount = 3
count = 0

#Configure GPIO LED and buzzer pin constants
LEDPinRED = 22
LEDPinBLUE = 19
LEDPinGREEN = 5
BUZZERPin = 17

#Configure LCD constants
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27
port = 1

# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

lcd.backlight_enabled = True
lcd.close(clear=True)
lcd.write_string('Hello, Starting program!')
sleep (3)
lcd.clear()
lcd.write_string('Bye for now')
#lcd.cursor_pos = (1, 0)
#lcd.write_string('Starting program')
lcd.crlf
sleep (5)
lcd.close(clear=True)
lcd.backlight_enabled = False