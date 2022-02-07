#Import the libraries for working with GPIO and time
import RPi.GPIO as GPIO
import time

#set GPIO mode to BCM.
GPIO.setmode(GPIO.BCM)

#create constants to refer to GPIO ports by meaningful names
LEDPinRED = 22
LEDPinGREEN = 5
button = 18

#setup GPIO for input or output
GPIO.setup(LEDPinRED, GPIO.OUT)   # Red LED
GPIO.setup(LEDPinGREEN, GPIO.OUT)   # Green LED
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button with the initial state HIGH

# Set LED's to off and button to LOW and initial state to 0
GPIO.output(LEDPinRED,False)
GPIO.output(LEDPinGREEN,False)
state = 0

try:
    print ("Push the red button to switch the light mode. To exit press CTRL-C on your keyboard")
    
    #The while loop to detect button press and switch the LED state in sequential order
    while True:
        if GPIO.input (button) == GPIO.LOW:
            if state==0:
                GPIO.output(LEDPinRED,False)
                GPIO.output(LEDPinGREEN,True)
                print ("The light is now green")
                state=1
                time.sleep(0.2)
                
            elif state==1:
                GPIO.output(LEDPinRED,True)
                GPIO.output(LEDPinGREEN,False)
                print ("The light is now red")
                state=2
                time.sleep(0.2)
                
            elif state==2:
                GPIO.output(LEDPinRED,False)
                GPIO.output(LEDPinGREEN,False)
                print ("The light off. Program still running. To exit press CTRL-C on your keyboard.")
                state=0
                time.sleep(0.2)

        #time.sleep(0.1)

finally:
    print ("You pressed CTRL-C. Exiting.")
    GPIO.cleanup()


