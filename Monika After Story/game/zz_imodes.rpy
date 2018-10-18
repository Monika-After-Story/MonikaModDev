# module containing what we call interactive modes
# basically things like headpats and other mouse-based interactions should be
# defined here
#
# screens are defined at 0, so be careful what you attempt to import for use
#
# Some thoughts:
#   The modebar is only available during idle mode (aka no dialogue, games)
#   This bar currently will let you adjust the zoom.
#   In the future, this bar will let you use interactive patting/poking tools
#
#   Because we are limiting this to idle mode, the modebar toggle should jump
#   out of idle flow via jumps. Even though we can certainly do this via 
#   show screens and py functions, it's just simpler to adjust flow by doing
#   direct jumps


init -1 python in mas_modebar:
    import store

    # enable the mode bar
    toggle_enabled = True

    # is the panel visible or not
    modebar_visible = False


# trasnform for the modebar show
transform mas_modebar_tr_show:
    xpos 1280 xanchor 0 ypos 10 yanchor 0
    easein 1.0 xpos 1210

transform mas_modebar_tr_hide:
    xpos 1210 xanchor 0 ypos 10 yanchor 0
    easeout 1.0 xpos 1280

## mode bar labels
label mas_modebar_show_modebar:

    show screen mas_modebar at mas_modebar_tr_show

    # please note, that we actually do NOT want to return to ch30 until 
    # we are done using the modebar.
    # TODO: this should be looped differently
    jump temp_loop

label temp_loop:
    pause 10.0
    jump temp_loop


label mas_modebar_hide_modebar:
    show screen mas_modebar at mas_modebar_tr_hide
    hide screen
    # TODO reset some vars
    jump ch30_loop


screen mas_modebar_toggle():
    zorder 50

    style_prefix "hkb"

    if store.mas_modebar.toggle_enabled:
        if store.mas_modebar_visible:
            textbutton _(">") action Jump("mas_modebar_hide_modebar")
        else:
            textbutton _("<") action Jump("mas_modebar_show_modebar")

    else:
        if store.mas_modebar_visible:
            frame:
                ypadding 5
                xsize 120


image mas_modebar_bg = Frame(
    "mod_assets/frames/black70_pinkborder100.png",
    left=Borders(2, 2, 2, 2)
)

screen mas_modebar():
    zorder 50
    frame:
        area (1210, 10, 70, 490)
        background mas_modebar_bg
        vbox:
            textbutton _("not a button") action NullAction()
            textbutton _("not a button") action NullAction()






