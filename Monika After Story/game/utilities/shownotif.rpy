#Whether we want notifs or not
default persistent._mas_enable_notifications = False

#Need the activewindow db
default persistent._mas_windowreacts_database = dict()
init python:
    #List of notif quips
    notif_quips = [
        persistent.playername + ", I want to talk to you about something.",
        "Are you there" + persistent.playername + "?",
        "Can you come here for a second?",
        persistent.playername + ", do you have a second?",
        "I have something to tell you, " + persistent.playername + "!",
    ]

    #List of name quips
    name_quips = [
        "Sweetheart",
        "Darling",
        "Honey",
        "Angel",
        "Monika",
    ]

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
    play sound "mod_assets/sounds/effects/notif.wav"
    $ tip.showWindow(title,body)
    return

#START: Utility Methods
init python:
    def mas_getActiveWindow():
        from win32gui import GetWindowText, GetForegroundWindow
        return GetWindowText(GetForegroundWindow()).lower()

    def mas_isFocused():
        return mas_getActiveWindow() == config.name.lower()


init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
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