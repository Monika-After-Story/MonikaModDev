init python:
    #We need to make sure reload works
    try:
        UnregisterClass(tip.classAtom,tip.hinst)
    except:
        pass

    #Firstly, we want to create the notification class
    import sys
    sys.path.extend((renpy.config.gamedir + '\\python-packages\\win32', renpy.config.gamedir +'\\python-packages\\win32\\Lib'))
    import balloontip
    tip = balloontip.WindowsBalloonTip()

label display_notif(title, body):
    $ tip.showWindow(title,body)
    return

#Need to keep testing timing
label monika_loveyou:
    call display_notif("Monika", "I just wanted to tell you...")
    pause 15.0
    call display_notif("Monika", "I love you!")
    return

#START: Utility Methods
init python:
    def mas_getActiveWindow():
        from win32gui import GetWindowText, GetForegroundWindow
        return GetWindowText(GetForegroundWindow()).lower()

    def mas_isFocused():
        return mas_getActiveWindow() == config.name.lower()


#START: Testing labels
label check_window:
    m 1hub "Okay, [player]!"
    m 2dsc "Let's see, your active window is.{w=0.5}.{w=0.5}."

    pause 5.0

    if mas_isFocused():
        m 1hub "Me, yay!"
    else:
        $ active_wind = mas_getActiveWindow()
        m 3eua "[active_wind]."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whatwatching",
            rules={"no unlock": None},
            unlocked=False,
            conditional="'youtube' in mas_getActiveWindow()",
            action=EV_ACT_PUSH
        )
    )


label monika_whatwatching:
    call display_notif("Monika","What are you watching, "+player+"?")
    return