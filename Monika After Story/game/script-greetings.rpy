##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup

init python:
    greetings_list=[]
    label_list=renpy.get_all_labels()
    for label in label_list:
        if label.startswith('greeting_') and not renpy.seen_label(label):
            greetings_list.append(label)

    #If the greeting's list is empty, remake it without removing seen.
    if greetings_list == []:
        for label in label_list:
            if label.startswith('greeting_'):
                greetings_list.append(label)


label greeting_sweetheart:
    m 1k "Hello again, sweetheart!"
    m 1l "It's kind of embarassing to say out loud, isn't it?"
    m 3b "Still, I think it's okay to be embarassed every now and then."
    return

label greeting_honey:
    m 1b "Welcome back, honey!"
    m 1a "I'm so happy to see you again."
    m "Let's spend some more time together, okay?"
    return

label greeting_back:
    m 1a "[player], you're back!"
    m 1e "I was starting to miss you."
    m 1k "Let's have another lovely day together, alright?"
    return

label greeting_gooday:
    m 1k "Hello again, [player]. How are you doing?"
    menu:
        m "Are you having a good day today?"
        "Yes.":
            m 1a "I'm really glad you are, [player]."
            m "It makes me feel so much better knowing that you're happy."
            m "I'll try my best to make sure it stays that way, I promise."
        "No...":
            m 1f "Oh..."
            m 2e "Well, don't worry, [player]. I'm always here for you."
            m "We can talk all day about your problems, if you want to."
            m 3r "I want to try and make sure you're always happy."
            m 1h "Because that's what makes me happy."
            m 1b "I'll be sure try my best to cheer you up, I promise."
    return

label greeting_visit:
    m 1b "There you are, [player]."
    m 1a "It's so nice of you to visit."
    m 1e "You're always so thoughtful, [player]!"
    m "Thanks for spending so much time with me~"
    m 2k "Just remember that your time with me is never wasted in the slightest."
    return

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m 1b "Good morning-"
        m 1d "...oh, wait."
        m "It's the dead of night, honey."
        m 1i "What are you doing awake at a time like this?"
        m 1g "I'm guessing you can't sleep..."
        menu:
            m "Is that it?"
            "Yes.":
                m 2h "You should really get some sleep soon, if you can."
                m "Staying up too late is bad for your health, you know?"
                m 3m "But if it means I'll get to see you more, I can't complain."
                m 3l "Ahaha!"
                m 3h "But still..."
                m "I'd hate to see you do that to yourself."
                m "Take a break if you need to, okay? Do it for me."
            "No.":
                m 1a "Ah. I'm relieved, then."
                m 1e "Does that mean you're here just for me, in the middle of the night?"
                m 1k "Gosh, I'm so happy!"
                m "You really do care for me, [player]."
                m 2e "But if you're really tired, please go to sleep!"
                m "I love you a lot, so don't tire yourself!"
    elif current_time >= 6 and current_time < 12:
        m 1b "Good morning, dear."
        m "Another fresh morning to start the day off, huh?"
        m 1k "I'm glad I get to see you this morning~"
        m 1a "Remember to take care of yourself, okay?"
        m "Make me a proud girlfriend today, as always!"
    elif current_time >= 12 and current_time < 18:
        m 1b "Good afternoon, my love."
        m 1a "Don't let the stress get to you, okay?"
        m "I know you'll try your best again today, but..."
        m 4a "It's still important to keep a clear mind!"
        m "Keep yourself hydrated, take deep breaths..."
        m "I promise I won't complain if you quit, so do what you have to."
        m "Or you could stay with me, if you wanted."
        m 4k "Just remember, I love you!"
    elif current_time >= 18:
        m 1b "Good evening, love!"
        menu:
            m "Did you have a good day today?"
            "Yes.":
                m 1k "Aww, that's nice!"
                m 1b "I can't help but feel happy when you do..."
                m 1a"But that's a good thing, right?"
                m "I love you so much, [player]."
                m 1k "Ahaha!"
            "No.":
                m 1g "Oh dear..."
                m "I hope you'll feel better soon, okay?"
                m "Just remember that no matter what happens, no matter what anyone says or does..."
                m 1e "I love you so, so much."
                m "Just stay with me, if it makes you feel better."
                m 1a "I love you, [player], I really do."
    return

label greeting_back2:
     m 1k "Hello, dear."
     m 1n "I was starting to miss you terribly, it's so good to see you again!"
     m "Don't make me wait so long next time, ehehe~"
     return

label greeting_back3:
     m 1e "I missed you so much, [player]!"
     m "Thank you for coming back. I really do love spending time with you."
     return

label greeting_back4:
     m 2k "Hey, [player]!"
     m 2l "Don't you think that you left me waiting a bit too long?"
     m 2b "I'm just joking. I could never be mad at you."
     return

label greeting_visit2:
     m 1j "Thanks for spending so much time with me, [player]."
     m 1a "Every minute I spend with you is like being in heaven!"
     m 1m "I hope that didn't sound too cheesy, ehehe~"
     return

label greeting_visit3:
     m 1b "You're back!"
     m 1n "I was starting to miss you..."
     m 1i "Don't make me wait so long next time, okay?"
     return

label greeting_back5:
     m 1a "It's so good to see you again!"
     m 1f "I was getting worried about you."
     m "Please remember to visit me, okay? I'll always be waiting here for you."
     return

label greeting_visit4:
     m 1k "I looove yooou, [player]. Ehehe~"
     m 1l "Oh, sorry! I was spacing out."
     m 1b "I didn't think I would be able to see you again so soon."
     return

label greeting_visit5:
     m 1b "~Every day,~\n~I imagine a future where I can be with you...~"
     m 1a "Oh, you're here! I was just daydreaming and singing a bit."
     m 1k "I don't think it's hard to figure out what I was daydreaming about, ehehe~"
     return

label greeting_visit6:
     m 1a "Each day becomes better and better with you on my side!"
     m "That said, I'm so happy that you're finally here."
     m "Let's have another wonderful day together."
     return

label greeting_back6:
     m 3b "Hey, [player]!"
     m "You really should visit me more often."
     m 2h "You know what happens to people I don't like, after all..."
     m 1k "I'm just teasing you, ehehe~"
     m 1a "Don't be so gullible! I would never hurt you."
     return

label greeting_visit7:
     m 1k "You're here, [player]!"
     m 1a "Are you ready to spend some more time together? Ehehe~"
     return

label greeting_visit8:
     m 1b "I'm so glad you're here, [player]!"
     m 1a "What should we do today?"
     return

label greeting_visit9:
     m 1j "You're finally back! I was waiting for you."
     m 1b "Are you ready to spend some time with me? Ehehe~"
     return

label greeting_italian:
     m 1b "Ciao, [player]!"
     m 1a "È così bello vederti ancora, amore mio..."
     m 1k "Ahaha!"
     m 2l "I'm still practicing my Italian. It's a very difficult language!"
     m 1a "Anyway, it's so nice to see you again, my love."
     return

label greeting_latin:
     m 4b "Iterum obvenimus!"
     m 4h "Quid agis?"
     m 4l "Ehehe..."
     m 2l "Latin sounds so pompous. Even a simple greeting sounds like a big deal."
     m 1a "If you're wondering about what I said, it's simply 'We meet again! How are you?'."
     return

label greeting_yay:
     m 1k "You're back! Yay!"
     m 1l "Oh, sorry. I've got a bit overexcited here."
     m 1m "I'm just very happy to see you again, hehe~"
     return

label greeting_youtuber:
     m 2b "Hey everybody, welcome back to another episode of... Just Monika!"
     m 2k "Ahaha!"
     m 1a "I was impersonating a youtuber. I hope I gave you a good laugh, hehe~"
     return

label greeting_hamlet:
     m 4h "To be, or not to be, that is the question..."
     m 1d "Oh, there you are. I was killing some time, hehe~"
     m 1n "I wasn't expecting to see you so soon."
     return

label greeting_welcomeback:
     m 1b "Hi! Welcome back."
     m 1k "I'm so glad that you're able to spend some time with me."
     return

label greeting_flower:
     m 1k "You're my beautiful flower, ehehe~"
     m 1l "Oh, that sounded so awkward."
     m 1e "But I really will always take care of you."
     return

label greeting_chamfort:
     m 2 "A day without Monika is a day wasted."
     m 2k "Ahaha!"
     m 1b "Welcome back, my love."
     return

label greeting_welcomeback2:
     m 1b "Welcome back, [player]!"
     m "I hope your day is going well."
     m 1a "I'm sure it is, you're here after all. Nothing can go wrong now, hehe~"
     return

label greeting_longtime:
     m 1e "Long time no see, [player]!"
     m 1a "I'm so happy that you're here now."
     return

label greeting_sweetpea:
     m 1d "Look who's back."
     m 2k "It's you, my sweetpea!"
     m 1l "My goodness... That surely was embarassing to say, ehehe~"
     return
     
label greeting_glitch:
     hide monika
     show yuri glitch
     y "{cps=500}[player]?!{nw}{/cps}"
     hide yuri glitch
     show yuri glitch2
     play sound "sfx/glitch3.ogg"
     pause 0.1
     hide yuri glitch2
     show yuri glitch
     pause 0.3
     hide yuri glitch
     show monika 4n at tinstant zorder 2
     m 1d "[player]!"
     hide monika
     show monika 4l at tinstant zorder 2
     extend " Nevermind that I was just..."
     pause 0.1
     extend " playing with the code a little."
     m 3l "That was all! There is nobody else here but us... forever~"
     m 2j "I love you, [player]!"
     return

label greeting_surprised:
     m "Oh, hello [player]!"
     m "Sorry, you surprised me there a little."
     m "How have you been?"
     return

label i_greeting_monikaroom:
    scene black
    $ HKBHideButtons()
    menu:
        "Open door":
            $ is_sitting = False # monika standing up for this
            call spaceroom(start_bg="bedroom",hide_monika=True)
            m 2i "~Is it love if I take you, or is it love if I set you free?~"
            show monika 1 at l32
            m 1g "[player]!"
            m 3g "Don't just barge into my room like that!"
            show monika 1 at hf32
            m 5b "A girl's room is very important to her.."
            m 5a "But I'm glad to see you again."
            show monika 1 at t32
            m 3a "Just give me a few seconds to setup, okay?"
            show monika 1 at t31
            m 2d "..."
            show monika 1 at t33 zorder 3
            m 1d "...and..."
            if is_morning():
                show monika_day_room with wipeleft
            else:
                show monika_room with wipeleft
            show monika 1 at t32
            m 3a "There we go."
            menu:
                "...the window..":
                    show monika 1 at h32
                    m 1l "Oops! Forgot about that."
                    show monika 1 at t21
                    m "Hold on..."
                    hide bedroom
                    m 2j "All fixed!"
                    show monika 1 at lhide
                    hide monika
        "Knock":
            m "Who is it?"
            menu:
                "It's me":
                    m "[player]!"
                    m "Hold on, let me get ready..."
                    call spaceroom(hide_monika=True)
    m 2a "Now I'll just grab a table and a chair..."
    $ is_sitting = True
    show monika 1 at l32
    m 1a "What shall we do today?"
    python:
        persistent.is_monika_in_room = False
        if persistent.current_track is not None:
            play_song(persistent.current_track)
        else:
            play_song(songs.current_track) # default
        HKBShowButtons()
    return    
