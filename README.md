# Monika After Story

This is a mod for the free game DDLC from Team Salvato, available for download [here](ddlc.moe). I don't own any part of the game.

Basically, it replaces the end of the original game with a simulator of your eternal life with Monika, featuring new events, handlers, and metacommentary. Think Love Plus meets Totono.

If you have any problems with the game, feel free to raise issues here. Pull requests for new stuff is always welcome, so long as it's well written and makes sense. If you want to request new features, that's fine too.

### Have an idea for a topic, but don't want to add it yourself?

Use this [suggestion box](http://freesuggestionbox.com/pub/dreoode) to submit full or partial scripts for Monika's topic, and it'll get written about eventually.

 ### Guide to Adding New Stuff
  You'll need the Ren'Py SDK available [here](https://www.renpy.org/latest.html). Point the project directory to this root folder (you should see Monika After Story available in the Ren'Py launcher).

 The unpacked images and .rpy files in "Monika After Story"/game/ are what Ren'Py uses to launch the project, so any changes you make have to go there to work.
 The original scripts and images are unpackaged can be found in the folders called original_scripts/ and original_images/ for you to refer to if you're stuck.

Quick list of important scripts:
script.rpy is where the script starts
script-ch30.rpy is the script for Monika's room
script-topics.rpy is where Monika's conversation topics are
screens.rpy handles the game menus.
splash.rpy handles the splash screens (if you want a pop-up dialogue box or something)

If you just want to add more edgy dialogue for Monika in the infinite loop, go to script-topics.rpy
Use one of the other topics as a template
Then go to the end of the file and add it in.

Example new dialogue code block:
```
init python:
    #This is a list of keywords for this topic
    for key in ['my','key','words']:
        monika_topics[key] = 'monika_example' #id
    if not (persistent.monika_random_built) : persistent.monika_random_topics.append('monika_example')

label monika_example:
    m "This is an example topic."
    m "I feel like this doesn't actually belong here..."
    m "Why would somebody just add the example template directly into the mod?"
    m "They really shouldn't be allowed to contribute to this repository anymore."
    return
```

For things more complicated than adding in dialogue, consult Ren'Py tutorials.
