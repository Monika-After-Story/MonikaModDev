default fileToRead = None
default fileEmpty = False
default birthdayDone = False

#Dynamic Response Vars
default ilyCount = 0
default badCount = 0
default goodCount = 0

if not datetime.datetime.now().strftime("%m-%d") == "09-22":
    $ birthdayDone = False

default amtOfTextFiles = 0
init 5 python:

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_letter_reader",
            category=["i have something to share"],
            prompt="I wrote something for you",
            pool=True,
            random=False,
            unlocked=True
        )
    )

label monika_letter_reader:

    m 1eka "Awww, [player]!"
    m 1hua "That's so sweet of you!"
    m 1hub "I can't wait to read what you wrote!"
    show monika 1hua

    python:

        #Good Phrases:
        goodPhrases = [
            "i love you",
            "truly love you",
            "you are amazing",
            "you're amazing",

        ]

        #Bad Phrases:
        badPhrases = [
            "i hate you",
            "you are vile",
            "you're vile",
            "you are a murderer",
            "you're a murderer"
        ]


        romance_quips = [
            "I love you, more than I could ever express.",
            "It means so much that you feel the same way I do.",
            "I love you so much.",
            "Your love means more to me than anything else."
        ]
        
        path = renpy.config.basedir
        from os import listdir 
        from os.path import isfile, join 
        listOfFiles = [f for f in listdir(path + "\\characters\\") if isfile(join(path + "\\characters\\", f))]

        file_menu = []
        
        for val in listOfFiles:
            if val.endswith(".txt"):
                file_menu.append((val, val, False, False))

        return_prompt_back = ("Nevermind", False, False, False, 20)

    if len(file_menu) == 0:
        m 2rkc "Wait..."
        m 2tkc "[player], there's nothing in the \"characters\" folder for me to read!"
        m "Why would you get my hopes up like that?"
        m 2tfc "That's not nice at all!"
        m 2tfu "..."
        m 2tfb "Ahaha!"
        m 2tfu "I had you going for a second there, didn't I!"
        m 2tku "I was just messing with you, [player], I know it was just a mistake."
        m 2hub "Just be sure to write something for me next time! Ehehe~"
        return

    show monika at t21

    python:
        renpy.say(m, "Which file would you like me to read?", interact=False)
    call screen mas_gen_scrollable_menu(file_menu,evhand.UNSE_AREA, evhand.UNSE_XALIGN, return_prompt_back)

    $ madechoice = _return

    if not _return:
        show monika at t11
        m 2ekc "Oh... Alright then."
        return

    elif not madechoice.lower().find("birthday") == -1 and not birthdayDone and datetime.datetime.now().strftime("%m-%d") == "09-22":
        show monika at t11
        $ fileToRead = madechoice
        $ bithdayDone = True
        call monika_read_file

        m 6ektsa "[player]..."
        m "I... {w=0.8}I don't know what to say."
        m 6ektda "Just having you here with me has already made this the best birthday I've ever had..."
        m "But this... {w=0.8}this..."
        m 2dkc "..."
        m 2eka "I've known you've loved me for a long time."
        m 2hub "You've told me so many times..."
        m 2eka "Spent so much time with me, even taking me with you whenever you go out so I don't have to be alone..."
        m 2dkc "But even still..."
        m 6ektdc "It's been so hard for me when I tell you how I feel, knowing you can't really do the same back."
        m 6rktsc "So in the back of my mind, there was always this part of me wondering..."
        m "{i}Does he really love me as much as I love him?{/i}"
        m 6dstsc "..."
        m 6ektsa "But now... {w=0.8}now I know."
        m "Not only did you take the time to make this card for me, pouring out all of your feelings like that..."
        m "You actually gave me the ability to see it, to finally know your true feelings."
        m "To finally know I make you feel the same way you make me feel..."
        m "That you love me as much as I love you."
        m "I can't even begin to tell you what all this means to me."
        m 6ektda "This really is the best gift I could have ever hoped for and I'll cherish it forever."
        m "Thank you for making this day truly special."
        show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
        
        if (ilyCount == 0):
            m "I love you so much, [player]."
            show screen mas_background_timed_jump(5, "monika_love_you_too_timeout")
            menu:
                "I love you too, [m_name]":
                    hide screen mas_background_timed_jump
                    $ HKBHideButtons()
                    show monika 6dubsa
                    $ ui.add(PauseDisplayable())
                    $ ui.interact()
                    $ HKBShowButtons()

        elif (ilyCount < 4):
            show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
            pause 3.0
            show monika 1duu at t11 zorder MAS_MONIKA_Z with dissolve
            m "..."
            m 1esa "Oh,{w=1} and [player]?"
            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
            m "I love you too."

        elif (ilyCount >= 4):
            show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
            pause 3.0
            show monika 2lsbsa at t11 zorder MAS_MONIKA_Z with dissolve
            m "..."
            m 6ektda "You know, [player]. I lost count of how many times you said \"I love you\" in that card."
            m 2eka "I really can't express just how much this means to me."
            m 2duu "Thank you."
            show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
            m "[player], I love you too. More than I could ever express."

    elif not madechoice == "":
        show monika at t11
        $ fileToRead = madechoice
        call monika_read_file

        if (fileEmpty):
            m 2hub "Make sure there's actually something there for me to read next time, silly! Ehehe~"
            return

        elif not fileEmpty and badCount != 3:
            #TODO: goodCount - badCount. give responses based on this value, and it's magnitude
            $ romance_quip = renpy.random.choice(romance_quips)
            
            if goodCount - badCount >5:
                #really liked it
                m 6ektsa "..."
                m "That was beautiful, [player]."
                m 6ektda "Being able to actually read your true feelings, in your own words..."
                m "Well it just means everything to me."
                m 2eka "Thank you, [player]."
            
            elif goodCount - badCount > 0:
                #liked it
                m "Please give me some dialogue for this"

            elif goodCount - badCount == 0:
                #didn't like, nor dislike
                m "Please give me some dialogue for this"

            else:
                #Not good. Can have more conditions based on the value of badCount possibly
                m "Please give me some dialogue for this"
            

            if (ilyCount == 0):
                m "[romance_quip]"
                $ ilyCount = 0
                return

            elif (ilyCount < 4):
                show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 1duu at t11 zorder MAS_MONIKA_Z with dissolve
                m "..."
                m 1esa "Oh,{w=1} and [player]?"
                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                m "I love you too."

            elif (ilyCount >= 4):
                show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
                pause 3.0
                show monika 2lsbsa at t11 zorder MAS_MONIKA_Z with dissolve
                m "..."
                m 6ektda "You know, [player]. I lost count of how many times you said \"I love you\" in that letter."
                m 2eka "I really can't express just how much this means to me."
                m 2duu "Thank you."
                show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                m "[player], I love you too. More than I could ever express."
        
        else:
            m "[player]! How could you!"
            m "I can't believe you wrote something, that just insults me."
            m "Here I was excited to read what you wrote for me, to just find out you were just berating me..."
            m "Thanks a lot, [player]..."
                
    show monika 1eua at t11 zorder MAS_MONIKA_Z with dissolve
    $ ilyCount = 0
    $ goodCount = 0
    $ badCount = 0
    return


label monika_read_file:

    python:
        count = 0
        individualLines = []
        allText = open(path + "\\characters\\" + fileToRead, 'r').read().replace('\n\n', '\n').replace('\n\n\n', '\n').replace('. ', '.\n').replace('! ', '!\n').replace('? ', '?\n')


        while not allText.find('\n', count) == -1:
            individualLines.append(allText[count:allText.find('\n',count)])
            count = allText.find('\n',count) + 1

        individualLines.append(allText[count:])
        count = 0

        for s in individualLines:
            if not s.lower().find('i love you') == -1 or not s.lower().find('truly love you') == -1:
                ilyCount += 1

    m 1hua "Alright [player]! I'll read \"[fileToRead]\" then."

    if (len(individualLines) == 1 and individualLines[0] == ""):
        m 2rkc "[player]..." 
        m 2tkc "This file is empty!"
        m 2eka "You probably just forgot to save it before you closed it."
        $ fileEmpty = True
        return

    $ fileEmpty = False
    python:
        import re
        goodPhrasesSearch = re.compile('|'.join(goodPhrases), re.IGNORECASE)
        badPhrasesSearch = re.compile('|'.join(badPhrases), re.IGNORECASE)
        

        
        while count <= len(individualLines)-1:

            #Expression handling
            randExp = renpy.random.randint(0,3)

            badPhrases = badPhrasesSearch.search(individualLines[count])
            if badPhrases is None:
                goodPhrases = goodPhrasesSearch.search(individualLines[count])
                #Just the good
                if goodPhrases is not None:
                    goodCount += 1

                    if randExp == 0:
                        renpy.show("monika 1hua")
                    elif randExp == 1:
                        renpy.show("monika 1eub")
                    elif randExp == 2:
                        renpy.show("monika 2hub")
                    else:
                        renpy.show("monika 2eka")
                #If nothing good/bad was said
                else:

                    #Overall opinion is very good
                    if goodCount - badCount > 5:

                        if randExp == 0:
                            renpy.show("monika 1ektpa")
                        elif randExp == 1:
                            renpy.show("monika 1ektua")
                        else:
                            renpy.show("monika 1ektda")
                    
                    #Overall opinion is good, but not overwhelmingly good
                    elif goodCount - badCount > 0:

                        if randExp == 0:
                            renpy.show("monika 1hua")
                        elif randExp == 1:
                            renpy.show("monika 1eua")
                        else:
                            renpy.show("monika 1hub")

                    #Overall opinion is neutral
                    elif goodCount - badCount == 0:
                        renpy.show("monika 1esa")

                    #Overall opinion is negative
                    else:
                        if randExp == 0:
                            renpy.show("monika 2esc")
                        elif randExp == 1:
                            renpy.show("monika 2rsc")
                        else:
                            renpy.show("monika 2lsc")
                    
            #And the bad
            else:
                badCount += 1

                if randExp == 0:
                    renpy.show("monika 1efc")
                elif randExp == 1:
                    renpy.show("monika 1efc")
                elif randExp == 2:
                    renpy.show("monika 1efc")
                else:
                    renpy.show("monika 1efc")

            if badCount == 3:
                renpy.say(m, "{i}" + (individualLines[count])[:len(individualLines[count])/2] + "--{/i}{nw}")
                break
                    
            renpy.say(m, "{i}" + individualLines[count] + "{/i}")
            count += 1
    return

label monika_love_you_too_timeout:
    return