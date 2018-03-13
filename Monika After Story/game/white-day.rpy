### Special event for white day.
### Only available to those who gave roses.obj to Monika


default mas_w_day_file_decoded = False

init 4 python:
    #This defines White Day
    white_day = datetime.datetime(year=2018, month=3, day=12)
    mas_w_day_file_decoded = False

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_white_day_start',
                                             action=EV_ACT_PUSH,
                                             conditional="seen_event('monika_valentines_start')",
                                             start_date=white_day,
                                             end_date=white_day + datetime.timedelta(days=5)
                                             ))


label monika_white_day_start:
    m "[player]!"
    m "I have a little surprise for you~"
    m "It's something that I really worked hard on!"
    m "But..."
    m "You have to solve a little game first before you can see it."
    m "I made sure to wrap it up nicely so you won't get it until you figure out what it is."
    m "So don't try to cheat, okay?"
    m "Alright, the encoded name is..."
    m "NjM2ODZmNjM2ZjZjNjE3NDY1NzM="
    m "Got it, [player]?"
    m "I'll give you two clues to solve it."
    m "64, then 467578."
    m "If you forget, just ask me and I'll repeat them for you, okay?"
    m "I'll give you five days to solve it!"
    m "Good luck, [player]~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_giftname',prompt="Clues for the gift",
                                                            action=EV_ACT_UNLOCK,
                                                            conditional="seen_event('monika_white_day_start')",
                                                            start_date=white_day,
                                                            end_date=white_day + datetime.timedelta(days=5)
                                                            ))

label monika_giftname:
    m "Alright, [player]."
    m "The name to solve is..."
    m "NjM2ODZmNjM2ZjZjNjE3NDY1NzM="
    m "And the clues are..."
    m "64, then 467578."
    m "Good luck, [player]!"
    return




init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_decoding',
                                             action=EV_ACT_UNLOCK,
                                             prompt="I know the name of your gift",
                                             conditional="seen_event('monika_white_day_start')",
                                             start_date=white_day,
                                             end_date=white_day + datetime.timedelta(days=5),
                                             ))

label monika_decoding:
    m 1k "That's good!"
    $ done = False
    while not done:
        $ file_name = renpy.input("What's the decoded name?",allow=letters_only,length=10)
        if file_name.lower() != "chocolates":
            m 1h "..."
            m 1n "Wrong!"
            m "That's not the right name, [player]!"
            m 1b "Try again?"
            menu:
                "Yes":
                    m "Ok!"
                "No":
                    m "Oh, alright then."
                    m "Just let me know when you've solved it, okay?"
                    m "I know you can do it!"
                    $ done = True
                    return
        else:
            $ done = True
            python:
                with open(config.basedir + "/game/mod_assets/NjM2ODZmNjM2ZjZjNjE3NDY1NzM=", "r") as reader:
                    base_string = reader.read()
                    decoded = base_string.decode("base64")
                    with open(config.basedir + "/characters/chocolates.png", "wb") as writer:
                        writer.write(decoded)
                        mas_w_day_file_decoded = True
    m 1k "Yes! That's it!"
    m 1k "Go check it out, [player]. It should be in the character folder where you can find my file."
    m "Let me know when you see it!"
    $ evhand.event_database["monika_decoded"].unlocked = True
    $ evhand.event_database["monika_decoded"].unlock_date = datetime.datetime.now()
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_decoded',
                                             action=EV_ACT_UNLOCK,
                                             prompt="I saw your gift",
                                             conditional="mas_w_day_file_decoded",
                                             start_date=white_day,
                                             end_date=white_day + datetime.timedelta(days=5)
                                             ))

label monika_decoded:
    if not mas_w_day_file_decoded:
        m "No, you haven't, [player]!"
        m "You've yet to solve the puzzle after all."
    return
