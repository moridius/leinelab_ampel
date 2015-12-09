#!/usr/bin/python3

import foreman
import logging
import sleekxmpp
import configparser
import time

HELP = """Available commands are: %s """

class AmpelBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, commands):
        super().__init__(jid, password)

        self.commands = commands
        self.status = None

        self.add_event_handler('session_start', self.sess_start)
        self.add_event_handler('message', self.message)

    def sess_start(self, event):
        self.set_status()
        self.get_roster()

    def set_status(self):
        new_status = foreman.notify('Status')
        if self.status != new_status:
            self.send_presence(pstatus=new_status)
            self.status = new_status

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            if msg['body'] in self.commands:
                answer = foreman.notify(msg['body'])
                if answer != 'ok':
                    reply = msg.reply(answer)
            else:
                reply = msg.reply(HELP % ', '.join(self.commands))
            reply.send()

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('jabber.ini')

    jabber = config['jabber']
    stuff = config['stuff']
    commands = stuff['commands'].split(',')
    
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-8s %(message)s')

    client = AmpelBot(jabber['user'], jabber['pass'], commands)
    client.connect()
    
    client.process(block=False)
    
    while True:
        client.set_status()
        time.sleep(0.2)
