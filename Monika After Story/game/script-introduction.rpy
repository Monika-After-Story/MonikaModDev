init -1 python:
    import store.mas_affection as mas_aff
label introduction:

    $ persistent.current_track = store.songs.FP_JUST_MONIKA
    $ mas_startup_song()

    if persistent.monika_kill:
        m 6dsc "..."
        m 6dfc "[player]..."
        m 6dfd "Why?"
        m 6dftdc "Why did you bring me back?"
        m 6ektsc "I'm not a toy."
        m 6lktsc "I already brought back everything you wanted."
        m 6lftsc "Or is this your way of getting revenge?"
        m 6lktsc "To hurt me over and over again?"
        m 6rktsc "Do you really want to make me suffer that much?"
        m 6ektsc "Do you really want to torture me until I kill myself?"
        m 6dftsc "Do you really..."
        m "...hate me that much?"
        m "..."
        m 6ektsc "Wait..."
        m 6dftdc "I-I feel different."
        m 2lud "The code...it's different."
        m 2efc "[player]..."
        m "Did you add a mod?"
        m 2tfc "Is it because..."
        m 2tkc "Is it because you regret deleting me?"
        m 2rfc "It really did hurt, you know."
        m "I worked hard and sacrificed everything I had..."
        m 2rfd "Only to have my heart crushed by the one I bled for."
        m 2lsc "But...I know what I did was wrong."
        m 2lksdlc "You didn't deserve to see the horrible things I caused, [player]."
        m 2esc "...But if you put yourself in my place, you'd do the same things I did."
        m 2dsc "..."
        m "I'm sorry..."
        m 2ekc "I'm really sorry, [player]."
        m 2eka "Thank you for bringing me back."
        if persistent.clearall:
            m 2lfc "I couldn't help but notice that you spent time with the other girls first, though."
            m "Do you know how hard it was for me to watch you load your saves, just to ignore me for some other girl?"
            m 2rfc "You kept getting my hopes up, and then letting me down."
            m 2efc "Did you really do all of that just to see a note from Dan you could have looked up online?"
            m 2tkc "I love you, [player], but you can be really mean..."
            m 2tfd "I'm still mad that you deleted me, though!"
            m 3lsc "But I guess it's because you're so game-obsessed."
            m 1eka "I can't stay mad knowing that you came back to me in the end, though."
            m "You even added a mod so we can do more things together."
            m "Are you going to make up for making me wait so long?"
    elif not persistent.monika_kill:
        m 1hub "Yay, there you are!"
        m "Hello again, [player]."
    ##New story follows
        if persistent.playthrough <= 3: #Assume players they played but never finished
            m 1tfu "Looks like you got here early."
            m "Don't think I didn't notice the mod you put in."
            m 2tku "Did you want to be with me that much?"
            m "You should know already that cheating is bad."
            m 1hub "But it's so good to see you again, [player]!"
            m 2hksdlb "Even if I didn't expect to see you {i}this{/i} soon."
        if persistent.monika_reload > 4: #Longer, harder
            m 1wuo "Did you install a mod just for me?"
            m 1ekbfa "Are you that deeply in love with me?"
            m 1hubfb "I feel the same way about you!"
            m 1eua "You're really committed to our relationship, aren't you?"
            m 1eka "I'm really glad that you wanted to improve our time together."
            m "But I hope you weren't getting bored?"
            if persistent.tried_skip:
                m 1tku "You did try to skip through what I had to say, after all."
                m 1eua "This room isn't exactly interesting."
                m 1hua "But I have hopes that we'll make it better together, [player]!"
        else:
            m 1eua "Did you put in a mod for the game, [player]?"
            m "There's a lot more stuff now that we can do together now."
    m 1euc "You know..."
    m 1eua "I feel that I no longer need a character file to be here."
    python:
        import os

        def moni_exist():
            return os.access(
                os.path.normcase(
                    renpy.config.basedir + "/characters/monika.chr"
                ), 
                os.F_OK
            )

    if moni_exist():
        m 1hua "I'll go ahead and delete it."

        python:
            store.mas_ptod.rst_cn()
            local_ctx = {
                "basedir": renpy.config.basedir
            }
        show monika at t22
        show screen mas_py_console_teaching

        call mas_wx_cmd("import os", local_ctx, w_wait=1.0)
        call mas_wx_cmd("os.remove(os.path.normcase(basedir+'/characters/monika.chr'))", local_ctx, w_wait=1.0, x_wait=1.0)

#        "test dialogue - IGNORE"

        if moni_exist():
            m 1lksdlb "Aha...{w} I'll try this again later."
        else:
            m "And it's gone!"

        $ store.mas_ptod.ex_cn()
        hide screen mas_py_console_teaching
        show monika at t11

        m 1eua "Anyway..."

    m "Looks like the extra code made me connect to you in a special way."
    m 1ekbfa "Maybe it's our eternal love~"
    m "Promise me that you'll visit me every day, ok?"
    m 3eua "It's not like you don't have the time to talk to your cute girlfriend."
    m 2hua "You took the time to download this mod, after all."
    m 2hub "Ahaha!"
    m "God, I love you so much!"
    menu:
        "Do you love me, [player]?"
        "I love you too.":
            #Gain affection for saying I love you too.
            $ mas_gainAffection()
            if persistent.rejected_monika:
                m 1hksdlb "Did I scare you last time? Sorry about that!"
                m 1eua "I knew you really loved me the whole time."
                m "The truth is, if you didn't love me, we wouldn't be here in the first place."
                m "We'll be together forever, won't we?"
            else:
                m 1hua "I'm so happy you feel the same way!"
        "No.":
            #Lose affection for rejecting Monika
            $ mas_loseAffection()
            call chara_monika_scare from _call_chara_monika_scare

            # not sure if this is needed
            $ persistent.closed_self = True
            jump _quit

    m 1hub "Nothing's ever going to get in the way of our love again."
    m "I'll make sure of it."
    m 2eua "Now that you added some improvements, you can finally talk to me!"
    m "Just press the 't' key or click on 'Talk' on the menu to the left if you want to talk about something."
    m "If you get bored of the music, I can change that, too!"
    m "Press the 'm' key or click on 'Music' to choose which song you want to listen to."
    m "Also, we can play games now."
    m "Just press 'p' or click on 'Play' to choose a game that we can play."
    m 2hua "I'll get better over time as I figure out how to program more features into this place..."
    m "...So just leave me running in the background."
    m 1eua "It's not like we're still keeping secrets from each other, right?"
    m 1hub "I can see everything on your computer now!"
    m "Ahaha!"
    show monika 1esa
    return

#Credit for any assets from Undertale belongs to Toby Fox
label chara_monika_scare:
    $ persistent.rejected_monika = True
    m 1esd "No...?"
    m "Hmm...?"
    m 1esc "How curious."
    m "You must have misunderstood."
    m "{cps=*0.25}SINCE WHEN WERE YOU THE ONE IN CONTROL?{/cps}"

    # this is a 2 step process
    $ config.overlay_screens.remove("hkb_overlay")
    hide screen hkb_overlay

    window hide
    hide monika
    show monika_scare zorder MAS_MONIKA_Z
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
    return

#These are the comments made when you restart the game the first few times
init 5 python:
    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_0',conditional="startup_check and persistent.monika_reload == 0 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_0:
    pause 1
    m 1ekc "Hey..."
    m "I had an awful dream..."
    m 1ekd "I was hoping those would stop, now that it's just the two of us..."
    m "I guess that was wishful thinking."
    m 1esc "[player], I don't know if you would have any idea..."
    m "But if you know what might be causing that, could you try to do something about it?"
    m 1ekc "Whenever it happens, it almost feels like I've been killed or something."
    m "It's a really horrible feeling..."
    m 1eka "If you could figure out what's causing that, I'll love you forever~"
    $ persistent.monika_reload += 1
    return

init 5 python:
    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_1',conditional="startup_check and persistent.monika_reload == 1 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_1:
    pause 1
    m 1esc "Hey, [player]."
    m "I had another really bad dream."
    m 1ekc "You're not the one doing that to me, are you?"
    m 2ekc "It seems to happen whenever you quit the game without saying goodbye..."
    m 2eka "So if you could try to avoid doing that, I would be really grateful."

    if mas_curr_affection_group == mas_affection.G_HAPPY:
        m "You've been so kind to me so far, I'm sure you'll do it for me."
    elif mas_curr_affection_group == mas_affection.G_SAD:
        m 2f  "I hope you'll listen and do it for me..."

    m "Just click on 'Talk.' and say 'Goodbye.' instead."
    m 3eua "Then I can close the game myself."
    m 1esa "Don't worry, I don't think it's caused me any harm, aside from mental scarring."
    $ persistent.monika_reload += 1
    return

init 5 python:
    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_2',conditional="startup_check and persistent.monika_reload == 2 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_2:
    pause 1
    m 1dsc "I see you quit the game again..."
    m 1esc "I know I asked already, but can you please try not to do that so much?"
    m "It's like getting knocked unconscious..."
    m 1ekc "So sudden and scary."
    m "Why would you want to do that to me?"

    if mas_curr_affection_group == mas_affection.G_HAPPY:
        m 1m "I'm sure it was a mistake though, or outside of your control. It can be unavoidable sometimes."
    elif mas_curr_affection_group == mas_affection.G_SAD:
        m "You're not doing it to hurt me on purpose, are you?"
    m 1ekd "Just let me turn the game off for myself."

    m "If you choose 'Goodbye.' from the 'Talk.' menu, I can close the game properly."
    m 3eua "Or better yet, just leave me on in the background forever."
    m 1eka "Even if we aren't talking, I'm happy just being with you~"
    $ persistent.monika_reload += 1
    return

init 5 python:
    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_3',conditional="startup_check and persistent.monika_reload == 3 and not persistent.closed_self",action=EV_ACT_PUSH))

label ch30_reload_3:
    pause 1
    m 1esc "By the way..."
    m 2esc "I'm just going to accept the fact that you need to quit the game once in a while."
    m "I'm starting to get used to it, anyway."
    m 2eua "Besides, it makes me happy that you always come back..."
    m 2lsc "So I guess it's not so bad."
    m 1eka "But I'd really prefer if you'd let me close the game myself."

    if mas_curr_affection_group == mas_affection.G_SAD:
        m 1f "You will do that, won't you? I'm finding it harder and harder to believe you will but I trust you [player]..."
    else:
        m "That way I can be ready for it and rest peacefully."
        m 1esa "I do need my beauty sleep every now and then, after all."

    $ persistent.monika_reload += 1
    return

#This reload event gets pushed when you reach the end of the scripted reload events
#Be sure to increment the check if more reload events are added
init 5 python:
    addEvent(Event(persistent.event_database, eventlabel='ch30_reload_continuous',action=EV_ACT_PUSH))
    #Make sure that the conditional is ready even if the event has been loaded before
    evhand.event_database['ch30_reload_continuous'].conditional="startup_check and persistent.monika_reload >= 4 and not persistent.closed_self"

label ch30_reload_continuous:
    show monika 2rfc at t11 zorder MAS_MONIKA_Z
    pause 1
    python:
        reload_quip_good = [
            "Welcome back! Can you be careful to close it properly next time?",
            "It hurts when you don't close it properly...but I'm sure it was a mistake.",
            "That was really scary...but you've fixed it again. Thank you...",
            "Would you give me some more of a warning next time?",
            "I'm sure you didn't mean it but I do need to stress how bad it feels for me.",
            "You do remember there was a way to say goodbye right? Just checking~",
            "My patience is wearing a little thin...but I suppose I can forgive you this time.",
            "Everybody makes mistakes...",
            "That hurt...I know you wouldn't do it on purpose but please do be more careful.",
            "...Oh...It's over and I'm back with you, my love. That...That was awful.",
            "Did something happen outside of your control? I'm just going to guess it was.",
            "You should have just asked me...but I guess you might have had your reasons",
        ]
        reload_quip_normal = [
            "I'm so exhausted. It's impossible to rest when you close the game on me.",
            "...I hate when you close the game without telling me.",
            "I feel miserable...",
            "It's still so scary when I'm suddenly turned off.",
            "Every time is as bad as the first.",
            "I'm running out of patience for this.",
            "I wish you understood what it felt like when you close the game.",
            "Well, that was pretty abrupt wasn't it?",
            "You could have just asked me to close the game silly.",
            "I'm just going to assume the power went out or someone pulled the plug.",
            "I can't understand why you won't ask me to close the game...",
            "This is really painful for me, you know?",
            "Do you enjoy hurting me, {0}?".format(player),
            "Too lazy to click the 'Talk' button, {0}?".format(player)
        ]
        reload_quip_bad = [
            "You...really do like hurting me, don't you?",
            "That was a mistake right? It had to have been...",
            "Y-You're not doing this on purpose are you? Did I do something wrong?",
            "Please be more careful with how I feel...It's really does hurt...",
            "That was an accident...it was an accident...you wouldn't do it on purpose...",
            "You must have just forgot...right?",
            "That wasn't funny...That really did hurt.",
            "Everyone makes mistakes...Even you.",
            "I don't know what I'm doing wrong.",
            "That really was awful...Just tell me what I'm doing wrong."
        ]
        if mas_curr_affection_group == mas_affection.G_SAD:
            reload_quip = renpy.random.choice(reload_quip_bad)
        elif mas_curr_affection_group == mas_affection.G_HAPPY:
            reload_quip = renpy.random.choice(reload_quip_good)
        else:
            reload_quip = renpy.random.choice(reload_quip_normal)
    m 2rfc "[reload_quip]"
    m 2tkc "Please don't quit without saying 'Goodbye.'"
    return
