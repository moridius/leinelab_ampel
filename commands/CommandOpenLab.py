#!/home/leinelab/ampel/ve_python

import pins
import tw
import spaceapi

pins.EnableRed( False )
pins.EnableGreen( True )

tw.SendTweet( True )

spaceapi.TriggerAPI( True )
