rpy python 3
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_check_window",
            prompt="TEST ACTIVE WINDOW CHECK",
            category=['dev'],
            random=False,
            pool=True,
            unlocked=True
        )
    )

label monika_check_window:
    m 1hub "Okay, [player]!"
    m 2dsc "Let's see...your active window is.{w=0.5}.{w=0.5}."

    pause 2.0

    if mas_isFocused():
        m 1hub "Me, yay!"
    else:
        $ active_wind = mas_getActiveWindow(True)
        if active_wind:
            m 3eua "[active_wind]."
        else:
            m 1hksdlb "[player], you don't have an active window!"
    return
