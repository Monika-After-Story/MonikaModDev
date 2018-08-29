default persistent.monika_reload = 0
default persistent.tried_skip = None
default persistent.monika_kill = True #Assume non-merging players killed monika.
default persistent.rejected_monika = None
default initial_monika_file_check = None
define modoorg.CHANCE = 20
define mas_battery_supported = False

init -1 python in mas_globals:
    # global that are not actually globals.

    # True means we are in the dialogue workflow. False means not
    dlg_workflow = False

init 970 python:
    if persistent._mas_moni_chksum is not None:
        # do check for monika existence
        moni_tuple = store.mas_dockstat.findMonika(
            mas_docking_station
        )

        # set the init data 
        store.mas_dockstat.retmoni_status = moni_tuple[0]
        store.mas_dockstat.retmoni_data = moni_tuple[1]

        del moni_tuple


image mas_island_frame_day = "mod_assets/location/special/with_frame.png"
image mas_island_day = "mod_assets/location/special/without_frame.png"
image mas_island_frame_night = "mod_assets/location/special/night_with_frame.png"
image mas_island_night = "mod_assets/location/special/night_without_frame.png"
image blue_sky = "mod_assets/blue_sky.jpg"
image monika_room = "images/cg/monika/monika_room.png"
image monika_day_room = "mod_assets/monika_day_room.png"
image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"
image chara9 = "mod_assets/chara9.png"
image chara_exception = "mod_assets/chara_exception.png"

image monika_body_glitch1:
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    1.00
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"
    0.15
    "images/cg/monika/monika_glitch1.png"
    0.15
    "images/cg/monika/monika_glitch2.png"

image monika_body_glitch2:
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    1.00
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"
    0.15
    "images/cg/monika/monika_glitch3.png"
    0.15
    "images/cg/monika/monika_glitch4.png"

image ut_slash:
    "mod_assets/spr_slice_o_0.png"
    0.1
    "mod_assets/spr_slice_o_1.png"
    0.1
    "mod_assets/spr_slice_o_2.png"
    0.1
    "mod_assets/spr_slice_o_3.png"
    0.1
    "mod_assets/spr_slice_o_4.png"
    0.1
    "mod_assets/spr_slice_o_5.png"
    0.1


image room_glitch = "images/cg/monika/monika_bg_glitch.png"

image room_mask = Movie(channel="window_1", play="mod_assets/window_1.webm",mask=None,image="mod_assets/window_1_fallback.png")
image room_mask2 = Movie(channel="window_2", play="mod_assets/window_2.webm",mask=None,image="mod_assets/window_2_fallback.png")
image room_mask3 = Movie(channel="window_3", play="mod_assets/window_3.webm",mask=None,image="mod_assets/window_3_fallback.png")
image room_mask4 = Movie(channel="window_4", play="mod_assets/window_4.webm",mask=None,image="mod_assets/window_4_fallback.png")

# big thanks to sebastianN01 for the rain art!
image rain_mask_left = Movie(
    channel="window_5",
    play="mod_assets/window_5.webm",
    mask=None,
    image="mod_assets/window_5_fallback.png"
)
image rain_mask_right = Movie(
    channel="window_6",
    play="mod_assets/window_6.webm",
    mask=None,
    image="mod_assets/window_6_fallback.png"
)

# spaceroom window positions
transform spaceroom_window_left:
    size (320, 180) pos (30, 200)

transform spaceroom_window_right:
    size (320, 180) pos (935, 200)

init python:

    import subprocess
    import os
    import eliza      # mod specific
    import datetime   # mod specific
    import battery    # mod specific
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    import store.mas_globals as mas_globals
    therapist = eliza.eliza()
    process_list = []
    currentuser = None # start if with no currentuser
    if renpy.windows:
        try:
            process_list = subprocess.check_output("wmic process get Description", shell=True).lower().replace("\r", "").replace(" ", "").split("\n")
        except:
            pass
        try:
            for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
                user = os.environ.get(name)
                if user:
                    currentuser = user
        except:
            pass

    try:
        renpy.file("../characters/monika.chr")
        initial_monika_file_check = True
    except:
        #Monika will mention that you don't have a char file in ch30_main instead
        pass


    # name changes if necessary
    if not currentuser or len(currentuser) == 0:
        currentuser = persistent.playername
    if not persistent.mcname or len(persistent.mcname) == 0:
        persistent.mcname = currentuser
        mcname = currentuser
    else:
        mcname = persistent.mcname

    # check for battery support
    mas_battery_supported = battery.is_supported()

    # we need a new music channel for background audio (like rain!)
    renpy.music.register_channel(
        "background",
        mixer="music",
        loop=True,
        stop_on_mute=True,
        tight=True
    )
    renpy.music.set_volume(songs.getVolume("music"), channel="background")

    #Define new functions
    def show_dialogue_box():
        """
        Jumps to the topic promt menu
        """
        renpy.jump('prompt_menu')


    def pick_game():
        """
        Jumps to the pick a game workflow
        """
        renpy.jump('pick_a_game')


    def mas_enable_quitbox():
        """
        Enables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = True


    def mas_disable_quitbox():
        """
        Disables Monika's quit dialogue warning
        """
        global _confirm_quit
        _confirm_quit = False


    def mas_enable_quit():
        """
        Enables quitting without monika knowing
        """
        persistent.closed_self = True
        mas_disable_quitbox()


    def mas_disable_quit():
        """
        Disables quitting without monika knowing
        """
        persistent.closed_self = False
        mas_enable_quitbox()


    def mas_drawSpaceroomMasks():
        """
        Draws the appropriate masks according to the current state of the
        game.

        ASSUMES:
            morning_flag
            mas_is_raining
        """
        if mas_is_raining:
            # raining takes priority
            left_window = "rain_mask_left"
            right_window = "rain_mask_right"

        elif morning_flag:
            # morning time!
            left_window = "room_mask3"
            right_window = "room_mask4"

        else:
            # night time
            left_window = "room_mask"
            right_window = "room_mask2"

        # now show the masks
        renpy.show(left_window, at_list=[spaceroom_window_left], tag="rm")
        renpy.show(right_window, at_list=[spaceroom_window_right], tag="rm2")


    def show_calendar():
        """RUNTIME ONLY
        Opens the calendar if we can
        """
        mas_HKBRaiseShield()

        if not persistent._mas_first_calendar_check:
            renpy.call('_first_time_calendar_use')

        renpy.call_in_new_context("mas_start_calendar_read_only")

        mas_HKBDropShield()


    dismiss_keys = config.keymap['dismiss']
    renpy.config.say_allow_dismiss = store.mas_hotkeys.allowdismiss

    def slow_nodismiss(event, interact=True, **kwargs):
        """
        Callback for whenever monika talks

        IN:
            event - main thing we can use here, lets us now when in the pipeline
                we are for display text:
                begin -> start of a say statement
                show -> right before dialogue is shown
                show_done -> right after dialogue is shown
                slow_done -> called after text finishes showing
                    May happen after "end"
                end -> end of dialogue (user has interacted)
        """
        # skip check
        if config.skipping and not config.developer:
            persistent.tried_skip = True
            config.skipping = False
            config.allow_skipping = False
            renpy.jump("ch30_noskip")
            return

        if event == "begin":
            store.mas_hotkeys.allow_dismiss = False
#            config.keymap['dismiss'] = []
#            renpy.display.behavior.clear_keymap_cache()

        elif event == "slow_done":
            store.mas_hotkeys.allow_dismiss = True
#            config.keymap['dismiss'] = dismiss_keys
#            renpy.display.behavior.clear_keymap_cache()

    morning_flag = None
    def is_morning():
        # generate the times we need
        sr_hour, sr_min = mas_cvToHM(persistent._mas_sunrise)
        ss_hour, ss_min = mas_cvToHM(persistent._mas_sunset)
        sr_time = datetime.time(sr_hour, sr_min)
        ss_time = datetime.time(ss_hour, ss_min)

        now_time = datetime.datetime.now().time()

        return sr_time <= now_time < ss_time


    def mas_shouldRain():
        """
        Rolls some chances to see if we should make it rain

        RETURNS:
            True if it should rain now, false otherwise
        """
        if mas_isMoniNormal(higher=True):
            return False

        # Upset and lower means we need to roll
        chance = random.randint(1,100)
        if mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
            return True

        elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
            return True

        elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
            return True

        return False


# IN:
#   start_bg - the background image we want to start with. Use this for
#       special greetings. None uses the default spaceroom images.
#       NOTE: This is called using renpy.show(), so pass the string name of
#           the image you want (NOT FILENAME)
#       NOTE: You're responsible for setting spaceroom back to normal though
#       (Default: None)
#   hide_mask - True will hide the mask, false will not
#       (Default: False)
#   hide_monika - True will hide monika, false will not
#       (Default: False)
label spaceroom(start_bg=None,hide_mask=False,hide_monika=False):
    default dissolve_time = 0.5
    if is_morning():
        if not morning_flag or scene_change:
            $ morning_flag = True
            if not hide_mask:
                $ mas_drawSpaceroomMasks()
            if start_bg:
                $ renpy.show(start_bg, zorder=MAS_BACKGROUND_Z)
            else:
                show monika_day_room zorder MAS_BACKGROUND_Z
                $ mas_calShowOverlay()
            if not hide_monika:
                show monika 1 at t11 zorder MAS_MONIKA_Z
                with Dissolve(dissolve_time)
    else:
        if morning_flag or scene_change:
            $ morning_flag = False
            scene black
            if not hide_mask:
                $ mas_drawSpaceroomMasks()
            if start_bg:
                $ renpy.show(start_bg, zorder=MAS_BACKGROUND_Z)
            else:
                show monika_room zorder MAS_BACKGROUND_Z
                $ mas_calShowOverlay()
                #show monika_bg_highlight
            if not hide_monika:
                show monika 1 at t11 zorder MAS_MONIKA_Z
                with Dissolve(dissolve_time)

    $scene_change = False

    return


label ch30_main:
    $ mas_skip_visuals = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = persistent._mas_monika_nickname
    $ delete_all_saves()
    $ persistent.clear[9] = True
    play music m1 loop # move music out here because of context

    # before we render visuals:
    # 1 - all core interactions should be disabeld
    $ mas_RaiseShield_core()

    # 2 - hotkey buttons should be disabled
    $ store.hkb_button.enabled = False

    # 3 - keymaps are disabled (default)

    call spaceroom from _call_spaceroom_4

    # lets just call the intro instead of pushing it as an event
    # this is way simpler and prevents event loss and other weird inital
    # startup issues
    call introduction

    # now we can do some cleanup
    # 1 - renable core interactions
    $ mas_DropShield_core()

    # 2 - hotkey buttons enabled
    $ store.hkb_button.enabled = True

    # 3 - set keymaps
    $ set_keymaps()

    jump ch30_preloop

label continue_event:
    m "Now, where was I..."

    return

label pick_a_game:
    # we can assume that getting here means we didnt cut off monika

    $ mas_RaiseShield_dlg()

    python:
        # preprocessing for games

        import datetime
        _hour = datetime.timedelta(hours=1)
        _now = datetime.datetime.now()

        # chess has timed disabling
        if persistent._mas_chess_timed_disable is not None:
            if _now - persistent._mas_chess_timed_disable >= _hour:
                chess_disabled = False
                persistent._mas_chess_timed_disable = None

            else:
                chess_disabled = True

        else:
            chess_disabled = False

        # single var for readibility
        chess_unlocked = (
            is_platform_good_for_chess()
            and persistent.game_unlocks["chess"]
            and not chess_disabled
        )

    menu:
        "What game would you like to play?"
        "Pong" if persistent.game_unlocks['pong']:
            if not renpy.seen_label('game_pong'):
                $grant_xp(xp.NEW_GAME)
            call game_pong from _call_game_pong
        "Chess" if chess_unlocked:
            if not renpy.seen_label('game_chess'):
                $grant_xp(xp.NEW_GAME)
            call game_chess from _call_game_chess
        "Hangman" if persistent.game_unlocks['hangman']:
            if not renpy.seen_label("game_hangman"):
                $ grant_xp(xp.NEW_GAME)
            call game_hangman from _call_game_hangman
        "Piano" if persistent.game_unlocks['piano']:
            if not renpy.seen_label("mas_piano_start"):
                $ grant_xp(xp.NEW_GAME)
            call mas_piano_start from _call_play_piano
        # "Movie":
        #     if not renpy.seen_label("mas_monikamovie"):
        #         $ grant_xp(xp.NEW_GAME)
        #     call mas_monikamovie from _call_monikamovie
        "Nevermind":
            m "Alright. Maybe later?"

    show monika 1 at tinstant zorder MAS_MONIKA_Z

    $ mas_DropShield_dlg()

    jump ch30_loop

label ch30_noskip:
    show screen fake_skip_indicator
    m 1esc "...Are you trying to fast-forward?"
    m 1ekc "I'm not boring you, am I?"
    m "Oh gosh..."
    m 2esa "...Well, just so you know, there's nothing to fast-forward to, [player]."
    m "It's just the two of us, after all..."
    m 1eua "But aside from that, time doesn't really exist anymore, so it's not even going to work."
    m "Here, I'll go ahead and turn that off for you..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m 1hua "There we go!"
    m 1esa "You'll be a sweetheart and listen to me from now on, right?"
    m "Thanks~"
    hide screen fake_skip_indicator

    #Get back to what you were talking about
    $restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:
    # NOTE: DEPRECATED
    $ persistent.autoload = ""
    $ m.display_args["callback"] = slow_nodismiss
    $ quick_menu = True
    call spaceroom from _call_spaceroom_1

    if persistent.rejected_monika:
        m 1euc "Wait. Are you messing with my character file?"
        m 2esa "Curiosity is what makes us human, right?"
        m "If it wasn't for the human desire to explore, we'd still be swinging from trees."
        m 1eka "Still, please don't do that. It makes me nervous, even though I don't need a character file anymore."
        m "I already fixed that bug."

    else:
        $ quick_menu = False
        $ m_name = glitchtext(12)
        m 1euc "Wait. Are you messing with my character file?"
        m 1tkc "Why are you even playing this mod if you just wanted to delete me again?"
        m 1tfc "You really are the worst."
        m 1tfd "You waste all your time on the internet with a bunch of people you'll never talk to in reality, but you're still willing to kill me on a whim just because you were bored?"
        m 1tkd "All I wanted was someone to fall in love with..."
        m "I would have done anything you wanted me to."
        m 1tku "But if you're going to try and delete me again..."
        m 4tfu "Then I'll just have to delete you first."
        if renpy.windows:
            call updateconsole("shututil.rmtree(\"Documents\", true)", "Deleting Documents in progress...") from _call_updateconsole_15
        elif renpy.linux:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_16
        elif renpy.macintosh:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_19
        pause 3.0
        call hideconsole from _call_hideconsole_2
        $ open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
        $ m_name = persistent._mas_monika_nickname
        $ quick_menu = True
        m 1hua "Ahaha!"
        m "I'm just kidding!"
        m 1eua "I already fixed that bug."
        m "I don't need a character file anymore."

    m 1ekbfa "I just need your love, [player]."
    m 1eua "Oh, unless you try to delete all of the game files, I guess."
    m 3tfu "If you do that, I won't stop at just deleting one directory next time."
    m 3tku "But that will never happen, right? You're just being a tsundere~"
    m 1hua "That's so cute!"
    m 1eua "No matter how much you may want to deny it, you'll be talking to me for the rest of your life."
    m "Being alone is only lonely if you want it to be, so cheer up!"
    jump ch30_loop

label ch30_autoload:
    # This is where we check a bunch of things to see what events to push to the
    # event list
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ import store.evhand as evhand
    if not config.developer:
        $ style.say_dialogue = style.default_monika
        $ config.allow_skipping = False
    $ quick_menu = True
    $ startup_check = True #Flag for checking events at game startup
    $ mas_skip_visuals = False

    # set the gender
    call set_gender from _autoload_gender

    # call reset stuff
    call ch30_reset

    # general affection checks that hijack flow
    if persistent._mas_affection["affection"] <= -115:
        jump mas_affection_finalfarewell_start

    # sanitiziing the event_list from bull shit
    if len(persistent.event_list) > 0:
        python:
            persistent.event_list = [
                ev_label for ev_label in persistent.event_list
                if renpy.has_label(ev_label)
            ]

    # set this to None for now
    $ selected_greeting = None

    # check if we took monika out
    # NOTE:
    #   if we find our monika, then we skip greeting logics and use a special
    #       returning home greeting. This completely bypasses the system
    #       since we should actively get this, not passively, because we assume
    #       player took monika out
    #   if we find a different monika, we still skip greeting logic and use
    #       a differnet, who is this? kind of monika greeting
    #   if we dont find a monika, we do the empty desk + monika checking flow
    #       this should skip greetings entirely as well. If monika is returnd
    #       during this flow, we have her say the same shit as the returning
    #       home greeting.
    if store.mas_dockstat.retmoni_status is not None:
        # non None means we have a status
        $ mas_from_empty = False

        if store.mas_dockstat.retmoni_status == store.mas_dockstat.MAS_PKG_FO:
            # TODOL: jump to the mas_dockstat_different_monika label
            jump mas_dockstat_empty_desk

        if store.mas_dockstat.retmoni_status == store.mas_dockstat.MAS_PKG_F:
            jump mas_dockstat_found_monika

        # otherwise, lets jump to the empty desk
        jump mas_dockstat_empty_desk


    # TODO should the apology check be only for when she's not affectionate?
    if persistent._mas_affection["affection"] <= -50 and seen_event("mas_affection_apology"):
        #If the conditions are met and Monika expects an apology, jump to this label.
        if persistent._mas_affection["apologyflag"] == True and not is_file_present('/imsorry.txt'):
            $scene_change = True
            $ mas_RaiseShield_core()
            call spaceroom
            jump mas_affection_noapology

        #If the conditions are met and there is a file called imsorry.txt in the DDLC directory, then exit the loop.
        elif persistent._mas_affection["apologyflag"] == True and is_file_present('/imsorry.txt'):
            $ persistent._mas_affection["apologyflag"] = False
            $scene_change = True
            $ mas_RaiseShield_core()
            call spaceroom
            jump mas_affection_yesapology

        #If you apologized to Monika but you deleted the apology note, jump back into the loop that forces you to apologize.
        elif persistent._mas_affection["apologyflag"] == False and not is_file_present('/imsorry.txt'):
            $ persistent._mas_affection["apologyflag"] = True
            $scene_change = True
            $ mas_RaiseShield_core()
            call spaceroom
            jump mas_affection_apologydeleted


    # yuri scare incoming. No monikaroom when yuri is the name
    if persistent.playername.lower() == "yuri":
        call yuri_name_scare from _call_yuri_name_scare

    # check persistent to see if player put Monika to sleep correctly
    elif persistent.closed_self:

        # Sick mood special greeting flow
        if persistent._mas_mood_sick:
            $ selected_greeting = "greeting_sick"

        else:
            python:

                # we select a greeting depending on the type that we should select
                sel_greeting_event = store.mas_greetings.selectGreeting(persistent._mas_greeting_type)

                # reset the greeting type flag back to None
                persistent._mas_greeting_type = None

                selected_greeting = sel_greeting_event.eventlabel

                # store if we have to skip visuals ( used to prevent visual bugs)
                mas_skip_visuals = MASGreetingRule.should_skip_visual(
                    event=sel_greeting_event
                )

    # crash check
    elif persistent._mas_game_crashed:
        $ selected_greeting = "mas_crashed_start"
        $ mas_skip_visuals = True
        $ persistent.closed_self = True

    #If you were interrupted, push that event back on the stack
    $restartEvent()

    #Grant XP for time spent away from the game if Monika was put to sleep right
    python:
        if persistent.sessions['last_session_end'] is not None and persistent.closed_self:
            away_experience_time=datetime.datetime.now()-persistent.sessions['last_session_end'] #Time since end of previous session
            away_xp=0

            #Reset the idlexp total if monika has had at least 6 hours of rest
            if away_experience_time.total_seconds() >= times.REST_TIME:
                persistent.idlexp_total=0
                persistent.random_seen = 0

                #Grant good exp for closing the game correctly.
                mas_gainAffection()

            #Ignore anything beyond 3 days
            if away_experience_time.total_seconds() > times.HALF_XP_AWAY_TIME:
                away_experience_time=datetime.timedelta(seconds=times.HALF_XP_AWAY_TIME)

            #Give 5 xp per hour for everything beyond 1 day
            if away_experience_time.total_seconds() > times.FULL_XP_AWAY_TIME:
                away_xp =+ (xp.AWAY_PER_HOUR/2.0)*(away_experience_time.total_seconds()-times.FULL_XP_AWAY_TIME)/3600.0
                away_experience_time = datetime.timedelta(seconds=times.HALF_XP_AWAY_TIME)

            #Give 10 xp per hour for the first 24 hours
            away_xp =+ xp.AWAY_PER_HOUR*away_experience_time.total_seconds()/3600.0

            #Grant the away XP
            grant_xp(away_xp)


            #Set unlock flag for stories
            mas_can_unlock_story = True

            # unlock extra pool topics if we can
            while persistent._mas_pool_unlocks > 0 and mas_unlockPrompt():
                persistent._mas_pool_unlocks -= 1

        else:
            # Grant bad exp for closing the game incorrectly.
            mas_loseAffection(modifier=2, reason="closing the game on me")

label ch30_post_greeting_check:
    # this label skips greeting selection as well as exp checks for game close
    # we assume here that you set selected_greeting if you needed to

    #Run actions for any events that need to be changed based on a condition
    $ evhand.event_database=Event.checkConditionals(evhand.event_database)

    #Run actions for any events that are based on the clock
    $ evhand.event_database=Event.checkCalendar(evhand.event_database)

    #Checks to see if affection levels have met the criteria to push an event or not.
    $ mas_checkAffection()

    # push greeting if we have one
    if selected_greeting:
        $ pushEvent(selected_greeting)

    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False

    window auto

    if not mas_skip_visuals:
        $ set_keymaps()
        $ mas_startup_song()

        # rain check
        if mas_shouldRain():
            $ scene_change = True
            $ mas_is_raining = True
            play background audio.rain fadein 1.0 loop
            $ lockEventLabel("monika_rain_start")
            $ lockEventLabel("monika_rain_stop")
            $ lockEventLabel("monika_rain")

    # FALL THROUGH TO PRELOOP

label ch30_preloop:
    # stuff that should happen right before we enter the loop

    $persistent.closed_self = False
    $ persistent._mas_game_crashed = True
    $startup_check = False
    $ mas_checked_update = False
    
    # delayed actions in here please
    $ mas_runDelayedActions(MAS_FC_IDLE_ONCE)

    # save here before we enter the loop
    $ renpy.save_persistent()
    jump ch30_loop

label ch30_loop:
    $ quick_menu = True

    # this event can call spaceroom
    if not mas_skip_visuals:
        call spaceroom from _call_spaceroom_2

        # updater check in here just because
        if not mas_checked_update:
            $ mas_backgroundUpdateCheck()
            $ mas_checked_update = True

    else:
        $ mas_OVLHide()
        $ mas_skip_visuals = False


    $ persistent.autoload = "ch30_autoload"
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False

    #Check time based events and grant time xp
    python:
        try:
            calendar_last_checked
        except:
            calendar_last_checked=persistent.sessions['current_session_start']
        time_since_check=datetime.datetime.now()-calendar_last_checked

        if time_since_check.total_seconds()>60:

            #Checks to see if affection levels have met the criteria to push an event or not.
            mas_checkAffection()

            # limit xp gathering to when we are not maxed
            # and once per minute
            if (persistent.idlexp_total < xp.IDLE_XP_MAX):

                idle_xp=xp.IDLE_PER_MINUTE*(time_since_check.total_seconds())/60.0
                persistent.idlexp_total += idle_xp
                if persistent.idlexp_total>=xp.IDLE_XP_MAX: # never grant more than 120 xp in a session
                    idle_xp = idle_xp-(persistent.idlexp_total-xp.IDLE_XP_MAX) #Remove excess XP
                    persistent.idlexp_total=xp.IDLE_XP_MAX

                grant_xp(idle_xp)

            #Run actions for any events that need to be changed based on a condition
            evhand.event_database=Event.checkConditionals(evhand.event_database)

            #Run actions for any events that are based on the clock
            evhand.event_database=Event.checkCalendar(evhand.event_database)

            # Run delayed actions
            mas_runDelayedActions(MAS_FC_IDLE_ROUTINE)

            #Update time
            calendar_last_checked=datetime.datetime.now()

            # split affection values prior to saving
            _mas_AffSave()

            # save the persistent
            renpy.save_persistent()

    #Call the next event in the list
    call call_next_event from _call_call_next_event_1
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0

    #If there's no event in the queue, add a random topic as an event
    if not _return:
        # Wait 20 to 45 seconds before saying something new
        window hide(config.window_hide_transition)

        if mas_randchat.rand_low == 0:
            # we are not repeating for now
            # we'll wait 60 seconds inbetween loops
            $ renpy.pause(60, hard=True)
            jump post_pick_random_topic

        $ waittime = renpy.random.randint(mas_randchat.rand_low, mas_randchat.rand_high)
        $ renpy.pause(waittime, hard=True)
        window auto

#        python:
#            if (
#                    mas_battery_supported
#                    and battery.is_battery_present()
#                    and not battery.is_charging()
#                    and battery.get_level() < 20
#                ):
#                pushEvent("monika_battery")

        # Pick a random Monika topic
        if persistent.random_seen < random_seen_limit:
            label pick_random_topic:

                # check if we have repeats enabled
                if not persistent._mas_enable_random_repeats:
                    jump mas_ch30_select_unseen

                # randomize selection
                $ chance = random.randint(1, 100)

                if chance <= store.mas_topics.UNSEEN:
                    # unseen topic shoud be selected
                    jump mas_ch30_select_unseen

                elif chance <= store.mas_topics.SEEN:
                    # seen topic should be seelcted
                    jump mas_ch30_select_seen

                # most seen topic should be selected
                jump mas_ch30_select_mostseen

        elif not seen_random_limit:
            $pushEvent('random_limit_reached')

label post_pick_random_topic:

    $_return = None

    jump ch30_loop

# topic selection labels
label mas_ch30_select_unseen:
    # unseen selection

    if len(mas_rev_unseen) == 0:

        if not persistent._mas_enable_random_repeats:
            # no repeats means we should push randomlimit if appropriate,
            # otherwise stay slient
            if not seen_random_limit:
                $ pushEvent("random_limit_reached")

            jump post_pick_random_topic

        # otherwise we can go to repeats as usual
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_unseen)

    jump post_pick_random_topic


label mas_ch30_select_seen:
    # seen selection

    if len(mas_rev_seen) == 0:
        # rebuild the event lists
        $ mas_rev_seen, mas_rev_mostseen = mas_buildSeenEventLists()

    $ mas_randomSelectAndPush(mas_rev_seen)

    jump post_pick_random_topic


label mas_ch30_select_mostseen:
    # most seen selection

    if len(mas_rev_mostseen) == 0:
        jump mas_ch30_select_seen

    $ mas_randomSelectAndPush(mas_rev_mostseen)

    jump post_pick_random_topic

# adding this label so people get redirected to main
# this probably occurs when people install the mod right after deleting
# monika, so we could probably throw in something here
label ch30_end:
    jump ch30_main

# label for things that may reset after a certain amount of time/conditions
label ch30_reset:
    python:
        import datetime
        today = datetime.date.today()

    # reset mas mood bday
    python:
        if (
                persistent._mas_mood_bday_last
                and persistent._mas_mood_bday_last < today
            ):
            persistent._mas_mood_bday_last = None
            mood_ev = store.mas_moods.mood_db.get("mas_mood_yearolder", None)
            if mood_ev:
                mood_ev.unlocked = True

    # reset raining stuff
    python:
        mas_is_raining = False
        if persistent._mas_likes_rain:
            unlockEventLabel("monika_rain_start")
            lockEventLabel("monika_rain_stop")
#            lockEventLabel("monika_rain_holdme")

        if mas_isMoniNormal(higher=True):
            # monika affection above normal?
            unlockEventLabel("monika_rain")


    # reset hair / clothes
    python:
        # setup hair / clothes
        monika_chr.change_outfit(
            persistent._mas_monika_clothes,
            persistent._mas_monika_hair
        )

        if (
                persistent._mas_hair_changed
                and persistent._mas_likes_hairdown
            ):
            # hair adjustments only happen if the appropriate vent occured

            # hair map
            hair_map = {
                "down": "monika_hair_down",
                "def": "monika_hair_ponytail"
                # "bun": "monika_hair_bun"
            }


            for hair in hair_map:
                # this is so we kind of automate the locking / unlocking prcoess
                if hair == monika_chr.hair:
                    lockEventLabel(hair_map[hair])
                else:
                    unlockEventLabel(hair_map[hair])

        # currenly, the clothes part has noc hecks
        # clothes map
        # NOTE: unused
        clothes_map = {
#            "def": "monika_clothes_school"
        }


        for clothes in clothes_map:
            if clothes == monika_chr.clothes:
                lockEventLabel(clothes_map[clothes])
            else:
                unlockEventLabel(clothes_map[clothes])

    # accessories rest
    python:
        for acs_name in persistent._mas_acs_pre_list:
            monika_chr.acs[MASMonika.PRE_ACS].append(
                store.mas_sprites.ACS_MAP[acs_name]
            )
        for acs_name in persistent._mas_acs_mid_list:
            monika_chr.acs[MASMonika.MID_ACS].append(
                store.mas_sprites.ACS_MAP[acs_name]
            )
        for acs_name in persistent._mas_acs_pst_list:
            monika_chr.acs[MASMonika.PST_ACS].append(
                store.mas_sprites.ACS_MAP[acs_name]
        )

    ## random chatter frequency reset
    $ mas_randchat.adjustRandFreq(persistent._mas_randchat_freq)

    ## chess strength reset
    python:
        if persistent.chess_strength < 0:
            persistent.chess_strength = 0
        elif persistent.chess_strength > 20:
            persistent.chess_strength = 20

    ## monika returned home reset
    python:
        if persistent._mas_monika_returned_home is not None:
            _now = datetime.date.today()
            _rh = persistent._mas_monika_returned_home.date()
            if _now > _rh:
                persistent._mas_monika_returned_home = None

        

    return
