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
# import RPi.GPIO as GPIO

BLYNK_AUTH_TOKEN = "Bm7q73fxUgn88ztlTApzlL1ReDDSK68j"

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH_TOKEN)

# Set up GPIO pins
led1_pin = 22
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
        print("LED1 On")
    else:
        # Turn off LED1
        print("LED1 Off")

# Register virtual pin handler for V1
@blynk.handle_event("write V1")
def v1_write_handler(pin, value):
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if value == 1:
        # Turn on LED2
        print("LED2 On")
    else:
        # Turn off LED2
        print("LED2 Off")


@blynk.handle_event("read V2")
def v2_read_handler(pin):
    print(READ_PRINT_MSG.format(pin))
    # blynk.virtual_write(pin, potvalue)
    blynk.virtual_write(pin, random.randint(0, 5000))
    

@blynk.handle_event("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    # You can also use blynk.sync_virtual(pin)

@blynk.handle_event("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')


while True:
    try: 
        potvalue += 1
        if potvalue > 4900:
            potvalue = 0
        print("pot = ", potvalue)
        # blynk.virtual_write(pot_virt_pin, potvalue)
        # time.sleep(1)

        blynk.run()
    except KeyboardInterrupt:
        # GPIO.cleanup()
        break
