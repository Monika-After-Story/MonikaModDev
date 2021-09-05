# START: vars
# Whether dark mode is enabled or not
default persistent._mas_dark_mode_enabled = False

# Whether auto ui change is enabled or not
default persistent._mas_auto_mode_enabled = False

init -1 python in mas_globals:
    # None on init, True if dark ui, False otherwise
    dark_mode = None

    # The door-knock greets, if door open, need to keep a broken textbox, so this would be set False for those before the spaceroom call
    change_textbox = True

    # The colors we're using for buttons
    button_text_hover_color = None
    button_text_idle_color = None

init -201 python in mas_ui:

    dark_suffix = "_dark"

    # img strings and other constants

    # confirm
    CNF_BG = "gui/overlay/confirm.png"

    # selector
    SEL_SB_FRAME = "mod_assets/frames/black70_pinkborder100_5px.png"

init -200 python in mas_ui:

    style_stash = {}

    dark_button_text_idle_color = "#FD5BA2"
    dark_button_text_hover_color = "#FFABD8"
    dark_button_text_insensitive_color = "#8C8C8C"

    light_button_text_idle_color = "#000"
    light_button_text_hover_color = "#fa9"
    light_button_text_insensitive_color = "#8C8C8C"

    # ---- files ----

    # confirm screen
    cm_bg = CNF_BG

    # selector
    sel_sb_frame = SEL_SB_FRAME

    SCROLLABLE_MENU_X = 680
    SCROLLABLE_MENU_Y = 40

    SCROLLABLE_MENU_W = 560

    SCROLLABLE_MENU_TALL_H = 640
    SCROLLABLE_MENU_MEDIUM_H = 572
    SCROLLABLE_MENU_LOW_H = 528
    SCROLLABLE_MENU_VLOW_H = 484

    SCROLLABLE_MENU_TXT_TALL_H = 528
    SCROLLABLE_MENU_TXT_MEDIUM_H = 440
    SCROLLABLE_MENU_TXT_LOW_H = 396

    SCROLLABLE_MENU_XALIGN = -0.05

    # HOW TO CHOOSE:
    #    TXT for menus w/ the dlg box
    #    TALL for menus w/o final buttons
    #    MEDIUM for menus w/ one final button
    #    LOW for menus w/ 2 final buttons
    #    VLOW for menus w/ 3 final buttons

    SCROLLABLE_MENU_TALL_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_TALL_H)
    SCROLLABLE_MENU_MEDIUM_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_MEDIUM_H)
    SCROLLABLE_MENU_LOW_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_LOW_H)
    SCROLLABLE_MENU_VLOW_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_VLOW_H)

    SCROLLABLE_MENU_TXT_TALL_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_TXT_TALL_H)
    SCROLLABLE_MENU_TXT_MEDIUM_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_TXT_MEDIUM_H)
    SCROLLABLE_MENU_TXT_LOW_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_TXT_LOW_H)

# START: Helper method(s)
init python:
    import store.mas_globals as mas_globals
    import store.mas_ui as mas_ui

    def mas_getTimeFile(filestring):
        """
        Returns the filestring pointing to the right asset for day/night

        IN:
            the DAY variant of the image file needed

        RETURNS:
            filestring pointing to the right path
        """

        # Light handling
        if not mas_globals.dark_mode:
            return filestring

        # Dark handling
        else:
            # Need to isolate this for just the extension and the path so we can form a new one
            if '.' in filestring:
                extension = filestring[filestring.index('.'):]
                path = filestring[:filestring.index('.')]
                return path + "_d" + extension
            # If that fails then we just return the normal one
            return filestring

    # FIXME: the next four methods could be refactored into some sort of "StyleUtils" static class
    def mas_swapStyle(base_name, dark_name, morning_flag):
        """
        Swaps the single style between default and dark variants.

        IN:
            morning_flag - Light/dark mode switch
        """
        if base_name not in mas_ui.style_stash:
            mas_ui.style_stash[base_name] = getattr(style, base_name)

        if morning_flag:
            stashed_style = mas_ui.style_stash[base_name]
            setattr(style, base_name, mas_ui.style_stash[base_name])
        else:
            dark_style = getattr(style, dark_name)
            setattr(style, base_name, dark_style)

    def mas_hasDarkStyle(style_name):
        """
        Check if selected style has a dark alternative.
        """
        dark_style_name = style_name + mas_ui.dark_suffix

        for other_tuple in renpy.style.styles:
            other_name = other_tuple[0]
            if other_name == dark_style_name:
                return True

        return False

    def mas_isDarkStyle(style_name):
        """
        Check if selected style is a dark style.
        """
        return style_name.endswith(mas_ui.dark_suffix)

    def mas_isTextDarkStyle(style_name):
        """
        Check if selected style is a text_dark style.
        """
        text_dark_suffix = "_text" + mas_ui.dark_suffix
        return style_name.endswith(text_dark_suffix)

    def mas_darkMode(morning_flag=False):
        """
        Swaps all styles to dark/light mode provided on the input

        IN:
            morning_flag - if True, light mode, if False, dark mode
        """
        # Create aliases
        # FIXME: could be done on startup for some speedup
        new_aliases = {}

        for style_tuple, style_ptr in renpy.style.styles.iteritems():
            style_name = style_tuple[0]
            if mas_isTextDarkStyle(style_name):
                text_dark_suffix = "_text" + mas_ui.dark_suffix
                suffix_len = len(text_dark_suffix)
                alias_name = style_name[:-suffix_len] + mas_ui.dark_suffix + "_text"
                if not style.exists(alias_name):
                    new_aliases[alias_name] = style_ptr

        for alias_name, alias_style_ptr in new_aliases.iteritems():
            setattr(style, alias_name, alias_style_ptr)

        # Automagically switch every style which has a dark variant
        for style_tuple in renpy.style.styles.keys():
            style_name = style_tuple[0]
            if not mas_isDarkStyle(style_name) and mas_hasDarkStyle(style_name):
                dark_style_name = style_name + mas_ui.dark_suffix
                mas_swapStyle(style_name, dark_style_name, morning_flag)

        if not morning_flag:
            # Handle the global swaps
            mas_globals.dark_mode = True

            mas_globals.button_text_idle_color = mas_ui.dark_button_text_idle_color
            mas_globals.button_text_hover_color = mas_ui.dark_button_text_hover_color
            mas_globals.button_text_insensitive_color = mas_ui.dark_button_text_insensitive_color

            # Textbox
            if mas_globals.change_textbox:
                style.say_window = style.window_dark

        else:
            # Handle the global swaps
            mas_globals.dark_mode = False

            mas_globals.button_text_idle_color = mas_ui.light_button_text_idle_color
            mas_globals.button_text_hover_color = mas_ui.light_button_text_hover_color
            mas_globals.button_text_insensitive_color = mas_ui.light_button_text_insensitive_color

            # Textbox
            if mas_globals.change_textbox:
                style.say_window = style.window

        # Timefile changes
        mas_ui.cm_bg = mas_getTimeFile(mas_ui.CNF_BG)
        mas_ui.sel_sb_frame = mas_getTimeFile(mas_ui.SEL_SB_FRAME)

        # Reset the global flag
        mas_globals.change_textbox = True

        style.rebuild()

# START: Settings menu helpers
init python in mas_settings:
    _persistent = renpy.game.persistent

    ui_changed = False
    dark_mode_clicked = False

    import store
    def _auto_mode_toggle():
        """
        Handles the toggling of fields so the menu options become mutually exclusive
        """
        # We're disablng this so we only set it false
        if _persistent._mas_auto_mode_enabled:
            _persistent._mas_auto_mode_enabled = False
            if store.mas_current_background.isFltNight():
                store.mas_darkMode(True)

        # But here we need to also switch the other button since this is mutually exclusive
        else:
            _persistent._mas_auto_mode_enabled = True
            _persistent._mas_dark_mode_enabled = False

    def _dark_mode_toggle():
        """
        Handles the toggling of fields so the menu options become mutually exclusive
        """
        if _persistent._mas_dark_mode_enabled:
            _persistent._mas_dark_mode_enabled = False

        else:
            _persistent._mas_dark_mode_enabled = True
            _persistent._mas_auto_mode_enabled = False

        global dark_mode_clicked
        dark_mode_clicked = True

    def _ui_change_wrapper(*args):
        """
        Wrapper around UI changes

        IN:
            *args - values to pass to dark mode
        """
        global ui_changed
        ui_changed = True
        store.mas_darkMode(*args)


# START: Generic button styles
# FIXME: can be renamed or removed later
style generic_button_base:
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style generic_button_light is generic_button_base:
    background Frame("mod_assets/buttons/generic/[prefix_]bg.png", Borders(5, 5, 5, 5), tile=False)

style generic_button_dark is generic_button_base:
    background Frame("mod_assets/buttons/generic/[prefix_]bg_d.png", Borders(5, 5, 5, 5), tile=False)

style generic_button_text_base:
    font gui.default_font
    size gui.text_size
    align (0.5, 0.1)
    outlines []

style generic_button_text_light is generic_button_text_base:
    idle_color mas_ui.light_button_text_idle_color
    hover_color mas_ui.light_button_text_hover_color
    insensitive_color mas_ui.light_button_text_insensitive_color

style generic_button_text_dark is generic_button_text_base:
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    insensitive_color mas_ui.dark_button_text_insensitive_color

# fancy checkbox buttons lose the box when selected
# and the entire frame gets colored
style generic_fancy_check_button:
    properties gui.button_properties("check_button")
    foreground "mod_assets/buttons/checkbox/[prefix_]fancy_check.png"
    hover_background Solid("#ffe6f4")
    selected_background Solid("#FFBDE1")

style generic_fancy_check_button_dark:
    properties gui.button_properties("check_button_dark")
    foreground "mod_assets/buttons/checkbox/[prefix_]fancy_check.png"
    hover_background Solid("#d9739c")
    selected_background Solid("#CE4A7E")

style generic_fancy_check_button_text is gui_button_text:
    properties gui.button_text_properties("generic_fancy_check_button")
    font "gui/font/Halogen.ttf"
    color "#BFBFBF"
    hover_color "#000000"
    selected_color "#000000"
    outlines []

style generic_fancy_check_button_text_dark is gui_button_text_dark:
    properties gui.button_text_properties("generic_fancy_check_button_dark")
    font "gui/font/Halogen.ttf"
    color "#BFBFBF"
    hover_color "#FFAA99"
    selected_color "#FFAA99"
    outlines []

# START: image definitions
image menu_bg:
    topleft
    ConditionSwitch(
        "not mas_globals.dark_mode", "gui/menu_bg.png",
        "mas_globals.dark_mode", "gui/menu_bg_d.png")
    menu_bg_move

image game_menu_bg:
    topleft
    ConditionSwitch(
        "not mas_globals.dark_mode", "gui/menu_bg.png",
        "mas_globals.dark_mode", "gui/menu_bg_d.png")
    menu_bg_loop

image menu_nav:
    ConditionSwitch(
        "not mas_globals.dark_mode", "gui/overlay/main_menu.png",
        "mas_globals.dark_mode", "gui/overlay/main_menu_d.png")
    menu_nav_move

init -1 python:

    # set default and interface font groups
    # NOTE: this MUST be after -2
    gui.default_font = FontGroup().add(
        "mod_assets/font/SourceHanSansK-Regular.otf", 0xac00, 0xd7a3 # kr
    ).add(
        "mod_assets/font/SourceHanSansSC-Regular.otf", 0x4e00, 0x9faf # s-cn
    ).add(
        "mod_assets/font/mplus-2p-regular.ttf", 0x3000, 0x4dff  # jp + others
    ).add(
        "gui/font/Aller_Rg.ttf", 0x0000, 0xffff # latin-1
    )
    gui.interface_font = gui.default_font
    gui.button_text_font = gui.default_font
    gui.choice_button_text_font = gui.default_font

init -1 python in mas_ui:
    import store

    music_menu_font = store.FontGroup().add( # use mplus as base
        "mod_assets/font/SourceHanSansK-Regular.otf", 0xac00, 0xd7a3 # kr
    ).add(
        "mod_assets/font/SourceHanSansSC-Regular.otf", 0x4e00, 0x9faf # s-cn
    ).add(
        "mod_assets/font/mplus-2p-regular.ttf", 0x0000, 0xffff  # jp
    )

# START: Helper methods that we use inside screens
init 25 python in mas_ui:
    # Methods for mas_check_scrollable_menu
    def check_scr_menu_return_values(buttons_data, return_all):
        """
        A method to return buttons keys and values

        IN:
            buttons_data - the screen buttons data
            return_all - whether or not we return all items

        OUT:
            dict of key-value pairs
        """
        return {item[0]: item[1]["return_value"] for item in buttons_data.iteritems() if item[1]["return_value"] == item[1]["true_value"] or return_all}

    def check_scr_menu_choose_prompt(buttons_data, selected_prompt, default_prompt):
        """
        A method to choose a prompt for the return button.

        IN:
            buttons_data - the screen buttons data
            selected_prompt - the prompt for the return button when at least one item was selected
            default_prompt - the prompt to use when no items are selected

        OUT:
            string with prompt
        """
        for data in buttons_data.itervalues():
            if data["return_value"] == data["true_value"]:
                return selected_prompt
        return default_prompt

    # Methods for twopane_scrollable_menu
    TWOPANE_MENU_MAX_FLT_ITEMS = 50
    TWOPANE_MENU_SEARCH_DBS = (
        store.mas_all_ev_db_map["EVE"].values()
        # + store.mas_all_ev_db_map["BYE"].values()
        # + store.mas_all_ev_db_map["STY"].values()
        + store.mas_all_ev_db_map["CMP"].values()
        # + store.mas_all_ev_db_map["SNG"].values()
    )
    TWOPANE_MENU_DELEGATES_CALLBACK_MAP = {
        "mas_compliment_": store.mas_compliments.compliment_delegate_callback
    }

    def twopane_menu_delegate_callback(ev_label):
        """
        A method to handle delegate logic for some of our events
        when the user skips a delegate label using search
        NOTE: the callback will be called before we push the event
        TODO: add more callbacks as needed

        IN:
            ev_label - the ev_label of the event the user's selected
        """
        for prefix in TWOPANE_MENU_DELEGATES_CALLBACK_MAP:
            if ev_label.startswith(prefix):
                TWOPANE_MENU_DELEGATES_CALLBACK_MAP[prefix]()
                return
        return

    def _twopane_menu_filter_events(ev, search_query, search_kws, only_pool, only_random, only_unseen, only_seen):
        """
        The filter for events in the twopane menu

        IN:
            ev - event object
            search_query - search query to filter by
            search_kws - search_query splitted using spaces

        OUT:
            boolean whether or not the event pass the criteria
        """
        ev_prompt = ev.prompt.lower()
        ev_label = ev.eventlabel.lower()
        ev_cat_full = " ".join(map(str, ev.category)) if ev.category else ""

        # First, basic filters so we only deal with appropriate events
        if ev_prompt == ev_label:
            return False

        if not ev.unlocked:
            return False

        if ev.anyflags(store.EV_FLAG_HFNAS):
            return False

        if not ev.checkAffection(store.mas_curr_affection):
            return False

        if only_pool and not ev.pool:
            return False

        if only_random and not ev.random:
            return False

        if only_unseen and ev.shown_count != 0:
            return False

        if only_seen and ev.shown_count == 0:
            return False

        if not search_query:
            return True

        # This is so we can interrup the loop early
        for search_kw in search_kws:
            if (
                search_kw in ev_prompt
                or search_kw in ev_label
                or (ev_cat_full and search_kw in ev_cat_full)
            ):
                return True

        return False

    def _twopane_menu_sort_events(ev, search_query, search_kws):
        """
        The sortkey for events in the twopane menu.

        IN:
            ev - event object
            search_query - search query to sort by
            search_kws - search_query splitted using spaces

        OUT:
            weight as int
        """
        ev_prompt = ev.prompt.lower()
        ev_label = ev.eventlabel.lower()
        ev_cat_full = " ".join(map(str, ev.category)) if ev.category else ""

        weight = 0
        base_increment = 2
        base_modifier = len(search_kws) + 1

        if search_query == ev_prompt or search_query == ev_label:
            weight += base_increment * base_modifier**8

        elif search_query in ev_prompt:
            if ev_prompt.startswith(search_query):
                weight += base_increment * base_modifier**7

            else:
                weight += base_increment * base_modifier**6

        elif search_query in ev_label:
            if ev_label.startswith(search_query):
                weight += base_increment * base_modifier**5

            else:
                weight += base_increment * base_modifier**4

        else:
            for search_kw in search_kws:
                if search_kw in ev_prompt:
                    weight += base_increment * base_modifier**3

                elif search_kw in ev_label:
                    weight += base_increment * base_modifier**2

                elif ev_cat_full:
                    if search_kw in ev.category:
                        weight += base_increment * base_modifier

                    elif search_kw in ev_cat_full:
                        weight += base_increment

        return weight

    def _twopane_menu_search_events(search_query):
        """
        The actual method that does filtering and searching for the twopane menu.
        NOTE: won't return more than TWOPANE_MENU_MAX_FLT_ITEMS events

        IN:
            search_query - search query to filter and sort by

        OUT:
            list of event objects or None if empty query was given
        """
        if not search_query:
            return None

        search_query = search_query.lower()

        only_pool = False
        if "#pool" in search_query:
            search_query = search_query.replace("#pool", "")
            only_pool = True

        only_random = False
        if "#random" in search_query:
            search_query = search_query.replace("#random", "")
            only_random = True

        only_unseen = False
        if "#unseen" in search_query:
            search_query = search_query.replace("#unseen", "")
            only_unseen = True

        only_seen = False
        if "#seen" in search_query:
            search_query = search_query.replace("#seen", "")
            only_seen = True

        search_query = search_query.strip()
        search_kws = search_query.split()

        flt_evs = [
            ev
            for ev in TWOPANE_MENU_SEARCH_DBS
            if _twopane_menu_filter_events(ev, search_query, search_kws, only_pool, only_random, only_unseen, only_seen)
        ]
        flt_evs.sort(key=lambda ev: _twopane_menu_sort_events(ev, search_query, search_kws), reverse=True)

        return flt_evs[0:TWOPANE_MENU_MAX_FLT_ITEMS]

    def twopane_menu_adj_ranged_callback(adj):
        """
        This is called by an adjustment of the twopane menu
        when its range is being changed (set)

        IN:
            adj - the adj object
        """
        widget = renpy.get_widget("twopane_scrollable_menu", "search_input", "screens")
        caret_relative_pos = 1.0
        if widget is not None:
            caret_pos = widget.caret_pos
            content_len = len(widget.content)

            if content_len > 0:
                caret_relative_pos = caret_pos / float(content_len)

        # This ensures that the caret is always visible (close enough) to the user
        # when they enter text
        adj.change(adj.range * caret_relative_pos)

    def twopane_menu_search_callback(search_query):
        """
        The callback the input calls when the user enters anything.
        Updates flt_evs of the twopane menu and causes RenPy to update the screen.

        IN:
            search_query - search query to filter and sort by
        """
        # Get the screen to pass events into
        scr = renpy.get_screen("twopane_scrollable_menu")
        if scr is not None:
            # Search
            scr.scope["flt_evs"] = _twopane_menu_search_events(search_query)
        # Update the screen
        renpy.restart_interaction()
