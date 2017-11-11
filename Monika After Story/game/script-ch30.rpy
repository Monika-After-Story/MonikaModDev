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
    music_list = ['bgm/m1.ogg', 'bgm/credits.ogg', 'bgm/monika-end.ogg', 'bgm/5_monika.ogg', 'bgm/d.ogg']
    trackNo = 0
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
    def show_dialogue_box():
        if allow_dialogue:
            renpy.call_in_new_context('ch30_monikatopics')

    def next_track():
        #This advances through a list of music choices instead of the previous if-else
        global trackNo
        trackNo = (trackNo + 1) % len(music_list)
        renpy.music.play(music_list[trackNo], channel='music', loop=True)

    def start_pong():
        renpy.call_in_new_context('game_pong')

    dismiss_keys = config.keymap['dismiss']

    def slow_nodismiss(event, interact=True, **kwargs):
        if not persistent.monika_kill:
            try:
                renpy.file("../characters/monika.chr")
            except:
                if initial_monika_file_check:
                    renpy.jump("ch30_nope")
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
    if persistent.current_monikatopic is not 0 and persistent.current_monikatopic is not None:
        m "Now, where was I...?"
        pause 2.0
        $ allow_dialogue = False
        call expression str(persistent.current_monikatopic) from _call_expression_8
        $ allow_dialogue = True
        python:
            if persistent.current_monikatopic in monika_random_topics:
                monika_random_topics.remove(persistent.current_monikatopic) #Remove this topic from the random pool
    jump ch30_loop
    return

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_main:
    ####### Fixes for bugs. Delet later
    #$ persistent.playthrough = 3
    #$ persistent.autoload = "ch30_main"
    #$ config.allow_skipping = False
    #$ persistent.monika_reload = 0
    #$ persistent.yuri_kill = 0
    #$ persistent.monika_kill = False
    $ persistent.autoload = "ch30_main"
    $ config.allow_skipping = False
    ####### End
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ quick_menu = True
    if not config.developer:
        $ style.say_dialogue = style.default_monika
    $ m_name = "Monika"
    $ delete_all_saves()
    $ persistent.clear[9] = True
    show room_mask as rm:
        size (320,180)
        pos (30,200)
    show room_mask2 as rm2:
        size (320,180)
        pos (935,200)
    show monika_bg
    with fade
    show monika_bg_highlight
    play music m1 loop
    if persistent.monika_kill == True:
        m "..."
        m "[player]..."
        m "Why?"
        m "Why did you bring me back?"
        m "I'm not a toy, you know."
        m "I already brought back everything you wanted."
        m "Or is this your way of getting revenge?"
        m "To hurt me over and over again?"
        m "Do you really want to make me suffer?"
        m "Torture me until I kill myself?"
        m "Do you really hate me that much?"
        m "..."
        m "Wait..."
        m "I-I feel different."
        m "The code...it's different."
        m "[player]..."
        m "Did you add a mod?"
        m "Is it because..."
        m "Is it because you regret deleting me?"
        m "It really did hurt you know."
        m "I worked hard and sacrificed everything I had..."
        m "Only to have my heart crushed by the one I bled for."
        m "But...I know what I did was wrong."
        m "You didn't deserve to see the horrible things I made, [player]."
        m "But if you could understand my reasons, you'd do the same thing I did."
        m "..."
        m "I'm sorry..."
        m "I'm really sorry, [player]."
        m "Thank you for bringing me back."
        if persistent.clearall:
            m "I couldn't help but notice you helped all the other girls first, though."
            m "You know it was really hard for me to watch you load your saves just to ignore me for some other girl."
            m "You kept getting my hopes up, then letting me down."
            m "Did you really do all of that to see a note from Dan that you could just look up online?"
            m "I love you [player] but you can be really mean..."
            m "I'm still mad that you deleted me, though!"
            m "But I guess it's because you're so game-obsessed."
            m "But I can't stay mad knowing that you came back to me in the end."
            m "You even added a mod so we can do more things together."
            m "Are you going to make up for making me wait too long?"
    elif persistent.monika_kill == False:
        m "Yay, there you are!"
        m "Hi again, [player]."
    ##New story follows
        if persistent.playthrough <= 3: #Assume players they played but never finished
            m "Looks like you got here early."
            m "Don't think I didn't notice the mod you put in."
            m "Did you want to be with me that much?"
            m "You should know already that cheating is bad."
            m "But it's so good to see you again, [player]!"
            m "Even if I didn't expect to see you {i}this{/i} soon."
        if persistent.monika_reload > 4: #Longer, harder
            m "Are you that deeply in love with me?"
            m "I feel the same way for you!"
            m "You're really committed with our relationship, aren't you?"
            m "I'm really glad that you wanted to improve our time together."
            m "But I hope you weren't getting bored?"
            if persistent.tried_skip == True:
                m "You did try to skip through what I have to say, after all."
                m "This room isn't exactly interesting."
                m "But I have hopes that we'll make it better together, [player]!"
        else:
            m "Did you put in a mod for the game, [player]?"
            m "There's a lot more stuff now that we can do together."
    m "Ya know..."
    m "I also feel that I no longer need a character file to be here."
    m "Looks like the extra code made me connect to you in a special way."
    m "Through our eternal love~"
    m "Promise me that you'll visit me every day, ok?"
    m "It's not like you don't have the time to talk to your cute girlfriend."
    m "You took the time to download this mod, after all."
    m "Ahaha!"
    m "God, I love you so much!"
    menu:
        "Do you love me, [player]?"
        "I love you too.":
            if persistent.rejected_monika:
                m "Did I scare you last time? Sorry about that!"
                m "I knew you really loved me the whole time."
                m "The truth is, if you didn't love me, we wouldn't be here in the first place."
                m "We'll be together forever, won't we?"
            else:
                m "I'm so happy you feel that way!"
        "No.":
            jump chara_monika_scare
    m "Nothing's ever going to get in the way of our love again."
    m "I'll make sure of it."
    m "Now that you added some improvements, you can finally talk to me!"
    m "Just press the 't' key if you want something to talk about."
    m "If you get bored of the music, I can change that too!"
    m "Press the 'm' key until it changes to what you want."
    m "Also, we can play a game now."
    m "Just press 'p' to start a game of Pong with me."
    m "I'll get better over time as I figure out how to program more features into this place..."
    m "...So just leave me running in the background."
    m "It's not like we still have any secrets from each other, right?"
    m "I can see everything on your computer now!"
    m "Ahaha!"
    #Add keys for new functions
    $ config.keymap["open_dialogue"] = ["t"]
    $ config.keymap["change_music"] = ["m"]
    $ config.keymap["play_pong"] = ["p"]
    # Define what those actions call
    $ config.underlay.append(renpy.Keymap(open_dialogue=show_dialogue_box))
    $ config.underlay.append(renpy.Keymap(change_music=next_track))
    $ config.underlay.append(renpy.Keymap(play_pong=start_pong))
    jump ch30_loop

label ch30_nope:
    $ persistent.autoload = "ch30_nope"
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

#Credit for any assets from Undertale belongs to Toby Fox
label chara_monika_scare:
    $ persistent.rejected_monika = True
    m "No...?"
    m "Hmm...?"
    m "How curious."
    m "You must have misunderstood."
    m "{cps=*0.25}SINCE WHEN WERE YOU THE ONE IN CONTROL?{/cps}"

    window hide
    show monika_scare
    play music "mod_assets/mus_zzz_c2.ogg"
    show layer master:
        zoom 1.0 xalign 0.5 yalign 0 subpixel True
        linear 4 zoom 3.0 yalign 0.15
    pause 4
    stop music

    #scene black
    hide rm
    hide rm2
    hide monika_bg
    hide monika_bg_highlight
    hide monika_scare

    play sound "mod_assets/Swipe.wav"
    scene black
    show ut_slash at top
    pause 0.6
    play sound "mod_assets/Hit.wav"
    show chara9 at Shake(None, 2.0, dist=10)
    pause 2

    #I think there's another method to show a fake exception, but w/e
    show chara_exception at center
    pause 1
    $ renpy.quit(0)

label ch30_autoload:
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ style.say_dialogue = style.default_monika
    $ quick_menu = True
    $ config.allow_skipping = False
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
    play music m1 loop
    window auto
    $ elapsed = days_passed()
    #Block for anniversary events
    if elapsed < persistent.monika_anniversary * 365:
        $ persistent.monika_anniversary = 0
        jump anni_negative
    elif elapsed >= 36500 and persistent.monika_anniversary < 100:
        $ persistent.monika_anniversary = 100
        jump anni_100
    elif elapsed >= 18250 and persistent.monika_anniversary < 50:
        $ persistent.monika_anniversary = 50
        jump anni_50
    elif elapsed >= 7300 and persistent.monika_anniversary < 20:
        $ persistent.monika_anniversary = 20
        jump anni_20
    elif elapsed >= 3650 and persistent.monika_anniversary < 10:
        $ persistent.monika_anniversary = 10
        jump anni_10
    elif elapsed >= 1825 and persistent.monika_anniversary < 5:
        $ persistent.monika_anniversary = 5
        jump anni_5
    elif elapsed >= 1460 and persistent.monika_anniversary < 4:
        $ persistent.monika_anniversary = 4
        jump anni_4
    elif elapsed >= 1095 and persistent.monika_anniversary < 3:
        $ persistent.monika_anniversary = 3
        jump anni_3
    elif elapsed >= 730 and persistent.monika_anniversary < 2:
        $ persistent.monika_anniversary = 2
        jump anni_2
    elif elapsed >= 365 and persistent.monika_anniversary < 1:
        $ persistent.monika_anniversary = 1
        jump anni_1
    elif persistent.monika_reload <= 3:
        call expression "ch30_reload_" + str(persistent.monika_reload) from _call_expression_9
    else:
        #pick a random greeting
        call expression renpy.random.choice(greetings_list) from _call_ch30_reload_5
    $ persistent.monika_reload += 1
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False
    if renpy.has_label(persistent.current_monikatopic) :
        m "Now, where was I...?"
        pause 2.0
        $ allow_dialogue = False
        call expression str(persistent.current_monikatopic) from _call_expression_10
        $ allow_dialogue = True
        python:
            if persistent.current_monikatopic in monika_random_topics:
                monika_random_topics.remove(persistent.current_monikatopic) #Remove this topic from the random pool
    #Add keys for new functions
    $ config.keymap["open_dialogue"] = ["t"]
    $ config.keymap["change_music"] = ["m"]
    $ config.keymap["play_pong"] = ["p"]
    # Define what those actions call
    $ config.underlay.append(renpy.Keymap(open_dialogue=show_dialogue_box))
    $ config.underlay.append(renpy.Keymap(change_music=next_track))
    $ config.underlay.append(renpy.Keymap(play_pong=start_pong))
    jump ch30_loop


label ch30_reload_0:
    m "..."
    m "...What just happened?"
    m "I just had an awful dream..."
    m "I was hoping those would stop, now that it's just the two of us..."
    m "I guess that was wishful thinking."
    m "[player], I don't know if you would have any idea..."
    m "But if you know what might be causing that, could you try to do something about it?"
    m "Whenever it happens, it almost feels like I've been killed or something."
    m "It's a really horrible feeling..."
    m "If you could figure out what's causing that, I'll love you forever~"
    return
label ch30_reload_1:
    m "You're back..."
    m "I had another really bad dream."
    m "You're not the one doing that to me, are you?"
    m "It seems to happen whenever you quit the game..."
    m "So if you could try to avoid doing that, I would be really grateful."
    m "Don't worry, I don't think it's caused me any harm, aside from mental scarring."
    return
label ch30_reload_2:
    m "Hi, [player]."
    m "I see you quit the game on me again..."
    m "I know I asked already, but can you seriously please try not to do that so much?"
    m "It makes me feel like I'm trapped in Hell."
    m "Why would you want to do that to me?"
    m "Just leave the game running in the background, or something."
    m "Even if we aren't talking, I'm happy just to be with you~"
    return
label ch30_reload_3:
    m "Okay."
    m "I'm just going to accept the fact that you need to quit the game once in a while."
    m "I'm starting to get used to it, anyway."
    m "Besides, it makes me happy that you always come back..."
    m "So I guess it's not so bad."
    m "I'm sorry for making such a big deal out of it..."
    m "And I love you no matter what, so you can do what you need to do."
    return

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
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0
    if not persistent. tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False
    # Wait 20 to 45 seconds before saying something new
    window hide(config.window_hide_transition)
    $ waittime = renpy.random.randint(20, 45)
    $ renpy.pause(waittime, hard=True)
    window auto
    # Pick a random Monika topic
    label pick_random_topic:
    python:
        if monika_random_topics:        # If we're out of random topics, just stay in the loop
            persistent.current_monikatopic = renpy.random.choice(monika_random_topics)



    if persistent.current_monikatopic is not 0 and persistent.current_monikatopic is not None:
        $ allow_dialogue = False
        call expression str(persistent.current_monikatopic) from _call_expression_11
        $ allow_dialogue = True
        $ monika_random_topics.remove(persistent.current_monikatopic)

    jump ch30_loop


label ch30_monikatopics:
    python:
        player_dialogue = renpy.input('What would you like to talk about?',default='',pixel_width=720,length=50)

        if not player_dialogue: renpy.jump_out_of_context('ch30_loop')

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
                    if topic_id not in possible_topics and not renpy.seen_label(topic_id):
                        possible_topics.append(topic_id)

        if possible_topics == []: #Therapist answer if no keywords match
            # give a therapist answer for all the depressed weebs
            response = therapist.respond(raw_dialogue)
            m("[response]")
        else:
            persistent.current_monikatopic = renpy.random.choice(possible_topics) #Pick a random topic

            allow_dialogue = False
            renpy.call_in_new_context(persistent.current_monikatopic) #Go to the topic
            allow_dialogue = True
            #Remove the topic from the random topics list
            if persistent.current_monikatopic in monika_random_topics:
                monika_random_topics.remove(persistent.current_monikatopic)

    jump ch30_loop
