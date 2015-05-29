#!/home/leinelab/ampel/ve_python

import pins
import tw
import spaceapi

pins.EnableRed( True )
pins.EnableGreen( False )

tw.SendTweet( False )

spaceapi.TriggerAPI( False )
