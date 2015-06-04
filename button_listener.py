#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import os

fpid = os.fork()

if fpid != 0:
    #util.log( "Forked foreman script." )
    #util.log( "pid: " + str(fpid) )
    sys.exit(0) # stop parent process, child continues


# Pin festlegen
pin_button = 11
USE_GPIO = True
fifo = '/home/leinelab/ampel/fifo'
status_file = '/home/leinelab/ampel/commands/status'

GPIO.cleanup( )
GPIO.setmode( GPIO.BOARD )
GPIO.setup( pin_button, GPIO.IN )

def GetPin( pin ):
    if USE_GPIO:
        return GPIO.input( pin )
    else:
        return True

def GetStatus():
    with open(status_file) as f:
        return f.read()

def SendCommand(commandStr):
    with open(fifo, 'w') as f:
        f.write(commandStr + '\n')

try:
    while True:
        GPIO.wait_for_edge( pin_button, GPIO.RISING )
        if GetStatus() == 'Open':
            SendCommand('CloseLab')
        else:
            SendCommand('OpenLab')
        time.sleep(4)
except:
    pass
