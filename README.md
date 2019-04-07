# README

Any Wizard is a script that replaces colours randomly in a random image with other colours or images, generates a name, and tweets out the result.

## How do I get set up?

- \$ pip install -r requirements.txt
- Add your Twitter API credentials to config.sample.ini
- Rename config.sample.ini to config.ini
- Add replacement images to /images if desired
- Setup templates, read section "Creating Templates" below
- \$ py anywizard.py

## Template image requirements

- Twitter keeps png files in the png format if the tweeted file has an alpha channel, so make one pixel transparent in any template image
- 440x220px is recommended since that is the size of preview images on Twitter

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
- Wizard image templates should be named wizard.[n].png where [n] can be [0-9]. This gives the ability to have variations per template
- FXZ image templates should be named fx.[n].png where n can be [0-9]
- FX images should be black and white, where white pixels indicate where an effect is to be applied
- Currently, FX will also be a fill image, and 2 FX will be attempted

### Who do I talk to?

- @anywizard https://twitter.com/anywizard
