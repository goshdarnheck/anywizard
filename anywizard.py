import time
import configparser
import os
import tweepy
from Text import TextGenerator
from ImageGenerator import ImageGenerator

# Get start time so we can log elapsed time
start_time = time.time()

# Open and parse config file
dir = os.path.dirname(os.path.abspath(__file__))
Config = configparser.ConfigParser()
Config.read(os.path.join(dir, 'config.ini'))


tweet = Config.getboolean('settings', 'tweet')
templateSetting = Config.get('settings', 'template')

print("Tweeting: " + str(tweet))
print("Template Setting: " + str(templateSetting))

# Generate Image
imageGenerator = ImageGenerator(dir, templateSetting)
imageGenerator.createImage('output.png')

# Get Text to Tweet
textGen = TextGenerator()
tweetText = textGen.getRandomTweetText()
print("\nTweet: " + tweetText + "\n")

# Tweet!
if tweet:
    auth = tweepy.OAuthHandler(Config.get('TwitterApiCreds', 'consumer_key'), Config.get(
        'TwitterApiCreds', 'consumer_secret'))
    auth.set_access_token(Config.get('TwitterApiCreds', 'access_token'), Config.get(
        'TwitterApiCreds', 'access_token_secret'))
    tweepyApi = tweepy.API(auth)
    tweetRes = tweepyApi.update_status_with_media(tweetText,
        os.path.join(dir, 'output.png'))

# Display elapsed time
elapsed_time = time.time() - start_time
print('Completed in %ss' % round(elapsed_time, 2))
