# Module that contains all workflow-specific shield functions
#
# Please avoid putting generalized shield functions in here

init python:
    # please add descriptions of workflows and what needs to be
    # enabled / disabled

    ######################### Full Disable ####################################
    # Not a workflow, just a specific set of shield functions that disable
    # and enable core interactions. Certain RenPy / DDLC-based interactions
    # may still work even when this shield is raised
    def mas_DropShield_full():
        """
        Enables:
            - Talk button + hotkey
            - Music button + hotkey + volume keys + mute key
            - Play button + hotkey
            - Calendar overlay
            - Escape key
        """
        mas_HKDropShield()
        mas_OVLDropShield()
        enable_esc()


    def mas_RaiseShield_full():
        """
        Disables:
            - Talk button + hotkey
            - Music button + hotkey + volume keys + mute key
            - Play button + hotkey
            - Calendar overlay
            - Escape key
        """
        mas_HKRaiseShield()
        mas_OVLRaiseShield()
        disable_esc()


    #################### Allow Dialogue workflow ##############################
    # Used when Monika is speaking.
    def mas_DropShield_dlg():
        """
        Enables:
            - Talk button + hotkey
            - Play button + hotkey
            - Calendar overlay

        Intended Flow:
            - Monika stops talking

        Sets:
            - mas_globals.dlg_workflow to Flase
        """
        store.mas_hotkeys.talk_enabled = True
        store.mas_hotkeys.play_enabled = True
        store.mas_globals.dlg_workflow = False
        mas_calDropOverlayShield()

    
    def mas_RaiseShield_dlg():
        """
        Disables:
            - Talk button + hotkey
            - Play button + hotkey
            - Calendar overlay

        Intended Flow:
            - Monika starts talking

        Sets:
            - mas_globals.dlg_workflow to True
        """
        store.mas_hotkeys.talk_enabled = False
        store.mas_hotkeys.play_enabled = False
        store.mas_globals.dlg_workflow = True
        mas_calRaiseOverlayShield()


    ################### Non-spaceroom start workflow ##########################
    # Used when we do not start in the spaceroom, but allow for escape
    def mas_DropShield_nspr():
        """
        Enables:
            - Talk button + hotkey
            - Music button + hotkey + volume keys + mute key
            - Play button + hotkey
            - Calendar overlay

        Intended Flow:
            - Game is returning to spaceroom after an inital start outside
            - Escape was NOT disabled
            - We were in a dialogue workflow
        """
        store.mas_globals.dlg_workflow = False
        mas_HKDropShield()
        mas_OVLDropShield()


    def mas_RaiseShield_nspr():
        """
        Disables:
            - Talk button + hotkey
            - Music button + hotkey + volume keys + mute key
            - Play button + hotkey
            - Calendar overlay

        Intended Flow:
            - Game just started, but we do not want to enter the spaceroom
            - Escape should NOT be disabled
            - We are entering a dialogue workflow
        """
        store.mas_globals.dlg_workflow = True
        mas_HKRaiseShield()
        mas_OVLRaiseShield()


    ################### Music Menu opened workflow ############################
    # Used when the music menu opens.
    def mas_DropShield_mumu():
        """
        Enables:
            - Talk button + hotkey
            - Music button
            - Play button + hotkey
            - Calendar overlay

        Intended Flow:
            - The Music menu is closed
        """
        store.mas_hotkeys.talk_enabled = True
        store.mas_hotkeys.play_enabled = True
        mas_OVLDropShield()


    def mas_RaiseShield_mumu():
        """
        Disables:
            - Talk button + hotkey
            - Music button
            - Play button + hotkey
            - Calendar overlay           

        Intended Flow:
            - The Music menu is opened
        """
        store.mas_hotkeys.talk_enabled = False
        store.mas_hotkeys.play_enabled = False
        mas_OVLRaiseShield()

