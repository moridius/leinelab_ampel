#!/home/leinelab/ampel/ve_python

import pins
import tw
import spaceapi
import filesys

pins.EnableRed( True )
pins.EnableGreen( False )

# avoid double postings
if filesys.LoadStatus() == "Closed":
	exit()

filesys.SaveStatus('Closed')

tw.SendTweet( False )

spaceapi.TriggerAPI( False )
