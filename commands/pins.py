#!/home/leinelab/ampel/ve_python

import RPi.GPIO as gpio

pin_red   = 18
pin_green = 16

gpio.cleanup()
gpio.setmode( gpio.BOARD )
gpio.setup( pin_red, gpio.OUT )
gpio.setup( pin_green, gpio.OUT )


def EnablePin( pin, enable ):
    if enable:
        gpio.output( pin, gpio.HIGH )
    else:
        gpio.output( pin, gpio.LOW )


def EnableRed( enable ):
    global pin_red
    EnablePin( pin_red, enable )


def EnableGreen( enable ):
    global pin_green
    EnablePin( pin_green, enable )
