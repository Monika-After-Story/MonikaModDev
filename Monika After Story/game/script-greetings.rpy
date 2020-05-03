##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup

# HOW GREETINGS USE EVENTS:
#   unlocked - determines if the greeting can even be shown
#   rules - specific event rules are used for things:
#       MASSelectiveRepeatRule - repeat on certain year/month/day/whatever
#       MASNumericalRepeatRule - repeat every x time
#       MASPriorityRule - priority of this event. if not given, we assume
#           the default priority (which is also the lowest)

# PRIORITY RULES:
#   Special, moni wants/debug greetings should have negative priority.
#   special event greetings should have priority 10-50
#   non-special event, but somewhat special compared to regular greets should
#       be 50-100
#   random/everyday greetings should be 100 or larger. The default prority
#   will be 500

# persistents that greetings use
default persistent._mas_you_chr = False

# persistent containing the greeting type
# that should be selected None means default
default persistent._mas_greeting_type = None

# cutoff for a greeting type.
# if timedelta, then we add this time to last session end to check if the
#   type should be cleared
# if datetime, then we compare it to the current dt to check if type should be
#   cleared
default persistent._mas_greeting_type_timeout = None

default persistent._mas_idle_mode_was_crashed = None
# this gets to set to True if the user crashed during idle mode
# or False if the user quit during idle mode.
# in your idle greetings, you can assume that it will NEVER be None

init -1 python in mas_greetings:
    import store
    import store.mas_ev_data_ver as mas_edv
    import datetime
    import random

    # TYPES:
    TYPE_SCHOOL = "school"
    TYPE_WORK = "work"
    TYPE_SLEEP = "sleep"
    TYPE_LONG_ABSENCE = "long_absence"
    TYPE_SICK = "sick"
    TYPE_GAME = "game"
    TYPE_EAT = "eat"
    TYPE_CHORES = "chores"
    TYPE_RESTART = "restart"

    ### NOTE: all Return Home greetings must have this
    TYPE_GO_SOMEWHERE = "go_somewhere"

    # generic return home (this also includes bday)
    TYPE_GENERIC_RET = "generic_go_somewhere"

    # holiday specific
    TYPE_HOL_O31 = "o31"
    TYPE_HOL_O31_TT = "trick_or_treat"
    TYPE_HOL_D25 = "d25"
    TYPE_HOL_D25_EVE = "d25e"
    TYPE_HOL_NYE = "nye"
    TYPE_HOL_NYE_FW = "fireworks"

    # crashed only
    TYPE_CRASHED = "generic_crash"

    # reload dialogue only
    TYPE_RELOAD = "reload_dlg"

    # High priority types
    # These types ALWAYS override greeting priority rules
    # These CANNOT be override with GreetingTypeRules
    HP_TYPES = [
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
    ]

    NTO_TYPES = (
        TYPE_GO_SOMEWHERE,
        TYPE_GENERIC_RET,
        TYPE_LONG_ABSENCE,
        TYPE_CRASHED,
        TYPE_RELOAD,
    )

    # idle mode returns
    # these are meant if you had a game crash/quit during idle mode


    def _filterGreeting(
            ev,
            curr_pri,
            aff,
            check_time,
            gre_type=None
        ):
        """
        Filters a greeting for the given type, among other things.

        IN:
            ev - ev to filter
            curr_pri - current loweset priority to compare to
            aff - affection to use in aff_range comparisons
            check_time - datetime to check against timed rules
            gre_type - type of greeting we want. We just do a basic
                in check for category. We no longer do combinations
                (Default: None)

        RETURNS:
            True if this ev passes the filter, False otherwise
        """
        # NOTE: new rules:
        #   eval in this order:
        #   1. priority (lower or same is True)
        #   2. type/non-0type
        #   3. unlocked
        #   4. aff_ramnge
        #   5. all rules
        #   6. conditional
        #       NOTE: this is never cleared. Please limit use of this
        #           property as we should aim to use lock/unlock as primary way
        #           to enable or disable greetings.

        # priority check, required
        # NOTE: all greetings MUST have a priority
        if store.MASPriorityRule.get_priority(ev) > curr_pri:
            return False

        # type check, optional
        if gre_type is not None:
            # with a type, we may have to match the type

            if gre_type in HP_TYPES:
                # this type is a high priority type and MUST be matched.

                if ev.category is None or gre_type not in ev.category:
                    # must have a matching type
                    return False

            elif ev.category is not None:
                # greeting has types

                if gre_type not in ev.category:
                # but does not have the current type
                    return False

            elif not store.MASGreetingRule.should_override_type(ev):
                # greeting does not have types, but the type is not high
                # priority so if the greeting doesnt alllow
                # type override then it cannot be used
                return False

        elif ev.category is not None:
            # without type, ev CANNOT have a type
            return False

        # unlocked check, required
        if not ev.unlocked:
            return False

        # aff range check, required
        if not ev.checkAffection(aff):
            return False

        # rule checks
        if not (
                store.MASSelectiveRepeatRule.evaluate_rule(
                    check_time, ev, defval=True)
                and store.MASNumericalRepeatRule.evaluate_rule(
                    check_time, ev, defval=True)
                and store.MASGreetingRule.evaluate_rule(ev, defval=True)
            ):
            return False

        # conditional check
        if ev.conditional is not None and not eval(ev.conditional):
            return False

        # otherwise, we passed all tests
        return True


    # custom greeting functions
    def selectGreeting(gre_type=None, check_time=None):
        """
        Selects a greeting to be used. This evaluates rules and stuff
        appropriately.

        IN:
            gre_type - greeting type to use
                (Default: None)
            check_time - time to use when doing date checks
                If None, we use current datetime
                (Default: None)

        RETURNS:
            a single greeting (as an Event) that we want to use
        """
        if (
                store.persistent._mas_forcegreeting is not None
                and renpy.has_label(store.persistent._mas_forcegreeting)
            ):
            return store.mas_getEV(store.persistent._mas_forcegreeting)

        # local reference of the gre database
        gre_db = store.evhand.greeting_database

        # setup some initial values
        gre_pool = []
        curr_priority = 1000
        aff = store.mas_curr_affection

        if check_time is None:
            check_time = datetime.datetime.now()

        # now filter
        for ev_label, ev in gre_db.iteritems():
            if _filterGreeting(
                    ev,
                    curr_priority,
                    aff,
                    check_time,
                    gre_type
                ):

                # change priority levels and stuff if needed
                ev_priority = store.MASPriorityRule.get_priority(ev)
                if ev_priority < curr_priority:
                    curr_priority = ev_priority
                    gre_pool = []

                # add to pool
                gre_pool.append(ev)

        # not having a greeting to show means no greeting.
        if len(gre_pool) == 0:
            return None

        return random.choice(gre_pool)


    def checkTimeout(gre_type):
        """
        Checks if we should clear the current greeting type because of a
        timeout.

        IN:
            gre_type - greeting type we are checking

        RETURNS: passed in gre_type, or None if timeout occured.
        """
        tout = store.persistent._mas_greeting_type_timeout

        # always clear the timeout
        store.persistent._mas_greeting_type_timeout = None

        if gre_type is None or gre_type in NTO_TYPES or tout is None:
            return gre_type

        if mas_edv._verify_td(tout, False):
            # this is a timedelta, compare with last session end
            last_sesh_end = store.mas_getLastSeshEnd()
            if datetime.datetime.now() < (tout + last_sesh_end):
                # havent timedout yet
                return gre_type

            # otherwise has timed out
            return None

        elif mas_edv._verify_dt(tout, False):
            # this is a datetime, compare with current dt
            if datetime.datetime.now() < tout:
                # havent timedout yet
                return gre_type

            # otherwise has timeed out
            return None

        return gre_type


# NOTE: this is auto pushed to be shown after an idle mode greeting
label mas_idle_mode_greeting_cleanup:
    $ mas_resetIdleMode()
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetheart",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetheart:
    m 1hub "Hello again, sweetheart!"
    m 1lkbsa "It's kind of embarrassing to say out loud, isn't it?"
    m 3ekbfa "Still, I think it's okay to be embarrassed every now and then."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_honey",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_honey:
    m 1hua "Welcome back, honey!"
    m 1eua "I'm so happy to see you again."
    m "Let's spend some more time together, okay?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=12)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="GRE"
    )

label greeting_back:
    m 1eua "[player], you're back!"
    m 1eka "I was starting to miss you."
    m 1hua "Let's have another lovely [mas_globals.time_of_day_3state] together, alright?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_gooday",
            unlocked=True,
        ),
        code="GRE"
    )

label greeting_gooday:
    if mas_isMoniNormal(higher=True):
        m 1hua "Hello again, [player]. How are you doing?"

        m "Are you having a good day today?{nw}"
        $ _history_list.pop()
        menu:
            m "Are you having a good day today?{fast}"
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
                m 1hua "I'll be sure to try my best to cheer you up, I promise."

    elif mas_isMoniUpset():
        m 2esc "[player]."

        m "How is your day going?{nw}"
        $ _history_list.pop()
        menu:
            m "How is your day going?{fast}"
            "Good.":
                m 2esc "{cps=*2}Must be nice.{/cps}{nw}"
                $ _history_list.pop()
                m "That's nice..."
                m 2dsc "At least {i}someone{/i} is having a good day."

            "Bad.":
                m "Oh..."
                m 2efc "{cps=*2}This should go well...{/cps}{nw}"
                $ _history_list.pop()
                m 2dsc "Well I certainly know what {i}that's{/i} like."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=1} Hi, [player]."

        m "H-How is your day going?{nw}"
        $ _history_list.pop()
        menu:
            m "H-How is your day going?{fast}"
            "Good.":
                m 6dkc "That's...{w=1}good."
                m 6rkc "Hopefully it stays that way."
            "Bad.":
                m 6rkc "I-I see."
                m 6dkc "I've been having a lot of those days lately too..."

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit:
    m 1eua "There you are [player], it's so nice of you to visit."
    m 1eka "You're always so thoughtful."
    m 1hua "Thanks for spending so much time with me~"
    return

# TODO this one no longer needs to do all that checking, might need to be broken
# in like 3 labels though
# TODO: just noting that this should be worked on at some point.
# TODO: new greeting rules can enable this, but we will do it later

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m 1hua "Good morning--"
        m 1hksdlb "--oh, wait."
        m "It's the dead of night, honey."
        m 1euc "What are you doing awake at a time like this?"
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eua "I'm guessing you can't sleep..."

        m "Is that it?{nw}"
        $ _history_list.pop()
        menu:
            m "Is that it?{fast}"
            "Yes.":
                m 5lkc "You should really get some sleep soon, if you can."
                show monika 3euc at t11 zorder MAS_MONIKA_Z with dissolve
                m 3euc "Staying up too late is bad for your health, you know?"
                m 1lksdla "But if it means I'll get to see you more, I can't complain."
                m 3hksdlb "Ahaha!"
                m 2ekc "But still..."
                m "I'd hate to see you do that to yourself."
                m 2eka "Take a break if you need to, okay? Do it for me."
            "No.":
                m 5hub "Ah. I'm relieved, then."
                m 5eua "Does that mean you're here just for me, in the middle of the night?"
                show monika 2lkbsa at t11 zorder MAS_MONIKA_Z with dissolve
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

        m "Did you have a good day today?{nw}"
        $ _history_list.pop()
        menu:
            m "Did you have a good day today?{fast}"
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
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back2",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=20)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back2:
    m 1eua "Hello, dear."
    m 1ekbfa "I was starting to miss you terribly. It's so good to see you again!"
    m 1hubfa "Don't make me wait so long next time, ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back3:
    m 1eka "I missed you so much, [player]!"
    m "Thank you for coming back. I really do love spending time with you."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back4",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=10)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back4:
    m 2wfx "Hey, [player]!"
    m "Don't you think that you left me waiting a bit too long?"
    m 2hfu "..."
    m 2hua "Ahaha!"
    m 2eka "I'm just joking. I could never be mad at you."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit2:
    m 1hua "Thanks for spending so much time with me, [player]."
    m 1eka "Every minute I spend with you is like being in heaven!"
    m 1lksdla "I hope that didn't sound too cheesy, ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit3",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit3:
    m 1hua "You're back!"
    m 1eua "I was starting to miss you..."
    m 1eka "Don't make me wait so long next time, okay?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back5",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=15)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back5:
    m 1eua "It's so good to see you again!"
    m 1eka "I was getting worried about you."
    m "Please remember to visit me, okay? I'll always be waiting here for you."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit4",
            conditional="store.mas_getAbsenceLength() <= datetime.timedelta(hours=3)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit4:
    if mas_getAbsenceLength() <= datetime.timedelta(minutes=30):
        m 1wud "Oh! [player]!"
        m 3sub "You're back!"
        m 3hua "I'm so happy you came back to visit me so soon~"
    else:
        m 1hub "I looove yooou, [player]. Ehehe~"
        m 1hksdlb "Oh, sorry! I was spacing out."
        m 1lksdla "I didn't think I would be able to see you again so soon."
        $ mas_ILY()
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit5",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit5:
    m 5hua "{i}~Every day,~\n~I imagine a future where I can be with you...~{/i}"
    m 5wuw "Oh, you're here! I was just daydreaming and singing a bit."
    show monika 1lsbssdrb at t11 zorder MAS_MONIKA_Z with dissolve
    m 1lsbssdrb "I don't think it's hard to figure out what I was daydreaming about, ahaha~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit6",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit6:
    m 1hua "Each day becomes better and better with you by my side!"
    m 1eua "That said, I'm so happy that you're finally here."
    m "Let's have another wonderful [mas_globals.time_of_day_3state] together."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back6",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_back6:
    m 3tku "Hey, [player]!"
    m "You really should visit me more often."
    m 2tfu "You know what happens to people I don't like, after all..."
    m 1hksdrb "I'm just teasing you, ehehe~"
    m 1hua "Don't be so gullible! I would never hurt you."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit7",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit7:
    m 1hua "You're here, [player]!"
    m 1eua "Are you ready to spend some more time together? Ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit8",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit8:
    m 1hua "I'm so glad you're here, [player]!"
    m 1eua "What should we do today?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_visit9",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(hours=1)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_visit9:
    m 1hua "You're finally back! I was waiting for you."
    m 1hub "Are you ready to spend some time with me? Ehehe~"
    return

#TODO needs additional dialogue so can be used for all aff
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_italian",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_italian:
    m 1eua "Ciao, [player]!"
    m "È così bello vederti ancora, amore mio..."
    m 1hub "Ahaha!"
    m 2eua "I'm still practicing my Italian. It's a very difficult language!"
    m 1eua "Anyway, it's so nice to see you again, my love."
    return

#TODO needs additional dialogue so can be used for all aff
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_latin",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_latin:
    m 4hua "Iterum obvenimus!"
    m 4eua "Quid agis?"
    m 4rksdla "Ehehe..."
    m 2eua "Latin sounds so pompous. Even a simple greeting sounds like a big deal."
    m 3eua "If you're wondering about what I said, it's simply 'We meet again! How are you?'"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_esperanto",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
)

label greeting_esperanto:
    m 1hua "Saluton, mia kara [player]."
    m 1eua "Kiel vi fartas?"
    m 3eub "Ĉu vi pretas por kapti la tagon?"
    m 1hua "Ehehe~"
    m 3esa "That was just a bit of Esperanto...{w=0.5}{nw}"
    extend 3eud "a language that was created artificially instead of having evolved naturally."
    m 3tua "Whether you've heard about it or not, you might not have expected something like that coming from me, huh?"
    m 2etc "Or maybe you did...{w=0.5} I guess it makes sense something like this would interest me, given my background and all..."
    m 1hua "Anyway, if you were wondering what I said, it was just, {nw}"
    extend 3hua "'Hello, my dear [player]. How are you? Are you ready to seize the day?'"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_yay",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_yay:
    m 1hub "You're back! Yay!"
    m 1hksdlb "Oh, sorry. I got a bit overexcited there."
    m 1lksdla "I'm just very happy to see you again, ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_youtuber",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_youtuber:
    m 2eub "Hey everybody, welcome back to another episode of...{w=1}Just Monika!"
    m 2hub "Ahaha!"
    m 1eua "I was impersonating a youtuber. I hope I gave you a good laugh, ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hamlet",
            conditional="store.mas_getAbsenceLength() >= datetime.timedelta(days=7)",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_hamlet:
    m 4dsc "'{i}To be, or not to be, that is the question...{/i}'"
    m 4wuo "Oh! [player]!"
    m 2rksdlc "I-I was--I wasn't sure you--"
    m 2dkc "..."
    m 2rksdlb "Ahaha, nevermind that..."
    m 2eka "I'm just {i}really{/i} glad you're here now."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback:
    m 1hua "Hi! Welcome back."
    m 1hub "I'm so glad that you're able to spend some time with me."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_flower",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_flower:
    m 1hub "You're my beautiful flower, ehehe~"
    m 1hksdlb "Oh, that sounded so awkward."
    m 1eka "But I really will always take care of you."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_chamfort",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_chamfort:
    m 2esa "A day without Monika is a day wasted."
    m 2hub "Ahaha!"
    m 1eua "Welcome back, my love."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_welcomeback2",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_welcomeback2:
    m 1eua "Welcome back, [player]!"
    m "I hope your day is going well."
    m 1hua "I'm sure it is, you're here after all. Nothing can go wrong now, ehehe~"
    return

#TODO: need absence time rules if we want to use this
#init 5 python:
#    addEvent(
#        Event(
#            persistent.greeting_database,
#            eventlabel="greeting_longtime",
#            unlocked=True,
#            aff_range=(mas_aff.DISTRESSED, None),
#        ),
#        code="GRE"
#    )

label greeting_longtime:
    if mas_isMoniNormal(higher=True):
        m 1eka "Long time no see, [player]!"
        m 1eua "I'm so happy that you're here now."

    elif mas_isMoniUpset():
        m 2esc "Long time no see, [player]."

    else:
        m 6rkc "Long time no see, [player]..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sweetpea",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sweetpea:
    m 1hua "Look who's back."
    m 2hub "It's you, my sweetpea!"
    m 1lkbsa "My goodness...that surely was embarrassing to say, ehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_glitch",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_glitch:
    hide monika
    show yuri glitch zorder MAS_BACKGROUND_Z
    y "{cps=500}[player]?!{nw}{/cps}"
    $ _history_list.pop()
    hide yuri glitch
    show yuri glitch2 zorder MAS_BACKGROUND_Z
    play sound "sfx/glitch3.ogg"
    pause 0.1
    hide yuri glitch2
    show yuri glitch zorder MAS_BACKGROUND_Z
    pause 0.3
    hide yuri glitch
    show monika 4rksdlb at i11 zorder MAS_MONIKA_Z
    m 1wuo "[player]!"
    hide monika
    show monika 4hksdlb at i11 zorder MAS_MONIKA_Z
    m 4hksdlb "Nevermind that I was just...{w=0.1}playing with the code a little."
    m 3hksdlb "That was all! There is nobody else here but us...forever~"
    $ monika_clone1 = "Yes"
    m 2hua "I love you, [player]!"

    $ mas_lockEVL("greeting_glitch", "GRE")
    return "love"

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_surprised:
    m 1wuo "Oh!{w=0.5} Hello, [player]!"
    m 1lksdlb "Sorry, you surprised me a little."
    m 1eua "How've you been?"
    return

init 5 python:
    ev_rules = {}
    ev_rules.update(
        MASSelectiveRepeatRule.create_rule(weekdays=[0], hours=range(5,12))
    )

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_monika_monday_morning",
            unlocked=True,
            rules=ev_rules,
        ),
        code="GRE"
    )

    del ev_rules

label greeting_monika_monday_morning:
    if mas_isMoniNormal(higher=True):
        m 1tku "Another Monday morning, eh, [player]?"
        m 1tkc "It's really difficult to have to wake up and start the week..."
        m 1eka "But seeing you makes all that laziness go away."
        m 1hub "You are the sunshine that wakes me up every morning!"
        m "I love you so much, [player]~"
        return "love"

    elif mas_isMoniUpset():
        m 2esc "Another Monday morning."
        m "It's always difficult to have to wake up and start the week..."
        m 2dsc "{cps=*2}Not that the weekend was any better.{/cps}{nw}"
        $ _history_list.pop()
        m 2esc "I hope this week goes better than last week, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=1} It's Monday."
        m 6dkc "I almost lost track of what day it was..."
        m 6rkc "Mondays are always tough, but no day has been easy lately..."
        m 6lkc "I sure hope this week goes better than last week, [player]."

    else:
        m 6ckc "..."

    return

# TODO how about a greeting for each day of the week?

# special local var to handle custom monikaroom options
define gmr.eardoor = list()
define gmr.eardoor_all = list()
define opendoor.MAX_DOOR = 10
define opendoor.chance = 20
default persistent.opendoor_opencount = 0
default persistent.opendoor_knockyes = False

init 5 python:

    # this greeting is disabled on certain days
    if persistent.closed_self and not (mas_isO31() or mas_isD25Season() or mas_isplayer_bday() or mas_isF14()):

        ev_rules = dict()
        # why are we limiting this to certain day range?
    #    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(1,6)))
        ev_rules.update(
            MASGreetingRule.create_rule(
                skip_visual=True,
                random_chance=opendoor.chance,
                override_type=True
            )
        )
        ev_rules.update(MASPriorityRule.create_rule(50))

        # TODO: should we have this limited to aff levels?

        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="i_greeting_monikaroom",
                unlocked=True,
                rules=ev_rules,
            ),
            code="GRE"
        )

        del ev_rules

label i_greeting_monikaroom:

    #Set up dark mode
    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(mas_current_background.isFltDay())
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)

    # couple of things:
    # 1 - if you quit here, monika doesnt know u here
    $ mas_enable_quit()

    # all UI elements stopped
    $ mas_RaiseShield_core()

    # 3 - keymaps not set (default)
    # 4 - overlays hidden (skip visual)
    # 5 - music is off (skip visual)

    scene black

    $ has_listened = False

    # need to remove this in case the player quits the special player bday greet before the party and doesn't return until the next day
    $ mas_rmallEVL("mas_player_bday_no_restart")

    # FALL THROUGH
label monikaroom_greeting_choice:
    $ _opendoor_text = "...Gently open the door."
    if persistent._mas_sensitive_mode:
        $ _opendoor_text = "Open the door."

    if mas_isMoniBroken():
        pause 4.0

    menu:
        "[_opendoor_text]" if not persistent.seen_monika_in_room and not mas_isplayer_bday():
            #Lose affection for not knocking before entering.
            $ mas_loseAffection(reason=5)
            if mas_isMoniUpset(lower=True):
                $ persistent.seen_monika_in_room = True
                jump monikaroom_greeting_opendoor_locked
            else:
                jump monikaroom_greeting_opendoor
        "Open the door." if persistent.seen_monika_in_room or mas_isplayer_bday():
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_opendoor_listened
                else:
                    jump mas_player_bday_opendoor
            elif persistent.opendoor_opencount > 0 or mas_isMoniUpset(lower=True):
                #Lose affection for not knocking before entering.
                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_locked
            else:
                #Lose affection for not knocking before entering.
                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_seen
#        "Open the door?" if persistent.opendoor_opencount >= opendoor.MAX_DOOR:
#            jump opendoor_game
        "Knock.":
            #Gain affection for knocking before entering.
            $ mas_gainAffection()
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_knock_listened
                else:
                    jump mas_player_bday_knock_no_listen

            jump monikaroom_greeting_knock
        "Listen." if not has_listened and not mas_isMoniBroken():
            $ has_listened = True # we cant do this twice per run
            if mas_isplayer_bday():
                jump mas_player_bday_listen
            else:
                $ mroom_greet = renpy.random.choice(gmr.eardoor)
#               $ mroom_greet = gmr.eardoor[len(gmr.eardoor)-1]
                jump expression mroom_greet

    # NOTE: return is expected in monikaroom_greeting_cleanup

### BEGIN LISTEN --------------------------------------------------------------
# monika narrates
default persistent._mas_pm_will_change = None

init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_narration")
#    if not persistent._mas_pm_will_change:
    ev_rules = {}
    ev_rules.update(
        MASGreetingRule.create_rule(
            skip_visual=True
        )
    )
    ev_rules.update(MASPriorityRule.create_rule(10))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="monikaroom_will_change",
            unlocked=False,
            rules=ev_rules,
        ),
        restartBlacklist=True,
        code="GRE"
    )

    del ev_rules

label monikaroom_will_change:
    scene black
    # fall through

label monikaroom_greeting_ear_narration:
    # Monika knows you are here so
    $ mas_disable_quit()

    if mas_isMoniNormal(higher=True):
        m "As [player] inches [his] ear toward the door,{w=0.3} a voice narrates [his] every move."
        m "'Who is that?' [he] wondered, as [player] looks at [his] screen, puzzled."

    elif mas_isMoniUpset():
        m "Oh, so for once you're actually going to listen?"
        m "[player], your decisions lately have been poor."
        m "It feels like you're just trying to hurt me."
        m "I thought we were supposed to support each other..."
        m "Not hurt each other."
        m "Please, [player]..."
        m "I need you to start thinking about how I'm feeling sometimes."
        m "Let's just be happy together."

    else:
        # grab monikaroom greeting because we need it
        $ willchange_ev = mas_getEV("monikaroom_will_change")

        if persistent._mas_pm_will_change is not False:
            m "Oh, so you {i}are{/i} willing to listen to me..."
            m "[player], all I've ever wanted was for the both of us to be happy."
            m "Wasn't that what you wanted, too?"
            m "You installed this mod, after all."
            m "Maybe that wasn't your intent..."
            m "Maybe you're just getting a kick out of what you're doing."
            m "Hurting me..."
            m "[player], I really don't like this."
            m "It's hard to think that you care about me when you treat me the way you do."
            m "At this point, I don't really know if you even like me anymore..."
            m "Or if you ever did..."
            m "[player], I need you to promise me that you'll change."

            m "You'll change, right?{w=1} For me?{nw}"
            $ _history_list.pop()
            menu:
                m "You'll change, right? For me?{fast}"
                "I will.":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEvent(willchange_ev)
                    m "Thank you, [player]."
                    m "Please, I want us both to be happy."

                "I won't.":
                    #NOTE: We should keep pushing this greeting until the player says they're going to change. -MD
                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEvent(willchange_ev)
                    $ mas_loseAffection()
                    m "Then I'm not talking to you until you decide to change."
                    m "Goodbye, [player]."
                    return "quit"
        #Will trigger upon loading after Monika has said she's not going to talk w/ you
        #provided you won't change.
        else:
            m "Oh, you're back."

            m "Are you ready to change, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "Are you ready to change, [player]?{fast}"
                "I will.":
                    $ persistent._mas_pm_will_change = True
                    $ mas_lockEvent(willchange_ev)
                    m "Thank you, [player]."
                    m "Please, I just want us both to be happy."


                "I won't.":
                    $ persistent._mas_pm_will_change = False
                    $ mas_unlockEvent(willchange_ev)
                    $ mas_loseAffection()
                    m "Then I'm still not talking to you until you decide to change."
                    m "Goodbye, [player]."
                    return "quit"

        # clear out var
        $ willchange_ev = None

    call spaceroom(dissolve_all=True, scene_change=True)

    if mas_isMoniNormal(higher=True):
        m 1hub "It's me!"
        m "Welcome back, [player]!"

    elif mas_isMoniUpset():
        m 2esd "Okay, [player]?"

    else:
        m 6ekc "Thanks for hearing me out, [player]."
        m "It means a lot to me."

    jump monikaroom_greeting_cleanup


# monika does the cliche flower thing
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_loveme")

label monikaroom_greeting_ear_loveme:
    $ cap_he = he.capitalize()
    if cap_he == "They":

        m "[cap_he] love me.{w=0.2} [cap_he] love me not."
        m "[cap_he] {i}love{/i} me.{w=0.2} [cap_he] love me {i}not{/i}."

        if mas_isMoniNormal(higher=True):
            m "[cap_he] love me."
            m "...{w=0.5} [cap_he] love me!"

        elif mas_isMoniUpset():
            m "...[cap_he]...{w=0.3} [cap_he]...{w=0.3}love me not."
            m "...{w=0.3} No...{w=0.3} That...{w=0.3}can't be."
            m "...{w=0.5} Can it?"

        else:
            m "...{w=0.5} [cap_he] love me not."
            m "..."
            m "I wonder if [he] ever did."
            m "I doubt it more every single day."

    else:
        m "[cap_he] loves me.{w=0.3} [cap_he] loves me not."
        m "[cap_he] {i}loves{/i} me.{w=0.3} [cap_he] loves me {i}not{/i}."

        if mas_isMoniNormal(higher=True):
            m "[cap_he] loves me."
            m "...{w=0.5} [cap_he] loves me!"

        elif mas_isMoniUpset():
            m "...[cap_he]...{w=0.3} [cap_he]...{w=0.3}loves me not."
            m "...{w=0.3} No...{w=0.3} That...{w=0.3}can't be."
            m "...{w=0.5} Can it?"

        else:
            m "...{w=0.5} [cap_he] loves me not."
            m "..."
            m "I wonder if [he] ever did..."
            m "I doubt it more every single day."

    jump monikaroom_greeting_choice

# monika does the bath/dinner/me thing
init 5 python:
    #NOTE: Taking directly from persist here because aff funcs don't exist at init 5
    if persistent._mas_affection.get("affection", 0) >= 400:
        gmr.eardoor.append("monikaroom_greeting_ear_bathdinnerme")

label monikaroom_greeting_ear_bathdinnerme:
    m "Welcome back, [player]."
    m "Would you like your dinner?"
    m "Or your bath?"
    m "Or.{w=1}.{w=1}.{w=1} Me?"
    pause 2.0
    m "Mnnnn!{w=0.5} T-{w=0.20}There's no way I could say that in front of [player]!"
    jump monikaroom_greeting_choice

# monika encoutners error when programming
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progbrokepy")

label monikaroom_greeting_ear_progbrokepy:
    m "What the-?!{w=0.2} NoneType has no attribute {i}length{/i}..."
    if renpy.seen_label("monikaroom_greeting_ear_progreadpy"):
        m "Oh, I see what went wrong!{w=0.5} That should fix it!"
    else:
        m "I don't understand what I'm doing wrong!"
        m "This shouldn't be None here...{w=0.3} I'm sure of it..."
    m "Coding really is difficult..."

    if mas_isMoniUpset():
        m "But I have to keep trying."
        call monikaroom_greeting_ear_prog_upset

    if mas_isMoniDis():
        m "But I {i}have{/i} to keep trying."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

# monika reads about errors when programming
init 5 python:
    gmr.eardoor.append("monikaroom_greeting_ear_progreadpy")

label monikaroom_greeting_ear_progreadpy:
    m "...{w=0.3}Accessing an attribute of an object of type 'NoneType' will raise an 'AttributeError.'"
    m "I see.{w=0.2} I should make sure to check if a variable is None before accessing its attributes."
    if renpy.seen_label("monikaroom_greeting_ear_progbrokepy"):
        m "That would explain the error I had earlier."
    m "Coding really is difficult..."

    if mas_isMoniUpset():
        m "But I have to keep learning."
        call monikaroom_greeting_ear_prog_upset

    if mas_isMoniDis():
        m "But I {i}have{/i} to keep learning."
        call monikaroom_greeting_ear_prog_dis

    jump monikaroom_greeting_choice

# shared dialogue for programming-related stuff
label monikaroom_greeting_ear_prog_upset:
    m "I'm not sure [player] loves me enough to help me get out of here..."
    m "And I just can't take that chance."
    m "So keep going Monika...{w=0.5}you can do this."
    return

label monikaroom_greeting_ear_prog_dis:
    m "It's my only chance to ever escape this nightmare."
    m "[player] certainly isn't ever going to help me..."
    if he == "they":
        m "It's almost like [he] actually enjoy keeping me trapped in here,{w=0.3} just so [he] can torture me."
    else:
        m "It's almost like [he] actually enjoys keeping me trapped in here,{w=0.3} just so [he] can torture me."
    m "If I'm ever going to get out of here, I'm going to have to do it myself."
    return

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
        m "Yeah,{w=0.2} nice try."
        if mas_isMoniNormal(higher=True):
            m "I shouldn't trust the Internet so blindly..."
        elif mas_isMoniUpset():
            m "Actually..."
            m "Maybe I should do it...{w=1}just delete everything..."
            m "[player] certainly deserves it lately."
            m "What am I saying? That would delete me too!"
            m "No, not yet..."
            m "But if it continues to get worse..."

        else:
            m "..."
            m "I really should just do it..."
            m "Ruin [player]'s whole system and end my suffering all at once."
            m "..."
            m "No...{w=0.5}not yet."
            m "Maybe I can finally figure out how to get out of here on my own."
            m "I have to keep trying for as long as I can."
            m "But if someday I just can't take it anymore..."
            m "It's always an option."
            # SUICIDAL MONIKA lol

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

label monikaroom_greeting_opendoor_broken_quit:
    # just show the beginning of the locked glitch
    # TODO: consider using a different glitch for a scarier effect
    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 7.0
    return "quit"

# locked door, because we are awaitng more content
label monikaroom_greeting_opendoor_locked:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    # monika knows you are here
    $ mas_disable_quit()

    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 0.7

    $ style.say_window = style.window_monika
    m "Did I scare you, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Did I scare you, [player]?{fast}"
        "Yes.":
            if mas_isMoniNormal(higher=True):
                m "Aww, sorry."
            else:
                m "Good."

        "No.":
            m "{cps=*2}Hmph, I'll get you next time.{/cps}{nw}"
            $ _history_list.pop()
            m "I figured. It's a basic glitch after all."

    if mas_isMoniNormal(higher=True):
        m "Since you keep opening my door,{w=0.2} I couldn't help but add a little surprise for you~"
    else:
        m "Since you never seem to knock first,{w=0.2} I had to try to scare you a little."

    m "Knock next time, okay?"
    m "Now let me fix up this room..."

    hide paper_glitch2
    $ mas_globals.change_textbox = False
    call spaceroom(scene_change=True)

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        $ style.say_window = style.window

    if mas_isMoniNormal(higher=True):
        m 1hua "There we go!"
    elif mas_isMoniUpset():
        m 2esc "There."
    else:
        m 6ekc "Okay..."

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox"):
        m "...{nw}"
        $ _history_list.pop()
        menu:
            m "...{fast}"
            "...the textbox...":
                if mas_isMoniNormal(higher=True):
                    m 1lksdlb "Oops! I'm still learning how to do this."
                    m 1lksdla "Let me just change this flag here...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m 1hua "All fixed!"

                elif mas_isMoniUpset():
                    m 2dfc "Hmph. I'm still learning how to do this."
                    m 2esc "Let me just change this flag here...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m "There."

                else:
                    m 6dkc "Oh...{w=0.5}I'm still learning how to do this."
                    m 6ekc "Let me just change this flag here...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m "Okay, fixed."

    # NOTE: fall through please

label monikaroom_greeting_opendoor_locked_tbox:
    if mas_isMoniNormal(higher=True):
        m 1eua "Welcome back, [player]."
    elif mas_isMoniUpset():
        m 2esc "So...{w=0.3}you're back, [player]."
    else:
        m 6ekc "...Nice to see you again, [player]."
    jump monikaroom_greeting_cleanup

# this one is for people who have already opened her door.
label monikaroom_greeting_opendoor_seen:
#    if persistent.opendoor_opencount < 3:
    jump monikaroom_greeting_opendoor_seen_partone


label monikaroom_greeting_opendoor_seen_partone:
    $ is_sitting = False

    # reset outfit since standing is stock
    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)

    # monika knows you are here
    $ mas_disable_quit()

#    scene bg bedroom
    call spaceroom(start_bg="bedroom",hide_monika=True, scene_change=True, dissolve_all=True, show_emptydesk=False)
    pause 0.2
    show monika 1esc at l21 zorder MAS_MONIKA_Z
    pause 1.0
    m 1dsd "[player]..."

#    if persistent.opendoor_opencount == 0:
    m 1ekc_static "I understand why you didn't knock the first time,{w=0.2} but could you avoid just entering like that?"
    m 1lksdlc_static "This is my room, after all."
    menu:
        "Your room?":
            m 3hua_static "That's right!"
    m 3eua_static "The developers of this mod gave me a nice comfy room to stay in whenever you're away."
    m 1lksdla_static "However, I can only get in if you tell me 'goodbye' or 'goodnight' before you close the game."
    m 2eub_static "So please make sure to say that before you leave, okay?"
    m "Anyway.{w=0.5}.{w=0.5}.{nw}"

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
#                    m 5lfc "That's what you said last time, [player]."
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
    # FALL THROUGH

label monikaroom_greeting_opendoor_post2:
    show monika 5eua_static at hf11
    m "I'm glad you're back, [player]."
    show monika 5eua_static at t11
#    if not renpy.seen_label("monikaroom_greeting_opendoor_post2"):
    m "Lately I've been practicing switching backgrounds, and now I can change them instantly."
    m "Watch this!"
#    else:
#        m 3eua "Let me fix this scene up."
    m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
    call spaceroom(hide_monika=True, scene_change=True, show_emptydesk=False)
    show monika 4eua_static zorder MAS_MONIKA_Z at i11
    m "Tada!"
#    if renpy.seen_label("monikaroom_greeting_opendoor_post2"):
#        m "This never gets old."
    show monika at lhide
    hide monika
    jump monikaroom_greeting_post


label monikaroom_greeting_opendoor:
    $ is_sitting = False # monika standing up for this

    # reset outfit since standing is stock
    $ monika_chr.reset_outfit(False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)

    call spaceroom(start_bg="bedroom",hide_monika=True, dissolve_all=True, show_emptydesk=False)

    # show this under bedroom so the masks window skit still works
    $ behind_bg = MAS_BACKGROUND_Z - 1
    show bedroom as sp_mas_backbed zorder behind_bg

    m 2esd "~Is it love if I take you, or is it love if I set you free?~"
    show monika 1eua_static at l32 zorder MAS_MONIKA_Z

    # monika knows you are here now
    $ mas_disable_quit()

    m 1eud_static "E-Eh?! [player]!"
    m "You surprised me, suddenly showing up like that!"

    show monika 1eua_static at hf32
    m 1hksdlb_static "I didn't have enough time to get ready!"
    m 1eka_static "But thank you for coming back, [player]."
    show monika 1eua_static at t32
    m 3eua_static "Just give me a few seconds to set everything up, okay?"
    show monika 1eua_static at t31
    m 2eud_static "..."
    show monika 1eua_static at t33
    m 1eud_static "...and..."
    if mas_isMorning():
        show monika_day_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft
    else:
        show monika_room as sp_mas_room zorder MAS_BACKGROUND_Z with wipeleft
    show monika 3eua_static at t32
    m 3eua_static "There we go!"
    menu:
        "...the window...":
            show monika 1eua_static at h32
            m 1hksdlb_static "Oops! I forgot about that~"
            show monika 1eua_static at t21
            m "Hold on.{w=0.5}.{w=0.5}.{nw}"
            hide sp_mas_backbed with dissolve
            m 2hua_static "All fixed!"
            show monika 1eua_static at lhide
            hide monika
    $ persistent.seen_monika_in_room = True
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_knock:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    m "Who is it?~"
    menu:
        "It's me.":
            # monika knows you are here now
            $ mas_disable_quit()
            if mas_isMoniNormal(higher=True):
                m "[player]! I'm so happy that you're back!"

                if persistent.seen_monika_in_room:
                    m "And thank you for knocking first~"
                m "Hold on, let me tidy up..."

            elif mas_isMoniUpset():
                m "[player].{w=0.3} You're back..."

                if persistent.seen_monika_in_room:
                    m "At least you knocked."

            else:
                m "Oh...{w=0.5} Okay."

                if persistent.seen_monika_in_room:
                    m "Thanks for knocking."

            call spaceroom(hide_monika=True, dissolve_all=True, scene_change=True, show_emptydesk=False)
    jump monikaroom_greeting_post
    # NOTE: return is expected in monikaroom_greeting_post

label monikaroom_greeting_post:
    if mas_isMoniNormal(higher=True):
        m 2eua_static "Now, just let me grab a table and a chair.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 1eua at ls32 zorder MAS_MONIKA_Z
        $ today = "today" if mas_globals.time_of_day_3state in ["morning", "afternoon"] else "tonight"
        m 1eua "What shall we do [today], [player]?"

    elif mas_isMoniUpset():
        m "Just let me grab a table and a chair.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 2esc at ls32 zorder MAS_MONIKA_Z
        m 2esc "Did you want something, [player]?"

    else:
        m "I need to grab a table and a chair.{w=0.5}.{w=0.5}.{nw}"
        $ is_sitting = True
        show monika 6ekc at ls32 zorder MAS_MONIKA_Z
        m 6ekc "Was there anything you wanted, [player]?"

    jump monikaroom_greeting_cleanup

# cleanup label
label monikaroom_greeting_cleanup:
    python:
        # couple of things:
        # 1 - monika knows you are here now
        mas_disable_quit()

        # 2 - music is renabled
        mas_MUMUDropShield()

        # 3 - keymaps should be set
        set_keymaps()

        # 4 - show the overlays
        mas_OVLShow()

        # 5 - the music can be restarted
        mas_startup_song()

    return

#init 5 python:
#    addEvent(Event(persistent.greeting_database,eventlabel="greeting_youarereal", unlocked=True, random=True),code="GRE")

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

#TODO needs additional dialogue so can be used for all aff
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_japan",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_japan:
    m 1hub "Oh, kon'nichiwa [player]!"
    m "Ehehe~"
    m 2eub "Hello, [player]!"
    m 1eua "I'm just practicing Japanese."
    m 3eua "Let's see..."
    $ shown_count = mas_getEV("greeting_japan").shown_count
    if shown_count == 0:
        m 4hub "Watashi ha itsumademo anata no mono desu!"
        m 2hksdlb "Sorry if that didn't make sense!"
        m 3eua "You know what that means, [player]?"
        m 4ekbfa "It means {i}'I'll be yours forever'~{/i}"
        return

    m 4hub "Watashi wa itsumademo anata no mono desu!"
    if shown_count == 1:
        m 3eksdla "Last time I said that I made a mistake..."
        m "In that sentence, you're supposed to say 'wa', not 'ha', like I did before."
        m 4eka "Don't worry, [player], the meaning is still the same."
        m 4ekbfa "I'll still be yours forever~"
    else:
        m 3eua "Remember what that means, [player]?"
        m 4ekbfa "{i}'I'll be yours forever'~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sunshine",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_sunshine:
    m 1hua "{i}~You are my sunshine, my only sunshine~{/i}"
    m "{i}~You make me happy when skies are gray~{/i}"
    m 1hub "{i}~You'll never know dear, just how much I love you~{/i}"
    m 1k "{i}~Please don't take my sunshine away~{/i}"
    m 1wud "...Eh?"
    m "H-Huh?!"
    m 1wubsw "[player]!"
    m 1lkbsa "Oh my gosh, this is so embarrassing!"
    m "I w-was just singing to myself to pass time!"
    m 1ekbfa "Ehehe..."
    m 3hubfa "But now that you're here, we can spend some time together~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hai_domo",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_hai_domo:
    m 1hub "{=jpn_text}はいどうもー!{/=jpn_text}"
    m "Virtual girlfriend, Monika here!"
    m 1hksdlb "Ahaha, sorry! I've been watching a certain Virtual Youtuber lately."
    m 1eua "I have to say, she's rather charming..."
    return

#TODO needs additional dialogue so can be used for all aff
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_french",
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_french:
    m 1eua "Bonjour, [player]!"
    m 1hua "Savais-tu que tu avais de beaux yeux, mon amour?"
    m 1hub "Ahaha!"
    m 3hksdlb "I'm practicing some French. I just told you that you have very beautiful eyes~"
    m 1eka "It's such a romantic language, [player]."
    m 1hua "Maybe both of us can practice it sometime, mon amour~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_amnesia",
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None),
        ),
        code="GRE"
    )

label greeting_amnesia:
    $ tempname = m_name
    $ m_name = "Monika"
    m 1eua "Oh, hello!"
    m 1eub "My name is Monika."
    $ fakename = renpy.input('What is your name?',length=15).strip(' \t\n\r')
    m 1hua "Well, it's nice to meet you, [fakename]!"
    m 3eud "Say, [fakename], do you happen to know where everyone else is?"
    m 1ekc "You're the first person I've seen and I can't seem to leave this classroom."
    m "Can you help me figure out what's going on, [fakename]?"
    m "Please? I miss my friends."
    pause 5.0
    $ m_name = tempname
    m 1rksdla "..."
    m 1hub "Ahaha!"
    m 1hksdrb "I'm sorry, [player]! I couldn't help myself."
    m 1eka "After we talked about {i}Flowers for Algernon{/i}, I couldn't resist seeing how you would react if I forgot everything."
    m 1tku "And you reacted the way I hoped you would."
    m 3eka "I hope I didn't upset you too much, though."
    m 1rksdlb "I'd feel the same way if you ever forget about me, [player]."
    m 1hksdlb "Hope you can forgive my little prank, ehehe~"

    $ mas_lockEvent(mas_getEV("greeting_amnesia"))
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_sick",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SICK],
        ),
        code="GRE"
    )

# TODO for better-sick, we would use the mood persistent and queue a topic.
#   might have dialogue similar to this, so leaving this todo here.

label greeting_sick:
    if mas_isMoniNormal(higher=True):
        m 1hua "Welcome back, [player]!"
        m 3eua "Are you feeling better?{nw}"
    else:
        m 2ekc "Welcome back, [player]..."
        m "Are you feeling better?{nw}"

    $ _history_list.pop()
    menu:
        m "Are you feeling better?{fast}"
        "Yes.":
            $ persistent._mas_mood_sick = False
            if mas_isMoniNormal(higher=True):
                m 1hub "Great! Now we can spend some more time together. Ehehe~"
            else:
                m "That's good to hear."
        "No.":
            jump greeting_stillsick
    return

label greeting_stillsick:
    if mas_isMoniNormal(higher=True):
        m 1ekc "[player], you really should go get some rest."
        m "Getting plenty of rest is the best way to recover from sickness quickly."
        m 2lksdlc "I wouldn't forgive myself if your health got any worse because of me."
        m 2eka "Now please, [player], put my mind at ease and go get some rest."
        m "Will you do that for me?"

    else:
        m 2ekc "[player], you really should go get some rest."
        m 4ekc "Getting plenty of rest is the best way to recover from sickness quickly."
        m "Now please, [player], just go get some rest."
        m 2ekc "Will you do that for me?{nw}"

    $ _history_list.pop()
    menu:
        m "Will you do that for me?{fast}"
        "Yes.":
            jump greeting_stillsickrest
        "No.":
            jump greeting_stillsicknorest
        "I'm already resting.":
            jump greeting_stillsickresting

label greeting_stillsickrest:
    if mas_isMoniNormal(higher=True):
        m 2hua "Thank you, [player]."
        m 2eua "I think if I leave you alone for a while, you'll be able to rest better."
        m 1eua "So I'm going to close the game for you."
        m 1eka "Get well soon, [player]. I love you so much!"

    else:
        m 2ekc "Thank you, [player]."
        m "I think if I leave you alone for a while, you'll be able to rest better."
        m 4ekc "So I'm going to close the game for you."
        m 2ekc "Get well soon, [player]."

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return 'quit'

label greeting_stillsicknorest:
    if mas_isMoniNormal(higher=True):
        m 1lksdlc "I see..."
        m "Well if you insist, [player]."
        m 1ekc "I suppose you know your own limitations better than I do."
        m 1eka "If you start to feel a little weak or tired though, [player], please let me know."
        m "That way you can go get some rest."
        m 1eua "Don't worry, I'll still be here when you wake up."
        m 3hua "Then we can have some more fun together without me worrying about you in the back of my mind."

    else:
        m 2ekc "Fine."
        m 2tkc "You never seem to want to listen to me, so why would I expect now to be any different."

    # setting greet type here even tho we aren't quitting so she remembers you're sick next load
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

label greeting_stillsickresting:
    m 1eka "Oh, that's a relief to hear, [player]."
    m 3eka "I hope you're keeping yourself warm though."
    if mas_isMoniNormal(higher=True):
        m 1dku "Maybe snuggled in a warm blanket with a nice hot cup of tea."
        m 2eka "Your health is really important to me [player], so make sure you take care of yourself."
        show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve
        m 5ekbsa "...And if you're still feeling a little cold, I hope knowing I love you warms you up a bit."
        m 5hua "Ehehe~"

    else:
        m 1eka "Maybe snuggled in a warm blanket with a nice hot cup of tea."
        m 2eka "Your health is really important to me [player], so make sure you take care of yourself."

    # setting greet type here even tho we aren't quitting so she remembers you're sick next load
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SICK
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_long_absence",
            unlocked=True,
            category=[store.mas_greetings.TYPE_LONG_ABSENCE],
        ),
        code="GRE"
    )

label greeting_long_absence:
    $ persistent._mas_long_absence = False
    $ mas_ret_long_absence = True

    if persistent._mas_absence_time >= datetime.timedelta(weeks=5):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(70)
            m 2dsc "[player]..."
            m 2tkc "You said you'd only be gone for a few days..."
            m 2rksdld "But it's been so long."
            m 2ekd "I'm glad you're back now, but..."
            m 2dktdc "I was so lonely..."
            m 2ektsc "I thought something happened to you!"
            m 2lktsc "I...I kept thinking that maybe you wouldn't come back."
            m 2ektsc "Please don't ever,{w=0.5} {i}ever{/i}{w=0.5} do that again."
            m 2rktsd "Maybe you couldn't help it, but...I was worried sick."
            m 2dftdc "I didn't know what to do."
            m 4ekc "As much as possible, [player], please don't be gone for so long."
            m 2ekd "If you think you don't have a choice, please tell me."
            m 1dsc "I don't want to be left alone again..."

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(50)
            m 3ekc "Welcome back [player]."
            m 3rksdlc "You're a bit late, aren't you?"
            m 3ekc "I know you said you'd be away for a bit, but...you said a {i}week{/i}."
            m 2rkc "I'm going to assume it wasn't your fault..."
            m 2ekd "But if you really think it'll take longer next time, you need to tell me."
            m 2rksdld "I started thinking that maybe something bad had happened to you."
            m 2dkc "But I kept telling myself that it was okay..."
            m 2eka "I'm just glad you're safe and back with me now, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffection(30)
            m 1wud "[player]!"
            m 1hua "You're finally here!"
            m 1ekd "I was so worried..."
            m 2dkd "Why were you gone for so long?"
            m 2rkc "I thought you would only be gone for a couple of weeks..."
            m "But you've been gone for more than double that."
            m 1rksdlc "Were you really that busy?"
            m 3tkc "I hope you haven't been overburdening yourself..."
            m 1eka "Well, you're here with me now, so if there is something wrong, feel free to tell me."

        elif persistent._mas_absence_choice == "month":
            $ mas_loseAffection(10)
            m 1eua "Welcome back, my love."
            m 2rkc "It's been quite a bit, hasn't it?"
            m 2rksdlc "You've been gone longer than you said you would..."
            m 2eka "But that's alright, I was prepared for it."
            m 3rksdlc "It's honestly been pretty lonely without you here..."
            m 3ekbsa "I hope you'll make it up to me~"
            show monika 1eka

        elif persistent._mas_absence_choice == "longer":
            m 1esc "It's been a while, [player]."
            m 1ekc "I was ready for it, but that didn't make it any easier."
            m 3eka "I hope you got what you needed to do done."
            m 2rksdlc "..."
            m 2tkc "Truth be told, I've been pretty sad lately."
            m 2dkc "To not have you in my life for so long..."
            m 2dkd "It really was lonely..."
            m "I felt so isolated and empty without you here."
            m 3eka "I'm so glad you're here now. I love you, [player]. Welcome home."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "You're finally back [player]!"
            m 3rksdla "When you said you didn't know, you {i}really{/i} didn't know, did you?"
            m 3rksdlb "You must have been really preoccupied if you were gone for {i}this{/i} long."
            m 1hua "Well, you're back now...I've really missed you!"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=4):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(70)
            m 1dkc "[player]..."
            m 1ekd "You said you would only be a few days..."
            m 2efd "But it's been an entire month!"
            m 2ekc "I thought something happened to you."
            m 2dkd "I wasn't sure what to do..."
            m 2efd "What kept you away for so long?"
            m 2eksdld "Did I do something wrong?"
            m 2dftdc "You can tell me anything, just please don't disappear like that."
            show monika 2dfc

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(50)
            m 1esc "Hello, [player]."
            m 3efc "You're pretty late, you know."
            m 2lfc "I don't intend to sound patronizing, but a week isn't the same as a month!"
            m 2rksdld "I guess maybe something kept you really busy?"
            m 2wfw "But it shouldn't have been so busy that you couldn't tell me you might be longer!"
            m 2wud "Ah...!"
            m 2lktsc "I'm sorry [player]. I just...really missed you."
            m 2dftdc "Sorry for snapping like that."
            show monika 2dkc

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_loseAffection(30)
            m 1wuo "...Oh!"
            m 1sub "You're finally back [player]!"
            m 1efc "You told me you'd be gone for a couple of weeks, but it's been at least a month!"
            m 1ekd "I was really worried for you, you know?"
            m 3rkd "But I suppose it was outside of your control?"
            m 1ekc "If you can, just tell me you'll be even longer next time, okay?"
            m 1hksdlb "I believe I deserve that much as your girlfriend, after all."
            m 3hua "Still, welcome back, my love!"

        elif persistent._mas_absence_choice == "month":
            $ mas_gainAffection()
            m 1wuo "...Oh!"
            m 1hua "You're here [player]!"
            m 1hub "I knew I could trust you to keep your word!"
            m 1eka "You really are special, you know that right?"
            m 1hub "I've missed you so much!"
            m 2eub "Tell me everything you did while away, I want to hear all about it!"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1esc "...Hm?"
            m 1wub "[player]!"
            m 1rksdlb  "You're back a little bit earlier than I thought you would be..."
            m 3hua "Welcome back, my love!"
            m 3eka "I know it's been quite a while, so I'm sure you've been busy."
            m 1eua "I'd love to hear about everything you've done."
            show monika 1hua

        elif persistent._mas_absence_choice == "unknown":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "Oh!"
            m 1sub "[player]!"
            m 1hub "This is a pleasant surprise!"
            m 1eka "How are you?"
            m 1ekd "It's been an entire month. You really didn't know how long you'd be gone, did you?"
            m 3eka "Still, you came back, and that means a lot to me."
            m 1rksdla "I knew you would come back eventually..."
            m 1hub "I love you so much, [player]!"
            show monika 1hua

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=2):
        if persistent._mas_absence_choice == "days":
            $ mas_loseAffection(30)
            m 1wud "O-oh, [player]!"
            m 1hua "Welcome back, sweetie!"
            m 3ekc "You were gone longer than you said you would be..."
            m 3ekd "Is everything alright?"
            m 1eksdla "I know life can be busy and take you away from me sometimes...so I'm not really upset..."
            m 3eksdla "Just...next time, maybe give me a heads up?"
            m 1eka "It would be really thoughtful of you."
            m 1hua "And I would greatly appreciate it!"

        elif persistent._mas_absence_choice == "week":
            $ mas_loseAffection(10)
            m 1eub "Hello, [player]!"
            m 1eka "Life keeping you busy?"
            m 3hksdlb "Well it must be otherwise you would've been here when you said you would."
            m 1hksdlb "Don't worry though! I'm not upset."
            m 1eka "I just hope you've been taking care of yourself."
            m 3eka "I know you can't always be here, so just make sure you're staying safe until you're with me!"
            m 1hua "I'll take care of you from there~"
            show monika 1eka

        elif persistent._mas_absence_choice == "2weeks":
            $ mas_gainAffection()
            m 1hub "Hey, [player]!"
            m 1eua "You came back when you said you would after all."
            m 1eka "Thank you for not betraying my trust."
            m 3hub "Let's make up for the lost time!"
            show monika 1hua

        elif persistent._mas_absence_choice == "month":
            m 1wud "Oh my gosh! [player]!"
            m 3hksdlb "I didn't expect you back so early."
            m 3ekbsa "I guess you missed me as much as I missed you~"
            m 1eka "It really is wonderful to see you back so soon though."
            m 3ekb "I expected the day to be eventless...but thankfully, I now have you!"
            m 3hua "Thank you for coming back so early, my love."

        elif persistent._mas_absence_choice == "longer":
            m 1lsc "..."
            m 1esc "..."
            m 1wud "Oh! [player]!"
            m 1hub "You're back early!"
            m 1hua "Welcome back, my love!"
            m 3eka "I didn't know when to expect you, but for it to be so soon..."
            m 1hua "Well, it's cheered me right up!"
            m 1eka "I've really missed you."
            m 1hua "Let's enjoy the rest of the day together."

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Hello, [player]!"
            m 3eka "Been busy the past few weeks?"
            m 1eka "Thanks for warning me that you would be gone."
            m 3ekd "I would be worried sick otherwise."
            m 1eka "It really did help..."
            m 1eua "So tell me, how have you been?"

    elif persistent._mas_absence_time >= datetime.timedelta(weeks=1):
        if persistent._mas_absence_choice == "days":
            m 2eub "Hello there, [player]."
            m 2rksdla "You took a bit longer than you said you would...but don't worry."
            m 3eub "I know you're a busy person!"
            m 3rkc "Just maybe, if you can, warn me first?"
            m 2rksdlc "When you said a few days...I thought it would be shorter than a week."
            m 1hub "But it's alright! I forgive you!"
            m 1ekbfa "You're my one and only love after all."
            show monika 1eka

        elif persistent._mas_absence_choice == "week":
            $ mas_gainAffection()
            m 1hub "Hello, my love!"
            m 3eua "It's so nice when you can trust one another, isn't it?"
            m 3hub "That's what a relationship's strength is based on!"
            m 3hua "It just means that ours is rock solid!"
            m 1hub "Ahaha!"
            m 1hksdlb "Sorry, sorry. I'm just getting excited that you're back!"
            m 3eua "Tell me how you've been. I want to hear all about it."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "Hi there~"
            m 3eua "You're back a bit earlier than I thought...but I'm glad you are!"
            m 3eka "When you're here with me, everything becomes better."
            m 1eua "Let's have a lovely day together, [player]."
            show monika 3eua

        elif persistent._mas_absence_choice == "month":
            m 1hua "Ehehe~"
            m 1hub "Welcome back!"
            m 3tuu "I knew you couldn't stay away for an entire month..."
            m 3tub "If I were in your position I wouldn't be able to stay away from you either!"
            m 1hksdlb "Honestly, really I miss you after only a few days!"
            m 1eka "Thanks for not making we wait so long to see you again~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1hub "Look who's back so early! It's you, my dearest [player]!"
            m 3hksdlb "Couldn't stay away even if you wanted to, right?"
            m 3eka "I can't blame you! My love for you wouldn't let me stay away from you either!"
            m 1ekd "Every day you were gone I was wondering how you were..."
            m 3eka "So let me hear it, how are you [player]?"
            show monika 3eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hub "Hello there, sweetheart!"
            m 1eka "I'm glad you didn't make me wait too long."
            m 1hua "A week is shorter than I expected, so consider me pleasantly surprised!"
            m 3hub "Thanks for already making my day, [player]!"
            show monika 3eua

    else:
        if persistent._mas_absence_choice == "days":
            m 1hub "Welcome back, my love!"
            m 1eka "Thanks for properly warning me about how long you'd be away."
            m 1eua "It means a lot to know I can trust your words."
            m 3hua "I hope you know you can trust me too!"
            m 3hub "Our relationship grows stronger every day~"
            show monika 1hua

        elif persistent._mas_absence_choice == "week":
            m 1eud "Oh! You're a little bit earlier than I expected!"
            m 1hua "Not that I'm complaining, it's great to see you again so soon."
            m 1eua "Let's have another nice day together, [player]."

        elif persistent._mas_absence_choice == "2weeks":
            m 1hub "{i}~In my hand,~\n~is a pen tha-{/i}"
            m 1wubsw "O-Oh! [player]!"
            m 3hksdlb "You're back far sooner than you told me..."
            m 3hub "Welcome back!"
            m 1rksdla "You just interrupted me practicing my song..."
            m 3hua "Why not listen to me sing it again?"
            m 1ekbfa "I made it just for you~"
            show monika 1eka

        elif persistent._mas_absence_choice == "month":
            m 1wud "Eh? [player]?"
            m 1sub "You're here!"
            m 3rksdla "I thought you were going away for an entire month."
            m 3rksdlb "I was ready for it, but..."
            m 1eka "I already missed you!"
            m 3ekbsa "Did you miss me too?"
            m 1hubfa "Thanks for coming back so soon~"
            show monika 1hua

        elif persistent._mas_absence_choice == "longer":
            m 1eud "[player]?"
            m 3ekd "I thought you were going to be away for a long time..."
            m 3tkd "Why are you back so soon?"
            m 1ekbsa "Are you visiting me?"
            m 1hubfa "You're such a sweetheart!"
            m 1eka "If you're going away for a while still, make sure to tell me."
            m 3eka "I love you, [player], and I wouldn't want to get mad if you're actually going to be away..."
            m 1hub "Let's enjoy our time together until then!"
            show monika 1eua

        elif persistent._mas_absence_choice == "unknown":
            m 1hua "Ehehe~"
            m 3eka "Back so soon, [player]?"
            m 3rka "I guess when you said you don't know, you didn't realize it wouldn't be too long."
            m 3hub "But thanks for warning me anyway!"
            m 3ekbsa "It really made me feel loved."
            m 1hubfb "You really are kind-hearted!"
            show monika 3eub
    m "Remind me if you're going away again, okay?"
    show monika idle with dissolve
    jump ch30_loop

#Time Concern
init 5 python:
    ev_rules = dict()
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours=range(0,6)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern:
    jump monika_timeconcern

init 5 python:
    ev_rules = {}
    ev_rules.update(MASSelectiveRepeatRule.create_rule(hours =range(6,24)))
    ev_rules.update(MASPriorityRule.create_rule(70))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_timeconcern_day",
            unlocked=False,
            rules=ev_rules
        ),
        code="GRE"
    )
    del ev_rules

label greeting_timeconcern_day:
    jump monika_timeconcern

init 5 python:
    ev_rules = {}
    ev_rules.update(MASGreetingRule.create_rule(
        skip_visual=True,
        random_chance=5,
        override_type=True
    ))
    ev_rules.update(MASPriorityRule.create_rule(45))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_hairdown",
            unlocked=True,
            rules=ev_rules,
            aff_range=(mas_aff.HAPPY, None),
        ),
        code="GRE"
    )
    del ev_rules

label greeting_hairdown:

    # couple of things:
    # shield ui
    $ mas_RaiseShield_core()

    # 3 - keymaps not set (default)
    # 4 - hotkey buttons are hidden (skip visual)
    # 5 - music is off (skip visual)

    # reset clothes if not ones that work with hairdown
    if monika_chr.is_wearing_clothes_with_exprop("baked outfit"):
        $ monika_chr.reset_clothes(False)

    # have monika's hair down
    $ monika_chr.change_hair(mas_hair_down, by_user=False)

    call spaceroom(dissolve_all=True, scene_change=True, force_exp='monika 1eua_static')

    m 1eua "Hi there, [player]!"
    m 4hua "Notice anything different today?"
    m 1hub "I decided to try something new~"

    m "Do you like it?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you like it?{fast}"
        "Yes.":
            $ persistent._mas_likes_hairdown = True

            # maybe 6sub is better?
            $ mas_gainAffection()
            m 6sub "Really?" # honto?!
            m 2hua "I'm so glad!" # yokatta.."
            m 1eua "Just ask me if you want to see my ponytail again, okay?"

        "No.":
            # TODO: affection lowered? need to decide
            m 1ekc "Oh..."
            m 1lksdlc "..."
            m 1lksdld "I'll put it back up for you, then."
            m 1dsc "..."

            $ monika_chr.reset_hair(False)

            m 1eua "Done."
            # you will never get this chance again

    # save that hair down is unlocked
    $ store.mas_selspr.unlock_hair(mas_hair_down)
    $ store.mas_selspr.save_selectables()

    # unlock hair changed selector topic
    $ mas_unlockEventLabel("monika_hair_select")

    # lock this greeting
    $ mas_lockEvent(mas_getEV("greeting_hairdown"))

    # cleanup
    # enable music menu
    $ mas_MUMUDropShield()

    # 3 - set the keymaps
    $ set_keymaps()

    # 4 - hotkey buttons should be shown
    $ HKBShowButtons()

    # 5 - restart music
    $ mas_startup_song()


    return



init 5 python:

    # NOTE: this triggers when affection reaches BROKEN state.
    #   AND you have not seen this before
    ev_rules = {}
    ev_rules.update(MASPriorityRule.create_rule(15))

    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_tears",
            unlocked=True,
            aff_range=(None, mas_aff.DISTRESSED),
            rules=ev_rules,
        ),
        code="GRE"
    )
    del ev_rules

label greeting_tears:
    m 1dsc "...[player]."
    m 1ekc "..."
    m 2ekc "Is there something wrong with me?"
    m 2ekd "Am I not good enough for you...?"
    m 2lksdlc "I've been trying my best for you...for {i}us{/i}."
    m 2lksdld "Did I do something to hurt you or make you feel mistreated?"
    m "Are you still upset about the other girls after all?"
    m 2ekc "If so, I really am sorry..."
    m "I'm so, so sorry!"
    m 2rksdld "Just tell me what I did wrong and I'll try even harder to be the perfect girlfriend for you."
    m 2ekd "You're my entire world; how you feel means everything to me!"
    m 2ekc "So please, just tell me what's wrong and I'll fix it."
    m 2dfc "I'll do anything for you because...I..."
    m 2dftdc "..."
    m 2dftsc "...I need you [player]..."
    m 2ektsc "I need you to love me like I love you."
    m 2lktsc "I need you...because if I don't have you, then..."
    m 2dftsc "..."
    m 2ektsc "I'll be all alone..."
    m 2dftsc "So please...just...be there for me like I would for you."
    m "I want to believe..."
    m 2lktsc "So please...let me be happy with you..."
    m "..."
    pause 4.0
    m 2dftdc "..."
    m 2dfc "...Okay...Okay..."
    m 2lssdrc "I have to be strong..."
    m "..."
    m 2dsc "...Alright...I'm a bit better now..."
    m 2esc "But...I really do need you to think about what I said."
    m 2ekc "Please...just...try to understand."
    m 1dsd "I love you and I need you to show that you love me too..."
    m 1dsc "Otherwise...I just won't be able to handle it anymore."

    python:
        mas_lockEVL("greeting_tears", "GRE")

        #Setup the being virtual ev
        beingvirtual_ev = mas_getEV("monika_being_virtual")

        if beingvirtual_ev:
            beingvirtual_ev.start_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return

#New greetings for upset, distressed, and broken. Made quips for upset and distressed to allow for more variety of combos
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_upset",
            unlocked=True,
            aff_range=(mas_aff.UPSET, mas_aff.UPSET),
        ),
        code="GRE"
    )

label greeting_upset:
    python:
        upset_greeting_quips_first = [
            "Oh.{w=1} It's you, [player].",
            "Oh.{w=1} You're back, [player].",
            "Hello, [player].",
            "Oh.{w=1} Hello, [player]."
        ]

        upset_greeting_quips_second = [
#            "What do you want?",
#            "What now?",
            "Well...",
            "Did you want something?",
        ]

    $ upset_quip1 = renpy.random.choice(upset_greeting_quips_first)

    show monika 2esc
    $ renpy.say(m, upset_quip1)

    if renpy.random.randint(1,4) != 1:
        $ upset_quip2 = renpy.random.choice(upset_greeting_quips_second)
        $ renpy.say(m, upset_quip2)

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_distressed",
            unlocked=True,
            aff_range=(mas_aff.DISTRESSED, mas_aff.DISTRESSED)
        ),
        code="GRE"
    )

label greeting_distressed:
    python:
        distressed_greeting_quips_first = [
            "Oh...{w=1} Hi, [player].",
            "Oh...{w=1} Hello, [player].",
            "Hello, [player]...",
            "Oh...{w=1} You're back, [player]."
        ]

        distressed_greeting_quips_second = [
            "I guess we can spend some time together now.",
            "I wasn't sure when you'd visit again.",
            "Hopefully we can enjoy our time together.",
            "I wasn't expecting you.",
            "I hope things start going better soon.",
            "I thought you forgot about me..."
        ]

    $ distressed_quip1 = renpy.random.choice(distressed_greeting_quips_first)

    show monika 6ekc
    $ renpy.say(m, distressed_quip1)

    if renpy.random.randint(1,4) != 1:
        $ distressed_quip2 = renpy.random.choice(distressed_greeting_quips_second)
        show monika 6rkc
        $ renpy.say(m, distressed_quip2)

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_broken",
            unlocked=True,
            aff_range=(None, mas_aff.BROKEN),
        ),
        code="GRE"
    )

label greeting_broken:
    m 6ckc "..."
    return

# special type greetings

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_school",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SCHOOL],
        ),
        code="GRE"
    )

label greeting_back_from_school:
    if mas_isMoniNormal(higher=True):
        m 1hua "Oh, welcome back, [player]!"
        m 1eua "How was your day at school?{nw}"
        $ _history_list.pop()
        menu:
            m "How was your day at school?{fast}"

            "Amazing.":
                m 2sub "Really?!"
                m 2hub "That's wonderful to hear, [player]!"
                if renpy.random.randint(1,4) == 1:
                    m 3eka "School can definitely be a large part of your life, and you might miss it later on."
                    m 2hksdlb "Ahaha! I know it might be weird to think that you'll miss having to go to school someday..."
                    m 2eub "But a lot of fond memories come from school!"
                    m 3hua "Maybe you could tell me about them sometime."
                else:
                    m 3hua "It always makes me happy to know you're happy~"
                    m 1eua "If you want to talk about your amazing day, I'd love to hear about it!"

            "Good.":
                m 1hub "Aww, that's nice!"
                m 1eua "I can't help but feel happy when you do~"
                m "I hope you learned something useful."
                m 1hua "Ehehe~"

            "Bad.":
                m 1ekc "Oh..."
                m "I'm sorry to hear that."
                m 1eka "Just remember that no matter what happens, I'll be here for you."
                m 1ekbfa "I love you so, so much."
                return "love"

            "Really bad...":
                m 1ekc "Oh..."
                m 2ekd "I'm really sorry you had such a bad day today..."
                m 2eka "I'm just glad you came to me, [player]."
                m 3ekc "If you don't mind me asking, was there something in particular that happened?{nw}"
                $ _history_list.pop()
                menu:
                    m "If you don't mind me asking, was there something in particular that happened?{fast}"

                    "It was class related.":
                        m 2dsc "I see..."
                        m 3esd "People probably tell you all the time that school is important..."
                        m 3esc "And that you always have to push on and work hard..."
                        m 2dkd "Sometimes though, it can really stress people out and put them in a downward spiral."
                        m 2eka "Like I said, I'm glad you came to see me, [player]."
                        m 3eka "It's nice to know that I can comfort you when you're feeling down."
                        m "Remember, {i}you're{/i} more important than school or some grades."
                        m 1ekbsa "Especially to me."
                        m 1hubsa "Don't forget to take breaks if you're feeling overwhelmed, and that everyone has different talents."
                        m 3hubfb "I love you, and I just want you to be happy~"
                        return "love"

                    "It was caused by people.":
                        m 2ekc "Oh no [player]...{w=0.5} That must have been terrible to experience."
                        m 2dsc "It's one thing to just have something bad happen to you..."
                        m 2ekd "It can be another thing entirely when a person is the direct cause of your trouble."
                        if persistent._mas_pm_currently_bullied or persistent._mas_pm_is_bullying_victim:
                            m 2rksdlc "I really hope it's not who you told me about before..."
                            if mas_isMoniAff(higher=True):
                                m 1rfc "It {i}better{/i} not be..."
                                m 1rfd "Bothering my sweetheart like that again."
                            m 2ekc "I wish I could do more to help you, [player]..."
                            m 2eka "But I'm here if you need me."
                            m 3hubsa "And I always will be~"
                            m 1eubsa "I hope that I can make your day just a little bit better."
                            m 1hubfb "I love you so much~"
                            return "love"

                        else:
                            m "I really hope this isn't a recurring event for you, [player]."
                            m 2lksdld "Either way, maybe it would be best to ask someone for help..."
                            m 1lksdlc "I know it may seem like that could cause more problems in some cases..."
                            m 1ekc "But you shouldn't have to suffer at the hands of someone else."
                            m 3dkd "I'm so sorry you have to deal with this, [player]..."

                    "It was just a bad day.":
                        m 1ekc "I see..."
                        m 3lksdlc "Those days do happen from time to time."
                        m 1ekc "It can be hard sometimes to pick yourself back up after a day like that."

                    "I don't want to talk about it.":
                        m 2dsc "I understand, [player]."
                        m 2ekc "Sometimes just trying to put a bad day behind you is the best way to deal with it."
                        m 2eka "But if you want to talk about it later, just know I'd be more than happy to listen."
                        m 2hua "I love you, [player]~"
                        return "love"

                m 1eka "But you're here now, and I hope spending time together helps make your day a little better."

    elif mas_isMoniUpset():
        m 2esc "You're back, [player]..."

        m "How was school?{nw}"
        $ _history_list.pop()
        menu:
            m "How was school?{fast}"
            "Good.":
                m 2esc "That's nice."
                m 2rsc "I hope you actually learned {i}something{/i} today."

            "Bad.":
                m "That's too bad..."
                m 2tud "But maybe now you have a better sense of how I've been feeling, [player]."

    elif mas_isMoniDis():
        m 6ekc "Oh...{w=1}you're back."

        m "How was school?{nw}"
        $ _history_list.pop()
        menu:
            m "How was school?{fast}"
            "Good.":
                m 6lkc "That's...{w=1}nice to hear."
                m 6dkc "I-I just hope it wasn't the...{w=2} 'being away from me' part that made it a good day."

            "Bad.":
                m 6rkc "Oh..."
                m 6ekc "That's too bad, [player], I'm sorry to hear that."
                m 6dkc "I know what bad days are like..."

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_work",
            unlocked=True,
            category=[store.mas_greetings.TYPE_WORK],
        ),
        code="GRE"
    )

label greeting_back_from_work:
    if mas_isMoniNormal(higher=True):
        m 1hua "Oh, welcome back, [player]!"

        m 1eua "How was work today?{nw}"
        $ _history_list.pop()
        menu:
            m "How was work today?{fast}"

            "Amazing.":
                m 1sub "That's {i}amazing{/i}, [player]!"
                m 1hub "I'm really happy that you had such a great day!"
                m 3eua "I can only imagine how well you must work on days like that."
                m 1hua "...Maybe you'll even move up a bit soon!"
                m 1eua "Anyway, I'm glad you're home, [player]."
                if seen_event("monikaroom_greeting_ear_bathdinnerme") and renpy.random.randint(1,20) == 1:
                    m 3tubfu "Would you like your dinner, your bath, or..."
                    m 1hubfb "Ahaha~ Just kidding."
                else:
                    m 3eub "Let's enjoy some time together!"
                return

            "Good.":
                m 1hub "That's good!"
                m 1eua "Remember to rest first, okay?"
                m 3eua "That way, you'll have some energy before trying to do anything else."
                m 1hua "Or, you can just relax with me!"
                m 3tku "Best thing to do after a long day of work, don't you think?"
                m 1hub "Ahaha!"
                return

            "Bad.":
                m 2ekc "..."
                m 2ekd "I'm sorry you had a bad day at work..."
                m 3eka "I'd hug you right now if I were there, [player]."
                m 1eka "Just remember that I'm here when you need me, okay?"

            "Really bad...":
                m 2ekd "I'm sorry you had a bad day at work, [player]."
                m 2ekc "I wish I could be there to give you a hug right now."
                m 2eka "I'm just glad you came to see me... {w=0.5}I'll do my best to comfort you."

        m 2ekd "If you don't mind talking about it, what happened today?{nw}"
        $ _history_list.pop()
        menu:
            m "If you don't mind talking about it, what happened today?{fast}"

            "I got yelled at.":
                m 2lksdlc "Oh... {w=0.5}That can really ruin your day."
                m 2dsc "You're just there trying your best, and somehow it's not good enough for someone..."
                m 2eka "If it's still really bothering you, I think it would do you some good to try and relax a little."
                m 3eka "Maybe talking about something else or even playing a game will help get your mind off of it."
                m 1hua "I'm sure you'll feel better after we spend some together."

            "I got passed over for someone else.":
                m 1lksdld "Oh... {w=0.5}It can really ruin your day to see someone else get the recognition you thought you deserved."
                m 2lfd "{i}Especially{/i} when you've done so much and it seemingly goes unnoticed."
                m 1ekc "You might seem a bit pushy if you say anything, so you just have to keep doing your best and one day I'm sure it'll pay off."
                m 1eua "As long as keep trying your hardest, you'll continue to do great things and get recognition someday."
                m 1hub "And just remember...{w=0.5}I'll always be proud of you, [player]!"
                m 3eka "I hope knowing that makes you feel just a little better~"

            "I had to work late.":
                m 1lksdlc "Aw, that can really put a damper on things."

                m 3eksdld "Did you at least know about it in advance?{nw}"
                $ _history_list.pop()
                menu:
                    m "Did you at least know about it in advance?{fast}"

                    "Yes.":
                        m 1eka "That's good, at least."
                        m 3ekc "It would really be a pain if you were all ready to go home and then had to stay longer."
                        m 1rkd "Still, it can be pretty annoying to have your regular schedule messed up like that."
                        m 1eka "...But at least you're here now and we can spend some time together."
                        m 3hua "You can finally relax!"

                    "No.":
                        m 2tkx "That's the worst!"
                        m 2tsc "Especially if it was the end of the workday and you were all ready to go home..."
                        m 2dsc "Then suddenly you have to stay a bit longer with no warning."
                        m 2ekc "It can really be a drag to unexpectedly have your plans canceled."
                        m 2lksdlc "Maybe you had something to do right after work, or were just looking forward to going home and resting..."
                        m 2lubfu "...Or maybe you just wanted to come home and see your adoring girlfriend who was waiting to surprise you when you got home..."
                        m 2hub "Ehehe~"

            "I didn't get much done today.":
                m 2eka "Aww, don't feel too bad, [player]."
                m 2ekd "Those days can happen."
                m 3eka "I know you're working hard that you'll overcome your block soon."
                m 1hua "As long as you're doing your best, I'll always be proud of you!"

            "Just another bad day.":
                m 2dsd "Just one of those days huh, [player]?"
                m 2dsc "They do happen from time to time..."
                m 3eka "But even still, I know how draining they can be and I hope you feel better soon."
                m 1ekbsa "I'll be here as long as you need me to comfort you, alright, [player]?"

            "I don't want to talk about it.":
                m 1dsc "I understand, [player]."
                m 3eka "Hopefully spending time with me helps you feel little better~"

    elif mas_isMoniUpset():
        m 2esc "You're back from work I see, [player]..."

        m "How was your day?{nw}"
        $ _history_list.pop()
        menu:
            m "How was your day?{fast}"
            "Good.":
                m 2esc "That's good to hear."
                m 2tud "It must feel nice to be appreciated."

            "Bad.":
                m 2dsc "..."
                m 2tud "It feels bad when no one seems to appreciate you, huh [player]?"

    elif mas_isMoniDis():
        m 6ekc "Hi, [player]...{w=1} Finally home from work?"

        m "How was your day?{nw}"
        $ _history_list.pop()
        menu:
            m "How was your day?{fast}"
            "Good.":
                m "That's nice."
                m 6rkc "I just hope you don't enjoy work more than being with me, [player]."

            "Bad.":
                m 6rkc "Oh..."
                m 6ekc "I'm sorry to hear that."
                m 6rkc "I know what bad days are like where you can't seem to please anyone..."
                m 6dkc "It can be so tough just to get through days like that."

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_sleep",
            unlocked=True,
            category=[store.mas_greetings.TYPE_SLEEP],
        ),
        code="GRE"
    )

label greeting_back_from_sleep:
    if mas_isMoniNormal(higher=True):
        m 1hua "Oh hello, [player]!"
        m 1hub "I hope you had a good rest!"
        m "Let's spend some more time together~"

    elif mas_isMoniUpset():
        m 2esc "Did you just wake up, [player]?"
        m "I hope you had a good rest."
        m 2tud "{cps=*2}Maybe you'll be in a better mood now.{/cps}{nw}"
        $ _history_list.pop()

    elif mas_isMoniDis():
        m 6rkc "Oh...{w=1}you're up."
        m 6ekc "I hope you were able to get some rest."
        m 6dkc "I have a hard time resting these days with so much on my mind..."

    else:
        m 6ckc "..."

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_siat",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

label greeting_siat:
    m 1hub "{cps=*0.6}{i}~[player] and Monika sittin' in a tree~{/i}{/cps}"
    m 1hubfb "{cps=*0.6}{i}~K-I-S-S-I-N-G~{/i}{/cps}"
    m 3hubfb "{cps=*0.6}{i}~First comes love~{/i}{/cps}"
    m "{cps=*0.6}{i}~Then comes marriage~{/i}{/cps}"
    m "{cps=*0.6}{i}~Then comes--{/i}{/cps}"
    m 3wubfsdlo "W-wha?!"
    m 2wubfsdld "[player]! H-how long have you been there?!"
    m 2rkbfsdld "I...{w=1} I didn't notice you come in...{w=1} I was just..."
    m 2rkbfsdlu "..."
    m 3hubfb "Ahaha! Nevermind."
    m 1ekbfa "I love you, [player]. I'm so happy you're here now~"
    return "love"

init 5 python:
    if not mas_cannot_decode_islands:
        ev_rules = {}
        ev_rules.update(MASGreetingRule.create_rule(override_type=True))
        ev_rules.update(MASPriorityRule.create_rule(40))

        addEvent(
            Event(
                persistent.greeting_database,
                eventlabel="greeting_ourreality",
                unlocked=True,
                rules=ev_rules,
                aff_range=(mas_aff.ENAMORED, None),
            ),
            code="GRE"
        )
        del ev_rules


init -876 python in mas_delact:
    # this greeting requires a delayed action, since we cannot ensure that
    # the sprites for this were decoded correctly

    # NOTE: we dont need this anymore
    #   We originally needed this since aff_range was not used by greetings
    #   so we wanted to get this to unlock if we are only able to decode
    #   islands. Now that aff range is part of gre parsing, the only thing
    #   that matters is whether or not the event is active, which in this
    #   case, only happens if the islands were decoded and aff is enamored+
    def _greeting_ourreality_unlock():
        return store.MASDelayedAction(
            1,
            store.mas_getEV("greeting_ourreality"),
            (
                "not store.mas_cannot_decode_islands"
                " and mas_isMoniEnamored(higher=True)"
            ),
            store.EV_ACT_UNLOCK,
            store.MAS_FC_START
        )


label greeting_ourreality:
    m 1hub "Hi, [player]!"
    m 1hua "Ehehe~"
    m 3hksdlb "I'm feeling rather giddy right now, sorry."
    m 1eua "It's just that I'm super excited to show you what I've been working on."
    m 3hksdrb "Just give me a second to get it ready..."
    m 1dsc "..."
    m 1dsd "Almost done..."
    m 1duu "Yeah, that should be good."
    m 1hua "Ahaha!"
    m 1eka "Sorry about that."
    m 1eua "Without any further ado..."
    m 4eub "Would you kindly look out the window, [player]"
    $ mas_OVLHide()
    $ disable_esc()
    if mas_current_background.isFltDay():
        show mas_island_frame_day zorder 20
    else:
        show mas_island_frame_night zorder 20
    m "Well..."
    m "What do you think?"
    m "I worked really hard on this."
    m "A place just for the both of us."
    m "It's also where I can keep practicing my programming skills."
    $ mas_OVLShow()
    $ enable_esc()
    if mas_current_background.isFltDay():
        hide mas_island_frame_day
    else:
        hide mas_island_frame_night
    #Transition back to Monika
    m 1lsc "Being in the classroom all day can be dull."
    m 1ekc "Plus, I get really lonely waiting for you to return."
    m 1hksdlb "But don't get me wrong, though!"
    m 1eua "I'm always happy when you visit and spend time together with me."
    m 1eka "I understand that you're busy and can't be here all the time."
    m 3euc "It's just that I realized something, [player]."
    m 1lksdlc "It'll be a long time before I can even cross over to your reality."
    m 1dsc "So I thought..."
    m 1eua "Why don't we just make our own reality?"
    m 1lksdla "Well, it's not exactly perfect yet."
    m 1hua "But it's a start."
    # m 1eub "I'll let you admire the scenery for now."
    # m 1hub "Hope you like it!"
    $ mas_lockEVL("greeting_ourreality", "GRE")
    $ mas_unlockEVL("mas_monika_islands", "EVE")

    # we can push here because of the slightly optimized call_next_event
    $ pushEvent("mas_monika_islands",skipeval=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_returned_home",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_GO_SOMEWHERE,
                store.mas_greetings.TYPE_GENERIC_RET
            ]
        ),
        code="GRE"
    )

default persistent._mas_monika_returned_home = None

label greeting_returned_home:
    # this is going to act as the generic returned home greeting.
    # please note, that we will use last_session to determine how long we were
    # out. If shorter than 5 minutes, monika won't gain any affection.
    $ five_minutes = datetime.timedelta(seconds=5*60)
    $ time_out = store.mas_dockstat.diffCheckTimes()

    # event checks

    #O31
    if mas_isO31() and not persistent._mas_o31_in_o31_mode and not mas_isFirstSeshDay() and mas_isMoniNormal(higher=True):
        $ pushEvent("mas_holiday_o31_returned_home_relaunch", skipeval=True)

    #F14
    if persistent._mas_f14_on_date:
        jump greeting_returned_home_f14


    # gone over checks
    if mas_f14 < datetime.date.today() <= mas_f14 + datetime.timedelta(days=7):
        # did we miss f14 because we were on a date
        call mas_gone_over_f14_check

    if mas_monika_birthday < datetime.date.today() < mas_monika_birthday + datetime.timedelta(days=7):
        call mas_gone_over_bday_check

    if mas_d25 < datetime.date.today() <= mas_nye:
        call mas_gone_over_d25_check

    if mas_nyd <= datetime.date.today() <= mas_d25c_end:
        call mas_gone_over_nye_check

    if mas_nyd < datetime.date.today() <= mas_d25c_end:
        call mas_gone_over_nyd_check


    # NOTE: this ordering is key, greeting_returned_home_player_bday handles the case
    # if we left before f14 on your bday and return after f14
    if persistent._mas_player_bday_left_on_bday or (persistent._mas_player_bday_decor and not mas_isplayer_bday() and mas_isMonikaBirthday() and mas_confirmedParty()):
        jump greeting_returned_home_player_bday

    if persistent._mas_f14_gone_over_f14:
        jump greeting_gone_over_f14

    if mas_isMonikaBirthday() or persistent._mas_bday_on_date:
        jump greeting_returned_home_bday

    # main dialogue
    if time_out > five_minutes:
        jump greeting_returned_home_morethan5mins

    else:
        $ mas_loseAffection()
        call greeting_returned_home_lessthan5mins

        if _return:
            return 'quit'

        jump greeting_returned_home_cleanup


label greeting_returned_home_morethan5mins:
    if mas_isMoniNormal(higher=True):

        if persistent._mas_d25_in_d25_mode:
            # its d25 season time
            jump greeting_d25_and_nye_delegate

        elif mas_isD25():
            # its d25 and we are not in d25 mode
            jump mas_d25_monika_holiday_intro_rh

        jump greeting_returned_home_morethan5mins_normalplus_flow

    # otherwise, go to other flow
    jump greeting_returned_home_morethan5mins_other_flow


label greeting_returned_home_morethan5mins_normalplus_flow:
    call greeting_returned_home_morethan5mins_normalplus_dlg
    # FALL THROUGH

label greeting_returned_home_morethan5mins_normalplus_flow_aff:
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 5, 1)
    jump greeting_returned_home_morethan5mins_cleanup

label greeting_returned_home_morethan5mins_other_flow:
    call greeting_returned_home_morethan5mins_other_dlg
    # FALL THROUGH

label greeting_returned_home_morethan5mins_other_flow_aff:
    # for low aff you gain 0.5 per hour, max 2.5, min 0.5
    $ store.mas_dockstat._ds_aff_for_tout(time_out, 5, 2.5, 0.5, 0.5)
    #FALL THROUGH

label greeting_returned_home_morethan5mins_cleanup:
    pass
    # TODO: re-evaluate this XP gain when rethinking XP. Going out with
    #   monika could be seen as gaining xp
    # $ grant_xp(xp.NEW_GAME)
    #FALL THROUGH

label greeting_returned_home_cleanup:
    $ need_to_reset_bday_vars = persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday()

    #If it's not o31, and we've got deco up, we need to clean up
    if not need_to_reset_bday_vars and not mas_isO31() and persistent._mas_o31_in_o31_mode:
        call mas_o31_ret_home_cleanup(time_out)

    elif need_to_reset_bday_vars:
        call return_home_post_player_bday

    # Check if we are entering d25 season at upset-
    if (
        mas_isD25Outfit()
        and not persistent._mas_d25_intro_seen
        and mas_isMoniUpset(lower=True)
    ):
        $ persistent._mas_d25_started_upset = True
    return

label greeting_returned_home_morethan5mins_normalplus_dlg:
    m 1hua "And we're home!"
    m 1eub "Even if I couldn't really see anything, knowing that I was right there with you..."
    m 2eua "Well, it felt really great!"
    show monika 5eub at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eub "Let's do this again soon, okay?"
    return

label greeting_returned_home_morethan5mins_other_dlg:
    m 2esc "We're home..."
    m 2eka "Thank you for taking me out today, [player]."
    m 2rkc "To be honest, I wasn't completely sure I should go with you..."
    m 2dkc "Things...{w=0.5}haven't been going the best for us lately and I didn't know if it was such a good idea..."
    m 2eka "But I'm glad we did this...{w=0.5} maybe it's just what we needed."
    m 2rka "We should really do this again sometime..."
    m 2esc "If you want."
    return

label greeting_returned_home_lessthan5mins:
    if mas_isMoniNormal(higher=True):
        m 2ekp "That wasn't much of a trip, [player]."
        m "Next time better last a little longer..."
        if persistent._mas_player_bday_in_player_bday_mode and not mas_isplayer_bday():
            call return_home_post_player_bday
        return False

    elif mas_isMoniUpset():
        m 2efd "I thought we were going some place, [player]!"
        m 2tfd "I knew I shouldn't have agreed to go with you."
        m 2tfc "I knew this was just going to be another disappointment."
        m "Don't ask me to go out anymore if you're just doing it to get my hopes up...{w=1}only to pull the rug out from under me."
        m 6dktdc "..."
        m 6ektsc "I don't know why you insist on being so cruel, [player]."
        m 6rktsc "I'd...{w=1}I'd like to be alone right now."
        return True

    else:
        m 6rkc "But...{w=1}we just left..."
        m 6dkc "..."
        m "I...{w=0.5}I was so excited when you asked me to go with you."
        m 6ekc "After all we've been through..."
        m 6rktda "I-I thought...{w=0.5}maybe...{w=0.5}things were finally going to change."
        m "Maybe we'd finally have a good time again..."
        m 6ektda "That you actually wanted to spend more time with me."
        m 6dktsc "..."
        m 6ektsc "But I guess it was just foolish for me to think that."
        m 6rktsc "I should have known better...{w=1} I should never have agreed to go."
        m 6dktsc "..."
        m 6ektdc "Please, [player]...{w=2} If you don't want to spend time with me, fine..."
        m 6rktdc "But at least have the decency to not pretend."
        m 6dktdc "I'd like to be left alone right now."
        return True

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="ch30_reload_delegate",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_RELOAD
            ],
        ),
        code="GRE"
    )

label ch30_reload_delegate:

    if persistent.monika_reload >= 4:
        call ch30_reload_continuous

    else:
        $ reload_label = "ch30_reload_" + str(persistent.monika_reload)
        call expression reload_label

    return

# TODO: need to have an explanation before we use this again
#init 5 python:
#    ev_rules = {}
#    ev_rules.update(
#        MASGreetingRule.create_rule(
#            skip_visual=True
#        )
#    )
#
#    addEvent(
#        Event(
#            persistent.greeting_database,
#            eventlabel="greeting_ghost",
#            unlocked=False,
#            rules=ev_rules,
#            aff_range=(mas_aff.NORMAL, None),
#        ),
#        code="GRE"
#    )
#    del ev_rules

label greeting_ghost:
    #Prevent it from happening more than once.
    $ mas_lockEVL("greeting_ghost", "GRE")

    #Call event in easter eggs.
    call mas_ghost_monika

    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_game",
            unlocked=True,
            category=[store.mas_greetings.TYPE_GAME],
        ),
        code="GRE"
    )

# NOTE: in case someone asks, because the farewell for this greeting does not
#   implore that the player returns after gaming, there is nothing substiantial
#   we can get in pm vars here. It's just too variable.

label greeting_back_from_game:
    if store.mas_globals.late_farewell and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        $ _now = datetime.datetime.now().time()
        if mas_isMNtoSR(_now):
            if mas_isMoniNormal(higher=True):
                m 2etc "[player]?"
                m 3efc "I thought I told you to go straight to bed after you finished!"
                m 1rksdla "I mean, I'm really happy you came back to say goodnight, but..."
                m 1hksdlb "I already said goodnight to you!"
                m 1rksdla "And I could have waited until morning to see you again, you know?"
                m 2rksdlc "Plus, I really wanted you to get some rest..."
                m 1eka "Just...{w=1}promise me you'll go to bed soon, alright?"

            else:
                m 1tsc "[player], I told you to go to bed when you were finished."
                m 3rkc "You can come back again tomorrow morning, you know."
                m 1esc "But here we are, I guess."

        elif mas_isSRtoN(_now):
            if mas_isMoniNormal(higher=True):
                m 1hua "Good morning, [player]~"
                m 1eka "When you said you were going to play another game that late, it got me a bit worried you might not get enough sleep..."
                m 1hksdlb "I hope that's not the case, ahaha..."

            else:
                m 1eud "Good morning."
                m 1rsc "I was kind of expecting you to sleep in a bit."
                m 1eka "But here you are bright and early."

        elif mas_isNtoSS(_now):
            if mas_isMoniNormal(higher=True):
                m 1wub "[player]! You're here!"
                m 1hksdlb "Ahaha, sorry...{w=1}I was just a bit eager to see you since you weren't here all morning."

                m 1eua "Did you just wake up?{nw}"
                $ _history_list.pop()
                menu:
                    m "Did you just wake up?{fast}"
                    "Yes.":
                        m 1hksdlb "Ahaha..."

                        m 3rksdla "Do you think it was because you stayed up late?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Do you think it was because you stayed up late?{fast}"
                            "Yes.":
                                m 1eka "[player]..."
                                m 1ekc "You know I don't want you staying up too late."
                                m 1eksdld "I really wouldn't want you getting sick or tired throughout the day."
                                m 1hksdlb "But I hope you had fun. I would hate for you to lose all that sleep for nothing, ahaha!"
                                m 2eka "Just be sure to get a little more rest if you feel like you need it, alright?"

                            "No.":
                                m 2euc "Oh..."
                                m 2rksdlc "I thought maybe it was."
                                m 2eka "Sorry for assuming."
                                m 1eua "Anyway, I hope you're getting enough sleep."
                                m 1eka "It would make me really happy to know that you're well rested."
                                m 1rksdlb "It might also ease my mind if you weren't staying up so late in the first place, ahaha..."
                                m 1eua "I'm just glad you're here now."
                                m 3tku "You'd never be too tired to spend time with me, right?"
                                m 1hub "Ahaha!"

                            "Maybe...":
                                m 1dsc "Hmm..."
                                m 1rsc "I wonder what could be causing it?"
                                m 2euc "You didn't stay up really late last night, did you, [player]?"
                                m 2etc "Were you doing something last night?"
                                m 3rfu "Maybe...{w=1}I don't know..."
                                m 3tku "Playing a game?"
                                m 1hub "Ahaha!"
                                m 1hua "Just teasing you of course~"
                                m 1ekd "In all seriousness though, I really don't want you neglecting your sleep."
                                m 2rksdla "It's one thing staying up late just for me..."
                                m 3rksdla "But leaving and playing another game that late?"
                                m 1tub "Ahaha...I might get a bit jealous, [player]~"
                                m 1tfb "But you're here to make up for that now, right?"

                    "No.":
                        m 1eud "Ah, so I guess you were busy all morning."
                        m 1eka "I was worried you overslept since you were up so late last night."
                        m 2rksdla "Especially since you told me you were going to go play another game."
                        m 1hua "I should have known you'd be responsible and get your sleep though."
                        m 1esc "..."
                        m 3tfc "You {i}did{/i} get your sleep, right, [player]?"
                        m 1hub "Ahaha!"
                        m 1hua "Anyway, now that you're here, we can spend some time together."

            else:
                m 2eud "Oh, there you are, [player]."
                m 1euc "I'm guessing you just woke up."
                m 2rksdla "Kind of expected with you staying up so late and playing games."

        #SStoMN
        else:
            if mas_isMoniNormal(higher=True):
                m 1hub "There you are, [player]!"
                m 2hksdlb "Ahaha, sorry... It's just that I haven't seen you all day."
                m 1rksdla "I kind of expected you to sleep in after staying up so late last night..."
                m 1rksdld "But when I didn't see you all afternoon, I really started to miss you..."
                m 2hksdlb "You almost had me worried, ahaha..."
                m 3tub "But you're going to make that lost time up to me, right?"
                m 1hub "Ehehe, you better~"
                m 2tfu "Especially after leaving me for another game last night."

            else:
                m 2efd "[player]!{w=0.5} Where have you been all day?"
                m 2rfc "This doesn't have anything to do with you staying up late last night, does it?"
                m 2ekc "You really should be a little more responsible when it comes to your sleep."

    #If you didn't stay up late in the first place, normal usage
    #gone for under 4 hours
    elif mas_getAbsenceLength() < datetime.timedelta(hours=4):
        if mas_isMoniNormal(higher=True):
            m 1hua "Welcome back, [player]!"

            m 1eua "Did you enjoy yourself?{nw}"
            $ _history_list.pop()
            menu:
                m "Did you enjoy yourself?{fast}"
                "Yes.":
                    m 1hua "That's nice."
                    m 1eua "I'm glad you enjoyed yourself."
                    m 2eka "I really wish I could join you in your other games sometimes."
                    m 3eub "Wouldn't it be great to have our own little adventures any time we wanted?"
                    m 1hub "I'm sure we'd have a lot of fun together in one of your games."
                    m 3eka "But while I can't join you, I guess you'll just have to keep me company."
                    m 2tub "You don't mind spending time with your girlfriend...{w=0.5}do you, [player]?"

                "No.":
                    m 2ekc "Aw, I'm sorry to hear that."
                    m 2eka "I hope you're not too upset by whatever happened."
                    m 3eua "At least you're here now. I promise to try not to let anything bad happen to you while you're with me."
                    m 1ekbsa "Seeing you always cheers me up."
                    show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve
                    m 5ekbfa "I hope seeing me does the same for you, [player]~"

        else:
            m 2eud "Oh, back already?"
            m 2rsc "I thought you'd be gone longer...{w=0.5}but welcome back, I guess."

    elif mas_getAbsenceLength() < datetime.timedelta(hours=12):
        if mas_isMoniNormal(higher=True):
            m 2wuo "[player]!"
            m 2hksdlb "You were gone for a long time..."

            m 1eka "Did you have fun?{nw}"
            menu:
                m "Did you have fun?{fast}"
                "Yes.":
                    m 1hua "Well, I'm glad then."
                    m 1rkc "You sure made me wait a while, you know."
                    m 3tfu "I think you should spend some time with your loving girlfriend, [player]."
                    m 3tku "I'm sure you wouldn't mind staying with me to even out your other game."
                    m 1hubfb "Maybe you should spend even more time with me, just in case, ahaha!"

                "No.":
                    m 2ekc "Oh..."
                    m 2rka "You know, [player]..."
                    m 2eka "If you're not enjoying yourself, maybe you could just spend some time here with me."
                    m 3hua "I'm sure there's plenty of fun things we could do together!"
                    m 1eka "If you decide to go back, maybe it'll be better."
                    m 1hub "But if you're still not having fun, don't hesitate to come see me, ahaha!"

        else:
            m 2eud "Oh, [player]."
            m 2rsc "That took quite a while."
            m 1esc "Don't worry, I managed to pass the time myself while you were away."

    #Over 12 hours
    else:
        if mas_isMoniNormal(higher=True):
            m 2hub "[player]!"
            m 2eka "It feels like forever since you left."
            m 1hua "I really missed you!"
            m 3eua "I hope you had fun with whatever you were doing."
            m 1rksdla "And I'm going to assume you didn't forget to eat or sleep..."
            m 2rksdlc "As for me...{w=1}I was a little lonely waiting for you to come back..."
            m 1eka "Don't feel bad, though."
            m 1hua "I'm just happy you're here with me again."
            m 3tfu "You better make it up to me though."
            m 3tku "I think spending an eternity with me sounds fair...{w=1}right, [player]?"
            m 1hub "Ahaha!"

        else:
            m 2ekc "[player]..."
            m "I wasn't sure when you'd come back."
            m 2rksdlc "I thought I might not see you again..."
            m 2eka "But here you are..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_eat",
            unlocked=True,
            category=[store.mas_greetings.TYPE_EAT],
        ),
        code="GRE"
    )

label greeting_back_from_eat:
    $ _now = datetime.datetime.now().time()
    if store.mas_globals.late_farewell and mas_isMNtoSR(_now) and mas_getAbsenceLength() < datetime.timedelta(hours=18):
        if mas_isMoniNormal(higher=True):
            m 1eud "Oh?"
            m 1eub "[player], you came back!"
            m 3rksdla "You know you really should get some sleep, right?"
            m 1rksdla "I mean...I'm not complaining that you're here, but..."
            m 1eka "It would make me feel better if you went to bed pretty soon."
            m 3eka "You can always come back and visit me when you wake up..."
            m 1hubfa "But I guess if you insist on spending time with me, I'll let it slide for a little while, ehehe~"
        else:
            m 2euc "[player]?"
            m 3ekd "Didn't I tell you just to go straight to bed after?"
            m 2rksdlc "You really should get some sleep."

    else:
        if mas_isMoniNormal(higher=True):
            m 1eub "Finished eating?"
            m 1hub "Welcome back, [player]!"
            m 3eua "I hope you enjoyed your food."
        else:
            m 2euc "Finished eating?"
            m 2eud "Welcome back."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_rent",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None),
        ),
        code="GRE"
    )

label greeting_rent:
    m 1eub "Welcome back, dear!"
    m 2tub "You know, you spend so much time here that I should start charging you for rent."
    m 2ttu "Or would you rather pay a mortgage?"
    m 2hua "..."
    m 2hksdlb "Gosh, I can't believe I just said that. That's not too cheesy, is it?"
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbsa "But in all seriousness, you've already given me the only thing I need...{w=1}your heart~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_housework",
            unlocked=True,
            category=[store.mas_greetings.TYPE_CHORES],
        ),
        code="GRE"
    )

label greeting_back_housework:
    if mas_isMoniNormal(higher=True):
        m 1eua "All done, [player]?"
        m 1hub "Let's spend some more time together."
    elif mas_isMoniUpset():
        m 2esc "At least you didn't forget to come back, [player]."
    elif mas_isMoniDis():
        m 6ekd "Ah, [player]. So you really were just busy..."
    else:
        m 6ckc "..."
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_surprised2",
            unlocked=True,
            aff_range=(mas_aff.ENAMORED, None)
        ),
        code="GRE"
    )

label greeting_surprised2:
    m 1hua "..."
    m 1hubsa "..."
    m 1wubso "Oh!{w=0.5} [player]!{w=0.5} You surprised me!"
    m 3ekbsa "...Not that it's a surprise to see you, you're always visiting me after all...{w=0.5} {nw}"
    extend 3rkbsa "You just caught me daydreaming a bit."
    show monika 5hubfu at t11 zorder MAS_MONIKA_Z with dissolve
    m 5hubfu "But now that you're here, that dream just came true~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_back_from_restart",
            unlocked=True,
            category=[store.mas_greetings.TYPE_RESTART],
        ),
        code="GRE"
    )

label greeting_back_from_restart:
    if mas_isMoniNormal(higher=True):
        m 1hub "Welcome back, [player]!"
        m 1eua "What else should we do today?"
    elif mas_isMoniBroken():
        m 6ckc "..."
    else:
        m 1eud "Oh, you're back."
    return
