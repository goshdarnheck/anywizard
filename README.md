# README

Any Wizard is a script that replaces colours randomly in a random image with other colours or images, generates a name, and tweets out the result.

## How do I get set up?

- \$ pip install -r requirements.txt
- Add your Twitter API credentials to config.sample.ini
- Rename config.sample.ini to config.ini
- Add replacement images to /images if desired
- \$ py anywizard.py

## Config

- Create a file named config.ini (a sample is supplied as config.sample.ini)
- Add your Twitter API credentials to config.ini unders [TwitterApiCreds]
- Settings:
  - Tweet: boolean, whether or not to send tweet
  - Template: string, folder name of template to load. A value of "random" (without quotes) will load a random template from the templates folder

## Creating Templates

- Each template must have it's own folder in the templates directory
- Each template must have a config.json file
- Config.json files can have the following properties:
  - Colours: an array of colours to replace, each colour an array with rgba values repsectively
- Wizard image templates and FX image are recommened to be 440px x 220px PNG files (Twitters current preview image size)
- Wizard image templates work best w/ Twitter when they have an alpha channel (otherwise Twitter may generate and serve JPG files instead of PNGs)
- Wizard image templates should be named wizard.[n].png where [n] can be [0-9]. This gives the ability to have variations per template
- FX image templates should be named fx.[n].png where n can be [0-9]
- FX images should be black and white, where white pixels indicate where an effect is to be applied

### Who do I talk to?

- @anywizard https://twitter.com/anywizard
