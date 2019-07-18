import os
import random
from PIL import Image
import re
import json
import anycolours


class ImageGenerator:
    def __init__(self, dir, templateSetting):
        self.dir = dir
        self.templateSetting = templateSetting
        self.templateFolderName = self.getTemplateFolderName(
            self.templateSetting)
        self.templateImage = self.getRandomTemplateImage(
            self.templateFolderName)

    def createImage(self, filename):
        with open((os.path.join(os.path.dirname(__file__), 'templates/%s/config.json' % self.templateFolderName))) as f:
            coloursToReplaceJson = json.load(f)
        coloursToReplace = coloursToReplaceJson["colours"]

        # Load template and fill image and fx image
        templateImagePixels = self.templateImage.load()

        # replace colours from colour settings with random colours
        randomColours = anycolours.getRandomColoursList(len(coloursToReplace))
        self.replaceColours(templateImagePixels,
                            coloursToReplace, randomColours)

        self.applyFx(templateImagePixels)
        self.applyFx(templateImagePixels)

        self.templateImage.save(os.path.join(self.dir, filename))

        return self.templateImage

    def applyFx(self, templateImagePixels):
        fillImage = self.getRandomFillImage()
        fxMaskImage = self.getRandomFxMaskImage(self.templateFolderName)
        if (fxMaskImage):
            fxMaskImagePixels = fxMaskImage.load()
            self.applyReplacementFx(self.templateImage, templateImagePixels,
                                    fxMaskImagePixels, fillImage.load())

    def getTemplateFolderName(self, templateSetting):
        templateImageList = os.listdir('%s/templates' % self.dir)
        templateFolderName = random.choice(
            templateImageList) if templateSetting == 'random' else templateSetting
        print("CLASS Template Folder: " + templateFolderName)
        return templateFolderName

    def getRandomTemplateImage(self, templateFolderName):
        imageList = [f for f in os.listdir(
            '%s/templates/%s' % (self.dir, templateFolderName)) if re.match(r'wizard\.[0-9]+\.png', f)]
        imageName = random.choice(imageList)
        print("CLASS Template Image: %s" % imageName)
        templateImage = Image.open('%s/templates/%s/%s' %
                                   (self.dir, templateFolderName, imageName))

        return templateImage.convert('RGBA')

    def replaceColours(self, templateImagePixels, coloursToReplace, replacementColors):
        for y in list(range(self.templateImage.size[1])):
            for x in list(range(self.templateImage.size[0])):
                for z in range(0, len(coloursToReplace)):
                    if templateImagePixels[x, y] == (coloursToReplace[z][0], coloursToReplace[z][1], coloursToReplace[z][2], 255):
                        templateImagePixels[x, y] = (
                            replacementColors[z][0], replacementColors[z][1], replacementColors[z][2], 255)

    def getRandomFillImage(self):
        fillImageList = os.listdir('%s/images' % self.dir)
        randomFillImageName = random.choice(fillImageList)
        fillImage = Image.open('%s/images/%s' %
                               (self.dir, randomFillImageName))
        print("Fill Image: " + randomFillImageName)
        return fillImage.convert('RGBA')

    def getRandomFxMaskImage(self, templateFolderName):
        fxMaskList = [f for f in os.listdir(
            '%s/templates/%s' % (self.dir, templateFolderName)) if re.match(r'fx\.[0-9]+\.png', f)]

        if (fxMaskList):
            fxMaskImageName = random.choice(fxMaskList)
            fxMaskImage = Image.open('%s/templates/%s/%s' %
                                     (self.dir, templateFolderName, fxMaskImageName))
            print("FX Image: " + fxMaskImageName)
            return fxMaskImage.convert('RGBA')
        else:
            return 0

    def applyReplacementFx(self, templateImage, templateImagePixels, fxMaskImagePixels, fillImagePixels):
        for y in list(range(templateImage.size[1])):
            for x in list(range(templateImage.size[0])):
                if (fxMaskImagePixels[x, y] == (255, 255, 255, 255)):
                    templateImagePixels[x, y] = fillImagePixels[x, y]
