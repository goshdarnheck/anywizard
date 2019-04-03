import configparser
import random
import os
import json
import tweepy
from PIL import Image
from colour import Color
from pprint import pprint


def getTweepyApi(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


# Read Config File
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

# Choose random template and open template image
templateImageList = os.listdir('%s/templates' % dir)
templateFolderName = random.choice(templateImageList)
templateImage = Image.open('%s/templates/%s/wizard.1.png' %
                           (dir, templateFolderName))
templateImage = templateImage.convert('RGBA')
print("Template Folder: " + templateFolderName)
print("Template Image: wizard.1.png")

# Load colours to replace from template config
with open((os.path.join(os.path.dirname(__file__), 'templates/%s/config.json' % templateFolderName))) as f:
    coloursToReplaceJson = json.load(f)
coloursToReplace = coloursToReplaceJson["colours"]

# random  fill image
fillImageList = os.listdir('%s/images' % dir)
fillImageName = random.choice(fillImageList)
fillImage = Image.open('%s/images/%s' % (dir, fillImageName))
fillImage = fillImage.convert('RGBA')
print("Fill Image: " + fillImageName)

# watermark image
watermarkImage = Image.open(os.path.join(
    os.path.dirname(__file__), 'watermark.png'))
watermarkImage = watermarkImage.convert('RGBA')

templateImagePixels = templateImage.load()
fillImagePixels = fillImage.load()
watermarkImagePixels = watermarkImage.load()

imageIndex = random.randint(0, len(coloursToReplace) - 1)

# Generate Random Colours
randomColours = []
for i in range(0, len(coloursToReplace)):
    c = Color(hsl=(random.uniform(0, 1),
                   random.uniform(0, 1), random.uniform(0, 1)))
    r = max(0, int(round(c.red * 256 - 1)))
    g = max(0, int(round(c.green * 256 - 1)))
    b = max(0, int(round(c.blue * 256 - 1)))

    randomColours.append([r, g, b])

# Replace Colours
for y in list(range(templateImage.size[1])):
    for x in list(range(templateImage.size[0])):
        for z in range(0, len(coloursToReplace)):
            if templateImagePixels[x, y] == (coloursToReplace[z][0], coloursToReplace[z][1], coloursToReplace[z][2], 255):
                if (z == imageIndex):
                    templateImagePixels[x, y] = fillImagePixels[x, y]
                else:
                    templateImagePixels[x, y] = (
                        randomColours[z][0], randomColours[z][1], randomColours[z][2], 255)

# Add Watermark
for x in range(templateImage.size[0] - 96, templateImage.size[0]):
    for y in range(templateImage.size[1] - 20, templateImage.size[1]):
        if (watermarkImagePixels[x - templateImage.size[0] + 96, y - templateImage.size[1] + 20][3] >= 255):
            templateImagePixels[x, y] = watermarkImagePixels[x -
                                                             templateImage.size[0] + 96, y - templateImage.size[1] + 20]

# Save Image
templateImage.save(os.path.join(dir, 'output.png'))
print("Output: " + os.path.join(dir, 'output.png'))

# Create Random Name
tweetText = '%s %s %s %s' % (
    random.choice(list(open(os.path.join(os.path.dirname(
        __file__), 'text/adjectives.txt')))).rstrip().title(),
    random.choice(
        list(open(os.path.join(os.path.dirname(__file__), 'text/nouns.txt')))).rstrip(),
    random.choice(
        list(open(os.path.join(os.path.dirname(__file__), 'text/jobs.txt')))).rstrip(),
    random.choice(
        list(open(os.path.join(os.path.dirname(__file__), 'text/emojis.txt'), encoding="utf-8"))).rstrip()
)
print("Tweet: " + tweetText)

# Tweet!
print("Tweeting: " + str(tweet))
if tweet:
    tweepyApi = getTweepyApi(twitterConfig)
    thing = tweepyApi.update_with_media(
        os.path.join(dir, 'output.png'), tweetText)
