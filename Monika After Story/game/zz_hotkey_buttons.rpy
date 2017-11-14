# Module that handles hotkey button screen
#


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

screen hkb_overlay():

    zorder 50

    style_prefix "hkb"

    vbox:
        xalign 0
        yalign 0.95
    
        if allow_dialogue:
            textbutton _("Talk") action Jump("ch30_monikatopics")
        else:
            textbutton _("Talk"):
                action NullAction() 
                style "hkbd_button"

        textbutton _("Music") action Function(select_music)

        if allow_dialogue:
            textbutton _("Pong") action Function(start_pong)
        else:
            textbutton _("Pong"):
                action NullAction()
                style "hkbd_button"


init python:
    config.overlay_screens.append("hkb_overlay")
