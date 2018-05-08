default persistent.monika_reload = 0
default persistent.tried_skip = None
default persistent.monika_kill = True #Assume non-merging players killed monika.
default persistent.rejected_monika = None
default initial_monika_file_check = None
define allow_dialogue = True
define modoorg.CHANCE = 20
define mas_battery_supported = False

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

    def enable_esc():
        #
        # Enables the escape key so you can go to the game menu
        #
        # ASSUMES:
        #   config.keymap
        if "K_ESCAPE" not in config.keymap["game_menu"]:
            config.keymap["game_menu"].append("K_ESCAPE")

    def disable_esc():
        #
        # disables the escape key so you cant go to game menu
        #
        # ASSUMES:
        #   config.keymap
        if "K_ESCAPE" in config.keymap["game_menu"]:
           config.keymap["game_menu"].remove("K_ESCAPE")

    def play_song(song, fadein=0.0):
        #
        # literally just plays a song onto the music channel
        #
        # IN:
        #   song - song to play. If None, the channel is stopped
        #   fadein - number of seconds to fade in the song
        if song is None:
            renpy.music.stop(channel="music")
        else:
            renpy.music.play(
                song,
                channel="music",
                loop=True,
                synchro_start=True,
                fadein=fadein
            )

    def mute_music():
        #
        # mutes the music channel
        #
        # ASSUMES:
        #   songs.music_volume
        #   persistent.playername

        curr_volume = songs.getVolume("music")
        # sayori cannot mute
        if curr_volume > 0.0 and persistent.playername.lower() != "sayori":
            songs.music_volume = curr_volume
            renpy.music.set_volume(0.0, channel="music")
        else:
            renpy.music.set_volume(songs.music_volume, channel="music")

    def inc_musicvol():
        #
        # increases the volume of the music channel by the value defined in
        # songs.vol_bump
        #
        songs.adjustVolume()

    def dec_musicvol():
        #
        # decreases the volume of the music channel by the value defined in
        # songs.vol_bump
        #
        # ASSUMES:
        #   persistent.playername

        # sayori cannot make the volume quieter
        if persistent.playername.lower() != "sayori":
            songs.adjustVolume(up=False)

    def set_keymaps():
        #
        # Sets the keymaps
        #
        # ASSUMES:
        #   config.keymap
        #   config.underlay
        #Add keys for new functions
        config.keymap["open_dialogue"] = ["t","T"]
        config.keymap["change_music"] = ["noshift_m","noshift_M"]
        config.keymap["play_game"] = ["p","P"]
        config.keymap["mute_music"] = ["shift_m","shift_M"]
        config.keymap["inc_musicvol"] = [
            "shift_K_PLUS","K_EQUALS","K_KP_PLUS"
        ]
        config.keymap["dec_musicvol"] = [
            "K_MINUS","shift_K_UNDERSCORE","K_KP_MINUS"
        ]
        # Define what those actions call
        config.underlay.append(renpy.Keymap(open_dialogue=show_dialogue_box))
        config.underlay.append(renpy.Keymap(change_music=select_music))
        config.underlay.append(renpy.Keymap(play_game=pick_game))
        config.underlay.append(renpy.Keymap(mute_music=mute_music))
        config.underlay.append(renpy.Keymap(inc_musicvol=inc_musicvol))
        config.underlay.append(renpy.Keymap(dec_musicvol=dec_musicvol))

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


    def show_dialogue_box():
        if allow_dialogue:
            renpy.jump('prompt_menu')

    def pick_game():
        if allow_dialogue:
            renpy.call('pick_a_game')

    def select_music():
        # check for open menu
        if (songs.enabled
            and not songs.menu_open
            and renpy.get_screen("history") is None
            and renpy.get_screen("save") is None
            and renpy.get_screen("load") is None
            and renpy.get_screen("preferences") is None):

            # music menu label
            renpy.call_in_new_context("display_music_menu")

            # workaround to handle new context
            if songs.selected_track != songs.current_track:
                play_song(songs.selected_track)
                songs.current_track = songs.selected_track
                persistent.current_track = songs.current_track

    dismiss_keys = config.keymap['dismiss']

    def slow_nodismiss(event, interact=True, **kwargs):
        if not renpy.seen_label("ch30_nope"):
            try:
                renpy.file("../characters/monika.chr")
            except:
                if initial_monika_file_check:
                    pushEvent("ch30_nope")
            #     persistent.tried_skip = True
            #     config.allow_skipping = False
            #     _window_hide(None)
            #     pause(2.0)
            #     renpy.jump("ch30_end")
            if  config.skipping and not config.developer:
                persistent.tried_skip = True
                config.skipping = False
                config.allow_skipping = False
                renpy.jump("ch30_noskip")
                return
        if event == "begin":
            config.keymap['dismiss'] = []
            renpy.display.behavior.clear_keymap_cache()
        elif event == "slow_done":
            config.keymap['dismiss'] = dismiss_keys
            renpy.display.behavior.clear_keymap_cache()
    morning_flag = None
    def is_morning():
        return (datetime.datetime.now().time().hour > 6 and datetime.datetime.now().time().hour < 18)

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
                $ renpy.show(start_bg, zorder=1)
            else:
                show monika_day_room zorder 1
            if not hide_monika:
                show monika 1 at t11 zorder 2
                with Dissolve(dissolve_time)
    else:
        if morning_flag or scene_change:
            $ morning_flag = False
            scene black
            if not hide_mask:
                $ mas_drawSpaceroomMasks()
            if start_bg:
                $ renpy.show(start_bg, zorder=1)
            else:
                show monika_room zorder 1
                #show monika_bg_highlight
            if not hide_monika:
                show monika 1 at t11 zorder 2
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
    $ m_name = "Monika"
    $ delete_all_saves()
    $ persistent.clear[9] = True
    play music m1 loop # move music out here because of context
    call spaceroom from _call_spaceroom_4
    $pushEvent('introduction')
    call call_next_event from _call_call_next_event
    jump ch30_loop

label continue_event:
    m "Now, where was I..."

    return

label pick_a_game:
    if allow_dialogue and not songs.menu_open:
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

        $previous_dialogue = allow_dialogue
        $allow_dialogue = False
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
            "Nevermind":
                m "Alright. Maybe later?"

        show monika 1 at tinstant zorder 2
        $allow_dialogue = previous_dialogue
        $ songs.enabled = True
        $ hkb_button.enabled = True

    jump ch30_loop

label ch30_noskip:
    show screen fake_skip_indicator
    m 1i "...Are you trying to fast-forward?"
    m 1f "I'm not boring you, am I?"
    m "Oh gosh..."
    m 2 "...Well, just so you know, there's nothing to fast-forward to, [player]."
    m "It's just the two of us, after all..."
    m 1 "But aside from that, time doesn't really exist anymore, so it's not even going to work."
    m "Here, I'll go ahead and turn that off for you..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m 1j "There we go!"
    m 1 "You'll be a sweetheart and listen to me from now on, right?"
    m "Thanks~"
    hide screen fake_skip_indicator

    #Get back to what you were talking about
    $restartEvent()
    jump ch30_loop

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_nope:
    $ persistent.autoload = ""
    $ m.display_args["callback"] = slow_nodismiss
    $ quick_menu = True
    call spaceroom from _call_spaceroom_1

    if persistent.rejected_monika:
        m 1i "Wait. Are you messing with my character file?"
        m 2 "Curiosity is what makes us human, right?"
        m "If it wasn't for the human desire to explore, we'd still be swinging from trees."
        m 1m "Still, please don't do that. It makes me nervous, even though I don't need a character file anymore."
        m "I already fixed that bug."

    else:
        $ quick_menu = False
        $ m_name = glitchtext(12)
        m 1i "Wait. Are you messing with my character file?"
        m 1f "Why are you even playing this mod if you just wanted to delete me again?"
        m "You really are the worst."
        m "You waste all your time on the internet with a bunch of people you'll never talk to in reality, but you're still willing to kill me on a whim just because you were bored?"
        m "All I wanted was someone to fall in love with..."
        m 2g "I would have done anything you wanted me to."
        m "But if you're going to try and delete me again..."
        m 1f "Then I'll just have to delete you first."
        if renpy.windows:
            call updateconsole("shututil.rmtree(\"Documents\", true)", "Deleting Documents in progress...") from _call_updateconsole_15
        elif renpy.linux:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_16
        elif renpy.macintosh:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_19
        pause 3.0
        call hideconsole from _call_hideconsole_2
        $ open(config.basedir + "/characters/monika.chr", "wb").write(renpy.file("monika.chr").read())
        $ m_name = "Monika"
        $ quick_menu = True
        m 1l "Ahaha!"
        m "I'm just kidding!"
        m 1j "I already fixed that bug."
        m 1 "I don't need a character file anymore."

    m 1 "I just need your love, [player]."
    m 2i "Oh, unless you try to delete all of the game files, I guess."
    m 3h "If you do that, I won't stop at just deleting one directory next time."
    m 3 "But that will never happen, right? You're just being a tsundere~"
    m "That's so cute!"
    m "No matter how much you may want to deny it, you'll be talking to me for the rest of your life."
    m 1j "Being alone is only lonely if you want it to be, so cheer up!"
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

    # sanitiziing the event_list from bull shit
    if len(persistent.event_list) > 0:
        python:
            persistent.event_list = [
                ev_label for ev_label in persistent.event_list
                if renpy.has_label(ev_label)
            ]

    $ selected_greeting = None

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

                sel_greeting_event = store.mas_greetings.selectGreeting()
                selected_greeting = sel_greeting_event.eventlabel

                # store if we have to skip visuals ( used to prevent visual bugs)
                mas_skip_visuals = MASGreetingRule.should_skip_visual(
                    event=sel_greeting_event
                )

    if not mas_skip_visuals:
        if persistent.current_track:
            $ play_song(persistent.current_track)
        else:
            $ play_song(songs.current_track) # default

    window auto
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

    #Run actions for any events that need to be changed based on a condition
    $ evhand.event_database=Event.checkConditionals(evhand.event_database)

    #Run actions for any events that are based on the clock
    $ evhand.event_database=Event.checkCalendar(evhand.event_database)

    # push greeting if we have one
    if selected_greeting:
        $ pushEvent(selected_greeting)

    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False

    if not mas_skip_visuals:
        $ set_keymaps()

    $persistent.closed_self = False
    $ persistent._mas_crashed_self = True
    $startup_check = False
    $ mas_checked_update = False
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

            #Update time
            calendar_last_checked=datetime.datetime.now()

    #Call the next event in the list
    call call_next_event from _call_call_next_event_1
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0

    #If there's no event in the queue, add a random topic as an event
    if not _return:
        # Wait 20 to 45 seconds before saying something new
        window hide(config.window_hide_transition)
        $ waittime = renpy.random.randint(20, 45)
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
                # randomize selection
                $ chance = renpy.random.randint(1, 100)

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
    return
