##This file contains all of the variations of goodbye that monika can give.
## This also contains a store with a utility function to select an appropriate
## farewell

init -1 python in mas_farewells:

    # custom farewell functions
    def selectFarewell():
        """
        Selects a farewell to be used. This evaluates rules and stuff
        appropriately.

        RETURNS:
            a single farewell (as an Event) that we want to use
        """

        # filter events by their unlocked property first
        unlocked_farewells = renpy.store.Event.filterEvents(
            renpy.store.evhand.farewell_database,
            unlocked=True,
            pool=False
        )

        # filter farewells using the special rules dict
        random_farewells_dict = renpy.store.Event.checkRepeatRules(
            unlocked_farewells
        )

        # check if we have a farewell that actually should be shown now
        if len(random_farewells_dict) > 0:

            # select one label randomly
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]

        # since we don't have special farewells for this time we now check for special random chance
        # pick a farewell filtering by special random chance rule
        random_farewells_dict = renpy.store.Event.checkFarewellRules(
            unlocked_farewells
        )

        # check if we have a farewell that actually should be shown now
        if len(random_farewells_dict) > 0:

            # select on label randomly
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]

        # We couldn't find a suitable farewell we have to default to normal random selection
        # filter random events normally
        random_farewells_dict = renpy.store.Event.filterEvents(
            unlocked_farewells,
            random=True
        )

        # select one randomly
        return random_farewells_dict[
            renpy.random.choice(random_farewells_dict.keys())
        ]

# farewells selection label
label mas_farewell_start:
    $ import store.evhand as evhand
    # we use unseen menu values

    python:
        # preprocessing menu
        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True
        )

    if len(bye_pool_events) > 0:
        # we have selectable options
        python:
            # build a prompt list
            bye_prompt_list = [
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ]

            # add the random selection
            bye_prompt_list.append(("Goodbye", -1, False, False))

            # setup the last option
            bye_prompt_back = ("Nevermind", False, False, False, 20)

        # call the menu
        call screen mas_gen_scrollable_menu(bye_prompt_list, evhand.UNSE_AREA, evhand.UNSE_XALIGN, bye_prompt_back)

        if not _return:
            # user its nevermind
            return

        if _return != -1:
            # push teh selected event
            $ pushEvent(_return.eventlabel)
            return

    # otherwise, select a random farewell
    $ farewell = store.mas_farewells.selectFarewell()
    $ pushEvent(farewell.eventlabel)

    return

###### BEGIN FAREWELLS ########################################################
## FARE WELL RULES:
# unlocked - True means this farewell is ready for selection
# random - randoms are used in teh default farewell action
# pool - pooled ones are selectable in the menu
# rules - TODO documentation
###

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_leaving_already",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_leaving_already:
    m 1c "Aww, leaving already?"
    m 1e "It's really sad whenever you have to go..."
    m 3a "Just be sure to come back as soon as you can, okay?"
    m "I love you so much, [player]. Stay safe!"
    #Don't show this farewell again
    $evhand.farewell_database["bye_leaving_already"].random=False
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_goodbye",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_goodbye:
    m 1c "Goodbye, [player]!"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_sayanora",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_sayanora:
    m 1j "Sayonara, [player]~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_farewellfornow",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_farewellfornow:
    m 1e "Farewell for now, my love~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_untilwemeetagain",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_untilwemeetagain:
    m 2e "'{i}Goodbyes are not forever, Goodbyes are not the end. They simply mean I’ll miss you, Until we meet again.{/i}'"
    m "Ehehe, 'till then, [player]!"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_take_care",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_take_care:
    m 1a "Don't forget that I always love you, [player]~"
    m 1k "Take care!"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(21,24)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_going_to_sleep:
    m "Are you going to sleep, [player]?"
    m 1e "I'll be seeing you in your dreams."
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="I'm going to class.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_to_class:
    m 1j "Study hard, [player]!"
    m 1 "Nothing is more attractive than a [guy] with good grades."
    m 1j "See you later!"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="I'm going to work.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_to_work:
    m 1j "Work hard, [player]!"
    m 1 "I'll be here for you when you get home from work."
    m 1j "Bye-bye!"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="I'm going to sleep.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_sleep:

    python:
        import datetime
        curr_hour = datetime.datetime.now().hour

    # these conditions are in order of most likely to happen with our target
    # audience

    if 20 <= curr_hour < 24:
        # decent time to sleep
        m "Alright, [player]."
        m 1j "Sweet dreams!"

    elif 0 <= curr_hour < 3:
        # somewhat late to sleep
        m "Alright, [player]."
        m 3e "But you should sleep a little earlier next time."
        m 1j "Anyway, good night!"

    elif 3 <= curr_hour < 5:
        # pretty late to sleep
        m 1m "[player]..."
        m "Make sure you get enough rest, okay?"
        m "I don't want you to get sick."
        m 1j "Good night!"
        m 1n "Or morning, rather. Ahaha~"
        m 1j "Sweet dreams!"

    elif 5 <= curr_hour < 12:
        # you probably stayed up the whole night
        show monika 2q
        pause 0.7
        m 2g "[player]!"
        m "You stayed up the entire night!"
        m 2i "I bet you can barely keep your eyes open."
        $ _cantsee_a = glitchtext(15)
        $ _cantsee_b = glitchtext(12)
        menu:
            "[_cantsee_a]":
                pass
            "[_cantsee_b]":
                pass
        m 2q "I thought so.{w} Go get some rest, [player]."
        m 2f "I wouldn't want you to get sick."
        m 1e "Sleep earlier next time, okay?"
        m 1j "Sweet dreams!"

    elif 12 <= curr_hour < 18:
        # afternoon nap
        m 1m "Taking an afternoon nap, I see."
        # TODO: monika says she'll join you, use sleep sprite here
        # and setup code for napping
        m 1j "Ahaha~ Have a good nap, [player]."

    elif 18 <= curr_hour < 20:
        # little early to sleep
        m 1f "Already going to bed?"
        m "It's a little early, though..."
        show monika 1m
        menu:
            m "Care to spend a little more time with me?"
            "Of course!":
                m 1j "Yay!"
                m 1a "Thanks, [player]."
                return
            "Sorry, I'm really tired.":
                m 1e "Aww, that's okay."
                m 1 "Good night, [player]."

# TODO: probably a shocked sprite and additonal dialgoue, also potentially
# tie this with affection later
#            "No.":
#                m 2r "..."
#                m "Fine."
    else:
        # otheerwise
        m "Alright, [player]."
        m 1j "Sweet dreams!"

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_illseeyou",random=True),eventdb=evhand.farewell_database)

label bye_illseeyou:
    m 1b "I'll see you tomorrow, [player]."
    m 1k "Don't forget about me, okay?"
    return 'quit'

init 5 python: ## Implementing Date/Time for added responses based on the time of day
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_haveagoodday:
    m 1b "Have a good day today, [player]."
    m 1b "I hope you accomplish everything you had planned for today."
    m 1b "I'll be here waiting for you when you get back."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_enjoyyourafternoon:
    m 1f "I hate to see you go so early, [player]."
    m 1e "I do understand that you're busy though."
    m 1a "Promise me you'll enjoy your afternoon, okay?"
    m 1j "Goodbye~"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_goodevening:
    m 1k "I had fun today."
    m 1a "Thank you for spending so much time with me, [player]."
    m 1j "Until then, have a good evening."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(20,24)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_goodnight:
    m 1a "Goodnight, [player]."
    m 1e "I'll see you tomorrow, okay?"
    m 1j "Remember, 'Sleep tight, and don't let the bedbugs bite', ehehe."
    m 1k "I love you~"
    return 'quit'
