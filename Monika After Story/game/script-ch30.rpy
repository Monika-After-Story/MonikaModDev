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
        if morning_flag != True or scene_change:
            $ morning_flag = True
            if not hide_mask:
                show room_mask3 as rm:
                    size (320,180)
                    pos (30,200)
                show room_mask4 as rm2:
                    size (320,180)
                    pos (935,200)
            if start_bg:
                $ renpy.show(start_bg, zorder=1)
            else:
                show monika_day_room zorder 1
            if not hide_monika:
                show monika 1 at t11 zorder 2
                with Dissolve(dissolve_time)
    elif not is_morning():
        if morning_flag != False or scene_change:
            $ morning_flag = False
            scene black
            if not hide_mask:
                show room_mask as rm:
                    size (320,180)
                    pos (30,200)
                show room_mask2 as rm2:
                    size (320,180)
                    pos (935,200)
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
    $ m_name = persistent._mas_monika_nickname
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
        $previous_dialogue = allow_dialogue
        $allow_dialogue = False
        menu:
            "What game would you like to play?"
            "Pong" if persistent.game_unlocks['pong']:
                if not renpy.seen_label('game_pong'):
                    $grant_xp(xp.NEW_GAME)
                call game_pong from _call_game_pong
            "Chess" if is_platform_good_for_chess() and persistent.game_unlocks['chess']:
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
        $ m_name = persistent._mas_monika_nickname
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

    # TODO: temporary for testing
    jump monika_finalfarewell

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
            
    #Grant good exp for closing the game correctly.
    $ mas_gainAffection()
            
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

    if not mas_skip_visuals:
        $ set_keymaps()

    $persistent.closed_self = False
    $ persistent._mas_crashed_self = True
    $startup_check = False
    jump ch30_loop

label ch30_loop:
    $ quick_menu = True

    # this event can call spaceroom
    if not mas_skip_visuals:
        call spaceroom from _call_spaceroom_2
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

        python:
            if (
                    mas_battery_supported
                    and battery.is_battery_present()
                    and not battery.is_charging()
                    and battery.get_level() < 20
                ):
                pushEvent("monika_battery")

        # Pick a random Monika topic
        if persistent.random_seen < random_seen_limit:
            label pick_random_topic:
            python:
                if len(monika_random_topics) > 0:  # still have topics

                    if persistent._mas_monika_repeated_herself:
                        sel_ev = monika_random_topics.pop(0)
                    else:
                        sel_ev = renpy.random.choice(monika_random_topics)
                        monika_random_topics.remove(sel_ev)

                    pushEvent(sel_ev)
                    persistent.random_seen += 1

                elif persistent._mas_enable_random_repeats:
                    # user wishes for reptitive monika. We will oblige, but
                    # a somewhat intelligently.
                    # NOTE: these are ordered using the shown_count property
                    # NOTE: These start off as list of event objects and then
                    # sorted differently. WATCH OUT
                    monika_random_topics = Event.filterEvents(
                        evhand.event_database,
                        random=True
                    ).values()
                    monika_random_topics.sort(key=Event.getSortShownCount)
                    monika_random_topics = [
                        ev.eventlabel for ev in monika_random_topics
                    ]
                    # NOTE: now the monika random topics are back to being
                    #   labels. Safe to do normal operation.

                    persistent._mas_monika_repeated_herself = True
                    sel_ev = monika_random_topics.pop(0)
                    pushEvent(sel_ev)
                    persistent.random_seen += 1

                elif not seen_random_limit: # no topics left
#                    monika_random_topics = list(all_random_topics)
#                    pushEvent(renpy.random.choice(monika_random_topics))
                    pushEvent("random_limit_reached")
        elif not seen_random_limit:
            $pushEvent('random_limit_reached')

    $_return = None

    jump ch30_loop

# adding this label so people get redirected to main
# this probably occurs when people install the mod right after deleting
# monika, so we could probably throw in something here
label ch30_end:
    jump ch30_main
