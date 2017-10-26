# Monika After Story

Monika After Story is a mod for the free game [Doki Doki Literature Club](http://ddlc.moe) from Team Salvato. This mod replaces the ending of Act 3 with a simulator of your eternal life with Monika, featuring new events, handlers, and metacommentary. Think Love Plus meets Totono.

Check the [releases page](https://github.com/Backdash/MonikaModDev/releases) for the latest build.

### Bugs, suggestions, and other feedback

If you have any problems with the game, please file a [bug report](https://github.com/Backdash/MonikaModDev/issues/new?labels=bug&body=Describe%20bug%20and%20steps%20for%20reproduction%20here&title=[Bug]%20-%20).

We are also happy to hear [your suggestions](https://github.com/Backdash/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=[Suggestion]%20-%20) for new content, features, and dialogue for future versions!

 ### Guide to Adding New Stuff

If you would like to help with this project, navigate to the [git repository for Monika After Story](https://github.com/Backdash/MonikaModDev). Check the [issues page](https://github.com/Backdash/MonikaModDev/issues) to find current projects that you can help to address or [suggest something new](https://github.com/Backdash/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=[Suggestion]%20-%20). If you have a change that you would like to submit, open a [pull request](https://github.com/Backdash/MonikaModDev/pulls) with your proposed changes, which will be tested and approved by established collaborators on the project.

Beyond coding, we can always use the talents of good writers and artists to help expand the game's content.

To help with coding, you'll need the Ren'Py SDK available [here](https://www.renpy.org/latest.html). Point the project directory to this MonikaModDev folder (you should see Monika After Story available in the Ren'Py launcher).

 The unpacked images and .rpy files in "Monika After Story"/game/ are what Ren'Py uses to launch the project, so any changes you make have to go there to work. The original scripts and images are unpackaged can be found in the folders called original_scripts/ and original_images/ for you to refer to if you're stuck.

Quick list of important scripts:
script.rpy is where the script starts, 
script-ch30.rpy is the script for Monika's room, 
script-topics.rpy is where Monika's conversation topics are, 
screens.rpy handles the game menus, and
splash.rpy handles the splash screens (if you want a pop-up dialogue box or something)

If you just want to add more edgy dialogue for Monika in the infinite loop, go to script-topics.rpy and use the following template for your new content.

Example new dialogue code block:
```
init python:
    #This is a list of keywords for this topic
    for key in ['my','key','words']:
        monika_topics.setdefault(key,[])
        monika_topics[key].append('monika_example') #id
    if not (persistent.monika_random_built) : persistent.monika_random_topics.append('monika_example')

label monika_example:
    m "This is an example topic."
    m "I feel like this doesn't actually belong here..."
    m "Why would somebody just add the example template directly into the mod?"
    m "They really shouldn't be allowed to contribute to this repository anymore."
    return
```

For things more complicated than simple dialogue, consult the Ren'Py documentation available online.

 ### Join the conversation
 
If you want to actively participate in building this mod, we now have our own Discord Server that you can join by following this link: https://discord.gg/7P5DnJ4. You can also [follow us on twitter](https://twitter.com/MonikaAfterMod) for game updates, and a constant stream of our favorite Monika-related content from around the web.

We do our best to conform to Team Salvato's [guidelines for fan works](http://teamsalvato.com/blog/ddlc-store-translations-fan-work/). All characters and original content are property of Team Salvato. Monika After Story is an open source project, and in addition to named contributors, this mod includes contributions from anonymous users of 4chan, where this project got its start.
