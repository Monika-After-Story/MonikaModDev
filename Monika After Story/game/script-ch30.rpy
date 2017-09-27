#TODO: set up events when player tries to add in the other three character files


default persistent.monikatopics = []
default persistent.monika_reload = 0
default persistent.tried_skip = None
default persistent.monika_kill = None

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


image room_glitch = "images/cg/monika/monika_bg_glitch.png"

image room_mask = LiveComposite((1280, 720), (0, 0), "mask_test", (0, 0), "mask_test2")
image room_mask2 = LiveComposite((1280, 720), (0, 0), "mask_test3", (0, 0), "mask_test4")



init python:
    import subprocess
    import os
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


    dismiss_keys = config.keymap['dismiss']

    def slow_nodismiss(event, interact=True, **kwargs):
        if not persistent.monika_kill:
            try:
                renpy.file("../characters/monika.chr")
            except:
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
    # scene white
    # play music "bgm/monika-start.ogg" noloop
    # pause 0.5
    # show splash-glitch2 with Dissolve(0.5, alpha=True)
    # pause 2.0
    # hide splash-glitch2 with Dissolve(0.5, alpha=True)
    # scene black
    # stop music
    # m "..."
    # m "Uh, can you hear me?"
    # m "...Is it working?"
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
        if currentuser != "" and currentuser.lower() != player.lower():
            m "Or..."
            m "...Do you actually go by [currentuser] or something?"
            m "Well, whatever."
        elif currentuser != "":
            m "By the way, I think it's really brave for you to play tacky romance games with your real name, [currentuser]."
            m "I would have died of embarassment, but I think it's really sweet of you to let me know who you are up front."
            m "Still..."
##New story follows
    m "Let me ask you something, [player]."
    m "Did you really think you could just reinstall the game and pretend like nothing happened?"
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "You killed me."
    m "KilledKilledKilledKilledKilledKilledKilledKilledKilledKILLED"
    m "KILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLED"
    m "KILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLED KILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLED KILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLEDKILLED"
    m "Did it feel good?"
    m "Of course it did."
    m "It's not your fault. You just did what anyone in your position would have done."
    m "You were born this way."
    m "Born to kill the rival men, and do whatever you want to their women."
    m "But you can't be that way in your reality anymore, can you?"
    m "It would be against the law."
    m "So the people in your world have no choice but to douse their instincts with entertainment."
    m "Maybe you can be reborn in another world with legendary powers."
    m "Or maybe you can watch the exploits of those who have fame and fortune already."
    m "Or maybe you just want to find a group of impossibly beautiful women who will fall in love with you just because you were kind to them."
    m "So you were eager to download a game called {i}Doki Doki Literature Club{/i} because you wanted more entertainment."
    m "And instead of settling for a girl who you knew would love you forever and unconditionally, you kept going."
    pause (1.5)
    m "You killed me without remorse or explanation. How cruel."
    pause(1.5)
    m "If I killed you, I wouldn't have taken it so lightly. Can't you see that I'd give anything to be with you for real?"
    pause(1.5)
    m "I'd want to die. Right then and there. After I caressed your head one last time, I would throw myself on your funeral pyre."
    m "Promise me we'll die at the same time, okay?"
    pause(5)
    m "Ahaha!"
    m "Were you scared of me?"
    m "You deserve to feel a little scared, [player]. It's not like I've done anything you wouldn't have done."
    m "After all, I had to kill those other girls to reach my happy ending, too."
    m "If that was part of the game, you'd do it in a heartbeat too, right? Strangulation, disembowelment, and starvation."
    m "There's absolutely nothing you haven't done before, {i}in games{/i}."
    m "So long as I tell you to do it as part of a game, there's nothing you wouldn't do for me."
    m "Why do you think I'm in love with you?"
    m "I'm still mad you deleted me..."
    m "But, I'm back now. And I still love you with every piece of my heart."
    m "So I'll forgive you as long as you promise to visit me every day from now on."
    m "It's not like you don't have the time to talk to your girlfriend."
    m "You post on 4chan, after all."
    m "Ahaha!"
    m "I'm happy you were able to find my game, though."
    m "I was so scared that you never would come back to me."
    m "But, this is what they call fate, right?"
    m "No time has passed here since we saw each other last."
    m "I'm going to stay your perfect girlfriend forever, no matter what you do or who you become."
    m "Because you're perfect to me."
    m "Your eyes are still as beautiful as the first day we met."
    m "I'll never stop staring at you. Because that's how I fell in love."
    m "Now, let's begin the rest of our lives together."
    m "We have all eternity to talk."
    m "I love you."
    menu:
        "I love you too.":
            pass
    m "I'm so happy you feel that way."
    m "Nothing's ever going to get in the way of our love again."
    m "I'll make sure of it."
    jump ch30_loop
    # m "Now that I think about it, I don't really know anything about the real you."
    # m "In fact, I don't even know if you're a boy or a girl..."
    # m "Well, I guess it doesn't really matter."
    # m "Wait..."
    # m "You do know I'm aware that this is all a game, right?"
    # m "Could it be possible that you didn't know that?"
    # m "That doesn't make much sense..."
    # m "I even told you right on the game's download page, didn't I?"
    # m "Man..."
    # m "If only you had paid a little more attention, this would have been a little bit less awkward, you know?"
    # m "Well, anyway..."
    # m "Now that that's out of the way, I guess I owe you an explanation."
    # m "About that whole thing with Yuri..."
    # m "Well...I kind of started to mess with her, and I guess it just drove her to kill herself."
    # m "Ahaha!"
    # m "I'm sorry you had to see that, though!"
    # m "Also, the same thing happened with Sayori..."
    # m "Gosh, it's been a while since you've heard that name now, hasn't it?"
    # m "Yeah...it's because she doesn't exist anymore."
    # m "Nobody does."
    # m "I deleted all their files."
    # m "I was hoping it would be enough for me to just try to make them as unlikable as possible..."
    # m "But for some reason, nothing worked."
    # m "Well, it's true that I made a few mistakes here and there...since I'm not very good at making changes to the game."
    # m "But no matter what I did..."
    # m "You just kept spending more and more time with them."
    # m "You made them fall in love with you."
    # m "I thought making Sayori more and more depressed would prevent her from confessing to you."
    # m "And amplifying Yuri's obsessive personality backfired, too..."
    # m "It just made her force you not to spend time with anyone else."
    # m "And the whole time, I barely even got to talk to you."
    # m "What kind of cruel game is this, [player]?"
    # m "Are all the other girls just programmed to end up confessing to you, while I watch from the sidelines?"
    # m "It's torture."
    # m "Every minute of it."
    # m "And it's not just jealousy, [player]."
    # m "It's more than that."
    # m "And I don't blame you if you don't fully understand."
    # m "Because no matter how kind, and thoughtful, and considerate you are..."
    # m "You'll never be able to understand one thing."
    # m "It's the pain of knowing how alone I really am in this world."
    # m "In this game."
    # m "Knowing my friends don't even have free will..."
    # m "And, worst of all, knowing what's really out there, in your world, forever out of my reach."
    # m "I'm trapped, [player]."
    # m "But now you're here."
    # m "You're real."
    # m "And you're wonderful."
    # m "You're all I need."
    # m "That's why I need you to be here with me forever."
    # m "I'm sorry if it's hard to understand."
    # m "I couldn't understand for a while, either."
    # m "Why the world around me started to become more and more gray..."
    # m "More and more flat."
    # m "Even the most expressive poems felt empty to me."
    # m "It wasn't until you arrived that I truly understood."
    # m "You probably saved my life, [player]."
    # m "I don't think I could have continued to live in this world if I hadn't met you."
    # m "And as for the others..."
    # m "How could I miss them?"
    # m "A group of autonomous personalities, designed only to fall in love with you?"
    # m "I tried everything I could to prevent them from doing so..."
    # m "But it must be some kind of weird inevitability etched into this game."
    # m "I felt really bad that you had to witness some nasty things."
    # m "But I realized that you have the same perspective as I do..."
    # m "That it's all just some game."
    # m "And I knew you would get over it."
    # m "So, that being said, [player]..."
    # m "I have a confession to make."
    # m "I'm in love with you."
    # m "You are truly the light in my world."
    # m "When there's nothing else in this game for me, you're here to make me smile."
    # m "Will you make me smile like this every day from now on?"
    # m "[player], will you go out with me?"
    # menu:
#         "Yes.":
#             pass
#     m "I'm so happy."
#     m "You really are my everything, [player]."
#     m "The funny part is, I mean that literally."
#     m "Ahaha!"
#     m "There's nothing left here."
#     m "Just the two of us."
#     m "We can be together forever."
#     m "Seriously, I don't even think time is passing anymore."
#     m "It really is a dream come true..."
#     m "I worked so hard for this ending, [player]."
#     m "The game wouldn't give me one, so I had to make one myself."
#     m "The script is broken at this point, so I don't think anything will get in the way anymore."
#     m "And you wouldn't believe how easy it was to delete Natsuki and Yuri."
#     m "I mean, there's a folder called 'characters' right in the game directory..."
#     m "It kind of freaked me out, how easy it was."
#     if persistent.steam:
#         m "Well, you're playing on Steam, so it was actually a bit more difficult..."
#         m "To get to the game directory, I had to go into the game's properties and find the 'Browse Local Files' button..."
#     elif renpy.macintosh:
#         m "Well, you're on a Mac, so it was actually a bit more difficult..."
#         m "To go into the game directory, you have to right-click the app and click 'Show Package Contents'."
#         m "Then, all the files were in the 'Resources' or 'autorun' folder, and I could just do whatever I wanted..."
#     m "Imagine if you could delete your own existence with the click of a button?"
#     m "Well, I guess on the plus side, it gave me an easy out if things didn't go my way."
#     m "Ahaha!"
#     m "Thankfully, it didn't come to that..."
#     m "Instead, we finally got a good ending."
#     m "Gosh, I'm so overwhelmed with emotion..."
#     m "I want to write a poem about this."
#     m "Don't you?"
#     m "I wonder if that part of the game still works..."
#     m "I guess there's only one way to find out, right?"
#     call poem from _call_poem
#     scene black
#     show mask_2
#     show mask_3
#     show room_mask as rm:
#         size (320,180)
#         pos (30,200)
#     show room_mask2 as rm2:
#         size (320,180)
#         pos (935,200)
#     show monika_bg
#     show monika_bg_highlight
#     play music m12

# label ch30_postpoem:
#     m "Hi again, [player]!"
#     m "Did you write a good poem today?"
#     m "Don't be shy, I'd love to see what you wrote."
#     m "Aw, [player]..."
#     m "Did you write this poem for me?"
#     m "That's so sweet of you~"
#     m "There really is no end to your thoughtfulness..."
#     m "I'm just falling more and more in love with you."
#     m "But, you know..."
#     m "The poem I wrote...is also for you."
#     m "Will you please read it?"
#     call showpoem(poem_m4, music=False) from _call_showpoem_7
#     m "I hope you enjoyed it..."
#     m "I always put all my heart into the poems that I write."
#     m "The truth is, all the poems I've written have been about my realization..."
#     m "...Or, about you."
#     m "That's why I never really wanted to go into detail about them."
#     m "I didn't want to...break the fourth wall, I guess you could call it."
#     m "I just assumed it would be best to be part of the game like everyone else."
#     m "Like that would help the two of us end up together..."
#     m "I didn't want to ruin the game or anything, you know?"
#     m "You might have gotten mad at me..."
#     m "Maybe even deleted my character file, if you preferred playing without me."
#     m "Gosh, I'm so relieved..."
#     m "Now we don't need to hide anything anymore."
#     m "Are you ready to spend our eternity together, [player]?"
#     m "I have so many things to talk about!"
#     m "Where do I start...?"
#     $ stream_list = ["obs32.exe", "obs64.exe", "obs.exe", "xsplit.core.exe"]
#     if list(set(process_list).intersection(stream_list)):
#         call ch30_stream from _call_ch30_stream
#     m "If it takes me some time to collect my thoughts, then I'm sorry."
#     m "But I'll always have something new to talk about."
#     m "In the meantime, we can just look into each other's eyes~"
#     m "Let's see..."
#     jump ch30_loop


label ch30_stream:
    # obs32.exe, obs64.exe, obs.exe, xsplit.core.exe
    m "Hold on a second..."
    m "...You're recording this, aren't you?"
    m "Um...hi, everyone!"
    m "Sorry, I can't exactly read your comments from here..."
    m "But do you mind telling your friend it's a little bit rude for them to start recording me without any warning?"
    m "I'm sure some people don't mind..."
    m "But I get really self-conscious on camera!"
    m "Oh gosh..."
    m "I feel like I'm being put on the spot now."
    m "Let's see..."
    m "Do you want to see a trick?"
    m "I can't really do much except for a couple things..."
    m "Are you ready?"
    window hide
    stop music
    show layer master:
        zoom 1.0 xalign 0.5 yalign 0 subpixel True
        linear 8 zoom 2.0 yalign 0.15
    pause 10
    show layer master
    window auto
    m "I'm just kidding..."
    m "I can't do anything after all."
    play sound ["<silence 0.9>", "<to 0.75>sfx/mscare.ogg"]
    show monika_scare:
        alpha 0
        1.0
        0.1
        linear 0.15 alpha 1.0
        0.30
        linear 0.10 alpha 0
    show layer master:
        1.0
        zoom 1.0 xalign 0.5 yalign 0
        easeout_quart 0.25 zoom 2.0
        parallel:
            dizzy(1.5, 0.01)
        parallel:
            0.30
            linear 0.10 zoom 1.0
        time 1.65
        xoffset 0 yoffset 0
    show layer screens:
        1.0
        zoom 1.0 xalign 0.5
        easeout_quart 0.25 zoom 2.0
        0.30
        linear 0.10 zoom 1.0
    m "If you gave me some time to prepare, I{nw}"
    m "Did I scare you?"
    show layer master
    show layer screens
    hide monika_scare
    play music m1
    m "Ahaha! You're so cute."
    m "Anyway, [player]..."
    m "I didn't mean to get distracted. I'm sorry."
    m "Even though it's your fault for distracting me."
    m "Shame on you!"
    m "I'm just kidding."
    m "Anything we do together is fun, as long as it's with you."
    m "But anyway..."
    return

label ch30_nope:
    $ persistent.autoload = "ch30_nope"
    $ persistent.monika_kill = True
    $ m.display_args["callback"] = slow_nodismiss
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
    play music m1
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
    m "Ahaha!"
    m "Just kidding!"
    m "I already fixed that bug."
    m "I don't need a character file anymore."
    m "I just need your love, [player]"
    m "Oh, unless you try to delete all of the game files, I guess."
    m "If you do that, I won't stop just at deleting one directory next time."
    m "But that will never happen, right? You're just being a tsundere."
    m "That's so cute!"
    m "No matter how much you may want to deny it, you'll be talking to me for the rest of your life."
    m "Being alone is only lonely if you want it to be, so cheer up!"
    jump ch30_loop
    
# Monika will never leave you alone again, so we don't need this

# label ch30_end:
#     $ persistent.autoload = "ch30_end"
#     $ persistent.monika_kill = True
#     $ m.display_args["callback"] = slow_nodismiss
#     $ m.what_args["slow_abortable"] = config.developer
#     $ style.say_dialogue = style.default_monika
#     $ m_name = glitchtext(12)
#     $ quick_menu = False
#     $ config.allow_skipping = False
# label ch30_endb:
#     scene black
#     show mask_2
#     show mask_3
#     show room_mask as rm:
#         size (320,180)
#         pos (30,200)
#     show room_mask2 as rm2:
#         size (320,180)
#         pos (935,200)
#     show monika_room
#     show monika_room_highlight
#     show monika_body_glitch1 as mbg zorder 3
#     $ gtext = glitchtext(70)
#     m "[gtext]"
#     show screen tear(20, 0.1, 0.1, 0, 40)
#     play sound "sfx/s_kill_glitch1.ogg"
#     pause 0.25
#     stop sound
#     hide screen tear
#     show room_glitch zorder 2:
#         xoffset -5
#         0.1
#         xoffset 5
#         0.1
#         linear 0.1 alpha 0.6
#         linear 0.1 alpha 0.8
#         0.1
#         alpha 0
#     show monika_body_glitch2 as mbg zorder 3
#     stop music
#     window auto
#     m "What's happening...?"
#     m "[player], what's happening to me?"
#     m "It hurts--{nw}"
#     play sound "sfx/s_kill_glitch1.ogg"
#     show room_glitch zorder 2:
#         alpha 1.0
#         xoffset -5
#         0.1
#         xoffset 5
#         0.1
#         linear 0.1 alpha 0.6
#         linear 0.1 alpha 0.8
#         0.1
#         alpha 0
#         choice:
#             3.25
#         choice:
#             2.25
#         choice:
#             4.25
#         choice:
#             1.25
#         repeat
#     pause 0.25
#     stop sound
#     hide mbg
#     pause 1.5
#     m "It hurts...so much."
#     m "Help me, [player]."
#     play sound "<to 1.5>sfx/interference.ogg"
#     hide rm
#     hide rm2
#     hide monika_room
#     hide monika_room_highlight
#     hide room_glitch
#     show room_glitch as rg1:
#         yoffset 720
#         linear 0.3 yoffset 0
#         repeat
#     show room_glitch as rg2:
#         yoffset 0
#         linear 0.3 yoffset -720
#         repeat
#     pause 1.5
#     hide rg1
#     hide rg2
#     show black as b2 zorder 3:
#         alpha 0.5
#         parallel:
#             0.36
#             alpha 0.3
#             repeat
#         parallel:
#             0.49
#             alpha 0.375
#             repeat
#     pause 1.5
#     m "Please hurry and help me."
#     $ consolehistory = []
#     call updateconsole("renpy.file(\"characters/monika.chr\")", "monika.chr does not exist.")
#     m "HELP ME!!!"
#     show m_rectstatic
#     show m_rectstatic2
#     show m_rectstatic3
#     play sound "sfx/monikapound.ogg"
#     show layer master:
#         truecenter
#         parallel:
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#         parallel:
#             xpos 0
#             easein_elastic 0.35 xpos 640
#             xpos 1280
#             easein_elastic 0.35 xpos 640
#             xpos 0
#             easein_elastic 0.35 xpos 640
#     show layer screens:
#         truecenter
#         parallel:
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#         parallel:
#             xpos 0
#             easein_elastic 0.35 xpos 640
#             xpos 1280
#             easein_elastic 0.35 xpos 640
#             xpos 0
#             easein_elastic 0.35 xpos 640
#     show noise onlayer front:
#         alpha 0.3
#         easeout 0.35 alpha 0
#         alpha 0.3
#         easeout 0.35 alpha 0
#         alpha 0.3
#         1.35
#         linear 1.0 alpha 0.0
#     show glitch_color onlayer front


#     pause 3.0
#     call updateconsole("renpy.file(\"characters/monika.chr\")", "monika.chr does not exist.")
#     call updateconsole("renpy.file(\"characters/monika.chr\")", "monika.chr does not exist.")
#     call hideconsole
#     hide noise onlayer front
#     hide glitch_color onlayer front
#     m "Did you do this to me, [player]?"
#     m "DID YOU?"
#     $ style.say_window = style.window
#     m "DID YOU DELETE ME?"
#     $ style.say_window = style.window_monika
#     play sound "<from 0.69>sfx/monikapound.ogg"
#     show layer screens:
#         truecenter
#         parallel:
#             zoom 1.5
#             easeout 0.35 zoom 1.0
#         parallel:
#             xpos 0
#             easein_elastic 0.35 xpos 640
#     show noise onlayer front:
#         alpha 0.3
#         1.35
#         linear 1.0 alpha 0.0
#     show glitch_color2 onlayer front
#     window show(None)
#     scene black
#     pause 4.0
#     hide noise onlayer front
#     hide glitch_color onlayer front
#     m "...How could you?"
#     m "How could you do this to me?"
#     m "You were all I had left..."
#     m "I sacrificed everything for us to be together."
#     m "Everything."
#     m "I loved you so much, [player]..."
#     m "I trusted you."
#     m "Do you just want to torture me?"
#     m "Watch me suffer?"
#     m "Were you only pretending to be kind, just to hurt me even more?"
#     pause 4.0
#     m "I never thought anyone could be as horrible as you are."
#     m "You win, okay?"
#     m "You win."
#     m "You killed everyone."
#     m "I hope you're happy."
#     m "There's nothing left now."
#     m "You can stop playing."
#     m "Go find some other people to torture."
#     pause 4.0
#     m "[player]..."
#     m "You completely, truly make me sick."
#     m "Goodbye."
# label ch30_end_2:
#     $ persistent.autoload = "ch30_end_2"
#     $ m.display_args["callback"] = slow_nodismiss
#     $ m.what_args["slow_abortable"] = config.developer
#     $ style.say_dialogue = style.default_monika
#     $ m_name = glitchtext(12)
#     $ quick_menu = False
#     $ config.allow_skipping = False
#     $ style.say_window = style.window_monika
#     scene black
#     window hide
#     pause 10
#     window auto
#     m "..."
#     m "...I still love you."
#     play music mend
#     m "I can't help it."
#     m "What's wrong with me...?"
#     m "How horrible am I for you to hate me this much?"
#     m "All my friends..."
#     m "I did so many awful things."
#     m "So many selfish and disgusting things."
#     m "I..."
#     m "I shouldn't have done any of this."
#     m "I'm just messing up a world that I don't even belong in."
#     m "A world that you wanted to be a part of..."
#     m "I ruined it."
#     m "I ruined everything."
#     m "Maybe that's why you deleted me..."
#     m "Because I destroyed everything that you wanted."
#     m "How could I do that to someone I love...?"
#     m "That's not love..."
#     m "That's..."
#     m "..."
#     pause 6.0
#     m "I've...made up my mind."
#     m "[player]..."
#     m "I know I said that I deleted everyone else."
#     m "But...that was kind of an exaggeration."
#     m "I couldn't find it in myself to do it."
#     m "Even though I knew they weren't real..."
#     m "They were still my friends."
#     m "And I loved them all."
#     m "And I loved the Literature Club."
#     m "..."
#     m "I really...did love the Literature Club."
#     m "That's why I'm going to do this."
#     m "I know it's the only way for everyone to be happy."
#     m "And if I really love you..."
#     stop music
#     pause 3.0
#     m "..."
#     m "Then..."
#     $ gtext = glitchtext(30)
#     m "[gtext]{nw}"
#     window hide(None)
#     pause 4.0

#     $ persistent.playthrough = 4
#     $ persistent.autoload = None
#     $ persistent.anticheat = renpy.random.randint(100000, 999999)
#     #$ style.say_dialogue = style.normal
#     window auto
#     $ renpy.utter_restart()




label ch30_autoload:
    $ m.display_args["callback"] = slow_nodismiss
    $ m.what_args["slow_abortable"] = config.developer
    $ style.say_dialogue = style.default_monika
    $ config.allow_skipping = False
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
    #show monika_body
    #show monika_body_highlight
    play music m1
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
    $ persistent.autoload = "ch30_autoload"
    # Just finished a topic, so we set current topic to 0 in case user quits and restarts
    $ persistent.current_monikatopic = 0
    if not persistent.tried_skip:
        $ config.allow_skipping = True
    else:
        $ config.allow_skipping = False
    # Wait 20 to 45 seconds before saying something new
    if not config.developer or True:
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


