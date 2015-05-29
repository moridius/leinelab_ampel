#!/home/leinelab/ampel/ve_python

import random
import sys
from twython import Twython

def SendTweet( openLab ):
    dry_run = True
    
    #if openLab:
    #    print( "We want to open the Lab!" )
    #else:
    #    print( "We want to close the Lab!" )

    apiKey            = "wKBROv4Uk5pNS8S9IiOXydKb9"
    apiSecret         = "1sOOlFArqoooztzMNA5KSHfEzrGbFMkl4tgHjA4csDt5GzIEg3"
    accessToken       = "887504742-mZ5mX6egJlTHtAadrz0vWQ5kknZYFeQPenjKsjQO"
    accessTokenSecret = "eGiEUD1j3qSITil3XedVTr8UtPRYXtqeaozmGAxvAhY6d"

    twitter = Twython( apiKey, apiSecret, accessToken, accessTokenSecret )
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
        print( "Tweeted: " + tweet )
    else:
        print( "Tweeted: " + tweet + " (dry run)" )
    #except:
    #    print( "Couldn't choose a tweet (list empty)!", file=sys.stderr )
    #    sys.exit(3)
