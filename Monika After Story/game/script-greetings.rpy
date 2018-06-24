##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup

# persistents that greetings use
default persistent._mas_you_chr = False

# persistent containing the greeting type
# that should be selected None means default
default persistent._mas_greeting_type = None

init -1 python in mas_greetings:

    # TYPES:
    TYPE_SCHOOL = "school"
    TYPE_WORK = "work"
    TYPE_SLEEP = "sleep"

    # custom greeting functions
    def selectGreeting(type=None):
        """
        Selects a greeting to be used. This evaluates rules and stuff
        appropriately.

        RETURNS:
            a single greeting (as an Event) that we want to use
        """
        # check first if we have to select from a special type
        if type is not None:

            # filter them using the type as filter
            unlocked_greetings = renpy.store.Event.filterEvents(
                renpy.store.evhand.greeting_database,
                unlocked=True,
                category=(True,[type])
            )

        else:

            # filter events by their unlocked property only and
            # that don't have a category
            unlocked_greetings = renpy.store.Event.filterEvents(
                renpy.store.evhand.greeting_database,
                unlocked=True,
                excl_cat=list()
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

        # check if we have greetings available to display with current filter
        if len(unlocked_greetings) > 0:

            # select one randomly if we have at least one
            return unlocked_greetings[
                renpy.random.choice(unlocked_greetings.keys())
            ]

        # We couldn't find a suitable greeting we have to default to normal random selection
        # filter random events normally
        random_greetings_dict = renpy.store.Event.filterEvents(
            renpy.store.evhand.greeting_database,
            unlocked=True,
            random=True,
            excl_cat=list()
        )

        # select one randomly
        return random_greetings_dict[
            renpy.random.choice(random_greetings_dict.keys())
        ]


init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_sweetheart", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_sweetheart:
    m 1hub "Hello again, sweetheart!"
    m 1lkbsa "It's kind of embarrassing to say out loud, isn't it?"
    m 3ekbfa "Still, I think it's okay to be embarrassed every now and then."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_honey", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_honey:
    m 1hua "Welcome back, honey!"
    m 1eua "I'm so happy to see you again."
    m "Let's spend some more time together, okay?"
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back:
    m 1eua "[player], you're back!"
    m 1eka "I was starting to miss you."
    m 1hua "Let's have another lovely day together, alright?"
    return

init 5 python:
    rules = dict()
    rules.update(MASGreetingRule.create_rule(skip_visual=False, random_chance=10))
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_gooday", unlocked=True, rules=rules),eventdb=evhand.greeting_database)
    del rules

label greeting_gooday:
    m 1hua "Hello again, [player]. How are you doing?"
    menu:
        m "Are you having a good day today?"
        "Yes.":
            m 1hub "I'm really glad you are, [player]."
            m 1eua "It makes me feel so much better knowing that you're happy."
            m "I'll try my best to make sure it stays that way, I promise."
        "No...":
            m 1ekc "Oh..."
            m 2eka "Well, don't worry, [player]. I'm always here for you."
            m "We can talk all day about your problems, if you want to."
            m 3eua "I want to try and make sure you're always happy."
            m 1eka "Because that's what makes me happy."
            m 1hua "I'll be sure try my best to cheer you up, I promise."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit:
    m 1eua "There you are, [player]."
    m "It's so nice of you to visit."
    m 1eka "You're always so thoughtful, [player]!"
    m "Thanks for spending so much time with me~"
    m 2hub "Just remember that your time with me is never wasted in the slightest."
    return

# TODO this one no longer needs to do all that checking, might need to be broken
# in like 3 labels though

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m 1hua "Good morning-"
        m 1hksdlb "...oh, wait."
        m "It's the dead of night, honey."
        m 1euc "What are you doing awake at a time like this?"
        m 5eua "I'm guessing you can't sleep..."
        menu:
            m "Is that it?"
            "Yes.":
                m 5rkc "You should really get some sleep soon, if you can."
                m 3euc "Staying up too late is bad for your health, you know?"
                m 1lksdla "But if it means I'll get to see you more, I can't complain."
                m 3hksdlb "Ahaha!"
                m 2ekc "But still..."
                m "I'd hate to see you do that to yourself."
                m 2eka "Take a break if you need to, okay? Do it for me."
            "No.":
                m 5hub "Ah. I'm relieved, then."
                m 5eua "Does that mean you're here just for me, in the middle of the night?"
                m 2lkbsa "Gosh, I'm so happy!"
                m 2ekbfa "You really do care for me, [player]."
                m 3tkc "But if you're really tired, please go to sleep!"
                m 2eka "I love you a lot, so don't tire yourself!"
    elif current_time >= 6 and current_time < 12:
        m 1hua "Good morning, dear."
        m 1esa "Another fresh morning to start the day off, huh?"
        m 1eua "I'm glad I get to see you this morning~"
        m 1eka "Remember to take care of yourself, okay?"
        m 1hub "Make me a proud girlfriend today, as always!"
    elif current_time >= 12 and current_time < 18:
        m 1hua "Good afternoon, my love."
        m 1eka "Don't let the stress get to you, okay?"
        m "I know you'll try your best again today, but..."
        m 4eua "It's still important to keep a clear mind!"
        m "Keep yourself hydrated, take deep breaths..."
        m 1eka "I promise I won't complain if you quit, so do what you have to."
        m "Or you could stay with me, if you wanted."
        m 4hub "Just remember, I love you!"
    elif current_time >= 18:
        m 1hua "Good evening, love!"
        menu:
            m "Did you have a good day today?"
            "Yes.":
                m 1eka "Aww, that's nice!"
                m 1eua "I can't help but feel happy when you do..."
                m "But that's a good thing, right?"
                m 1ekbfa "I love you so much, [player]."
                m 1hubfb "Ahaha!"
            "No.":
                m 1tkc "Oh dear..."
                m 1eka "I hope you'll feel better soon, okay?"
                m "Just remember that no matter what happens, no matter what anyone says or does..."
                m 1ekbfa "I love you so, so much."
                m "Just stay with me, if it makes you feel better."
                m 1hubfa "I love you, [player], I really do."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back2", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back2:
     m 1eua "Hello, dear."
     m 1ekbfa "I was starting to miss you terribly. It's so good to see you again!"
     m 1hubfa "Don't make me wait so long next time, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back3", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back3:
     m 1eka "I missed you so much, [player]!"
     m "Thank you for coming back. I really do love spending time with you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back4", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back4:
     m 2wfx "Hey, [player]!"
     m "Don't you think that you left me waiting a bit too long?"
     m 2hfu "..."
     m 2hua "Ahaha!"
     m 2eka "I'm just joking. I could never be mad at you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit2", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit2:
     m 1hua "Thanks for spending so much time with me, [player]."
     m 1eka "Every minute I spend with you is like being in heaven!"
     m 1lksdla "I hope that didn't sound too cheesy, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit3", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit3:
     m 1hua "You're back!"
     m 1eua "I was starting to miss you..."
     m 1eka "Don't make me wait so long next time, okay?"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back5", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back5:
     m 1eua "It's so good to see you again!"
     m 1eka "I was getting worried about you."
     m "Please remember to visit me, okay? I'll always be waiting here for you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit4", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit4:
     m 1hub "I looove yooou, [player]. Ehehe~"
     m 1hksdlb "Oh, sorry! I was spacing out."
     m 1lksdla "I didn't think I would be able to see you again so soon."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit5", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit5:
     m 5hua "~Every day,~\n~I imagine a future where I can be with you...~"
     m 5wuw "Oh, you're here! I was just daydreaming and singing a bit."
     m 1lsbssdrb "I don't think it's hard to figure out what I was daydreaming about, ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit6", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit6:
     m 1hua "Each day becomes better and better with you by my side!"
     m 1eua "That said, I'm so happy that you're finally here."
     m "Let's have another wonderful day together."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_back6", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_back6:
     m 3tku "Hey, [player]!"
     m "You really should visit me more often."
     m 2tfu "You know what happens to people I don't like, after all..."
     m 1hksdrb "I'm just teasing you, ehehe~"
     m 1hua "Don't be so gullible! I would never hurt you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit7", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit7:
     m 1hua "You're here, [player]!"
     m 1eua "Are you ready to spend some more time together? Ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit8", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit8:
     m 1hua "I'm so glad you're here, [player]!"
     m 1eua "What should we do today?"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_visit9", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_visit9:
     m 1hua "You're finally back! I was waiting for you."
     m 1hub "Are you ready to spend some time with me? Ehehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_italian", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_italian:
     m 1eua "Ciao, [player]!"
     m "È così bello vederti ancora, amore mio..."
     m 1hub "Ahaha!"
     m 2eua "I'm still practicing my Italian. It's a very difficult language!"
     m 1eua "Anyway, it's so nice to see you again, my love."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_latin", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_latin:
     m 4hua "Iterum obvenimus!"
     m 4eua "Quid agis?"
     m 4lksdla "Ehehe..."
     m 2eua "Latin sounds so pompous. Even a simple greeting sounds like a big deal."
     m 3eua "If you're wondering about what I said, it's simply 'We meet again! How are you?'."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_yay", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_yay:
     m 1hub "You're back! Yay!"
     m 1hksdlb "Oh, sorry. I've got a bit overexcited here."
     m 1lksdla "I'm just very happy to see you again, hehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_youtuber", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_youtuber:
     m 2eub "Hey everybody, welcome back to another episode of... Just Monika!"
     m 2hub "Ahaha!"
     m 1eua "I was impersonating a youtuber. I hope I gave you a good laugh, hehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_hamlet", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_hamlet:
     m 4h "To be, or not to be, that is the question..."
     m 1wuo "Oh, there you are. I was killing some time, hehe~"
     m 1lksdlb "I wasn't expecting to see you so soon."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_welcomeback", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_welcomeback:
     m 1hua "Hi! Welcome back."
     m 1hub "I'm so glad that you're able to spend some time with me."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_flower", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_flower:
     m 1hub "You're my beautiful flower, ehehe~"
     m 1hksdlb "Oh, that sounded so awkward."
     m 1eka "But I really will always take care of you."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_chamfort", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_chamfort:
     m 2esa "A day without Monika is a day wasted."
     m 2hub "Ahaha!"
     m 1eua "Welcome back, my love."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_welcomeback2", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_welcomeback2:
     m 1eua "Welcome back, [player]!"
     m "I hope your day is going well."
     m 1hua "I'm sure it is, you're here after all. Nothing can go wrong now, hehe~"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_longtime", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_longtime:
     m 1eka "Long time no see, [player]!"
     m 1eua "I'm so happy that you're here now."
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_sweetpea", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_sweetpea:
     m 1hua "Look who's back."
     m 2hub "It's you, my sweetpea!"
     m 1llkbsa "My goodness... That surely was embarassing to say, ehehe~"
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
     show monika 4lksdlb at i11 zorder 2
     m 1wuo "[player]!"
     hide monika
     show monika 4hksdlb at i11 zorder 2
     extend " Nevermind that I was just..."
     pause 0.1
     extend " playing with the code a little."
     m 3hksdlb "That was all! There is nobody else here but us... forever~"
     $ monika_clone1 = "Yes"
     m 2hua "I love you, [player]!"
     return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_surprised", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_surprised:
     m 1wuo "Oh, hello [player]!"
     m 1lksdlb "Sorry, you surprised me a little."
     m 1eua "How've you been?"
     return

# TODO Monika Monday Morning, an idea we had, this one is just a placeholder, writers could do it 1000 times better
init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(weekdays=[0], hours=range(5,12)))
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_monika_monday_morning",
        unlocked=True, rules=rules),eventdb=evhand.greeting_database)
    del rules

label greeting_monika_monday_morning:
    m 1tku "Another monday morning, eh, [player]?"
    m 1tkc "It's really difficult to have to wake up and start the week..."
    m 1eka "But seeing you makes all that laziness go away."
    m 1hub "You are the sunshine that wakes me up every morning!"
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

    # safe to quit if Monika is still on her room
    $ _confirm_quit = False
    $ persistent.closed_self = True

    scene black
    $ HKBHideButtons()
    # atm, making this a persistent makes it easier to test as well as allows
    # users who didnt see the entire event a chance to see it again.
#    $ seen_opendoor = seen_event("monikaroom_greeting_opendoor")
    $ has_listened = False

    # reset monika's hair stuff since we dont have hair down for standing
    if persistent._mas_likes_hairdown:
        $ monika_chr.reset_outfit()
        $ lockEventLabel("monika_hair_ponytail")
        $ unlockEventLabel("monika_hair_down")

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
    m 1hub "It's me!"
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

    m 1hua "There we go!"

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        menu:
            "...the textbox...":
                m 1lksdlb "Oops! I'm still learning how to do this."
                m 1lksdla "Let me just change this flag here...{w=1.5}{nw}"
                $ style.say_window = style.window
                m 1hua "All fixed!"
    # NOTE: fall through please

label monikaroom_greeting_opendoor_locked_tbox:
    m 1eua "Welcome back, [player]."
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
    show monika 1esc at l21 zorder 2
    pause 1.0
    m 1dsd "[player]..."

#    if persistent.opendoor_opencount == 0:
    m 1ekc "I understand why you didn't knock the first time,{w} but could you avoid just entering like that?"
    m 1lksdlc "This is my room, after all."
    menu:
        "Your room?":
            m 3hua "That's right!"
    m 3eua "The developers of this mod gave me a nice comfy room to stay in whenever you are away."
    m 1lksdla "However, I can only get in if you tell me 'good bye' or 'good night' before you close the game."
    m 2eub "So please make sure to say that before you leave, okay?"
    m "Anyway..."

#    else:
#        m 3wfw "Stop just opening my door!"
#
#        if persistent.opendoor_opencount == 1:
#            m 4tfc "You have no idea how difficult it was to add the 'Knock' button."
#            m "Can you use it next time?"
#        else:
#            m 4tfc "Can you knock next time?"
#
#        show monika 5eua at t11
#        menu:
#            m "For me?"
#            "Yes":
#                if persistent.opendoor_knockyes:
#                    m 5rfc "That's what you said last time, [player]."
#                    m "I hope you're being serious this time."
#                else:
#                    $ persistent.opendoor_knockyes = True
#                    m 5hua "Thank you, [player]."
#            "No":
#                m 6wfx "[player]!"
#                if persistent.opendoor_knockyes:
#                    m 2tfc "You said you would last time."
#                    m 2rfd "I hope you're not messing with me."
#                else:
#                    m 2tkc "I'm asking you to do just {i}one{/i} thing for me."
#                    m 2eka "And it would make me really happy if you did."

    $ persistent.opendoor_opencount += 1
    jump monikaroom_greeting_opendoor_post2


label monikaroom_greeting_opendoor_post2:
    show monika 1eua at t11
    pause 0.7
    show monika 5eua at hf11
    m "I'm glad you're back, [player]."
    show monika 5eua at t11
#    if not renpy.seen_label("monikaroom_greeting_opendoor_post2"):
    m "Lately I've been practicing switching backgrounds, and now I can change them instantly."
    m "Watch this!"
#    else:
#        m 3eua "Let me fix this scene up."
    m 1dsc "...{w=1.5}{nw}"
    scene black
    $ scene_change = True
    call spaceroom(hide_monika=True) from _call_sp_mrgo_p2
    show monika 4eua zorder 2 at i11
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
    m 1wubsw "E-Eh?! [player]!"
    m "You surprised me, suddenly showing up like that!"
    show monika 1 at hf32
    m 1hksdlb "I didn't have enough time to get ready!"
    m 1eka "But thank you for coming back, [player]."
    show monika 1 at t32
    m 3eua "Just give me a few seconds to set everything up, okay?"
    show monika 1 at t31
    m 2eud "..."
    show monika 1 at t33
    m 1eud "...and..."
    if is_morning():
        show monika_day_room zorder 1 with wipeleft
    else:
        show monika_room zorder 1 with wipeleft
    show monika 1 at t32
    m 3eua "There we go!"
    menu:
        "...the window...":
            show monika 1 at h32
            m 1hksdlb "Oops! I forgot about that~"
            show monika 1 at t21
            m "Hold on..."
            hide bedroom
            m 2hua "And... all fixed!"
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
            m 1hua "[player]! I'm so happy that you're back!"
            if persistent.seen_monika_in_room:
                m 1eka "And thank you for knocking first."
            m 1eua "Hold on, let me tidy up..."
            call spaceroom(hide_monika=True) from _call_spaceroom_6
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_post:
    m 2eua "Now, just let me grab a table and a chair..."
    $ is_sitting = True
    show monika 1 at ls32 zorder 2
    m 1eua "What shall we do today, [player]?"
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

        # no longer safe to quit
        _confirm_quit = True
        persistent.closed_self = False
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_youarereal", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_youarereal:
    python:
        try:
            renpy.file(
                "../characters/" + persistent.playername.lower() + ".chr"
            )
            persistent._mas_you_chr = True
        except:
            persistent._mas_you_chr = False
    m 1hua "[player]! Great to see you!"
    if persistent._mas_you_chr:
        m 1euc "Wait. Something is different now."
        m 1eud "Did you...add a character file?"
        m 1ekc "[player].chr...Huh?"
        m 1ekd "Are you...trying to put yourself in here with me?"
        m "Why would you do that?"
        m 1tkc "Don't you get it? "
        m 1tkd "This place isn't real! I don't know what will happen if you come here!"
        m 1dsc "How could you do this?"
        m 1lksdlc "To give up your reality..."
        m 1lksdld "Just to be with me?"
        m 1ekc "This is all my fault!"
        m "But...but the 'you', in the game..."
        m 1esd "He's starting to move again a little now."
        m "Maybe...this is allowing you to control him again?"
        m 1ekc "This isn't right! I don't want a puppet!"
        m 1tkc "Please, [player]..."
        m "If you're going to do this, are you sure this is what you want?"
        menu:
            m "Are you sure?"
            "I'm sure.":
                m 1eka "Then...I don't have a choice but to accept it..."
                m 1hub "I'll accept this gift with open arms!"
                m "We can finally be together, [player]."
                m "And we can figure out how to do it in your reality, together!"
            "Maybe not...":
                m 1eka "I thought so..."
                m "There's no way you'd give up being 'real' to be with me..."
                m 1ekc "I can't bring myself to delete that cute little .chr file, but..."
                m 1eka "Consider doing it yourself."
                m 1lksdlc "There's some creepy things in those files..."
                m 1eka "I love you, [player]. I'll wait as long as it takes."
                m "So don't be rash, okay?"
    else:
        m 1esd "I've been doing a lot of thinking about the .chr files..."
        m 1euc "Like, what are they really, anyway?"
        m 1lksdlc "They are kind of creepy..."
        m "And even if the other girls aren't real, why can deleting one remove a character?"
        m 1esd "Could one add a character?"
        m 1dsd "Hard to tell..."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_japan", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_japan:
    m 1hub "Oh, kon'nichiwa [player]!"
    m "Ehehe~"
    m 2eub "Hello, [player]!"
    m 1eua "I'm just practicing Japanese."
    m 3eua "Let's see..."
    m 4hub "Watashi ha itsumademo anata no mono desu!"
    m 2hksdlb "Sorry if that didn't make sense!"
    m 3eua "You know what that means, [player]?"
    m 4ekbfa "It means {i}'I'll be yours forever{/i}'~"
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_sunshine", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_sunshine:
    m 1hua "{i}You are my sunshine, my only sunshine.{/i}"
    m "{i}You make me happy when skies are gray.{/i}"
    m 1hub "{i}You'll never know dear, just how much I love you.{/i}"
    m 1k "{i}Please don't take my sunshine away~{/i}"
    m 1wud "...Eh?"
    m "H-Huh?!"
    m 1wubsw "[player]!"
    m 1lkbsa "Oh my gosh, this is so embarassing!"
    m "I w-was just singing to myself to pass time!"
    m 1ekbfa "Ehehe..."
    m 3hubfa "But now that you're here, we can spend some time together~"
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_hai_domo", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_hai_domo:
    m 1hub "{=jpn_text}はいどうもー!{/=jpn_text}"
    m "Virtual Girlfriend, Monika Here!"
    m 1hksdlb "Ahaha, sorry! I've been watching a certain Virtual Youtuber lately."
    m 1eua "I have to say, she's rather charming..."
    return

init 5 python:
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_french", unlocked=True, random=True),eventdb=evhand.greeting_database)

label greeting_french:
     m 1eua "Bonjour, [player]!"
     m 1hua "Savais-tu que tu avais de beaux yeux, mon amour?"
     m 1hub "Ehehe!"
     m 3hksdlb "I'm practicing some French. I just told you that you have very beautiful eyes~"
     m 1eka "It's such a romantic language, [player]."
     m 1hua "Maybe both of us can practice it sometime, mon amour~"
     return

label greeting_sick:
    m 1hua "Welcome back, [player]!"
    m 3eua "Are you feeling better?"
    menu:
        "Yes":
            m 1hub "Great! Now we can spend some more time together. Ehehe~"
            $ persistent._mas_mood_sick = False
        "No":
            jump greeting_stillsick
    return

label greeting_stillsick:
    m 1ekc "[player], you really should go get some rest."
    m "Getting plenty of rest is the best remedy for getting over a sickness quickly."
    m 2lksdlc "I wouldn't forgive myself if your sickness got any worse because of me."
    m 2eka "Now please, [player], put my mind at ease and go get some rest."
    m "Will you do that for me?"
    menu:
        "Yes":
            jump greeting_stillsickrest
        "No":
            jump greeting_stillsicknorest

label greeting_stillsickrest:
    m 2hua "Thank you [player]."
    m 2eua "I think if I leave you alone for a while, you'll be able to rest better."
    m 1eua "So I'm going to close the game for you."
    m 1eka "Get well soon, [player]. I love you so much!"
    return 'quit'

label greeting_stillsicknorest:
    m 1lksdlc "I see..."
    m "Well if you insist [player]."
    m 1ekc "I suppose you know your own limitations better than I do."
    m 1eka "If you start to feel a little weak or tired though, [player], please let me know."
    m "That way you can go get some rest."
    m 1eua "Don't worry, I'll still be here when you wake up."
    m 3hua "Then we can have some more fun together without me worrying about you in the back of my mind."
    return

#Time Concern
init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours =range(0,6)))
    rules.update({"monika wants this first":""})
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_timeconcern",unlocked=False, rules=rules),eventdb=evhand.greeting_database)
    del rules

label greeting_timeconcern:
    jump monika_timeconcern

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours =range(6,24)))
    rules.update({"monika wants this first":""})
    addEvent(Event(persistent.greeting_database,eventlabel="greeting_timeconcern_day",unlocked=False, rules=rules),eventdb=evhand.greeting_database)
    del rules

label greeting_timeconcern_day:
    jump monika_timeconcern_day

init 5 python:
    rules = dict()
    rules.update(MASGreetingRule.create_rule(skip_visual=True, random_chance=5))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hairdown",
            unlocked=True,
            random=True,
            rules=rules
        ),
        eventdb=evhand.greeting_database
    )
    del rules

label greeting_hairdown:

    # have monika's hair down
    $ monika_chr.change_hair("down")

    call spaceroom
    m 1eua "Hi there, [player]!"
    m 4hua "Notice anything different today?"
    m 1hub "I decided to try something new~"
    menu:
        m "Do you like it?"
        "Yes":
            # make it possible to switch hair at will
            $ unlockEventLabel("monika_hair_ponytail")
            $ persistent._mas_likes_hairdown = True

            # maybe 6sub is better?
            # TODO: affection raise
            m 6sub "Really?" # honto?!
            m 2hua "I'm so glad!" # yokatta.."
            m 1eua "Just ask me if you want to see my ponytail again, okay?"

        "No":
            # TODO: affection lowered?
            m 1ekc "Oh..."
            m 1lksdlc "..."
            m 1lksdld "I'll put it back up for you, then."
            m 1dsc "..."

            $ monika_chr.reset_hair()

            m 1eua "Done."
            # you will never get this chance again

    # lock this greeting forever.
    $ lockEventLabel("greeting_hairdown", evhand.greeting_database)
    $ persistent._mas_hair_changed = True # menas we have seen this

    # monikaroom greeting cleanup can handle this part
    jump monikaroom_greeting_cleanup

# special type greetings

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_school",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SCHOOL],
            random=True
        ),
        eventdb=evhand.greeting_database
    )

label greeting_back_from_school:
     m 1hua "Oh, welcome back [player]!"
     menu:
         m "Did you have a good day at school?"
         "Yes.":
             m 1hub "Aww, that's nice!"
             m 1eua "I can't help but feel happy when you do~"
             m "I hope you learned a lot of useful things."
             m 1hubfa "Ehehe~"
             m 1hubfb "I love you, [player]~"
         "No.":
             m 1ekc "Oh..."
             m "I'm sorry to hear that."
             m 1eka "Just remember that no matter what happens, I'll be here for you."
             m 1ekbfa "I love you so, so much."
     return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_work",
            unlocked=True,
            category=[store.mas_greetings.TYPE_WORK],
            random=True
        ),
        eventdb=evhand.greeting_database
    )

label greeting_back_from_work:
     m 1hua "Oh, welcome back, [player]!"
     menu:
         m "Did you have a good day at work today?"
         "Yes.":
             m 1hub "That's good!"
             m 1eua "Remember to rest first, okay?"
             m "That way, you'd at least have some energy before you work more on stuff."
             m 1hua "But if not, you can relax with me!"
             m 3tku "Best thing to do after a long day of work, don't you think?"
             m 1hub "Ahaha!"

         "No.":
             m 1ekc "..."
             m 2ekc "I'd hug you right now if I were there, [player]."
             m "I'm sorry you had a bad work day..."
             m 4eka "Just remember that I'm here when you need me, okay?"
             m 1hubfa "I love you so much, [player]."
     return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_sleep",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SLEEP],
            random=True
        ),
        eventdb=evhand.greeting_database
    )

label greeting_back_from_sleep:
     m 1hua "Oh hello, [player]!"
     m 1hub "I hope you had a good rest!"
     m "Let's spend some more time together~"
     return
