#Whether dark mode is enabled or not
default persistent._mas_dark_mode_enabled = False

#Whether auto ui change is enabled or not
default persistent._mas_auto_mode_enabled = False

#START: mas_globals addition
init -1 python in mas_globals:
    #None on init, True if we're using dark ui, False if not
    dark_mode = None

#START: Door greeting labels overrides

init 999 python:
    config.label_overrides["i_greeting_monikaroom"] = "i_greeting_monikaroom_override"
    config.label_overrides["monikaroom_greeting_choice"] = "monikaroom_greeting_choice_override"

label i_greeting_monikaroom_override:

    if persistent._mas_auto_mode_enabled:
        $ mas_darkMode(morning_flag)
    else:
        $ mas_darkMode(not persistent._mas_dark_mode_enabled)

    # couple of things:
    # 1 - if you quit here, monika doesnt know u here
    $ mas_enable_quit()

    # 2 - music button + hotkeys should be disabled
    $ store.mas_hotkeys.music_enabled = False

    # 3 - keymaps not set (default)
    # 4 - overlays hidden (skip visual)
    # 5 - music is off (skip visual)

    scene black

    $ has_listened = False

    # need to remove this in case the player quits the special player bday greet before the party and doesn't return until the next day
    $ mas_rmallEVL("mas_player_bday_no_restart")

    # FALL THROUGH
label monikaroom_greeting_choice_override:
    $ _opendoor_text = "...Gently open the door."
    if persistent._mas_sensitive_mode:
        $ _opendoor_text = "Open the door."

    if mas_isMoniBroken():
        pause 4.0

    menu:
        "[_opendoor_text]" if not persistent.seen_monika_in_room and not mas_isplayer_bday():
            #Lose affection for not knocking before entering.
            $ mas_loseAffection(reason=5)
            if mas_isMoniUpset(lower=True):
                $ persistent.seen_monika_in_room = True
                jump monikaroom_greeting_opendoor_locked
            else:
                jump monikaroom_greeting_opendoor
        "Open the door." if persistent.seen_monika_in_room or mas_isplayer_bday():
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_opendoor_listened
                else:
                    jump mas_player_bday_opendoor
            elif persistent.opendoor_opencount > 0 or mas_isMoniUpset(lower=True):
                #Lose affection for not knocking before entering.
                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_locked
            else:
                #Lose affection for not knocking before entering.
                $ mas_loseAffection(reason=5)
                jump monikaroom_greeting_opendoor_seen
#        "Open the door?" if persistent.opendoor_opencount >= opendoor.MAX_DOOR:
#            jump opendoor_game
        "Knock.":
            #Gain affection for knocking before entering.
            $ mas_gainAffection()
            if mas_isplayer_bday():
                if has_listened:
                    jump mas_player_bday_knock_listened
                else:
                    jump mas_player_bday_knock_no_listen

            jump monikaroom_greeting_knock
        "Listen." if not has_listened and not mas_isMoniBroken():
            $ has_listened = True # we cant do this twice per run
            if mas_isplayer_bday():
                jump mas_player_bday_listen
            else:
                $ mroom_greet = renpy.random.choice(gmr.eardoor)
#               $ mroom_greet = gmr.eardoor[len(gmr.eardoor)-1]
                jump expression mroom_greet

    # NOTE: return is expected in monikaroom_greeting_cleanup

#START: Opendoor locked override
init 999 python:
    config.label_overrides["monikaroom_greeting_opendoor_locked"] = "monikaroom_greeting_opendoor_locked_override"
# locked door, because we are awaitng more content
label monikaroom_greeting_opendoor_locked_override:
    if mas_isMoniBroken():
        jump monikaroom_greeting_opendoor_broken_quit

    # monika knows you are here
    $ mas_disable_quit()

    show paper_glitch2
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.2
    stop sound
    pause 0.7

    $ style.say_window = style.window_monika
    m "Did I scare you, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Did I scare you, [player]?{fast}"
        "Yes.":
            if mas_isMoniNormal(higher=True):
                m "Aww, sorry."
            else:
                m "Good."

        "No.":
            m "{cps=*2}Hmph, I'll get you next time.{/cps}{nw}"
            $ _history_list.pop()
            m "I figured. It's a basic glitch after all."

    if mas_isMoniNormal(higher=True):
        m "Since you keep opening my door,{w} I couldn't help but add a little surprise for you~"
    else:
        m "Since you never seem to knock first,{w} I had to try to scare you a little."

    m "Knock next time, okay?"
    m "Now let me fix up this room..."

    hide paper_glitch2
    call spaceroom(scene_change=True, change_textbox=False)

    if renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox_override"):
        $ style.say_window = style.window

    if mas_isMoniNormal(higher=True):
        m 1hua "There we go!"
    elif mas_isMoniUpset():
        m 2efc "There."
    else:
        m 6ekc "Okay..."

    if not renpy.seen_label("monikaroom_greeting_opendoor_locked_tbox_override"):
        menu:
            "...the textbox...":
                if mas_isMoniNormal(higher=True):
                    m 1lksdlb "Oops! I'm still learning how to do this."
                    m 1lksdla "Let me just change this flag here...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m 1hua "All fixed!"

                elif mas_isMoniUpset():
                    m 2dfc "Hmph. I'm still learning how to do this."
                    m 2efc "Let me just change this flag here...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m "There."

                else:
                    m 6dkc "Oh...{w}I'm still learning how to do this."
                    m 6ekc "Let me just change this flag here...{w=1.5}{nw}"
                    $ style.say_window = style.window
                    m "Okay, fixed."

    # NOTE: fall through please

label monikaroom_greeting_opendoor_locked_tbox_override:
    if mas_isMoniNormal(higher=True):
        m 1eua "Welcome back, [player]."
    elif mas_isMoniUpset():
        m 2efc "So...{w}you're back, [player]."
    else:
        m 6ekc "...Nice to see you again, [player]."
    jump monikaroom_greeting_cleanup

#START: Spaceroom label override
init 999 python:
    config.label_overrides["spaceroom"] = "spaceroom_override"

label spaceroom_override(start_bg=None, hide_mask=False, hide_monika=False, dissolve_all=False, dissolve_masks=False, scene_change=False, force_exp=None, change_textbox=True):

    with None

    if scene_change:
        scene black

    python:
        monika_room = None

        # MORNING CHECK
        # establishes correct room to use
        if mas_isMorning():
            if not morning_flag or scene_change:
                morning_flag = True
                monika_room = "monika_day_room"

        else:
            if morning_flag or scene_change:
                morning_flag = False
                monika_room = "monika_room"

        if persistent._mas_auto_mode_enabled:
            mas_darkMode(morning_flag, change_textbox)
        else:
            mas_darkMode(not persistent._mas_dark_mode_enabled, change_textbox)

        ## are we hiding monika
        if not hide_monika:
            if force_exp is None:
#                force_exp = "monika idle"
                if dissolve_all:
                    force_exp = store.mas_affection._force_exp()

                else:
                    force_exp = "monika idle"

            if not renpy.showing(force_exp):
                renpy.show(force_exp, at_list=[t11], zorder=MAS_MONIKA_Z)

                if not dissolve_all:
                    renpy.with_statement(None)

        # if we onyl want to dissolve masks, then we dissolve now
        if not dissolve_all and not hide_mask:
            mas_drawSpaceroomMasks(dissolve_masks)

        # actual room check
        # are we using a custom bg or not
        if start_bg:
            if not renpy.showing(start_bg):
                renpy.show(start_bg, tag="sp_mas_room", zorder=MAS_BACKGROUND_Z)

        elif monika_room is not None:
            if not renpy.showing(monika_room):
                renpy.show(
                    monika_room,
                    tag="sp_mas_room",
                    zorder=MAS_BACKGROUND_Z
                )
                mas_calShowOverlay()


    # vignette
    if store.mas_globals.show_vignette:
        show vignette zorder 70

    # bday stuff (this checks itself)
    if persistent._mas_922_in_922_mode:
        $ store.mas_dockstat.surpriseBdayShowVisuals()

    # d25 seasonal
    if persistent._mas_d25_deco_active:
        $ store.mas_d25_event.showD25Visuals()

    # player bday
    if persistent._mas_player_bday_decor:
        $ store.mas_player_bday_event.show_player_bday_Visuals()

    if datetime.date.today() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs_pst(mas_acs_roses)

    # dissolving everything means dissolve last
    if dissolve_all and not hide_mask:
        $ mas_drawSpaceroomMasks(dissolve_all)

    return

# START: Dark mode function
#NOTE: Scrollbar/sliders will remain as normal
default mas_globals.dark_mode = None

init python:
    def mas_darkMode(morning_flag=False, change_textbox=True):
        if not morning_flag:
            store.mas_globals.dark_mode = True
            #style.mas_adjust_vbar = style.mas_adjust_vbar_dark
            style.mas_adjustable_button_text = style.mas_adjustable_button_text_dark
            style.mas_mbs_button = style.mas_mbs_button_dark
            style.mas_adjustable_button = style.mas_adjustable_button_dark
            #style.hkb_button = style.hkb_button_dark
            #style.hkb_button_text = style.hkb_button_text_dark
            #style.hkbd_button = style.hkbd_button_dark
            #style.hkbd_button_text = style.hkbd_button_text_dark
            #style.hkb_text = style.hkb_text_dark
            #style.check_button = style.check_button_dark
            #style.check_button_text = style.check_button_text_dark
            #style.choice_button = style.choice_button_dark
            #style.choice_vbox = style.choice_vbox_dark
            #style.scrollable_menu_button = style.scrollable_menu_button_dark
            #style.twopane_scrollable_menu_button = style.twopane_scrollable_menu_button_dark
            style.slider = style.slider_dark
            style.slider_slider = style.slider_slider_dark
            style.scrollbar = style.scrollbar_dark
            style.frame = style.frame_dark
            style.confirm_frame = style.confirm_frame_dark
            style.game_menu_outer_frame = style.game_menu_outer_frame_dark
            style.edited_def = style.edited_def_dark
            style.poemgame_text = style.poemgame_text_dark
            style.namebox = style.namebox_dark
            #style.navigation_button_text = style.navigation_button_text_dark
            style.main_menu_version = style.main_menu_version_dark
            style.confirm_prompt_text = style.confirm_prompt_text_dark
            style.island_button = style.island_button_dark
            style.island_button_text = style.island_button_text_dark
            style.music_menu_outer_frame = style.music_menu_outer_frame_dark
            style.quick_button_text = style.quick_button_text_dark
            #style.mas_selector_sidebar_vbar = style.mas_selector_sidebar_vbar_dark
            #style.choice_button_text = style.choice_button_text_dark
            #style.scrollable_menu_button_text = style.scrollable_menu_button_text_dark
            #style.twopane_scrollable_menu_button_text = style.twopane_scrollable_menu_button_text_dark
            #style.twopane_scrollable_menu_special_button_text = style.twopane_scrollable_menu_special_button_text_dark
            #style.twopane_scrollable_menu_new_button_text = style.twopane_scrollable_menu_new_button_text_dark
            style.button = style.button_dark
            gui.main_menu_background = "menu_bg_d"
            gui.game_menu_background = "game_menu_bg_d"
            ctc = "ctc_d"
            style.main_menu_frame = style.main_menu_frame_dark
            style.window_monika = style.window_monika_dark
            style.window = style.window_dark

            if change_textbox:
                style.say_window = style.window_dark
        else:
            store.mas_globals.dark_mode = False
            #style.mas_adjust_vbar = style.mas_adjust_vbar_def
            style.mas_adjustable_button_text = style.mas_adjustable_button_text_def
            style.mas_mbs_button = style.mas_mbs_button_def
            style.mas_adjustable_button = style.mas_adjustable_button_def
            #style.hkb_button = style.hkb_button_def
            #style.hkb_button_text = style.hkb_button_text_def
            #style.hkbd_button = style.hkbd_button_def
            #style.hkbd_button_text = style.hkbd_button_text_def
            #style.hkb_text = style.hkb_text_def
            #style.check_button = style.check_button_def
            #style.check_button_text = style.check_button_text_def
            #style.choice_button = style.choice_button_def
            #style.choice_vbox = style.choice_vbox_def
            #style.scrollable_menu_button = style.scrollable_menu_button_def
            #style.twopane_scrollable_menu_button = style.twopane_scrollable_menu_button_def
            style.slider = style.slider_def
            style.slider_slider = style.slider_slider_def
            style.scrollbar = style.scrollbar_def
            style.frame = style.frame_def
            style.confirm_frame = style.confirm_frame_def
            style.game_menu_outer_frame = style.game_menu_outer_frame_def
            style.edited_def = style.edited_def_def
            style.poemgame_text = style.poemgame_text_def
            style.namebox = style.namebox_def
            #style.navigation_button_text = style.navigation_button_text_def
            style.main_menu_version = style.main_menu_version_def
            style.confirm_prompt_text = style.confirm_prompt_text_def
            style.island_button = style.island_button_def
            style.island_button_text = style.island_button_text_def
            style.music_menu_outer_frame = style.music_menu_outer_frame_def
            style.quick_button_text = style.quick_button_text_def
            #style.mas_selector_sidebar_vbar = style.mas_selector_sidebar_vbar_def
            #style.choice_button_text = style.choice_button_text_def
            #style.scrollable_menu_button_text = style.scrollable_menu_button_text_def
            #style.twopane_scrollable_menu_button_text = style.twopane_scrollable_menu_button_text_def
            #style.twopane_scrollable_menu_special_button_text = style.twopane_scrollable_menu_special_button_text_def
            #style.twopane_scrollable_menu_new_button_text = style.twopane_scrollable_menu_new_button_text_def
            style.button = style.button_def
            gui.main_menu_background = "menu_bg"
            gui.game_menu_background = "game_menu_bg"
            ctc = "ctc"
            style.main_menu_frame = style.main_menu_frame_def
            style.window_monika = style.window_monika_def
            style.window = style.window_def

            if change_textbox:
                style.say_window = style.window_def

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
    idle_color "#000"
    hover_color "#fa9"
    outlines []
    kerning 0.2
    xalign 0.5
    yalign 0.5
    font gui.default_font
    size gui.text_size

style mas_adjustable_button_text_dark is default:
    idle_color "#e670af"
    hover_color "#ffcce8"
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
    idle_color "#e670af"
    hover_color "#ffcce8"
    kerning 0.2
    outlines []

style hkb_dark_text is default:
    xalign 0.5
    size gui.text_size
    font gui.default_font
    color "#e670af"
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
#    idle_background Frame("gui/button/choice_idle_background_d.png")
#    hover_background Frame("gui/button/choice_hover_background_d.png")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style choice_button_text_dark is button_text_dark

style choice_button_text_dark is default:
    properties gui.button_text_properties("choice_dark_button")
    idle_color "#e670af"
    hover_color "#ffcce8"
    outlines []

style choice_dark_button_text is button_text_dark

style choice_dark_button_text is default:
    properties gui.button_text_properties("choice_dark_button")
    idle_color "#e670af"
    hover_color "#ffcce8"
    outlines []

style talk_choice_dark_vbox is choice_dark_vbox:
    xcenter 960

style talk_choice_dark_button is choice_dark_button
style talk_choice_dark_button_text is choice_dark_button_text

style scrollable_menu_dark_button is choice_dark_button:
    properties gui.button_properties("scrollable_menu_dark_button")
#    idle_background Frame("gui/button/scrollable_menu_idle_background_d.png")
#    hover_background Frame("gui/button/scrollable_menu_hover_background_d.png")

style scrollable_menu_dark_button_text is choice_dark_button_text:
    properties gui.button_text_properties("scrollable_menu_dark_button")
    idle_color "#e670af"
    hover_color "#ffcce8"

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
#    idle_background Frame("gui/button/twopane_scrollable_menu_idle_background_d.png")
#    hover_background Frame("gui/button/twopane_scrollable_menu_hover_background_d.png")

style twopane_scrollable_menu_dark_button_text is choice_dark_button_text:
    properties gui.button_text_properties("twopane_scrollable_menu_dark_button")
    idle_color "#e670af"
    hover_color "#ffcce8"

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

    background "menu_nav_d"

style slider_def:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

style slider_dark:
    ysize 18
    base_bar Frame("gui/scrollbar/horizontal_poem_bar_d.png", tile=False)
    thumb "gui/slider/horizontal_hover_thumb.png"

#style slider_dark_label is pref_label
#style slider_dark_label_text is pref_label_text
#style slider_dark_slider is gui_slider_dark
#style slider_dark_button is gui_button_dark
#style slider_dark_button_text is gui_button_text
#style slider_dark_pref_vbox is pref_vbox

style slider_slider_def is gui_slider
style slider_slider_def:
    xsize 350

style slider_slider_dark is gui_slider_dark
style slider_slider_dark:
    xsize 350

#style bar_def:
#    ysize 18
#    base_bar Frame("gui/scrollbar/horizontal_poem_bar.png", tile=False)
#    thumb Frame("gui/scrollbar/horizontal_poem_thumb.png", top=6, right=6, tile=True)

#style bar_dark:
#    ysize 18
#    base_bar Frame("gui/scrollbar/horizontal_poem_bar_d.png", tile=False)
#    thumb Frame("gui/scrollbar/horizontal_poem_thumb_d.png", top=6, right=6, tile=True)

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
    color "#e670af"
    outlines []
    hover_outlines [(3, "#ffcce8", 0, 0)]
    insensitive_outlines [(3, "#ffcce8", 0, 0)]

style main_menu_version_def is main_menu_text:
    color "#000000"
    size 16
    outlines []

style main_menu_version_dark is main_menu_text:
    color "#e670af"
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

#START: toggle methods
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
        #renpy.show_screen("navigation")

screen preferences():

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 4

    default tooltip = Tooltip("")

    use game_menu(_("Settings"), scroll="viewport"):

        vbox:
            xoffset 50

            hbox:
                box_wrap True

                if renpy.variant("pc"):

                    vbox:
                        style_prefix ("radio" if not mas_globals.dark_mode else "radio_dark")
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

#                vbox:
#                    style_prefix "check"
#                    label _("Skip")
#                    textbutton _("Unseen Text") action Preference("skip", "toggle")
#                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    #textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                #Disable/Enable space animation AND lens flair in room
                vbox:
                    style_prefix ("check" if not mas_globals.dark_mode else "check_dark" )
                    label _("Graphics")
                    textbutton _("Disable Animation") action ToggleField(persistent, "_mas_disable_animations")
                    textbutton _("Change Renderer") action Function(renpy.call_in_new_context, "mas_gmenu_start")

                    #Handle buttons
                    textbutton _("Dark UI"):
                        action [Function(mas_darkMode, persistent._mas_dark_mode_enabled), Function(mas_settings._dark_mode_toggle)]
                        selected persistent._mas_dark_mode_enabled
                    textbutton _("Day/Night UI"):
                        action [Function(mas_darkMode, morning_flag), Function(mas_settings._auto_mode_toggle)]
                        selected persistent._mas_auto_mode_enabled


                vbox:
                    style_prefix ("check" if not mas_globals.dark_mode else "check_dark" )
                    label _("Gameplay")
                    if persistent._mas_unstable_mode:
                        textbutton _("Unstable"):
                            action SetField(persistent, "_mas_unstable_mode", False)
                            selected persistent._mas_unstable_mode

                    else:
                        textbutton _("Unstable"):
                            action [Show(screen="dialog", message=layout.UNSTABLE, ok_action=Hide(screen="dialog")), SetField(persistent, "_mas_unstable_mode", True)]
                            selected persistent._mas_unstable_mode
                            hovered tooltip.Action(layout.MAS_TT_UNSTABLE)

                    textbutton _("Repeat Topics"):
                        action ToggleField(persistent,"_mas_enable_random_repeats", True, False)
                        hovered tooltip.Action(layout.MAS_TT_REPEAT)

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.
                vbox:
                    style_prefix ("check" if not mas_globals.dark_mode else "check_dark" )
                    label _(" ")
                    textbutton _("Sensitive Mode"):
                        action ToggleField(persistent, "_mas_sensitive_mode", True, False)
                        hovered tooltip.Action(layout.MAS_TT_SENS_MODE)

                    if renpy.windows and store.mas_windowreacts.can_show_notifs:
                        textbutton _("Window Reacts"):
                            action ToggleField(persistent, "_mas_windowreacts_windowreacts_enabled", True, False)
                            hovered tooltip.Action(layout.MAS_TT_ACTV_WND)

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                python:
                    ### random chatter preprocessing
                    if mas_randchat_prev != persistent._mas_randchat_freq:
                        # adjust the randoms if it changed
                        mas_randchat.adjustRandFreq(
                            persistent._mas_randchat_freq
                        )

                    # setup the display string
                    rc_display = mas_randchat.getRandChatDisp(
                        persistent._mas_randchat_freq
                    )

                    # setup previous values
                    mas_randchat_prev = persistent._mas_randchat_freq


                    ### sunrise / sunset preprocessing
                    # figure out which value is changing (if any)
                    if mas_suntime.change_state == mas_suntime.RISE_CHANGE:
                        # we are modifying sunrise

                        if mas_suntime.sunrise > mas_suntime.sunset:
                            # ensure sunset remains >= than sunrise
                            mas_suntime.sunset = mas_suntime.sunrise

                        if mas_sunrise_prev == mas_suntime.sunrise:
                            # if no change since previous, then switch state
                            mas_suntime.change_state = mas_suntime.NO_CHANGE

                        mas_sunrise_prev = mas_suntime.sunrise

                    elif mas_suntime.change_state == mas_suntime.SET_CHANGE:
                        # we are modifying sunset

                        if mas_suntime.sunset < mas_suntime.sunrise:
                            # ensure sunrise remains <= than sunset
                            mas_suntime.sunrise = mas_suntime.sunset

                        if mas_sunset_prev == mas_suntime.sunset:
                            # if no change since previous, then switch state
                            mas_suntime.change_state = mas_suntime.NO_CHANGE

                        mas_sunset_prev = mas_suntime.sunset
                    else:
                        # decide if we are modifying sunrise or sunset

                        if mas_sunrise_prev != mas_suntime.sunrise:
                            mas_suntime.change_state = mas_suntime.RISE_CHANGE

                        elif mas_sunset_prev != mas_suntime.sunset:
                            mas_suntime.change_state = mas_suntime.SET_CHANGE

                        # set previous values
                        mas_sunrise_prev = mas_suntime.sunrise
                        mas_sunset_prev = mas_suntime.sunset


                    ## prepreocess display time
                    persistent._mas_sunrise = mas_suntime.sunrise * 5
                    persistent._mas_sunset = mas_suntime.sunset * 5
                    sr_display = mas_cvToDHM(persistent._mas_sunrise)
                    ss_display = mas_cvToDHM(persistent._mas_sunset)

                vbox:

                    hbox:
                        label _("Sunrise   ")

                        # display time
                        label _("[[ " + sr_display + " ]")

                    bar value FieldValue(mas_suntime, "sunrise", range=mas_max_suntime, style="slider")


                    hbox:
                        label _("Sunset   ")

                        # display time
                        label _("[[ " + ss_display + " ]")

                    bar value FieldValue(mas_suntime, "sunset", range=mas_max_suntime, style="slider")


                vbox:

                    hbox:
                        label _("Random Chatter   ")

                        # display str
                        label _("[[ " + rc_display + " ]")

                    bar value FieldValue(persistent, "_mas_randchat_freq",
                    range=6, style="slider")

                    hbox:
                        label _("Ambient Volume")

                    bar value Preference("mixer amb volume")


                vbox:

                    label _("Text Speed")

                    #bar value Preference("text speed")
                    bar value FieldValue(_preferences, "text_cps", range=170, max_is_zero=False, style="slider", offset=30)

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


            hbox:
                textbutton _("Update Version"):
                    action Function(renpy.call_in_new_context, 'forced_update_now')
                    style ("navigation_button" if not mas_globals.dark_mode else "navigation_dark_button")

                textbutton _("Import DDLC Save Data"):
                    action Function(renpy.call_in_new_context, 'import_ddlc_persistent_in_settings')
                    style ("navigation_button" if not mas_globals.dark_mode else "navigation_dark_button")


    text tooltip.value:
        xalign 0.0 yalign 1.0
        xoffset 300 yoffset -10
        style ("main_menu_version_def" if not mas_globals.dark_mode else "main_menu_version_dark")
#        layout "greedy"
#        text_align 0.5
#        xmaximum 650

    text "v[config.version]":
        xalign 1.0 yalign 0.0
        xoffset -10 
        style ("main_menu_version_def" if not mas_globals.dark_mode else "main_menu_version_dark")

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

style quick_button_text_def is button_text

style quick_button_text_def:
    properties gui.button_text_properties("quick_button")
    outlines []

style quick_button_text_dark is button_text_dark

style quick_button_text_dark:
    properties gui.button_text_properties("quick_button_dark")
    outlines []

#START: music selector styles

style music_menu_outer_frame_def is game_menu_outer_frame_def

style music_menu_outer_frame_def:
    background "mod_assets/music_menu.png"

style music_menu_outer_frame_dark is game_menu_outer_frame_dark

style music_menu_outer_frame_dark:
    background "mod_assets/music_menu_d.png"

#START: selector styles

#style mas_selector_sidebar_vbar_def:
#    xsize 18
#    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
##    thumb "gui/slider/horizontal_hover_thumb.png"
#    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
#    bar_vertical True
#    bar_invert True

#style mas_selector_sidebar_vbar_dark:
#    xsize 18
#    base_bar Frame("gui/scrollbar/vertical_poem_bar_d.png", tile=False)
##    thumb "gui/slider/horizontal_hover_thumb.png"
#    thumb Frame("gui/scrollbar/vertical_poem_thumb_d.png", left=6, top=6, tile=True)
#    bar_vertical True
#    bar_invert True

#START: image definitions

image ctc:
    "gui/ctc.png"
    xalign 0.81 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat

image ctc_dark:
    "gui/ctc.png"
    xalign 1.10 yalign 0.98 xoffset -5 alpha 0.0 subpixel True
    block:
        easeout 0.75 alpha 1.0 xoffset 0
        easein 0.75 alpha 0.5 xoffset -5
        repeat

image menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_move

image menu_bg_d:
    topleft
    "gui/menu_bg_d.png"
    menu_bg_move

image game_menu_bg:
    topleft
    "gui/menu_bg.png"
    menu_bg_loop

image game_menu_bg_d:
    topleft
    "gui/menu_bg_d.png"
    menu_bg_loop

image menu_nav:
    "gui/overlay/main_menu.png"
    menu_nav_move

image menu_nav_d:
    "gui/overlay/main_menu_d.png"
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
define gui.scrollable_menu_button_dark_text_idle_color = "#e670af"
define gui.scrollable_menu_button_dark_text_hover_color = "#ffcce8"

define gui.hkb_dark_button_width = 120
define gui.hkb_dark_button_height = None
define gui.hkb_dark_button_tile = False
#define gui.hkb_button_borders = Borders(0, 5, 0, 5)
define gui.hkb_dark_button_text_font = gui.default_font
define gui.hkb_dark_button_text_size = gui.text_size
define gui.hkb_dark_button_text_xalign = 0.5
#define gui.hkb_button_text_xanchor = 0.5
define gui.hkb_dark_button_text_idle_color = "#e670af"
define gui.hkb_dark_button_text_hover_color = "#ffcce8"
define gui.hkb_dark_button_text_kerning = 0.2

define gui.choice_dark_button_width = 420
define gui.choice_dark_button_height = None
define gui.choice_dark_button_tile = False
define gui.choice_dark_button_borders = Borders(100, 5, 100, 5)
define gui.choice_dark_button_text_font = gui.default_font
define gui.choice_dark_button_text_size = gui.text_size
define gui.choice_dark_button_text_xalign = 0.5
define gui.choice_dark_button_text_idle_color = "#e670af"
define gui.choice_dark_button_text_hover_color = "#ffcce8"

define gui.scrollable_menu_dark_button_width = 560
define gui.scrollable_menu_dark_button_height = None
define gui.scrollable_menu_dark_button_tile = False
define gui.scrollable_menu_dark_button_borders = Borders(25, 5, 25, 5)
define gui.scrollable_menu_dark_button_text_font = gui.default_font
define gui.scrollable_menu_dark_button_text_size = gui.text_size
define gui.scrollable_menu_dark_button_text_xalign = 0.0
define gui.scrollable_menu_dark_button_text_idle_color = "#e670af"
define gui.scrollable_menu_dark_button_text_hover_color = "#ffcce8"

define gui.twopane_scrollable_menu_dark_button_width = 250
define gui.twopane_scrollable_menu_dark_button_height = None
define gui.twopane_scrollable_menu_dark_button_tile = False
define gui.twopane_scrollable_menu_dark_button_borders = Borders(25, 5, 25, 5)
define gui.twopane_scrollable_menu_dark_button_text_font = gui.default_font
define gui.twopane_scrollable_menu_dark_button_text_size = gui.text_size
define gui.twopane_scrollable_menu_dark_button_text_xalign = 0.0
define gui.twopane_scrollable_menu_dark_button_text_idle_color = "#e670af"
define gui.twopane_scrollable_menu_dark_button_text_hover_color = "#ffcce8"

define gui.island_button_dark_height = None
define gui.island_button_dark_width = 205
define gui.island_button_dark_tile = False
define gui.island_button_dark_text_font = gui.default_font
define gui.island_button_dark_text_size = gui.text_size
define gui.island_button_dark_text_xalign = 0.5
define gui.island_button_dark_text_idle_color = "#e670af"
define gui.island_button_dark_text_hover_color = "#ffcce8"
define gui.island_button_dark_text_kerning = 0.2

define gui.quick_button_dark_text_height = None
define gui.quick_button_dark_text_width = 205
define gui.quick_button_dark_text_tile = False
define gui.quick_button_dark_text_font = gui.default_font
define gui.quick_button_dark_text_size = 14
define gui.quick_button_dark_text_xalign = 0.5
define gui.quick_button_dark_text_yalign = 0.995
define gui.quick_button_dark_text_idle_color = "#F2A4F1"
define gui.quick_button_dark_text_hover_color = "#FFDEFE"
define gui.quick_button_dark_text_kerning = 0.2

#define gui.slider_dark_size = 30
#define gui.slider_dark_tile = False
#define gui.slider_dark_borders = Borders(4, 4, 4, 4)
#define gui.vslider_dark_borders = Borders(4, 4, 4, 4)
#define gui.vscrollbar_dark_borders = Borders(4, 4, 4, 4)

#define gui.bar_dark_size = 36
#define gui.scrollbar_dark_size = 12
#define gui.slider_dark_size = 30
#define gui.bar_dark_tile = False
#define gui.scrollbar_dark_tile = False
#define gui.slider_dark_tile = False
#define gui.bar_dark_borders = Borders(4, 4, 4, 4)
#define gui.scrollbar_dark_borders = Borders(4, 4, 4, 4)
#define gui.slider_dark_borders = Borders(4, 4, 4, 4)
#define gui.vbar_dark_borders = Borders(4, 4, 4, 4)
##define gui.vscrollbar_dark_borders = Borders(4, 4, 4, 4)
#define gui.vslider_dark_borders = Borders(4, 4, 4, 4)
#define gui.unscrollable_dark = "hide"


#START: screen overrides

init offset = 1

screen hkb_overlay():

    zorder 50
    style_prefix ("hkb" if not mas_globals.dark_mode else "hkb_dark")

    vbox:
        xpos 0.05
#        xalign 0.05
        yanchor 1.0
        ypos 715
#        yalign 0.95

        if store.hkb_button.talk_enabled:
            textbutton _("Talk") action Function(show_dialogue_box) style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
        else:
            frame:
                ypadding 5
                xsize 120

                background Image(mas_getTimeFile("mod_assets/hkb_disabled_background.png"))
                text "Talk"


        if store.hkb_button.extra_enabled:
            textbutton _("Extra") action Function(mas_open_extra_menu) style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
        else:
            frame:
                ypadding 5
                xsize 120

                background Image(mas_getTimeFile("mod_assets/hkb_disabled_background.png"))
                text "Extra"


        if store.hkb_button.music_enabled:
            textbutton _("Music") action Function(select_music) style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
        else:
            frame:
                ypadding 5
                xsize 120

                background Image(mas_getTimeFile("mod_assets/hkb_disabled_background.png"))
                text "Music"

        if store.hkb_button.play_enabled:
            textbutton _("Play") action Function(pick_game) style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
        else:
            frame:
                ypadding 5
                xsize 120

                background Image(mas_getTimeFile("mod_assets/hkb_disabled_background.png"))
                text "Play"

screen mas_extramenu_area():
    zorder 52

    key "e" action Jump("mas_extra_menu_close")
    key "E" action Jump("mas_extra_menu_close")

    frame:
        area (0, 0, 1280, 720)
        background Solid("#0000007F")
        # close button
        textbutton _("Close"):
            area (61, 594, 120, 35)
            style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
            action Jump("mas_extra_menu_close")
        # zoom control
        frame:
            area (195, 450, 80, 255)
            background Frame(mas_getTimeFile("mod_assets/frames/trans_pink2pxborder100.png"), left=((Borders(2, 2, 2, 2, pad_top=2, pad_bottom=4)) if not mas_globals.dark_mode else Borders(3, 3, 3, 3, pad_top=2, pad_bottom=4)))
            vbox:
                spacing (2 if not mas_globals.dark_mode else 3)
                label "Zoom":
                    style ("hkb_button_text" if not mas_globals.dark_mode else "hkb_dark_button_text")
                # resets the zoom value back to default
                textbutton _("Reset"):
                    style "mas_adjustable_button"
                    xsize 72
                    ysize (35 if not mas_globals.dark_mode else 40)
                    xalign 0.3
                    action SetField(store.mas_sprites, "zoom_level", store.mas_sprites.default_zoom_level)
                # actual slider for adjusting zoom
                bar value FieldValue(store.mas_sprites, "zoom_level", store.mas_sprites.max_zoom):
                    style "mas_adjust_vbar"
                    xalign 0.5
                $ store.mas_sprites.adjust_zoom()

screen say(who, what):
    style_prefix "say"

    window:
        id "window"

        text what id "what"

        if who is not None:

            window:
                style "namebox"
                text who id "who"

    # If there's a side image, display it above the text. Do not display
    # on the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign (0.0 if not mas_globals.dark_mode else 2.5) yalign (1.0 if not mas_globals.dark_mode else 2.5)

    use quick_menu


screen updater:

    modal True

    style_prefix "updater"

    frame:

        has side "t c b":
            spacing gui._scale(10)

        label _("Updater")

        fixed:

            vbox:

                if u.state == u.ERROR:
                    text _("An error has occured:")
                elif u.state == u.CHECKING:
                    text _("Checking for updates.")
                elif u.state == u.UPDATE_AVAILABLE:
                    text _("Version [u.version] is available. Do you want to install it?")

                elif u.state == u.UPDATE_NOT_AVAILABLE:
                    text _("Monika After Story is up to date.")
                elif u.state == u.PREPARING:
                    text _("Preparing to download the updates.")
                elif u.state == u.DOWNLOADING:
                    text _("Downloading the updates. (Progress bar may not advance during download)")
                elif u.state == u.UNPACKING:
                    text _("Unpacking the updates.")
                elif u.state == u.FINISHING:
                    text _("Finishing up.")
                elif u.state == u.DONE:
                    text _("The updates have been installed. Please reopen Monika After Story.")
                elif u.state == u.DONE_NO_RESTART:
                    text _("The updates have been installed.")
                elif u.state == u.CANCELLED:
                    text _("The updates were cancelled.")

                if u.message is not None:
                    null height gui._scale(10)
                    text "[u.message!q]"

                if u.progress is not None:
                    null height gui._scale(10)
                    bar value u.progress range 1.0 left_bar Solid("#cc6699") right_bar Solid("#ffffff" if not mas_globals.dark_mode else "#13060d") thumb None

        hbox:

            spacing gui._scale(25)

            if u.can_proceed:
                textbutton _("Proceed") action u.proceed

            if u.can_cancel:
                textbutton _("Cancel") action Return()

screen name_input(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    key "K_RETURN" action [Play("sound", gui.activate_sound), ok_action]

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            input default "" value VariableInputValue("player") length 12 allow "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen dialog(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("OK") action ok_action

screen quit_dialog(message, ok_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("QUIT") action ok_action

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            if in_sayori_kill and message == layout.QUIT:
                add "confirm_glitch" xalign 0.5

            else:
                label _(message):
                    style "confirm_prompt"
                    xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                if mas_finalfarewell_mode:
                    textbutton _("-") action yes_action
                    textbutton _("-") action yes_action
                else:
                    textbutton _("Yes") action [SetField(persistent, "_mas_game_crashed", False), Show(screen="quit_dialog", message=layout.QUIT_YES, ok_action=yes_action)]
                    textbutton _("No") action no_action, Show(screen="dialog", message=layout.QUIT_NO, ok_action=Hide("dialog"))

screen update_check(ok_action,cancel_action,mode):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "update_check"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            if mode == 0:
                label _('An update is now avalable!'):
                    style "confirm_prompt"
                    xalign 0.5

            elif mode == 1:
                label _("No update available."):
                    style "confirm_prompt"
                    xalign 0.5

            elif mode == 2:
                label _('Checking for updates...'):
                    style "confirm_prompt"
                    xalign 0.5
            else:
                # otherwise, we assume a timeout
                label _('Timeout occured while checking for updates. Try again later.'):
                    style "confirm_prompt"
                    xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Install") action [ok_action, SensitiveIf(mode == 0)]

                textbutton _("Cancel") action cancel_action

    timer 1.0 action Return("None")

screen mas_generic_restart:
    # this will always return True
    # this has like a be right back button

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

screen mas_chess_confirm():

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Are you sure you want to give up?"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action Return(True)
                textbutton _("No") action Return(False)

screen mas_gmenu_confirm(sel_rend):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Switch renderer to " + sel_rend + "?"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action Return(True)
                textbutton _("No") action Return(False)

#START: Selector override
screen mas_selector_sidebar(items, mailbox, confirm, cancel, remover=None):
    zorder 50
#    modal True

    frame:
        area (1075, 5, 200, 625)
        background Frame(mas_getTimeFile("mod_assets/frames/black70_pinkborder100_5px.png"), left=6, top=6, tile=True)

        vbox:
            xsize 200
            xalign 0.5
            viewport id "sidebar_scroll":
                mousewheel True
                arrowkeys True

                vbox:
                    xsize 200
                    spacing 10
                    null height 1

                    # add the remover
                    if remover is not None:
                        add remover:
                            xalign 0.5

                    for selectable in items:
                        add selectable:
#                            xoffset 5
                            xalign 0.5

                    null height 1

            null height 10

            if mailbox.read_conf_enable():
                textbutton _("Confirm"):
                    style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
                    xalign 0.5
                    action Jump(confirm)
            else:
                frame:
                    ypadding 5
                    xsize 120
                    xalign 0.5

                    background Image(mas_getTimeFile("mod_assets/hkb_disabled_background.png"))
                    text "Confirm" style ("hkb_text" if not mas_globals.dark_mode else "hkb_dark_text")

            textbutton _("Cancel"):
                style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
                xalign 0.5
                action Jump(cancel)
#                action Function(mailbox.mas_send_return, -1)

        vbar value YScrollValue("sidebar_scroll"):
            style "mas_selector_sidebar_vbar"
            xoffset -25

screen navigation():

    vbox:
        style_prefix ("navigation" if not mas_globals.dark_mode else "navigation_dark")

        xpos gui.navigation_xpos
        yalign 0.8

        spacing gui.navigation_spacing


        if main_menu:

            textbutton _("Just Monika") action If(persistent.playername, true=Start(), false=Show(screen="name_input", message="Please enter your name", ok_action=Function(FinishEnterName)))

        else:

            textbutton _("History") action [ShowMenu("history"), SensitiveIf(renpy.get_screen("history") == None)]

            textbutton _("Save Game") action [ShowMenu("save"), SensitiveIf(renpy.get_screen("save") == None)]

        textbutton _("Load Game") action [ShowMenu("load"), SensitiveIf(renpy.get_screen("load") == None)]

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:
            textbutton _("Main Menu") action NullAction(), Show(screen="dialog", message="No need to go back there.\nYou'll just end up back here so don't worry.", ok_action=Hide("dialog"))

        textbutton _("Settings") action [ShowMenu("preferences"), SensitiveIf(renpy.get_screen("preferences") == None)]

        if store.mas_windowreacts.can_show_notifs and not main_menu:
            textbutton _("Alerts") action [ShowMenu("notif_settings"), SensitiveIf(renpy.get_screen("notif_settings") == None)]

        #textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc"):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action Help("README.html")

            ## The quit button is banned on iOS and unnecessary on Android.
            textbutton _("Quit") action Quit(confirm=_confirm_quit)


screen twopane_scrollable_menu(prev_items, main_items, left_area, left_align, right_area, right_align, cat_length):

        style_prefix ("twopane_scrollable_menu" if not mas_globals.dark_mode else "twopane_scrollable_menu_dark")

        fixed:
            area left_area

            bar adjustment prev_adj style "vscrollbar" xalign left_align

            viewport:
                yadjustment prev_adj
                mousewheel True
                arrowkeys True

                vbox:

                    for i_caption,i_label in prev_items:
                        textbutton i_caption:
                            if renpy.has_label(i_label) and not seen_event(i_label):
                                style ("twopane_scrollable_menu_new_button" if not mas_globals.dark_mode else "twopane_scrollable_menu_dark_new_button")
                            if not renpy.has_label(i_label):
                                style ("twopane_scrollable_menu_special_button" if not mas_globals.dark_mode else "twopane_scrollable_menu_dark_special_button")

                            action Return(i_label)



                    null height 20

                    if cat_length == 0:
                        textbutton _("That's enough for now.") action Return(False)
                    elif cat_length > 1:
                        textbutton _("Go Back") action Return(-1)


        if main_items:

            fixed:
                area right_area

                bar adjustment main_adj style "vscrollbar" xalign right_align

                viewport:
                    yadjustment main_adj
                    mousewheel True
                    arrowkeys True

                    vbox:

                        for i_caption,i_label in main_items:
                            textbutton i_caption:
                                if renpy.has_label(i_label) and not seen_event(i_label):
                                    style ("twopane_scrollable_menu_new_button" if not mas_globals.dark_mode else "twopane_scrollable_menu_dark_new_button")
                                if not renpy.has_label(i_label):
                                    style ("twopane_scrollable_menu_special_button" if not mas_globals.dark_mode else "twopane_scrollable_menu_dark_special_button")

                                action Return(i_label)

                        null height 20

                        textbutton _("That's enough for now.") action Return(False)

screen mas_gen_scrollable_menu(items, display_area, scroll_align, *args):

        style_prefix ("scrollable_menu" if not mas_globals.dark_mode else "scrollable_menu_dark")

        fixed:
            area display_area

            bar adjustment prev_adj style "vscrollbar" xalign scroll_align

            viewport:
                yadjustment prev_adj
                mousewheel True

                vbox:
#                    xpos x
#                    ypos y

                    for item_prompt,item_value,is_italic,is_bold in items:
                        textbutton item_prompt:
                            if is_italic and is_bold:
                                style ("scrollable_menu_crazy_button" if not mas_globals.dark_mode else "scrollable_menu_dark_crazy_button")
                            elif is_italic:
                                style ("scrollable_menu_new_button" if not mas_globals.dark_mode else "scrollable_menu_dark_new_button")
                            elif is_bold:
                                style ("scrollable_menu_special_button" if not mas_globals.dark_mode else "scrollable_menu_dark_special_button")
                            action Return(item_value)

                    for final_items in args:
                        if final_items[4] > 0:
                            null height final_items[4]

                        textbutton _(final_items[0]):
                            if final_items[2] and final_items[3]:
                                style ("scrollable_menu_crazy_button" if not mas_globals.dark_mode else "scrollable_menu_dark_crazy_button")
                            elif final_items[2]:
                                style ("scrollable_menu_new_button" if not mas_globals.dark_mode else "scrollable_menu_dark_new_button")
                            elif final_items[3]:
                                style ("scrollable_menu_special_button" if not mas_globals.dark_mode else "scrollable_menu_dark_special_button")
                            action Return(final_items[1])

screen scrollable_menu(items, display_area, scroll_align, nvm_text, remove=None):

        style_prefix ("scrollable_menu" if not mas_globals.dark_mode else "scrollable_menu_dark")

        fixed:
            area display_area

            bar adjustment prev_adj style "vscrollbar" xalign scroll_align

            viewport:
                yadjustment prev_adj
                mousewheel True

                vbox:
#                    xpos x
#                    ypos y

                    for i_caption,i_label in items:
                        textbutton i_caption:
                            if renpy.has_label(i_label) and not seen_event(i_label):
                                style ("scrollable_menu_new_button" if not mas_globals.dark_mode else "scrollable_menu_dark_new_button")
                            if not renpy.has_label(i_label):
                                style ("scrollable_menu_special_button" if not mas_globals.dark_mode else "scrollable_menu_dark_special_button")
                            action Return(i_label)



                    null height 20

                    if remove:
                        # in case we want the option to hide this menu
                        textbutton _(remove[0]) action Return(remove[1])

                    textbutton _(nvm_text) action Return(False)

screen mas_calendar_events_scrollable_list(items, display_area, scroll_align, first_item=None, final_item=None, mask="#000000B2", frame="mod_assets/calendar/calendar_bg.png"):

        style_prefix ("scrollable_menu" if not mas_globals.dark_mode else "scrollable_menu_dark")

        zorder 51

        if mask:
            add Solid(mask)

        fixed:
            area display_area
            if frame:
                add Frame(frame, 60, 60)

            bar adjustment prev_adj style "vscrollbar" xalign scroll_align

            viewport:
                yadjustment prev_adj
                mousewheel True

                vbox:

                    if first_item:

                        text _(first_item[0]):
                            if first_item[1]:
                                italic True
                            if first_item[2]:
                                bold True
                            xpos 0.2
                            ypos 0.5

                    null height 30


                    for item_prompt,is_italic,is_bold in items:
                        text item_prompt:
                            if is_italic:
                                italic True
                            if is_bold:
                                bold True
                            xpos 0.05


                    if final_item:
                        if final_item[4] > 0:
                            null height final_item[4]

                        textbutton _(final_item[0]):
                            if final_item[2]:
                                text_italic True
                            if final_item[3]:
                                text_bold True
                            background None
                            hover_sound gui.hover_sound
                            activate_sound gui.activate_sound

                            action Return(final_item[1])

screen choice(items):
    style_prefix ("choice" if not mas_globals.dark_mode else "choice_dark")

    vbox:
        for i in items:
            textbutton i.caption action i.action

screen rigged_choice(items):
    style_prefix ("choice" if not mas_globals.dark_mode else "choice_dark")

    vbox:
        for i in items:
            textbutton i.caption action i.action

    timer 1.0/30.0 repeat True action Function(RigMouse)

screen talk_choice(items):
    style_prefix ("talk_choice" if not mas_globals.dark_mode else "talk_choice_dark")

    vbox:
        for i in items:
            textbutton i.caption action i.action

screen game_menu(title, scroll=None):

    # when teh game menu is open, we should disable the hotkeys
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()

    # Add the backgrounds.
    if main_menu:
        add gui.main_menu_background
    else:
        key "mouseup_3" action Return()
        add gui.game_menu_background

    style_prefix "game_menu"

    frame:
        style "game_menu_outer_frame"

        hbox:

            # Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 1.0

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial 1.0

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    # if not main_menu and not persistent.menu_bg_m and renpy.random.randint(0, 49) == 0:
    #     on "show" action Show("game_menu_m")

    textbutton _("Return"):
        style ("return_button" if not mas_globals.dark_mode else "return_dark_button")

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


#START: Helper method(s)
init 5 python:
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

#START: THE OOFERIDE
init python:
    ## custom displayable
    class MASSelectableImageButtonDisplayable(renpy.Displayable):
        """
        Custom button for the selectable items.
        """
        import pygame
        from store.mas_selspr import MB_DISP

        # constnats
        THUMB_DIR = "mod_assets/thumbs/"

        WIDTH = 180 # default width
        TX_WIDTH = 170 # width of the text object

        # technically this should change.
        TOTAL_HEIGHT = 218
        SELECTOR_HEIGHT = 180

        # this is the default, but the real may change using the expanding
        # frame properties.
        TOP_FRAME_HEIGHT = 38 # default
        TOP_FRAME_TEXT_HEIGHT = 35 # part of the top frame where text should be
        TOP_FRAME_CHUNK = 35 # each text chunk should consist of 35px
        TOP_FRAME_SPACER = 5 # pixels between each text chunk line

        # mouse stuff
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP
        )
        MOUSE_WHEEL = (4, 5)


        def __init__(self,
                _selectable,
                select_map,
                viewport_bounds,
                mailbox={},
                multi_select=False
            ):
            """
            Constructor for this displayable

            IN:
                selectable - the selectable object we want to encapsulate
                select_map - dict containing group keys of previously selected
                    objects.
                viewport_bounds - tuple of the following format:
                    [0]: xpos of the viewport upper left
                    [1]: ypos of the viewport upper left
                    [2]: width of the viewport
                    [3]: height of the viewport
                    [4]: border size
                mailbox - dict to send messages to outside from this
                    displayable.
                    (Default: {})
                multi_select - True means we can select more than one item.
                    False otherwise
                    (Default: False)
            """
            super(MASSelectableImageButtonDisplayable, self).__init__()

            self.selectable = _selectable
            self.select_map = select_map
            self.mailbox = mailbox
            self.multi_select = multi_select
            self.been_selected = False

            # if this is a remover, we don't use the thumb
            if self.selectable.remover:
                thumb_path = self.THUMB_DIR + "remove.png"

            else:
                # as a precaution, if a thumb doesn't exist, we use a
                # placeholder.
                thumb_path = self.THUMB_DIR + _selectable.thumb
                if not renpy.loadable(thumb_path):
                    thumb_path = self.THUMB_DIR + "unknown.png"

            self.thumb = Image(thumb_path)

            # image setups
            self.thumb_overlay = Image(
                mas_getTimeFile("mod_assets/frames/selector_overlay.png")
            )
            self.thumb_overlay_locked = Image(
                mas_getTimeFile("mod_assets/frames/selector_overlay_disabled.png")
            )
            self.top_frame = Frame(
                mas_getTimeFile("mod_assets/frames/selector_top_frame.png"),
                left=4,
                top=4,
                tile=True
            )
            self.top_frame_selected = Frame(
                mas_getTimeFile("mod_assets/frames/selector_top_frame_selected.png"),
                left=4,
                top=4,
                tile=True
            )
            self.top_frame_locked = Frame(
                mas_getTimeFile("mod_assets/frames/selector_top_frame_disabled.png"),
                left=4,
                top=4,
                tile=True
            )

            # renpy solids and stuff
            self.hover_overlay = Solid("#ffaa99aa" if not mas_globals.dark_mode else "#ffaa99aa")

            # text objects
            # NOTE: we build these on first render
            self.item_name = None
            self.item_name_hover = None
#            self.item_name = self._display_name(False, self.selectable.display_name)
#            self.item_name_hover = self._display_name(True, self.selectable.display_name)

            # setup viewport bound values
            vpx, vpy, vpw, vph, vpb = viewport_bounds
            self.xlim_lo = vpx + vpb
            self.xlim_up = (vpx + vpw) - vpb
            self.ylim_lo = vpy + vpb
            self.ylim_up = (vpy + vph) - vpb

            # flags
            self.hovered = False
            self.hover_jumped = False # True means we just jumped to label

            # these get changed
            self.hover_width = self.WIDTH
            self.hover_height = self.TOTAL_HEIGHT

            self.selected = False
            self.select_jump = False

            self.first_render = True

            # when True, we make a call to end the interaction after reaching
            # the end of event.
            self.end_interaction = False

            # top frame sizes
            self.top_frame_height = self.TOP_FRAME_HEIGHT

            # cached renders
            self.render_cache = {}

            # locked mode
            self.locked = not self.selectable.unlocked
            self.locked_thumb = Image("mod_assets/thumbs/locked.png")


        def _blit_bottom_frame(self, r, _renders):
            """
            bliting the bottom frames

            IN:
                r - render to blit to
                _renders - list of bottom renders to blit
            """
            for _render in _renders:
                r.blit(_render, (0, self.top_frame_height))


        def _blit_top_frame(self, r, _renders, _disp_name):
            """
            bliting the top frames

            IN:
                r - render to blit to
                _renders - list of top renders to blit
                _disp_name - list of display name renders to blit
            """
            for _render in _renders:
                r.blit(_render, (0, 0))

            # text
            line_index = 1
            for line in _disp_name:
                r.blit(
                    line,
                    (
                        5,
                        (line_index * self.TOP_FRAME_CHUNK)
                        - line.get_size()[1]
                    )
                )
                line_index += 1


        def _check_display_name(self, _display_name_text, st, at):
            """
            Checks the given display name to see if it fits within the frame
            bounds. We will have to adjust if not

            IN:
                _display_name_text - display name as text

            RETURNS:
                the rendered display name rendre if it fits, None if not.
            """
            # render the text object we want to test
            _disp_text = self._display_name(False, _display_name_text)
            _render = renpy.render(
                _disp_text,
                1000,
                self.TOP_FRAME_CHUNK,
                st,
                at
            )
            dtw, dth = _render.get_size()

            # check width
            if dtw > self.TX_WIDTH:
                return None

            return _render


        def _check_render_split(self, line, lines_list, st, at):
            """
            Checks the given line to see if it fits within a line render.

            NOTE: adds hypen and multiple lines if the line is too long

            IN:
                line - the line we want to check for render
                lines_list - list to add lines to
                st - st for renpy render
                at - at for renpy render

            OUT:
                lines_list - list with lines added
            """
            _render = self._check_display_name(line, st, at)
            if not _render:
                self._hypen_render_split(line, lines_list, st, at)

            else:
                self.item_name.append(_render)
                lines_list.append(line)


        def _display_name(self, selected, _text):
            """
            Returns the text object for the display name.

            IN:
                selected - True if selected, False if not
                _text - actual text to convert into display name obj

            RETURNS:
                the text object for the display name
            """
            #if not mas_globals.dark_mode:
            if selected:
                color = ("#fa9" if not mas_globals.dark_mode else "#ffaa99")
            else:
                color = ("#000" if not mas_globals.dark_mode else "#e670af")

            #else:
            #    if selected:
            #        color = "#ffaa99"
            #    else:
            #        color = "#e670af"

            return Text(
                _text,
                font=gui.default_font,
                size=gui.text_size,
                color=color,
                outlines=[]
            )


        def _hover(self):
            """
            Does hover actions, which include playing hover sound and sending
            hover msg if appropriate
            """
            if not self.hovered:
                self.hover_jumped = False

            elif not self.hover_jumped:
                # first time hovering
                self.hover_jumped = True

                # play hover sound
                renpy.play(gui.hover_sound, channel="sound")

                # send out hover dlg
                if self.selectable.hover_dlg is not None:
                    self._send_hover_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

                # always reset on a hover
                self.end_interaction = True


        def _hypen_render_split(self, line, lines_list, st, at, tokens=None):
            """
            Splits a line via hypen.

            We do a reverse through the string to find appropriate render
            sizes.

            NOTE: we add renders to self.item_name

            IN:
                line - line to split
                lines_list - list to add lines to
                st - st for renpy render
                at - at for renpy render
                tokens - current list of tokens, if we are in the token mode.
                    Insert the leftover token word at position 1.
                    (Default: None)

            OUT:
                lines_list - list with lines added
            """
            # NOTE: we do reverse because it is more likely that text is
            #   just barely too large, than dealing with one huge string.
            index = len(line)-2
            while index >= 0:
                # split and add hypen
                line1 = line[:index] + "-"

                # check the render
                _l1_render = self._check_display_name(line1, st, at)
                if _l1_render:
                    # add line 1
                    self.item_name.append(_l1_render)
                    lines_list.append(line1)

                    # recurse 2nd line
                    line2 = line[index:]
                    if tokens is not None:
                        tokens.insert(1, line2)
                    else:
                        self._check_render_split(line2, lines_list, st, at)
                    return

                # doesnt fit, decreaes index and continue
                index -= 1


        def _is_over_me(self, x, y):
            """
            Returns True if the given x, y is over us.
            This also handles if the mouse is past the viewport bounds.

            IN:
                x - x coord relative to upper left of this displayable
                y - y coord relative to upper left of this displayable
            """
            mouse_x, mouse_y = renpy.get_mouse_pos()
            return (
                self.xlim_lo <= mouse_x <= self.xlim_up
                and self.ylim_lo <= mouse_y <= self.ylim_up
                and 0 <= x <= self.hover_width
                and 0 <= y <= self.hover_height
            )


        def _rand_select_dlg(self, dlg_list):
            """
            Randomly selects dialogue from the given list

            IN:
                dlg_list - list to select from

            ASSUMES the list is not empty
            """
            return dlg_list[random.randint(0, len(dlg_list)-1)]


        def _render_bottom_frame(self, hover, st, at):
            """
            Renders the bottom frames, returns a list of the renders in order
            of bliting.

            IN:
                hover - True means we are hovering (or are selected), false
                    otherwise

            RETURNS:
                list of renders, in correct blit order
            """
            _renders = [
                self._render_bottom_frame_piece(self.thumb, st, at),
                self._render_bottom_frame_piece(self.thumb_overlay, st, at)
            ]

            if hover:
                _renders.append(
                    self._render_bottom_frame_piece(self.hover_overlay, st, at)
                )

            return _renders


        def _render_bottom_frame_piece(self, piece, st, at):
            """
            Renders a single bottom frame piece and returns it
            """
            return renpy.render(
                piece,
                self.WIDTH,
                self.SELECTOR_HEIGHT,
                st,
                at
            )


        def _render_display_name(self, hover, _text, st, at):
            """
            Renders display name

            IN:
                hover - True if selected, False if not
                _text - actual text to render
                st - st for renpy render
                at - at for renpy render

            """
            return renpy.render(
                self._display_name(hover, _text),
                self.WIDTH,
                self.TOP_FRAME_CHUNK,
                st,
                at
            )


        def _render_top_frame(self, hover, st, at):
            """
            Renders the top renders, returns a list of the renders in order of
            bliting.

            IN:
                hover - True means we are hovering (or are selected

            RETURNS:
                list of renders, in correct blit order
            """
            if hover:
                _main_piece = self._render_top_frame_piece(
                    self.top_frame_selected,
                    st,
                    at
                )

            else:
                _main_piece = self._render_top_frame_piece(
                    self.top_frame,
                    st,
                    at
                )

            return [_main_piece]


        def _render_top_frame_piece(self, piece, st, at):
            """
            Renders a top frame piece. No Text, please
            """
            return renpy.render(
                piece,
                self.WIDTH,
                self.top_frame_height,
                st,
                at
            )


        def _select(self):
            """
            Makes this item a selected item. Also handles other logic realted
            to selecting this.
            """
            # if already selected, then we need to deselect.
            if self.selected:
                # TODO: this actually can break things if we dselect
                #   probably should handle this a smarter way like if
                #   something was selected originally, dont make it possible
                #   to deselect.
                #   or make it select what was originally selected.
                # deselect self
#                self.selected = False
#                renpy.redraw(self, 0)

                # end interaction so display text is rest
#                self.end_interaction = True
                return

            # TODO: should be moved to the top when deselect can happen
            # play the select sound
            renpy.play(gui.activate_sound, channel="sound")

            # otherwise select self
            self.selected = True

            if not self.multi_select:
                # must clean select map
                for item in self.select_map.itervalues():
                    # setting to False will queue for removal of item
                    # NOTE: the caller must handle teh removal
                    item.selected = False
                    renpy.redraw(item, 0)

            # add this item to the select map
            self.select_map[self.selectable.name] = self

            # the appropriate dialogue
            if self.been_selected:
                if self.selectable.select_dlg is not None:
                    self._send_select_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

            else:
                # not been selected before
                self.been_selected = True
                if self.selectable.first_select_dlg is not None:
                    self._send_first_select_text()

                elif self.selectable.select_dlg is not None:
                    self._send_select_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

            # always reset interaction if something has been selected
            self.end_interaction = True


        def _send_first_select_text(self):
            """
            Sends first select text to mailbox

            ASSUMES first select text exists
            """
            self._send_msg_disp_text(
                self._rand_select_dlg(
                    self.selectable.first_select_dlg
                )
            )


        def _send_hover_text(self):
            """
            Sends hover text to mailbox

            ASSUMES hover text exists
            """
            self._send_msg_disp_text(
                self._rand_select_dlg(
                    self.selectable.hover_dlg
                )
            )


        def _send_msg_disp_text(self, msg):
            """
            Sends text message to mailbox.

            IN:
                msg - text message to send
            """
            self.mailbox.send_disp_text(msg)


        def _send_select_text(self):
            """
            Sends the select text to mailbox

            ASSUMES select text exists
            """
            self._send_msg_disp_text(
                self._rand_select_dlg(
                    self.selectable.select_dlg
                )
            )


        def _setup_display_name(self, st, at):
            """
            Sets up item_name and item_name_hover with list of renders, ready
            for bliting.

            IN:
                st - st for renpy render
                at - at for renpy render
            """
            # lets initially check if the pure text renders nicely
            _render = self._check_display_name(
                self.selectable.display_name,
                st,
                at
            )

            if _render:
                self.item_name = [_render]
                self.item_name_hover = [
                    self._render_display_name(
                        True,
                        self.selectable.display_name,
                        st,
                        at
                    )
                ]
                return

            # if we got a None, the text is too long.
            # prepare item_name for renders
            self.item_name = []
            _lines = self._split_render(self.selectable.display_name, st, at)

            # render the hover variants
            # and calculate total height
#            top_height = 0
            self.item_name_hover = [
                self._render_display_name(True, line, st, at)
                for line in _lines
            ]
#            top_height += (_render.get_size()[1] + self.TOP_FRAME_SPACER)

            # now setup the new frame size
            self.top_frame_height = (
                (self.TOP_FRAME_CHUNK * len(self.item_name_hover))
            )


        def _split_render(self, disp_name, st, at):
            """
            Attempts to split the displayname, then checks renders for it
            to see if it fits within the bounds.

            NOTE: this will add renders to self.item_name

            IN:
                disp_name - display name to split
                st - st for renpy render
                at - at for renpy render

            RETURNS:
                list of string lines that fit when rendered.
            """
            _tokens = disp_name.split()
            _lines = []

            self._split_render_tokens(_tokens, _lines, st, at)

            return _lines


        def _split_render_tokens(self, tokens, lines_list, st, at, loop=False):
            """
            Token version of _split_render

            IN:
                tokens - tokens to handle with
                lines_list - list of string lines that we rendered
                st - st for renpy render
                at - at for renpy render
                loop - True if we are recursively calling this.
                    (Default: False)
            """
            # sanity check
            if len(tokens) == 0:
                return

            if len(tokens) > 2 or loop:
                self._token_render_split(tokens, lines_list, st, at)

            elif len(tokens) <= 1:
                self._hypen_render_split(tokens[0], lines_list, st, at)

            else:
                # otherwise, we can just use the 2 splits
                self._check_render_split(tokens[0], lines_list, st, at)
                self._check_render_split(tokens[1], lines_list, st, at)


        def _token_render_split(self, tokens, lines_list, st, at):
            """
            Uses the given tokens to determine best fit render options for
            those tokens.

            NOTE: we also do self.item_name

            IN:
                tokens - list of string tokens to apply best fit
                lines_list - list to add lines to
                st - st for renpy render
                at - at for renpy render

            OUT:
                lines_list - list with lines added
            """
            # reverse order siunce we want to maximize render line size
            index = len(tokens)
            while index > 0:

                # build a string with a number of tokens
                line1 = " ".join(tokens[:index])

                # check the render
                _l1_render = self._check_display_name(line1, st, at)
                if _l1_render:
                    # add line 1
                    self.item_name.append(_l1_render)
                    lines_list.append(line1)

                    # recurse the remaining tokens
                    self._split_render_tokens(
                        tokens[index:],
                        lines_list,
                        st,
                        at,
                        True
                    )
                    return

                # otherwise, lower index
                index -= 1

            # if we got here, then we are dealing with a single token that is
            # too long.
            self._hypen_render_split(tokens[0], lines_list, st, at, tokens)
            self._split_render_tokens(tokens[1:], lines_list, st, at, True)


        def event(self, ev, x, y, st):
            """
            EVENT. We only want to handle 2 cases:
                MOUSEMOTION + hover is over us
                MOUSEDOWN + mouse is over us
            """
            # window event means we need to re-render everything
            if ev.type == pygame.WINDOWEVENT:
                self.first_render = True
                renpy.redraw(self, 0)
                return

            if ev.type in self.MOUSE_EVENTS:

                if ev.type == pygame.MOUSEMOTION:
                    if not self.locked:
                        self.hovered = self._is_over_me(x, y)
                        renpy.redraw(self, 0)

                elif ev.type == pygame.MOUSEBUTTONDOWN:

                    if ev.button in self.MOUSE_WHEEL:
                        # TODO: scrolling in mouse wheel is not perfect,
                        #   the previously hovered item gest hovered instead
                        #   of what we actually want.
                        if not self.locked:
                            self.hovered = self._is_over_me(x, y)
                            renpy.redraw(self, 0)

                    elif ev.button == 1:
                        # left click
                        if not self.locked and self._is_over_me(x, y):
                            self._select()
                            renpy.redraw(self, 0)

#                        elif self.selected and not self.multi_select:
#                            self.selected = False
#                            renpy.redraw(self, 0)

            # apply hover dialogue logic if not selected
            if not self.selected and not self.locked:
                self._hover()

            if self.end_interaction:
                self.end_interaction = False
                renpy.end_interaction(True)


        def render(self, width, height, st, at):
            """
            Render. we want the button here.
            """
            if self.first_render:
                # on first render, we do the rendering.
                # this is so we can just blit later instead of rendering each
                # time.

                # setup the display name
                self._setup_display_name(st, at)

                # now save the render cache
                if self.locked:
                    _locked_bot_renders = [
                        self._render_bottom_frame_piece(
                            self.locked_thumb,
                            st,
                            at
                        ),
                        self._render_bottom_frame_piece(
                            self.thumb_overlay_locked,
                            st,
                            at
                        )
                    ]
                    _locked_top_renders = [
                        self._render_top_frame_piece(
                            self.top_frame_locked,
                            st,
                            at
                        )
                    ]

                    self.render_cache = {
                        "bottom": _locked_bot_renders,
                        "bottom_hover": _locked_bot_renders,
                        "top": _locked_top_renders,
                        "top_hover": _locked_top_renders,
                        "disp_name": self.item_name,
                        "disp_name_hover": self.item_name
                    }

                else:
                    self.render_cache = {
                        "bottom": self._render_bottom_frame(False, st, at),
                        "bottom_hover": self._render_bottom_frame(True, st, at),
                        "top": self._render_top_frame(False, st, at),
                        "top_hover": self._render_top_frame(True, st, at),
                        "disp_name": self.item_name,
                        "disp_name_hover": self.item_name_hover
                    }

                # setup the hiehg tof this displyaable
                self.real_height = self.top_frame_height + self.SELECTOR_HEIGHT
                self.hover_height = self.real_height

                # now that we have cached renders, no need to render again
                self.first_render = False

            # now which renders are we going to select
            if self.locked:
                _suffix = ""
            elif self.hovered or self.selected:
                _suffix = "_hover"
            else:
                _suffix = ""

            _bottom_renders = self.render_cache["bottom" + _suffix]
            _top_renders = self.render_cache["top" + _suffix]
            _disp_name = self.render_cache["disp_name" + _suffix]

            # now blit
            r = renpy.Render(self.WIDTH, self.real_height)
            self._blit_top_frame(r, _top_renders, _disp_name)
            self._blit_bottom_frame(r, _bottom_renders)
            return r
