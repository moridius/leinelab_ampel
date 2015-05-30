#!/home/leinelab/ampel/ve_python

import pins
import tw
import spaceapi
import filesys

pins.EnableRed( True )
pins.EnableGreen( False )

filesys.SaveStatus('Closed')

tw.SendTweet( False )

spaceapi.TriggerAPI( False )
