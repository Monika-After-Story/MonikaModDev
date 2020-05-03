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
# TOC:
# EXM010 - ZOOM stuff
# EXM900 - EXTRA menu stuff


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

#    def mas_MBToggleHide():
#        """RUNTIME ONLY
#        hides the toggle.
#        """
#        if mas_MBToggleIsVisible():
#            config.overlay_screens.remove("mas_modebar_toggle")
#            renpy.hide_screen("mas_modebar_toggle")
#
#
#    def mas_MBToggleShow():
#        """RUNTIME ONLY
#        Shows the toggle
#        """
#        if not mas_MBToggleIsVisible():
#            config.overlay_screens.append("mas_modebar_toggle")
#
#
#    def mas_MBToggleRaiseShield():
#        """RUNTIME ONLY
#        Disables the modebar toggle
#        """
#        store.mas_modebar.toggle_enabled = False
#
#
#    def mas_MBToggleDropShield():
#        """RUNTIME ONLY
#        Enables the modebar toggle
#        """
#        store.mas_modebar.toggle_enabled = True
#
#
#    def mas_MBToggleIsEnabled():
#        """
#        RETURNS: True if the modebar toggle is enabled, False otherwise
#        """
#        return store.mas_modebar.toggle_enabled
#
#
#    def mas_MBToggleIsVisible():
#        """
#        RETURNS: True if the modebar toggle is visible, False otherwise
#        """
#        return "mas_modebar_toggle" in config.overlay_screens



init -1 python in mas_extramenu:
    import store

    # true if menu is visible, False otherwise
    menu_visible = False


label mas_extra_menu:
    $ store.mas_extramenu.menu_visible = True
    $ prev_zoom = store.mas_sprites.zoom_level

    # disable other overlays
    $ mas_RaiseShield_core()

    if not persistent._mas_opened_extra_menu:
        call mas_extra_menu_firsttime

    $ persistent._mas_opened_extra_menu = True

    show screen mas_extramenu_area
    jump mas_idle_loop

label mas_extra_menu_close:
    $ store.mas_extramenu.menu_visible = False
    hide screen mas_extramenu_area

    if store.mas_sprites.zoom_level != prev_zoom:
        call mas_extra_menu_zoom_callback

    # re-enable overlays
    if store.mas_globals.in_idle_mode:
        $ mas_coreToIdleShield()
    else:
        $ mas_DropShield_core()

    show monika idle

    jump ch30_loop

label mas_idle_loop:
    pause 10.0
    $ renpy.not_infinite_loop(60)
    jump mas_idle_loop

default persistent._mas_opened_extra_menu = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_extra_menu_firsttime",
            prompt="Can you explain the Extras menu?",
            category=["misc"]
        )
    )

label mas_extra_menu_firsttime:
    if not persistent._mas_opened_extra_menu:
        m 1hua "Welcome to the Extras menu, [player]!"

    m 1eua "This is where I'll add things that aren't games, like special interactions you can do with your mouse."
    m "You can also open this menu by pressing the 'e' key."

    if not persistent._mas_opened_extra_menu:
        m 1hua "Look forward to some neat things in this menu!"

    python:
        this_ev = mas_getEV("mas_extra_menu_firsttime")
        this_ev.unlocked = True
        this_ev.pool = True

    # explaining different features here
    call mas_extra_menu_zoom_intro

    return

################################# ZOOM LABELS #################################
# [EXM010]

label mas_extra_menu_zoom_intro:
    m 1eua "One thing I added is a way for you to adjust your field of view, so now you can sit closer or farther away from me."
    m 1eub "You can adjust this using the slider in the 'Zoom' section of the Extras menu."
    return

default persistent._mas_pm_zoomed_out = False
default persistent._mas_pm_zoomed_in = False
default persistent._mas_pm_zoomed_in_max = False

label mas_extra_menu_zoom_callback:
    $ import store.mas_sprites as mas_sprites
    $ aff_larger_than_zero = _mas_getAffection() > 0
    # logic about the zoom

    if mas_sprites.zoom_level < mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_out
            ):
            # zoomed OUT
            call mas_extra_menu_zoom_out_first_time
            $ persistent._mas_pm_zoomed_out = True

    elif mas_sprites.zoom_level == mas_sprites.max_zoom:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in_max
            ):
            # zoomed in max
            call mas_extra_menu_zoom_in_max_first_time
            $ persistent._mas_pm_zoomed_in_max = True
            $ persistent._mas_pm_zoomed_in = True

    elif mas_sprites.zoom_level > mas_sprites.default_zoom_level:

        if (
                aff_larger_than_zero
                and not persistent._mas_pm_zoomed_in
            ):
            # zoomed in not max
            call mas_extra_menu_zoom_in_first_time
            $ persistent._mas_pm_zoomed_in = True

    return

label mas_extra_menu_zoom_out_first_time:
    m 1ttu "Can't sit up straight for long?"
    m "Or maybe you just want to see the top of my head?"
    m 1hua "Ehehe~"
    return

label mas_extra_menu_zoom_in_first_time:
    m 1ttu "Sitting a bit closer?"
    m 1hua "I don't mind."
    return

label mas_extra_menu_zoom_in_max_first_time:
    m 6wuo "[player]!"
    m 6rkbfd "When your face is this close..."
    m 6ekbfd "I feel..."
    show monika 6hkbfa
    pause 2.0
    m 6hubfa "Warm..."
    return

################################# EXTRA MENU STUFF ############################
# [EXM900]



# FIXME: the following styles cannot be checked because of the commented code
style mas_mbs_vbox is vbox:
    spacing 0

style mas_mbs_button is generic_button_light
#    xysize (35, 35)

style mas_mbs_button_dark is generic_button_dark
#    xysize (35, 35)

style mas_mbs_button_text is generic_button_text_light

style mas_mbs_button_text_dark is generic_button_text_dark

#screen mas_modebar_toggle():
#    zorder 50
#
#    fixed:
#        area (1245, 500, 35, 35)
#        style_prefix "mas_mbs"
#
#        if store.mas_modebar.toggle_enabled:
#            if store.mas_modebar.modebar_visible:
#                textbutton _(">") action Jump("mas_modebar_hide_modebar")
#            else:
#                textbutton _("<") action Jump("mas_modebar_show_modebar")
#
#        else:
#            if store.mas_modebar.modebar_visible:
#                frame:
#                    xsize 35
#                    background Image("mod_assets/buttons/squares/square_disabled.png")
#                    text ">"
#            else:
#                frame:
#                    xsize 35
#                    background Image("mod_assets/buttons/squares/square_disabled.png")
#                    text "<"

#screen mas_extramenu_toggle():
#    zorder 55
#
#    fixed:
#        area (0.05, 559, 120, 35)
#        style_prefix "hkb"
#
#        if store.mas_modebar.toggle_enabled:
#            if store.mas_modebar.modebar_visible:
#                textbutton _("Close") action Jump("mas_modearea_hide_modearea")
#            else:
#                textbutton _("Tools") action Jump("mas_modearea_show_modearea")
#
#        else:
#            if store.mas_modebar.modebar_visible:
#                frame:
#                    xsize 120
#                    background Image("mod_assets/hkb_disabled_background.png")
#                    text "Close"
#            else:
#                frame:
#                    xsize 120
#                    background Image("mod_assets/hkb_disabled_background.png")
#                    text "Tools"


#image mas_modebar_bg = Image("mod_assets/frames/modebar.png")

#screen mas_modebar():
#    zorder 50
#    fixed:
#        area (1210, 10, 70, 490)
#        add "mas_modebar_bg"
#        vbox:
#            textbutton _("not") action NullAction()
#            textbutton _("not3") action NullAction()

style mas_extra_menu_frame:
    background Frame("mod_assets/frames/trans_pink2pxborder100.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_frame_dark:
    background Frame("mod_assets/frames/trans_pink2pxborder100_d.png", Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))

style mas_extra_menu_label_text is hkb_button_text:
    color "#FFFFFF"

style mas_extra_menu_label_text_dark is hkb_button_text_dark:
    color "#FD5BA2"

style mas_adjust_vbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"
    bar_vertical True

style mas_adjustable_button is generic_button_light:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_dark is generic_button_dark:
    xysize (None, None)
    padding (3, 3, 3, 3)

style mas_adjustable_button_text is generic_button_text_light:
    kerning 0.2

style mas_adjustable_button_text_dark is generic_button_text_dark:
    kerning 0.2

screen mas_extramenu_area():
    zorder 52

    key "e" action Jump("mas_extra_menu_close")
    key "E" action Jump("mas_extra_menu_close")

    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")

        # close button
        textbutton _("Close"):
            area (60, 596, 120, 35)
            style "hkb_button"
            action Jump("mas_extra_menu_close")

        # zoom control
        frame:
            area (195, 450, 80, 255)
            style "mas_extra_menu_frame"
            vbox:
                spacing 2
                label "Zoom":
                    text_style "mas_extra_menu_label_text"
                    xalign 0.5

                # resets the zoom value back to default
                textbutton _("Reset"):
                    style "mas_adjustable_button"
                    xsize 72
                    ysize 35
                    xalign 0.3
                    action SetField(store.mas_sprites, "zoom_level", store.mas_sprites.default_zoom_level)

                # actual slider for adjusting zoom
                bar value FieldValue(store.mas_sprites, "zoom_level", store.mas_sprites.max_zoom):
                    style "mas_adjust_vbar"
                    xalign 0.5
                $ store.mas_sprites.adjust_zoom()

        # TODO: frame for nose boop control
        # TODO: only have available if certain affection +
        #   (Definitely not below normal)
#        frame:
#            area (280, 450, 80, 120)
#            background Frame("mod_assets/frames/trans_pink2pxborder100.png", left=Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4))
#
#            vbox:
#                spacing 2
#
#                label "Boop":
#                    style "hkb_button_text"
