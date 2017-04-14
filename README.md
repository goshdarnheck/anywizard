# README #

Any Wizard is a script that replaces colours randomly in a random image with other colours or images, generates a name, and tweets out the result.

### How do I get set up? ###

* $ pip install -r requirements.txt
* Add your Twitter API credentials to config.sample.ini
* Rename config.sample.ini to config.ini
* Add replacement images to /images if desired
* Add template images to /templates
* $ python main.py

### Template image requirements ###

* Twitter keeps png files in the png format if the tweeted file has an alpha channel, so make one pixel transparent in any template image
* 440x220px is recommended since that is the size of preview images on Twitter
* Colours that will be replaced (also see colours.png):
   * \#ff0000
   * \#00ff00
   * \#0000ff
   * \#cc0000
   * \#00cc00
   * \#0000cc
   * \#660000
   * \#006600
   * \#000066
   * \#ffff00
   * \#00ffff
   * \#ff00ff
   * \#ff9900
   * \#00ff99
   * \#9900ff

### Who do I talk to? ###

* @anywizard https://twitter.com/anywizard