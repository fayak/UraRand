#!/usr/bin/env python3

import sys
import signal
import time
import smbus
import RPi.GPIO as GPIO

I2C_ADDR = 0x19
GPIO_PIN = 7

loop = True

def _init_counter(callback):
    print("Init")

    bus = smbus.SMBus(1)
    bus.write_byte(I2C_ADDR, 0x71)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_PIN, GPIO.IN)

    GPIO.add_event_detect(GPIO_PIN, GPIO.FALLING)
    GPIO.add_event_callback(GPIO_PIN, callback)

def _stop_counter():
    print("Stop")

    bus = smbus.SMBus(1)
    bus.write_byte(I2C_ADDR, 0)

def _signal_handler(sig, frame):
    global loop
    loop = False

def collect(callback):
    global loop
    _init_counter(callback)

    signal.signal(signal.SIGINT, _signal_handler)
    loop = True
    while loop:
        time.sleep(0.1)
    _stop_counter()
