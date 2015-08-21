#!/home/leinelab/ampel/ve_python

import urllib.request

import time
import subprocess
import sys
import os
import util
from threading import Thread, Event
import RPi.GPIO as gpio
import filesys

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

        self.set('red')
        self.set('green', False)
        filesys.SaveStatus('Closed')

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


g_fifo_path = "/home/leinelab/ampel/fifo"
if not os.path.exists( g_fifo_path ):
    os.mkfifo( g_fifo_path )
g_fifo = open( g_fifo_path, 'r' )


# Tasks 

class BasicTask(Thread):
    
    def __init__(self, ampel):
        super().__init__()
        self.stop = Event()
        self.ampel = ampel

    def shutdown(self):
        self.stop.set()

class Glow(BasicTask):

    def run(self): 
        util.log('Started glowing')

        self.ampel.set('red', False)
        self.ampel.set('green', True)
        filesys.SaveStatus('Open')

        while not self.stop.is_set():
            time.sleep(1)

        self.ampel.set('red', True)
        self.ampel.set('green', False)
        filesys.SaveStatus('Closed')

        util.log('Shutting down now.')


class Blink(BasicTask):

    def run(self): 
        util.log('Started glowing')

        self.ampel.set('red', False)
        self.ampel.set('green', True)

        while not self.stop.is_set():
            self.ampel.set('red', True)
            self.ampel.set('green', True)
            time.sleep(1)
            self.ampel.set('red', False)
            self.ampel.set('green', False)
            time.sleep(1)

        self.ampel.set('red', True)

        util.log('Shutting down now.')


def PollForCommand():
    global g_fifo
    #util.log( "Poll for command..." )
    try:
        content = g_fifo.read() # .decode() ?
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

current_task = None
util.log( "Started. Wait for commands..." )

while True:
    command = PollForCommand()
   
    if command == "":
        continue
    
    print(command)
    
    if command == "OpenLab" and current_task is None:
        current_task = Glow(ampel)
        current_task.start()
        
    if command == "CloseLab" and current_task is not None:
        current_task.shutdown()
        current_task = None
	
