import RPi.GPIO as GPIO
from time import sleep
from rpi_lcd import LCD

GPIO.setmode(GPIO.BCM)

lcd = LCD ()
blinkCount = 3
count = 0
LEDPinRED = 22
LEDPinBLUE = 19
LEDPinGREEN = 5
BUZZERPin = 17


GPIO.setup(LEDPinRED, GPIO.OUT)
GPIO.setup(LEDPinBLUE, GPIO.OUT)
GPIO.setup(LEDPinGREEN, GPIO.OUT)
GPIO.setup(BUZZERPin, GPIO.OUT)


try:
    while count < blinkCount:
        GPIO.output(LEDPinRED , True)
        print ("RED LED ON")
        lcd.text('RED LED ON"', 1)
        sleep(3)
        GPIO.output(LEDPinRED , False)
        print ("RED LED OFF")
        lcd.text('RED LED OFF', 1)
        GPIO.output(BUZZERPin,1)
        sleep(1)
        GPIO.output(BUZZERPin,0)
        GPIO.output(LEDPinBLUE, True)
        print ("BLUE LED ON")
        lcd.text('BLUE LED ON', 1)
        sleep(3)
        GPIO.output(LEDPinBLUE, False)
        print ("BLUE LED OFF")
        lcd.text('BLUE LED OFF', 1)
        GPIO.output(BUZZERPin,1)
        sleep(1)
        GPIO.output(BUZZERPin,0)
        GPIO.output(LEDPinGREEN, True)
        print ("GREEN LED ON")
        lcd.text('GREEN LED ON', 1)
        sleep(3)
        GPIO.output(LEDPinGREEN, False)
        print ("GREEN LED OFF")
        lcd.text('GREEN LED OFF', 1)
        GPIO.output(BUZZERPin,1)
        sleep(1)
        GPIO.output(BUZZERPin,0)
        count += 1
    print ("Done!")
finally:
    GPIO.cleanup()
    sleep (3)
    lcd.clear()