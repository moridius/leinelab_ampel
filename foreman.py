#!/usr/bin/python3

import time
import subprocess
import sys
import os
import util
import socket
from threading import Thread, Event
import RPi.GPIO as gpio

class Ampel(object):

    def __init__(self, dry = False):
        self.dry = dry
        self.pins = {
            "red": 12,
            "green": 16
        }

        if self.dry:
            # no more setup needed
            return
        
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)

        for number in self.pins.values():
            gpio.setup( number, gpio.OUT )

    def set(self, pin, enable=True):
        if self.dry:
            print(pin, enable)
            return
        
        if enable:
            gpio.output(self.pins[pin], gpio.HIGH)
        else:
            gpio.output(self.pins[pin], gpio.LOW)


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
    name = 'OpenLab'
    
    def run(self): 
        util.log('Opened')
        
        self.ampel.set('green', True)
        self.ampel.set('red', False)


class Blink(BasicTask):
    name = 'BlinkLab'

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
    name = 'CloseLab'

    def run(self):
        util.log('Closed')

        self.ampel.set('green', False)
        self.ampel.set('red', True)


class Foreman(object):

    def __init__(self, path, dry=False):
        self.path = path
        self.sock = socket.socket(socket.AF_UNIX,
                                  socket.SOCK_STREAM)
        self.sock.bind(path)

        self.ampel = Ampel(dry)
        self.current_task = None

        self.change_task(Closed)

    def __del__(self):
        self.sock.close()

        # delete unix socket if it still exists
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass
        
    def loop(self):
        self.sock.listen(1)
        while True:
            conn, peer_addr = self.sock.accept()
            try:
                req = conn.recv(1024)
                if type(req) is bytes:
                    req = req.decode()
                    res = self.handle_command(req) or ''
                    res = res.encode()
                    conn.send(res)
            finally:
                conn.close()

    def handle_command(self, command):
        if command == "OpenLab":
            if type(self.current_task) is not Opened:
                self.change_task(Opened)
                return 'ok'

        elif command == "CloseLab":
            if type(self.current_task) is not Closed:
                self.change_task(Closed)
                return 'ok'
            
        elif command == "BlinkLab":
            if type(self.current_task) is not Blink:
                self.change_task(Blink)
                return 'ok'
            
        elif command == "ButtonPressed":
            if type(self.current_task) is not Closed:
                self.change_task(Closed)
            else:
                self.change_task(Opened)
            return 'ok'

        elif command == "Status":
            return self.current_task.name

    def change_task(self, new_task):
        if self.current_task is not None:
            self.current_task.shutdown()
        self.current_task = new_task(self.ampel)
        self.current_task.start()  


def notify(cmd, path='/var/run/ampel.sock'):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(path)
    s.send(cmd.encode())
    res = s.recv(1024).decode()
    s.close()
    return res

if __name__ == '__main__':
    a = Foreman('/var/run/ampel.sock', dry=False)
    a.loop()
