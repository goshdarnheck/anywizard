import os
import random


class TextGenerator:
    def getRandomLineFromTxt(self, filename):
        return random.choice(list(open(os.path.join(os.path.dirname(
            __file__), 'text/%s.txt' % filename), encoding="utf-8"))).rstrip().title()

    def getAdjective(self):
        return self.getRandomLineFromTxt('adjectives')

    def getNoun(self):
        return self.getRandomLineFromTxt('nouns')

    def getJob(self):
        return self.getRandomLineFromTxt('jobs')

    def getWizardName(self):
        name = '%s %s %s' % (
            self.getAdjective(),
            self.getNoun(),
            self.getJob()
        )

        return name

    def randomEmoji(self):
        return self.getRandomLineFromTxt('emojis')

    def randomEmojiText(self):
        return self.getRandomLineFromTxt('emojitext')

    def getRandomTweetText(self):
        name = self.getWizardName()
        emoji = self.randomEmoji()
        emojiText = self.randomEmojiText()

        return u'✦ %s ✦\n%s: %s' % (name, emojiText, emoji)
