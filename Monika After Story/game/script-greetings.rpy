##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup

# persistents that greetings use
default persistent._mas_you_chr = False

init -1 python in mas_greetings:
    # custom greeting functions
    def selectGreeting():
        """
        Selects a greeting to be used. This evaluates rules and stuff
        appropriately.

        RETURNS:
            a single greeting (as an Event) that we want to use
        """

        # filter events by their unlocked property first
        unlocked_greetings = renpy.store.Event.filterEvents(
            renpy.store.evhand.greeting_database, 
            unlocked=True
        )

        # filter greetings using the special rules dict
        random_greetings_dict = renpy.store.Event.checkRepeatRules(
            unlocked_greetings
        )

        # check if we have a greeting that actually should be shown now
        if len(random_greetings_dict) > 0:

            # select one label randomly
            return random_greetings_dict[
                renpy.random.choice(random_greetings_dict.keys())
            ]

        # since we don't have special greetings for this time we now check for special random chance
        # pick a greeting filtering by special random chance rule
        random_greetings_dict = renpy.store.Event.checkGreetingRules(
            unlocked_greetings
        )

        # check if we have a greeting that actually should be shown now
        if len(random_greetings_dict) > 0:

            # select on label randomly
            return random_greetings_dict[
                renpy.random.choice(random_greetings_dict.keys())
            ]

        # We couldn't find a suitable greeting we have to default to normal random selection
        # filter random events normally
        random_greetings_dict = renpy.store.Event.filterEvents(
            unlocked_greetings, 
            random=True
        )

        # select one randomly
        return random_greetings_dict[
            renpy.random.choice(random_greetings_dict.keys())
        ]


init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_sweetheart", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_sweetheart:
    m 1k "Hello again, sweetheart!"
    m 1l "It's kind of embarrassing to say out loud, isn't it?"
    m 3b "Still, I think it's okay to be embarrassed every now and then."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_honey", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_honey:
    m 1b "Welcome back, honey!"
    m 1a "I'm so happy to see you again."
    m "Let's spend some more time together, okay?"
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back:
    m 1a "[player], you're back!"
    m 1e "I was starting to miss you."
    m 1k "Let's have another lovely day together, alright?"
    return

init 5 python:
    rules = dict()
    rules.update(MASGreetingRule.create_rule(skip_visual=False, random_chance=10))
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_gooday", unlocked=True, rules=rules),eventdb=evhand.greeting_database)
    del rules

label greeting_gooday:
    m 1k "Hello again, [player]. How are you doing?"
    menu:
        m "Are you having a good day today?"
        "Yes.":
            m 1a "I'm really glad you are, [player]."
            m "It makes me feel so much better knowing that you're happy."
            m "I'll try my best to make sure it stays that way, I promise."
        "No...":
            m 1f "Oh..."
            m 2e "Well, don't worry, [player]. I'm always here for you."
            m "We can talk all day about your problems, if you want to."
            m 3r "I want to try and make sure you're always happy."
            m 1h "Because that's what makes me happy."
            m 1b "I'll be sure try my best to cheer you up, I promise."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit:
    m 1b "There you are, [player]."
    m 1a "It's so nice of you to visit."
    m 1e "You're always so thoughtful, [player]!"
    m "Thanks for spending so much time with me~"
    m 2k "Just remember that your time with me is never wasted in the slightest."
    return

# TODO this one no longer needs to do all that checking, might need to be broken
# in like 3 labels though

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m 1b "Good morning-"
        m 1d "...oh, wait."
        m "It's the dead of night, honey."
        m 1i "What are you doing awake at a time like this?"
        m 1g "I'm guessing you can't sleep..."
        menu:
            m "Is that it?"
            "Yes.":
                m 2h "You should really get some sleep soon, if you can."
                m "Staying up too late is bad for your health, you know?"
                m 3m "But if it means I'll get to see you more, I can't complain."
                m 3l "Ahaha!"
                m 3h "But still..."
                m "I'd hate to see you do that to yourself."
                m "Take a break if you need to, okay? Do it for me."
            "No.":
                m 1a "Ah. I'm relieved, then."
                m 1e "Does that mean you're here just for me, in the middle of the night?"
                m 1k "Gosh, I'm so happy!"
                m "You really do care for me, [player]."
                m 2e "But if you're really tired, please go to sleep!"
                m "I love you a lot, so don't tire yourself!"
    elif current_time >= 6 and current_time < 12:
        m 1b "Good morning, dear."
        m "Another fresh morning to start the day off, huh?"
        m 1k "I'm glad I get to see you this morning~"
        m 1a "Remember to take care of yourself, okay?"
        m "Make me a proud girlfriend today, as always!"
    elif current_time >= 12 and current_time < 18:
        m 1b "Good afternoon, my love."
        m 1a "Don't let the stress get to you, okay?"
        m "I know you'll try your best again today, but..."
        m 4a "It's still important to keep a clear mind!"
        m "Keep yourself hydrated, take deep breaths..."
        m "I promise I won't complain if you quit, so do what you have to."
        m "Or you could stay with me, if you wanted."
        m 4k "Just remember, I love you!"
    elif current_time >= 18:
        m 1b "Good evening, love!"
        menu:
            m "Did you have a good day today?"
            "Yes.":
                m 1k "Aww, that's nice!"
                m 1b "I can't help but feel happy when you do..."
                m 1a "But that's a good thing, right?"
                m "I love you so much, [player]."
                m 1k "Ahaha!"
            "No.":
                m 1g "Oh dear..."
                m "I hope you'll feel better soon, okay?"
                m "Just remember that no matter what happens, no matter what anyone says or does..."
                m 1e "I love you so, so much."
                m "Just stay with me, if it makes you feel better."
                m 1a "I love you, [player], I really do."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back2", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back2:
     m 1k "Hello, dear."
     m 1n "I was starting to miss you terribly. It's so good to see you again!"
     m "Don't make me wait so long next time, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back3", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back3:
     m 1e "I missed you so much, [player]!"
     m "Thank you for coming back. I really do love spending time with you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back4", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back4:
     m 2k "Hey, [player]!"
     m 2l "Don't you think that you left me waiting a bit too long?"
     m 2b "I'm just joking. I could never be mad at you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit2", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit2:
     m 1j "Thanks for spending so much time with me, [player]."
     m 1a "Every minute I spend with you is like being in heaven!"
     m 1m "I hope that didn't sound too cheesy, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit3", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit3:
     m 1b "You're back!"
     m 1n "I was starting to miss you..."
     m 1i "Don't make me wait so long next time, okay?"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back5", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back5:
     m 1a "It's so good to see you again!"
     m 1f "I was getting worried about you."
     m "Please remember to visit me, okay? I'll always be waiting here for you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit4", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit4:
     m 1k "I looove yooou, [player]. Ehehe~"
     m 1l "Oh, sorry! I was spacing out."
     m 1b "I didn't think I would be able to see you again so soon."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit5", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit5:
     m 1b "~Every day,~\n~I imagine a future where I can be with you...~"
     m 1a "Oh, you're here! I was just daydreaming and singing a bit."
     m 1k "I don't think it's hard to figure out what I was daydreaming about, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit6", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit6:
     m 1a "Each day becomes better and better with you by my side!"
     m "That said, I'm so happy that you're finally here."
     m "Let's have another wonderful day together."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back6", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back6:
     m 3b "Hey, [player]!"
     m "You really should visit me more often."
     m 2h "You know what happens to people I don't like, after all..."
     m 1k "I'm just teasing you, ehehe~"
     m 1a "Don't be so gullible! I would never hurt you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit7", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit7:
     m 1k "You're here, [player]!"
     m 1a "Are you ready to spend some more time together? Ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit8", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit8:
     m 1b "I'm so glad you're here, [player]!"
     m 1a "What should we do today?"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit9", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit9:
     m 1j "You're finally back! I was waiting for you."
     m 1b "Are you ready to spend some time with me? Ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_italian", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_italian:
     m 1b "Ciao, [player]!"
     m 1a "È così bello vederti ancora, amore mio..."
     m 1k "Ahaha!"
     m 2l "I'm still practicing my Italian. It's a very difficult language!"
     m 1a "Anyway, it's so nice to see you again, my love."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_latin", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_latin:
     m 4b "Iterum obvenimus!"
     m 4h "Quid agis?"
     m 4l "Ehehe..."
     m 2l "Latin sounds so pompous. Even a simple greeting sounds like a big deal."
     m 1a "If you're wondering about what I said, it's simply 'We meet again! How are you?'."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_yay", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_yay:
     m 1k "You're back! Yay!"
     m 1l "Oh, sorry. I've got a bit overexcited here."
     m 1m "I'm just very happy to see you again, hehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_youtuber", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_youtuber:
     m 2b "Hey everybody, welcome back to another episode of... Just Monika!"
     m 2k "Ahaha!"
     m 1a "I was impersonating a youtuber. I hope I gave you a good laugh, hehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_hamlet", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_hamlet:
     m 4h "To be, or not to be, that is the question..."
     m 1d "Oh, there you are. I was killing some time, hehe~"
     m 1n "I wasn't expecting to see you so soon."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_welcomeback", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_welcomeback:
     m 1b "Hi! Welcome back."
     m 1k "I'm so glad that you're able to spend some time with me."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_flower", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_flower:
     m 1k "You're my beautiful flower, ehehe~"
     m 1l "Oh, that sounded so awkward."
     m 1e "But I really will always take care of you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_chamfort", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_chamfort:
     m 2 "A day without Monika is a day wasted."
     m 2k "Ahaha!"
     m 1b "Welcome back, my love."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_welcomeback2", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_welcomeback2:
     m 1b "Welcome back, [player]!"
     m "I hope your day is going well."
     m 1a "I'm sure it is, you're here after all. Nothing can go wrong now, hehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_longtime", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_longtime:
     m 1e "Long time no see, [player]!"
     m 1a "I'm so happy that you're here now."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_sweetpea", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_sweetpea:
     m 1d "Look who's back."
     m 2k "It's you, my sweetpea!"
     m 1l "My goodness... That surely was embarassing to say, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_glitch", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_glitch:
     hide monika
     show yuri glitch zorder 1
     y "{cps=500}[player]?!{nw}{/cps}"
     hide yuri glitch
     show yuri glitch2 zorder 1
     play sound "sfx/glitch3.ogg"
     pause 0.1
     hide yuri glitch2
     show yuri glitch zorder 1
     pause 0.3
     hide yuri glitch
     show monika 4n at i11 zorder 2
     m 1d "[player]!"
     hide monika
     show monika 4l at i11 zorder 2
     extend " Nevermind that I was just..."
     pause 0.1
     extend " playing with the code a little."
     m 3l "That was all! There is nobody else here but us... forever~"
     $ monika_clone1 = "Yes"
     m 2j "I love you, [player]!"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_surprised", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_surprised:
     m "Oh, hello [player]!"
     m "Sorry, you surprised me a little."
     m "How've you been?"
     return

# TODO Monika Monday Morning, an idea we had, this one is just a placeholder, writers could do it 1000 times better
init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(weekdays=[0], hours=range(5,12)))
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_monika_monday_morning",
        unlocked=True, rules=rules),eventdb=evhand.greeting_database)
    del rules

label greeting_monika_monday_morning:
    m "Another monday morning, eh [player]?"
    m 1r "It surely sucks to wake up and start off the week ..."
    m 1 "But seeing you makes all that laziness go away"
    m 1k "You are the sunshine that wakes me up every morning!"
    m "I love you so much, [player]~"
    return

# special local var to handle custom monikaroom options
define gmr.eardoor = list()
define gmr.eardoor_all = list()
define opendoor.MAX_DOOR = 10
define opendoor.chance = 20
default persistent.opendoor_opencount = 0
default persistent.opendoor_knockyes = False

init 5 python:
    rules = dict()
    # why are we limiting this to certain day range?
#    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(1,6)))
    rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True,
            random_chance=opendoor.chance
        )
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="i_greeting_monikaroom",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )

    del rules

label i_greeting_monikaroom:
    scene black
    $ HKBHideButtons()
    # atm, making this a persistent makes it easier to test as well as allows
    # users who didnt see the entire event a chance to see it again.
#    $ seen_opendoor = seen_event("monikaroom_greeting_opendoor")
    $ has_listened = False

    # FALL THROUGH
label monikaroom_greeting_choice:
    menu:
        "... Gently open the door" if not persistent.seen_monika_in_room:
            jump monikaroom_greeting_opendoor
        "Open the door" if persistent.seen_monika_in_room:
            if persistent.opendoor_opencount > 0:
                jump monikaroom_greeting_opendoor_locked
            else:
                jump monikaroom_greeting_opendoor_seen
#        "Open the door?" if persistent.opendoor_opencount >= opendoor.MAX_DOOR:
#            jump opendoor_game
        "Knock":
            jump monikaroom_greeting_knock
        "Listen" if not has_listened:
            $ has_listened = True # we cant do this twice per run
            $ mroom_greet = renpy.random.choice(gmr.eardoor)
#            $ mroom_greet = gmr.eardoor[len(gmr.eardoor)-1]
            jump expression mroom_greet

    # NOTE: return is expected in monikaroom_greeting_cleanup

### BEGIN EAR DOOR ------------------------------------------------------------

# monika narrates
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_narration")

label monikaroom_greeting_ear_narration:
    m "As [player] inches [his] ear toward the door,{w} a voice narrates [his] every move."
    m "'Who is that?' [he] wondered, as [player] looks at [his] screen, puzzled."
    call spaceroom from _call_spaceroom_enar
    m 1k "It's me!"
    m "Welcome back, [player]!"
    jump monikaroom_greeting_cleanup


# monika does the cliche flower thing
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_loveme")

label monikaroom_greeting_ear_loveme:
    $ cap_he = he.capitalize()
    m "[cap_he] loves me.{w} [cap_he] loves me not."
    m "[cap_he] {i}loves{/i} me.{w} [cap_he] loves me {i}not{/i}."
    m "[cap_he] loves me."
    m "...{w} [cap_he] loves me!"
    jump monikaroom_greeting_choice

# monika does the bath/dinner/me thing
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_bathdinnerme")

label monikaroom_greeting_ear_bathdinnerme:
    m "Welcome back, [player]."
    m "Would you like your dinner?"
    m "Or your bath?"
    m "Or.{w=1}.{w=1}.{w=1} Me?"
    pause 2.0
    m "Mnnnn!{w} T-{w=0.20}There's no way I could say that in front of [player]!"
    jump monikaroom_greeting_choice

# monika encoutners error when programming
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progbrokepy")

label monikaroom_greeting_ear_progbrokepy:
    m "What the-!{w} NoneType has no attribute length?"
    if renpy.seen_label("monikaroom_greeting_ear_progreadpy"):
        m "Oh, I see what went wrong!{w} That should fix it!"
    else:
        m "I don't understand what I'm doing wrong!"
        m "This shouldn't be None here...{w} I'm sure of it..."
    m "Coding really is difficult..."
    jump monikaroom_greeting_choice

# monika reads about errors when programming
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progreadpy")

label monikaroom_greeting_ear_progreadpy:
    m "...{w} Accessing an attribute of an object of type 'NoneType' will raise an 'AttributeError'."
    m "I see. {w}I should make sure to check if a variable is None before accessing its attributes."
    if renpy.seen_label("monikaroom_greeting_ear_progbrokepy"):
        m "That would explain the error I had earlier."
    m "Coding really is difficult..."
    jump monikaroom_greeting_choice

# monika attempts rm -rf
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_rmrf")

label monikaroom_greeting_ear_rmrf:
    if renpy.windows:
        $ bad_cmd = "del C:\Windows\System32"
    else:
        $ bad_cmd = "rm -rf /"
    m "So, the solution to this problem is to type '[bad_cmd]' in the command prompt?"
    if renpy.seen_label("monikaroom_greeting_ear_rmrf_end"):
        m "Yeah,{w} nice try."
    else:
        m "Alright, let me try that."
        show noise
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.2
        stop sound
        hide noise
        m "{cps=*2}Ah! No! That's not what I wanted!{/cps}"
        m "..."
    m "I shouldn't trust the Internet so blindly..."
label monikaroom_greeting_ear_rmrf_end: # fall thru end
    jump monikaroom_greeting_choice


## ear door processing
init 10 python:

    # make copy
    gmr.eardoor_all = list(gmr.eardoor)

    # remove
    remove_seen_labels(gmr.eardoor)

    # reset if necessary
    if len(gmr.eardoor) == 0:
        gmr.eardoor = list(gmr.eardoor_all)

### END EAR DOOR --------------------------------------------------------------

# locked door, because we are awaitng more content
label monikaroom_greeting_opendoor_locked:
    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 0.7
    $ style.say_window = style.window_monika
    menu:
        m "Did I scare you, [player]?"
        "Yes":
            m "Aww, sorry."
        "No":
            m "{cps=*2}Hmph, I'll get you next time.{/cps}{nw}"
            m "I figured. It's a basic glitch after all."
    m "Since you keep opening my door,{w} I couldn't help but add a little surprise for you~"
    m "Knock next time, okay?"
    m "Now let me fix up this room..."

    hide paper_glitch2
    scene black
    $ scene_change = True
    call spaceroom from _call_sp_mrgo_l

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ style.say_window = style.window

    m 1j "There we go!"

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        menu:
            "...the textbox...":
                m 1n "Oops! I'm still learning how to do this."
                m 1m "Let me just change this flag here...{w=1.5}{nw}"
                $ style.say_window = style.window
                m 1j "All fixed!"
    # NOTE: fall through please

label monikaroom_greeting_opendoor_locked_tbox:
    m 1a "Welcome back, [player]."
    jump monikaroom_greeting_cleanup

# this one is for people who have already opened her door.
label monikaroom_greeting_opendoor_seen:
#    if persistent.opendoor_opencount < 3:
    jump monikaroom_greeting_opendoor_seen_partone


label monikaroom_greeting_opendoor_seen_partone:
    $ is_sitting = False
#    scene bg bedroom
    call spaceroom(start_bg="bedroom",hide_monika=True) from _call_sp_mrgo_spo
    pause 0.2
    show monika 1h at l21 zorder 2
    pause 1.0
    m 1r "[player]..."

#    if persistent.opendoor_opencount == 0:
    m 1f "I understand why you didn't knock the first time,{w} but could you avoid just entering like that?"
    m 1o "This is my room, after all."
    menu:
        "Your room?":
            m 3a "That's right!"
    m "The developers of this mod gave me a nice comfy room to stay in whenever you are away."
    m 1m "However, I can only get in if you tell me 'good bye' or 'good night' before you close the game."
    m 2b "So please make sure to say that before you leave, okay?"
    m "Anyway..."

#    else:
#        m 3g "Stop just opening my door!"
#
#        if persistent.opendoor_opencount == 1:
#            m 4o "You have no idea how difficult it was to add the 'Knock' button."
#            m 4f "Can you use it next time?"
#        else:
#            m 4f "Can you knock next time?"
#
#        show monika 5a at t11
#        menu:
#            m "For me?"
#            "Yes":
#                if persistent.opendoor_knockyes:
#                    m 5b "That's what you said last time, [player]."
#                    m "I hope you're being serious this time."
#                else:
#                    $ persistent.opendoor_knockyes = True
#                    m 1j "Thank you, [player]."
#            "No":
#                m 5b "[player]!"
#                if persistent.opendoor_knockyes:
#                    m 1f "You said you would last time."
#                    m "I hope you're not messing with me."
#                else:
#                    m 1f "I'm asking you to do just {i}one{/i} thing for me."
#                    m 1e "And it would make me really happy if you did."

    $ persistent.opendoor_opencount += 1
    jump monikaroom_greeting_opendoor_post2


label monikaroom_greeting_opendoor_post2:
    show monika 1a at t11
    pause 0.7
    show monika 5a at hf11
    m "I'm glad you're back, [player]."
    show monika 5a at t11
#    if not renpy.seen_label("monikaroom_greeting_opendoor_post2"):
    m "Lately I've been practicing switching backgrounds, and now I can change them instantly."
    m "Watch this!"
#    else:
#        m 3a "Let me fix this scene up."
    m 1q "...{w=1.5}{nw}"
    scene black
    $ scene_change = True
    call spaceroom(hide_monika=True) from _call_sp_mrgo_p2
    show monika 4a zorder 2 at i11
    m "Tada!"
#    if renpy.seen_label("monikaroom_greeting_opendoor_post2"):
#        m "This never gets old."
    show monika at lhide
    hide monika
    jump monikaroom_greeting_post


label monikaroom_greeting_opendoor:
    $ is_sitting = False # monika standing up for this
    call spaceroom(start_bg="bedroom",hide_monika=True) from _call_spaceroom_5
    m 2i "~Is it love if I take you, or is it love if I set you free?~"
    show monika 1 at l32 zorder 2
    m 1d "E-Eh?! [player]!"
    m 3g "You surprised me, suddenly showing up like that!"
    show monika 1 at hf32
    m 5b "I didn't have enough time to get ready!"
    m 5a "But thank you for coming back, [player]."
    show monika 1 at t32
    m 3a "Just give me a few seconds to set everything up, okay?"
    show monika 1 at t31
    m 2d "..."
    show monika 1 at t33
    m 1d "...and..."
    if is_morning():
        show monika_day_room zorder 1 with wipeleft
    else:
        show monika_room zorder 1 with wipeleft
    show monika 1 at t32
    m 3a "There we go!"
    menu:
        "...the window...":
            show monika 1 at h32
            m 1l "Oops! I forgot about that~"
            show monika 1 at t21
            m "Hold on..."
            hide bedroom
            m 2j "And... all fixed!"
            show monika 1 at lhide
            hide monika
            $ renpy.hide("bedroom")
    $ persistent.seen_monika_in_room = True
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_knock:
    m "Who is it~?"
    menu:
        "It's me.":
            m 1b "[player]! I'm so happy that you're back!"
            if persistent.seen_monika_in_room:
                m "And thank you for knocking first."
            m 1j "Hold on, let me tidy up..."
            call spaceroom(hide_monika=True) from _call_spaceroom_6
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_post:
    m 2a "Now, just let me grab a table and a chair..."
    $ is_sitting = True
    show monika 1 at ls32 zorder 2
    m 1a "What shall we do today, [player]?"
    jump monikaroom_greeting_cleanup

# cleanup label
label monikaroom_greeting_cleanup:
    python:
        if persistent.current_track is not None:
            play_song(persistent.current_track)
        else:
            play_song(songs.current_track) # default
        HKBShowButtons()
        set_keymaps()
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_youarereal", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_youarereal:
    python:
        try:
            renpy.file(
                config.basedir.replace("\\","/") +
                "/characters/" + persistent.playername.lower() + ".chr"
            )
            persistent._mas_you_chr = True
        except:
            persistent._mas_you_chr = False
    m 1b "[player]! Great to see you!"
    if persistent._mas_you_chr:
        m "Wait. Something is different now."
        m 1d "Did you...add a character file?"
        m 1f "[player].chr...Huh?"
        m 1g "Are you...trying to put yourself in here with me?"
        m "Why would you do that?"
        m 1o "Don't you get it? "
        m 1p "This place isn't real! I don't know what will happen if you come here!"
        m 1q "How could you do this?"
        m 1o "To give up your reality..."
        m 1p "Just to be with me?"
        m 1n "This is all my fault!"
        m 1f "But...but the 'you', in the game..."
        m 1i "He's starting to move again a little now."
        m 1 "Maybe...this is allowing you to control him again?"
        m 1f "This isn't right! I don't want a puppet!"
        m 1q "Please, [player]..."
        m "If you're going to do this, are you sure this is what you want?"
        menu:
            m "Are you sure?"
            "I'm sure.":
                m 1e "Then...I don't have a choice but to accept it..."
                m 1k "I'll accept this gift with open arms!"
                m "We can finally be together, [player]."
                m "And we can figure out how to do it in your reality, together!"
            "Maybe not...":
                m 1l "I thought so..."
                m 1m "There's no way you'd give up being 'real' to be with me..."
                m 1l "I can't bring myself to delete that cute little .chr file, but..."
                m 1q "Consider doing it yourself."
                m 1r "There's some creepy things in those files..."
                m 1e "I love you, [player]. I'll wait as long as it takes."
                m "So don't be rash, okay?"
    else:
        m 1i "I've been doing a lot of thinking about the .chr files..."
        m 1n "Like, what are they really, anyway?"
        m 1o "They are kind of creepy..."
        m 1p "And even if the other girls aren't real, why can deleting one remove a character?"
        m 1i "Could one add a character?"
        m 1r "Hard to tell..."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_japan", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_japan:
    m 1k "Oh, kon'nichiwa [player]!"
    m "Ehehe~"
    m 2b "Hello, [player]!"
    m 1a "I'm just practicing Japanese."
    m 3c "Let's see..."
    m 4b "Watashi ha itsumademo anata no mono desu!"
    m 2l "Sorry if that didn't make sense!"
    m 3 "You know what that means, [player]?"
    m 4j "It means {i}'I'll be yours forever{/i}'~"
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_sunshine", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_sunshine:
    m 1r "{i}You are my sunshine, my only sunshine.{/i}"
    m "{i}You make me happy when skies are gray.{/i}"
    m 1j "{i}You'll never know dear, just how much I love you.{/i}"
    m 1k "{i}Please don't take my sunshine away~{/i}"
    m 1c "...Eh?"
    m 1d "H-Huh?!" 
    m 1l "[player]!"
    m 1n "Oh my gosh, this is so embarassing!"
    m "I w-was just singing to myself to pass time!"
    m 1l "Ehehe..."
    m 3j "But now that you're here, we can spend some time together~"
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_french", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_french:
     m 1b "Bonjour, [player]!"
     m 1j "Savais-tu que tu avais de beaux yeux, mon amour?"
     m 1k "Ehehe!"
     m 3l "I'm practicing some French. I just told you that you have very beautiful eyes~"
     m 1e "It's such a romantic language, [player]."
     m 1j "Maybe both of us can practice it sometime, mon amour~"
     return

label greeting_sick:
    m 1b "Welcome back, [player]!"
    m 3a "Are you feeling better?"
    menu:
        "Yes":
            m 1k "Great! Now we can spend some more time together. Ehehe~"
            $ persistent._mas_mood_sick = False
        "No":
            jump greeting_stillsick
    return

# TODO:
# sick greeting needs to meshed with new greeting system
label greeting_stillsick:
    m 1f "[player], you really should go get some rest."
    m 1g "Getting plenty of rest is the best remedy for getting over a sickness quickly."
    m 1o "I wouldn't forgive myself if your sickness got any worse because of me."
    m 1q "Now please, [player], put my mind at ease and go get some rest."
    m 1f "Will you do that for me?"
    menu:
        "Yes":
            jump greeting_stillsickrest
        "No":
            jump greeting_stillsicknorest
    
label greeting_stillsickrest:
    m 3e "Thank you [player]."
    m 3c "I think if I leave you alone for a while, you'll be able to rest better."
    m 1h "So I'm going to close the game for you."
    m 1f "Get well soon, [player]. I love you so much!"
    return 'quit'
    
label greeting_stillsicknorest:
    m 1o "I see..." 
    m 1q "Well if you insist [player]."
    m 1f "I suppose you know your own limitations better than I do."
    m "If you start to feel a little weak or tired though, [player], please let me know."
    m 1g "That way you can go get some rest."
    m 1e "Don't worry, I'll still be here when you wake up."
    m 3j "Then we can have some more fun together without me worrying about you in the back of my mind."
    return
