#!/home/leinelab/ampel/ve_python

import random
import sys
import json
from twython import Twython

sys.path.append("/home/leinelab/ampel")
import util

util.log_file = "twitter.log"
util.log_append = True

credentials = {}

with open('/home/leinelab/ampel/commands/credentials.json') as cred:
    credStr = cred.read()
    credentials = json.loads(credStr)

def SendTweet( openLab ):
    dry_run = False
    
    #if openLab:
    #    print( "We want to open the Lab!" )
    #else:
    #    print( "We want to close the Lab!" )

    twitter = Twython( credentials['apiKey'], credentials['apiSecret'], credentials['accessToken'], credentials['accessTokenSecret'] )
    #print( "Initialised Twitter access." )

    # read possible tweets from file
    possible_tweets = []
    #try:
    tweet_file = "/home/leinelab/ampel/open_texts.txt"
    if not openLab:
        tweet_file = "/home/leinelab/ampel/close_texts.txt"

    f = open( tweet_file, 'r' )
    possible_tweets = f.readlines()
    f.close()
    #except:
    #    print( "Couldn't read tweet file!", file=sys.stderr )
    #    sys.exit(2)

    random.seed()
    #try:
    tweet = random.choice( possible_tweets )
    if openLab:
        tweet = tweet[:-1] + " [LeineLab opened]"
    else:
        tweet = tweet[:-1] + " [LeineLab closed]"

    if not dry_run:
        twitter.update_status( status=tweet )
        util.log( "Tweeted: " + tweet )
    else:
        util.log( "Tweeted: " + tweet + " (dry run)" )
    #except:
    #    print( "Couldn't choose a tweet (list empty)!", file=sys.stderr )
    #    sys.exit(3)
