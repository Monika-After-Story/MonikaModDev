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
    $ atv_wnd_keys = None
    m 1hub "Okay, [player]!"
    m 3eub "Put some keywords in atv_wnd_keys now."
    m 1eua "Okay, I'll pause for 3 seconds, switch to the window and then I'll tell you if those were in there."
    pause 3.0
    $ ActiveWindow = mas_getActiveWindow(True)
    $ inActiveWindow = mas_isInActiveWindow(atv_wnd_keys)
    m 1hua "Okay, your active window was: [ActiveWindow], and your keys returned [inActiveWindow]."
    return