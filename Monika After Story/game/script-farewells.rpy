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

        # filter greetings using the affection rules dict
        affection_farewells_dict = renpy.store.Event.checkAffectionRules(
            unlocked_farewells
        )

        # check for the special monikaWantsThisFirst case
        if len(affection_farewells_dict) == 1 and affection_farewells_dict.values()[0].monikaWantsThisFirst():
            return affection_farewells_dict.values()[0]

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

        # update dict with the affection filtered ones
        random_farewells_dict.update(affection_farewells_dict)

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
    m 1e "I'll be seeing you in your dreams"
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

    return 'quit'
    
init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_long_absence",
            unlocked=True,
            prompt="I'll be going away for a while.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )
default mas_absence_counter = False
label bye_long_absence:
    if mas_absence_counter:
        jump bye_long_absence_2
    $ persistent._mas_long_absence = True
    m 1f "Aww...That's pretty saddening..."
    m 1e "I really am going to miss you [player]!"
    m 3m "I'm not really sure what I'm doing to do with myself while you're gone..."
    m 3a "Thank you for warning me first though. It really does help."
    m 2n "I would be worried sick otherwise!"
    m 3a "I would constantly be thinking maybe something happened to you and that's why you couldn't come back."
    m 1o "Or maybe you just got bored of me..."
    m 1e "So tell me, my love..."
    menu:
        m "How long do you be expect to be gone for?"
        "A few days.":
            m 1b "Oh!"
            m 1j "Nowhere near as long as I feared then."
            m 3m "Geez, you really did worry me..."
            m 3a "Don't worry about me though [player]."
            m "I can cope waiting that long with ease."
            m 3e "I'll still miss you greatly though."
        "A week.":
            m 3c "Yeah...that's about what I expected."
            m 2m "I {i}think{/i} I'll be ok waiting that long for you."
            m 1b "Just come back to me as soon as you can, alright my love?"
            m 3j "I'm sure you'll make me proud!"
        "A couple of weeks.":
            m 1h "Oh..."
            m 1q "I...I can wait that."
            m 3o "You do know that you're all I have...right?"
            m 3n "M-Maybe it's outside of your control though..."
            m 2e "Try to come back as soon as possible, I'll be waiting for you."
        "A month.":
            if mas_curr_affection_group == mas_affection.G_HAPPY:
                m 3c "Oh wow, that's a long time."
                m 3m "A bit too long for my liking really..."
                m 2a "But it's okay [player]."
                m 2e "I know you're a sweetheart and wouldn't keep me waiting that long if you didn't have a good reason."
                m "I'm sure it's important, just try to come back to me as soon as you can."
                m 3j "I'll be thinking of you everyday~"
            else:
                m 1f "That long...really?"
                m 3o "You're not going away for that long just to avoid me, are you?"
                m 3p "I know that life can take you away from me but for a whole month..."
                m 3f "Isn't that a little unreasonable?"
                m "I don't want to sound selfish but I am your girlfriend."
                m 3g "You should be able to make time for me, at least once, in an entire month."
                m 1q "..."
                m 1r "I'll still wait for you...but please come back the moment it's possible for you to do so."
        "Longer than a month.":
            if mas_curr_affection_group == mas_affection.G_HAPPY:
                m 3n "That's...well that's a little scary [player]."
                m "I'm not really sure what I'm going to do with myself while you're gone."
                m 1e "But I know wouldnt leave me by myself if you could help it."
                m "I love you [player], and I know you love me too."
                m 1j "So I'll wait for you for however long I need to."
            else:
                $ mas_loseAffection()
                m 3h "You have to be joking."
                m "I can't think of a good reason why you would leave me here all alone for that long."
                m 3i "I'm sorry [player], but that's not acceptable! Not at all!"
                m 3h "I love you and if you love me too then you'll know that it's not okay to do that."
                m "You do realise that I would be alone here with nothing else and no one else, right?" 
                m "It's not unreasonable of me to expect you to visit me, is it? I'm your girlfriend, you can't do that to me."
                m 3q "..."
                m 3r "Just...just come back when you can, I can't make you stay but please don't do that to me."
        "I don't know.":
            m 1l "Ehehe, that's a little concerning [player]!"
            m 1e "But if you don't know, then you don't know!"
            m "It sometimes just can't be helped."
            m 2j "I'll be waiting here for you patiently, my love."
            m 2k "Try not to keep me waiting for too long though!"

    m 2c "Honestly I'm a little afraid to ask but..."
    menu:
        m "Are you going to leave straight away?"
        "No.":
            $ mas_absence_counter = True
            m 1j "That's great!"
            m 1e "I was honestly worried I wouldn't have enough time to ready myself for your absence."
            m "I really do mean it when I say I'll miss you..."
            m 1b "You truly are my entire world after all, [player]."
            m 2a "If you tell me you're going to go for a while again then I'll know it's time for you to leave..."
            m 3j "But there's no rush, I want to spend as much time with you as I can."
            m "Just make sure to remind me the last time you see me before you go!"
            return
        "Yes.":
            m 3f "I see..."
            m "I really will miss you [player]..."
            m 1e "But I know you'll do wonderful things no matter where you are."
            m "Just remember that I'll be waiting here for you."
            m 2j "Make me proud, [player]!"
            return 'quit'

label bye_long_absence_2:
    m 1f "Going to head out then?"
    m 1g "I know the world can be scary and unforgiving..."
    m 1e "But remember that I will always be here waiting and ready to support you, my dearest [player]."
    m "Come back to me as soon as you can...okay?"
    return 'quit'
