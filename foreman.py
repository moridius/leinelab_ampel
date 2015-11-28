#!/usr/bin/python3

import time
import sys
import os
import socket
import logging
import argparse
from threading import Thread, Event

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
        
        import RPi.GPIO as gpio
        self.gpio = gpio
        
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)

        for number in self.pins.values():
            gpio.setup( number, gpio.OUT )

    def set(self, pin, enable=True):
        state = { True: 'on', False: 'off' }[enable]
        logging.debug('%s lamp is now %s' % (pin, state))
        
        if self.dry:
            return
        
        if enable:
            self.gpio.output(self.pins[pin], self.gpio.HIGH)
        else:
            self.gpio.output(self.pins[pin], self.gpio.LOW)


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
        logging.info('Opened')
        
        self.ampel.set('green', True)
        self.ampel.set('red', False)


class Blink(BasicTask):
    name = 'BlinkLab'

    def run(self): 
        logging.info('Started blinking')

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
        logging.info('Closed')

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dry-run', action='store_true',
                        dest='dry')
    parser.add_argument('--log-level', type=str, default='INFO',
                        dest='log_level')

    args = parser.parse_args()

    FORMAT= '%(levelname)-8s %(message)s'
    logging.basicConfig(format=FORMAT, level=args.log_level)
    
    f = Foreman('/var/run/ampel.sock', dry=args.dry)
    f.loop()
