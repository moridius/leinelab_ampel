#!/home/leinelab/ampel/ve_python

import urllib.request

import time
import subprocess
import sys
import os
import util

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
        return content
    else:
        return ""


def IsCommandRunning( cmd ):
    try:
        return ( cmd.poll() == None )
    except:
        return False


def KillCommand( cmd ):
    try:
        cmd.terminate()
    except:
        pass


def RunCommand( cmdStr ):
    if cmdStr == "":
        return None

    cmd_parts = cmdStr.split()
    cmd = [ "/home/leinelab/ampel/commands/Command" + cmd_parts[0] + ".py" ]
    cmd += cmd_parts[1:]

    try:
        return subprocess.Popen( cmd )
    except:
        pass


## MAIN ##

current_command = None
util.log( "Started. Wait for commands..." )

while True:
    command = PollForCommand()
    if command != "":
        util.log( "Received command: " + command )
        if IsCommandRunning( current_command ):
            util.log( "There is a running command, I'll kill it." )
            KillCommand( current_command )

        util.log( "Run new command..." )
        current_command = RunCommand( command )
    time.sleep( 1 )
