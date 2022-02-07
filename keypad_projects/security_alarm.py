#Import libraries
import RPi.GPIO as GPIO
import time
import Keypad #import freenove library modified to use BCM GPIO.
from RPLCD import i2c #import LCD library

#set gpio mode to BCM
GPIO.setmode(GPIO.BCM)

#configure keypad
ROWS = 4        # number of rows of the Keypad
COLS = 4        #number of columns of the Keypad
keys =  [   '1','2','3','A',    #key layout
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D'     ]

rowsPins = [6,13,23,24]        #connect to the row pinouts of the keypad
colsPins = [25,16,20,21]        #connect to the column pinouts of the keypad

keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS)    #create Keypad object
keypad.setDebounceTime(50)      #set the debounce time 

#configure button and buzzer
button = 18
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button with the initial state HIGH
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

#intialize buzzer and set to off
GPIO.setup(BUZZERPin, GPIO.OUT)
GPIO.output(BUZZERPin,0)

#variables for alarm
passlen = 4
password = "1234"
timeout = 10


def writelcd (message):
    lcd.close(clear=True)
    lcd.write_string(message)
    time.sleep (0.5)
    
def blinklcd (message):
    t_end = time.time() + 5
    while time.time() < t_end:
        lcd.close(clear=True)
        time.sleep(.5)
        lcd.write_string(message)
        GPIO.output(BUZZERPin,1)
        time.sleep(.5)
        GPIO.output(BUZZERPin,0)
    
#Check passcode function
def passcheck():
    #import global variables
    global passlen
    global password
    global timeout
    #intialize passcode variable
    temp = ''
    #prompt for passcode
    timermesssage="{} seconds to enter passcode!".format(timeout)
    print (timermesssage)
    writelcd(timermesssage)
    time.sleep(3)
    #start the timer loop
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        print ("Enter passcode")
        writelcd("Enter passcode")
        while len(temp) <= (passlen - 1) and not time.time() > timeout_start + timeout:
            key = keypad.getKey()       #obtain the state of keys
            if(key != keypad.NULL):     #if there is key pressed, print its key code.
                print ("You Pressed Key:", key)
                temp += (key)
                print (temp)
                writelcd(temp)

        if (temp == password):
            print ("Correct!")
            writelcd("Correct!")
            temp = ''
            time.sleep (3)
            print ("arming the alarm")
            writelcd("arming the alarm")
            time.sleep (3)
            main()
                        
        elif (temp != password):
            print ("Wrong")
            writelcd("Wrong")
            temp = ''
    boom()

#timeout function
def boom():
    print ("Police has been alerted!")
    blinklcd("Police Alerted!")
    time.sleep(3)
    main()
    exit()

#main function
def main ():
    global button
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button with the initial state HIGH
    lcd.backlight_enabled = True
    print ("Dont press the button!")
    writelcd("Dont press the button!")
    while True:
        if GPIO.input (button) == GPIO.LOW:
            writelcd("You pressed the button!")
            print ("You pressed the button!")
            time.sleep(3)
            passcheck()
try:
    main()

finally:
    GPIO.cleanup()
    print("\nApplication stopped! Disarmed!")
    writelcd("Disarmed!")
    time.sleep(3)
    lcd.close(clear=True)
    lcd.backlight_enabled = False

 