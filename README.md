# Monika After Story

This is a mod for the free game DDLC from Team Salvato, available for download [here](ddlc.moe). I don't own any part of the game.

Basically, it replaces the end of the original game with a simulator of your eternal life with Monika, featuring new events, handlers, and metacommentary. Think Love Plus meets Totono.

If you have any problems with the game, feel free to raise issues here. Pull requests for new stuff is always welcome, so long as it's well written and makes sense. If you want to request new features, that's fine too.

 ### Guide to Adding New Stuff
  You'll need the Ren'Py SDK available [here](https://www.renpy.org/latest.html). Point the project directory to this root folder (you should see Monika After Story available in the Ren'Py launcher).

 The unpacked images and .rpy files in "Monika After Story"/game/ are what Ren'Py uses to launch the project, so any changes you make have to go there to work.
 The original scripts and images are unpackaged can be found in the folders called original_scripts/ and original_images/ for you to refer to if you're stuck.

Quick list of important scripts:
script.rpy is where the script starts
script-ch30.rpy is the script for Monika's room
screens.rpy handles the game menus.
splash.rpy handles the splash screens (if you want a pop-up dialogue box or something)

If you just want to add more edgy dialogue for Monika in the infinite loop, go to script-ch30.rpy
Look for `label ch30_loop:` in script-ch30.rpy
Increase the variable number_of_dialogues by how many dialogues you're adding.
Then go to the end of the file and add it in.

Example new dialogue code block:
```python:
label ch30_50:
    m "Contribute already~"
        return
	```

For things more complicated than adding in dialogue, consult Ren'Py tutorials.