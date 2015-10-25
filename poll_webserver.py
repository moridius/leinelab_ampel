#!/home/leinelab/ampel/ve_python

import urllib.request
import os
import os.path
import datetime
import time
import sys
import util

fpid = os.fork()

util.log_file = "poll.log"

if fpid != 0:
    util.log( "Forked poll script." )
    util.log( "pid: " + str(fpid) )
    sys.exit(0) # stop parent process, child continues

util.log( "Start poll script." )

fifo_path = "/var/run/ampel.fifo"
#if not os.path.exists( fifo_path ):
#    os.mkfifo( fifo_path )
#fifo = open( fifo_path, 'w' )

util.log( "Poll script started." )

while True:
    res = urllib.request.urlopen( "https://leinelab.net/ampel/job.php" )
    content = res.read().decode()
    if content != "":
        fifo = open( fifo_path, 'w' )
        fifo.write( content )
        fifo.close()
        util.log( "Polled webserver and got something. " + datetime.datetime.now().isoformat() )
    else:
        util.log( "Polled webserver, got nothing. " + datetime.datetime.now().isoformat() )
    time.sleep( 15 )
