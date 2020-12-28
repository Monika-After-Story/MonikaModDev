rpy python 3
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
    $ active_window_keys = None
    m 1hub "Okay, [player]!"

    m 3eua "Do you want it to be inclusive?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you want it to be inclusive?{fast}"

        "Yes.":
            $ non_inclusive = False

        "No.":
            $ non_inclusive = True

    m 1hub "Okay!"
    m 3eub "Put some keywords in the 'active_window_keys' list now."
    m 1eua "Okay, I'll pause for 3 seconds, switch to the window and then I'll tell you if those keywords were in there."
    pause 3.0
    $ ActiveWindow = mas_getActiveWindow(True)
    $ inActiveWindow = mas_isInActiveWindow(active_window_keys, non_inclusive)
    m 1hua "Okay, your active window was: [ActiveWindow], and your keys returned [inActiveWindow]."
    return
