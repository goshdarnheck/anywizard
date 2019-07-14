from colour import Color
import random


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
