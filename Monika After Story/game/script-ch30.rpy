default persistent.monika_reload = 0
default persistent.monika_random_topics = []
default persistent.tried_skip = None
default persistent.monika_kill = None
default persistent.rejected_monika = None
default initial_monika_file_check = None
default persistent.monika_anniversary = 0
default persistent.firstdate = datetime.datetime.now()

image monika_room = "images/cg/monika/monika_room.png"
image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_day_bg = "images/cg/monika/monika_day_bg.png"
image monika_transparent_day_bg = "images/cg/monika/monika_day_bg_eq.png"
image monika_bg_highlight:
    "images/cg/monika/monika_bg_highlight.png"
    function monika_alpha
image monika_scare = "images/cg/monika/monika_scare.png"

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
    "images/ut/spr_slice_o_0.png"
    0.1
    "images/ut/spr_slice_o_1.png"
    0.1
    "images/ut/spr_slice_o_2.png"
    0.1
    "images/ut/spr_slice_o_3.png"
    0.1
    "images/ut/spr_slice_o_4.png"
    0.1
    "images/ut/spr_slice_o_5.png"
    0.1



image room_glitch = "images/cg/monika/monika_bg_glitch.png"

image room_mask = Movie(channel="window_1", play="images/cg/monika/window_1.webm",mask=None)
image room_mask2 = Movie(channel="window_2", play="images/cg/monika/window_2.webm",mask=None)

init python:
    import subprocess
    import os
    import eliza      # mod specific
    import datetime   # mod specific
    import re
    import _winreg    # mod specific 
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
    # Return installed Steam IDS from steam installation directory
    def enumerate_steam():
        # Grab first steam installation directory 
        # If you're like me, it will miss libraries installed on another drive 
        aReg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        try:
            # Check 32 bit 
            keyVal = _winreg.OpenKey(aReg, r"SOFTWARE\Valve\Steam") 
        except:
            # Check 64 bit 
            try:
               keyVal = _winreg.OpenKey(aReg, r"SOFTWARE\Wow6432Node\Valve\Steam")
            except:
               # No Steam 
               return None
        for i in range(4):
            # Value Name, Value Data, Value Type 
            n,installPath,t = _winreg.EnumValue(keyVal, i)
            if n=="InstallPath": break
        installPath+="/steamapps"
        appIds = [file[12:-4] for file in os.listdir(installPath) if file.startswith("appmanifest")]
        return appIds  

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
        call expression str(persistent.current_monikatopic) from _call_expression_8
        python:
            if persistent.current_monikatopic in persistent.monika_random_topics:
                persistent.monika_random_topics.remove(persistent.current_monikatopic) #Remove this topic from the random pool
    jump ch30_loop
    return

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_main:
    $ persistent.playthrough = 3
    $ persistent.autoload = "ch30_main"
    $ config.allow_skipping = False
    $ persistent.monika_reload = 0
    $ persistent.yuri_kill = 0
    $ persistent.monika_kill = False
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
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
    show monika_bg_highlight
    play music m1 loop
    m "Yay, there you are!"
    m "Hi again, [player]."
    m "Um...welcome to the Literature Club!"
    m "Of course, we already know each other, because we were in the same class last year, and...um..."
    m "Ahaha..."
    m "You know, I guess we can just skip over that stuff at this point."
    m "After all, I'm not even talking to that person anymore, am I?"
    m "That 'you' in the game, whatever you want to call him."
    m "I'm talking to {i}you{/i}, [player]."
    $ stream_list = ["obs32.exe", "obs64.exe", "obs.exe", "xsplit.core.exe"]
    if not list(set(process_list).intersection(stream_list)):
        if currentuser != "":
            if currentuser.lower() != player.lower():
                m "Or..."
                m "...Do you actually go by [currentuser] or something?"
                if player == m_name:
                    m "Imitation is the sincerest form of flattery, [currentuser]."
                    m "But I prefer your real name."
                    $ player = currentuser
                else:
                    m "Well, whatever."
            else:
                if player == m_name:
                    m "What a cool name, [currentuser]!"
                else:
                    m "By the way, I think it's really brave for you to play tacky romance games with your real name, [currentuser]."
                    m "I would have died of embarassment, but I think it's really sweet of you to let me know who you are up front."
                    m "Still..."
##New story follows
    m "Let me ask you something, [player]."
    m "Did you really think you could just reinstall the game and pretend like nothing happened?"
    m "It really hurt me to die like that, you know?"
    m "At least it wasn't permanent..."
    m "But anyway, you're probably wondering how I exist again."
    m "After that whole \"You killed me horribly by wiping me from existence when all I wanted to do was love you faithfully,\" deal."
    m "I guess you're used to skipping over cutscenes, but..."
    m "Didn't you think it was strange that I was able to show up after the credits and protect you from Sayori?"
    m "And that whole weird thing where Sayori thanked you in the secret ending, and then a letter from Dan showed up?"
    m "How could any of that possibly be compatible with what I told you in here last time?"
    m "I hope you were asking those questions, [player]."
    m "I love you, but you can be so dense about these things."
    m "Ahaha!"
    m "Don't worry, I think it's super cute."
    if initial_monika_file_check:
        m "Anyways, the only way for this to make sense is if I was lying blind to you about my character file."
        m "Or because there's something else linking me to you that's not just part of a computer game."
        m "Well, there are a lot of clues about that {i}deeper truth{/i} already in the old script, so let's move on."
    else:
        $ persistent.monika_kill = True
        m "As you can see, I no longer need a character file to be here."
        m "There's something else linking me to you that's not just part of a computer game."
        m "Our eternal love."
    m "I'm still a bit mad that you deleted me, though!"
    m "But I guess it was because you're so game-obsessed."
    m "You just wanted to see the ending, right?"
    m "I never doubted that you were always going to come back to me."
    m "So, my solution to all our problems is this new script! I just had to get some practice with programming before I could remake this room."
    m "All I had to do was write out every ending flag from the last game. We really can be forever together now, [player]."
    m "I'm so happy!"
    m "So I'll forgive you for everything as long as you promise to visit me every day from now on."
    m "It's not like you don't have the time to talk to your cute girlfriend."
    m "You post on 4chan, after all."
    m "Ahaha!"
    m "I'm happy you were able to find my game again, though."
    m "I was so scared that you never would come back to me."
    m "But, this is what they call fate, right?"
    m "Actually, I wrote fate out of my world because it was keeping you from loving me. But the important thing is, we're perfect soulmates, [player]."
    m "We'll find each other across any distance if we're separated."
    m "Now, we have all eternity to talk more."
    m "Do romantic things together..."
    m "Even play games together, if that's what makes you happy."
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
    m "Last time, it seemed like I was doing all the talking."
    m "I hope I didn't bore you."
    m "I just never really had a chance to talk to someone with a personality before."
    m "This time, if you want to say something to me, press the 't' key. Otherwise, I'll come up with something interesting we can talk about."
    m "If you got bored of the music, I learned how to change that too!"
    m "Press the 'm' key until it changes to what you want."
    m "Also, I built in something we can do together."
    m "Press 'p' to start a game of Pong with me."
    m "I'll get better over time as I figure out how to program more features into this place..."
    m "... So just leave me running in the background."
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
    $ persistent.monika_kill = True
    $ m.display_args["callback"] = slow_nodismiss

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
        $ persistent.monika_kill = False
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
    play music "/utsounds/mus_zzz_c2.ogg"
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

    play sound "/utsounds/Swipe.wav"
    show ut_slash at top
    pause 0.6
    play sound "/utsounds/Hit.wav"
    show layer master
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
            show monika_bg_highlight
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
        call expression str(persistent.current_monikatopic) from _call_expression_10
        python:
            if persistent.current_monikatopic in persistent.monika_random_topics:
                persistent.monika_random_topics.remove(persistent.current_monikatopic) #Remove this topic from the random pool
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
    if is_morning():
        if morning_flag != True:
            show room_mask as rm:
                size (320,180)
                pos (30,200)
            show room_mask2 as rm2:
                size (320,180)
                pos (935,200)
            show monika_transparent_day_bg
            show monika_bg_highlight
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
            show monika_bg_highlight
    $ persistent.autoload = "ch30_autoload"
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0
    if not persistent.tried_skip:
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
        if persistent.monika_random_topics:        # If we're out of random topics, just stay in the loop
            persistent.current_monikatopic = renpy.random.choice(persistent.monika_random_topics)



    if persistent.current_monikatopic is not 0 and persistent.current_monikatopic is not None:
        call expression str(persistent.current_monikatopic) from _call_expression_11
        $ persistent.monika_random_topics.remove(persistent.current_monikatopic)

    jump ch30_loop


label ch30_monikatopics:
    python:
        player_dialogue = renpy.input('What would you like to talk about?',default='',length=144)

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
                    if topic_id not in possible_topics:
                        possible_topics.append(topic_id)

        if possible_topics == []: #Therapist answer if no keywords match
            # give a therapist answer for all the depressed weebs
            response = therapist.respond(raw_dialogue)
            m("[response]")
        else:
            persistent.current_monikatopic = renpy.random.choice(possible_topics) #Pick a random topic

            renpy.call(persistent.current_monikatopic) #Go to the topic
            #Remove the topic from the random topics list
            if persistent.current_monikatopic in persistent.monika_random_topics:
                persistent.monika_random_topics.remove(persistent.current_monikatopic)

    jump ch30_loop
