import time
import RPi.GPIO as GPIO
import random 

MIN_GREEN_TIME_NS = 6  # Minimum green light time in seconds for North & South
TIME_PER_CAR = 60       # Additional green light time in seconds per car
MIN_GREEN_TIME_EW = 60  # Fixed green light time in seconds for East & West
ALL_RED_TRANSITION = 3  # All Red light duration for transitions

# Define LED pin configurations for grouped LEDs
GREEN_NS = 22
GREEN_EW = 25
YELLOW_NS = 27
YELLOW_EW = 24
RED_NS = 17
RED_EW = 23

ALL_LEDS = [GREEN_NS, GREEN_EW, YELLOW_NS, YELLOW_EW, RED_NS, RED_EW]

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in ALL_LEDS:
    GPIO.setup(pin, GPIO.OUT)

def turn_off_all_lights():
    for pin in ALL_LEDS:
        GPIO.output(pin, False)

def get_NS_car_count():
    return random.randint(0, 5)

def traffic_light_sequence():
    while True:
        car_count = get_NS_car_count()
        green_time_ns = MIN_GREEN_TIME_NS + car_count * TIME_PER_CAR
        
        # North & South Green, East & West Red
        turn_off_all_lights()
        GPIO.output(GREEN_NS, True)
        GPIO.output(RED_EW, True)
        print(f"North & South Green light for {green_time_ns} seconds.")
        time.sleep(green_time_ns)

        # North & South Yellow, East & West Red
        GPIO.output(GREEN_NS, False)
        GPIO.output(YELLOW_NS, True)
        print("North & South Yellow light for 10 seconds.")
        time.sleep(10)
        
        # All Red for transition
        GPIO.output(YELLOW_NS, False)
        GPIO.output(RED_NS, True)
        GPIO.output(RED_EW, True)
        print(f"All Red light for {ALL_RED_TRANSITION} seconds.")
        time.sleep(ALL_RED_TRANSITION)

        # East & West Green, North & South Red
        GPIO.output(RED_EW, False)
        GPIO.output(GREEN_EW, True)
        print(f"East & West Green light for {MIN_GREEN_TIME_EW} seconds.")
        time.sleep(MIN_GREEN_TIME_EW)

        # East & West Yellow, North & South Red
        GPIO.output(GREEN_EW, False)
        GPIO.output(YELLOW_EW, True)
        print("East & West Yellow light for 10 seconds.")
        time.sleep(10)

        # All Red for transition
        GPIO.output(YELLOW_EW, False)
        GPIO.output(RED_NS, True)
        GPIO.output(RED_EW, True)
        print(f"All Red light for {ALL_RED_TRANSITION} seconds.")
        time.sleep(ALL_RED_TRANSITION)

try:
    traffic_light_sequence()
except KeyboardInterrupt:
    turn_off_all_lights()
    GPIO.cleanup()
