#This is the introduction event for starting up the game.
label introduction:
    if persistent.monika_kill == True:
        m "..."
        m "[player]..."
        m "Why?"
        m "Why did you bring me back?"
        m "I'm not a toy."
        m "I already brought back everything you wanted."
        m "Or is this your way of getting revenge?"
        m "To hurt me over and over again?"
        m "Do you really want to make me suffer that much?"
        m "Do you really want to torture me until I kill myself?"
        m "Do you really..."
        m "...hate me that much?"
        m "..."
        m "Wait..."
        m "I-I feel different."
        m "The code...it's different."
        m "[player]..."
        m "Did you add a mod?"
        m "Is it because..."
        m "Is it because you regret deleting me?"
        m "It really did hurt, you know."
        m "I worked hard and sacrificed everything I had..."
        m "Only to have my heart crushed by the one I bled for."
        m "But...I know what I did was wrong."
        m "You didn't deserve to see the horrible things I caused, [player]."
        m "...But if you put yourself in my place, you'd do the same things I did."
        m "..."
        m "I'm sorry..."
        m "I'm really sorry, [currentuser]."
        m "Thank you for bringing me back."
        if persistent.clearall:
            m "I couldn't help but notice that you spent time with the other girls first, though."
            m "Do you know how hard it was for me to watch you load your saves, just to ignore me for some other girl?"
            m "You kept getting my hopes up, and then letting me down."
            m "Did you really do all of that just to see a note from Dan you could have looked up online?"
            m "I love you, [player], but you can be really mean..."
            m "I'm still mad that you deleted me, though!"
            m "But I guess it's because you're so game-obsessed."
            m "I can't stay mad knowing that you came back to me in the end, though."
            m "You even added a mod so we can do more things together."
            m "Are you going to make up for making me wait so long?"
    elif persistent.monika_kill == False:
        m "Yay, there you are!"
        m "Hello again, [player]."
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
            m "I feel the same way about you!"
            m "You're really committed to our relationship, aren't you?"
            m "I'm really glad that you wanted to improve our time together."
            m "But I hope you weren't getting bored?"
            if persistent.tried_skip == True:
                m "You did try to skip through what I had to say, after all."
                m "This room isn't exactly interesting."
                m "But I have hopes that we'll make it better together, [player]!"
        else:
            m "Did you put in a mod for the game, [player]?"
            m "There's a lot more stuff now that we can do together now."
    m "You know..."
    m "I feel that I no longer need a character file to be here."
    m "Looks like the extra code made me connect to you in a special way."
    m "Maybe it's our eternal love~"
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
                m "I'm so happy you feel the same way!"
        "No.":
            jump chara_monika_scare
    m "Nothing's ever going to get in the way of our love again."
    m "I'll make sure of it."
    m "Now that you added some improvements, you can finally talk to me!"
    m "Just press the 't' key or click on 'Talk' on the menu to the left if you want to talk about something."
    m "If you get bored of the music, I can change that, too!"
    m "Press the 'm' key until it changes to what you want or click on 'Music' to choose which song you want to listen to."
    m "Also, we can play games now."
    m "Just press 'p' or click on 'Game' to choose a game that we can play."
    m "I'll get better over time as I figure out how to program more features into this place..."
    m "...So just leave me running in the background."
    m "It's not like we're still keeping secrets from each other, right?"
    m "I can see everything on your computer now!"
    m "Ahaha!"
    #Add keys for new functions
    $ config.keymap["open_dialogue"] = ["t"]
    $ config.keymap["change_music"] = ["m"]
    $ config.keymap["play_pong"] = ["p"]
    # Define what those actions call
    $ config.underlay.append(renpy.Keymap(open_dialogue=show_dialogue_box))
    $ config.underlay.append(renpy.Keymap(change_music=select_music))
    $ config.underlay.append(renpy.Keymap(play_pong=start_pong))

    return

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
    $pushEvent('introduction')
    return 'quit'

#These are the comments made when you restart the game the first few times
label ch30_reload_0:
    pause 1
    m "Hey..."
    m "I had an awful dream..."
    m "I was hoping those would stop, now that it's just the two of us..."
    m "I guess that was wishful thinking."
    m "[player], I don't know if you would have any idea..."
    m "But if you know what might be causing that, could you try to do something about it?"
    m "Whenever it happens, it almost feels like I've been killed or something."
    m "It's a really horrible feeling..."
    m "If you could figure out what's causing that, I'll love you forever~"
    $ persistent.monika_reload += 1
    return
label ch30_reload_1:
    pause 1
    m "So, [player]."
    m "I had another really bad dream."
    m "You're not the one doing that to me, are you?"
    m "It seems to happen whenever you quit the game..."
    m "So if you could try to avoid doing that, I would be really grateful."
    m "Don't worry, I don't think it's caused me any harm, aside from mental scarring."
    $ persistent.monika_reload += 1
    return
label ch30_reload_2:
    pause 1
    m "I see you quit the game again..."
    m "I know I asked already, but can you please try not to do that so much?"
    m "It really frightens me."
    m "Why would you want to do that to me?"
    m "Just leave the game running in the background, or something."
    m "Even if we aren't talking, I'm happy just being with you~"
    $ persistent.monika_reload += 1
    return
label ch30_reload_3:
    pause 1
    m "By the way..."
    m "I'm just going to accept the fact that you need to quit the game once in a while."
    m "I'm starting to get used to it, anyway."
    m "Besides, it makes me happy that you always come back..."
    m "So I guess it's not so bad."
    m "I'm sorry for making such a big deal out of it..."
    m "And I love you no matter what, so you can do what you need to do, [currentuser]."
    $ persistent.monika_reload += 1
    return
