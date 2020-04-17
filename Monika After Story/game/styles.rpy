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

    # checkbox
    cbx_style_prefix = "check"

    # game menu 
    gm_label_style = "game_menu_label"

    # music menu (music selector)
    mms_style_prefix = "music_menu"
    mms_button_prev_style = "music_menu_prev_button"
    mms_button_return_style = "music_menu_return_button"
    mms_frame_content_style = "music_menu_content_frame"
    mms_frame_navigation_style = "music_menu_navigation_frame"
    mms_frame_outer_style = "music_menu_outer_frame"

    # quick menu
    qm_style_prefix = "quick"

    # radio button
    rab_style_prefix = "radio"

    # return button
    rb_button_style = "return_button"

    # slider
    sld_style_prefix = "slider"

    # scrollable menu
    sm_style_prefix = "scrollable_menu"
    sm_button_crazy_style = "scrollable_menu_crazy_button"
    sm_button_new_style = "scrollable_menu_new_button"
    sm_button_special_style = "scrollable_menu_special_button"

    # selector menu
    st_cbx_style = "outfit_check_button"

    # two pane scrollable
    tpsm_style_prefix = "twopane_scrollable_menu"
    tpsm_button_new_style = "twopane_scrollable_menu_new_button"
    tpsm_button_special_style = "twopane_scrollable_menu_special_button"

    # floating islands

    fli_style_prefix = "island"

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

    def mas_darkMode(morning_flag=False):
        """
        Swaps all styles to dark/light mode provided on the input

        IN:
            morning_flag - if True, light mode, if False, dark mode
        """
        if not morning_flag:
            mas_globals.dark_mode = True

            # Global swaps
            mas_globals.button_text_hover_color = mas_ui.dark_button_text_hover_color
            mas_globals.button_text_idle_color = mas_ui.dark_button_text_idle_color
            mas_globals.button_text_insensitive_color = mas_ui.dark_button_text_insensitive_color

            # ui swaps
            mas_ui.cbx_style_prefix = "check_dark"
            mas_ui.gm_label_style = "game_menu_label_dark"
            mas_ui.mms_style_prefix = "music_menu_dark"
            mas_ui.mms_button_prev_style = "music_menu_dark_prev_button"
            mas_ui.mms_button_return_style = "music_menu_dark_return_button"
            mas_ui.mms_frame_content_style = "music_menu_dark_content_frame"
            mas_ui.mms_frame_navigation_style = "music_menu_dark_navigation_frame"
            mas_ui.mms_frame_outer_style = "music_menu_dark_outer_frame"
            mas_ui.qm_style_prefix = "quick_dark"
            mas_ui.rab_style_prefix = "radio_dark"
            mas_ui.rb_button_style = "return_dark_button"
            mas_ui.sld_style_prefix = "slider_dark"
            mas_ui.sm_style_prefix = "scrollable_menu_dark"
            mas_ui.sm_button_crazy_style = "scrollable_menu_dark_crazy_button"
            mas_ui.sm_button_new_style = "scrollable_menu_dark_new_button"
            mas_ui.sm_button_special_style = "scrollable_menu_dark_special_button"
            mas_ui.st_cbx_style = "outfit_check_dark_button"
            mas_ui.tpsm_style_prefix = "twopane_scrollable_menu_dark"
            mas_ui.tpsm_button_new_style = "twopane_scrollable_menu_dark_new_button"
            mas_ui.tpsm_button_special_style = "twopane_scrollable_menu_dark_special_button"
            mas_ui.fli_style_prefix = "island_dark"

        else:
            mas_globals.dark_mode = False

            # Handle the global swaps
            mas_globals.button_text_hover_color = mas_ui.light_button_text_hover_color
            mas_globals.button_text_idle_color = mas_ui.light_button_text_idle_color
            mas_globals.button_text_insensitive_color = mas_ui.light_button_text_insensitive_color

            # ui swaps
            mas_ui.cbx_style_prefix = "check"
            mas_ui.gm_label_style = "game_menu_label"
            mas_ui.mms_style_prefix = "music_menu"
            mas_ui.mms_button_prev_style = "music_menu_prev_button"
            mas_ui.mms_button_return_style = "music_menu_return_button"
            mas_ui.mms_frame_content_style = "music_menu_content_frame"
            mas_ui.mms_frame_navigation_style = "music_menu_navigation_frame"
            mas_ui.mms_frame_outer_style = "music_menu_outer_frame"
            mas_ui.qm_style_prefix = "quick"
            mas_ui.rab_style_prefix = "radio"
            mas_ui.rb_button_style = "return_button"
            mas_ui.sld_style_prefix = "slider"
            mas_ui.sm_style_prefix = "scrollable_menu"
            mas_ui.sm_button_crazy_style = "scrollable_menu_crazy_button"
            mas_ui.sm_button_new_style = "scrollable_menu_new_button"
            mas_ui.sm_button_special_style = "scrollable_menu_special_button"
            mas_ui.st_cbx_style = "outfit_check_button"
            mas_ui.tpsm_style_prefix = "twopane_scrollable_menu"
            mas_ui.tpsm_button_new_style = "twopane_scrollable_menu_new_button"
            mas_ui.tpsm_button_special_style = "twopane_scrollable_menu_special_button"
            mas_ui.fli_style_prefix = "island"

        # FIXME: it will be done automagically later (requires consistent naming between styles)
        mas_swapStyle("button"                    , "button_dark"                    , morning_flag)
        mas_swapStyle("button_text"               , "button_dark_text"               , morning_flag)
        mas_swapStyle("choice_button"             , "choice_dark_button"             , morning_flag)
        mas_swapStyle("choice_button_text"        , "choice_dark_button_text"        , morning_flag)
        mas_swapStyle("confirm_frame"             , "confirm_frame_dark"             , morning_flag)
        mas_swapStyle("confirm_prompt_text"       , "confirm_prompt_text_dark"       , morning_flag)
        mas_swapStyle("hkb_button"                , "hkb_dark_button"                , morning_flag)
        mas_swapStyle("hkb_button_text"           , "hkb_dark_button_text"           , morning_flag)
        mas_swapStyle("edited"                    , "edited_dark"                    , morning_flag)
        mas_swapStyle("frame"                     , "frame_dark"                     , morning_flag)
        mas_swapStyle("game_menu_outer_frame"     , "game_menu_outer_frame_dark"     , morning_flag)
        mas_swapStyle("main_menu_frame"           , "main_menu_frame_dark"           , morning_flag)
        mas_swapStyle("main_menu_version"         , "main_menu_version_dark"         , morning_flag)
        mas_swapStyle("mas_adjustable_button"     , "mas_adjustable_button_dark"     , morning_flag)
        mas_swapStyle("mas_adjustable_button_text", "mas_adjustable_button_text_dark", morning_flag)
        mas_swapStyle("mas_adjust_vbar"           , "mas_adjust_vbar_dark"           , morning_flag)
        mas_swapStyle("mas_mbs_button"            , "mas_mbs_button_dark"            , morning_flag)
        mas_swapStyle("mas_mbs_button_text"       , "mas_mbs_button_text_dark"       , morning_flag)
        mas_swapStyle("mas_extra_menu_frame"      , "mas_extra_menu_frame_dark"      , morning_flag)
        mas_swapStyle("mute_all_button"           , "mute_all_button_dark"           , morning_flag)
        mas_swapStyle("mute_all_button_text"      , "mute_all_button_dark_text"      , morning_flag)
        mas_swapStyle("namebox"                   , "namebox_dark"                   , morning_flag)
        mas_swapStyle("navigation_button_text"    , "navigation_button_text_dark"    , morning_flag)
        mas_swapStyle("page_label"                , "page_label_dark"                , morning_flag)
        mas_swapStyle("page_label_text"           , "page_label_dark_text"           , morning_flag)
        mas_swapStyle("poemgame_text"             , "poemgame_text_dark"             , morning_flag)
        mas_swapStyle("pref_label"                , "pref_dark_label"                , morning_flag)
        mas_swapStyle("pref_label_text"           , "pref_dark_label_text"           , morning_flag)
        mas_swapStyle("say_label"                 , "say_label_dark"                 , morning_flag)
        mas_swapStyle("scrollbar"                 , "scrollbar_dark"                 , morning_flag)
        mas_swapStyle("slot_button"               , "slot_button_dark"               , morning_flag)
        mas_swapStyle("slot_button_text"          , "slot_button_dark_text"          , morning_flag)
        mas_swapStyle("talk_choice_button"        , "talk_choice_dark_button"        , morning_flag)
        mas_swapStyle("talk_choice_button_text"   , "talk_choice_dark_button_text"   , morning_flag)
        mas_swapStyle("window"                    , "window_dark"                    , morning_flag)
        mas_swapStyle("window_monika"             , "window_monika_dark"             , morning_flag)

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


# START: screens styles
style window_monika_def is window:
    background Image("gui/textbox_monika.png", xalign=0.5, yalign=1.0)

style window_monika_dark is window:
    background Image("gui/textbox_monika_d.png", xalign=0.5, yalign=1.0)

style navigation_dark_button is gui_button

style navigation_dark_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style navigation_dark_button_text is gui_button_text_dark

style navigation_dark_button_text:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#FFD9E8"
    outlines [(4, "#DE367E", 0, 0), (2, "#DE367E", 2, 2)]
    hover_outlines [(4, "#FF80B7", 0, 0), (2, "#FF80B7", 2, 2)]
    insensitive_outlines [(4, "#FFB2D4", 0, 0), (2, "#FFB2D4", 2, 2)]

style pref_dark_label is gui_label
style pref_dark_label_text is gui_label_text

style pref_dark_label:
    top_margin gui.pref_spacing
    bottom_margin 2

style pref_dark_label_text:
    font "gui/font/RifficFree-Bold.ttf"
    size 24
    color "#FFD9E8"
    outlines [(3, "#DE367E", 0, 0), (1, "#DE367E", 1, 1)]
    yalign 1.0

style check_dark_label is pref_label
style check_dark_label_text is pref_label_text
style check_dark_button is gui_button_dark
style check_dark_button_text is gui_button_text_dark
style check_dark_vbox is pref_vbox

style check_dark_vbox:
    spacing gui.pref_button_spacing

style check_dark_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground_d.png"

style check_dark_button_text:
    properties gui.button_text_properties("check_dark_button")
    color "#8C8C8C" 
    hover_color "#FF80B7"
    selected_color "#DE367E"
    font "gui/font/Halogen.ttf"
    outlines []

style outfit_check_dark_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground_d.png"

style outfit_check_dark_button_text:
    properties gui.button_text_properties("outfit_check_button")
    font "gui/font/Halogen.ttf"
    color "#BFBFBF"
    selected_color "#FFEEEB"
    hover_color "#FFAA99"
    outlines []

style button_dark:
    properties gui.button_properties("button_dark")

style button_dark_text is gui_text:
    properties gui.button_text_properties("button_dark")
    yalign 0.5

style main_menu_frame_dark is empty

style main_menu_frame_dark:
    xsize 310
    yfill True

    background "menu_nav"

style slider_def:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

style slider_dark:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar_d.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

style slider_dark_button_text:
    properties gui.button_text_properties("slider_button")

style slider_dark_vbox:
    xsize 450

style slider_dark_slider is gui_slider_dark
style slider_dark_slider:
    xsize 350

style slider_dark_label is pref_label
style slider_dark_label_text is pref_label_text
style slider_dark_slider is gui_slider_dark
style slider_dark_button is gui_button
style slider_dark_button_text is gui_button_text
style slider_dark_pref_vbox is pref_vbox

style scrollbar_dark:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar_d.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True

style vscrollbar_def:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_vertical True
    bar_invert True

style vscrollbar_dark:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar_d.png", tile=False)
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    unscrollable "hide"
    bar_vertical True
    bar_invert True

style frame_dark:
    padding gui.frame_borders.padding
    background Frame("gui/frame_d.png", gui.frame_borders, tile=gui.frame_tile)

style confirm_frame_dark:
    background Frame([ "gui/confirm_frame.png", "gui/frame_d.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style game_menu_outer_frame_dark:
    bottom_padding 30
    top_padding 120

    background "gui/overlay/game_menu_d.png"

style default_def:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

style default_dark:
    font gui.default_font
    size gui.text_size
    color gui.text_color
    outlines []
    line_overlap_split 1
    line_spacing 1

style edited_dark is default:
    font "gui/font/VerilySerifMono.otf"
    kerning 8
    outlines []
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

style poemgame_text_dark:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []

    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

style namebox_dark is default

style namebox_dark:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox_d.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label_dark is default

style say_label_dark:
    color "#FFD9E8"
    font gui.name_font
    size gui.name_text_size
    xalign gui.name_xalign
    yalign 0.5
    outlines [(3, "#DE367E", 0, 0), (1, "#DE367E", 1, 1)]

style window_dark is default

style window_dark:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox_d.png", xalign=0.5, yalign=1.0)

style navigation_button_text_dark is gui_button_text_dark

style navigation_button_text_dark:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#FFD9E8"
    outlines [(4, "#DE367E", 0, 0), (2, "#DE367E", 2, 2)]
    hover_outlines [(4, "#FF80B7", 0, 0), (2, "#FF80B7", 2, 2)]
    insensitive_outlines [(4, "#FFB2D4", 0, 0), (2, "#FFB2D4", 2, 2)]

style main_menu_version_dark is main_menu_text:
    color mas_ui.dark_button_text_idle_color
    size 16
    outlines []

style confirm_prompt_text_dark is gui_prompt_text

style confirm_prompt_text_dark:
    color "#FD5BA2"
    outlines []
    text_align 0.5
    layout "subtitle"

style radio_dark_label is pref_label
style radio_dark_label_text is pref_label_text
style radio_dark_button is gui_button_dark
style radio_dark_button_text is gui_button_text_dark
style radio_dark_vbox is pref_vbox

style radio_dark_vbox:
    spacing gui.pref_button_spacing

style radio_dark_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/check_[prefix_]foreground_d.png"

style radio_dark_button_text:
    properties gui.button_text_properties("radio_dark_button")
    font "gui/font/Halogen.ttf"
    color "#8C8C8C" 
    hover_color "#FF80B7"
    selected_color "#DE367E"
    outlines []

style return_dark_button is navigation_button
style return_dark_button_text is navigation_dark_button_text

style return_dark_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin -40

style game_menu_label_def is gui_label
style game_menu_label_def_text is gui_label_text

style game_menu_label_def:
    xpos 50
    ysize 120

style game_menu_label_def_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#fff"
    outlines [(6, "#b59", 0, 0), (3, "#b59", 2, 2)]
    yalign 0.5

style game_menu_label_dark is gui_label
style game_menu_label_dark_text is gui_label_text

style game_menu_label_dark:
    xpos 50
    ysize 120

style game_menu_label_dark_text:
    font "gui/font/RifficFree-Bold.ttf"
    size gui.title_text_size
    color "#FFD9E8"
    outlines [(6, "#DE367E", 0, 0), (3, "#DE367E", 2, 2)]
    yalign 0.5



# START: islands event styles

style island_dark_button is button_dark

style island_dark_button is default:
    properties gui.button_properties("island_button")
    idle_background  "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_dark_button_text is button_text_dark

style island_dark_button_text is default:
    properties gui.button_text_properties("island_dark_button")
    idle_background  "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    outlines []

style page_label_dark is gui_label
style page_label_dark_text is gui_label_text

style page_label_dark:
    xpadding 50
    ypadding 3

style page_label_dark_text:
    color "#FFD9E8"
    outlines []
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style slot_button_dark is gui_button
style slot_button_dark_text is gui_button_text

style slot_button_dark:
    properties gui.button_properties("slot_button")

style slot_button_dark_text:
    properties gui.button_text_properties("slot_button")
    color "#8C8C8C"
    outlines []

style mute_all_button_dark is check_dark_button
style mute_all_button_dark_text is check_dark_button_text

# START: quick menu styles

style quick_dark_button:
    properties gui.button_properties("quick_dark_button")
    activate_sound gui.activate_sound

# style quick_dark_button_text is button_text_dark
style quick_dark_button_selected_text
style quick_dark_button_text:
    properties gui.button_text_properties("quick_dark_button")
    outlines []

# START: music selector styles

style music_menu_dark_label is game_menu_label_dark
style music_menu_dark_label_text is game_menu_label_dark_text

style music_menu_dark_outer_frame is game_menu_outer_frame_dark

style music_menu_dark_outer_frame:
    background "mod_assets/music_menu_d.png"

style music_menu_dark_navigation_frame is game_menu_navigation_frame
style music_menu_dark_content_frame is game_menu_content_frame

style music_menu_dark_button_text is navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "mod_assets/font/mplus-2p-regular.ttf"
    color "#FFD9E8"
    outlines [(4, "#DE367E", 0, 0), (2, "#DE367E", 2, 2)]
    hover_outlines [(4, "#FF80B7", 0, 0), (2, "#FF80B7", 2, 2)]
    insensitive_outlines [(4, "#FFB2D4", 0, 0), (2, "#FFB2D4", 2, 2)]

style music_menu_dark_return_button is return_button:
    xminimum 0
    xmaximum 200
    xfill False

style music_menu_dark_prev_button is return_button:
    xminimum 0
    xmaximum 135
    xfill False

style music_menu_dark_return_button_text is navigation_dark_button_text
style music_menu_dark_prev_button_text is navigation_dark_button_text:
    min_width 135
    text_align 1.0

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


# START: gui definitions
define gui.button_width = None
define gui.button_height = 36
define gui.button_borders = Borders(4, 4, 4, 4)
define gui.button_tile = False
define gui.button_text_font = gui.interface_font
define gui.button_text_size = gui.interface_text_size
define gui.button_text_idle_color = gui.idle_color
define gui.button_text_hover_color = gui.hover_color
define gui.button_text_selected_color = gui.selected_color
define gui.button_text_insensitive_color = gui.insensitive_color
define gui.button_text_xalign = 0.0

define gui.button_dark_width = None
define gui.button_dark_height = 36
define gui.button_dark_borders = Borders(4, 4, 4, 4)
define gui.button_dark_tile = False
define gui.button_dark_text_font = gui.interface_font
define gui.button_dark_text_size = gui.interface_text_size
define gui.button_dark_text_idle_color = gui.idle_color
define gui.button_dark_text_hover_color = gui.hover_color
define gui.button_dark_text_selected_color = gui.selected_color
define gui.button_dark_text_insensitive_color = gui.insensitive_color
define gui.button_dark_text_xalign = 0.0

define gui.check_button_dark_borders = Borders(28, 4, 4, 4)
define gui.check_button_def_borders = Borders(28, 4, 4, 4)

define gui.island_dark_button_height = None
define gui.island_dark_button_width = 205
define gui.island_dark_button_tile = False
define gui.island_dark_button_text_font = gui.default_font
define gui.island_dark_button_text_size = gui.text_size
define gui.island_dark_button_text_xalign = 0.5
define gui.island_dark_button_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.island_dark_button_text_hover_color = mas_ui.dark_button_text_hover_color
define gui.island_dark_button_text_kerning = 0.2

define gui.quick_dark_button_text_height = None
define gui.quick_dark_button_text_width = 205
define gui.quick_dark_button_text_tile = False
define gui.quick_dark_button_text_font = gui.default_font
define gui.quick_dark_button_text_size = 14
define gui.quick_dark_button_text_xalign = 0.5
define gui.quick_dark_button_text_yalign = 0.995
define gui.quick_dark_button_text_idle_color = "#FFAA99"
define gui.quick_dark_button_text_selected_color = "#FFEEEB"
define gui.quick_dark_button_text_hover_color = "#FFD4CC"
define gui.quick_dark_button_text_kerning = 0.2
