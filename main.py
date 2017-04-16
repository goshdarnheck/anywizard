import ConfigParser
import Image
import random
import os
import tweepy
from colour import Color
from pprint import pprint

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

# Read Config File
dir = os.path.dirname(os.path.abspath(__file__))
Config = ConfigParser.ConfigParser()
Config.read(os.path.join(dir, 'config.ini'))

twitterConfig = { 
    'consumer_key'        : Config.get('TwitterApiCreds', 'consumer_key'),
    'consumer_secret'     : Config.get('TwitterApiCreds', 'consumer_secret'),
    'access_token'        : Config.get('TwitterApiCreds', 'access_token'),
    'access_token_secret' : Config.get('TwitterApiCreds', 'access_token_secret') 
}

# random template
templateImageList = os.listdir('%s/templates' % dir)
templateImage = Image.open('%s/templates/%s' % (dir, random.choice(templateImageList)))
templateImage = templateImage.convert('RGBA')

# random  fill image
fillImageList = os.listdir('%s/images' % dir)
fillImage = Image.open('%s/images/%s' % (dir, random.choice(fillImageList)))
fillImage = fillImage.convert('RGBA')

# watermark image
watermarkImage = Image.open(os.path.join(os.path.dirname(__file__), 'watermark.png'))
watermarkImage = watermarkImage.convert('RGBA')

templateImagePixels = templateImage.load()
fillImagePixels = fillImage.load()
watermarkImagePixels = watermarkImage.load()

coloursToReplace = [
    # Red
    #ff0000
    [255, 0, 0, 255],

    # Green
    #00ff00
    [0, 255, 0, 255],

    # Blue
    #0000ff
    [0, 0, 255, 255],

    # Red MEDIUMN
    #cc0000
    [204, 0, 0, 255],

    # Green MEDIUMN
    #00cc00
    [0, 204, 0, 255],

    # Blue MEDIUMN
    #0000cc
    [0, 0, 204, 255],

    # Red DARK
    #660000
    [102, 0, 0, 255],

    # Green DARK
    #006600
    [0, 102, 0, 255],

    # Blue DARK
    #000066
    [0, 0, 102, 255],

    # Yellow
    #ffff00
    [255, 255, 0, 255],

    # Cyan
    #00ffff
    [0, 255, 255, 255],

    # Magenta
    #ff00ff
    [255, 0, 255, 255],

    # Orange
    #ff9900
    [255, 153, 0, 255],

    # Spring Green
    #00ff99
    [0, 255, 153, 255],

    # Electric Violet
    #9900ff
    [153, 0, 255, 255]
]

imageIndex = random.randint(0, len(coloursToReplace) -1)

# Generate Random Colours
randomColours = []
for i in range(0, len(coloursToReplace)):
    c = Color(hsl=(random.uniform(0, 1), random.uniform(0.7, 1), 0.5))
    r = max(0, int(round(c.red * 256 -1)))
    g = max(0, int(round(c.green * 256 -1)))
    b = max(0, int(round(c.blue * 256 -1)))

    randomColours.append([r,g,b])

# Replace Colours
for y in xrange(templateImage.size[1]):
    for x in xrange(templateImage.size[0]):
        for z in range(0, len(coloursToReplace)):
            if templateImagePixels[x, y] == (coloursToReplace[z][0], coloursToReplace[z][1], coloursToReplace[z][2], 255):
                if (z == imageIndex):
                    templateImagePixels[x, y] = fillImagePixels[x, y]
                else:
                    templateImagePixels[x, y] = (randomColours[z][0], randomColours[z][1], randomColours[z][2], 255)

# Add Watermark
for x in range(templateImage.size[0] - 96, templateImage.size[0]):
    for y in range(templateImage.size[1] - 20, templateImage.size[1]):
        if (watermarkImagePixels[x - templateImage.size[0] + 96, y - templateImage.size[1] + 20][3] >= 255):
            templateImagePixels[x, y] = watermarkImagePixels[x - templateImage.size[0] + 96, y - templateImage.size[1] + 20]
    
# Save Image
templateImage.save(os.path.join(dir, 'output.png'))

# Create Random Name
tweet = '%s %s %s' % (
	random.choice(list(open(os.path.join(os.path.dirname(__file__), 'adjectives.txt')))).rstrip().title(),
	random.choice(list(open(os.path.join(os.path.dirname(__file__), 'nouns.txt')))).rstrip(),
	random.choice(list(open(os.path.join(os.path.dirname(__file__), 'jobs.txt')))).rstrip()
)
print(tweet)

# Tweet!
api = get_api(twitterConfig)
api.update_with_media(os.path.join(dir, 'output.png'), tweet)
