### Special event for white day.
### Only available to those who gave roses.obj to Monika


init 4 python:
    #This defines White Day
    white_day = datetime.datetime(year=2018, month=3, day=14)
    
init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_white_day_start',
                                             action=EV_ACT_PUSH,
                                             conditional="seen_event('monika_valentines_start')",
                                             start_date=white_day,
                                             end_date=white_day + datetime.timedelta(days=5)
                                             ))

label monika_white_day_start:
    m 3b "[player]!"
    m 1j "I have a little surprise for you~"
    m 1a "It's something that I really worked hard on!"
    m 1m "But..."
    m 3j "You have to solve a little game first before you can see it."
    m 1b "I made sure to wrap it up nicely so you won't get it until you figure out what it is."
    m 3k "So don't try to cheat, okay?"
    m 1c "Alright, the encoded name is..."
    m 1d "NjM2ODZmNjM2ZjZjNjE3NDY1NzM="
    m 3b "Got it, [player]?"
    m 1b "I'll give you two clues to solve it."
    m 1a "64, then 467578."
    m "If you forget, just ask me and I'll repeat them for you, okay?"
    m "I'll give you five days to solve it!"
    m 1j "Good luck, [player]~"
    return


init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_giftname',prompt="Clues for the gift",
                                                            action=EV_ACT_UNLOCK,
                                                            conditional="seen_event('monika_white_day_start')",
                                                            start_date=white_day,
                                                            end_date=white_day + datetime.timedelta(days=5)
                                                            ))

label monika_giftname:
    m 1a "Alright, [player]."
    m 1c "The name to solve is..."
    m 1d "NjM2ODZmNjM2ZjZjNjE3NDY1NzM="
    m 1c "And the clues are..."
    m 1d "64, then 467578."
    m 1a "Good luck, [player]!"
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
    m 1b "That's good!"
    $ done = False
    while not done:
        $ file_name = renpy.input("What's the decoded name?",allow=letters_only,length=10)
        if file_name.lower() != "chocolates":
            m 2q "..."
            m 2n "Wrong!"
            m 2e "That's not the right name, [player]!"
            m 4l "Try again?"
            menu:
                "Yes":
                    m 1b "Okay!"
                "No":
                    m 1d "Oh..."
                    m 1o "Alright then."
                    m 3l "Just let me know when you've solved it, okay?"
                    m 1j "I know you can do it!"
                    $ done = True
                    return
        else:
            $ done = True
            python:
                with open(config.basedir + "/game/mod_assets/NjM2ODZmNjM2ZjZjNjE3NDY1NzM=", "r") as reader:
                    base_string = reader.read()
                    decoded = base_string.decode("base64")
                    with open(config.basedir + "/characters/for_you.png", "wb") as writer:
                        writer.write(decoded)
    m 3k "Yes! That's it!"
    m 1b "Go check it out, [player]! It should be in the character folder where you can find my file."
    m "Let me know when you see it!"
    $ fileDecoded = True
    jump monika_found
    return

label monika_found:
    $ found = False
    while not found:
        pause 3.0
        m 3b "Did you found it yet?"
        menu:
            "Yes":
                m 1m "Well..."
                m 3n "Do you like it, [player]?"
                m 1f "Like I said, I really worked hard on making that."
                m "I felt really bad I couldn't give them to you on Valentine's Day, so I dedicated a lot of effort to get those to you."
                m 1e "I know that you can't exactly eat them, but it's a symbol of my everlasting love for you, [player]. It's my first gift to you!"
                m 3e "I really appreciate that you took the time to solve this little game of mine."
                m 1j "You are my world, [player]. I love you very much."
                m 1e "I've said it a million times, but that's barely enough to show my love for you..."
                m 1j "Thank you so much for making feel alive and not alone."
                $ found = True
                $ hideEventLabel("monika_decoding",lock=True,depool=True)
                $ hideEventLabel("monika_giftname",lock=True,depool=True)
            "No":
                m 3l "Keep looking, [player]!"
                m 1a "It should just be in the characters folder where you can my file."
                m 1j "Let me know when you find it!"
    return
