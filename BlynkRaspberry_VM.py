# pip install blynk-library-python

import BlynkLib
import random
import time
# import RPi.GPIO as GPIO

# Initialize Blynk
blynk = BlynkLib.Blynk('jw1NZLXq38HoD_0YzrBQ2xcAIPY59nip')

# Set up GPIO pins
led1_pin = 17
led1_virt_pin = 0

led2_pin = 23
led2_virt_pin = 1

pot_pin = 34
pot_virt_pin = 2

term_virt_pin = 3

potvalue = 0

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)
# GPIO.setup(23, GPIO.OUT)

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(0)
def my_write_handler(value):
    print('Current V0 value: ')
    print(value)
    if value == ['1']:
        # Turn on LED1
        # GPIO.output(led1_pin, GPIO.HIGH)
        print("LED1 On")
    else:
        # Turn off LED1
        # GPIO.output(led1_pin, GPIO.LOW)
        print("LED1 Off")

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print('Current V1 value: ')
    print(value)
    if value == ['1']:
        # Turn on LED1
        # GPIO.output(led2_pin, GPIO.HIGH)
        print("LED2 On")
    else:
        # Turn off LED1
        # GPIO.output(led2_pin, GPIO.LOW)
        print("LED2 Off")

@blynk.VIRTUAL_READ(2)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(2, random.randint(0, 5000))

while True:
    try:
        potvalue += 1
        if potvalue > 4900:
            potvalue = 0
#         print("pot = ", potvalue)
        # blynk.virtual_write(pot_virt_pin, potvalue)
        blynk.run()
    except KeyboardInterrupt:
        # GPIO.cleanup()
        break