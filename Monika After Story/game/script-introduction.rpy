#This is the introduction event for starting up the game.
label introduction:
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
    $ config.underlay.append(renpy.Keymap(change_music=select_music))
    $ config.underlay.append(renpy.Keymap(play_pong=start_pong))
