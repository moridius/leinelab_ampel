#!/usr/bin/python3

import RPi.GPIO as gpio
import time
import os
import sys
import foreman
import logging

# Pin festlegen
pin_button = 11

if __name__ == '__main__':
    gpio.cleanup()
    gpio.setmode(gpio.BOARD)
    gpio.setup(pin_button, gpio.IN)

    while True:
        gpio.wait_for_edge( pin_button, gpio.FALLING )
        logging.info('ButtonPressed')
        foreman.notify('ButtonPressed')
