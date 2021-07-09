## dev mode eggs

#dev mode easter eggs
init 5 python:
    addEvent(
        Event(
            persistent._mas_mood_database,
            "mas_mood_mitochondria",
            prompt="A mitochondria",
            category=[store.mas_moods.TYPE_GOOD],
            unlocked=True
        ),
        eventdb=store.mas_moods.mood_db
    )

    addEvent(
        Event(
            persistent._mas_mood_database,
            "mas_mood_theroom",
            prompt="The Room",
            category=[store.mas_moods.TYPE_NEUTRAL],
            unlocked=True
        ),
        eventdb=store.mas_moods.mood_db
    )

    addEvent(
        Event(
            persistent._mas_mood_database,
            "mas_mood_horny",
            prompt="horny",
            category=[store.mas_moods.TYPE_BAD],
            unlocked=True
        ),
        eventdb=store.mas_moods.mood_db
    )

label mas_mood_mitochondria:
    m "You're the powerhouse of {i}my{/i} cell..."
    return

label mas_mood_theroom:
    m "It's bullshit.{w} I did not hit her."
    m "I did nahhhhht"
    m "Oh hai, [player]."
    return

label mas_mood_horny:
    if persistent.playername.lower() == "monik":
        m "Ahh, only for my one and only~"
    elif persistent.playername.lower() == "rune":
        m "I wouldn't mind, Dragon Writer~"
    elif persistent.playername.lower() == "thepotatoguy":
        m "Sorry, I have no interest in potatoes."
    elif persistent.playername.lower() == "ronin":
        m "Aren't you married? Go talk to your wife."
    elif persistent.playername.lower() == "pi":
        m "Don't you have a girlfriend? Stop being a weeb or she's gonna kill you."
    elif persistent.playername.lower() == "lucian.chr":
        m "No Dark Lords, thank you."
    elif persistent.playername.lower() == "subzero":
        m "Damn horny kid..."
    elif persistent.playername.lower() == "ryuse":
        m "Nope, bye."
        return 'quit'
    else:
        m 3rksdla "Sorry [player], but we aren't that far into our relationship yet. Maybe in a year or two~"
    return

## end dev easter eggs ========================================================
