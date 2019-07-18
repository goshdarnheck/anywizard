import time
import configparser
import os
import tweepy
from Text import TextGenerator
from ImageGenerator import ImageGenerator


def getTweepyApi(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


# Get start time so we can log elapsed time
start_time = time.time()

# Open and parse config file
dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(dir, 'config.ini'))

twitterConfig = {
    'consumer_key': Config.get('TwitterApiCreds', 'consumer_key'),
    'consumer_secret': Config.get('TwitterApiCreds', 'consumer_secret'),
    'access_token': Config.get('TwitterApiCreds', 'access_token'),
    'access_token_secret': Config.get('TwitterApiCreds', 'access_token_secret')
}

tweet = Config.getboolean('settings', 'tweet')
templateSetting = Config.get('settings', 'template')

print("Tweeting: " + str(tweet))
print("Template Setting: " + str(templateSetting))

# REFACTOR
imageGenerator = ImageGenerator(dir, templateSetting)
imageGenerator.createImage('output.png')
# REFACTOR

# Get Text to Tweet
textGen = TextGenerator()
tweetText = textGen.getRandomTweetText()
print("\nTweet: " + tweetText + "\n")

# Tweet!
if tweet:
    tweepyApi = getTweepyApi(twitterConfig)
    thing = tweepyApi.update_with_media(
        os.path.join(dir, 'output.png'), tweetText)

# Display elapsed time
elapsed_time = time.time() - start_time
print('Completed in %ss' % round(elapsed_time, 2))
