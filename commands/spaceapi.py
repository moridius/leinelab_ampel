#!/home/leinelab/ampel/ve_python

import urllib.request

def TriggerAPI( openIt ):
    print( "TriggerAPI" )
    urllib.request.urlopen( "https://leinelab.net/ampel/spaceapi.php?open=" + str( int( openIt ) ) )
