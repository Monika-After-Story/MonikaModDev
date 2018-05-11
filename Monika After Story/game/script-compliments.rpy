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
    m "hehehe~"
    m "I love you so much [player]!"
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
        "":
            pass
        "Thanks":
            pass
    return

init 5 python:
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_awesome",
        prompt="... you're awesome!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_awesome:
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
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_intelligent",
        prompt="... you're really intelligent!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_intelligent:
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
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_thanks",
        prompt="... Thanks for being here for me!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_thanks:
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
    addEvent(Event(persistent._mas_compliments_database,eventlabel="mas_compliment_smile",
        prompt="... I love your smile!",unlocked=True),eventdb=store.mas_compliments.compliment_database)

label mas_compliment_smile:
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
