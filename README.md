# README

Any Wizard is a script that replaces colours randomly in a random image with other colours or images, generates a name, and tweets out the result.

## How do I get set up?

- \$ pip install -r requirements.txt
- Add your Twitter API credentials to config.sample.ini
- Rename config.sample.ini to config.ini
- Add replacement images to /images if desired
- Add template images to /templates
- \$ python main.py

## Template image requirements

- Twitter keeps png files in the png format if the tweeted file has an alpha channel, so make one pixel transparent in any template image
- 440x220px is recommended since that is the size of preview images on Twitter

## Config

- create a file named config.ini (a sample is supplied as config.sample.ini)
- add your Twitter API credentials to config.ini unders [TwitterApiCreds]
- settings:
  - tweet: boolean, whether or not to send tweet
  - template: string, folder name of template to load. A value of random will load a random template from the templates folder

## Creating Templates

- each template must have it's own folder in the templates directory
- each template must have a config.json file
- config.json files can have the following properties:
  - colours: an array of colours to replace, each colour an array with rgba values repsectively
- wizard image templates should be named wizard.[n].png where [n] can be anything. this gives the ability to have variations per template

### Who do I talk to?

- @anywizard https://twitter.com/anywizard
