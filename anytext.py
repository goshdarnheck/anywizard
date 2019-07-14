import random
import os


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
