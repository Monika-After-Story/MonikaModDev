#NOTE: This ONLY works for Windows atm

#Whether we want notifs or not
default persistent._mas_enable_notifications = False

#Persistent windowreacts db
default persistent._mas_windowreacts_database = dict()

#A global list of events we DO NOT want to unlock on a new session
default persistent._mas_windowreacts_no_unlock_list = list()

init -10 python in mas_windowreacts:
    #The windowreacts db
    windowreact_db = {}

init python:
    #The initial setup
    #We need to extend the sys path to see our packages
    import sys
    sys.path.extend((renpy.config.gamedir + '\\python-packages\\win32', renpy.config.gamedir +'\\python-packages\\win32\\Lib'))
    import balloontip
    #Going to import win32gui for use in destroying notifs
    import win32gui

    #Now we initialize the notification class
    tip = balloontip.WindowsBalloonTip()

    #Now we set the hwnd of this temporarily
    tip.hwnd = None

    #List of notif quips (used for topic alerts)
    notif_quips = [
        persistent.playername + ", I want to talk to you about something.",
        "Are you there, " + persistent.playername + "?",
        "Can you come here for a second?",
        persistent.playername + ", do you have a second?",
        "I have something to tell you, " + persistent.playername + "!",
    ]

    #List of name quips (also used for topic alerts)
    name_quips = [
        "Sweetheart",
        "Darling",
        "Honey",
        "Angel",
        "Monika",
        persistent._mas_monika_nickname
    ]

    #List of hwnd IDs to destroy
    destroy_list = list()

    #START: Utility methods
    def mas_getActiveWindow():
        from win32gui import GetWindowText, GetForegroundWindow
        return GetWindowText(GetForegroundWindow()).lower()

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        return mas_getActiveWindow() == config.name.lower()

    def mas_isInActiveWindow(keywords):
        """
        Checks if ALL keywords are in the active window name

        IN:
            List of keywords
        """
        return len([s for s in keywords if s.lower() not in mas_getActiveWindow()]) == 0

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows:
            for hwnd in destroy_list:
                win32gui.DestroyWindow(hwnd)
                destroy_list.remove(hwnd)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if mas_isInActiveWindow(ev.category):
                if (not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle):
                    queueEvent(ev_label)
                    ev.unlocked=False

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them

        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if ev_label not in excluded:
                ev.unlocked=True


label display_notif(title, body):
    #Notif creation label
    #Title: Notification heading text
    #Body: Notification body text

    #We only show notifications if we're on windows, and MAS isn't the active window
    if renpy.windows and not mas_isFocused() and persistent._mas_enable_notifications:
        #Make the notif
        play sound "mod_assets/sounds/effects/notif.wav"
        $ tip.showWindow(title,body)

        #We need the IDs of the notifs to delete them from the tray
        $ destroy_list.append(tip.hwnd)
    return


#START: Window Reacts
init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="monika_whatwatching",
            category=['youtube'],
            show_in_idle=True
        ),
        code="WRS"
    )

label monika_whatwatching:
    call display_notif("Monika","What are you watching, "+player+"?")
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="monika_lookingat",
            category=['r34', 'monika'],
            show_in_idle=True
        ),
        code="WRS"
    )

label monika_lookingat:
    call display_notif("Monika", "Hey, "+player+"...what are you looking at?")
    $ queueEvent('monika_nsfw')
    return