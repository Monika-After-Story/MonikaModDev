# module containing what we call interactive modes (extras)
# basically things like headpats and other mouse-based interactions should be
# defined here
#
# screens are defined at 0, so be careful what you attempt to import for use
#
# Some thoughts:
#   the extras menu is a grid screen showed when the eExtras menu option is
#   activated. 
#



init python:
  
    # extras menu function
    def mas_open_extra_menu():
        """
        Jumps to the extra menu workflow
        """
        renpy.jump("mas_extra_menu")


    ## panel functions
    # TODO

    ## toggle functions

    def mas_MBToggleHide():
        """RUNTIME ONLY
        hides the toggle.
        """
        if mas_MBToggleIsVisible():
            config.overlay_screens.remove("mas_modebar_toggle")
            renpy.hide_screen("mas_modebar_toggle")


    def mas_MBToggleShow():
        """RUNTIME ONLY
        Shows the toggle
        """
        if not mas_MBToggleIsVisible():
            config.overlay_screens.append("mas_modebar_toggle")


    def mas_MBToggleRaiseShield():
        """RUNTIME ONLY
        Disables the modebar toggle
        """
        store.mas_modebar.toggle_enabled = False


    def mas_MBToggleDropShield():
        """RUNTIME ONLY
        Enables the modebar toggle
        """
        store.mas_modebar.toggle_enabled = True


    def mas_MBToggleIsEnabled():
        """
        RETURNS: True if the modebar toggle is enabled, False otherwise
        """
        return store.mas_modebar.toggle_enabled


    def mas_MBToggleIsVisible():
        """
        RETURNS: True if the modebar toggle is visible, False otherwise
        """
        return "mas_modebar_toggle" in config.overlay_screens

### TESTING
init 100 python:
#    mas_MBToggleShow()
   config.overlay_screens.append("mas_modearea_toggle")



init -1 python in mas_extramenu:
    import store


label mas_extra_menu:
    return


# TODO: remov the below for the new stuff

## mode bar labels
label mas_modebar_show_modebar:

    $ store.mas_modebar.modebar_visible = True
#    show screen mas_modebar with easeinright
    show mas_modebar_bg zorder 6 at mas_modebar_tr_show
    pause 0.7
    show screen mas_modebar

    # please note, that we actually do NOT want to return to ch30 until 
    # we are done using the modebar.
    # TODO: this should be looped differently
    jump temp_loop

label temp_loop:
    pause 10.0
    jump temp_loop


label mas_modebar_hide_modebar:

    $ store.mas_modebar.modebar_visible = False
    hide screen mas_modebar
    show mas_modebar_bg at mas_modebar_tr_hide
    pause 0.7
    hide mas_modebar_bg

    # TODO reset some vars
    jump ch30_loop


label mas_modearea_show_modearea:
    $ store.mas_modebar.modebar_visible = True
    show screen mas_modearea
    jump temp_loop

label mas_modearea_hide_modearea:
    $ store.mas_modebar.modebar_visible = False
    hide screen mas_modearea
    jump ch30_loop

# trasnform for the modebar show
transform mas_modebar_tr_show:
    xpos 1280 xanchor 0 ypos 10 yanchor 0
    easein 0.7 xpos 1210 

transform mas_modebar_tr_hide:
    xpos 1210 xanchor 0 ypos 10 yanchor 0
    easeout 0.7 xpos 1280 

style mas_mbs_vbox is vbox
style mas_mbs_button is button
style mas_mbs_button_text is button_text

style mas_mbs_vbox:
    spacing 0

style mas_mbs_button is default:
#    width 35
#    height 35
#    tile False
    idle_background  "mod_assets/buttons/squares/square_idle.png"
    hover_background "mod_assets/buttons/squares/square_hover.png"
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style mas_mbs_button_text is default:
    font gui.default_font
    size gui.text_size
    xalign 0.5
    idle_color "#000"
    hover_color "#fa9"
    outlines []

screen mas_modebar_toggle():
    zorder 50

    fixed:
        area (1245, 500, 35, 35)
        style_prefix "mas_mbs"

        if store.mas_modebar.toggle_enabled:
            if store.mas_modebar.modebar_visible:
                textbutton _(">") action Jump("mas_modebar_hide_modebar")
            else:
                textbutton _("<") action Jump("mas_modebar_show_modebar")

        else:
            if store.mas_modebar.modebar_visible:
                frame:
                    xsize 35
                    background Image("mod_assets/buttons/squares/square_disabled.png")
                    text ">"
            else:
                frame:
                    xsize 35
                    background Image("mod_assets/buttons/squares/square_disabled.png")
                    text "<"

screen mas_modearea_toggle():
    zorder 55

    fixed:
        area (0.05, 559, 120, 35)
        style_prefix "hkb"

        if store.mas_modebar.toggle_enabled:
            if store.mas_modebar.modebar_visible:
                textbutton _("Close") action Jump("mas_modearea_hide_modearea")
            else:
                textbutton _("Tools") action Jump("mas_modearea_show_modearea")

        else:
            if store.mas_modebar.modebar_visible:
                frame:
                    xsize 120
                    background Image("mod_assets/hkb_disabled_background.png")
                    text "Close"
            else:
                frame:
                    xsize 120
                    background Image("mod_assets/hkb_disabled_background.png")
                    text "Tools"


image mas_modebar_bg = Image("mod_assets/frames/modebar.png")

screen mas_modebar():
    zorder 50
    fixed:
        area (1210, 10, 70, 490)
#        add "mas_modebar_bg"
        vbox:
            textbutton _("not") action NullAction()
            textbutton _("not3") action NullAction()

screen mas_modearea():
    zorder 52
    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")


#        textbutton _("not"):
#            area (
        
#        fixed:
#            area (




