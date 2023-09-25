#define BLYNK_TEMPLATE_ID "TMPL6lRXOjBIZ"
#define BLYNK_TEMPLATE_NAME "RaspberryPi IoT"
#define BLYNK_DEVICE_NAME "RaspberryPi"

# install Blynk library on Raspberry Pi
# pip install blynklib-rpi -- upgrade

# may need these
# sudo apt-get update
# sudo apt-get install python-dev python-pip libssl-dev libffi-dev


import blynklib
import random
import time
# import RPi.GPIO as GPIO

# BLYNK_AUTH_TOKEN = "Bm7q73fxUgn88ztlTApzlL1ReDDSK68j"
BLYNK_AUTH_TOKEN = "jw1NZLXq38HoD_0YzrBQ2xcAIPY59nip"

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN)

# Set up GPIO pins
led1_pin = 17
led1_virt_pin = 0

led2_pin = 23
led2_virt_pin = 1

pot_pin = 34
pot_virt_pin = 2

term_virt_pin = 3

potvalue = 0

WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"

# Register virtual pin handler for V0
@blynk.handle_event("write V0")
def v0_write_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == 1:
        # Turn on LED1
        GPIO.output(led1_pin, GPIO.HIGH)
        print("LED1 On")
    else:
        # Turn off LED1
        GPIO.output(led1_pin, GPIO.LOW)
        print("LED1 Off")


# Register virtual pin handler for V1
@blynk.handle_event("write V1")
def v1_write_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == 1:
        # Turn on LED2
        GPIO.output(led2_pin, GPIO.HIGH)
        print("LED2 On")
    else:
        # Turn off LED2
        GPIO.output(led2_pin, GPIO.LOW)
        print("LED2 Off")


@blynk.handle_event("read V2")
def v2_read_handler(pin):
    print(READ_PRINT_MSG.format(pin))
    # blynk.virtual_write(pin, potvalue)
    blynk.virtual_write(pin, random.randint(0, 5000))
    

CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'


@blynk.handle_event("connect")
def connect_handler():
    print(CONNECT_PRINT_MSG)
    print('Sleeping 2 sec in connect handler...')
    time.sleep(2)
    # blynk.disconnect()


@blynk.handle_event("disconnect")
def disconnect_handler():
    print(DISCONNECT_PRINT_MSG)
    print('Sleeping 4 sec in disconnect handler...')
    time.sleep(4)


while True:
    try: 
#         potvalue += 1
#         if potvalue > 4900:
#             potvalue = 0
#         print("pot = ", potvalue)
        # blynk.virtual_write(pot_virt_pin, potvalue)
        # time.sleep(1)

        blynk.run()
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
