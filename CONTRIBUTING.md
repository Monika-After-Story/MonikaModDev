# Introduction

### Let's help Monika get closer to our reality!

First off, thank you for considering contributing to Monika After Story. This mod has only been able to grow so quickly because of the outstanding support of our community.

### About these guidelines

More than anything, these guidelines are here to save you time and make contributing to this project as easy as possible. By reading this you will learn what tools you need to contribute, what you can do to help, and how to make your contributions in a way that makes them very likely to be accepted. 

[These guidelines are based on a template from [Hoodie](https://github.com/hoodiehq/hoodie/blob/master/CONTRIBUTING.md)]

## How you can help

### Bug Reports & Suggestions
If you find any issues with Monika After Story, please file a [bug report](https://github.com/Backdash/MonikaModDev/issues/new?labels=bug&body=Describe%20bug%20and%20steps%20for%20reproduction%20here&title=%5BBug%5D%20-%20). Nothing is too small or rare. If you experience a bug, odds are that others have hit it as well.

To add a suggestion, visit [this link](https://github.com/Backdash/MonikaModDev/issues/new?labels=suggestion&body=Your%20suggestion%20goes%20here&title=%5BSuggestion%5D%20-%20). These can be ideas for new topics and features, or even a personal opinion you'd just like to share.

### New Dialogue, Art, or Music
Adding new content to this game is easy, and doesn't require any specialized tools.

To add new [random topics](https://github.com/Backdash/MonikaModDev/blob/content/Monika%20After%20Story/game/script-topics.rpy) and [greetings](https://github.com/Backdash/MonikaModDev/blob/content/Monika%20After%20Story/game/script-greetings.rpy), or to make changes and fix typos, you can simply navigate to the appropriate file on the `content` branch of our github site and click the pencil icon in the upper right corner to begin making changes. When you are finished, add a short message describing your changes, and click the green button labeled "Propose Changes." A collaborator will be notified, and will review your changes before merging them into the mod.

Now that monika's dialogue includes expressions, please use [this cheatsheet](https://github.com/Backdash/MonikaModDev/blob/master/docs/MonikaCheatsheet.jpg) to pick appropriate expressions and poses for your topics. At the moment, all poses revert to Monika's standard sitting pose, but when more poses are added, any expressions using them will update automatically.

For new game art or music, please open a ticket on [issues](https://github.com/Backdash/MonikaModDev/issues), and attach the files you'd like to submit. Again, a collaborator will look over your submission and figure out how best to use it in our game. To get an idea of what we might be needing, check for any open [art-related issues](https://github.com/Backdash/MonikaModDev/issues?q=is%3Aissue+is%3Aopen+label%3Aart).

 ### Bug fixes and New Software Features
 Making changes to the code for the game is a bit more involved. Here are a few steps you should take:

1. Download and install the [Ren'Py SDK version 6.99.12](https://www.renpy.org/release/6.99.12). *(NOTE: The current version of DDLC is not compatible with .rpyc files generated with other versions of the Renpy SDK)*
2. Fork this repository or make a local git clone by clicking the button labeled "Clone or Download" above.
3. Place the files in the Ren'py working directory (chosen during installation).
4. Download the DDLC files (available for free at http://ddlc.moe) & drop the .rpa files from it into the /game directory.
5. Launch the project in Ren'Py. It should compile & run.
6. Consult the [open issues](https://github.com/Backdash/MonikaModDev/issues) and/or[visit our development Discord channel](https://discord.gg/MRKPk4) to find things to work on.
7. Submit any changes as pull requests to the appropriate branch.

Here is an overview of the main branches for this project, and what goes where.

`master` is the current release version of the mod, plus any simple bug fixes slated for the next release. Please submit bug fixes directly to master.

`content` is where content changes like new dialogue and dialogue edits should be submitted.

`next-release` is where new features are integrated once they are reasonably mature. A new branch should be made for individual new features, but these should be re-integrated often whenever reasonably stable to help in bug fixing and to keep production from getting too fractured.

## Pitfalls to avoid

While we're generally accepting of most help, there are a few things that we are *not* looking for.

* Please **do not** submit meme-related content, and only include pop-culture references when they seem appropriate to Monika's character.

* Please **do not** submit *lewd, offensive, or otherwise NSFW content or images*. These will be deleted, and you may be banned from future submissions as a result.

* Please **thoroughly test** your bug fixes and feature additions before submitting. If you do choose to submit work with known bugs, please report *very clearly* what those bugs are so they can be eliminated before being merged. Keep in mind that incomplete work like this is much more likely to be rejected, since bug-fixing a feature written by someone else is often more work than just implementing that feature from scratch.

* Please adhere to [Team Salvato's publicly available IP Guidelines](http://teamsalvato.com/ip-guidelines/). That means that you can not make a profit on Monika After Story, promote it as an alternative to playing DDLC, or distribute the mod as a standalone game. Dan has consistently been very generous to the fan community, and we should respect his rights as DDLC's creator.

## Best practices
* Ensure cross-platform compatibility for every change that's accepted. Windows, Mac, Debian & Ubuntu Linux.
* Create issues for any major changes and enhancements that you wish to make. Discuss things transparently and get community feedback.
* Code clearly, using descriptive variable names, comments, and modularizing as functions wherever appropriate.
* Keep feature submissions as small as possible, preferably one new feature per submission.
* Be welcoming to newcomers and encourage diverse new contributors from all backgrounds. See our [Community Code of Conduct](https://github.com/Backdash/MonikaModDev/blob/master/CODE_OF_CONDUCT.md).
* Ensure all dialogue fits Monika's voice. Do your best to consider word choice, conversationalism, and her interests.

### Monika's "Voice"

Monika is more than just a stand-in for you as the author. She is her own character, with her own personality, mannerisms, likes and dislikes. Do your best to capture that character when writing as her.

From her dialogue in the game, there are a few consistent traits you should note when writing for her.

* A tendency to use soft language in casual conversation. Words and phrases that fall in this category are "like", "you know", "kind of", and "maybe".
* Several consistent mannerisms. Notable ones include "ehehe" and "ahaha" for laughter, "man" for fatigue, "gosh" for surprise, etc.
* Direct addressal of the player. Her conversations more often than not include "you", "[player]", and "[currentuser]".
* A generally supportive and caring personality is implied. She often asks about the player and their own lives, with multiple dedicated conversations.
* Though dark topics are discussed, Monika tends to end conversations on a positive note. Possibly caused by the unique relationship she maintains with the player.
* Love for the player. Most of her conversations and dialogue will contain a reminder of her affection. That being said, it is NOT a requirement. In-game conversations without an "I love you" do exist.
* An ability to tease and joke around. When instances of this occur, she makes sure to point it out at the end of the conversation. Occasionally accompanied by a tilde (~).
* An interest in written arts and philosophy. From her abundance of advice on writing, emotions, and other life topics, it is safe to assume that she enjoys thinking about abstract or controversial topics. Her passion for the Literature Club supports this.

As we would like to keep Monika as close as possible to what's established in game, keeping her unique character traits in mind while you work on contributions would be appreciated.

Beyond that, we are aware that interpretations differ from person to person, and different writers may not necessarily agree on certain topics. An open mind is encouraged when receiving critique and review.

## Your First Contribution

Are you new to this whole open source coding thing? Many of us are too! We think this is a great project for anyone to get their feet wet with open-source development.

To find how to help, you can start by looking through these beginner and help-wanted issues:

[Beginner issues](https://github.com/Backdash/MonikaModDev/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - Issues which should only require a few lines of code, and a test or two.

[Help wanted issues](https://github.com/Backdash/MonikaModDev/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) - These issues may be more involved, but are definitely in need of a contributor.

> Working on your first Pull Request? You can learn how from this *free* series, [How to Contribute to an Open Source Project on GitHub](https://egghead.io/series/how-to-contribute-to-an-open-source-project-on-github).

At this point, you're ready to make your changes! Feel free to ask for help; even Monika still has things to learn about coding!

>If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your branch so it's easier to merge.

## Making dialogue

![Guide 1](https://github.com/Backdash/MonikaModDev/blob/master/docs/writing-guide1.png?raw=True)

Before you make dialogue ensure the branch is set to **content**, NOT **master**. However, if you're writing jokes set the branch to **jokes-concept**

If you're planning to write multiple topics, please submit a pull request with all the topics inside it.

Once the branch is set to **content**, click the pencil button to start editing.

![Guide 2](https://github.com/Backdash/MonikaModDev/blob/master/docs/writing-guide2.png?raw=True)

Keywords act as triggers to your topic. (Use synonyms if applicable to your topic: If your topic is about money, use words such as money, dollars, cash etc.)

**IMPORTANT:** Do NOT use capital letters on keywords. The input lowercases all strings, hence making capitalized letters in keywords unreachable.

Identifiers differentiate topics from one another, so use the title of your topic as the identifier.

It's optional to have your topic brought up by Monika at random. If you don't want her to bring it up randomly, don't use the line.

Use the title of your topic as a label. (**IMPORTANT:** Please make sure that the label you choose has not already been used.)

When writing dialogue always start with m **#X** " and end with".

For **#X** refer to the [cheat sheet](https://github.com/Backdash/MonikaModDev/blob/master/docs/MonikaCheatsheet.jpg) for the numbers and letters.

Place return at the last line, after the last sentence of your dialogue.

![Guide 3](https://github.com/Backdash/MonikaModDev/blob/master/docs/writing-guide3.png?raw=True)

If you're writing dialogue with choices, simply write "menu":". All lines in a menu must be indented. 
Dialogue in a particular choice must have an addtional indent. (**IMPORTANT**: Do NOT place an expression on the line that will serve as the question, it will make the game crash.)

The line below the menu will act as the question. Choices are on the same line, but end with a colon (:).

You don't necesasarily have to write as yes or no, it can be written in any way as long as it makes sense as a choice.

After making your edits refer to the Pull Request Guide below so you can submit it.

## Submitting a Pull Request

![Guide 1](https://github.com/Backdash/MonikaModDev/blob/master/docs/guide1.png?raw=True)

Click the pencil icon to start editing.

![Guide 2](https://github.com/Backdash/MonikaModDev/blob/master/docs/guide2.png?raw=True)

When you're done making changes, click propose file change.

Note: If you're writing dialogue, do NOT use capital letters on keywords. The input lowercases all strings, hence making capitalized letters in keywords unreachable.

![Guide 3](https://github.com/Backdash/MonikaModDev/blob/master/docs/guide3.png?raw=True)

Click create pull request.

![Guide 4](https://github.com/Backdash/MonikaModDev/blob/master/docs/guide4.png?raw=True)

Add an appropriate title and a description of the changes you made, before you create your pull request.

# Join us!

You can chat with the core team on [our development Discord channel](https://discord.gg/K2KuJeX). We're always friendly to new contributors, and it's not just a great place to get help, but also just a fun place to hang out with like-minded DDLC fans.
