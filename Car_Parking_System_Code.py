# GPIO and Associated Peripherals: -
# import board # Implements a general-purpose board structure which has the functionality needed for a range of purposes
import RPi.GPIO as GPIO # Module to control the GPIO on a Raspberry Pi
from RPLCD.gpio import CharLCD # A Raspberry Pi LCD library

# Pi Camera Interfacing: -
# import picamera # Provides a pure Python interface to the Raspberry Pi camera module
# picam = picamera.PiCamera()

from PIL import Image # Provides a class with the same name which is used to represent a PIL image
import pytesseract # A python wrapper for Google's Tesseract-OCR (Optical Character Recognition)
import random # Implements pseudo-random number generators for various distributions

# import time # Provides various time-related functions
from time import sleep # Suspends execution of the current thread for a given number of seconds

# Import library and create an instance of REST client:-
from Adafruit_IO import Client
# from Adafruit_IO import Feed
ADAFRUIT_IO_USERNAME = 'XXXXXXXXXX' # Username
ADAFRUIT_IO_KEY = '.....XXXXXXXXXX.....' # Active Key

# 'XXXXX' is IO Feed created in Adafruit: -
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
cars_feed = aio.feeds('XXXXX') 
details_feed = aio.feeds('XXXXX')

sensor1 = 6 # Pin to be connected to the IR sensor 1
sensor2 = 26 # Pin to be connected to the IR sensor 2
motor_pin = 5 # Pin to be connected to the motor

GPIO.setwarnings(False) # Disable warnings
GPIO.setup(sensor1, GPIO.IN) # Selected pin is configured as input
GPIO.setup(sensor2, GPIO.IN) # Selected pin is configured as input

# Direction Control of Servo Motor using Pulse Width Modulation (PWM): -
GPIO.setup(motor_pin, GPIO.OUT) # Selected pin is configured as output
servo = GPIO.PWM(motor_pin, 50) # Pin number, frequency in Hz
servo.start(0) # Start PWM signal generation with 0% duty cycle

# LCD Interfacing: -
lcd = CharLCD(pin_rs=22, pin_rw=24, pin_e=23, pins_data=[9,25,11,8], numbering_mode=GPIO.BCM, cols=16, rows=2, dotsize=8)
lcd.clear() # Clear the LCD
lcd.backlight = True # Turn backlight ON

# Necessary Variable Initializations: -
slots= [1,2,3,4,5,6,7,8,9,10]
alnum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
count = 10; flag1 = flag2 = False; data = {}

while True:
   
    if (GPIO.input(sensor1) == False and flag2 == False and count > 0):
        print("Sensor 1 Detected (1)")
        flag1 = True
        sleep(0.5)
       
    if flag1 == True:
        servo.ChangeDutyCycle(7.5) # 90-degree turn
        
        # Capture Number Plate Image using Pi Camera: -
#         picam.rotation = 180 # Retrieves or sets the current rotation of the camera’s image
#         picam.start_preview(alpha = 200) # Retrieves or sets the opacity of the renderer
#         time.sleep(5) # Suspends execution for the given number of seconds

#         picam.capture("Number_Plate_Image.png") # Capture an image from the camera, storing it in the output
#         picam.stop_preview() # Hides the preview overlay
#         picam.close() # Finalizes the state of the camera
              
        if (GPIO.input(sensor2) == False):
           
            lcd.clear()
            print("Sensor 2 Detected (2)")
            flag1 = False
            count = count - 1
            
            img = Image.open("Sample_Number_Plate.jpg") # Opens and identifies the given image file  
            result = pytesseract.image_to_string(img) # Returns unmodified output as string from Tesseract OCR processing
            
            # Print only necessary characters from the number plate: -
            number_plate = []
            for i in result:
                if i in alnum:
                    print(i, end='')
                    number_plate.append(i) # Place new items in the available space
            
            str_number_plate = ''.join([str(elem) for elem in number_plate]) # List comprehension           
            slot_num = random.choice(slots) # Return a random element from the non-empty sequence
            print_slot_num = "Slot Number: " + str(slot_num)
            
            # Send feed to Adafruit IO: -
            aio.send(details_feed.key, str(str_number_plate) + "\n" + print_slot_num)
            aio.send(cars_feed.key, str(10-count))
            
            # Data Logging for Car IN: -
            with open('abc.txt', mode ='w') as file:    
                     file.write(str_number_plate)
                     # print(result)
           
            # Write the specified Unicode string to the display: -
            print("\nNumber of Slot(s) Available: ", count)
            lcd.write_string("Available Slots: " + str(count))
            sleep(3); lcd.clear()
            lcd.write_string("Slot Number: " + str(slot_num))
            
            print("Car has been parked!")
            slots.remove(slot_num) # Removes the first occurrence of the element with the specified value
            data[slot_num] = result
            servo.ChangeDutyCycle(10) # Neutral
            sleep(0.5)
             
    if (GPIO.input(sensor2) == False and flag1 == False and count<=10):
        print("Sensor 2 Detected (3)")
        flag2 = True
        sleep(0.5)
       
    if flag2 == True:        
        servo.ChangeDutyCycle(7.5) # 90-degree turn
       
        # Capture Number Plate Image using Pi Camera: -
#         picam.rotation = 180 # Retrieves or sets the current rotation of the camera’s image
#         picam.start_preview(alpha = 200) # Retrieves or sets the opacity of the renderer
#         time.sleep(5) # Suspends execution for the given number of seconds

#         picam.capture("Number_Plate_Image.png") # Capture an image from the camera, storing it in the output
#         picam.stop_preview() # Hides the preview overlay
#         picam.close() # Finalizes the state of the camera
       
        img = Image.open("Sample_Number_Plate.jpg") # Opens and identifies the given image file  
        result = pytesseract.image_to_string(img) # Returns unmodified output as string from Tesseract OCR processing
       
        if (GPIO.input(sensor1) == False):
           
            lcd.clear()
            print("\nSensor 1 Detected (4)")
            flag2 = False
            count = count + 1
            
            # Print only necessary characters from the number plate: -
            number_plate = []
            for i in result:
                if i in alnum:
                    print(i, end='')
                    number_plate.append(i) # Place new items in the available space
            str_number_plate = ''.join([str(elem) for elem in number_plate]) # List comprehension
            
            # Data Logging for Car OUT: -
            with open('abc.txt', mode ='w') as file:    
                     file.write(str_number_plate)
                     # print(result)
           
            aio.send(cars_feed.key, str(10-count)) # Send feed to Adafruit IO
            print("\nNumber of Slot(s) Available: " + str(count) +"\nBYE....")
            lcd.write_string("Visit Us Again!"); sleep(3); lcd.clear()
            lcd.write_string("Available Slots: " + str(count)) # Write the specified Unicode string to the display
            
            print("Car has left the parking area!")
            slots.append(slot_num) # Place new items in the available space
            data.pop(slot_num) # Removes the last value from the list           
            servo.ChangeDutyCycle(10) # Neutral
            sleep(0.5)
