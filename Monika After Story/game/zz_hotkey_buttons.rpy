# Module that handles hotkey button screen
#

init python:

    # function to hide buttons
    def HKBHideButtons():
        #
        # Hides the hkb buttons
        #
        config.overlay_screens.remove("hkb_overlay")
        renpy.hide_screen("hkb_overlay")

    # function to show buttons
    def HKBShowButtons():
        #
        # Shows the hkb buttons
        #
        config.overlay_screens.append("hkb_overlay")

        # function to hide buttons
    def MovieOverlayHideButtons():
        #
        # Hides the movie buttons
        #
        if "movie_overlay" in config.overlay_screens:
            config.overlay_screens.remove("movie_overlay")
            renpy.hide_screen("movie_overlay")

    # function to show buttons
    def MovieOverlayShowButtons():
        #
        # Shows the movie buttons
        #
        config.overlay_screens.append("movie_overlay")
        

init -1 python in hkb_button:

    # new property to disable buttons
    # set to False to disable buttons
    enabled = True
    movie_buttons_enabled = False


# HOTKEY BUTTON SCREEN ========================================================
# Literally just hotkey buttons

# properties for these new buttons
# again copied from choice
define gui.hkb_button_width = 120
define gui.hkb_button_height = None
define gui.hkb_button_tile = False
define gui.hkb_button_borders = Borders(100, 5, 100, 5)
define gui.hkb_button_text_font = gui.default_font
define gui.hkb_button_text_size = gui.text_size
define gui.hkb_button_text_xalign = 0.5
define gui.hkb_button_text_idle_color = "#000"
define gui.hkb_button_text_hover_color = "#fa9"

# starting with a new style: hkb (hotkey button)
# most of this is copied from choice
style hkb_vbox is vbox
style hkb_button is button
style hkb_button_text is button_text

style hkb_vbox:
    spacing 0

style hkb_button is default:
    properties gui.button_properties("hkb_button")
    idle_background  "mod_assets/hkb_idle_background.png"
    hover_background "mod_assets/hkb_hover_background.png"

    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style hkb_button_text is default:
    properties gui.button_text_properties("hkb_button")
    outlines []

# and a disabled varient of the button
style hkbd_vbox is vbox
style hkbd_button is button
style hkbd_button_text is button_text

style hkbd_vbox:
    spacing 0

style hkbd_button is default:
    properties gui.button_properties("hkb_button")
    idle_background "mod_assets/hkb_disabled_background.png"
    hover_background "mod_assets/hkb_disabled_background.png"

style hkbd_button_text is default:
#    properties gui.button_text_properties("hkb_button")
    font gui.default_font
    size gui.text_size
    xalign 0.5
    idle_color "#000"
    hover_color "#000"
    outlines []

screen calendar_overlay:
    zorder 1

    vbox:
        xalign 0.305
        yalign 0.4

        if allow_dialogue and store.hkb_button.enabled:
            imagebutton:
                idle "mod_assets/calendar/calendar_button_normal.png"
                hover "mod_assets/calendar/calendar_button_hover.png"
                hover_sound gui.hover_sound
                activate_sound gui.activate_sound
                action Function(show_calendar)
        else:
            imagebutton:
                action NullAction()
                idle "mod_assets/calendar/calendar_button_normal.png"


screen hkb_overlay():

    zorder 50

    style_prefix "hkb"

    vbox:
        xalign 0.05
        yalign 0.95

        if allow_dialogue and store.hkb_button.enabled:
            textbutton _("Talk") action Jump("prompt_menu")
        else:
            textbutton _("Talk"):
                action NullAction()
                style "hkbd_button"

# NOTE: disabled until we have additoinal content
#if allow_dialogue and store.hkb_button.enabled:
#            textbutton _("Movies") action Jump("ch30_monikamovie")
#        else:
#            textbutton _("Movies"):
#                action NullAction()
#                style "hkbd_button"


        if store.hkb_button.enabled:
            textbutton _("Music") action Function(select_music)
        else:
            textbutton _("Music"):
                action NullAction()
                style "hkbd_button"

        if allow_dialogue and store.hkb_button.enabled:
            textbutton _("Play") action Jump("pick_a_game")
        else:
            textbutton _("Play"):
                action NullAction()
                style "hkbd_button"

screen movie_overlay():

    zorder 50

    style_prefix "hkb"

    vbox:
        xalign 0.95
        yalign 0.95

        if watchingMovie:
            textbutton _("Pause") action Jump("mm_movie_pausefilm")
        else:
            textbutton _("Pause") action NullAction() style "hkbd_button"

        if watchingMovie:
            textbutton _("Time") action Jump("mm_movie_settime")
        else:
            textbutton _("Time"):
                action NullAction()
                style "hkbd_button"

init python:
    HKBShowButtons()
