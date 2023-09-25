# pip install blynk-library-python

import BlynkLib
from BlynkTimer import BlynkTimer
import random
# import RPi.GPIO as GPIO

# Initialize Blynk
blynk = BlynkLib.Blynk('jw1NZLXq38HoD_0YzrBQ2xcAIPY59nip')

# Set up GPIO pins
# Define LED pin configurations for grouped LEDs
GREEN_NS = 22
GREEN_EW = 25
YELLOW_NS = 27
YELLOW_EW = 24
RED_NS = 17
RED_EW = 23

ALL_LEDS = [GREEN_NS, GREEN_EW, YELLOW_NS, YELLOW_EW, RED_NS, RED_EW]

cars_count = 0
cars_virt_pin = 2
send_interval = 3

term_virt_pin = 3

emergency_activated = False

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)
# GPIO.setup(23, GPIO.OUT)

# Emergency Vehicle Override
@blynk.ON('V0')
def v0_write_handler(value):
    if value == ['1']:
        # TODO change traffic_light_sequence to read emergency flag
        emergency_activated = True
        blynk.virtual_write(term_virt_pin, 'Emergency Vehicle Override Activated\n')
        print('Emergency Vehicle Override Activated')
    else:
        # TODO change traffic_light_sequence to read emergency flag
        emergency_activated = False
        blynk.virtual_write(term_virt_pin, 'Emergency Vehicle Override Deactivated\n')
        print('Emergency Vehicle Override Deactivated')
        print('Resuming Normal Sequence')

# TODO remove:
# @blynk.VIRTUAL_READ(2)
# def v2_read_handler(potvalue):
#     blynk.virtual_write(pot_virt_pin, potvalue)

# Terminal - execute the python command and echo it back
@blynk.ON('V3')
def v3_write_handler(value):
    value = value[0]
    blynk.virtual_write(term_virt_pin, 'Command: ' + value + '\n')
    try:
        result = str(eval(value))
        blynk.virtual_write(term_virt_pin, 'Result:\n  ')
        blynk.virtual_write(term_virt_pin, result)
        print('Result:', result)
    except Exception as e:
        blynk.virtual_write(term_virt_pin, 'Exception:\n  ' + repr(e))
        print('Exception:\n  ' + repr(e))
    finally:
        blynk.virtual_write(term_virt_pin, '\n')

# Get car count using YOLO
def get_NS_car_count():
    return random.randint(0, 100)

# Send car count to Blynk
def send_NS_car_count():
    cars_count = get_NS_car_count()
    blynk.virtual_write(cars_virt_pin, cars_count)

# Create BlynkTimer Instance
timer = BlynkTimer()

# Add Timers
timer.set_interval(send_interval, send_NS_car_count)

while True:
    try:
        blynk.run()
        timer.run()
    except KeyboardInterrupt:
        # GPIO.cleanup()
        break