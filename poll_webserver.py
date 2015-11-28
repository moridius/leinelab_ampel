#!/usr/bin/python3

import urllib.request
import os
import os.path
import datetime
import time
import sys
import util
import foreman

util.log_file = "poll.log"
util.log( "Start poll script." )

util.log( "Poll script started." )

while True:
    res = urllib.request.urlopen( "https://leinelab.net/ampel/job.php" )
    content = res.read().decode()
    if content != "":
        foreman.notify(content)
        util.log( "Polled webserver and got something. " + datetime.datetime.now().isoformat() )
    else:
        util.log( "Polled webserver, got nothing. " + datetime.datetime.now().isoformat() )
    time.sleep( 15 )
