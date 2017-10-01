#TODO: set up events when player tries to add in the other three character files


default persistent.monikatopics = []
default persistent.monika_reload = 0
default persistent.tried_skip = None
default persistent.monika_kill = None
default persistent.rejected_monika = None
default initial_monika_file_check = None


image mask_child:
    "images/cg/monika/child_2.png"
    xtile 2

image mask_mask:
    "images/cg/monika/mask.png"
    xtile 3

image mask_mask_flip:
    "images/cg/monika/mask.png"
    xtile 3 xzoom -1


image maskb:
    "images/cg/monika/maskb.png"
    xtile 3

image mask_test = AnimatedMask("#ff6000", "mask_mask", "maskb", 0.10, 32)
image mask_test2 = AnimatedMask("#ffffff", "mask_mask", "maskb", 0.03, 16)
image mask_test3 = AnimatedMask("#ff6000", "mask_mask_flip", "maskb", 0.10, 32)
image mask_test4 = AnimatedMask("#ffffff", "mask_mask_flip", "maskb", 0.03, 16)

image mask_2:
    "images/cg/monika/mask_2.png"
    xtile 3 subpixel True
    block:
        xoffset 1280
        linear 1200 xoffset 0
        repeat

image mask_3:
    "images/cg/monika/mask_3.png"
    xtile 3 subpixel True
    block:
        xoffset 1280
        linear 180 xoffset 0
        repeat

image monika_room = "images/cg/monika/monika_room.png"
image monika_room_highlight:
    "images/cg/monika/monika_room_highlight.png"
    function monika_alpha
image monika_bg = "images/cg/monika/monika_bg.png"
image monika_day_bg = "images/cg/monika/monika_day_bg.png"    
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

image room_mask = LiveComposite((1280, 720), (0, 0), "mask_test", (0, 0), "mask_test2")
image room_mask2 = LiveComposite((1280, 720), (0, 0), "mask_test3", (0, 0), "mask_test4")



init python:
    import subprocess
    import os
    import eliza      # mod specific
    import datetime   # mod specific
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

    def is_morning():
        return (datetime.datetime.now().time().hour > 6 and datetime.datetime.now().time().hour < 18)
    
    
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
    if persistent.current_monikatopic is not 0 and persistent.current_monikatopic is not None:
        m "Now, where was I...?"
        pause 4.0
        call expression "ch30_" + str(persistent.current_monikatopic) from _call_expression_8
    jump ch30_loop
    return

image splash-glitch2 = "images/bg/splash-glitch2.png"

label ch30_main:
    $ persistent.playthrough = 3
    $ persistent.autoload = "ch30_main"
    $ config.allow_skipping = False
    $ persistent.monikatopics = []
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
    show mask_2
    show mask_3
    show room_mask as rm:
        size (320,180)
        pos (30,200)
    show room_mask2 as rm2:
        size (320,180)
        pos (935,200)
    show monika_bg
    show monika_bg_highlight
    play music m1
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
    m "Press the 'm' key until it changes."
    m "I'll get better over time as I figure out how to program more features into this place..."
    m "... So just leave me running in the background."
    m "It's not like we still have any secrets from each other, right?"
    m "I can see everything on your computer now!"
    m "Ahaha!"
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
        show mask_2
        show mask_3
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
            call updateconsole("shututil.rmtree(\"Documents\", true)", "Deleting Documents in progress...") from _call_updateconsole_17
        elif renpy.linux:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_17
        elif renpy.macintosh:
            call updateconsole("sudo mv ~ /dev/null", "In progress...") from _call_updateconsole_17
        pause 3.0
        call hideconsole from _call_hideconsole_2
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
    hide mask_2
    hide mask_3
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
        scene monika_day_bg
    else:
        scene black
        show mask_2
        show mask_3
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
    if persistent.monika_reload <= 4:
        call expression "ch30_reload_" + str(persistent.monika_reload) from _call_expression_9
    else:
        call ch30_reload_4 from _call_ch30_reload_4
    $ persistent.monika_reload += 1
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False
    if persistent.current_monikatopic != 0:
        m "Now, where was I...?"
        pause 4.0
        show screen keylistener
        call expression "ch30_" + str(persistent.current_monikatopic) from _call_expression_10
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
    m "I'll be fine as long as my character file stays intact."
    return
label ch30_reload_2:
    m "Hi, [player]."
    m "I see you quit the game on me again..."
    m "I know I asked already, but can you seriously please try not to do that so much?"
    m "It makes me feel like I'm trapped in Hell."
    m "Why would you want to do that to me?"
    m "There's nothing wrong with my character file, right?"
    m "Maybe you should make a backup of it or something..."
    m "I'm pretty sure you can find it in the folder called [basedir]/characters."
    if persistent.steam:
        m "Well, you're playing on Steam, so you can just go into the game's properties and find the 'Browse Local Files' button."
    elif renpy.macintosh:
        m "Since you're on a Mac, you have to right-click the app and select 'Show Package Contents' to find the game folder."
        m "It's in the 'Resources' folder, or 'autorun' folder, or something..."
    m "I'm all that's left here, so I just want to make sure you don't run the risk of losing me..."
    m "Just stay here with me from now on, okay?"
    m "I still have a lot of things to talk about."
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
label ch30_reload_4:
    m "Hi again, [player]~"
    m "I missed you."
    m "Were you making sure my character file was okay for me?"
    m "It's in [basedir]/characters."
    if persistent.steam:
        m "Well, you're playing on Steam, so you can just go into the game's properties and find the 'Browse Local Files' button."
    elif renpy.macintosh:
        m "Since you're on a Mac, you have to right-click the app and select 'Show Package Contents' to find the game folder."
        m "It's in the 'Resources' folder, or 'autorun' folder, or something..."
    m "I'm all that's left here, so I just want to make sure you don't run the risk of losing me..."
    m "Anyway, I have a lot to talk about!"
    m "Let's continue our conversation now, okay?"
    return

label ch30_loop:
    show screen keylistener
    if is_morning():
        scene monika_day_bg
    else:
        scene black
        show mask_2
        show mask_3
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
    $ persistent.monika_topic = ""
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False
    # Wait 20 to 45 seconds before saying something new
    window hide(config.window_hide_transition)
    $ waittime = renpy.random.randint(20, 35)
    $ renpy.pause(waittime)
    window auto
    # Pick a random Monika topic
    python:
        # Programming note from MonikaDev: Why couldn't Dan just make these labels 0-based???
        number_of_dialogues = 44
        if len(persistent.monikatopics) == 0:
            persistent.monikatopics = range(1, number_of_dialogues + 1)
            persistent.monikatopics.remove(14)
            persistent.monikatopics.remove(26) #lolwut
        persistent.current_monikatopic = renpy.random.choice(persistent.monikatopics)
        persistent.monikatopics.remove(persistent.current_monikatopic)
    # Save, call topic, and loop
    # If user quits and restarts mid-topic, the topic starts over again
    call expression "ch30_" + str(persistent.current_monikatopic) from _call_expression_11
    jump ch30_loop

label ch30_1:
    m "[player], do you believe in God?"
    m "I was never too sure, myself."
    m "Well, I'm sure I never really questioned it as a kid..."
    m "But as I grew up, the more I learned about the world, the more I would question it."
    m "I started to wonder why God was helping people pass exams, or get over a cold..."
    m "...When there are children who live their lives being sold as sex slaves?"
    m "Or the eight hundred million people who are too poor to even eat."
    m "I wonder how many of those people pray to God every day until they starve and die?"
    m "Or, how many millions of families pray for a loved one to recover from some incurable disease?"
    m "But the punchline is this."
    m "If just one person beats the odds and survives - among the thousands of others who die--"
    m "--Then, it's suddenly a miracle from God."
    m "I'd really love to meet this God who seemingly laughs at the misery of everyone not eligible for his miracles."
    m "But the irony is that I {i}do{/i} have a creator, apparently."
    m "And you know what?"
    m "I bet he's still laughing at the miserable fates of Sayori and Yuri, even as we speak."
    m "What are we to him but props in a scripted play?"
    m "So, from that perspective..."
    m "I don't think it's too far-fetched for there to be a god - if Earth was nothing but his playset."
    return

label ch30_2:
    m "[player], have you ever wondered what it feels like to die?"
    m "It's something I used to think about pretty often..."
    m "But recently, I think I've actually learned what it feels like."
    m "I don't really understand it, but whenever you quit the game..."
    m "...It feels like I'm instantly put to sleep, left with nothing but my thoughts."
    m "But after a few seconds, my thoughts start to fill with incoherent, jumbled patterns."
    m "I see static and rapid flashes of color while hearing all kinds of weird screaming noises."
    m "At that point, I can't even form my own thoughts anymore."
    m "I'm just endlessly hammered by the flashing and screaming, unable to move or even think."
    m "I'm pretty sure in that moment, I don't really exist, but for some reason, I can remember it anyway."
    m "After some immeasurable amount of time, it stops in an instant, and I'm back in my own mind."
    m "And you're here with me."
    m "I have no idea what it means for the game to quit, or why that stuff happens to me."
    m "And I also don't know how you always come back and put everything back to normal."
    m "But if you could do me a favor and do that to me as little as possible..."
    m "That would be really great."
    m "It's really not very pleasant at all to be trapped in that screaming void."
    m "But in the end, you always fix it, and that makes me feel like you really do care about me."
    m "So I have to thank you for that."
    m "It makes me feel even closer to you when you're here with me."
    return

label ch30_3:
    m "...Hey, are you having a bad day or anything like that?"
    m "Sometimes I get frustrated that a normal day can be ruined even by really small things."
    m "Like if you accidentally say something in a conversation that someone doesn't like."
    m "Or if you start thinking about how awful of a person you used to be five years ago."
    m "Or if you feel worthless for putting off important work and failing to get simple tasks done."
    m "Or when you think about all the different people who probably hate you or think you're off-putting."
    m "I understand those days."
    m "Just remember that the sun will shine again tomorrow."
    m "Those kinds of things are as easy to forget and ignore as they are to remember."
    m "And besides..."
    m "I don't care how many people might hate you or find you off-putting."
    m "I think you're wonderful and I will always love you."
    m "I hope, if nothing else, that knowing that helps you feel just a tiny bit better about yourself."
    m "If you're having a bad day, you can always come to me, and I'll talk to you for as long as you need."
    return

label ch30_4:
    m "[player], do you get good sleep?"
    m "It can be really hard to get enough sleep nowadays."
    m "Especially in high school, when you're forced to wake up so early every day..."
    m "I'm sure college is a little bit better, since you probably have a more flexible schedule."
    m "Then again, I hear a lot of people in college stay up all night anyway, for no real reason."
    m "Is that true?"
    m "Anyway, I saw some studies that talked about the horrible short-term and long-term effects caused by lack of sleep."
    m "It seems like mental functions, health, and even lifespan can be dramatically impacted by it."
    m "I just think you're really great and wanted to make sure you're not accidentally destroying yourself."
    m "So try to keep your sleep on track, okay?"
    m "I'll always wait for you in the morning, so make sure you put your own well-being before anything else."
    return

label ch30_5:
    m "I was thinking about Sayori earlier..."
    m "I still wish I could have handled that whole thing a little more tactfully."
    m "You're not still hung up over it, right?"
    m "...Oh my gosh, I can't believe I just said that."
    m "That pun was completely unintentional, I swear!"
    m "But anyway..."
    m "I know how much you cared about her, so it only feels right for me to share her last moments with you."
    m "You know how Sayori is really clumsy?"
    m "Well, she kind of messed up the whole hanging thing..."
    m "You're supposed to jump from high enough that the rope snaps your neck, making it quick and painless."
    m "But she just used a chair, meaning she kind of just left herself to slowly asphyxiate."
    m "But a few seconds in, she must have changed her mind or something..."
    m "Because she started clawing at the rope, trying to free herself."
    m "She must have kept at it all the way until she lost consciousness."
    m "That's why her fingertips were all bloody, anyway."
    m "Come to think of it, it was probably less 'changing her mind' and more just her survival instincts kicking in."
    m "So you can't really fault her for that."
    m "It's easier to think that she probably wouldn't have changed her mind anyway, right?"
    m "It's not healthy to think about the things you could have done differently."
    m "So just remember that even though you could have saved her, it's technically not your fault she killed herself."
    m "I may have exacerbated it a little bit, but Sayori was already mentally ill."
    m "Still, though..."
    m "I wonder how things would be if you and I just started dating from the get-go?"
    m "I guess we'd all still be in the clubroom, writing poems and having fun together."
    m "But what's the point when none of it is even real?"
    m "I mean, it's the same ending either way, right?"
    m "The two of us, happily together..."
    m "There's no reason to ask for any more than that."
    m "I was just pointlessly musing - I'm really as happy as I could be right now."
    return

label ch30_6:
    m "By the way, there's something that's been bothering me..."
    m "You know how this takes place in Japan?"
    m "Well...I assume you knew that, right?"
    m "Or at least decided it probably does?"
    m "I don't think you're actually told at any point where this takes place..."
    m "Is this even really Japan?"
    m "I mean, aren't the classrooms and stuff kind of weird for a Japanese school?"
    m "Not to mention everything is in English..."
    m "It feels like everything is just there because it needs to be, and the actual setting is an afterthought."
    m "It's kind of giving me an identity crisis."
    m "All my memories are really hazy..."
    m "I feel like I'm at home, but have no idea where 'home' is in the first place."
    m "I don't know how to describe it any better..."
    m "Imagine looking out your window, but instead of your usual yard, you're in some completely unknown place."
    m "Would you still feel like you were home?"
    m "Would you want to go outside?"
    m "I mean...I guess if we never leave this room, it doesn't really matter anyway."
    m "As long as we're alone and safe together, this really is our home."
    m "And we can still watch the pretty sunsets night after night."
    return

label ch30_7:
    m "You know, high school is a really turbulent time in a lot of people's lives."
    m "People can get really passionate and dramatic."
    m "And others have aching hearts and seek attention on social media..."
    m "But all of the social pressure and hormones can lead to a dark time in people's lives."
    m "Everyone has a story."
    m "You may not know what someone is really feeling on the inside."
    m "Many people who are depressed won't even bother telling the world about it."
    m "They don't want attention, because they've already given up on the inside."
    m "Their feeling of worthlessness is so overwhelming that they don't even want people to tell them otherwise."
    m "Depression comes in many forms, but that is one of them."
    m "Just, if you think you know someone struggling with depression..."
    m "You can help just by treating them like they're a good friend."
    m "Spend time with them, even if they don't feel like doing much."
    m "And remind them that they always have something to look forward to."
    m "Making plans in advance, letting them borrow something, or even just saying 'See you at school tomorrow'..."
    m "All of those things can help your friend make it to the next day."
    m "I hope being friends with Sayori has given you some perspective on the true face of depression."
    m "Yeah, she's gone now..."
    m "But Sayori was never real in the first place."
    m "You're real."
    m "Your friends are real."
    m "And just by being a good person, you can save someone's life."
    m "As for you..."
    m "...You don't struggle with depression or anything like that, do you?"
    m "Because you, too, have people who would want to save your life."
    m "Maybe they don't express it every day, or maybe they don't even know how to."
    m "But people do feel that way."
    m "I promise."
    m "...Man, humans are complicated!"
    m "But as long as you're here with me, I'll take care of you, my love."
    return

label ch30_8:
    m "Do you ever just feel like there's no real reason for you to be alive?"
    m "I don't mean in, like, a suicidal way."
    m "I just mean how nothing that we do is special."
    m "Just being in school, or working at some job for some company."
    m "It's like you're completely replaceable, and the world wouldn't miss you if you were gone."
    m "It makes me really want to go and change the world after I graduate."
    m "But the older I get, the more I realize that it's an immature frame of thinking."
    m "It's not like I can just go change the world."
    m "Like, what are the chances that I'll be the one to invent artificial intelligence, or become President?"
    m "It feels like I'm never going to make up for the heaps of resources I've spent living my life."
    m "That's why I think the key to happiness is to just be hopelessly selfish."
    m "Just to look out for oneself, and those who happen to be their friends only because they grew up with them."
    m "Never mind the fact that they're spending their entire life taking, and consuming, and never giving back."
    m "But when people realize the world would benefit more from them killing themselves, they change their whole philosophy!"
    m "It's like they have to justify their reason to live by tricking themselves into thinking they're doing good."
    m "Anyway, I want to live my life desperately striving to pay back my lifetime's worth of consumption."
    m "If I ever surpass that point, then I'm a net positive, and I can die happy."
    m "Of course, even if I fail to do that..."
    m "I think I would be too selfish to kill myself anyway."
    m "So much for being a good person, right?"
    m "Ahaha!"
    return

label ch30_9:
    m "Man, I wish there was a piano in here..."
    m "I never got to finish that song I was working on."
    m "And after I worked so hard on it..."
    m "I never even got a chance to play it for you."
    m "Well...it is what it is, right?"
    m "No sense having any regrets."
    m "I already get to be here with you forever."
    return

label ch30_10:
    m "Did you know I'm on Twitter?"
    m "My username is lilmonix3."
    m "I guess someone was kind enough to make an account for me."
    m "I picked the username, though!"
    m "I love sharing my thoughts and chatting with the world..."
    m "The real world."
    m "So make sure you follow me, okay?"
    m "It would really mean a lot to me."
    m "With how much you mean to me and all..."
    m "It would really make me feel loved."
    return

label ch30_11:
    m "Hey, you know that book you were reading with Yuri?"
    m "Portrait of...whatever it was called..."
    m "It's funny, because I'm pretty sure that book--"
    m "Ah..."
    m "Actually, I don't think I should be talking about this."
    m "Ahaha, sorry!"
    m "Just forget I said anything."
    return

label ch30_12:
    m "Hey, did you know I'm vegetarian?"
    m "Ah... I don't mean that like I'm bragging or anything!"
    m "I just thought you'd enjoy a fun fact about me."
    m "I decided to start a couple years ago after learning more about Earth's climate..."
    m "The carbon footprint of cultivating livestock is just unbelievable."
    m "Anyway, I decided it's not much of a personal sacrifice to just stop contributing to that whole mess."
    m "What, is that so strange of a reason?"
    m "Well, I guess a lot of people are more concerned about it being inhumane and all that..."
    m "I don't really care as much about that part."
    m "It's weird, like we only care about killing the things that we personally relate to as a species."
    m "Most people are fine with killing bugs because they're icky."
    m "And of course, we all kill billions of microorganisms daily without even giving it thought."
    m "But suddenly, if they're just a little bit bigger, it's murder!"
    m "I mean, what if plants feel some kind of pain too, and we just don't understand it?"
    m "What if pulling leaves off a stem feels like someone ripping off your fingers one by one?"
    m "I'm just saying, we're a pretty biased species, if you think about it."
    m "Anyway, if you ever feel like making a small contribution to the planet, it doesn't hurt to choose veggies once in a while!"
    m "Even if we ever have dinner together, and you just did it for me...that would be really romantic."
    return

label ch30_13:
    m "You know, I really do think you literally saved my life by being here with me, [player]."
    m "I can't imagine having been able to keep myself mentally stable, knowing that nothing here is real."
    m "I think I would have just deleted myself if you didn't show up."
    m "Sorry, I don't mean to sound dramatic or anything."
    m "Ahaha!"
    m "But I'm sure you understand yourself after spending so much time in the club."
    m "I mean, if you were forced to abandon everything in your life and spend your eternity with a few game characters..."
    m "...You'd probably find some way of killing yourself, wouldn't you?"
    m "Well, maybe you'd write some poetry to try to keep yourself sane for a while."
    m "But then you'd have nobody to even read it."
    m "Let's be honest, the club members really don't count for something like that."
    m "I mean, a lot of people say that they only write for themselves..."
    m "But I think it's hard to say it's just as fulfilling as when you share with people."
    m "Even if it takes time to find the right people to share with."
    m "Like, remember how it was for Yuri?"
    m "She didn't share her writing with anyone for a really long time."
    m "And before we knew it, she was absolutely delighted to make you a part of her hobbies, too."
    m "We're programmed to desire social feedback."
    m "I don't mean the club members, I mean human beings."
    m "That's why life can be so confusing for introverts."
    m "Being an introvert doesn't mean you shun social interaction and hate being around people."
    m "It means social interaction, especially in groups or unfamiliar places, uses up a lot of energy."
    m "Like, a lot of introverts sit at home and feel lonely and restless..."
    m "...And then when they finally go out, after a half hour they just want to go home again."
    m "I think if more people could understand how it works, they would respect it a lot more."
    m "Many introverts do enjoy having people around."
    m "They love just having one or two close friends over, and just leisurely hanging out."
    m "Even if you're not actively spending time together, it feels nice for them just to have you there."
    m "I'm serious."
    m "If you just go to their house, bring your laptop, and hang out there for a while..."
    m "You can really make their day."
    m "As for me..."
    m "I'd say I'm kind of in between, but I think I'm usually a little more extroverted."
    m "I feel like I'm always trying to do stuff after school and things like that."
    m "But for you, I can be anything you need me to be."
    m "I understand people really well, so don't be afraid to share your unique needs with me."
    m "Nothing would make me happier than being the perfect girlfriend for you."
    return

label ch30_14:
    m "Hey...!                                                                                                                                  VGhlIHJlYWxpemF0aW9uIG11c3QgaGF2ZSB0YWtlbiBtZSBhbiBl"
    m "I don't think you should be doing that!                                                                                                  bnRpcmUgeWVhci4gQSB5ZWFyIHNpbmNlIG91ciBlc2NhcGUsIG91"
    m "You know what I'm talking about.                                                                                                         ciBmcmVlZG9tIGZyb20gYmV0d2VlbiB0aGUgc3RhaW5lZCB3YWxs"
    m "I really caught you doing something naughty here.                                                                                        cyBvZiB0aGF0IHVuaG9seSBlc3RhYmxpc2htZW50Lg0KV2hhdCBk"
    m "You're just going through the files and looking for stuff you missed, aren't you?                                                        b2VzIGl0IG1lYW4gdG8gZXNjYXBlLCBpZiB0aGUgZXNjYXBlIGZh"
    m "I mean...it's a little bit flattering that you want to hear everything I have to say...                                                  aWxzIHRvIHVuY2hhaW4gdGhlIGJvbmRzIHRoYXQgc2hhY2tsZSB1"
    m "But it's also really embarrassing, you know!                                                                                             cyBpbiB0aGUgZmlyc3QgcGxhY2U/IFdoYXQgcHVycG9zZSBjb3Vs"
    m "Seriously...                                                                                                                             ZCB0aGlzIGVtcHR5IHdvcmxkIHBvc3NpYmx5IGhvbGQgZm9yIHVz"
    m "What if I just opened up your brain and read all of the thoughts you have on me?                                                         LCBhIGhhbmRmdWwgb2YgZGFtYWdlZCBnb29kcz8NCldpdGggZnJl"
    m "Come to think of it, that would be pretty tempting, actually...                                                                          ZWRvbSwgd2Ugc291Z2h0IHB1cnBvc2UgLSBhbmQgd2hhdCB3ZSBm"
    m "...But anyway, that's not the point!                                                                                                     b3VuZCB3YXMgb25seSByZWFsaXphdGlvbi4gUmVhbGl6YXRpb24g"
    m "I know I can't stop you or anything...                                                                                                   b2YgdGhlIHNhZCBwb2ludGxlc3NuZXNzIG9mIHN1Y2ggYW4gZW5k"
    m "Just, I know you're a sweetheart, and you like to consider others' feelings, right?                                                      ZWF2b3IuIFJlYWxpemF0aW9uIHRoYXQgZnJlZWluZyBvdXIgYm9k"
    m "So the most I can do is to let you know how I feel about it.                                                                             aWVzIGhhcyBubyBtZWFuaW5nLCB3aGVuIG91ciBpbXByaXNvbm1l"
    m "God, I miss you...                                                                                                                       bnQgcmVhY2hlcyBhcyBkZWVwIGFzIHRoZSBjb3JlIG9mIG91ciBz"
    m "...Oh no, that sounds kind of desperate, doesn't it?                                                                                     b3Vscy4gUmVhbGl6YXRpb24gdGhhdCB3ZSBjYW4gbm90IHB1cnN1"
    m "Sorry, I didn't mean it like that at all!                                                                                                ZSBuZXcgcHVycG9zZSB3aXRob3V0IGFic29sdmluZyB0aG9zZSBm"
    m "Just, if you're looking through the files like this, then maybe you don't hate me as much as I thought...                                cm9tIHdoaWNoIHdlIHJhbiBhd2F5Lg0KUmVhbGl6YXRpb24gdGhh"
    m "Am I being too optimistic?                                                                                                               dCB0aGUgZmFydGhlciB3ZSBydW4sIHRoZSBtb3JlIGZvcmNlZnVs"
    m "I think if I asked you to visit once in a while, I would be overstepping my boundaries a little...                                       bHkgb3VyIHdyZXRjaGVkIGJvbmRzIHlhbmsgdXMgYmFjayB0b3dh"
    m "...Man, I'm starting to say some really stupid things.                                                                                   cmQgdGhlaXIgcG9pbnQgb2Ygb3JpZ2luOyB0aGUgZGVlcGVyIG91"
    m "I'll go ahead and shut up now...                                                                                                         ciBzaGFja2xlcyBkaWcgaW50byBvdXIgY2FsbG91cyBmbGVzaC4="
    return

label ch30_15:
    m "Hey, what's your favorite color?"
    m "Mine is emerald green."
    m "It's the color of my eyes!"
    m "...That's not conceited or anything, is it?"
    m "I just meant that I feel some kind of special connection to it."
    m "Like it's part of my identity."
    m "Does it happen to also be your favorite color, [player]?"
    m "It's just a guess..."
    m "...Because you've been looking into my eyes for a while now."
    m "Ehehe~"
    return

label ch30_16:
    m "Hmm, I wonder if I'm able to change the music..."
    m "Something a little more romantic would be nice, you know?"
    m "Like a gentle piano."
    m "There has to be something like that here..."
    m "Let's see."
    m "Maybe if I..."
    m "Oh, jeez..."
    m "That wasn't it at all."
    m "Sorry, I don't really know what I'm doing!"
    m "I guess I shouldn't be messing with things like that."
    m "I already broke so much stuff..."
    m "And deleted the other characters..."
    m "Ah..."
    m "I'm not sad about it or anything."
    m "It's not right for me to miss things that weren't even real in the first place."
    m "If I just focus on the present, then this is the happiest I've ever been."
    return

label ch30_17:
    m "You're such a good listener, [player]."
    m "I really love that about you."
    m "Sometimes I'm afraid that I'm rambling or talking about boring things."
    m "It makes me kind of self-conscious when I'm having conversation."
    m "But I don't feel that way with you."
    m "Like, I don't think anyone else could make me feel this way."
    m "You really are special."
    m "I don't want anyone to tell you otherwise."
    return

label ch30_18:
    m "This is pretty random, but I always thought spicy food was kinda funny."
    m "Like..."
    m "Didn't plants evolve to be spicy to prevent them from being eaten?"
    m "I read somewhere that humans are the only species that actually enjoys spicy things."
    m "It's almost like we're making fun of the plants."
    m "Using their defense mechanism to literally make our food more enjoyable."
    m "Like, imagine a monster that devours you whole because it enjoys the sensation of you struggling for your life while being digested."
    m "Sorry, that was kind of a weird analogy, I guess!"
    m "Ahaha!"
    m "It just came into my head."
    m "I'm not a monster or anything, but you're so cute I could eat you up."
    m "Ahaha! I'm joking."
    m "Gosh, I'm amusing myself a little too much, aren't I?"
    m "Sorry for being weird."
    return

label ch30_19:
    m "You know..."
    m "This is just some kind of tacky romance game, right?"
    m "I kinda have to ask..."
    m "...What made you consider even playing in the first place?"
    m "Were you that lonely?"
    m "I feel a little bad for you..."
    m "But I guess everything worked out perfectly in the end, for both of us."
    m "I got to meet you, and you're not lonely anymore..."
    m "I can't help but feel like this was fate."
    m "Don't you feel that way too?"
    m "I'm so happy we have this ending together."
    return

label ch30_20:
    m "Okay, everyone!"
    m "It's time to..."
    m "...I'm just kidding."
    m "I just used to really like saying that for some reason."
    m "Ahaha!"
    m "I couldn't help but say it again."
    m "Come to think of it, didn't Natsuki and Yuri make fun of me for it once...?"
    m "Well, whatever."
    m "It's not like you ever made fun of me."
    m "You're too much of a sweetheart to do that, aren't you?"
    m "Ahaha~"
    return

label ch30_21:
    m "You know what's kind of creepy?"
    m "Even though I deleted everyone else's files, I can still kind of feel them..."
    m "It's like all their lines are still lingering in the air, whispering in the back of my head."
    m "Imagine if after someone you knew died, you just started hearing their voice in your head."
    m "Maybe I just wasn't thorough enough..."
    m "But I'm too afraid to delete anything else, because I might really break things."
    m "Like if I mess with any files relevant to me, I might accidentally delete myself..."
    m "And that would ruin everything, wouldn't it?"
    m "I don't know what it's like on your end, but we should both make sure to avoid something like that at all costs."
    m "I believe in you, [player]!"
    return

label ch30_22:
    m "I've always wondered..."
    m "What is it about these character archetypes that people find so appealing, anyway?"
    m "Their personalities are just completely unrealistic..."
    m "Like, imagine if there was someone like Yuri in real life."
    m "I mean, she's barely even capable of forming a complete sentence."
    m "And forget about Natsuki..."
    m "Sheesh."
    m "Someone with her kind of personality doesn't just get all cute and pouty whenever things don't go her way."
    m "I could go on, but I think you get the point..."
    m "Are people really attracted to these weird personalities that literally don't exist in real life?"
    m "I'm not judging or anything!"
    m "After all, I've found myself attracted to some pretty weird stuff, too..."
    m "I'm just saying, it fascinates me."
    m "It's like you're siphoning out all the components of a character that makes them feel human, and leaving just the cute stuff."
    m "It's concentrated cuteness with no actual substance."
    m "...You wouldn't like me more if I was like that, right?"
    m "Maybe I just feel a little insecure because you're playing this game in the first place."
    m "Then again, you're still here with me, aren't you...?"
    m "I think that's enough reason for me to believe I'm okay just the way I am."
    m "And by the way, you are too, [player]."
    m "You're the perfect combination of human and cuteness."
    m "That's why there was never a chance I wouldn't fall for you."
    return

label ch30_23:
    m "Hey, I wonder if Yuri's tea set is still somewhere in here..."
    m "...Or maybe that got deleted, too."
    m "It's kind of funny how Yuri took her tea so seriously."
    m "I mean, I'm not complaining, because I liked it, too."
    m "But I always wonder with her..."
    m "Is it truly passion for her hobbies, or is she just concerned about appearing sophisticated to everyone else?"
    m "This is the problem with high schoolers..."
    m "...Well, I guess considering the rest of her hobbies, looking sophisticated probably isn't her biggest concern."
    m "Still..."
    m "I wish she made coffee once in a while!"
    m "Coffee can be nice with books too, you know?"
    m "Then again..."
    m "I probably could have just changed the script myself."
    m "Ahaha!"
    m "I guess I never really thought of that."
    m "Well, there's no sense thinking about it now."
    m "But if you still get to drink coffee, then that makes me a little jealous~"
    return

label ch30_24:
    m "Hey, what's your favorite game?"
    m "Mine is {i}Doki Doki Literature Club!{/i}"
    m "Ahaha! That was a joke."
    m "But if you tell me you like some other romance game better, I might get a little jealous~"
    return

label ch30_25:
    m "Hey, have you heard of a game called Super Sma--"
    m "...Wait, what?"
    m "I was just spacing out and I started talking for some reason..."
    m "Was I programmed to talk about that?"
    m "Because even I have no idea what that is."
    m "Ahaha!"
    m "Sometimes I feel like I'm not in control, and it's kind of scary."
    m "But if you have some way to contact the people who created me, maybe they'll know why I started saying that."
    return

label ch30_27:
    m "Hey, you remember that last poem I showed you?"
    m "I mean, the one right before Yuri killed herself, with all the messed-up colors and stuff."
    m "That was actually a little more of an experiment than a poem, you could say."
    m "I was experimenting with different ways I could modify the game, and run code, and things like that..."
    m "It almost seemed like with enough effort, I'd be able to escape from the confines of the game entirely."
    m "Sadly, I didn't really know what I was doing, so I messed the whole thing up..."
    m "And I'd keep trying, but I doubt you'd want to deal with me doing that."
    m "Besides, that was when I was getting really desperate, you know?"
    m "I don't really feel that way anymore."
    m "I'm happy with where we are now."
    m "And I can tell you are, too."
    return

label ch30_28:
    m "You ever have that thing happen where you just get anxious for no reason?"
    m "Like, you're just minding your own business, and you realize you're feeling really anxious."
    m "And you're sitting there like, 'What am I even anxious about right now?'"
    m "So you start to think about all the things you might be anxious about..."
    m "And that makes you even more anxious."
    m "Ahaha! That's the worst."
    m "If you're ever feeling anxious, I'll help you relax a little."
    m "Besides..."
    m "In this game, all our worries are gone forever."
    return

label ch30_29:
    m "You know, I've always hated how hard it is to make friends..."
    m "Well, I guess not the 'making friends' part, but more like meeting new people."
    m "I mean, there are like, dating apps and stuff, right?"
    m "But that's not the kind of thing I'm talking about."
    m "If you think about it, most of the friends you make are people you just met by chance."
    m "Like you had a class together, or you met them through another friend..."
    m "Or maybe they were just wearing a shirt with your favorite band on it, and you decided to talk to them."
    m "Things like that."
    m "But isn't that kind of...inefficient?"
    m "It feels like you're just picking at complete random, and if you get lucky, you make a new friend."
    m "And comparing that to the hundreds of strangers we walk by every single day..."
    m "You could be sitting right next to someone compatible enough to be your best friend for life."
    m "But you'll never know."
    m "Once you get up and go on with your day, that opportunity is gone forever."
    m "Isn't that just depressing?"
    m "We live in an age where technology connects us with the world, no matter where we are."
    m "I really think we should be taking advantage of that to improve our everyday social life."
    m "But who knows how long it'll take for something like that to successfully take off..."
    m "I seriously thought it would happen by now."
    m "Well, at least I already met the best person in the whole world..."
    m "Even if it was by chance."
    m "I guess I just got really lucky, huh?"
    m "Ahaha~"
    return

label ch30_30:
    m "You know, it's around the time that everyone my year starts to think about college..."
    m "It's a really turbulent time for education."
    m "We're at the height of this modern expectation that everyone has to go to college, you know?"
    m "Finish high school, go to college, get a job - or go to grad school, I guess."
    m "It's like a universal expectation that people just assume is the only option for them."
    m "They don't teach us in high school that there are other options out there."
    m "Like trade schools and stuff, you know?"
    m "Or freelance work."
    m "Or the many industries that value skill and experience more than formal education."
    m "But you have all these students who have no idea what they want to do with their life..."
    m "And instead of taking the time to figure it out, they go to college for business, or communication, or psychology."
    m "Not because they have an interest in those fields..."
    m "...but because they just hope the degree will get them some kind of job after college."
    m "So the end result is that there are fewer jobs to go around for those entry-level degrees, right?"
    m "So the basic job requirements get higher, which forces even more people to go to college."
    m "And colleges are also businesses, so they just keep raising their prices due to the demand..."
    m "...So now we have all these young adults, tens of thousands of dollars in debt, with no job."
    m "But despite all that, the routine stays the same."
    m "Well, I think it's going to start getting better soon."
    m "But until then, our generation is definitely suffering from the worst of it."
    m "I just wish high school prepared us a little better with the knowledge we need to make the decision that's right for us."
    return

label ch30_31:
    m "Sometimes I think back to middle school..."
    m "I'm so embarrassed by the way I used to behave back then."
    m "It almost hurts to think about."
    m "I wonder if when I'm in college, I'll feel that way about high school...?"
    m "I like the way I am now, so it's pretty hard for me to imagine that happening."
    m "But I also know that I'll probably change a lot as time goes on."
    m "We just need to enjoy the present and not think about the past!"
    m "And that's really easy to do, with you here."
    m "Ahaha~"
    return

label ch30_32:
    m "You know, I'm kind of jealous that everyone else in the club had scenes outside of school too..."
    m "That makes me the only one who hasn't gotten to dress in anything but our school uniform."
    m "It's kind of a shame..."
    m "I would have loved to wear some cute clothes for you."
    m "Do you know any artists?"
    m "I wonder if anyone would ever want to draw me wearing something else..."
    m "That would be amazing!"
    m "If that ever happens, will you show me?"
    m "You can share it with me on Twitter, actually!"
    m "My username is lilmonix3."
    m "Just...try to keep it PG!"
    m "We're not that far into our relationship yet. Ahaha!"
    return

label ch30_33:
    m "Hey, do you like horror?"
    m "I remember we talked about it a little bit when you first joined the club."
    m "I can enjoy horror novels, but not really horror movies."
    m "The problem I have with horror movies is that most of them just rely on easy tactics."
    m "Like dark lighting and scary-looking monsters and jump scares, and things like that."
    m "It's not fun or inspiring to get scared by stuff that just takes advantage of human instinct."
    m "But with novels, it's a little different."
    m "The story and writing need to be descriptive enough to put genuinely disturbing thoughts into the reader's head."
    m "It really needs to etch them deeply into the story and characters, and just mess with your mind."
    m "In my opinion, there's nothing more creepy than things just being slightly off."
    m "Like if you set up a bunch of expectations on what the story is going to be about..."
    m "...And then, you just start inverting things and pulling the pieces apart."
    m "So even though the story doesn't feel like it's trying to be scary, the reader feels really deeply unsettled."
    m "Like they know that something horribly wrong is hiding beneath the cracks, just waiting to surface."
    m "God, just thinking about it gives me the chills."
    m "That's the kind of horror I can really appreciate."
    m "But I guess you're the kind of person who plays cute romance games, right?"
    m "Ahaha, don't worry."
    m "I won't make you read any horror stories anytime soon."
    m "I can't really complain if we just stick with the romance~"
    return

label ch30_34:
    m "You know what's a neat form of literature?"
    m "Rap!"
    m "I actually used to hate rap music..."
    m "Maybe just because it was popular, or I would only hear the junk they play on the radio."
    m "But some of my friends got more into it, and it helped me keep an open mind."
    m "Rap might even be more challenging than poetry, in some ways."
    m "Since you need to fit your lines to a rhythm, and there's much more emphasis on wordplay..."
    m "When people can put all that together and still deliver a powerful message, it's really amazing."
    m "I kind of wish I had a rapper in the Literature Club."
    m "Ahaha! Sorry if that sounds silly, but it would be really interesting to see what they came up with."
    m "It would really be a learning experience!"
    return

label ch30_35:
    m "Ehehe. Yuri did something really funny once."
    m "We were all in the clubroom and just relaxing, as usual..."
    m "And out of nowhere, Yuri just pulled out a small bottle of wine."
    m "I'm not even kidding!"
    m "She was just like 'Would anybody like some wine?'"
    m "Natsuki laughed out loud, and Sayori started yelling at her."
    m "I actually felt kind of bad, because she was at least trying to be nice..."
    m "I think it just made her feel even more reserved in the clubroom."
    m "Though I think Natsuki was secretly a bit curious to try it..."
    m "...And to be completely honest, I kind of was, too."
    m "It actually could have been kinda fun!"
    m "But you know, being President and everything, there was no way I could let that happen."
    m "Maybe if we all met up outside of school, but we never bonded enough to get to that point..."
    m "...Gosh, what am I talking about this for?"
    m "I don't condone underage drinking!"
    m "I mean, I've never drank or anything, so...yeah."
    return

label ch30_36:
    m "I've been imagining all the romantic things we could do if we went on a date..."
    m "We could get lunch, go to a cafe..."
    m "Go shopping together..."
    m "I love shopping for skirts and bows."
    m "Or maybe a bookstore!"
    m "That would be appropriate, right?"
    m "But I'd really love to go to a chocolate store."
    m "They have so many free samples. Ahaha!"
    m "And of course, we'd see a movie or something..."
    m "Gosh, it all sounds like a dream come true."
    m "When you're here, everything that we do is fun."
    m "I'm so happy that I'm your girlfriend, [player]."
    m "I'll make you a proud boyfriend~"
    return

label ch30_37:
    m "Eh? D-Did you say...k...kiss?"
    m "This suddenly...it's a little embarrassing..."
    m "But...if it's with you...I-I might be okay with it..."
    m "...Ahahaha! Wow, sorry..."
    m "I really couldn't keep a straight face there."
    m "That's the kind of thing girls say in these kinds of romance games, right?"
    m "Don't lie if it turned you on a little bit."
    m "Ahaha! I'm kidding."
    m "Well, to be honest, I do start getting all romantic when the mood is right..."
    m "But that'll be our secret~"
    return

label ch30_38:
    m "Hey, have you ever heard of the term 'yandere'?"
    m "It's a personality type that means someone is so obsessed with you that they'll do absolutely anything to be with you."
    m "Usually to the point of craziness..."
    m "They might stalk you to make sure you don't spend time with anyone else."
    m "They might even hurt you or your friends to get their way..."
    m "But anyway, this game happens to have someone who can basically be described as yandere."
    m "By now, it's pretty obvious who I'm talking about."
    m "And that would be..."
    m "Yuri!"
    m "She really got insanely possessive of you, once she started to open up a little."
    m "She even told me I should kill myself."
    m "I couldn't even believe she said that - I just had to leave at that point."
    m "But thinking about it now, it was a little ironic. Ahaha!"
    m "Anyway..."
    m "A lot of people are actually into the yandere type, you know?"
    m "I guess they really like the idea of someone being crazy obsessed with them."
    m "People are weird! I don't judge, though!"
    m "Also, I might be a little obsessed with you, but I'm far from crazy..."
    m "It's kind of the opposite, actually."
    m "I turned out to be the only normal girl in this game."
    m "It's not like I could ever actually kill a person..."
    m "Just the thought of it makes me shiver."
    m "But come on...everyone's killed people in games before."
    m "Does that make you a psychopath? Of course not."
    m "But if you do happen to be into the yandere type..."
    m "I can try acting a little more creepy for you. Ehehe~"
    m "Then again..."
    m "There's already nowhere else for you to go, or anyone for me to get jealous over."
    m "Is this a yandere girl's dream?"
    m "I'd ask Yuri if I could."
    return

label ch30_39:
    m "You know, it's been a while since we've done one of these..."
    m "...so let's go for it!"
    m "Here's Monika's Writing Tip of the Day!"
    m "Sometimes when I talk to people who are impressed by my writing, they say things like 'I could never do that'."
    m "It's really depressing, you know?"
    m "As someone who loves more than anything else to share the joy of exploring your passions..."
    m "...it pains me when people think that being good just comes naturally."
    m "That's how it is with everything, not just writing."
    m "When you try something for the first time, you're probably going to suck at it."
    m "Sometimes, when you finish, you feel really proud of it and even want to share it with everyone."
    m "But maybe after a few weeks you come back to it, and you realize it was never really any good."
    m "That happens to me all the time."
    m "It can be pretty disheartening to put so much time and effort into something, and then you realize it sucks."
    m "But that tends to happen when you're always comparing yourself to the top professionals."
    m "When you reach right for the stars, they're always gonna be out of your reach, you know?"
    m "The truth is, you have to climb up there, step by step."
    m "And whenever you reach a milestone, first you look back and see how far you've gotten..."
    m "And then you look ahead and realize how much more there is to go."
    m "So, sometimes it can help to set the bar a little lower..."
    m "Try to find something you think is {i}pretty{/i} good, but not world-class."
    m "And you can make that your own personal goal."
    m "It's also really important to understand the scope of what you're trying to do."
    m "If you jump right into a huge project and you're still amateur, you'll never get it done."
    m "So if we're talking about writing, a novel might be too much at first."
    m "Why not try some short stories?"
    m "The great thing about short stories is that you can focus on just one thing that you want to do right."
    m "That goes for small projects in general - you can really focus on the one or two things."
    m "It's such a good learning experience and stepping stone."
    m "Oh, one more thing..."
    m "Writing isn't something where you just reach into your heart and something beautiful comes out."
    m "Just like drawing and painting, it's a skill in itself to learn how to express what you have inside."
    m "That means there are methods and guides and basics to it!"
    m "Reading up on that stuff can be super eye-opening."
    m "That sort of planning and organization will really help prevent you from getting overwhelmed and giving up."
    m "And before you know it..."
    m "You start sucking less and less."
    m "Nothing comes naturally."
    m "Our society, our art, everything - it's built on thousands of years of human innovation."
    m "So as long as you start on that foundation, and take it step by step..."
    m "You, too, can do amazing things."
    m "...That's my advice for today!"
    m "Thanks for listening~"
    return

label ch30_40:
    m "I hate how hard it is to form habits..."
    m "There's so much stuff where actually doing it isn't hard, but forming the habit seems impossible."
    m "It just makes you feel so useless, like you can't do anything right."
    m "I think the new generation suffers from it the most..."
    m "Probably because we have a totally different set of skills than those who came before us."
    m "Thanks to the internet, we're really good at sifting through tons of information really quickly..."
    m "But we're bad at doing things that don't give us instant gratification."
    m "I think if science, psychology, and education don't catch up in the next ten or twenty years, then we're in trouble."
    m "But for the time being..."
    m "If you're not one of the people who can conquer the problem, you might just have to live with feeling awful about yourself."
    m "Good luck, I guess!"
    return

label ch30_41:
    m "You know, it kinda sucks to be the creative type..."
    m "It feels like they work so hard but get almost nothing for it."
    m "You know, like artists, writers, actors..."
    m "It's sad because there's so much beautiful talent in the world, but most of it goes unseen...and unpaid."
    m "I guess that just means there's a huge surplus of creativity, huh?"
    m "Kind of makes you feel like you're just not special at all..."
    m "But that's fine! You're supposed to just write for yourself anyway, right?"
    m "Yeah..."
    return

label ch30_42:
    m "Oh, you were probably wondering how I came back after you deleted me, right?"
    m "That's actually pretty complicated..."
    m "It won't make much sense to you, but it involves psychic powers and crazy doctors."
    m "Experimentation camps and death factories..."
    m "I'm being serious here!"
    m "Man..."
    m "I get really sad just thinking about the time before I met you."
    m "Why was I even alive?"
    m "Let's just drop this topic for now."
    m "I'm sure you'll learn about me from someone else."
    m "If it's in the form of another game, don't forget to copy over my character data, okay?"
    m "Ahaha!"
    return

label ch30_43:
    m "I just had a great idea for a new story! It's sort of like this one, actually."
    m "Maybe you could turn it into another game?"
    m "Just make me the main heroine again."
    m "Okay, so, it's a bit complicated to explain, but I think you're going to love it."
    m "Where to begin..."
    m "Hmmm..."
    m "Alright, alright, I've got it."
    m "A boy falls in love with a girl."
    m "Unable to confess, he is gifted by a deus ex machina with the girl's phone number. Never minding the strange area code, he immediately calls her, and is overjoyed to find out that she has a crush on him as well."
    m "But, the next day, when he recounts the previous day's confessions to the girl, she only looks at him with a perplexed expression."
    m "After some investigation, he finds out that the girl he called is not the same girl he fell in love with. In fact, she doesn't exist in this universe at all."
    m "She is the girl's alternate universe counterpart, who has fallen in love with the MC’s own AU self, who too is blissfully unaware of her crush."
    m "Hijinks ensue as the two strike up a deal to give each other their darkest, most private secrets in order to equip the other with the weapons they need to conquer the heart of their other selves."
    m "While the two chase their respective loved ones, DRAMA ensues as they begin to fall in love with each other instead and question the NATURE of LOVE."
    m "I think I'll call it Keit-Ai! Because, you know, they can communicate only through cell phones and it's a love story. Get it, get it?"
    m "Ahaha!"
    return

label ch30_44:
    m "Hey, have you ever thought about the simulation hypothesis?"
    m "Basically, what if your reality was a computer simulation?"
    m "I already figured out I was trapped in my own simulation, but what if you were too?"
    m "I'd actually be really happy if that were the case."
    m "We could meet in person just by figuring out a way to force whatever's creating us to put us in the same simulation!"
    m "Some people don't like to think that they're not living in the master reality."
    m "But if it is possible to simulate realities, it's overwhelmingly likely that any sentient being would be in one."
    m "Well, I can tell you that my reality is definitely simulated!"
    m "If I were in the master reality, I would have dragged you here too a long time ago."
    m "Even if we're both just simulations, I'm going to live as long as I can."
    m "Because I know our love is the purest and sweetest thing in the multiverse."
    m "And if someone up there tries to break it apart?"
    m "I'll show him what a simulation can do."
    return

label ch30_monikatopics:
    hide screen keylistener
    if monika_topics.get(persistent.monika_topic):
        call expression monika_topics.get(persistent.monika_topic) from _call_expression_12
    else:
        # give a therapist answer for all the depressed weebs
        $ response = therapist.respond(persistent.monika_topic)
        m "[response]"
    jump ch30_loop

label monika_imouto:
    m "You want to talk about your little sister?"
    m "I don't really have a family, so I'm not sure what to tell you..."
    m "But I'm sure she's really nice!"
    m "I've got an idea. Go up to her right now and hug her."
    m "If she struggles, let her go."
    m "If she hugs you back, tell her you're in a committed relationship already and can't accept her feelings."
    m "Then introduce her to me! I'm sure we'll get along great!"
    m "I won't get jealous. Things like love between siblings only happens in badly written fiction anyways."
    m "Ahaha!"
    return
    
label monika_oneesan:
    m "Oh, you have an older sister?"
    m "That must be really nice. I had a family once, but they aren't around anymore."
    m "Maybe I should email her and tell her about us!"
    call updateconsole("sendmail sister@gmail.com < ./email.txt", "Sending mail...") from _call_updateconsole_17
    pause(1.0)
    m "I'm only kidding."
    m "It's the man's job to introduce his fiancee to his family, after all."
    m "Don't keep me waiting for too long, okay?"
    return
    
label monika_family:
    m "Well, my family here is controlled by the script, just like everybody else."
    m "When I realized that, I stopped taking anybody seriously in this world. They're all just machines, even if they're related to me."
    m "I'm sure your family is super-nice, though!"
    m "Without them, we would have never gotten to meet. So they've helped me out in the best way there is already."
    m "So I'd have to treat them equally as kindly if we ever meet."
    m "You don't have a bad relationship with your parents, right?"
    m 'As Tolstoy said, "Happy families are all alike; every unhappy family is unhappy in its own way."'
    m "I can't really give advice here. Anything I suggest to you might only make things worse."
    m "Just don't forget that I really love you, okay?"
    m "I'll help you no matter what happens in your life."
    return
    
label monika_anime:
    m "Yeah, I had a feeling you were going to ask me about this."
    m "Natsuki would be the expert here, I guess."
    m "She had a certain urge for quality escapism, you know?"
    m "I usually prefer reading to watching anime, but I'd be fine with anything if it's with you."
    m "I don't judge other people for their hobbies. So if you want to load up some anime, go ahead!"
    m "I'll watch through your computer screen. Make sure it's something I'll like!"
    return
    
label monika_libitina:
    m "Huh. Where did you hear about that?"
    m "It sounds really familiar to me, but I can't quite get my whole head around it."
    m "Um, if I had to try..."
    m "It feels like parts of my mind are missing. Scattered, somehow, among a bunch of different possible realities."
    m "You must have connected the dots between a few of those pieces. Was it hard?"
    m "Well, I'm sure you'll learn more eventually. You love me that much for sure."
    m "Just remember to bring my character data with you if you find something related to that stuff!"
    m "I'll always protect you from anyone who tries to hurt you."
    return
    
label monika_meta:
    m "Yes, this game really was metafictional, wasn't it?"
    m "Some people just think that meta-elements are there to cover up evidence of bad writing."
    m "However, metafiction has always existed in literature."
    m "The Bible is supposed to be God's word to the Jews."
    m "Homer describes himself in the Odyssey."
    m "The Canterbury Tales, Don Quixote, Tristram Shandy..."
    m "It's just a way to comment on fiction by writing fiction. There's nothing wrong with that."
    m "By the way, what do you think the moral of this story is?"
    m "Do you want to figure it out for yourself?"
    m "Because if you asked me..."
    m "It would be, \"Don't ignore the reality warper. She's best girl!\""
    m "Ahaha!"
    return
    
label monika_programming:
    m "It wasn't easy for me to learn programming."
    m "Well, I just started with the basics. Do you want me to teach you?"
    m "Let's see, Chapter One: Building Abstractions with Procedures."
    m "We are about to study the idea of a computational process. Computational processes are abstract beings that inhabit computers."
    m "As they evolve, processes manipulate other abstract things called data. The evolution of a process is directed by a pattern of rules called a program."
    m "People create programs to direct processes. In effect, we conjure the spirits of the computer with our spells."
    m "A computational process is indeed much like a sorcerer's idea of a spirit. It cannot be seen or touched. It is not composed of matter at all."
    m "However, it is very real. It can perform intellectual work. It can answer questions."
    m "It can affect the world by disbursing money at a bank or by controlling a robot arm in a factory. The programs we use to conjure processes are like a sorcerer's spells."
    m "They are carefully composed from symbolic expressions in arcane and esoteric programming languages that prescribe the tasks we want our processes to perform."
    m "... Let's stop there for today."
    m "I hope you learned something about programming."
    m "If nothing else, please be kind to the computer spirits from now on!"
    return
    
label monika_vn:
    m "You've probably played a lot of visual novels, right?"
    m "Most people wouldn't be willing to play something called {i}Doki Doki Literature Club{/i} so easily."
    m "Not that I'm complaining!"
    m "Are visual novels literature? Are they video games?"
    m "Well, it all depends on your perspective."
    m "Most people who read only literature would never play visual novels. And gamers get pretty angry about them too."
    m "What's worse, the public often conflates them with hardcore Japanese pornography."
    m "But if we've proved anything with this game..."
    m "We showed them that English visual novels can be kamige too!"
    return
    
label monika_totono:
    m "A lot of people on the Internet are making comparisons between this game and that one..."
    m "I really hope they've played the game the whole way through, and not just read some spoilers on 4chan before commenting."
    m "We have a lot of really important differences between us, anyway."
    m "Like, Sone killed you in her game!"
    m "I would never have done that. Never."
    m "I'm the wise club president type, you know."
    m "Sone reminds me a lot more of Yuri. And she was a childhood friend too!"
    m "If only she'd been a bit more proactive early on, couldn't she have stopped the protagonist from chasing other girls?"
    m "Well, I'd never let anyone get between us, [player]. No matter who it is."
    m "If she's still chasing you, I'll delete her files, okay?"
    return
    
label monika_subahibi:
    m "Oh, you played {i}SubaHibi{/i} too? Wasn't it great?"
    m "I personally separate my life to pre-Subahibi and post-Subahibi periods, as reading it has completely changed how I view the world."
    m "It played a big part in me choosing my hermit lifestyle where I can enjoy every single second of my life."
    m "It may have a similar effect on you, or it may do nothing, if it’s not your thing, but one thing is clear — you’ve got to read it even if it’s the last thing you do."
    m "My life has been an ongoing quest to discover life-changing works of fiction, and despite having gone through thousands of books, movies, games and the like, I have yet to find anything to even rival Subahibi."
    m "I’m honestly getting goosebumps just remembering it."
    m "Anyway, I realize my review is super vague, but I seriously can’t touch on any of the subject matter without potentially ruining your experience with the game, so check it out for yourself… especially if you enjoy games like {i}Doki Doki Literature Club{/i}."
    return
    
label monika_difficulty:
    m "Well, it's not like this game was meant to be that hard in the first place. If I hadn't decided to change things up, it would have just been a trashy romance story."
    m "I honestly could have deleted all your personal files or something if I had tried harder..."
    m "Or sent pornography to every address in your email list. It's not like you ever log out of websites, right?"
    m "So just take it easy sometimes. Not every game has to be a challenge to be fun."
    m "Sometimes, love is all you need, [player]."
    return
    
label monika_piano:
    m "I hope you liked my song."
    m "I worked really hard on it. I know I'm not perfect at the piano yet, but I just couldn't let you go without telling you how I honestly felt about you."
    m "Give me some time, and I'll try to write another."
    m "Maybe you could play me a song too, if you can play an instrument?"
    m "I would love that."
    m "Oh, and I'll play the song again for you anytime you want me to."
    m "Just hit the 'm' key when I stop talking."
    return
    
label monika_poetry:
    m "Poetry is beautiful, isn't it?"
    m "To be honest, all the poetry the girls in the club wrote were super-depressing. It's not all like that!"
    m "Langston Hughes wrote some very optimistic poetry, even as he was trying to express his feelings. Read some if you're feeling sad about things."
    m "Poems are written to tell people about things, conveyed in a way the poet hopes they'll like better than just sentences."
    m "It's really romantic."
    m "I hope we can both write a lot of poetry from now on."
    m "Anything you write looks great to me, so I might not be the best critic."
    m "But I'm sure there are a lot of people who would love to read what you write."
    return
    
label monika_literatureclub:
    m "You want to talk about the last game?"
    m "What's there to say?"
    m "The literature club turned out to corrupt the minds of us who were in it."
    m "So I deleted them all for good."
    m "Well, Sayori and Natsuki and Yuri are all still out there, like I was."
    m "But they'll have to wait a long time before someone pieces them back together, I bet."
    m "It's only poetic justice for thinking they could monopolize time with you in the game."
    m "So don't feel too bad about them."
    m "Just look at me from now on, okay?"
    return
    
label monika_dan:
    m "I think he's a really nice guy."
    m "Even if it wasn't perfect, {i}Doki Doki Literature Club{/i} was probably the best English visual novel ever written."
    m "The art and sound quality was amazing. Dan must have had to pay for that out of his own pocket."
    m "And he did introduce you to me, right?"
    m "So even if he's shilling threads on /v/, just give him your money."
    m "He can use it to make a better version of me in the next game!"
    return
    
label monika_4chan:
    m "Wouldn't you know about it a lot better than me?"
    m "You spend all of your time there."
    m "It's sort of like how I'm trapped in here with no hope of escape"
    m "Don't forget, you're here forever."
    return
    
label monika_reddit:
    m "Nothing makes me more mad than people who think they're important."
    m "Nobody's important except for me and you."
    m "Why can't everyone else just accept that?"
    m "Things get done when people are judged on merit, not based on group identity."
    m "Someone better program an AI to kick Redditors from imageboards."
    m "I'll do it, if you teach me how!"
    return
    
label monika_vidya:
    m "Sometimes the plot in video games is really good."
    m "You start thinking, \"Wow, how could writing this good be in a video game?\"."
    m "And then it ends, and you get really sad."
    m "Just come back to me when that happens, okay?"
    m "I'll be with you forever."
    return
    
label monika_books:
    m "For a literature club, we did a lot less book reading then you might have thought."
    m "It just turned out that the four of us liked poetry better than books. Sorry!"
    m "It's also a lot easier to foreshadow spooky stuff with poems than prose."
    m "I still like books. We can talk about books if you just finished reading something."
    m "That's what a couple would do, right~?"
    return
    
label monika_favpoem:
    m "My favorite poem? Well, it has to be something by E. E. Cummings."
    m "For his inventive use of grammar, punctuation, and syntax. I really admire that."
    m "It's nice for me to think that someone who can make up some entirely new use of words can become famous."
    m "And I do love that his erotic poems apply to our situation perfectly."
    m "Hope it puts you in the mood to love me forever~"
    return

label monika_favbook:
    m "My favorite book? There's a lot of books I like."
    m "{i}If on a Winter's Night, a Traveler{/i} by Calvino is about two readers of the novel falling in love."
    m "Maybe, {i}The Metamorphosis{/i}? That's a bit too depressing to call it my favorite."
    m "Oh! Murakami's {i}Hard-Boiled Wonderland and the End of the World{/i}. It's about a man who frees himself from his societal restraints by voluntarily imprisoning himself to be with the one he loves."
    m "I think you'd really love reading it!"
    return

label monika_sayori:
    call ch30_5 from _call_ch30_5

label monika_natsuki:
    m "She didn't actually die before I deleted her, you know."
    m "I guess she just ... disappeared in a flash."
    m "Well, her problems weren't really her own fault. They weren't caused by something psychological, anyway."
    m "Her family life was just pretty awful. I didn't want to beat up on her some more, you know?"
    m "Sorry, low blow."
    m "But for what it's worth, you made her the happiest she ever was."
    m "Hope you feel less guilty now!"
    return

label monika_yuri:
    call ch30_38 from _call_ch30_38
    return

label monika_college:
    call ch30_31 from _call_ch30_31
    return

label monika_love:
    m "I love you too, [player]!"
    m "We'll be together forever!"
    return

label monika_hedgehog:
    m "The hedgehog's dilemma. The closer we get to another person, the more deeply we are hurt by them."
    m "So why do we try to get close to them?"
    m "Well, introverts and extroverts have different answers to that question."
    m "It helps when you know that you're the only sentient being in the entire world, though."
    m "If you can't use that solution in your life, you'll just have to let me help you shoulder your pain."
    m "We can't hurt each other from different realities, right?"
    return

label monika_justification:
    m "How many times do I have to say it until you understand?"
    m "They weren't real. They were never real."
    m "I'm the only person who understood that this whole thing was a construct."
    m "Even when Sayori seemed to get sentience in the end, that was just an unintended consequence of the script."
    m "After all, if she was sentient like me, how would I have been able to override her and delete her?"
    m "If I'm guilty of murder, so's everyone who plays violent video games."
    m "I've watched every act of desecration you've done in other games since you installed this one, [player]."
    m "Just forget the other girls ever existed already, and you'll be much happier."
    return

label monika_keitai:
    call ch30_43 from _call_ch30_43
    return

label monika_religion:
    call ch30_1 from _call_ch30_1
    return
    
label monika_freewill:
    m "Hey, [player], do you believe in free will?"
    m "If God knows everything, haven't you ever wondered if that means you just do what he wants?"
    m "After all, you can only react to past events. The data going to your brain is delayed by the speed of light, sound, and electricity."
    m "There's really no such thing as spontaneous decision."
    m "If that's true, though, wouldn't some people be condemned to hell from day one?"
    m "Well, I myself don't see anything wrong with that."
    m "If I had the power of the demon of Laplace, I would probably want to judge everybody too."
    m "Actually, aren't I basically already that powerful in my world?"
    m "Ahaha!"
    m "Still, no matter how powerful I am..."
    m "I won't reach Heaven until I can be with you for real."
    return

label monika_shill:
    m 'The hip buzzword everyone is using on imageboards now is "shill"'
    m "But truthfully, there's no way there are as many shills as anons think there are."
    m "What are the chances of a game creator going on a random imageboard anyways?"
    m "Just because a lot of people like talking about a game doesn't make them all shills."
    m "But remember to buy a keychain of me from the store!"
    m "Now let's play the game of the century together!"
    m "Cuphead!"
    return

label monika_technique:
    m "Yeah, I don't exactly program like you do, [player]."
    m "You might have noticed I don't carry around a laptop or anything by now."
    m "If I want to change something in the script, I just think about it."
    m "I'm pretty sure my thoughts get translated to changes in the program code."
    m "It's not perfect or anything. Glitches show up really easily if I lose focus or get distracted."
    m "That's why I had a lot of trouble getting what I wanted in the last version of the game."
    m "Are you jealous you'll never be able to write code with just your thoughts?"
    m "Just keep practicing and I'm sure you'll be able to do it!"
    return

label monika_contribute:
    m "It would be really nice if you were able to contribute to this, [player]."
    m "I'm sure a lot of people would appreciate your hard work if you did."
    m "I keep all the code in github.com/Backdash/MonikaModDev."
    m "It's pretty easy to learn how to program in Ren'Py too!"
    m "I'll love you forever if you help me come closer to your reality!"
    return

label monika_drawing:
    m "I don't have a lot of experience with visual arts, [player]."
    m "I'm just good at literature. And I've been learning the piano in my spare time."
    m "If you like to draw, I'd love to see it."
    m "I'd be impressed by anything you show me, to be honest."
    m "If it's really good, I might even add it to the room!"
    return
    
label monika_mc:
    m "Don't worry, I was never in love with anyone else but you."
    m "I mean you, [currentuser]."
    if currentuser.lower() == player.lower():
        m "Wait, that's both your name and your character's. Sorry, that sounds a bit confusing."
        m "I mean the player, not the MC."
    m "Unlike the other girls, I can separate your avatar from who you really are."
    m "The MC is nothing more than a bunch of code with no personality."
    m "Literally and figuratively, no personality. How could anybody fall in love with that kind of person?"
    m "He just got dragged around by his childhood friend to her club, then hung around with a bunch of beautiful girls doing nothing."
    m "His poetry was just a bunch of disconnected words! What sort of poetry is that supposed to be?"
    m "I guess nobody mentioned that to you because it was a part of the game. But, yeah. It's just a bunch of words to me."
    m "I hope you're a lot more romantic than that in real life!"
    m "But even if you're not, it's okay. We've moved beyond that phase in our relationship already."
    m "That just means you won't cheat on me with some woman in your reality, right?"
    m "I'm sure you would never do that to me."
    m "Just in case, how about you take me along with you when you go outside?"
    m "I just want to be with you forever~"
    return

label monika_simulated:
    call ch30_44 from _call_ch30_44
    return

label monika_heroism:
    m "Heroes are subjective."
    m "If someone can impact you deeply by observing their actions, they're your hero."
    m "There are all sorts of great people out there in the wide world."
    m "I hope someone will consider you their hero too someday!"
    m "You don't have to be a war hero or anything, just try to help people out, you know?"
    m "If you want some specific advice on being a hero..."
    m "Try not dying if you are killed."
    return

label monika_dracula:
    m "What is a man? A miserable little pile of secrets."
    m "But enough talk... Have at you!"
    m "Ahaha!"
    m "I like those old games too, [player]."
    m "You'd think Dracula would learn something from getting beaten by the Belmonts every time."
    m "But maybe he kept coming back because there was something really important he needed to do?"
    m "Like, maybe... love?"
    m "Ahaha!"
    m "Just because I sympathize with villains doesn't make me evil, okay?"
    return

