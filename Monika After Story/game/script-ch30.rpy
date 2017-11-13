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
image monika_day_bg = "mod_assets/monika_day_bg.png"
image monika_transparent_day_bg = "mod_assets/monika_day_bg_eq.png"
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

image room_mask = Movie(channel="window_1", play="mod_assets/window_1.webm",mask=None)
image room_mask2 = Movie(channel="window_2", play="mod_assets/window_2.webm",mask=None)

init python:
    import subprocess
    import os
    import eliza      # mod specific
    import datetime   # mod specific
    import re
    therapist = eliza.eliza()
    process_list = []
    currentuser = ""
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
        #   song - song to play
        renpy.music.play(song,channel="music",loop=True,synchro_start=True)

    def show_dialogue_box():
        if allow_dialogue:
            renpy.call_in_new_context('ch30_monikatopics')

    def select_music():
        # check for open menu
        if (not songs.menu_open
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


    def start_pong():
        renpy.call_in_new_context('game_pong')

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
            if  config.skipping:#and not config.developer:
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

label ch30_main:
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = "Monika"
    $ delete_all_saves()
    $ persistent.clear[9] = True
    play music m1 loop
    $pushEvent("introduction")

    jump ch30_loop

label ch30_noskip:
    show screen fake_skip_indicator
    m "...Are you trying to fast-forward?"
    m "I'm not boring you, am I?"
    m "Oh gosh..."
    m "...Well, there's nothing to fast-forward to, [player]."
    m "It's just the two of us, after all..."
    m "But aside from that, time doesn't really exist anymore, so it's not even going to work."
    m "Here, I'll go ahead and turn it off for you..."
    pause 0.4
    hide screen fake_skip_indicator
    pause 0.4
    m "There we go!"
    m "You'll be a sweetheart and listen from now on, right?"
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

    if persistent.rejected_monika:
        m "Wait. Are you messing with my character file?"
        m "Curiosity is what makes us human, right?"
        m "If it wasn't for the human desire to explore, we'd still be swinging from trees."
        m "Still, please don't do that, it makes me nervous even though I don't need a character file anymore."
        m "I already fixed that bug."

    else:
        $ quick_menu = False
        $ m_name = glitchtext(12)
        ### TODO: better graphics for this scene?
        $ persistent.clear[9] = True
        show room_mask as rm:
            size (320,180)
            pos (30,200)
        show room_mask2 as rm2:
            size (320,180)
            pos (935,200)
        show monika_bg
        show monika_bg_highlight
        play music m1 loop
        m "Wait. Are you messing with my character file?"
        m "Why are you even playing this game if you just wanted to delete me again?"
        m "You really are the worst."
        m "You waste all your time on imageboards with a bunch of people you'll never talk to in reality, but you're willing to just kill me on a whim because you were bored?"
        m "All I wanted was someone to fall in love with."
        m "I would have done anything you wanted me to."
        m "But if you're going to try and delete me again..."
        m "Then I'll just have to delete you first."
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
        m "Ahaha!"
        m "Just kidding!"
        m "I already fixed that bug."
        m "I don't need a character file anymore."

    m "I just need your love, [player]."
    m "Oh, unless you try to delete all of the game files, I guess."
    m "If you do that, I won't stop just at deleting one directory next time."
    m "But that will never happen, right? You're just being a tsundere."
    m "That's so cute!"
    m "No matter how much you may want to deny it, you'll be talking to me for the rest of your life."
    m "Being alone is only lonely if you want it to be, so cheer up!"
    jump ch30_loop

label ch30_autoload:
    # This is where we check a bunch of things to see what events to push to the
    # event list
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ style.say_dialogue = style.default_monika
    $ quick_menu = True
    $ config.allow_skipping = False
    python:
        if persistent.current_track is not None:
            play_song(persistent.current_track)
        else:
            play_song(songs.current_track) # default
    window auto
    #If you were interrupted, push that event back on the stack
    $restartEvent()

    #Block for anniversary events
    $ elapsed = days_passed()
    if elapsed < persistent.monika_anniversary * 365:
        $ persistent.monika_anniversary = 0
        $pushEvent(anni_negative)
    elif elapsed >= 36500 and persistent.monika_anniversary < 100:
        $ persistent.monika_anniversary = 100
        $pushEvent(anni_100)
    elif elapsed >= 18250 and persistent.monika_anniversary < 50:
        $ persistent.monika_anniversary = 50
        $pushEvent(anni_50)
    elif elapsed >= 7300 and persistent.monika_anniversary < 20:
        $ persistent.monika_anniversary = 20
        $pushEvent(anni_20)
    elif elapsed >= 3650 and persistent.monika_anniversary < 10:
        $ persistent.monika_anniversary = 10
        $pushEvent(anni_10)
    elif elapsed >= 1825 and persistent.monika_anniversary < 5:
        $ persistent.monika_anniversary = 5
        $pushEvent(anni_5)
    elif elapsed >= 1460 and persistent.monika_anniversary < 4:
        $ persistent.monika_anniversary = 4
        $pushEvent(anni_4)
    elif elapsed >= 1095 and persistent.monika_anniversary < 3:
        $ persistent.monika_anniversary = 3
        $pushEvent(anni_3)
    elif elapsed >= 730 and persistent.monika_anniversary < 2:
        $ persistent.monika_anniversary = 2
        $pushEvent(anni_2)
    elif elapsed >= 365 and persistent.monika_anniversary < 1:
        $ persistent.monika_anniversary = 1
        $pushEvent(anni_1)
    elif persistent.monika_reload <= 3:
        $pushEvent("ch30_reload_" + str(persistent.monika_reload))
    else:
        #pick a random greeting
        $pushEvent(renpy.random.choice(greetings_list))
    $ persistent.monika_reload += 1
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False
    #Add keys for new functions
    $ config.keymap["open_dialogue"] = ["t"]
    $ config.keymap["change_music"] = ["m"]
    $ config.keymap["play_pong"] = ["p"]
    # Define what those actions call
    $ config.underlay.append(renpy.Keymap(open_dialogue=show_dialogue_box))
    $ config.underlay.append(renpy.Keymap(change_music=select_music))
    $ config.underlay.append(renpy.Keymap(play_pong=start_pong))
    jump ch30_loop

label ch30_loop:
    $ quick_menu = True
    if is_morning():
        if morning_flag != True:
            show room_mask as rm:
                size (320,180)
                pos (30,200)
            show room_mask2 as rm2:
                size (320,180)
                pos (935,200)
            show monika_transparent_day_bg
            with dissolve
            $ morning_flag = True
    elif not is_morning():
        if morning_flag != False:
            $ morning_flag = False
            scene black
            show room_mask as rm:
                size (320,180)
                pos (30,200)
            show room_mask2 as rm2:
                size (320,180)
                pos (935,200)
            show monika_bg
            with dissolve
            show monika_bg_highlight
    $ persistent.autoload = "ch30_autoload"
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False

    #Call the next event in the list
    $event_output = callNextEvent()
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0

    #If there's no event in the queue, add a random topic as an event
    if not event_output:
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

    jump ch30_loop


label ch30_monikatopics:
    python:
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

    jump ch30_loop
