default persistent.monika_reload = 0
default persistent.tried_skip = None
default persistent.monika_kill = True #Assume non-merging players killed monika.
default persistent.rejected_monika = None
default initial_monika_file_check = None
default persistent.monika_anniversary = 0
default persistent.firstdate = datetime.datetime.now()
define allow_dialogue = True

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
    import re
    import store.songs as songs
    import store.hkb_button as hkb_button
    therapist = eliza.eliza()
    process_list = []
    currentuser = persistent.playername #default to the player name
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

    #Define new functions
    def play_song(song):
        #
        # literally just plays a song onto the music channel
        #
        # IN:
        #   song - song to play. If None, the channel is stopped
        if song is None:
            renpy.music.stop(channel="music")
        else:
            renpy.music.play(song,channel="music",loop=True,synchro_start=True)

    def mute_music():
        #
        # mutes the music channel
        #
        # ASSUMES:
        #   songs.music_volume
        curr_volume = songs.getVolume("music")
        if curr_volume > 0.0:
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
            renpy.jump('ch30_monikatopics')

    def pick_game():
        if allow_dialogue:
            renpy.call_in_new_context('pick_a_game')

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
    def days_passed():
        now = datetime.datetime.now()
        delta = now - persistent.firstdate
        return delta.days

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
                $ renpy.show(start_bg)
            else:
                show monika_day_room
            if not hide_monika:
                show monika 1 at tinstant zorder 2
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
                $ renpy.show(start_bg)
            else:
                show monika_room
                #show monika_bg_highlight
            if not hide_monika:
                show monika 1 at tinstant zorder 2
                with Dissolve(dissolve_time)

    $scene_change = False

    return

label ch30_main:
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
        $ songs.enabled = False
        $ hkb_button.enabled = False
        $previous_dialogue = allow_dialogue
        $allow_dialogue = False
        menu:
            "What game would you like to play?"
            "Pong":
                call game_pong from _call_game_pong
            "Chess" if is_platform_good_for_chess():
                call game_chess from _call_game_chess
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
        m 1f"Then I'll just have to delete you first."
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
    if not config.developer:
        $ style.say_dialogue = style.default_monika
        $ config.allow_skipping = False
    $ quick_menu = True
    
    python:
        # random chance to do monika in room greeting
        # we'll say 1 in 20 
        if not config.developer:
            import random
            persistent.is_monika_in_room = (
                not seen_event("i_greeting_monikaroom")
                and random.randint(1,20) == 1
            )

        if not persistent.is_monika_in_room:
            if persistent.current_track is not None:
                play_song(persistent.current_track)
            else:
                play_song(songs.current_track) # default
    window auto
    #If you were interrupted, push that event back on the stack
    $restartEvent()

    $ elapsed = days_passed()
    #If one day is past & event 'gender' has not been viewed, then add 'gender' to the queue.
    if elapsed > 1 and not renpy.seen_label('gender') and not 'gender' in persistent.event_list:
        $queueEvent('gender')

    #Asks player if they want to be called by a different name
    if not seen_event('preferredname'):
        $pushEvent('preferredname')

    #Block for anniversary events
    if elapsed < persistent.monika_anniversary * 365 and not 'anni_negative' in persistent.event_list:
        $ persistent.monika_anniversary = 0
        $pushEvent(anni_negative)
    elif elapsed >= 36500 and persistent.monika_anniversary < 100 and not renpy.seen_label('anni_100') and not 'anni_100' in persistent.event_list:
        $ persistent.monika_anniversary = 100
        $pushEvent(anni_100)
    elif elapsed >= 18250 and persistent.monika_anniversary < 50 and not renpy.seen_label('anni_50') and not 'anni_50' in persistent.event_list:
        $ persistent.monika_anniversary = 50
        $pushEvent(anni_50)
    elif elapsed >= 7300 and persistent.monika_anniversary < 20 and not renpy.seen_label('anni_20') and not 'anni_20' in persistent.event_list:
        $ persistent.monika_anniversary = 20
        $pushEvent(anni_20)
    elif elapsed >= 3650 and persistent.monika_anniversary < 10 and not renpy.seen_label('anni_10') and not 'anni_10' in persistent.event_list:
        $ persistent.monika_anniversary = 10
        $pushEvent(anni_10)
    elif elapsed >= 1825 and persistent.monika_anniversary < 5 and not renpy.seen_label('anni_5') and not 'anni_5' in persistent.event_list:
        $ persistent.monika_anniversary = 5
        $pushEvent(anni_5)
    elif elapsed >= 1460 and persistent.monika_anniversary < 4 and not renpy.seen_label('anni_4') and not 'anni_4' in persistent.event_list:
        $ persistent.monika_anniversary = 4
        $pushEvent(anni_4)
    elif elapsed >= 1095 and persistent.monika_anniversary < 3 and not renpy.seen_label('anni_3') and not 'anni_3' in persistent.event_list:
        $ persistent.monika_anniversary = 3
        $pushEvent(anni_3)
    elif elapsed >= 730 and persistent.monika_anniversary < 2 and not renpy.seen_label('anni_2') and not 'anni_2' in persistent.event_list:
        $ persistent.monika_anniversary = 2
        $pushEvent(anni_2)
    elif elapsed >= 365 and persistent.monika_anniversary < 1 and not renpy.seen_label('anni_1') and not 'anni_1' in persistent.event_list:
        $ persistent.monika_anniversary = 1
        $pushEvent(anni_1)

    #queue up the next reload event it exists and isn't already queue'd
    $next_reload_event = "ch30_reload_" + str(persistent.monika_reload)
    if not seen_event(next_reload_event) and not persistent.closed_self:
        $queueEvent(next_reload_event)

    $persistent.closed_self = False

    #pick a random greeting
    if persistent.is_monika_in_room:
        $ pushEvent("i_greeting_monikaroom")
    else:
        $pushEvent(renpy.random.choice(greetings_list))

    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False

    if not persistent.is_monika_in_room:
        $ set_keymaps()
    jump ch30_loop

label ch30_loop:
    $ quick_menu = True

    # this event can call spaceroom
    if not persistent.is_monika_in_room:
        call spaceroom from _call_spaceroom_2

    $ persistent.autoload = "ch30_autoload"
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False

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
        # Pick a random Monika topic
        label pick_random_topic:
        python:
            if monika_random_topics:        # If we're out of random topics, just stay in the loop
                pushEvent(renpy.random.choice(monika_random_topics))

    $_return = None

    jump ch30_loop


label ch30_monikatopics:
    python:

        # this workaround is so the hotkey button overlay properly disables
        # certain buttons
        allow_dialogue = False

        player_dialogue = renpy.input('What would you like to talk about?',default='',pixel_width=720,length=50)

        if player_dialogue:

            raw_dialogue=player_dialogue
            player_dialogue = player_dialogue.lower()
            player_dialogue = re.sub(r'[^\w\s]','',player_dialogue) #remove punctuation
            persistent.current_monikatopic = 0

            player_dialogue = player_dialogue.split()
            #Look at all possible ngrams in the dialogue
            player_dialogue_ngrams=player_dialogue
            player_dialogue_bigrams = zip(player_dialogue, player_dialogue[1:])
            for bigram in player_dialogue_bigrams:
                player_dialogue_ngrams.append(' '.join(bigram))

            possible_topics=[] #track all topics that correspond to the input
            for key in player_dialogue_ngrams:
                if key in monika_topics:
                    for topic_id in monika_topics[key]:
                        if topic_id not in possible_topics:
                            possible_topics.append(topic_id)

            if possible_topics == []: #Therapist answer if no keywords match
                # give a therapist answer for all the depressed weebs
                response = therapist.respond(raw_dialogue)
                m("[response]")
            else:
                pushEvent(renpy.random.choice(possible_topics)) #Pick a random topic

        allow_dialogue = True

    jump ch30_loop
