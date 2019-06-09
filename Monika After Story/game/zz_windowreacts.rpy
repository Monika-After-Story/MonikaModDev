#NOTE: This ONLY works for Windows atm

#Whether Monika can use notifications or not
default persistent._mas_enable_notifications = False

#Whether notification sounds are enabled or not
default persistent._mas_notification_sounds = True

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

    #Group list, to populate the menu screen
    #NOTE: We do this so that we don't have to try to get a notification
    #In order for it to show up in the menu and in the dict
    _groups_list = [
        "Topic Alerts",
        "Window Reactions",
    ]

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

        #NOTE: This is part of the try/catch block. We only run this if there was no error in the try
        #Ensures that the game does not crash if we cannot load win32api or win32gui.
        else:
            import balloontip

            #Now we initialize the notification class
            tip = balloontip.WindowsBalloonTip()

            #Now we set the hwnd of this temporarily
            tip.hwnd = None

    #List of notif quips (used for topic alerts)
    notif_quips = [
        "[player], I want to talk to you about something.",
        "Are you there, [player]?",
        "Can you come here for a second?",
        "[player], do you have a second?",
        "I have something to tell you, [player]!",
    ]

    #List of hwnd IDs to destroy
    destroy_list = list()

    #START: Utility methods
    def mas_getActiveWindow(friendly=False):
        """
        Gets the active window name

        IN:
            friendly: whether or not the active window name is returned in a state usable by the user
        """
        if (
                renpy.windows
                and mas_windowreacts.can_show_notifs
                and persistent._mas_windowreacts_windowreacts_enabled
            ):
            from win32gui import GetWindowText, GetForegroundWindow

            if not friendly:
                return GetWindowText(GetForegroundWindow()).lower().replace(" ","")
            else:
                return GetWindowText(GetForegroundWindow()).lower()
        else:
            #TODO: Mac vers (if possible)
            #NOTE: We return "" so this doesn't rule out notifications
            return ""

    def mas_isFocused():
        """
        Checks if MAS is the focused window
        """
        #TODO: Mac vers (if possible)
        return store.mas_windowreacts.can_show_notifs and mas_getActiveWindow(True) == config.name.lower()

    def mas_isInActiveWindow(keywords):
        """
        Checks if ALL keywords are in the active window name

        IN:
            List of keywords
        """
        active_window = mas_getActiveWindow()
        return store.mas_windowreacts.can_show_notifs and len([s for s in keywords if s.lower() not in active_window]) == 0

    def mas_clearNotifs():
        """
        Clears all tray icons (also action center on win10)
        """
        if renpy.windows and store.mas_windowreacts.can_show_notifs:
            for index in range(len(destroy_list)-1,-1,-1):
                win32gui.DestroyWindow(destroy_list[index])
                destroy_list.pop(index)

    def mas_checkForWindowReacts():
        """
        Runs through events in the windowreact_db to see if we have a reaction, and if so, queue it
        """
        #Do not check anything if we're not supposed to
        if not persistent._mas_windowreacts_windowreacts_enabled or not store.mas_windowreacts.can_show_notifs:
            return

        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if (
                    (mas_isInActiveWindow(ev.category) and ev.unlocked and ev.checkAffection(mas_curr_affection))
                    and ((not store.mas_globals.in_idle_mode) or (store.mas_globals.in_idle_mode and ev.show_in_idle))
                    and ("notif-group" not in ev.rules or mas_notifsEnabledForGroup(ev.rules.get("notif-group")))
                ):
                #If we have a conditional, eval it and queue if true
                if ev.conditional and eval(ev.conditional):
                    queueEvent(ev_label)
                    ev.unlocked=False

                #Otherwise we just queue
                elif not ev.conditional:
                    queueEvent(ev_label)
                    ev.unlocked=False

                #Add the blacklist
                if "no unlock" in ev.rules:
                    mas_addBlacklistReact(ev_label)

    def mas_resetWindowReacts(excluded=persistent._mas_windowreacts_no_unlock_list):
        """
        Runs through events in the windowreact_db to unlock them

        IN:
            List of ev_labels to exclude from being unlocked
        """
        for ev_label, ev in mas_windowreacts.windowreact_db.iteritems():
            if ev_label not in excluded:
                ev.unlocked=True

    def mas_updateFilterDict():
        """
        Updates the filter dict with the groups in the groups list for the settings menu
        """
        for group in store.mas_windowreacts._groups_list:
            if persistent._mas_windowreacts_notif_filters.get(group) is None:
                persistent._mas_windowreacts_notif_filters[group] = False

    def mas_addBlacklistReact(ev_label):
        """
        Adds the given ev_label to the no unlock list

        IN:
            ev_label: eventlabel to add to the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label not in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.append(ev_label)

    def mas_removeBlacklistReact(ev_label):
        """
        Removes the given ev_label to the no unlock list if exists

        IN:
            ev_label: eventlabel to remove from the no unlock list
        """
        if renpy.has_label(ev_label) and ev_label in persistent._mas_windowreacts_no_unlock_list:
            persistent._mas_windowreacts_no_unlock_list.remove(ev_label)

    def mas_notifsEnabledForGroup(group):
        """
        Checks if notifications are enabled, and if enabled for the specified group

        IN:
            group: notification group to check
        """
        return persistent._mas_enable_notifications and persistent._mas_windowreacts_notif_filters.get(group,False)

    def mas_tryShowNotificationOSX(title, body):
        """
        Tries to push a notification to the notification center on macOS.
        If it can't it should fail silently to the user.

        IN:
            title: notification title
            body: notification body
        """
        os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(body,title))
    
    def mas_tryShowNotificationLinux(title, body):
        """
        Tries to push a notification to the notification center on Linux.
        If it can't it should fail silently to the user.

        IN:
            title: notification title
            body: notification body
        """
        os.system("notify-send '{0}' '{1}' -u low".format(title,body))


#Notification creation label
#IN:
#   title: Notification heading text
#   body: Notification body text
#   group: Notification group (for checking if we have this enabled)
#   skip_checks: Whether or not we skips checks

label display_notif(title, body, group=None, skip_checks=False):
    #We only show notifications if:
    #We are able to show notifs
    #MAS isn't the active window
    #User allows them
    #And if the notification group is enabled

    #OR if we skip checks
    #NOTE: THIS IS TO ONLY BE USED FOR INTRODUCTORY PURPOSES

    #First we want to create this location in the dict, but don't add an extra location if we're skipping checks
    if persistent._mas_windowreacts_notif_filters.get(group) is None and not skip_checks:
        $ persistent._mas_windowreacts_notif_filters[group] = False

    if (
            (
                mas_windowreacts.can_show_notifs
                and ((renpy.windows and not mas_isFocused()) or not renpy.windows)
                and mas_notifsEnabledForGroup(group)
            )
            or skip_checks
        ):

        #Play the notif sound if we have that enabled
        if persistent._mas_notification_sounds:
            play sound "mod_assets/sounds/effects/notif.wav"

        #Now we make the notif
        if (renpy.windows):
            # The Windows way
            $ tip.showWindow(renpy.substitute(title),renpy.substitute(body))

            #We need the IDs of the notifs to delete them from the tray
            $ destroy_list.append(tip.hwnd)

        elif (renpy.macintosh):
            # The macOS way
            $ mas_tryShowNotificationOSX(renpy.substitute(title),renpy.substitute(body))

        elif (renpy.linux):
            # The Linux way
            $ mas_tryShowNotificationLinux(renpy.substitute(title),renpy.substitute(body))
    return


#START: Window Reacts
init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="monika_whatwatching",
            category=['youtube'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label monika_whatwatching:
    call display_notif(m_name,"What are you watching, [player]?",'Window Reactions')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="monika_lookingat",
            category=['rule34', 'monika'],
            rules={"skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )

label monika_lookingat:
    call display_notif(m_name, "Hey, [player]...what are you looking at?",'Window Reactions')

    $ choice = random.randint(1,10)
    if choice == 1:
        $ queueEvent('monika_nsfw')

    elif choice == 2:
        $ queueEvent('monika_pleasure')

    elif choice < 4:
        show monika 1rsbssdlu
        pause 5.0

    elif choice < 7:
        show monika 2tuu
        pause 5.0

    else:
        show monika 2ttu
        pause 5.0
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="monika_monikamoddev",
            category=['monikamoddev'],
            rules={"notif-group": "Window Reactions", "skip alert": None},
            show_in_idle=True
        ),
        code="WRS"
    )


label monika_monikamoddev:
    call display_notif(m_name, "Aww, are you doing something for me?\nYou're so sweet~",'Window Reactions')
    return
