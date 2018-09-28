# Module that is just for hotkeys and other keymaps
#

init -10 python in mas_hotkeys:
    # earlier store for some hotkey related state

    # True means allow Dismiss, False means do not
    allow_dismiss = True

    def allowdismiss():
        """
        Justreturns current state of no_dismiss
        """
        return allow_dismiss


init -1 python in mas_hotkeys:
    # store for the main 3 hotkeys.

    # True means the talk hotkey is enabled, False means it is not
    talk_enabled = False

    # True means the music hotkey is enabled, False means its not
    music_enabled = False

    # True means the play hotkey is enabled, False means its not
    play_enabled = False

    ## other keys
    # True means the music lowering / stopping functions will work.
    # False means they will not
    mu_stop_enabled = True

    # True means dont allow windows to be hidden
    no_window_hiding = False


init python:

    def mas_HKRaiseShield():
        """RUNTIME ONLY
        Disables the main hotkeys
        """
        store.mas_hotkeys.talk_enabled = False
        store.mas_hotkeys.music_enabled = False
        store.mas_hotkeys.play_enabled = False


    def mas_HKDropShield():
        """RUNTIME ONLY
        Enables the main hotkeys
        """
        store.mas_hotkeys.talk_enabled = True
        store.mas_hotkeys.music_enabled = True
        store.mas_hotkeys.play_enabled = True


    def mas_HKIsEnabled():
        """
        RETURNS: True if all the main hotkeys are enabled, False otherwise
        """
        return (
            store.mas_hotkeys.talk_enabled
            and store.mas_hotkeys.music_enabled
            and store.mas_hotkeys.play_enabled
        )


    def mas_HKCanQuietMusic():
        """
        RETURNS: True if we can lower or stop the music, False if not
        """
        return (
            store.mas_hotkeys.music_enabled
            and store.mas_hotkeys.mu_stop_enabled
        )


    def enable_esc():
        """
        Enables the escape key so you can go to the game menu

        NOTE: this also enables opening the game menu from other means
        """
        global quick_menu
        quick_menu = True


    def disable_esc():
        """
        disables the escape key so you cant go to game menu

        NOTE: this also disables opening the game menu from other means
        """
        global quick_menu
        quick_menu = False


    def _mas_hk_mute_music():
        """
        hotkey specific muting / unmuting music channel
        """
        if store.mas_hotkeys.music_enabled and not _windows_hidden:
            mute_music(store.mas_hotkeys.mu_stop_enabled)


    def _mas_hk_inc_musicvol():
        """
        hotkey specific music volume increasing
        """
        if store.mas_hotkeys.music_enabled and not _windows_hidden:
            inc_musicvol()


    def _mas_hk_dec_musicvol():
        """
        hotkey specific music volume decreasing
        """
        if mas_HKCanQuietMusic() and not _windows_hidden:
            dec_musicvol()


    def _mas_hk_show_dialogue_box():
        """
        hotkey specific show dialgoue box
        """
        if store.mas_hotkeys.talk_enabled and not _windows_hidden:
            show_dialogue_box()


    def _mas_hk_pick_game():
        """
        hotkey specific pick game
        """
        if store.mas_hotkeys.play_enabled and not _windows_hidden:
            pick_game()


    def _mas_hk_select_music():
        """
        Runs the select music function if we are allowed to.
        INTENDED FOR HOTKEY USAGE ONLY
        """
        if store.mas_hotkeys.music_enabled and not _windows_hidden:
            select_music()


    def _mas_game_menu():
        """
        Wrapper aound _invoke_game_menu that follows additional ui rules
        """
        if not _windows_hidden:
            prev_disable_animations = persistent._mas_disable_animations
            _invoke_game_menu()

            # call backs for the game menu
            if prev_disable_animations != persistent._mas_disable_animations:
                mas_drawSpaceroomMasks()


    def _mas_quick_menu_cb(screen_name):
        """
        Opens game menu to the appropraite quick screen.
        NOTE: no checks are done here, please do not fuck this.
        """
        if not _windows_hidden:
            prev_disable_animations = persistent._mas_disable_animations
            renpy.call_in_new_context(
                "_game_menu", 
                _game_menu_screen=screen_name
            )

            # call backs for the game menu
            if prev_disable_animations != persistent._mas_disable_animations:
                mas_drawSpaceroomMasks()


    def _mas_hide_windows():
        """
        Wrapper around the _hide_windows label that hides windows
        """
        if not store.mas_hotkeys.no_window_hiding:
            renpy.call_in_new_context("_hide_windows")


    def set_keymaps():
        #
        # Sets the keymaps
        #
        # ASSUMES:
        #   config.keymap
        #   config.underlay
        #Add keys for new functions
        config.keymap["open_dialogue"] = ["t","T"]
        config.keymap["change_music"] = ["noshift_m","noshift_M"]
        config.keymap["play_game"] = ["p","P"]
        config.keymap["mute_music"] = ["shift_m","shift_M"]
        config.keymap["inc_musicvol"] = [
            "shift_K_PLUS","K_EQUALS","K_KP_PLUS"
        ]
        config.keymap["dec_musicvol"] = [
            "K_MINUS","shift_K_UNDERSCORE","K_KP_MINUS"
        ]

        # get replace the game menu with our version (to block certain
        # workflows correctly)
        config.keymap["mas_game_menu"] = list(config.keymap["game_menu"])
        config.keymap["game_menu"] = []

        # get and replcae the hide_windows with our version
        config.keymap["mas_hide_windows"] = list(config.keymap["hide_windows"])
        config.keymap["hide_windows"] = []

        # Define what those actions call
        config.underlay.append(
            renpy.Keymap(open_dialogue=_mas_hk_show_dialogue_box)
        )
        config.underlay.append(renpy.Keymap(change_music=_mas_hk_select_music))
        config.underlay.append(renpy.Keymap(play_game=_mas_hk_pick_game))
        config.underlay.append(renpy.Keymap(mute_music=_mas_hk_mute_music))
        config.underlay.append(renpy.Keymap(inc_musicvol=_mas_hk_inc_musicvol))
        config.underlay.append(renpy.Keymap(dec_musicvol=_mas_hk_dec_musicvol))
        config.underlay.append(renpy.Keymap(mas_game_menu=_mas_game_menu))
        config.underlay.append(renpy.Keymap(mas_hide_windows=_mas_hide_windows))

        # finally enable those buttons
        mas_HKDropShield()
