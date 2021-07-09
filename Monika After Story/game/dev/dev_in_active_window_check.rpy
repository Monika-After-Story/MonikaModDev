init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_inActiveWindowCheck",
            prompt="TEST IN ACTIVE WINDOW",
            category=['dev'],
            pool=True,
            unlocked=True
        )
    )


label monika_inActiveWindowCheck:
    $ active_window_regexp = None
    m 1hub "Okay, [player]!"
    m 3eub "Put a regexp into 'active_window_regexp' so I can use that to check."
    m 1eua "Okay, I'll pause for 3 seconds, switch to the window and then I'll tell you if those keywords were in there."
    pause 3.0
    $ inActiveWindow = mas_isInActiveWindow(regexp=active_window_regexp)
    m 1hua "Okay, your active window was: [mas_getActiveWindowHandle()], and your match returned [inActiveWindow]."
    return
