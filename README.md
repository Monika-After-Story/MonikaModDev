![Monika After Story](https://github.com/Backdash/MonikaModDev/blob/master/Monika%20After%20Story/game/mod_assets/menu_new.png?raw=True)

# Monika After Story (MAS)
Monika After Story is a mod for the free game [Doki Doki Literature Club](https://www.ddlc.moe) from [Team Salvato](http://teamsalvato.com/). MAS builds on Act 3 to create a simulator of your eternal life with Monika, featuring new events, handlers, and metacommentary!

Please check the [Releases](http://www.monikaafterstory.com/releases.html) page for the latest stable build.

If you would like to make your own mod like this one, check out our sister project: the [DDLCModTemplate](https://github.com/therationalpi/DDLCModTemplate).

### Installation

Video tutorial on install MAS: https://youtu.be/eH5Q4Xdlg6Y

* Navigate to the [releases page](http://www.monikaafterstory.com/releases.html).

* Click the latest version link. This will download a zip file to your system.

* Extract the contents the zip file into the `/game` folder of your DDLC installation.

* Running DDLC will now load the Monika After Story Mod.

*NOTE: Source files and files downloaded directed from the repository are for development purposes and may not behave as expected if used to mod the game. Please only use one of our [Release Versions](https://github.com/Backdash/MonikaModDev/releases).*

For more help with installation, please see our [Frequently Asked Questions](https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ)

### Features

* Spend forever with Monika!

* Dozens of new conversation topics

* You can now talk to Monika to tell her what you'd like to talk about

### Upcoming Features

* New games and activities to do with Monika

* More unique events and story


## Contributing to Monika After Story

### Bugs & Suggestions
If there are issues with MAS, please file a [bug report](https://github.com/Backdash/MonikaModDev/issues/new?labels=bug&body=Describe%20bug%20and%20steps%20for%20reproduction%20here&title=%5BBug%5D%20-%20).

To add a suggestion, visit [this link](https://github.com/Backdash/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=%5BSuggestion%5D%20-%20)

 ### Other Help
 Want to help with MAS? Navigate to the [issues page](https://github.com/Backdash/MonikaModDev/issues) to find current bugs or suggestions to work on.

If you have a change you'd like to submit, open a [pull request](https://github.com/Backdash/MonikaModDev/pulls). Any changes made will be reviewed by contributors & fixed/added on to as needed.

#### Adding Content
Want to add some content to MAS? Here's a list of important .RPY files the game uses.

- **script-ch30.rpy**: Main flow for MAS. This is where idle happens.
- **script-topics.rpy**: All **random** and **pool** topics used by Monika are written here. You can add your own dialogue by checking the information below!
- **script-greetings.rpy**: Add lines for Monika to greet you when loading the game.
- **script-farewells.rpy**: Add lines for Monika to say to you when closing the game.
- **script-moods.rpy**: Tell Monika that you're in _a mood_.
- **script-stories.rpy**: Add stories for Monika to tell you.
- **script-compliments.rpy**: Add compliments you can say to Monika.
- **script-apologies.rpy**: Add things to apologize for.

If you wish to add more dialogue to the space room, navigate to script-topics.rpy and use this template.

Example new dialogue code block:
```renpy
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_example", # event label (MUST BE UNIQUE)
            category=["example", "topic"], # list of categories this topic belongs in (These are automatically capitalized)
            prompt="Example Topic", # button text
            random=True, # True if this topic should appear randomly
            pool=True # True if this topic should appear in "Ask a Question"
        )
    )

label monika_example:
    m 1a "This is an example topic."
    m 3d "I feel like this doesn't actually belong here..."
    m 2e "Why would somebody just add the example template directly into the mod?"
    m 5r "They really shouldn't be allowed to contribute to this repository anymore."
    return
```
**For full explanations and details on all the possible keywords for Event, check the documentation for Event located in `definitions.rpy`**

For things more complicated than simple dialogue, consult the Ren'Py documentation available online.

[More info is available in our Contributing Guide](https://github.com/Monika-After-Story/MonikaModDev/wiki/Contributing-Guidelines)

 ### Join the conversation
You can [follow us on twitter](https://twitter.com/MonikaAfterMod) for game updates. 

Or if you're more Discord-ly inclined, for a constant stream of our favorite Monika-related content from around the web, and if you're interested in contributing to/building this mod, feel free to join our discord server:
 
 [![Discord](https://discordapp.com/api/guilds/372766620977725441/widget.png?style=banner1)](https://discord.gg/K2KuJeX)
 
 Please be sure to follow our [Code of Conduct](https://github.com/Monika-After-Story/MonikaModDev/wiki/Code-of-Conduct), which is essentially to be courteous and respectful.

## Frequently Asked Questions

A full FAQ is available here: [Frequently Asked Questions](https://github.com/Monika-After-Story/MonikaModDev/wiki/FAQ)
For any questions about the Coding Style go here: [Coding Style](https://github.com/Monika-After-Story/MonikaModDev/wiki/Coding-Style)
For Bug Testing: [Testing Flow and Bug Testing](https://github.com/Monika-After-Story/MonikaModDev/wiki/Testing-Flow-and-Bug-Testing)
Troubleshooting: [Troubleshooting](https://github.com/Monika-After-Story/MonikaModDev/wiki/Troubleshooting) Dialogue Coding: [Dialogue Coding](https://github.com/Monika-After-Story/MonikaModDev/wiki/Dialogue-Coding)
## License info

We do our best to conform to Team Salvato's [guidelines for fan works](http://teamsalvato.com/ip-guidelines/). All characters and original content are property of Team Salvato. Monika After Story is an open source project, and in addition to named contributors, this mod includes contributions from anonymous users of 4chan, where this project got its start. More info can be found on our [License Page](https://github.com/Monika-After-Story/MonikaModDev/wiki/License-and-Team-Salvato-Guidelines).

## Build Status:
### master: ![master](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=master)
### content: ![content](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=content)
### unstable: ![unstable](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=unstable)
### alpha: ![alpha](https://github.com/Monika-After-Story/MonikaModDev/workflows/CI/badge.svg?branch=alpha)
