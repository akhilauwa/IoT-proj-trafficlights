'''
Runs on Raspberry Pi
APP is Written by: Akhila Liyanage
Traffic lights is written by Chen Shen and Shijun Shao
'''


# pip install blynk-library-python
import threading
import BlynkLib
import random
# import RPi.GPIO as GPIO
import time

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

MIN_GREEN_TIME_NS = 3  # Minimum green light time in seconds for North & South
TIME_PER_CAR = 1       # Additional green light time in seconds per car
MIN_GREEN_TIME_EW = 3  # Fixed green light time in seconds for East & West
ALL_RED_TRANSITION = 3  # All Red light duration for transitions
YELLOW_TIME = 1

ALL_LEDS = [GREEN_NS, GREEN_EW, YELLOW_NS, YELLOW_EW, RED_NS, RED_EW]

cars_count = 0
cars_virt_pin = 2
send_interval = 10

term_virt_pin = 3

emergency_activated = False

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)
# GPIO.setup(23, GPIO.OUT)
# Setup GPIO pins
# GPIO.setmode(GPIO.BCM)
# for pin in ALL_LEDS:
#     GPIO.setup(pin, GPIO.OUT)

# Emergency Vehicle Override
@blynk.ON('V0')
def v0_write_handler(value):
    global emergency_activated
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
    return random.randint(0, 3)

# Send car count to Blynk
def send_NS_car_count():
    cars_count = get_NS_car_count()
    blynk.virtual_write(cars_virt_pin, cars_count)
    # set a new timer
    threading.Timer(send_interval, send_NS_car_count).start()

# Create BlynkTimer Instance
# timer = blynk.timer()

# Add Timers
# timer.set_interval(send_interval, send_NS_car_count)
def turn_off_all_lights():
    for pin in ALL_LEDS:
        pass
        # GPIO.output(pin, False)

def safe_sleep(seconds):
    end_time = time.time() + seconds
    while time.time() < end_time:
        if emergency_activated:
            break
        time.sleep(0.1)
        
def traffic_light_logic():
    global emergency_activated
    emergency_msg = True

    while True:
        if not emergency_activated:
            emergency_msg = True
            car_count = get_NS_car_count()
            green_time_ns = MIN_GREEN_TIME_NS + car_count * TIME_PER_CAR
            
            # North & South Green, East & West Red
            turn_off_all_lights()
            # GPIO.output(GREEN_NS, True)
            # GPIO.output(RED_EW, True)
            print(f"North & South Green light for {green_time_ns} seconds.")
            # time.sleep(green_time_ns)
            safe_sleep(green_time_ns)

            # North & South Yellow, East & West Red
            # GPIO.output(GREEN_NS, False)
            # GPIO.output(YELLOW_NS, True)
            print("North & South Yellow light for 10 seconds.")
            # time.sleep(10)
            safe_sleep(YELLOW_TIME)
            
            # All Red for transition
            # GPIO.output(YELLOW_NS, False)
            # GPIO.output(RED_NS, True)
            # GPIO.output(RED_EW, True)
            print(f"All Red light for {ALL_RED_TRANSITION} seconds.")
            # time.sleep(ALL_RED_TRANSITION)
            safe_sleep(ALL_RED_TRANSITION)

            # East & West Green, North & South Red
            # GPIO.output(RED_EW, False)
            # GPIO.output(GREEN_EW, True)
            print(f"East & West Green light for {MIN_GREEN_TIME_EW} seconds.")
            # time.sleep(MIN_GREEN_TIME_EW)
            safe_sleep(MIN_GREEN_TIME_EW)

            # East & West Yellow, North & South Red
            # GPIO.output(GREEN_EW, False)
            # GPIO.output(YELLOW_EW, True)
            print("East & West Yellow light for 10 seconds.")
            # time.sleep(10)
            safe_sleep(YELLOW_TIME)

            # All Red for transition
            # GPIO.output(YELLOW_EW, False)
            # GPIO.output(RED_NS, True)
            # GPIO.output(RED_EW, True)
            print(f"All Red light for {ALL_RED_TRANSITION} seconds.")
            # time.sleep(ALL_RED_TRANSITION)
            safe_sleep(ALL_RED_TRANSITION)
        else:
            # GPIO.output(GREEN_NS, True)
            # GPIO.output(RED_EW, True)
            # GPIO.output(GREEN_EW, False)
            # GPIO.output(RED_NS, False)
            if emergency_msg:
                print(f"Emergency.") # Just in case
                emergency_msg = False
            
# start the timer
send_NS_car_count()

# Create threads to modify our code sequence
traffic_thread = threading.Thread(target=traffic_light_logic)
traffic_thread.start()
    
# Main loop
while True:
    try:
        blynk.run()
    except KeyboardInterrupt:
        traffic_thread.join()
        # GPIO.cleanup()
