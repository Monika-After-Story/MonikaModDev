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
    addEvent(Event(persistent.event_database,eventlabel="preferredname",conditional="get_level()>=16 and not seen_event('preferredname')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

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
                elif lowername == player.lower():
                    m 1q "..."
                    m 1l "That's the same name you have right now, silly!"
                    m 1e "Try again~"
                elif lowername == mas_monika_twitter_handle:
                    m 2h "..."
                    # TODO: actaully have dialog here
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
                elif lowername == player.lower():
                    m 2h "..."
                    m 4l "That's the same name you have right now, silly!"
                    m 1b "Try again~"
                elif lowername == mas_monika_twitter_handle:
                    m 2h "..."
                    # TODO: actaully have dialog here
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
    addEvent(Event(persistent.event_database,eventlabel="unlock_chess",conditional="get_level()>=12 and not seen_event('unlock_chess') and not persistent.game_unlocks['chess']",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_chess:
    m 1a "So, [player]..."
    if renpy.seen_label('game_pong'):
        m 1i "I thought that you might be getting bored with Pong."
    else:
        m 3i "I know you haven't tried playing Pong with me, yet."
    m 3 "But I have a new game for us to play!"
    m 3a "This one's a lot more strategic..."
    m 3k "It's Chess!"
    m 1 "I'm not sure if you know how to play, but it's always been a bit of a hobby for me."
    m "So I'll warn you in advance!"
    m "I'm pretty good."
    m 1d "Now that I think about it, I wonder if that has anything to do with what I am..."
    m 1i "Being trapped inside this game, I mean."
    m 1 "I've never really thought of myself as a chess AI, but wouldn't it kind of fit?"
    m 3 "Computers are supposed to be very good at chess, after all."
    m "They've even beaten grandmasters."
    m 1 "But don't think of this as a battle of man vs machine."
    m 1j "Just think of it as playing a fun game with your beautiful girlfriend..."
    m "And I promise I'll go easy on you."
    if not is_platform_good_for_chess():
        m 2g "...Hold on."
        m 2f "Something isn't right here."
        m "I seem to be having trouble getting the game working."
        m 2o "Maybe the code doesn't work on this system?"
        m 2p "I'm sorry, [player], but chess will have to wait."
        m 4e "I promise we'll play if I get it working, though!"
    $persistent.game_unlocks['chess']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_hangman",conditional="get_level()>=20 and not seen_event('unlock_hangman')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_hangman:
    m 1a "Guess what, [player]."
    m 3b "I got a new game for you to try!"
    if renpy.seen_label('game_pong') and renpy.seen_label('game_chess'):
        m 1n "You're probably bored with Chess and Pong already."
    elif renpy.seen_label('game_pong') and not renpy.seen_label('game_chess'):
        m 3l "I thought you'd like to play Chess, but you've been so busy with Pong instead!"
    elif renpy.seen_label('game_chess') and not renpy.seen_label('game_pong'):
        m 1o "You really loved playing Chess with me, but you haven't touched Pong yet."
    else:
        m 1f "I was actually worried that you didn't like the other games I made for us to play..."
    m 1b "Soooo~"
    m 1k "I made Hangman!"
    m 1n "Hopefully it's not in poor taste..."
    m 1a "It was always my favorite game to play with the club."
    m 1f "But, come to think of it..."
    m 1o "The game is actually quite morbid."
    m "You guess letters for a word to save someone's life."
    m 1c "Get them all correct and the person doesn't hang."
    m 1o "But guess them all wrong..."
    m 1h "They die because you didn't guess the right letters."
    m 1m "Pretty dark, isn't it?"
    m 1l "But don't worry, [player], it's just a game after all!"
    m 1a "I assure you that no one will be hurt with this game."
    if persistent.playername.lower() == "sayori":
        m 3k "...Maybe~"
    $persistent.game_unlocks['hangman']=True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="unlock_piano",conditional="get_level()>=24 and not seen_event('unlock_piano')",action=EV_ACT_QUEUE)) #This needs to be unlocked by the random name change event

label unlock_piano:
    m 2a "Hey! I've got something exciting to tell you!"
    m 2b "I've finally added a piano to the room for us to use, [player]."
    if not persistent.instrument:
        m 3b "I really want to hear you play!"
        m "It might seem overwhelming at first, but at least give it a try."
        m 3j "After all, we all start somewhere."
    else:
        m 1b "Of course, playing music is nothing new to you."
        m 4b "So I'm expecting something nice! Ehehe~"
    m 4j "Wouldn't it be fun to play something together?"
    m "Maybe we could even do a duet!"
    m "We would both improve and have fun at the same time."
    m 1l "Maybe I’m getting a bit carried away. Sorry!"
    m 3b "I just want to see you enjoy the piano the same way I do."
    m "To feel the passion I have for it."
    m 3k "It's a wonderful feeling."
    m 1j "I hope this isn’t too forceful, but I would love it if you tried."
    m "For me, please~?"
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
    m 1m "[limit_quip]"
    if len(mas_rev_unseen)>0 or persistent._mas_enable_random_repeats:
        m 1f "I'm sure I'll have something to talk about after a little rest."
    else:
        if not renpy.seen_label("mas_random_ask"):
            call mas_random_ask from _mas_random_ask_call
            if _return:
                m "Now let me think of something to talk about."
                return
        m 1f "Hopefully I'll think of something fun to talk about soon."
    return

label mas_random_ask:
    m 1m "...{w} [player],"
    menu:
        m "Is it okay with you if I repeat stuff that I've said?"
        "Yes":
            m 1a "Great!"
            m "If you get tired of watching me talk about the same things over and over,{w} just open up the settings and uncheck 'Repeat Topics'."
            # TODO: this really should be a smug or wink face
            m "That tells me when {cps=*2}you're bored of me{/cps}{nw}"
            m "That tells me when {fast}you just want to quietly spend time with me."
            $ persistent._mas_enable_random_repeats = True
            return True
        "No":
            m 1e "I see."
            m 1a "If you change your mind, just open up the settings and click 'Repeat Topics'."
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
    m 2c "What's this?"
    m "Is that-"
    m 1b "Is that{fast} a tiny version of me?"
    m 1k "How cute!"
    show monika 1a
    menu:
        m "Did you install that so you could see me all the time?"
        "Of course!":
            pass
        "Yes":
            pass
        "...yes":
            pass
    m 1k "Ahaha~"
    m 1a "I'm flattered that you would download such a thing."
    m 3a "Just don't start spending more time with {i}that{/i} instead of me."
    m 1a "I'm the real one after all."
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

            # TODO: affection?
            m "I'm so glad you're here."
            jump mas_crashed_long_uthere.afterdontjoke

        "No":
            hide screen mas_background_timed_jump

            # TODO: affection?
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
            pass
        "...":
            pause 5.0
            label mas_crashed_long_foundlight:
                hide screen mas_background_timed_jump
                window show
                m "Nevermind, I found it."
                window hide

    # NOTE: add a sound for light switch?

    # turn on the lights
    $ scene_change = True
    call spaceroom(hide_monika=True)

    # look at you with crying eyes
    show monika 6ektsc at t11 zorder 2
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
    m 2f "Anyway..."
    menu:
        m "Do you know what happened, [player]?"
        "The game crashed.":
            m 2wud "The game...{w} crashed?"
            m 2g "That's scary, [player]."

        "I don't know.":
            m "Well..."
            m "I'd really appreciate it if you could look into it."
            m "It's scary to be suddenly thrown into the darkness like that."
            jump .end

    # ask player to do something about this
    menu:
        m "Do you think you can stop that from happening?"
        "I'll try.":
            $ persistent._mas_crashed_trynot = True
            m 1j "Thanks, [player]!"
            m 1a "I'm counting on you."
            m "But I'll mentally prepare myself just in case."

        "It just happens.":
            m 1f "Oh..."
            m 1o "That's okay.{w} I'll just mentally prepare myself in case it happens again."
            
    label .end:
        m "Anyway..."
        m 1a "What should we do today?"

### post crashed flow
label mas_crashed_post:
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
        m 1k "[v_quip]"

    jump mas_crashed_post

### crash labels
label mas_crashed_quip_takecare:
    m 2f "Another crash, [player]?"
    m "You should take better care of your computer."
    m 4n "It's my home, after all..."
    return

