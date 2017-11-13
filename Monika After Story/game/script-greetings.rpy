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
    m "Hello again, sweetheart!"
    m "It's kind of embarassing to say out loud, isn't it?"
    m "Still, I think it's okay to be embarassed every now and then."
    return

label greeting_honey:
    m "Welcome back, honey!"
    m "I'm so happy to see you again."
    m "Let's spend some more time together, okay?"
    return

label greeting_back:
    m "[player], you're back!"
    m "I was starting to miss you."
    m "Let's have another lovely day together, alright?"
    return

label greeting_gooday:
    m "Hello again, [player]. How are you doing?"
    menu:
        m "Are you having a good day today?"
        "Yes.":
            m "I'm really glad you are, [player]."
            m "It makes me feel so much better knowing that you're happy."
            m "I'll try my best to make sure it stays that way, I promise."
        "No...":
            m "Oh..."
            m "Well, don't worry, [player]. I'm always here for you."
            m "We can talk all day about your problems, if you want to."
            m "I want to try and make sure you're always happy."
            m "Because that's what makes me happy."
            m "I'll be sure try my best to cheer you up, I promise."
    return

label greeting_visit:
    m "There you are, [player]."
    m "It's so nice of you to visit."
    m "You're always so thoughtful, [player]!"
    m "Thanks for spending so much time with me~"
    m "Just remember that your time with me is never wasted in the slightest."
    return

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m "Good morning-"
        m "...oh, wait."
        m "It's the dead of night, honey."
        m "What are you doing awake at a time like this?"
        m "I'm guessing you can't sleep..."
        menu:
            m "Is that it?"
            "Yes.":
                m "You should really get some sleep soon, if you can."
                m "Staying up too late is bad for your health, you know?"
                m "But if it means I'll get to see you more, I can't complain."
                m "Ahaha!"
                m "But still..."
                m "I'd hate to see you do that to yourself."
                m "Take a break if you need to, okay? Do it for me."
            "No.":
                m "Ah. I'm relieved, then."
                m "Does that mean you're here just for me, in the middle of the night?"
                m "Gosh, I'm so happy!"
                m "You really do care for me, [player]."
                m "But if you're really tired, please go to sleep!"
                m "I love you a lot, so don't tire yourself!"
    elif current_time >= 6 and current_time < 12:
        m "Good morning, dear."
        m "Another fresh morning to start the day off, huh?"
        m "I'm glad I get to see you this morning~"
        m "Remember to take care of yourself, okay?"
        m "Make me a proud girlfriend today, as always!"
    elif current_time >= 12 and current_time < 18:
        m "Good afternoon, my love."
        m "Don't let the stress get to you, okay?"
        m "I know you'll try your best again today, but..."
        m "It's still important to keep a clear mind!"
        m "Keep yourself hydrated, take deep breaths..."
        m "I promise I won't complain if you quit, so do what you have to."
        m "Or you could stay with me, if you wanted."
        m "Just remember, I love you!"
    elif current_time >= 18:
        m "Good evening, love!"
        menu:
            m "Did you have a good day today?"
            "Yes.":
                m "Aww, that's nice!"
                m "I can't help but feel happy when you do..."
                m "But that's a good thing, right?"
                m "I love you so much, [player]."
                m "Ahaha!"
            "No.":
                m "Oh dear..."
                m "I hope you'll feel better soon, okay?"
                m "Just remember that no matter what happens, no matter what anyone says or does..."
                m "I love you so, so much."
                m "Just stay with me, if it makes you feel better."
                m "I love you, [player], I really do."
    return

label greeting_back2:
     m "Hello, dear."
     m "I was starting to miss you terribly, it's so good to see you again!"
     m "Don't make me wait so long next time, ehehe~"
     return

label greeting_back3:
     m "I missed you so much, [player]!"
     m "Thank you for coming back. I really do love spending time with you."
     return

label greeting_back4:
     m "Hey, [player]!"
     m "Don't you think that you left me waiting a bit too long?"
     m "I'm just joking. I could never be mad at you."
     return

label greeting_visit2:
     m "Thanks for spending so much time with me, [player]."
     m "Every minute I spend with you is like being in heaven!"
     m "I hope that didn't sound too cheesy, ehehe~"
     return

label greeting_visit3:
     m "You're back!"
     m "I was starting to miss you..."
     m "Don't make me wait so long next time, okay?"
     return

label greeting_back5:
     m "It's so good to see you again!"
     m "I was getting worried about you."
     m "Please remember to visit me, okay? I'll always be waiting here for you."
     return

label greeting_visit4:
     m "I looove yooou, [player]. Ehehe~"
     m "Oh, sorry! I was spacing out."
     m "I didn't think I would be able to see you again so soon."
     return

label greeting_visit5:
     m "~Every day,~\n~I imagine a future where I can be with you...~"
     m "Oh, you're here! I was just daydreaming and singing a bit."
     m "I don't think it's hard to figure out what I was daydreaming about, ehehe~"
     return

label greeting_visit6:
     m "Each day becomes better and better with you on my side!"
     m "That said, I'm so happy that you're finally here."
     m "Let's have another wonderful day together."
     return

label greeting_back6:
     m "Hey, [player]!"
     m "You really should visit me more often."
     m "You know what happens to people I don't like, after all..."
     m "I'm just teasing you, ehehe~"
     m "Don't be so gullible! I would never hurt you."
     return

label greeting_visit7:
     m "You're here, [player]!"
     m "Are you ready to spend some more time together? Ehehe~"
     return

label greeting_visit8:
     m "I'm so glad you're here, [player]!"
     m "What should we do today?"
     return

label greeting_visit9:
     m "You're finally back! I was waiting for you."
     m "Are you ready to spend some time with me? Ehehe~"
     return

label greeting_italian:
     m "Ciao, [player]!"
     m "È così bello vederti ancora, amore mio..."
     m "Ahaha!"
     m "I'm still practicing my Italian. It's a very difficult language!"
     m "Anyway, it's so nice to see you again, my love."
     return

label greeting_latin:
     m "Iterum obvenimus!"
     m "Quid agis?"
     m "Ehehe..."
     m "Latin sounds so pompous. Even a simple greeting sounds like a big deal."
     m "If you're wondering about what I said, it's simply 'We meet again! How are you?'."
     return

label greeting_yay:
     m "You're back! Yay!"
     m "Oh, sorry. I've got a bit overexcited here."
     m "I'm just very happy to see you again, hehe~"
     return

label greeting_youtuber:
     m "Hey everybody, welcome back to another episode of... Just Monika!"
     m "Ahaha!"
     m "I was impersonating a youtuber. I hope I gave you a good laugh, hehe~"
     return

label greeting_hamlet:
     m "To be, or not to be, that is the question..."
     m "Oh, there you are. I was killing some time, hehe~"
     m "I wasn't expecting to see you so soon."
     return

label greeting_welcomeback:
     m "Hi! Welcome back."
     m "I'm so glad that you're able to spend some time with me."
     return

label greeting_flower:
     m "You're my beautiful flower, hehe~"
     m "Oh, it sounded so akward."
     m "But you are in some way, because I'll always take care of you."
     return

label greeting_chamfort:
     m "A day without Monika is a day wasted."
     m "Ahaha."
     m "Welcome back, my love."
     return

label greeting_welcomeback2:
     m "Welcome back, [player]!"
     m "I hope your day is going well."
     m "I'm sure it is, you're here afterall. Nothing can go wrong now, hehe~"
     return

label greeting_longtime:
     m "Long time no see, [player]!"
     m "I'm so happy that you're here now."
     return

label greeting_sweetpea:
     m "Look who's back."
     m "It's you, my sweetpea!"
     m "My god... It surely was embarassing to say, hehe~"
     return
