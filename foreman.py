#!/home/leinelab/ampel/ve_python

import time
import subprocess
import requests
import sys
import os
import util
from threading import Thread, Event
import RPi.GPIO as gpio
import filesys

SPACEAPI_URL = 'https://leinelab.net/ampel/spaceapi.php?open=%s'

class Ampel(object):

    def __init__(self):
        self.pins = {
            "red": 12,
            "green": 16
        }

        gpio.cleanup()
        gpio.setmode( gpio.BOARD)

        for number in self.pins.values():
             gpio.setup( number, gpio.OUT )

    def set(self, pin, enable=True):
        if enable:
            gpio.output(self.pins[pin], gpio.HIGH)
        else:
            gpio.output(self.pins[pin], gpio.LOW)

if "fork" in sys.argv:
    fpid = os.fork()

    util.log_file = "ampel.log"

    if fpid != 0:
        util.log( "Forked foreman script." )
        util.log( "pid: " + str(fpid) )
        sys.exit(0) # stop parent process, child continues



# Tasks 

class BasicTask(Thread):
    
    def __init__(self, ampel):
        super().__init__()
        self.stop = Event()
        self.ampel = ampel

    def shutdown(self):
        self.stop.set()
        # wait until the Task has finished his work
        self.join()

class Opened(BasicTask):

    def run(self): 
        util.log('Opened')
        
        self.ampel.set('green', True)
        self.ampel.set('red', False)

        # open spaceapi
        requests.get(SPACEAPI_URL % '1')


class Blink(BasicTask):

    def run(self): 
        util.log('Started blinking')

        while not self.stop.is_set():
            self.ampel.set('red', True)
            self.ampel.set('green', True)
            time.sleep(1)
            self.ampel.set('red', False)
            self.ampel.set('green', False)
            time.sleep(1)


class Closed(BasicTask):

    def run(self):
        util.log('Closed')

        self.ampel.set('green', False)
        self.ampel.set('red', True)

        # close spaceapi
        requests.get(SPACEAPI_URL % '0')


def PollForCommand():
    global g_fifo
    #util.log( "Poll for command..." )
    try:
        content = g_fifo.read() # .decode() ?
    except KeyboardInterrupt:
        exit(0)
    except:
        util.log( "Couldn't decode command." )
        return ""

    # security feature 
    if content != "" and content[0] not in './~':
        return content.replace('\n', '')
    else:
        return ""


## MAIN ##

ampel = Ampel()

util.log( "Started. Wait for commands..." )

current_task = None
def change_task(new_task):
    global current_task
    if current_task is not None:
        current_task.shutdown()
    current_task = new_task(ampel)
    current_task.start()

change_task(Closed)

g_fifo_path = "/var/run/ampel.fifo"
if not os.path.exists( g_fifo_path ):
    os.mkfifo( g_fifo_path )
g_fifo = open( g_fifo_path, 'r' )

while True:
    command = PollForCommand()
   
    if command == "":
        continue
    
    util.log(command)
    
    if command == "OpenLab":
        if type(current_task) is not Opened:
            change_task(Opened)

    elif command == "CloseLab":
        if type(current_task) is not Closed:
            change_task(Closed)
    
    elif command == "BlinkLab":
        if type(current_task) is not Blink:
            change_task(Blink)
    
    elif command == "ButtonPressed":
        if type(current_task) is not Closed:
            change_task(Closed)
        else:
            change_task(Opened)
