#!/home/leinelab/ampel/ve_python

import pins
import tw
import spaceapi
import filesys

pins.EnableRed( False )
pins.EnableGreen( True )

# avoid double postings
if filesys.LoadStatus() == "Open":
	exit()

filesys.SaveStatus('Open')

tw.SendTweet( True )

spaceapi.TriggerAPI( True )
