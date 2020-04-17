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

    # hotkey buttons
    HKB_DISABLED_BG = "mod_assets/hkb_disabled_background.png"

    # selector
    SEL_SB_FRAME = "mod_assets/frames/black70_pinkborder100_5px.png"

init -200 python in mas_ui:

    style_stash = {}

    dark_button_text_hover_color = "#FFABD8"
    dark_button_text_idle_color = "#FD5BA2"
    dark_button_text_insensitive_color = "#8C8C8C"

    light_button_text_hover_color = "#fa9"
    light_button_text_idle_color = "#000"
    light_button_text_insensitive_color = "#8C8C8C"

    # ---- files ----

    # confirm screen
    cm_bg = CNF_BG

    # selector
    sel_sb_frame = SEL_SB_FRAME

    SCROLLABLE_MENU_X = 680
    SCROLLABLE_MENU_Y = 40
    SCROLLABLE_MENU_W = 560
    SCROLLABLE_MENU_H = 640
    SCROLLABLE_MENU_TXT_H = 500
    SCROLLABLE_MENU_XALIGN = -0.05

    SCROLLABLE_MENU_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_H)
    SCROLLABLE_MENU_TXT_AREA = (SCROLLABLE_MENU_X, SCROLLABLE_MENU_Y, SCROLLABLE_MENU_W, SCROLLABLE_MENU_TXT_H)

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

    def mas_swapStyle(base_name, dark_name, morning_flag):
        """
        Swaps the single style between default and dark variants.

        IN:
            morning_flag - Light/dark mode switch
        """
        if not base_name in mas_ui.style_stash:
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
        suffix_len = len(mas_ui.dark_suffix)
        return len(style_name) > suffix_len and style_name[-suffix_len:] == mas_ui.dark_suffix

    # FIXME: temporary
    def mas_isTextDarkStyle(style_name):
        """
        Check if selected style is a text_dark style.
        """
        complete_suffix = "_text" + mas_ui.dark_suffix
        suffix_len = len(complete_suffix)
        return len(style_name) > suffix_len and style_name[-suffix_len:] == complete_suffix

    def mas_darkMode(morning_flag=False):
        """
        Swaps all styles to dark/light mode provided on the input

        IN:
            morning_flag - if True, light mode, if False, dark mode
        """
        # Create aliases
        # FIXME: should be done on startup
        new_aliases = {}

        for style_tuple, style_ptr in renpy.style.styles.items():
            style_name = style_tuple[0]
            if mas_isTextDarkStyle(style_name):
                complete_suffix = "_text" + mas_ui.dark_suffix
                suffix_len = len(complete_suffix)
                alias_name = style_name[:-suffix_len] + mas_ui.dark_suffix + "_text"
                if not style.exists(alias_name):
                    new_aliases[alias_name] = style_ptr

        for alias_name, alias_style_ptr in new_aliases.items():
            setattr(style, alias_name, alias_style_ptr)

        # Automagically switch every style which has a dark variant
        for style_tuple in renpy.style.styles:
            style_name = style_tuple[0]
            if not mas_isDarkStyle(style_name) and mas_hasDarkStyle(style_name):
                dark_style_name = style_name + mas_ui.dark_suffix
                mas_swapStyle(style_name, dark_style_name, morning_flag)

        if not morning_flag:
            # Handle the global swaps
            mas_globals.dark_mode = True

            mas_globals.button_text_hover_color = mas_ui.dark_button_text_hover_color
            mas_globals.button_text_idle_color = mas_ui.dark_button_text_idle_color
            mas_globals.button_text_insensitive_color = mas_ui.dark_button_text_insensitive_color

            # Textbox
            if mas_globals.change_textbox:
                style.say_window = style.window_dark

        else:
            # Handle the global swaps
            mas_globals.dark_mode = False

            mas_globals.button_text_hover_color = mas_ui.light_button_text_hover_color
            mas_globals.button_text_idle_color = mas_ui.light_button_text_idle_color
            mas_globals.button_text_insensitive_color = mas_ui.light_button_text_insensitive_color

            # Textbox
            if mas_globals.change_textbox:
                style.say_window = style.window

        # timefile changes
        mas_ui.cm_bg = mas_getTimeFile(mas_ui.CNF_BG)
        mas_ui.sel_sb_frame = mas_getTimeFile(mas_ui.SEL_SB_FRAME)
    
        # Reset the global flag
        mas_globals.change_textbox = True

        style.rebuild()

# START: Settings menu helpers
init python in mas_settings:
    _persistent = renpy.game.persistent
    import store
    def _auto_mode_toggle():
        """
        Handles the toggling of fields so the menu options become mutually exclusive
        """
        # We're disablng this so we only set it false
        if _persistent._mas_auto_mode_enabled:
            _persistent._mas_auto_mode_enabled = False
            if not store.morning_flag:
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
        renpy.restart_interaction()


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
    align (0.5, 0.5)
    outlines []

style generic_button_text_light is generic_button_text_base:
    idle_color mas_ui.light_button_text_idle_color
    hover_color mas_ui.light_button_text_hover_color
    insensitive_color mas_ui.light_button_text_insensitive_color

style generic_button_text_dark is generic_button_text_base:
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    insensitive_color mas_ui.dark_button_text_insensitive_color


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
