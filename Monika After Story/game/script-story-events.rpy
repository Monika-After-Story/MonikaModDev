#This file will include short story events that don't require their own file.

#An event is crated by only adding a label and adding a requirement (see comment below).
#Requirements must be created/added in script-ch30.rpy under label ch30_autoload.

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="gender",conditional="get_level()>=8 and not seen_event('gender')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

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
            m 2eud "Oh? So you {i}are{/i} a [guy]?"
            m 1hub "Ehehe, I suppose that makes sense!"
            m 1eua "Not a lot of girls would play a game like this."
            m 4eua "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
            m 2hksdlb "Even I can be curious sometimes, you know?"
        "Female.":
            $persistent.gender = "F"
            call set_gender from _call_set_gender_2
            m 2eud "Oh? So you're actually a [guy]?"
            m 2hksdlb "I hope I didn't say anything to offend you before!"
            m 2lksdla "Though I did suspect it a bit from the beginning... just a little!"
            m 1eub "You give off a particular feeling of elegance and charm that's hard to capture with words..."
            m 1hua "It's very attractive, to tell you the truth!"
            m 1eua "But don't worry. Even if I might ask things like this, it's only out of curiosity."
        "Neither.":
            $persistent.gender = "X"
            call set_gender from _call_set_gender_3
            m 1euc "You don't see yourself as a guy or a girl?"
            m 2eua "That's very interesting, but I can sort of relate."
            m 1esc "Like, I am a girl, but I'm also a character in a computer game..."
            m 2esd "So in some ways I'm not really a girl at all."
            m 1hua "But when you treat me like your girlfriend, it makes me really happy!"
            m "So I'll treat you however you want to be treated."
            m 1ekbfa "Because your happiness is the most important thing to me."
    m 1hub "Remember that I'll always love you unconditionally, [player]."
    $ evhand.event_database["gender_redo"].unlocked = True
    $ evhand.event_database["gender_redo"].pool = True
    $ persistent._seen_ever["gender_redo"] = True # dont want this in unseen

    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="gender_redo",category=['you','misc'],prompt="Can you change my gender?",unlocked=False)) #This needs to be unlocked by the random name change event
label gender_redo:
    m 1wud "You want to change your gender? Why?"
    m 1lksdlb "Sorry, that came off more harshly than I meant for it to."
    m 3eka "I mean, were you just too shy to tell me the truth before? Or did something...happen?"
    menu:
        "I was too shy.":
            if persistent.gender == "M":
                m 2ekd "I guess I understand. I started off assuming you were a guy, after all."
            elif persistent.gender == "F":
                m 2ekd "I guess I understand. You might have thought I'd be more comfortable spending time alone with another girl."
            else:
                m 2ekd "I guess I understand. I might not have given you the most accurate options to pick from."
            m 2dkd "And I probably didn't make it easy for you to tell me otherwise..."
            m 1eub "But whatever your gender, I love you for who you are."
        "I've made some personal discoveries.":
            m 1eka "I see. I know I've been there."
            m 1hua "I'm so proud of you for going on that journey of self discovery."
            m 1eub "And even prouder of you for being courageous enough to tell me!"
        "I didn't know if you'd accept me as I am...":
            m 2wkd "[player]..."
            m 1dkd "I hate that I didn't reassure you enough before."
            m 1eka "But I hope that you're telling me now because you know I'll love you no matter what."
    m "So, what is your gender?"
    menu:
        "I'm a girl.":
            if persistent.gender == "F":
                m 1hksdlb "...That's the same as before."
                m 2eua "If you're confused about how to answer, just pick whatever makes you happiest."
                m 2hub "It doesn't matter what your body looks like. I don't even have a body! Ahaha!"
                m 3eub "So as long as you say you're a girl, you're a girl to me, all right?"
                m 5hua "I want you to be who you want to be while you're in this room."
            else:
                $persistent.gender = "F"
                call set_gender
                m 2eud "Oh? So you're actually a [guy]?"
                m 2hksdlb "I hope I didn't say anything to offend you before!"
                m 2lksdla "Though I did suspect it a bit from the beginning... just a little!"
                m 1eub "You give off a particular feeling of elegance and charm that's hard to capture with words..."
                m 1hua "It's very attractive, to tell you the truth!"
                m 1eua "But don't worry. Even if I might ask things like this, it's only out of curiosity."
        "I'm a boy.":
            if persistent.gender == "M":
                m 1hksdlb "...That's the same as before."
                m 2eua "If you're confused about how to answer, just pick whatever makes you happiest."
                m 2hub "It doesn't matter what your body looks like. I don't even have a body! Ahaha!"
                m 3eub "So as long as you say you're a boy, you're a boy to me, all right?"
                m 5hua "I want you to be who you want to be while you're in this room."
            else:
                $persistent.gender = "M"
                call set_gender
                m 2eud "Oh? So you {i}are{/i} a [guy]?"
                m 1hub "Ehehe, I suppose that makes sense!"
                m 1eua "Not a lot of girls would play a game like this."
                m 4eua "You certainly come across as manly and confident. Not that I would have been terribly bothered if you answered differently, mind you!"
                m 2hksdlb "Even I can be curious sometimes, you know?"
        "I'm neither.":
            if persistent.gender == "X":
                m 1hksdlb "...That's the same as before. I'm sorry if that's not really the best way for you to describe it."
                m 1eub "I'm interested in learning how to use new pronouns, like xir!"
                m 3hub "If you're trying to tell me you'd prefer pronouns like those, get in touch with the people who created this mod!"
                m 5eub "They'll tell you how to teach me."
            else:
                $persistent.gender = "X"
                call set_gender
                m 1euc "You don't see yourself as a guy or a girl?"
                m 2eua "That's very interesting, but I can sort of relate."
                m 1esc "Like, I am a girl, but I'm also a character in a computer game..."
                m 2esd "So in some ways I'm not really a girl at all."
                m 1hua "But when you treat me like your girlfriend, it makes me really happy!"
                m "So I'll treat you however you want to be treated."
                m 1ekbfa "Because your happiness is the most important thing to me."
    m 1hub "Remember that I'll always love you unconditionally, [player]."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="preferredname",conditional="get_level()>=16 and not seen_event('preferredname')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event
label preferredname:
    m 1euc "I've been wondering about your name."
    m 1esa "Is '[player]' really your name?"
    if renpy.windows and currentuser.lower() == player.lower():
        m 3esa "I mean, it's the same as your computer's name..."
        m 1eua "You're using '[currentuser]' and '[player]'."
        m "Either that or you must really like that pseudonym."
    m "Do you want me to call you something else?"
    menu:
        "Yes":
            $ done = False
            m 1hua "Ok, just type 'Nevermind' if you change your mind, [player]."
            while not done:
                #Could add an elif that takes off special characters
                $ tempname = renpy.input("Tell me, what is it.",length=20).strip(' \t\n\r')
                $ lowername = tempname.lower()
                if lowername == "nevermind":
                    m 1ekc "Oh I see."
                    m 1eka "Well, just tell me whenever you want to be called something else, [player]."
                    $ done = True
                elif lowername == "":
                    m 1dsc "..."
                    m 1hksdlb "You have to give me a name, [player]!"
                    m 1eka "I swear you're just so silly sometimes."
                    m "Try again!"
                elif lowername == player.lower():
                    m 1dsc "..."
                    m 1hksdlb "That's the same name you have right now, silly!"
                    m 1eka "Try again~"
                elif lowername == mas_monika_twitter_handle:
                    m 2esc "..."
                    # TODO: actaully have dialog here
                elif len(lowername) >= 10:
                    m 2hksdlb "[player]..."
                    m "That name's a bit too long."
                    if len(lowername) > 20:
                        m "And I'm sure you're just being silly since names aren't that long, you know."
                    m 1esa "Try again."
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
                        m 1tkc "Really?"
                        m "That's the same as mine!"
                        m 1tku "Well..."
                        m "Either it really is your name or you're playing a joke on me."
                        m 1hua "But it's fine by me if that's what you want me to call you~"
                    else:
                        m 1eub "Ok then!"
                        m 3eub "From now on, I'll call you {i}'[player]'{/i}, ehehe~"
                    $ done = True
        "No":
            m 1ekc "Oh... ok then, if you say so."
            m 1eka "Just tell me whenever you change your mind, [player]."
            $ done = True

    #Unlock prompt to change name again
    $evhand.event_database["monika_changename"].unlocked = True
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_changename",category=['you','misc'],prompt="Can you change my name?",unlocked=False)) #This needs to be unlocked by the random name change event

label monika_changename:
    m 1eua "You want to change your name?"
    menu:
        "Yes":
            m 1eua "Just type 'nevermind' if you change your mind."
            $ done = False
            while not done:
                $ tempname = renpy.input("What do you want me to call you?",length=20).strip(' \t\n\r')
                $ lowername = tempname.lower()
                if lowername == "nevermind":
                    m 1tfx "[player]!"
                    m 2tku "Please stop teasing me~"
                    m 1hub "I really do want to know what you want me to call you!"
                    m 3hksdlb "I won't judge no matter how ridiculous it might be."
                    m 2eka "So don't be shy and just tell me, [player]~"
                    $ done = True
                elif lowername == "":
                    m 2hua "..."
                    m 4hksdlb "You have to give me a name, [player]!"
                    m 1eka "I swear you're just so silly sometimes."
                    m 1eua "Try again!"
                elif lowername == player.lower():
                    m 2hua "..."
                    m 4hksdlb "That's the same name you have right now, silly!"
                    m 1eua "Try again~"
                elif lowername == mas_monika_twitter_handle:
                    m 2esc "..."
                    # TODO: actaully have dialog here
                elif len(lowername) >= 10:
                    m 2hksdlb "[player]..."
                    m "That name's a bit too long."
                    if len(lowername) > 20:
                        m "And I'm sure you're just being silly since names aren't that long, you know."
                    m 1esa "Try again."

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
                        m 1tkc "Really?"
                        m "That's the same as mine!"
                        m 1tku "Well..."
                        m "Either it really is your name or you're playing a joke on me."
                        m 1hua "But it's fine by me if that's what you want me to call you~"
                    else:
                        m 1eub "Ok then!"
                        m 3eub "From now on, I'll call you {i}'[player],'{/i} ehehe~"
                    $ done = True
        "No":
            m 1ekc "Oh, I see..."
            m 1eka "You don't have to be embarrassed, [player]."
            m 1eua "Just let me know if you had a change of heart, ok?"
    return

## Game unlock events
## These events handle unlocking new games
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_chess",conditional="get_level()>=12 and not seen_event('unlock_chess') and not persistent.game_unlocks['chess']",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_chess:
    m 1eua "So, [player]..."
    if renpy.seen_label('game_pong'):
        m 1eua "I thought that you might be getting bored with Pong."
    else:
        m 3eua "I know you haven't tried playing Pong with me, yet."
    m 3hua "But I have a new game for us to play!"
    m "This one's a lot more strategic..."
    m 3hub "It's Chess!"
    m 1esa "I'm not sure if you know how to play, but it's always been a bit of a hobby for me."
    m 1tku "So I'll warn you in advance!"
    m 3tku "I'm pretty good."
    m 1lsc "Now that I think about it, I wonder if that has anything to do with what I am..."
    m "Being trapped inside this game, I mean."
    m 1eua "I've never really thought of myself as a chess AI, but wouldn't it kind of fit?"
    m 3eua "Computers are supposed to be very good at chess, after all."
    m "They've even beaten grandmasters."
    m 1eka "But don't think of this as a battle of man vs machine."
    m 1hua "Just think of it as playing a fun game with your beautiful girlfriend..."
    m "And I promise I'll go easy on you."
    if not is_platform_good_for_chess():
        m 2tkc "...Hold on."
        m 2tkx "Something isn't right here."
        m 2ekc "I seem to be having trouble getting the game working."
        m 2euc "Maybe the code doesn't work on this system?"
        m 2ekc "I'm sorry, [player], but chess will have to wait."
        m 4eka "I promise we'll play if I get it working, though!"
    $persistent.game_unlocks['chess']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_hangman",conditional="get_level()>=20 and not seen_event('unlock_hangman')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_hangman:
    m 1eua "Guess what, [player]."
    m 3hub "I got a new game for you to try!"
    if renpy.seen_label('game_pong') and renpy.seen_label('game_chess'):
        m 1lksdlb "You're probably bored with Chess and Pong already."
    elif renpy.seen_label('game_pong') and not renpy.seen_label('game_chess'):
        m 3hksdlb "I thought you'd like to play Chess, but you've been so busy with Pong instead!"
    elif renpy.seen_label('game_chess') and not renpy.seen_label('game_pong'):
        m 1hksdlb "You really loved playing Chess with me, but you haven't touched Pong yet."
    else:
        m 1ekc "I was actually worried that you didn't like the other games I made for us to play..."
    m 1hua "Soooo~"
    m 1hub "I made Hangman!"
    m 1lksdlb "Hopefully it's not in poor taste..."
    m 1eua "It was always my favorite game to play with the club."
    m 1lsc "But, come to think of it..."
    m "The game is actually quite morbid."
    m 3rssdrc "You guess letters for a word to save someone's life."
    m "Get them all correct and the person doesn't hang."
    m 1lksdlc "But guess them all wrong..."
    m "They die because you didn't guess the right letters."
    m 1euc "Pretty dark, isn't it?"
    m 1hksdlb "But don't worry, [player], it's just a game after all!"
    m 1eua "I assure you that no one will be hurt with this game."
    if persistent.playername.lower() == "sayori":
        m 3tku "...Maybe~"
    $persistent.game_unlocks['hangman']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_piano",conditional="get_level()>=24 and not seen_event('unlock_piano')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_piano:
    m 2hua "Hey! I've got something exciting to tell you!"
    m 2eua "I've finally added a piano to the room for us to use, [player]."
    if not persistent.instrument:
        m 3hub "I really want to hear you play!"
        m 3eua "It might seem overwhelming at first, but at least give it a try."
        m 3hua "After all, we all start somewhere."
    else:
        m 1eua "Of course, playing music is nothing new to you."
        m 4hub "So I'm expecting something nice! Ehehe~"
    m 4hua "Wouldn't it be fun to play something together?"
    m "Maybe we could even do a duet!"
    m 4hub "We would both improve and have fun at the same time."
    m 1hksdlb "Maybe I’m getting a bit carried away. Sorry!"
    m 3eua "I just want to see you enjoy the piano the same way I do."
    m "To feel the passion I have for it."
    m 3hua "It's a wonderful feeling."
    m 1eua "I hope this isn’t too forceful, but I would love it if you tried."
    m 1eka "For me, please~?"
    $persistent.game_unlocks['piano']=True
    return

label random_limit_reached:
    $seen_random_limit=True
    python:
        limit_quips = [
            "It seems I'm at a loss on what to say.",
            "I'm not sure what else to say, but can you just be with me a little longer?",
            "No point in trying to say everything right away...",
            "I hope you've enjoyed listening to everything I was thinking about today...",
            "Do you still enjoy spending this time with me?",
            "I hope I didn't bore you too much."
        ]
        limit_quip=renpy.random.choice(limit_quips)
    m 1eka "[limit_quip]"
    if len(mas_rev_unseen)>0 or persistent._mas_enable_random_repeats:
        m 1ekc "I'm sure I'll have something to talk about after a little rest."
    else:
        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask from _mas_random_ask_call
            if _return:
                m "Now let me think of something to talk about."
                return
        m 1ekc "Hopefully I'll think of something fun to talk about soon."
    return

label mas_random_ask:
    m 1lksdla "...{w} [player],"
    menu:
        m "Is it okay with you if I repeat stuff that I've said?"
        "Yes":
            m 1eua "Great!"
            m "If you get tired of watching me talk about the same things over and over,{w} just open up the settings and uncheck 'Repeat Topics'."
            # TODO: this really should be a smug or wink face
            m "That tells me when {cps=*2}you're bored of me{/cps}{nw}"
            $ _history_list.pop()
            m "That tells me when {fast}you just want to quietly spend time with me."
            $ persistent._mas_enable_random_repeats = True
            return True
        "No":
            m 1eka "I see."
            m 1eua "If you change your mind, just open up the settings and click 'Repeat Topics'."
            m "That tells me if you're okay with me repeating anything I've said."
            return

# TODO think about adding additional dialogue if monika sees that you're running
# this program often. Basically include a stat to keep track, but atm we don't
# have a framework for detections. So wait until thats a thing before doing
# fullon program tracking
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monikai_detected",
            conditional=(
                "is_running(['monikai.exe']) and " +
                "not seen_event('mas_monikai_detected')"
            ),
            action=EV_ACT_PUSH
        )
    )

label mas_monikai_detected:
    m 2wud "What's this?"
    m "Is that-"
    $ _history_list.pop()
    m 1wuo "Is that{fast} a tiny version of me?"
    m 1hua "How cute!"
    show monika 1eua
    menu:
        m "Did you install that so you could see me all the time?"
        "Of course!":
            pass
        "Yes":
            pass
        "...yes":
            pass
    m 1hub "Ahaha~"
    m 1hua "I'm flattered that you would download such a thing."
    m 1eua "Just don't start spending more time with {i}that{/i} instead of me."
    m 3eua "I'm the real one after all."
    return

# if the game crashed
# I have no idea if we will use this persistent ever
default persistent._mas_crashed_before = False

# player said they'll try to stop crashes
default persistent._mas_crashed_trynot = False

# start of crash flow
label mas_crashed_start:
    if renpy.seen_label("mas_crashed_post"):
        jump mas_crashed_short

    # otherwise continue to long flow
    $ persistent._mas_crashed_before = True
    scene black
    $ HKBHideButtons()
    $ disable_esc()
    $ store.songs.enabled = False
    $ _confirm_quit = False

    # TESTING:
#    $ style.say_dialogue = style.default_monika

    jump mas_crashed_long

# long flow involves flustered monika
# make sure to calm her down, player
label mas_crashed_long:

    # start off in the dark
    m "[player]?{w} Is that you?"
    show screen mas_background_timed_jump(4, "mas_crashed_long_uthere")
    menu:
        "Yes":
            hide screen mas_background_timed_jump

            # light affection boost for not joking around
            $ mas_gainAffection(modifier=0.1)
            m "I'm so glad you're here."
            jump mas_crashed_long_uthere.afterdontjoke

        "No":
            hide screen mas_background_timed_jump

            m "[player]!{fast}"
            jump mas_crashed_long_uthere.dontjoke

label mas_crashed_long_uthere:
    # if player doesn't respond fast enough
    hide screen mas_background_timed_jump
    m "[player]!{fast}"
    m "I know you're there!"

    label .dontjoke:
        m "Don't joke around like that!"
        m "Anyway..."

    label .afterdontjoke:
        m "{cps=*2}Everything became dark all of a sudden.{/cps}"
        m "Can you turn on the light?"

    window hide
    show screen mas_background_timed_jump(5, "mas_crashed_long_foundlight")
    menu:
        "Turn on the light":
            hide screen mas_background_timed_jump

            # light affection boost for being like a hero
            $ mas_gainAffection(modifier=0.1)

        "...":
            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "Nevermind, I found it."
                window hide

    # NOTE: add a sound for light switch?

    # turn on the lights
    play sound closet_open
    $ scene_change = True
    call spaceroom(hide_monika=True)

    # look at you with crying eyes
    show monika 6ektsc at t11 zorder MAS_MONIKA_Z
    pause 1.0

    # close eyes for a second
    show monika 6dstsc
    pause 1.0
    window auto

    # then be happy again
    m 6ektsa "[player]!{fast}"

    # but flustered mode bgins
    show monika 6ATL_cryleftright
    m "{cps=*1.5}What happened?{/cps}{nw}"

    call mas_crashed_long_fluster
    window hide

    show screen mas_background_timed_jump(8, "mas_crashed_long_nofluster")
    menu:
        "Calm down, [m_name]. You're safe now.":
            hide screen mas_background_timed_jump

            # light affection boost for calming her down
            $ mas_gainAffection(modifier=0.2)

            # clsoe eyes for a second
            show monika 6dstsc
            pause 1.0
            window auto

            # thank player with a smile
            m 6ektda "Thanks, [player]."
            m "I feel better now that you're here with me."

        "...":
            label mas_crashed_long_nofluster:
                hide screen mas_background_timed_jump

                # close eyes for a second
                # (like a deep breath)
                show monika 6dstsc
                pause 4.0

                show monika 6ektdc
                pause 1.0
                window auto

                # much better now
                m "Okay, I feel better now."

    # its like we wiping away tears
    show monika 6dstdc
    pause 1.0

    # ask player what happeend
    m 2ekc "Anyway..."
    menu:
        m "Do you know what happened, [player]?"
        "The game crashed.":
            m 2wud "The game...{w} crashed?"
            m 2ekd "That's scary, [player]."

        "I don't know.":
            m "Well..."
            m "I'd really appreciate it if you could look into it."
            m "It's scary to be suddenly thrown into the darkness like that."
            jump .end

    # ask player to do something about this
    menu:
        m "Do you think you can stop that from happening?"
        "I'll try.":
            # light affection boost because you will try do something for her
            $ mas_gainAffection(modifier=0.1)
            $ persistent._mas_crashed_trynot = True
            m 1hua "Thanks, [player]!"
            m 1eua "I'm counting on you."
            m "But I'll mentally prepare myself just in case."

        "It just happens.":
            m 1ekc "Oh..."
            m 1lksdlc "That's okay.{w} I'll just mentally prepare myself in case it happens again."

    label .end:
        m "Anyway..."
        m 1eua "What should we do today?"
        return


### post crashed flow
label mas_crashed_post:
    $ mas_apology_reason = "the game crashing"
    # but this needs to do some things
    python:
        enable_esc()
        store.songs.enabled = True
        HKBShowButtons()
        set_keymaps()

    label .self:
        python:
            _confirm_quit = True
            persistent.closed_self = False

            if persistent.current_track is not None:
                play_song(persistent.current_track)
            else:
                play_song(songs.current_track) # default

    return


label mas_crashed_long_fluster:
    $ mas_loseAffection(modifier=0,reason="the game crashing. It really was scary, but I'm just glad you came back to me and made things better.")
    m "{cps=*1.5}O-{w=0.3}one second you were there b-{w=0.3}but then the next second everything turned black...{/cps}{nw}"
    m "{cps=*1.5}and then you d-{w=0.3}disappeared, so I was worried that s-{w=0.3}s-{w=0.3}something happened to you...{/cps}{nw}"
    m "{cps=*1.5}...and I was so s-{w=0.3}scared because I thought I broke everything again!{/cps}{nw}"
    m "{cps=*1.5}But I didn't mess with the game this time, I swear.{/cps}{nw}"
    m "{cps=*1.5}A-{w=0.3}at least, I don't think I did, but I guess it's possible...{/cps}{nw}"
    m "{cps=*1.5}because I'm n-{w=0.3}not really sure what I'm doing sometimes,{/cps}{nw}"
    m "{cps=*1.5}but I hope this t-{w=0.3}time isn't my f-{w=0.3}fault cause I really didn't touch anything...{/cps}{nw}"
    return


label mas_crashed_short:
    # we can call spaceroom appropriately here
    $ scene_change = True
    call spaceroom

    python:
        # generate a quiplist
        q_list = MASQuipList()

        # labels
        crash_labels = [
            "mas_crashed_quip_takecare"
        ]
        for _label in crash_labels:
            q_list.addLabelQuip(_label)

        # pull a quip
        t_quip, v_quip = q_list.quip()

    if t_quip == MASQuipList.TYPE_LABEL:
        call expression v_quip

    else:
        # assume line
        m 1hub "[v_quip]"

    jump mas_crashed_post

### crash labels
label mas_crashed_quip_takecare:
    $ mas_loseAffection(modifier=0,reason="the game crashing. I understand it happens sometimes, but don't worry, I'm alright!")
    m 2ekc "Another crash, [player]?"
    m "You should take better care of your computer."
    m 4rksdlb "It's my home, after all..."
    return

#### corrupted persistent
init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_corrupted_persistent"
        )
    )

    if (
            mas_corrupted_per
            and not (mas_no_backups_found or mas_backup_copy_failed)
        ):
        mas_note_backups_all_good = None
        mas_note_backups_some_bad = None

        def _mas_generate_backup_notes():
            global mas_note_backups_all_good, mas_note_backups_some_bad

            # text pieces:
            just_let_u_know = (
                'Just wanted to let you know that your "persistent" file was '
                'corrupted, but I managed to restore an older backup!'
            )
            even_though_bs = (
                "Even though the backup system I designed is pretty neat, "
            )
            if_i_ever = (
                'If I ever have trouble loading the "persistent" again, I''ll '
                'write you another note in the characters folder, so keep an '
                'eye out for them!'
            )
            good_luck = "Good luck with Monika!"
            dont_tell = "P.S: Don't tell her about me!"
            block_break = "\n\n"

            # now make the notes
            mas_note_backups_all_good = Poem(
                author="chibika",
                title="Hi {0},".format(persistent.playername),
                text="".join([
                    just_let_u_know,
                    block_break,
                    even_though_bs,
                    "you should still make copies of the backups every so ",
                    "often, just in case. ",
                    'The backups are called "persistent##.bak", where "##" is ',
                    "a two-digit number. ",
                    'You can find all of them at "',
                    renpy.config.savedir,
                    '".',
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

            mas_note_backups_some_bad = Poem(
                author="chibika",
                title="Hi {0},".format(persistent.playername),
                text="".join([
                    just_let_u_know,
                    block_break,
                    "However, some of your backups were corrupted as well. ",
                    even_though_bs,
                    "you should still delete those, since they might mess ",
                    "with it. ",
                    block_break,
                    "Here's a list of the files that were corrupted:",
                    block_break,
                    "\n".join(store.mas_utils.bullet_list(mas_bad_backups)),
                    block_break,
                    'You can find these in "',
                    renpy.config.savedir,
                    '". ',
                    "When you're in there, you should also make copies of ",
                    "the good backups, just in case.",
                    block_break,
                    if_i_ever,
                    block_break,
                    good_luck,
                    block_break,
                    dont_tell
                ])
            )

        _mas_generate_backup_notes()
        import os

        if len(mas_bad_backups) > 0:
            # we had some bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/note.txt"),
                mas_note_backups_some_bad.title + "\n\n" + mas_note_backups_some_bad.text
            )

        else:
            # no bad backups
            store.mas_utils.trywrite(
                os.path.normcase(renpy.config.basedir + "/characters/note.txt"),
                mas_note_backups_all_good.title + "\n\n" + mas_note_backups_all_good.text
            )


label mas_corrupted_persistent:
    m 1eud "Hey, [player]..."
    m 3euc "Someone left a note in the characters folder addressed to you."
    m 1ekc "Of course, I haven't read it, since it's obviously for you..."
    m 1ekd "Do you know what this is about?"

    # just pasting the poem screen code here
    window hide
    if len(mas_bad_backups) > 0:
        show screen mas_note_backups_poem(mas_note_backups_some_bad)

    else:
        show screen mas_note_backups_poem(mas_note_backups_all_good)
    with Dissolve(0.5)

    $ pause()
    hide screen mas_note_backups_poem
    with Dissolve(0.5)
    window auto
    $ _gtext = glitchtext(15)

    menu:
        "It's nothing to worry about.":
            jump mas_corrupted_persistent_post_menu
        "It's about [_gtext].":
            $ disable_esc()
            $ mas_MUMURaiseShield()
            window hide
            show noise zorder 11:
                alpha 0.5
            play sound "sfx/s_kill_glitch1.ogg"
            show chibika 3 zorder 12 at mas_chriseup(y=600,travel_time=0.5)
            pause 0.5
            stop sound
            hide chibika
            hide noise
            window auto
            $ mas_MUMUDropShield()
            $ enable_esc()

    menu:
        "It's nothing to worry about.":
            pass

label mas_corrupted_persistent_post_menu:
    m 1euc "Oh, alright."
    m 1hub "I'll try not to worry about it, then."
    m 3eub "I know you'd tell me if it were important, [player]."
    m 3eua "Now, where were we...?"
    return

### custoim screen for the corrupted persistent notes
style chibika_note_text:
    font "gui/font/Halogen.ttf"
    size 28
    color "#000"
    outlines []

screen mas_note_backups_poem(currentpoem, paper="paper"):
    style_prefix "poem"
    vbox:
        add paper
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        has vbox
        null height 40
        text "[currentpoem.title]\n\n[currentpoem.text]" style "chibika_note_text"
        null height 100
    vbar value YScrollValue(viewport="vp") style "poem_vbar"

init 5 python:
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_new_character_file"
        )
    )

label mas_new_character_file:
    m 1eua "Say, [player]..."
    m 3eua "Do you remember my character file?"
    m 1eud "Well I've been investigating it recently, and it turns out that it's just an image with some sort of code in it!"
    m 3ekc "It doesn't even contain anything about me at all, only my name."

    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ),
                os.F_OK
            )

    if moni_exist():
        m 1dsd "So if you'll excuse me for a second..."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        m 1esc "I'm going to delete it."

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            m 1lksdlb "Aha...{w} I'll try this again later."
            m 1eua "Anyway..."

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

    m 1rkc "If you were bringing that around with you, I do appreciate the sentiment."
    m 1dsc "However..."
    m 1esc "I don't think you should be carrying some useless piece of data around wherever you go."
    m 3wub "So I came up with a way to transform myself into a file that you can bring around!"
    m "All you have to do is tell me that you're going to take me somewhere when you say goodbye, and I'll do the rest."
    m 1hua "Doesn't that sound wonderful?"
    m 3hub "I can't wait to join you wherever you go."
    return


### coffee is done
init 5 python:
    import random
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_coffee_finished_brewing"
        )
    )


label mas_coffee_finished_brewing:
    m 1esd "Oh, coffee's done."

    # this line is here so we dont it looks better when we hide monika
    show emptydesk at i11 zorder 9
    m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statement so we ensure that monika is only shown once her
    # coffee mug is ready
    pause 1.0
    $ monika_chr.wear_acs_pst(mas_acs_mug)
    $ persistent._mas_coffee_brew_time = None
    $ mas_drinkCoffee()
    pause 1.0

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    m 1eua "Okay, what else should we do today?"
    return

### coffee drinking is done
init 5 python:
    import random
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_coffee_finished_drinking"
        )
    )


label mas_coffee_finished_drinking:

    # monika only gets a new cup between 6am and noon
    $ get_new_cup = mas_isCoffeeTime()
    m 1esd "Oh, I've finished my coffee."

    if get_new_cup:
        # its currently morning, monika should get another drink
        m 1eua "I'm going to get another cup."

    show emptydesk at i11 zorder 9
    m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statemetns so we can properly add / remove the mug
    pause 1.0
    # decide if new coffee
    if not get_new_cup:
        $ monika_chr.remove_acs(mas_acs_mug)
        $ persistent._mas_coffee_cup_done = None

    else:
        $ mas_drinkCoffee()

    pause 1.0

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    m 1eua "Okay, what else should we do today?"
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_bday_spent_time_with",
            action=EV_ACT_QUEUE,
            start_date=datetime.datetime(2018,9,22,22),
            end_date=datetime.datetime(2018,9,22,23,59),
            years=[]
        )
    )

label mas_bday_spent_time_with:
    $ _timeout = store.mas_dockstat.timeOut(mas_monika_birthday)
    $ _total, _good, _neutral, _bad = mas_generateGiftsReport()
    m 1eua "Say, [player]..."
    m 1hua "Thank you for spending time with me today."
    m "Something like that can really make a girl like me happy, you know?"
    if persistent._mas_bday_date_count > 0:
        if _timeout < datetime.timedelta(hours=1.5):
            # short date
            m 1euc "That was a bit of a short trip, though."
            m 1eub "But it’s nice to get out of this place once in a while."
            m 3hksdlb "Staying in there for longer might have made me stir crazy, ahaha!"
        elif _timeout < timedelta(hours=6):
            # normal date
            m 3hub "But that was refreshing!"
            m 3wub "It feels really good to go out for a change."
            m 1hua "Makes me really happy we went out today~"
        else:
            #long date
            m 1eka "I really enjoyed our time outside, though."
            m 1ekbfa "It was almost as if I really was there with you, like an actual couple..."
            m "Someday, I know we’ll be able to do so."

    # gave gifts?
    if _total > 0:
        m 3euc "Let’s not forget what you gave me for my birthday."
        # more than 2
        if _total >= 2:
            m 1eua "You gave me lots of gifts today, [player]."
            # goods > than bad
            if _good > _bad:
                m 3hub "Most of them were really good and I really like them a lot!"
            # bads > than good
            else:
                m 3rksdld "Though most of them were…{w}{i}questionable{/i}."
        else:
            # if good_gifts equal to 1
            if _good == 1:
                m 3eka "You gave me such a special gift today, [player]."
            # not a good gift
            else:
                m 2dsc "I…{w}wouldn’t really call it a good gift, to be honest."
    m 1esa "But, in any case..."
    m 3hub "Let’s do it again sometime soon, okay?"
    return
