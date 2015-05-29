#!/home/leinelab/ampel/ve_python

import urllib.request
import os
import os.path
import datetime
import time
import sys

print( "Start poll script." )
sys.stdout.flush()

fifo_path = "/home/leinelab/ampel/fifo"
#if not os.path.exists( fifo_path ):
#    os.mkfifo( fifo_path )
#fifo = open( fifo_path, 'w' )

print( "Poll script started." )
sys.stdout.flush()

while True:
    res = urllib.request.urlopen( "https://leinelab.net/ampel/job.php" )
    content = res.read().decode()
    if content != "":
        fifo = open( fifo_path, 'w' )
        fifo.write( content )
        fifo.close()
        print( "Polled webserver and got something. " + datetime.datetime.now().isoformat() )
    else:
        print( "Polled webserver, got nothing. " + datetime.datetime.now().isoformat() )
    sys.stdout.flush()
    time.sleep( 15 )
