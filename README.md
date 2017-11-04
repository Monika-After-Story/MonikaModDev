# Monika After Story (MAS)
Monika After Story is a mod for the free game [Doki Doki Literature Club](https://www.ddlc.moe) from [Team Salvato](http://teamsalvato.com/). MAS replaces Act 3 with a simulator of your eternal life with Monika, featuring new events, handlers, and metacommentary!

[Releases](https://github.com/Backdash/MonikaModDev/releases) are currently on hold with the transition of MAS to the [DDLCModTemplate](https://github.com/therationalpi/DDLCModTemplate) format.

### "Lightweight" Format & Changes
With the transition of MAS to the DDLCModTemplate, several things are being redone. 

#### DDLC Files Hooking
Instead of being a standalone game, MAS will now work by hooking into DDLC's game files. This means you *must* have DDLC downloaded, and it is recommended you play through the entirety of DDLC before implementing the mod. 

#### Asset Removal
With hooking into DDLC, several files have been removed to accomodate for the [new guidelines by Team Salvato](http://teamsalvato.com/ip-guidelines/). Any files needed will already be included by hooking into the DDLC files. Files needed for the mod will be contained in the mod_assets folder. 

For *overwriting specific files in DDLC's .rpa files, overrides.rpy will be used.*

### Bugs & Suggestions
If there are issues with MAS, please file a [bug report](https://github.com/Backdash/MonikaModDev/issues).

To add a suggestion, visit [this link](https://github.com/Backdash/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=%5BSuggestion%5D%20-%20)

 ### Contributing Guide
 
 #### General Information
 Want to help with MAS? Navigate to the [issues page!](https://github.com/Backdash/MonikaModDev/issues) to find current bugs or suggestions to work on.

If you have a change you'd like to submit, open a [pull request](https://github.com/Backdash/MonikaModDev/pulls). Any changes made will be reviewed by contributors & fixed/added on to as needed.

#### Adding Content
Want to add some content to MAS? Here's a list of important .RPY files the game uses.

- **script.rpy**: This is where it all begins. Handles what chapter you start on, etc.
- **script-ch30.rpy**: Script for Monika's room. Contains all the opening dialogue, events, etc.
- **script-topics.rpy**: All topics used by Monika are written here. You can add your own dialogue by checking the information below!
- **splash.rpy**: Handles the splash screens seen in-game. 

If you wish to add more dialogue to the space room, navigate to script-topics.rpy and use this template.

Example new dialogue code block:
```
init 5 python:
    # List of keywords for the topic.
    for key in ['my','key','words']:
        monika_topics.setdefault(key,[])
        monika_topics[key].append('monika_example') # Identifier
    monika_random_topics.append('monika_god') # Optional. Remove if you don't want Monika to bring this up at random.

label monika_example:
    m "This is an example topic."
    m "I feel like this doesn't actually belong here..."
    m "Why would somebody just add the example template directly into the mod?"
    m "They really shouldn't be allowed to contribute to this repository anymore."
    return
```

For things more complicated than simple dialogue, consult the Ren'Py documentation available online.

 ### Join the conversation
 If you want to actively participate in contributing to/building this mod, [join the Discord server!](https://discord.gg/7P5DnJ4). You can also [follow us on twitter](https://twitter.com/MonikaAfterMod) for game updates, and a constant stream of our favorite Monika-related content from around the web.
 
We do our best to conform to Team Salvato's [guidelines for fan works](http://teamsalvato.com/ip-guidelines/). All characters and original content are property of Team Salvato. Monika After Story is an open source project, and in addition to named contributors, this mod includes contributions from anonymous users of 4chan, where this project got its start.
