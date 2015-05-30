#!/home/leinelab/ampel/ve_python

import pins
import tw
import spaceapi
import filesys

pins.EnableRed( False )
pins.EnableGreen( True )

filesys.SaveStatus('Open')

tw.SendTweet( True )

spaceapi.TriggerAPI( True )
