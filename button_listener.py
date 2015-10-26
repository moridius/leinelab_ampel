#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import os
import sys
import util

debug = False
if 'debug' in sys.argv:
    debug = True

# Pin festlegen
pin_button = 11
USE_GPIO = True

GPIO.cleanup( )
GPIO.setmode( GPIO.BOARD )
GPIO.setup( pin_button, GPIO.IN )

def GetPin( pin ):
    if USE_GPIO:
        return GPIO.input( pin )
    else:
        return True

def SendCommand(commandStr):
    with util.open_fifo('w') as f:
        f.write(commandStr + '\n')

while True:
    GPIO.wait_for_edge( pin_button, GPIO.FALLING )
    if debug:
        print('ButtonPressed')
    SendCommand('ButtonPressed')
