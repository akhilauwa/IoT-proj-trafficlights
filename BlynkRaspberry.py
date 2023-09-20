#define BLYNK_TEMPLATE_ID "TMPL6lRXOjBIZ"
#define BLYNK_TEMPLATE_NAME "RaspberryPi IoT"
#define BLYNK_DEVICE_NAME "RaspberryPi"

# install Blynk library on Raspberry Pi
# pip install blynklib-rpi -- upgrade

# may need these
# sudo apt-get update
# sudo apt-get install python-dev python-pip libssl-dev libffi-dev


import BlynkLib
import time
import RPi.GPIO as GPIO

BLYNK_AUTH_TOKEN = "Bm7q73fxUgn88ztlTApzlL1ReDDSK68j"

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Set up GPIO pins
led1_pin = 22
led1_virt_pin = 0

led2_pin = 23
led2_virt_pin = 1

pot_pin = 34
pot_virt_pin = 2

term_virt_pin = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(pot_pin, GPIO.IN)

# TODO FIX PIN NAMES
# Register virtual pin handler for V0
@blynk.on("writeV0")
def v0_write_handler(pin, value):
    if int(value[0]) == 1:
        # Turn on LED1
        GPIO.output(22, GPIO.HIGH)
    else:
        # Turn off LED1
        GPIO.output(22, GPIO.LOW)

# Register virtual pin handler for V1
@blynk.on("writeV1")
def v1_write_handler(pin, value):
    if int(value[0]) == 1:
        # Turn on LED2
        GPIO.output(23, GPIO.HIGH)
    else:
        # Turn off LED2
        GPIO.output(23, GPIO.LOW)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    # You can also use blynk.sync_virtual(pin)

@blynk.on("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')

while True:
    try:
        potvalue = GPIO.input(pot_pin)
        print("pot =", potvalue)
        blynk.virtual_write(pot_virt_pin, potvalue)

        terminalStr = "pot = {}".format(potvalue)
        print(terminalStr)
        blynk.virtual_write(term_virt_pin, terminalStr)

        time.sleep(1)

        blynk.run()
    except KeyboardInterrupt:
        GPIO.cleanup()
        break
