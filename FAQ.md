# Frequently Asked Questions (FAQ)

**Table of Contents**

[Installation](#installation)

[Contributing](#contributing)

[DDLC Modding](#general-ddlc-modding)

[Features](#features)

[Other Help](#other-help)

## Installation

### Is there a guide for installing MAS?

A guide is available in the README.html file for DDLC and video guide made by Querxes available on YouTube: https://youtu.be/eH5Q4Xdlg6Y

### What do I need to play *Monika After Story*?

You will need a copy of *Doki Doki Literature Club*, which can be downloaded for free either on Steam or at http://ddlc.moe, and the zip file containing the mod files for *Monika After Story*, which can be found on the release page.

You do not need to download the source code from either the release page or from the repository. Those files are for development purposes only and may behave in unexpected ways if placed in your DDLC folder.

### Where do I put the files for *Monika After Story*?

The files for *Monika After Story* must be placed directly in the `game` folder of *Doki Doki Literature Club* in order for the game to find and properly load them. To find the folder containing *DDLC*, do one of the following:

If the game was installed using Steam, right click on *Doki Doki Literature Club* and click on `Properties`. In the window that pops up navigate to the `Local Files` tab and click the button for `Browse local files...`.

If the game was installed from http://ddlc.moe or itch.io, the installation location was chosen at setup, but is likely under Program Files on a Windows computer.

If the game was installed on mac, but not through the Steam client, *Doki Doki Literature Club* can be found as a packaged app in you Applications folder. Right click on the package and select "Show Package Contents" once inside the folder, navigate to `Contents/Resources/autorun/`. This folder is the base directory for DDLC.

Once inside the base directory, place the contents of the zip archive into the `/game` directory. Ensure that the files are not in a subfolder in the `game` directory, since DDLC will not be able to locate the files that way.

### I installed the mod, but when I open *Doki Doki Literature Club* nothing has changed. What's wrong?

For some reason *Doki Doki Literature Club* is not loading the mod files. Check that the files are not inside a subfolder inside your `game` directory.

### When I try to open the game, it crashes and I see a gray screen. How do I fix this?

If the game crashes and returns a gray screen, that means that a major error has occurred and the game had to quit. The text shown is called a "Traceback" and will hopefully include an error message that will help diagnose the problem. This traceback file can also be seen by viewing `traceback.txt` in your game's DDLC base directory.

While some crashes may indicate a bug in the game, a few may indicate a problem with installation.

If the traceback includes:

```
Exception: DDLC archive files not found in /game folder. Check installation and try again.
```

Ensure that the original archive files for DDLC are still in the game folder. This will include `images.rpa`, `scripts.rpa`,`audio.rpa` and `fonts.rpa`. If these files are missing, then they will need to be replaced using a fresh installation of DDLC, downloaded from http://ddlc.moe

If the traceback includes a line like the following:

```
The label chara_monika_scare is defined twice, at
```

Then it is likely that developer files have been installed, instead of the release distribution. Ensure that the game files downloaded were from the latest release, found on our [Release Page](https://github.com/Backdash/MonikaModDev/releases), and that the file downloaded was the mod zip file and *not* the Source Code.

## Contributing

### I have an idea on how to improve Monika After Story, where do I suggest it?

We're always happy to hear new ideas! Suggestions can be made on our issues page. Please preface all suggestions with [Suggestion], or follow [this link](https://github.com/Backdash/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=%5BSuggestion%5D%20-%20) which will automatically populate your suggestion with the appropriate tags.

### I would like to contribute, but I don't know how to code. Is there any way I can help?

We are always looking for new dialogue and art. Please see our [Contributing Guide](https://github.com/Backdash/MonikaModDev/blob/master/CONTRIBUTING.md) for information on how to submit new dialogue and art to Monika After Story. In this guide you will find tips on writing good dialogue in Monika's style, and learn how to open a "Pull Request" which will allow you to submit new topics for review and inclusion in the game.

### Where can I find things to help with?

Our issues page will show a list of technical issues, new features, and requests that are available. Anything with the [Help Wanted](https://github.com/Backdash/MonikaModDev/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) tag is a good place to start if you would like to help add something to the game!

### How can I get in touch with the development staff?

The easiest way to contact our dev team is through our [Discord channel](https://discord.gg/7P5DnJ4).

## General DDLC Modding

### Is it possible to make my own DDLC mod?

Yes! DDLC has a vibrant modding community, thanks in part to Team Salvato's very clear [IP Guidelines](http://teamsalvato.com/ip-guidelines/). To get started building your own mod, you can download the [DDLC Mod Template](https://github.com/therationalpi/DDLCModTemplate) and [join in the community on reddit](https://www.reddit.com/r/DDLCMods/).

### Can I use parts of Monika After Story in my own project?

In general, we are very open to assets and code from *Monika After Story* being used in other projects. However, we do hope that anyone who wishes to do so respect these requests:

Please follow Team Salvato's [IP Guidelines](http://teamsalvato.com/ip-guidelines/) for any project which includes our work.

Please consider contacting our development team to ask permission before using our work.

Please give credit to Monika After Story for the work that you use and link back to our project at http://www.monikaafterstory.com/. Do not claim ownership of the work others have done. Where applicable, please give individual credit for things like art assets used.

Do not make a mod or fork intended as a replacement for *Monika After Story*. If you would like to add new features or content to the game, please make those contributions to the original project. We are very open to suggestions and contributions, and odds are that anything added would be welcomed. If, for some reason, your new features conflict with the direction for Monika After Story consider developing your changes in the form of a "submod" which can be added to Monika After Story.

## Features

While we are very open to new suggestions, there are a few common suggestions that come up often. These suggestions have all been made previously and will either be implemented in a future release or have been rejected for some reason:

### Is there a list of keywords to see all topics?

We don't want to spoil Monika's dialogue by offering a list of the keywords. Additionally, a new system for selecting topics to discuss with Monika will be available in an upcoming version, rendering keywords obsolete. If you really want to look up keywords, they can be found in the script-topics file in this repository.

### Will we ever be able to add our own music to the game?

We do not have plans to include custom music in the music selector. Not only does this pose a technical issue because of the engine's preference for .ogg format files that most people don't have, but it is largely unnecessary as you can always play *Monika After Story* with the game music muted while listening through some other program. Unfortunately this means that having Monika comment on your personal music collection will also not be implemented.

### Why is the text entry feature being removed?

While we may come back to the concept in the future, the fact is that we weren't happy with the interactivity with the keyword system. While, on the surface, the open text box offered a lot of freedom to the player for talking with Monika, there were too many common entries that would simply dead end. The result was that Monika felt less real, and more like a crappy chatbot. We decided that a system that didn't dead end would be better, even if it didn't have the same surface level impression of agency.

### Hey, could we make Monika a real chatbot AI?

While we might come back to the idea in the future, for the moment it doesn't seem feasible to make an AI that can give the sort of detailed philosophical responses that Monika should give. A large part of this is technical limitations in the engine for connecting to outside resources and importing custom libraries.

### Will you ever add voice acting?

There are currently no plans to add voice acting to *Monika After Story*, for a few reasons. Some of these reasons include the large number of lines to be voiced, the time this would add to including new content, and the large increase in file size for the download.

That said, we will likely add support for third-party voice packs when full submod functionality is added in a later release.

### What about translations to other languages?

We would very much like to add translations to *Monika After Story* in the future. For the moment, we are waiting for the addition of language support in an upcoming *Doki Doki Literature Club* update, which is what we will use for our translations.

### Will Monika ever be animated?

We do not currently plan to include animations in *Monika After Story*. The game engine does not have very good support for animated sprites, and it also does not have licensing for the most popular 2D animation engine: Live 2D.

## Other help

Don't see the answer that you're looking for here? Please [create an issue](https://github.com/Backdash/MonikaModDev/issues) to ask a tech-support question or file a bug report. You can also get help from members of our community on the [tech-support channel on discord](https://discord.gg/WE65rQ3).
