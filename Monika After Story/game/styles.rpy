#START: vars
#Whether dark mode is enabled or not
default persistent._mas_dark_mode_enabled = False

#Whether auto ui change is enabled or not
default persistent._mas_auto_mode_enabled = False

init -1 python in mas_globals:
    #None on init, True if dark ui, False otherwise
    dark_mode = None

    #The door-knock greets, if door open, need to keep a broken textbox, so this would be set False for those before the spaceroom call
    change_textbox = True

    #The colors we're using for buttons
    button_text_hover_color = None
    button_text_idle_color = None

init -200 python in mas_ui:
    dark_button_text_hover_color = "#ffcce8"
    dark_button_text_idle_color = "#e670af"

    light_button_text_hover_color = "#fa9"
    light_button_text_idle_color = "#000"

#START: Helper method(s)
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

        #Light handling
        if not mas_globals.dark_mode:
            return filestring

        #Dark handling
        else:
            #Need to isolate this for just the extension and the path so we can form a new one
            if '.' in filestring:
                extension = filestring[filestring.index('.'):]
                path = filestring[:filestring.index('.')]
                return path + "_d" + extension
            #If that fails then we just return the normal one
            return filestring

    def mas_darkMode(morning_flag=False):
        """
        Swaps all styles to dark/light mode provided on the input

        IN:
            morning_flag - if True, light mode, if False, dark mode
        """
        if not morning_flag:
            mas_globals.dark_mode = True

            #Style swaps
            style.mas_adjustable_button_text = style.mas_adjustable_button_text_dark
            style.mas_mbs_button = style.mas_mbs_button_dark
            style.mas_adjustable_button = style.mas_adjustable_button_dark
            style.slider = style.slider_dark
            style.slider_slider = style.slider_slider_dark
            style.scrollbar = style.scrollbar_dark
            style.frame = style.frame_dark
            style.confirm_frame = style.confirm_frame_dark
            style.game_menu_outer_frame = style.game_menu_outer_frame_dark
            style.edited_def = style.edited_def_dark
            style.poemgame_text = style.poemgame_text_dark
            style.namebox = style.namebox_dark
            style.main_menu_version = style.main_menu_version_dark
            style.confirm_prompt_text = style.confirm_prompt_text_dark
            style.island_button = style.island_button_dark
            style.island_button_text = style.island_button_text_dark
            style.music_menu_outer_frame = style.music_menu_outer_frame_dark
            style.button = style.button_dark
            style.main_menu_frame = style.main_menu_frame_dark
            style.window_monika = style.window_monika_dark
            style.window = style.window_dark

            #Textbox handling
            if mas_globals.change_textbox:
                style.say_window = style.window_dark

            #Global swaps
            mas_globals.button_text_hover_color = mas_ui.dark_button_text_hover_color
            mas_globals.button_text_idle_color = mas_ui.dark_button_text_idle_color

        else:
            mas_globals.dark_mode = False

            #Style swaps
            style.mas_adjustable_button_text = style.mas_adjustable_button_text_def
            style.mas_mbs_button = style.mas_mbs_button_def
            style.mas_adjustable_button = style.mas_adjustable_button_def
            style.slider = style.slider_def
            style.slider_slider = style.slider_slider_def
            style.scrollbar = style.scrollbar_def
            style.frame = style.frame_def
            style.confirm_frame = style.confirm_frame_def
            style.game_menu_outer_frame = style.game_menu_outer_frame_def
            style.edited_def = style.edited_def_def
            style.poemgame_text = style.poemgame_text_def
            style.namebox = style.namebox_def
            style.main_menu_version = style.main_menu_version_def
            style.confirm_prompt_text = style.confirm_prompt_text_def
            style.island_button = style.island_button_def
            style.island_button_text = style.island_button_text_def
            style.music_menu_outer_frame = style.music_menu_outer_frame_def
            style.button = style.button_def
            style.main_menu_frame = style.main_menu_frame_def
            style.window_monika = style.window_monika_def
            style.window = style.window_def

            #Textbox
            if mas_globals.change_textbox:
                style.say_window = style.window_def

            #Handle the global swaps
            mas_globals.button_text_hover_color = mas_ui.light_button_text_hover_color
            mas_globals.button_text_idle_color = mas_ui.light_button_text_idle_color

        #Reset the global flag
        mas_globals.change_textbox = True

#START: Settings menu helpers
init python in mas_settings:
    _persistent = renpy.game.persistent
    import store
    def _auto_mode_toggle():
        """
        Handles the toggling of fields so the menu options become mutually exclusive
        """
        #We're disablng this so we only set it false
        if _persistent._mas_auto_mode_enabled:
            _persistent._mas_auto_mode_enabled = False
            if not store.morning_flag:
                store.mas_darkMode(True)

        #But here we need to also switch the other button since this is mutually exclusive
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


#START: Extras Menu Styles
style mas_adjust_vbar_def:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"
    bar_vertical True

style mas_adjust_vbar_dark:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar_d.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"
    bar_vertical True

style mas_adjustable_button_text_def is default:
    idle_color mas_ui.light_button_text_idle_color
    hover_color mas_ui.light_button_text_hover_color
    outlines []
    kerning 0.2
    xalign 0.5
    yalign 0.5
    font gui.default_font
    size gui.text_size

style mas_adjustable_button_text_dark is default:
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    outlines []
    kerning 0.2
    xalign 0.5
    yalign 0.5
    font gui.default_font
    size gui.text_size

style mas_mbs_button_def is default:
#    width 35
#    height 35
#    tile False
    idle_background  "mod_assets/buttons/squares/square_idle.png"
    hover_background "mod_assets/buttons/squares/square_hover.png"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mas_mbs_button_dark is default:
#    width 35
#    height 35
#    tile False
    idle_background  "mod_assets/buttons/squares/square_idle_d.png"
    hover_background "mod_assets/buttons/squares/square_hover_d.png"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mas_adjustable_button_def is default:
    idle_background Frame("mod_assets/buttons/squares/square_idle.png", left=3, top=3)
    hover_background Frame("mod_assets/buttons/squares/square_hover.png", left=3, top=3)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mas_adjustable_button_dark is default:
    idle_background Frame("mod_assets/buttons/squares/square_idle_d.png", left=3, top=3)
    hover_background Frame("mod_assets/buttons/squares/square_hover_d.png", left=3, top=3)
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

#START: Hotkey Buttons Styles

style hkb_dark_vbox is vbox
style hkb_dark_button is button_dark
style hkb_dark_button_text is button_text_dark

style hkb_dark_vbox:
    spacing 0

style hkb_dark_button is default:
    properties gui.button_properties("hkb_dark_button")
    idle_background  "mod_assets/hkb_idle_background_d.png"
    hover_background "mod_assets/hkb_hover_background_d.png"
    ypadding 5

    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style hkb_dark_button_text is default:
    properties gui.button_text_properties("hkb_dark_button")
    outlines []

style hkbd_dark_vbox is vbox
style hkbd_dark_button is button_dark
style hkbd_dark_button_text is button_text_dark

style hkbd_dark_vbox:
    spacing 0

style hkbd_dark_button is default:
    properties gui.button_properties("hkb_dark_button")
    idle_background "mod_assets/hkb_disabled_background_d.png"
    hover_background "mod_assets/hkb_disabled_background_d.png"

style hkbd_dark_button_text is default:
#    properties gui.button_text_properties("hkb_button")
    font gui.default_font
    size gui.text_size
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    kerning 0.2
    outlines []

style hkb_dark_text is default:
    xalign 0.5
    size gui.text_size
    font gui.default_font
    color mas_ui.dark_button_text_idle_color
    kerning 0.2
    outlines []


#START: screens styles
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
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]

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
    font "gui/font/Halogen.ttf"
    outlines []

style choice_dark_vbox is vbox
style choice_dark_button is button_dark
style choice_dark_button_text is button_text_dark

style choice_dark_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing gui.choice_spacing

style choice_dark_button is default:
    properties gui.button_properties("choice_dark_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text_dark is button_text_dark

style choice_button_text_dark is default:
    properties gui.button_text_properties("choice_dark_button")
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    outlines []

style choice_dark_button_text is button_text_dark

style choice_dark_button_text is default:
    properties gui.button_text_properties("choice_dark_button")
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color
    outlines []

style talk_choice_dark_vbox is choice_dark_vbox:
    xcenter 960

style talk_choice_dark_button is choice_dark_button
style talk_choice_dark_button_text is choice_dark_button_text

style scrollable_menu_dark_button is choice_dark_button:
    properties gui.button_properties("scrollable_menu_dark_button")

style scrollable_menu_dark_button_text is choice_dark_button_text:
    properties gui.button_text_properties("scrollable_menu_dark_button")
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color

style scrollable_menu_dark_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing 5

style scrollable_menu_dark_new_button is scrollable_menu_dark_button

style scrollable_menu_dark_new_button_text is scrollable_menu_dark_button_text:
    italic True

style scrollable_menu_dark_special_button is scrollable_menu_dark_button

style scrollable_menu_dark_special_button_text is scrollable_menu_dark_button_text:
    bold True

style scrollable_menu_dark_crazy_button is scrollable_menu_dark_button

style scrollable_menu_dark_crazy_button_text is scrollable_menu_dark_button_text:
    italic True
    bold True

style twopane_scrollable_menu_dark_button is choice_dark_button:
    properties gui.button_properties("twopane_scrollable_menu_dark_button")

style twopane_scrollable_menu_dark_button_text is choice_dark_button_text:
    properties gui.button_text_properties("twopane_scrollable_menu_dark_button")
    idle_color mas_ui.dark_button_text_idle_color
    hover_color mas_ui.dark_button_text_hover_color

style twopane_scrollable_menu_dark_special_button is twopane_scrollable_menu_dark_button


style twopane_scrollable_menu_dark_special_button_text is twopane_scrollable_menu_dark_button_text:
    bold True


style twopane_scrollable_menu_dark_new_button is twopane_scrollable_menu_dark_button


style twopane_scrollable_menu_dark_new_button_text is twopane_scrollable_menu_dark_button_text:
    italic True

style twopane_scrollable_menu_dark_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5

    spacing 5

style button_def:
    properties gui.button_properties("button")

style button_text_def is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5

style button_def_text is gui_text:
    properties gui.button_text_properties("button")
    yalign 0.5

style button_dark:
    properties gui.button_properties("button_dark")

style button_text_dark is gui_text:
    properties gui.button_text_properties("button_dark")
    yalign 0.5

style button_dark_text is gui_text:
    properties gui.button_text_properties("button_dark")
    yalign 0.5

style main_menu_frame_def is empty

style main_menu_frame_def:
    xsize 310
    yfill True

    background "menu_nav"

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

style slider_slider_def is gui_slider
style slider_slider_def:
    xsize 350

style slider_slider_dark is gui_slider_dark
style slider_slider_dark:
    xsize 350

style scrollbar_def:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)
    unscrollable "hide"
    bar_invert True

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

style frame_def:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style frame_dark:
    padding gui.frame_borders.padding
    background Frame("gui/frame_d.png", gui.frame_borders, tile=gui.frame_tile)

style confirm_frame_def:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_frame_dark:
    background Frame([ "gui/confirm_frame.png", "gui/frame_d.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style game_menu_outer_frame_def:
    bottom_padding 30
    top_padding 120

    background "gui/overlay/game_menu.png"

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

style edited_def is default:
    font "gui/font/VerilySerifMono.otf"
    kerning 8
    outlines [(10, "#000", 0, 0)]
    xpos gui.text_xpos
    xanchor gui.text_xalign
    xsize gui.text_width
    ypos gui.text_ypos
    text_align gui.text_xalign
    layout ("subtitle" if gui.text_xalign else "tex")

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

style poemgame_text_def:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#000"
    outlines []

    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

style poemgame_text_dark:
    yalign 0.5
    font "gui/font/Halogen.ttf"
    size 30
    color "#e670af"
    outlines []

    hover_xoffset -3
    hover_outlines [(3, "#fef", 0, 0), (2, "#fcf", 0, 0), (1, "#faf", 0, 0)]

style namebox_def is default

style namebox_def:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style namebox_dark is default

style namebox_dark:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox_d.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style window_def is default

style window_def:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style window_dark is default

style window_dark:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox_d.png", xalign=0.5, yalign=1.0)

style navigation_button_text_def is gui_button_text

style navigation_button_text_def:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]

style navigation_button_text_dark is gui_button_text_dark

style navigation_button_text_dark:
    properties gui.button_text_properties("navigation_button")
    font "gui/font/RifficFree-Bold.ttf"
    color mas_ui.dark_button_text_idle_color
    outlines []
    hover_outlines [(3, "#ffcce8", 0, 0)]
    insensitive_outlines [(3, "#ffcce8", 0, 0)]

style main_menu_version_def is main_menu_text:
    color "#000000"
    size 16
    outlines []

style main_menu_version_dark is main_menu_text:
    color mas_ui.dark_button_text_idle_color
    size 16
    outlines []

style confirm_prompt_text_def is gui_prompt_text

style confirm_prompt_text_def:
    color "#000"
    outlines []
    text_align 0.5
    layout "subtitle"

style confirm_prompt_text_dark is gui_prompt_text

style confirm_prompt_text_dark:
    color "#e670af"
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


#START: islands event styles
style island_button_def is button

style island_button_def is default:
    properties gui.button_properties("island_button")
    idle_background  "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_dark is button_dark

style island_button_dark is default:
    properties gui.button_properties("island_button")
    idle_background  "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_text_def is button_text

style island_button_text_def is default:
    properties gui.button_text_properties("island_button")
    idle_background  "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    outlines []

style island_button_def_text is default:
    properties gui.button_text_properties("island_button")
    idle_background  "mod_assets/island_idle_background.png"
    hover_background "mod_assets/island_hover_background.png"
    outlines []

style island_button_text_dark is button_text_dark

style island_button_text_dark is default:
    properties gui.button_text_properties("island_button_dark")
    idle_background  "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    outlines []

style island_button_dark_text is default:
    properties gui.button_text_properties("island_button_dark")
    idle_background  "mod_assets/island_idle_background_d.png"
    hover_background "mod_assets/island_hover_background_d.png"
    outlines []


#START: quick menu styles

style quick_dark_button:
    properties gui.button_properties("quick_dark_button")
    activate_sound gui.activate_sound

#style quick_dark_button_text is button_text_dark
style quick_dark_button_selected_text
style quick_dark_button_text:
    properties gui.button_text_properties("quick_dark_button")
    outlines []

#START: music selector styles
style music_menu_outer_frame_def is game_menu_outer_frame_def

style music_menu_outer_frame_def:
    background "mod_assets/music_menu.png"

style music_menu_outer_frame_dark is game_menu_outer_frame_dark

style music_menu_outer_frame_dark:
    background "mod_assets/music_menu_d.png"


#START: image definitions
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


#START: gui definitions
define gui.button_def_width = None
define gui.button_def_height = 36
define gui.button_def_borders = Borders(4, 4, 4, 4)
define gui.button_def_tile = False
define gui.button_def_text_font = gui.interface_font
define gui.button_def_text_size = gui.interface_text_size
define gui.button_def_text_idle_color = gui.idle_color
define gui.button_def_text_hover_color = gui.hover_color
define gui.button_def_text_selected_color = gui.selected_color
define gui.button_def_text_insensitive_color = gui.insensitive_color
define gui.button_def_text_xalign = 0.0

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

define gui.scrollable_menu_button_dark_width = 560
define gui.scrollable_menu_button_dark_height = None
define gui.scrollable_menu_button_dark_tile = False
define gui.scrollable_menu_button_dark_borders = Borders(25, 5, 25, 5)

define gui.scrollable_menu_button_dark_text_font = gui.default_font
define gui.scrollable_menu_button_dark_text_size = gui.text_size
define gui.scrollable_menu_button_dark_text_xalign = 0.0
define gui.scrollable_menu_button_dark_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.scrollable_menu_button_dark_text_hover_color = mas_ui.dark_button_text_hover_color

define gui.hkb_dark_button_width = 120
define gui.hkb_dark_button_height = None
define gui.hkb_dark_button_tile = False
define gui.hkb_dark_button_text_font = gui.default_font
define gui.hkb_dark_button_text_size = gui.text_size
define gui.hkb_dark_button_text_xalign = 0.5
define gui.hkb_dark_button_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.hkb_dark_button_text_hover_color = mas_ui.dark_button_text_hover_color
define gui.hkb_dark_button_text_kerning = 0.2

define gui.choice_dark_button_width = 420
define gui.choice_dark_button_height = None
define gui.choice_dark_button_tile = False
define gui.choice_dark_button_borders = Borders(100, 5, 100, 5)
define gui.choice_dark_button_text_font = gui.default_font
define gui.choice_dark_button_text_size = gui.text_size
define gui.choice_dark_button_text_xalign = 0.5
define gui.choice_dark_button_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.choice_dark_button_text_hover_color = mas_ui.dark_button_text_hover_color

define gui.scrollable_menu_dark_button_width = 560
define gui.scrollable_menu_dark_button_height = None
define gui.scrollable_menu_dark_button_tile = False
define gui.scrollable_menu_dark_button_borders = Borders(25, 5, 25, 5)
define gui.scrollable_menu_dark_button_text_font = gui.default_font
define gui.scrollable_menu_dark_button_text_size = gui.text_size
define gui.scrollable_menu_dark_button_text_xalign = 0.0
define gui.scrollable_menu_dark_button_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.scrollable_menu_dark_button_text_hover_color = mas_ui.dark_button_text_hover_color

define gui.twopane_scrollable_menu_dark_button_width = 250
define gui.twopane_scrollable_menu_dark_button_height = None
define gui.twopane_scrollable_menu_dark_button_tile = False
define gui.twopane_scrollable_menu_dark_button_borders = Borders(25, 5, 25, 5)
define gui.twopane_scrollable_menu_dark_button_text_font = gui.default_font
define gui.twopane_scrollable_menu_dark_button_text_size = gui.text_size
define gui.twopane_scrollable_menu_dark_button_text_xalign = 0.0
define gui.twopane_scrollable_menu_dark_button_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.twopane_scrollable_menu_dark_button_text_hover_color = mas_ui.dark_button_text_hover_color

define gui.island_button_dark_height = None
define gui.island_button_dark_width = 205
define gui.island_button_dark_tile = False
define gui.island_button_dark_text_font = gui.default_font
define gui.island_button_dark_text_size = gui.text_size
define gui.island_button_dark_text_xalign = 0.5
define gui.island_button_dark_text_idle_color = mas_ui.dark_button_text_idle_color
define gui.island_button_dark_text_hover_color = mas_ui.dark_button_text_hover_color
define gui.island_button_dark_text_kerning = 0.2

define gui.quick_dark_button_text_height = None
define gui.quick_dark_button_text_width = 205
define gui.quick_dark_button_text_tile = False
define gui.quick_dark_button_text_font = gui.default_font
define gui.quick_dark_button_text_size = 14
define gui.quick_dark_button_text_xalign = 0.5
define gui.quick_dark_button_text_yalign = 0.995
define gui.quick_dark_button_text_idle_color = "#F2A4F1"
define gui.quick_dark_button_text_selected_color = "#DFDFDF"
define gui.quick_dark_button_text_hover_color = "#FFDEFE"
define gui.quick_dark_button_text_kerning = 0.2
