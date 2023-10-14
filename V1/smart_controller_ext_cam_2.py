'''
Runs on Raspberry Pi
Communications (Blynk, socket) written by: Akhila Liyanage
Traffic lights logic written by Chen Shen and Shijun Shao
'''

import threading
import BlynkLib
import random
import RPi.GPIO as GPIO
import time
import socket

# Define the server's host and port
host = "192.168.35.111"  # Use the server's IP address or "localhost" for local testing
port = 9000  # Use the same port number as the server

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

MIN_GREEN_TIME_NS = 10  # Minimum green light time in seconds for North & South
TIME_PER_CAR = 3       # Additional green light time in seconds per car
MIN_GREEN_TIME_EW = 6  # Fixed green light time in seconds for East & West
ALL_RED_TRANSITION = 3  # All Red light duration for transitions

ALL_LEDS = [GREEN_NS, GREEN_EW, YELLOW_NS, YELLOW_EW, RED_NS, RED_EW]

cars_virt_pin = 2
send_interval = 3
term_virt_pin = 3

emergency_activated = False

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)
# GPIO.setup(23, GPIO.OUT)
# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
for pin in ALL_LEDS:
    GPIO.setup(pin, GPIO.OUT)

# Add a global flag to signal program termination
terminate_program = False

# Emergency Vehicle Override
@blynk.ON('V0')
def v0_write_handler(value):
    global emergency_activated
    if value == ['1']:
        # TODO change traffic_light_sequence to read emergency flag
        emergency_activated = True
        blynk.virtual_write(term_virt_pin, 'Emergency Vehicle Override Activated.\n')
        print('Emergency Vehicle Override Activated.')
    else:
        # TODO change traffic_light_sequence to read emergency flag
        emergency_activated = False
        blynk.virtual_write(term_virt_pin, 'Emergency Vehicle Override Deactivated.\n')
        print('Emergency Vehicle Override Deactivated.')
        print('Resuming Normal Sequence.')

# Get car count using YOLO
def get_NS_car_count(duration=20):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))

        # Send duration of count to server
        client_socket.send(str(duration).encode("utf-8"))

        # Receive car count from the server
        response = client_socket.recv(1024)  # Receive up to 1024 bytes
        car_count = int(response.decode('utf-8'))
        print(f"Car count: {car_count}.")

        print("Closing client socket...")
        client_socket.close()
        print("Client socket closed.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt registered.")
        print("Closing client socket...")
        client_socket.close()
        print("Client socket closed.")

    return car_count
# Helper function to change light state
def change_light_state(NS_green, NS_yellow, NS_red, EW_green, EW_yellow, EW_red):
    GPIO.output(GREEN_NS, NS_green)
    GPIO.output(YELLOW_NS, NS_yellow)
    GPIO.output(RED_NS, NS_red)
    GPIO.output(GREEN_EW, EW_green)
    GPIO.output(YELLOW_EW, EW_yellow)
    GPIO.output(RED_EW, EW_red)

# Send car count to Blynk
def send_NS_car_count(car_count):
    try:
        blynk.virtual_write(cars_virt_pin, car_count)
    except socket.error as e:
        print(f"Socket error: {e}")


# Turn off all LEDs
def turn_off_all_lights():
    for pin in ALL_LEDS:
        GPIO.output(pin, False)

# Safe sleep to check for emergency override
def safe_sleep(seconds):
    end_time = time.time() + seconds
    try:
        while time.time() < end_time:
            if emergency_activated:
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt registered.")
        print("Exiting sleep.")

# Traffic light logic (main)       
def traffic_light_logic():
    global emergency_activated, terminate_program  # <-- Add terminate_program here
    
    emergency_msg = True
    car_count = 0
    
    try:
        while not terminate_program:  # <-- Check the flag here
            if not emergency_activated:
                print("----------- Start of Sequence ----------- \n")
                emergency_msg = True
                green_time_ns = MIN_GREEN_TIME_NS + car_count * TIME_PER_CAR
                
                # North & South Green, East & West Red
                turn_off_all_lights()
                change_light_state(True, False, False, False, False, True)
                print(f"North & South Green light for {green_time_ns} seconds.")

                # NOTE calling get_NS_car_count(duration) here will cause the program to wait for the car count to finish
                car_count = get_NS_car_count(green_time_ns)
                send_NS_car_count(car_count)
                # time.sleep(green_time_ns)
                # safe_sleep(green_time_ns)

                # North & South Yellow, East & West Red
                change_light_state(False, True, False, False, False, True)
                print("North & South Yellow light for 10 seconds.")
                # time.sleep(10)
                safe_sleep(10)
                
                # All Red for transition
                change_light_state(False, False, True, False, False, True)
                print(f"All Red light for {ALL_RED_TRANSITION} seconds.")
                # time.sleep(ALL_RED_TRANSITION)
                safe_sleep(ALL_RED_TRANSITION)

                # East & West Green, North & South Red
                change_light_state(False, False, True, True, False, False)
                print(f"East & West Green light for {MIN_GREEN_TIME_EW} seconds.")
                # time.sleep(MIN_GREEN_TIME_EW)
                safe_sleep(MIN_GREEN_TIME_EW)

                # East & West Yellow, North & South Red
                change_light_state(False, False, True, False, True, False)
                print("East & West Yellow light for 10 seconds.")
                # time.sleep(10)
                safe_sleep(10)

                # All Red for transition
                change_light_state(False, False, True, False, False, True)
                print(f"All Red light for {ALL_RED_TRANSITION} seconds.")
                # time.sleep(ALL_RED_TRANSITION)
                safe_sleep(ALL_RED_TRANSITION)
            else:
                change_light_state(True, False, False, False, False, True)
                if emergency_msg:
                    print("Emergency activated.")
                    emergency_msg = False
    except KeyboardInterrupt:
        pass
    
    print("Exiting traffic_light_logic...")
    GPIO.cleanup()
                

# Run traffic_light_logic in the background
traffic_thread = threading.Thread(target=traffic_light_logic)
traffic_thread.start()
    
# Main loop
try:
    while not terminate_program:  # <-- Check the flag here
        blynk.run()
except KeyboardInterrupt:
    print("KeyboardInterrupt registered in main loop.")
    terminate_program = True  # Set the flag to signal all loops/threads to terminate
    traffic_thread.join()  # Wait for the traffic_light_logic thread to finish
finally:
    # Call GPIO.cleanup()
    GPIO.cleanup()

print("Program terminated gracefully.")