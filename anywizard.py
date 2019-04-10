import time
import re
import configparser
import random
import os
import json
import tweepy
from PIL import Image
from colour import Color


def getTweepyApi(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)


def getRandomColoursList(length):
    randomColours = []
    for _ in range(0, length):
        c = Color(hsl=(random.uniform(0, 1),
                       random.uniform(0, 1), random.uniform(0, 1)))
        r = max(0, int(round(c.red * 256 - 1)))
        g = max(0, int(round(c.green * 256 - 1)))
        b = max(0, int(round(c.blue * 256 - 1)))

        randomColours.append([r, g, b])

    return randomColours


def getTemplateFolderName(templateSetting):
    templateImageList = os.listdir('%s/templates' % dir)
    templateFolderName = random.choice(
        templateImageList) if templateSetting == 'random' else templateSetting
    print("Template Folder: " + templateFolderName)
    return templateFolderName


def getRandomTemplateImage(templateFolderName):
    imageList = [f for f in os.listdir(
        '%s/templates/%s' % (dir, templateFolderName)) if re.match(r'wizard\.[0-9]\.png', f)]
    imageName = random.choice(imageList)
    print("Template Image: %s" % imageName)
    templateImage = Image.open('%s/templates/%s/%s' %
                               (dir, templateFolderName, imageName))

    return templateImage.convert('RGBA')


def getRandomFillImage():
    fillImageList = os.listdir('%s/images' % dir)
    randomFillImageName = random.choice(fillImageList)
    fillImage = Image.open('%s/images/%s' % (dir, randomFillImageName))
    print("Fill Image: " + randomFillImageName)
    return fillImage.convert('RGBA')


def getRandomTweetText():
    name = '%s %s %s' % (
        random.choice(list(open(os.path.join(os.path.dirname(
            __file__), 'text/adjectives.txt')))).rstrip().title(),
        random.choice(
            list(open(os.path.join(os.path.dirname(__file__), 'text/nouns.txt')))).rstrip(),
        random.choice(
            list(open(os.path.join(os.path.dirname(__file__), 'text/jobs.txt')))).rstrip(),

    )

    emoji = random.choice(
        list(open(os.path.join(os.path.dirname(__file__), 'text/emojis.txt'), encoding="utf-8"))).rstrip()
    emojiText = random.choice(
        list(open(os.path.join(os.path.dirname(__file__), 'text/emojitext.txt'), encoding="utf-8"))).rstrip()

    return '%s\n- %s: %s' % (name, emojiText, emoji)


def getRandomFxMaskImage(templateFolderName):
    fxMaskList = [f for f in os.listdir(
        '%s/templates/%s' % (dir, templateFolderName)) if re.match(r'fx\.[0-9]\.png', f)]

    if (fxMaskList):
        fxMaskImageName = random.choice(fxMaskList)
        fxMaskImage = Image.open('%s/templates/%s/%s' %
                                 (dir, templateFolderName, fxMaskImageName))
        return fxMaskImage.convert('RGBA')
    else:
        return 0


def applyReplacementFx(templateImage, templateImagePixels, fxMaskImagePixels, fillImagePixels):
    for y in list(range(templateImage.size[1])):
        for x in list(range(templateImage.size[0])):
            if (fxMaskImagePixels[x, y] == (255, 255, 255, 255)):
                templateImagePixels[x, y] = fillImagePixels[x, y]


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


# Choose random template and open template image and convert to rgba
templateFolderName = getTemplateFolderName(templateSetting)
templateImage = getRandomTemplateImage(templateFolderName)

# Load colours to replace from template config
with open((os.path.join(os.path.dirname(__file__), 'templates/%s/config.json' % templateFolderName))) as f:
    coloursToReplaceJson = json.load(f)
coloursToReplace = coloursToReplaceJson["colours"]


# Load template and fill image and fx image
templateImagePixels = templateImage.load()

# Get Random Colours
randomColours = getRandomColoursList(len(coloursToReplace))

# Replace Colours
for y in list(range(templateImage.size[1])):
    for x in list(range(templateImage.size[0])):
        for z in range(0, len(coloursToReplace)):
            if templateImagePixels[x, y] == (coloursToReplace[z][0], coloursToReplace[z][1], coloursToReplace[z][2], 255):
                templateImagePixels[x, y] = (
                    randomColours[z][0], randomColours[z][1], randomColours[z][2], 255)

# Get FX Stuff
# Get 2 random fill images
fillImage = getRandomFillImage()
fillImage2 = getRandomFillImage()

# Get Random FX mask and apply fill image FX
fxMaskImage = getRandomFxMaskImage(templateFolderName)
if (fxMaskImage):
    fxMaskImagePixels = fxMaskImage.load()
    applyReplacementFx(templateImage, templateImagePixels,
                       fxMaskImagePixels, fillImage.load())

# Get Random FX mask and apply fill image again
fxMaskImage = getRandomFxMaskImage(templateFolderName)
if (fxMaskImage):
    fxMaskImagePixels = fxMaskImage.load()
    applyReplacementFx(templateImage, templateImagePixels,
                       fxMaskImagePixels, fillImage2.load())

# Save Image
templateImage.save(os.path.join(dir, 'output.png'))
print("Output: " + os.path.join(dir, 'output.png'))

# Get Text to Tweet
tweetText = getRandomTweetText()
print("\nTweet:")
print(tweetText)
print("\n")

# Tweet!
print("Tweeting: " + str(tweet))
if tweet:
    tweepyApi = getTweepyApi(twitterConfig)
    thing = tweepyApi.update_with_media(
        os.path.join(dir, 'output.png'), tweetText)

# Display elapsed time
elapsed_time = time.time() - start_time
print('Completed in %ss' % round(elapsed_time, 2))
