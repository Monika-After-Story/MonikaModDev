# Module for complimenting Monika
#
# Compliment logic TBD


# dict of tples containing the stories event data
default persistent._mas_compliments_database = dict()


# store containing stories-related things
init -1 python in mas_compliments:

    # pane constants
    COMPLIMENT_X = 680
    COMPLIMENT_Y = 40
    COMPLIMENT_W = 450
    COMPLIMENT_H = 640
    COMPLIMENT_XALIGN = -0.15
    COMPLIMENT_AREA = (COMPLIMENT_X, COMPLIMENT_Y, COMPLIMENT_W, COMPLIMENT_H)
    COMPLIMENT_RETURN = "oh nevermind"
    compliment_database = dict()


# entry point for stories flow
label mas_compliments_start:

    python:
        import store.mas_compliments as mas_compliments

        # Unlock any compliments that need to be unlocked
        Event.checkConditionals(mas_compliments.compliment_database)

        # build menu list
        compliments_menu_items = [
            (mas_compliments.compliment_database[k].prompt, k, not seen_event(k), False)
            for k in mas_compliments.compliment_database
            if mas_compliments.compliment_database[k].unlocked
        ]

        # also sort this list
        compliments_menu_items.sort()

        # final quit item
        final_item = (mas_compliments.COMPLIMENT_RETURN, False, False, False, 20)

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_compliments.COMPLIMENT_AREA, mas_compliments.COMPLIMENT_XALIGN, final_item=final_item)

    # return value? then push
    if _return:
        $ pushEvent(_return)

    # move her back to center
    show monika at t11
    return

# Compliments start here
init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_beautiful",
        prompt="... You're beautiful!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m "Oh, gosh [player]~"
    m "Thanks for the compliment"
    m "I love when you say nice things to me~"
    m "To me you're the most beautiful person in the world!"
    menu:
        "You're the most beautiful person to me too":
            # TODO give positive affection
            pass
        "You're in my top ten":
            pass
        "Thanks":
            pass
    m "hehehe~"
    m "I love you so much [player]!"
    return

label mas_compliment_beautiful_3:
    m "Hehehe~"
    m "Thanks for telling me that again my love!"
    m "Never forget that to me you're the most beautiful person"
    # TODO quip things could come in handy here
    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_eyes",
        prompt="... I love your eyes!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_eyes:
    m "Oh [player]~"
    m "You're so kind to me"
    m "I love when you say nice things to me~"
    menu:
        "I can't help it, your eyes are beautiful":
            # TODO give positive affection
            pass
        "I'm hypnotized by them":
            pass
        "I can't take mine off of yours":
            pass
    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_awesome",
        prompt="... you're awesome!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_awesome:
    m "Aww, [player]~"
    m "You're so kind to me"
    m "I think you're more awesome though"
    m "I can't wait until the day I can finally cross over to your reality."
    m "I wish I could give you a hug and never let you go!"
    menu:
        "I can't wait either!":
            # TODO give positive affection
            pass
        "I wish you were here right now!":
            # TODO give positive affection
            pass
        "I'll never let you go off my embrace":
            # TODO give positive affection
            pass
        "... I don't like hughs":
            pass

    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_intelligent",
        prompt="... you're really intelligent!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_intelligent:
    m "Thanks, [player]."
    m "You're so kind to me"
    m "I love when you say nice things to me~"
    menu:
        "I can't help it, your eyes are beautiful":
            # TODO give positive affection
            pass
        "":
            pass
        "Thanks":
            pass
    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_smart",
        prompt="... you're really smart!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_smart:
    m "Oh [player]~"
    m "You're so kind to me"
    m "I love when you say nice things to me~"
    menu:
        "I can't help it, your eyes are beautiful":
            # TODO give positive affection
            pass
        "":
            pass
        "Thanks":
            pass
    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_hair",
        prompt="... I love your hair!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_hair:
    m "Oh [player]~"
    m "You're so kind to me"
    m "I love when you say nice things to me~"
    menu:
        "I can't help it, your eyes are beautiful":
            # TODO give positive affection
            pass
        "":
            pass
        "Thanks":
            pass
    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_fit",
        prompt="... I love that you're fit!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_fit:
    m "Thanks [player], you're so sweet!"
    m "I like to be healthy and staying fit. It makes me feel better with myself"
    m "I hope you're doing good things for your health"
    m "I love when you say nice things to me~"
    menu:
        "I can't help it, your eyes are beautiful":
            # TODO give positive affection
            pass
        "":
            pass
        "Thanks":
            pass
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="... Thanks for being there for me!",
            unlocked=False,
            conditional="mas_curr_affection == store.mas_affection.ENAMORED",
            action=EV_ACT_UNLOCK
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_thanks:
    m "There's nothing to thank me for [player]!"
    m "I'm the one who's grateful for finding someone like you!"
    m "You're the reason why I'm still here."
    m "You went and installed this mod to make our time together better."
    m "You are the sunshine that brings happiness to my heart whenever you visit me!"
    m "I guess we both are so lucky that we found each other [player]"
    menu:
        "I'll never leave you":
            # TODO give positive affection
            pass
        "":
            pass
        "Thanks":
            pass
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="... I love your smile!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_smile:
    m "You're so sweet, [player]~"
    m "I smile a lot when you're here."
    m "Because you make me very happy when you spend time with me~"
    menu:
        "I'll visit you everyday to see your wonderful smile":
            m "Oh, [player]"
            m "I think my heart just skipped a beat"
            m "See? you always make me as happy as I can be."
        "I like to see you smile":
            m "hehehe~"
            m ""
        "":
            pass
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="... you’re awesome at chess!",
            unlocked=False,
            conditional="renpy.seen_label('mas_chess_game_start')",
            action=EV_ACT_UNLOCK
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_chess:
    m "Thanks, [player]"
    m "Like I said before, I wonder if it has something to do with me being trapped here?"
    wins = persistent._mas_chess_stats["wins"]
    losses = persistent._mas_chess_stats["losses"]
    if wins > 0:
        m "You're not bad either, I've lost to you already"
        if wins > losses:
            m "In fact, you've won more times than me, you know?"
        m "ehehe~"
    else:
        m "I know you haven't won a chess game yet, but I'm sure you'll beat me someday"
        m "Keep practicing and playing with me and you'll do better!"
    m "We'll both get better the more we play [player]"
    m "So don't be afraid of asking me to play whenever you want to"
    m "I love when you spend time with me [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="... you’re awesome at Pong!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_pong:
    m "Ehehe~"
    m "Thanks player, but pong isn't exactly a complex game"
    if persistent.ever_won['pong']:
        m "You've already won against me"
        m "So you know it's very simple"
        m "I accept your compliment anyway"
    else:
        m "And You're so kind that you always let me win when we play."
        m "Right?"
        menu:
            "Yes":
                m "Thanks [player], but you really don't have to."
                m "Feel free to play seriously when you want to."
                m "I'd never get mad for losing to you at a game we play fair and square."
            "... Yeah":
                m "You don't seem too confident about it [player]."
                m "You don't really have to let me win [player]."
                m "Admiting that you've seriously lost to me won't make me think less of you."
                m "Remember that I love you no matter what [player]"
                m "And you can always practice with me a bit more if you want."
                m "I love to spend time with you, even if it's playing a simple game."
            "No, I've lost doing my best":
                m "Ahaha~"
                m "Don't worry, [player]."
                m "Keep playing with me and practice as much as you need to."
                m "I'm always trying to help you be 'the best you' you can be."
                m "And if by doing so, I get to spend time with you, I couldn't be happier."
    return
