#This file will include short story events that don't require their own file.

#An event is crated by only adding a label and adding a requirement (see comment below).
#Requirements must be created/added in script-ch30.rpy under label ch30_autoload.

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="gender",conditional="get_level()>=8 and not seen_event('gender')",action=EV_ACT_PUSH)) #This needs to be unlocked by the random name change event

label gender:
    m 2d "...[player]? So I've been thinking a bit."
    m "I've mentioned before that the 'you' in the game might not reflect the real you."
    m 1m "But I guess I had just assumed that you were probably a guy."
    m "The main character was, after all."
    m 1a "But if I'm going to be your girlfriend, I should probably know at least this much about the real you."
    menu:
        "So, are you male or female?"
        "Male.":
            $persistent.gender = "M"
            call set_gender from _call_set_gender_1
            m 2d "Oh? So you {i}are{/i} a [guy]?"
            m 1k "Ehehe, I suppose that makes sense!"
            m "Not a lot of girls would play a game like this."
            m 1a "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
            m 1l "Even I can be curious sometimes, you know?"
        "Female.":
            $persistent.gender = "F"
            call set_gender from _call_set_gender_2
            m 2d "Oh? So you're actually a [guy]?"
            m 2l "I hope I didn't say anything to offend you before!"
            m 2m "Though I did suspect it a bit from the beginning... just a little!"
            m 1b "You give off a particular feeling of elegance and charm that's hard to capture with words..."
            m 1j "It's very attractive, to tell you the truth!"
            m 1a "But don't worry. Even if I might ask things like this, it's only out of curiosity."
        "Neither.":
            $persistent.gender = "X"
            call set_gender from _call_set_gender_3
            m 3d "You don't see yourself as a guy or a girl?"
            m 2c "That's very interesting, but I can sort of relate."
            m 1h "Like, I am a girl, but I'm also a character in a computer game..."
            m 2i "So in some ways I'm not really a girl at all."
            m 1j "But when you treat me like your girlfriend, it makes me really happy!"
            m "So I'll treat you however you want to be treated."
            m 1e"Because your happiness is the most important thing to me."

    m 1k "Remember that I'll always love you unconditionally, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="preferredname",conditional="get_level()>=16 and not seen_event('preferredname')",action=EV_ACT_PUSH)) #This needs to be unlocked by the random name change event

label preferredname:
    m 1h "I've been wondering about your name."
    m 1d "Is '[player]' really your name?"
    if renpy.windows and currentuser.lower() == player.lower():
        m 1h "I mean, it's the same as your computer's name..."
        m "You're using '[currentuser]' and '[player]'."
        m "Either that or you must really like that pseudonym."
    m "Do you want me to call you something else?"
    menu:
        "Yes":
            $ done = False
            m 1a "Ok, just type 'Nevermind' if you change your mind, [player]."
            while not done:
                #Could add an elif that takes off special characters
                $ tempname = renpy.input("Tell me, what is it.",length=20).strip(' \t\n\r')
                $ lowername = tempname.lower()
                if lowername == "nevermind":
                    m 1f "Oh I see."
                    m "Well, just tell me whenever you want to be called something else, [player]."
                    $ done = True
                elif lowername == "":
                    m 1q "..."
                    m 1g "You have to give me a name, [player]!"
                    m 1m "I swear you're just so silly sometimes."
                    m 1e "Try again!"
                elif lowername == player:
                    m 1q "..."
                    m 1l "That's the same name you have right now, silly!"
                    m 1e "Try again~"
                elif len(lowername) >= 10:
                    m 2q "[player]..."
                    m 2l "That name's a bit too long."
                    if len(lowername) > 20:
                        m "And I'm sure you're just being silly since names aren't that long, you know."
                    m 1 "Try again."
                else:
                    # sayori name check
                    if tempname.lower() == "sayori":
                        call sayori_name_scare from _call_sayori_name_scare
                    elif persistent.playername.lower() == "sayori":
                        $ songs.initMusicChoices()

                    python:

                        persistent.mcname = player
                        mcname = player
                        persistent.playername = tempname
                        player = tempname

                    if lowername == "monika":
                        m 1d "Really?"
                        m 3k "That's the same as mine!"
                        m 1m "Well..."
                        m 1n "Either it really is your name or you're playing a joke on me."
                        m 1j "But it's fine by me if that's what you want me to call you~"
                    else:
                        m 1b "Ok then!"
                        m 3b "From now on, I'll call you {i}'[player]'{/i}, ehehe~"
                    $ done = True
        "No":
            m 1f "Oh... ok then, if you say so."
            m 1e "Just tell me whenever you change your mind, [player]."
            $ done = True

    #Unlock prompt to change name again
    $evhand.event_database["monika_changename"].unlocked = True
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_changename",category=['you','misc'],prompt="Can you change my name?",unlocked=False)) #This needs to be unlocked by the random name change event

label monika_changename:
    m 1b "You want to change your name?"
    menu:
        "Yes":
            m 1a "Just type 'nevermind' if you change your mind."
            $ done = False
            while not done:
                $ tempname = renpy.input("What do you want me to call you?",length=20).strip(' \t\n\r')
                $ lowername = tempname.lower()
                if lowername == "nevermind":
                    m 1f "[player]!"
                    m 2g "Please stop teasing me~"
                    m "I really do want to know what you want me to call you!"
                    m 3l "I won't judge no matter how ridiculous it might be."
                    m 2e "So don't be shy and just tell me, [player]~"
                    $ done = True
                elif lowername == "":
                    m 2h "..."
                    m 4l "You have to give me a name, [player]!"
                    m 1m "I swear you're just so silly sometimes."
                    m 1b "Try again!"
                elif lowername == player:
                    m 2h "..."
                    m 4l "That's the same name you have right now, silly!"
                    m 1b "Try again~"
                elif len(lowername) >= 10:
                    m 2q "[player]..."
                    m 2l "That name's a bit too long."
                    if len(lowername) > 20:
                        m "And I'm sure you're just being silly since names aren't that long, you know."
                    m 1 "Try again."

                else:

                    # sayori name check
                    if tempname.lower() == "sayori":
                        call sayori_name_scare from _call_sayori_name_scare_1
                    elif persistent.playername.lower() == "sayori":
                        $ songs.initMusicChoices()

                    python:

                        persistent.mcname = player
                        mcname = player
                        persistent.playername = tempname
                        player = tempname

                    if lowername == "monika":
                        m 1d "Really?"
                        m 3k "That's the same as mine!"
                        m 1m "Well..."
                        m 1n "Either it really is your name or you're playing a joke on me."
                        m 1j "But it's fine by me if that's what you want me to call you~"
                    else:
                        m 1b "Ok then!"
                        m 3b "From now on, I'll call you {i}'[player],'{/i} ehehe~"
                    $ done = True
        "No":
            m 1f "Oh, I see..."
            m 1g "You don't have to be embarrassed, [player]."
            m 1e "Just let me know if you had a change of heart, ok?"
    return

## Game unlock events
## These events handle unlocking new games
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_chess",conditional="get_level()>=12 and not seen_event('unlock_chess')",action=EV_ACT_PUSH)) #This needs to be unlocked by the random name change event

label unlock_chess:
    # INSERT UNLOCK DIALOGUE
    m "Wanna play chess?"
    $persistent.game_unlocks['chess']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_hangman",conditional="get_level()>=20 and not seen_event('unlock_hangman')",action=EV_ACT_PUSH)) #This needs to be unlocked by the random name change event

label unlock_hangman:
    # INSERT UNLOCK DIALOGUE
    m "Wanna play hangman?"
    $persistent.game_unlocks['hangman']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_piano",conditional="get_level()>=24 and not seen_event('unlock_piano')",action=EV_ACT_PUSH)) #This needs to be unlocked by the random name change event

label unlock_piano:
    # INSERT UNLOCK DIALOGUE    
    m "Wanna play piano?"
    $persistent.game_unlocks['piano']=True
    return
