import pickle
import os
import tweepy
import schedule
import random
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

tweets_empty = False

def tweet():

    # Connecting to Twitter with tweepy
    # TODO error handling
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)

    # Get tweets from file
    # TODO move this error handling into master script alternating betweeen tweet_generation and post_tweets
    try:

        with open('tweets.data', 'rb') as filehandle:
                tweets = pickle.load(filehandle)

    except:
        print('error opening tweets.data file')
        return

    # send tweet
    text = tweets.pop()
    api.update_status(text)

    # write updated list of pending tweets to file
    with open('tweets.data', 'wb') as filehandle:
        pickle.dump(tweets, filehandle)

# Posting tweets every 10 to 100 minutes
schedule.every(10).to(100).minutes.do(tweet)

while os.path.getsize('tweets.data') > 0:
    schedule.run_pending()
