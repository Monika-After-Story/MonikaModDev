#NOTE: This ONLY works for Windows atm

#Whether Monika can use notifications or not
default persistent._mas_enable_notifications = False

#Whether Monika can see your active window or not
default persistent._mas_windowreacts_windowreacts_enabled = False

#Persistent windowreacts db
default persistent._mas_windowreacts_database = dict()

#A global list of events we DO NOT want to unlock on a new session
default persistent._mas_windowreacts_no_unlock_list = list()

#A dict of locations where notifs are used, and if they're enabled for said location
default persistent._mas_windowreacts_notif_filters = dict()

init -10 python in mas_windowreacts:
    #We need this in case we cannot get access to the libs, so everything can still run
    can_show_notifs = True

    #The windowreacts db
    windowreact_db = {}

init python:
    import os
    #The initial setup

    #We can only do this on windows
    if renpy.windows:
        #We need to extend the sys path to see our packages
        import sys
        sys.path.append(renpy.config.gamedir + '\\python-packages\\')

        #We try/catch/except to make sure the game can run if load fails here
        try:
            #Going to import win32gui for use in destroying notifs
            import win32gui
            #Import win32api so we know if we can or cannot use notifs
            import win32api

        except ImportError:
            #If we fail to import, then we're going to have to make sure nothing can run.
            store.mas_windowreacts.can_show_notifs = False

            #Log this
            store.mas_utils.writelog(
                "[WARNING]: win32api/win32gui failed to be imported, disabling notifications.\n"
            )

        else:
            import balloontip

            #Now we initialize the notification class
            try:
                tip = balloontip.WindowsBalloonTip()

            except:
                #So reload still works
                tip.classAtom = win32gui.UnregisterClass(tip.classAtom, tip.hinst)
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
        if renpy.windows and mas_windowreacts.can_show_notifs:
            from win32gui import GetWindowText, GetForegroundWindow
            return GetWindowText(GetForegroundWindow()).lower()
        else:
            #TODO: Mac vers (if possible)
            return ""

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        #TODO: Mac vers
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindow() == config.name.lower()

    def mas_isInActiveWindow(keywords):
        """
        Checks if ALL keywords are in the active window name

        IN:
            List of keywords
        """
        return store.mas_windowreacts.can_show_notifs and len([s for s in keywords if s.lower() not in mas_getActiveWindow()]) == 0

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows and store.mas_windowreacts.can_show_notifs:
            for hwnd in destroy_list:
                win32gui.DestroyWindow(hwnd)
                destroy_list.remove(hwnd)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        #Do not check anything if we're not enabling notifications
        if not persistent._mas_enable_notifications or not store.mas_windowreacts.can_show_notifs:
            return

        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if (
                    (mas_isInActiveWindow(ev.category) and ev.unlocked)
                    and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                ):
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
    
    def mas_tryShowNotificationOSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body,title))
    
    def mas_tryShowNotificationLinux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.
        """
        os.system("notify-send '{0}' '{1}' -u low".format(title,body))


label display_notif(title, body, location, skip_checks=False):
    #Notif creation label
    #Title: Notification heading text
    #Body: Notification body text

    #We only show notifications if:
    #We are able to show notifs
    #MAS isn't the active window
    #User allows them
    #And they're allowed in the location they're used in

    #OR if we skip checks
    #NOTE: THIS IS TO ONLY BE USED FOR INTRODUCTORY PURPOSES

    #First we want to create this location in the dict
    if persistent._mas_windowreacts_notif_filters.get(location) is None:
        $ persistent._mas_windowreacts_notif_filters[location] = False

    if (
            (mas_windowreacts.can_show_notifs
            and not mas_isFocused()
            and persistent._mas_enable_notifications
            and persistent._mas_windowreacts_notif_filters.get(location))
            or skip_checks
        ):

        #Make the notif
        if (renpy.windows):
            # The Windows way
            play sound "mod_assets/sounds/effects/notif.wav"
            $ tip.showWindow(title,body)

            #We need the IDs of the notifs to delete them from the tray
            $ destroy_list.append(tip.hwnd)

        elif (renpy.macintosh):
            # The macOS way
            $ mas_tryShowNotificationOSX(title,body)

        elif (renpy.linux):
            # The Linux way
            $ mas_tryShowNotificationLinux(title,body)
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
    call display_notif("Monika","What are you watching, "+player+"?",'Window Reactions')
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
    call display_notif("Monika", "Hey, "+player+"...what are you looking at?",'Window Reactions')
    $ queueEvent('monika_nsfw')
    return