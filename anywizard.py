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


def getRandomColoursList():
    randomColours = []
    for _ in range(0, len(coloursToReplace)):
        c = Color(hsl=(random.uniform(0, 1),
                       random.uniform(0, 1), random.uniform(0, 1)))
        r = max(0, int(round(c.red * 256 - 1)))
        g = max(0, int(round(c.green * 256 - 1)))
        b = max(0, int(round(c.blue * 256 - 1)))

        randomColours.append([r, g, b])

    return randomColours


def getTemplateFolderName(templateSetting):
    templateImageList = os.listdir('%s/templates' % dir)
    return random.choice(
        templateImageList) if templateSetting == 'random' else templateSetting


def getRandomTemplateImage(templateFolderName):
    templateImage = Image.open('%s/templates/%s/wizard.2.png' %
                               (dir, templateFolderName))
    return templateImage.convert('RGBA')


def getRandomFillImageName():
    fillImageList = os.listdir('%s/images' % dir)
    return random.choice(fillImageList)


def openRandomFillImage(fillImageName):
    fillImage = Image.open('%s/images/%s' % (dir, fillImageName))
    return fillImage.convert('RGBA')


def getRandomTweetText():
    return '%s %s %s %s' % (
        random.choice(list(open(os.path.join(os.path.dirname(
            __file__), 'text/adjectives.txt')))).rstrip().title(),
        random.choice(
            list(open(os.path.join(os.path.dirname(__file__), 'text/nouns.txt')))).rstrip(),
        random.choice(
            list(open(os.path.join(os.path.dirname(__file__), 'text/jobs.txt')))).rstrip(),
        random.choice(
            list(open(os.path.join(os.path.dirname(__file__), 'text/emojis.txt'), encoding="utf-8"))).rstrip()
    )


def getRandomFxMaskImageName(templateFolderName, removeThis):
    fxMaskList = [f for f in os.listdir(
        'templates/%s' % templateFolderName) if re.match(r'fx\.[0-9]\.png', f)]
    fxMaskImageName = random.choice(fxMaskList)
    return '%s/%s' % (templateFolderName, fxMaskImageName)


def getRandomFxMaskImage(fxMaskImageName):
    fxMaskImage = Image.open('templates/%s' % fxMaskImageName)
    return fxMaskImage.convert('RGBA')


def applyReplacementFx(templateImage, templateImagePixels, fxMaskImagePixels, fillImagePixels):
    for y in list(range(templateImage.size[1])):
        for x in list(range(templateImage.size[0])):
            if (fxMaskImagePixels[x, y] == (255, 255, 255, 255)):
                templateImagePixels[x, y] = fillImagePixels[x, y]


start_time = time.time()

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
templateSetting = Config.get('settings', 'template')


# Choose random template and open template image and convert to rgba
templateFolderName = getTemplateFolderName(templateSetting)
templateImage = getRandomTemplateImage(templateFolderName)
print("Template Folder: " + templateFolderName)
print("Template Image: wizard.2.png")

# Load colours to replace from template config
with open((os.path.join(os.path.dirname(__file__), 'templates/%s/config.json' % templateFolderName))) as f:
    coloursToReplaceJson = json.load(f)
coloursToReplace = coloursToReplaceJson["colours"]

# Choose random fill image and open file and convert to rgba
fillImageName = getRandomFillImageName()
fillImage = openRandomFillImage(fillImageName)
fillImageName2 = getRandomFillImageName()
fillImage2 = openRandomFillImage(fillImageName2)
print("Fill Image: " + fillImageName)
print("Fill Image 2: " + fillImageName2)

fxMaskImageName = getRandomFxMaskImageName(templateFolderName, 1)
fxMaskImage = getRandomFxMaskImage(fxMaskImageName)
fxMaskImageName2 = getRandomFxMaskImageName(templateFolderName, 2)
fxMaskImage2 = getRandomFxMaskImage(fxMaskImageName2)

# Load template and fill image and fx image
templateImagePixels = templateImage.load()
fillImagePixels = fillImage.load()
fillImagePixels2 = fillImage2.load()
fxMaskImagePixels = fxMaskImage.load()
fxMaskImagePixels2 = fxMaskImage2.load()

# Choose random replacement colour to be replaced by fill image
imageIndex = random.randint(0, len(coloursToReplace) - 1)


# Get Random Colours
randomColours = getRandomColoursList()


# Replace Colours
for y in list(range(templateImage.size[1])):
    for x in list(range(templateImage.size[0])):
        for z in range(0, len(coloursToReplace)):
            if templateImagePixels[x, y] == (coloursToReplace[z][0], coloursToReplace[z][1], coloursToReplace[z][2], 255):
                templateImagePixels[x, y] = (
                    randomColours[z][0], randomColours[z][1], randomColours[z][2], 255)


# Apply FX
applyReplacementFx(templateImage, templateImagePixels,
                   fxMaskImagePixels, fillImagePixels)

applyReplacementFx(templateImage, templateImagePixels,
                   fxMaskImagePixels2, fillImagePixels2)

# Save Image
templateImage.save(os.path.join(dir, 'output.png'))
print("Output: " + os.path.join(dir, 'output.png'))

# Get Text to Tweet
tweetText = getRandomTweetText()
print("Tweet: " + tweetText)

# Tweet!
print("Tweeting: " + str(tweet))
if tweet:
    tweepyApi = getTweepyApi(twitterConfig)
    thing = tweepyApi.update_with_media(
        os.path.join(dir, 'output.png'), tweetText)

elapsed_time = time.time() - start_time
print('Completed in %ss' % round(elapsed_time, 2))
