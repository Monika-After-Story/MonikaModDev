#Whether we want notifs or not
default persistent._mas_enable_notifications = False

init python:
    import sys
    sys.path.extend((renpy.config.gamedir + '\\python-packages\\win32', renpy.config.gamedir +'\\python-packages\\win32\\Lib'))
    import balloontip
    #Going to import win32gui for use in destroying notifs
    import win32gui

    #Now we initialize the notification class
    tip = balloontip.WindowsBalloonTip()

    #Now we set the hwnd of this temporarily
    tip.hwnd = None

    #List of notif quips
    notif_quips = [
        persistent.playername + ", I want to talk to you about something.",
        "Are you there, " + persistent.playername + "?",
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

    #List of hwnd IDs to destroy if we want to
    destroy_list = list()

#Notif creation label.
#Title: Notification heading text
#Body: Notification body text
label display_notif(title, body):
    #Make the notif
    play sound "mod_assets/sounds/effects/notif.wav"
    $ tip.showWindow(title,body)

    #We need the IDs of the notifs to delete them from the tray
    $ destroy_list.append(tip.hwnd)
    return

#START: Utility Methods
init python:
    def mas_getActiveWindow():
        from win32gui import GetWindowText, GetForegroundWindow
        return GetWindowText(GetForegroundWindow()).lower()

    def mas_isFocused():
        return mas_getActiveWindow() == config.name.lower()

    def mas_isInActiveWindow(keywords):
        return len([s for s in keywords if s.lower() not in mas_getActiveWindow()]) == 0


#START: Window Reacts
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_whatwatching",
            unlocked=False,
            rules={"no unlock": None},
            conditional="mas_isInActiveWindow(['youtube'])",
            action=EV_ACT_PUSH
        )
    )

init 7 python:
    mas_getEV('monika_whatwatching').conditional = "mas_isInActiveWindow(['youtube'])"
    mas_getEV('monika_whatwatching').action = EV_ACT_PUSH


label monika_whatwatching:
    call display_notif("Monika","What are you watching, "+player+"?")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_lookingat",
            unlocked=False,
            rules={"no unlock": None},
            conditional="mas_isInActiveWindow(['r34', 'monika'])",
            action=EV_ACT_PUSH
        )
    )

init 7 python:
    mas_getEV('monika_lookingat').conditional = "mas_isInActiveWindow(['r34', 'monika'])"
    mas_getEV('monika_lookingat').action = EV_ACT_PUSH

label monika_lookingat:
    call display_notif("Monika", "Hey, "+player+"...what are you looking at?")
    $ queueEvent('monika_nsfw')
    return