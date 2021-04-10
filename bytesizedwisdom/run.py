
# Not tested
import os
import time
import pickle

while True:
    try:
        with open('tweets.data', 'rb') as filehandle:
            tweets = pickle.load(filehandle)
        print(f'Posting {len(tweets)} tweets')

    except:
        print('error opening tweets.data file')

    os.system('python3 post_tweets.py')

    while os.path.getsize('tweets.data') > 0:
        time.sleep(6000)

    print('Generating tweets')
    os.system('python3 tweet_generation.py')

    while os.path.getsize('tweets.data') == 0:
        time.sleep(600)