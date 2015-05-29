#!/home/leinelab/ampel/ve_python

import RPi.GPIO as GPIO

# Pin festlegen
pin_button = 11

GPIO.cleanup( )
GPIO.setmode( GPIO.BOARD )
GPIO.setup( pin_button, GPIO.IN )

# LeineLab-Status
leine_lab_opened = False

def GetPin( pin ):
    if USE_GPIO:
        return GPIO.input( pin )
    else:
        return True

def WaitAndBlink():
    global pin_a
    global pin_b
    global pin_button
    SetPin( pin_a, 0 )
    for i in range(3):
        SetPin( pin_b, 1 )
        time.sleep( 0.5 )
        SetPin( pin_b, 0 )
        time.sleep( 0.5 )
        if not GetPin( pin_button ):
            SetPin( pin_a, 1 )
            return False
    SetPin( pin_b, 1 )
    pin_a, pin_b = pin_b, pin_a # swap pins
    return True

def DoSomething():
    global leine_lab_opened
    global red_out_timer
    leine_lab_opened = not leine_lab_opened
    TriggerAPI( leine_lab_opened )
    SendTweet( leine_lab_opened )
    if leine_lab_opened:
        print( "Stop timer." )
        try:
            red_out_timer.cancel()
        except:
            pass
    else:
        print( "Start timer." )
        red_out_timer = threading.Timer( 1800, DisableRed )
        red_out_timer.start()


## MAIN ##
try:
    while True:
        GPIO.wait_for_edge( pin_button, GPIO.RISING ) # wait for button pressed
        if WaitAndBlink():
            DoSomething()
            time.sleep( 2 )
except KeyboardInterrupt:
    pass
