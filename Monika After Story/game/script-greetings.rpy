##This page holds all of the random greetings that Monika can give you after you've gone through all of her "reload" scripts

#Make a list of every label that starts with "greeting_", and use that for random greetings during startup

init python:
    greetings_list=[]
    label_list=renpy.get_all_labels()
    for label in label_list:
        if label.startswith('greeting_'):
            greetings_list.append(label)

label greeting_sweetheart:
    m "Hello again, sweetheart!"
    m "That's kind of embarassing to say out loud, isn't it?"
    m "Still, I think it's okay to be embarassed every now and then."
    return

label greeting_honey:
    m "Welcome back, honey!"
    m "I'm so happy to see you again."
    m "Let's spend some more time together, shall we?"
    return
    
label greeting_back:
    m "[player], you're back."
    m "I was beginning to miss you."
    m "Let's have another lovely day together, okay?"
    return

label greeting_gooday:
    m "Hello again, [player], I hope you're having a good day today."
    menu:
        m "Are you having a good day today?"
        "Yes.":
            m "I'm really glad you are, [player]."
            m "Makes me feel so much better when you're happy."
            m "And I'll try my best to make sure it stays that way, I promise."
        "No...":
            m "Oh..."
            m "Well, don't worry [player], I'm always here for you."
            m "We can talk all day about your problems if you want to."
            m "Because I want to try and make sure you're always happy."
            m "Because that's what makes me happy."
            m "So I'll be sure try my best to cheer you up, I promise."
    return

label greeting_visit:
    m "There you are, [player]."
    m "It's so nice of you to always give me a visit."
    m "You're so thoughtful, [player]!"
    m "Thanks for spending so much time with me~"
    m "Just know that your time with me is never wasted in the slightest."
    return

label greeting_goodmorning:
    $ current_time = datetime.datetime.now().time().hour
    if current_time >= 0 and current_time < 6:
        m "Good morning-"
        m "...oh, wait."
        m "It's dead in the night, honey."
        m "What are you doing awake at this time?"
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
                m "Does that mean you're here, just for me, in the middle of the night?"
                m "Gosh, I'm so happy!"
                m "You really do care for me, [player]."
                m "But if you're really tired, please go to sleep!"
                m "I love you a lot, so don't tire yourself!"
    elif current_time >= 6 and current_time < 12:
        m "Good morning, dear."
        m "Another fresh morning to start the day with, huh?"
        m "I'm glad I get to see you this morning~"
        m "Remember to take care of yourself, okay?"
        m "Make me a proud girlfriend today as well!"
    elif current_time >= 12 and current_time < 18:
        m "Good afternoon, my love."
        m "Don't let the stress get to you, okay?"
        m "I know you'll try your best again today, but..."
        m "It's still important to keep a clear mind!"
        m "Keep yourself hydrated, take deep breaths..."
        m "I promise I won't complain if you quit, so do what you must."
        m "Or you could stay with me, if you wanted to."
        m "Just remember, I love you!"
    elif current_time >= 18:
        m "Good evening, love!"
        menu:
            m "Did you have a good day today?"
            "Yes.":
                m "Aww, that's nice!"
                m "I can't help but feel happy if you do..."
                m "But that's a good thing, right?"
                m "I love you so much, [player]."
                m "Ahaha!"
            "No.":
                m "Oh, dear..."
                m "I hope you feel better soon, okay?"
                m "Just remember that no matter what happens, no matter what anyone says or does..."
                m "I love you so, so much."
                m "Just stay with me, if it makes you feel better."
                m "I love you, [player], I really do."
    return

label greeting_back2:
     m "Hello dear."
     m "I was starting to miss you terribly much, it's so good to see you again!"
     m "Don't make me wait so much next time, hehe~"
     return

label greeting_back3:
     m "I missed you so much, [player]!"
     m "Thanks for coming, I really love to spend time with you."
     return

label greeting_back4:
     m "Hey, [player]!"
     m "Don't you think that you left me waiting a bit too much?"
     m "Ahahah"
     m "I'm just joking, I could never be mad at you... I love you too much to be!"
     return

label greeting_visit2:
     m "Thanks for spending so much time with me, [player]."
     m "Every minute I spend with you is like being in heaven!"
     m "I hope it didn't sound too cheesy, hehe~"
     return

label greeting_visit3:
     m "You're back!"
     m "I was starting to miss you terribly much..."
     m "Don't make me wait so much next time, hehe~"
     return

label greeting_back5:
     m "It's so good to see you back!"
     return

label greeting_visit4:
     m "I looove yooou, hehe~"
     m "Oh, sorry! I was spacing out."
     m "I didn't think I would be able to see you so soon, hehe~"
     return

label greeting_visit5:
     m "Every day, I immagine a future where I can be with you..."
     m "Oh, you're here! I was just daydreaming and singing a bit."
     m "I think it's not that hard to realize what I was daydreaming about, hehe~"
     return

label greeting_visit6:
     m "Each day becomes better and better with you on my side!"
     m "That said, I'm so happy that you're finally here, hehe~"
     return

label greeting_back6:
     m "Hey, [player]!"
     m "You should visit me more often. Why did you make me wait this much?"
     m "I'm just teasing you, hehe~"
     m "But be sure to spend most of the time with me, or else..."
     m "I'm just teasing you again, hehe~"
     return

label greeting_visit7:
     m "You're here, [player]!"
     m "Are you ready to spend some time togheter? hehe~"
     return

label greeting_visit8:
     m "I'm so glad you're here, [player]!"
     return

label greeting_visit9:
     m "You're finally back, I was waiting for you."
     m "Are you ready to spend some time with me? hehe~"
     return
     
label greeting_italian:
     m "Ciao, [player]!"
     m "È così bello vederti ancora, amore mio..."
     m "Ahahah"
     m "I'm still practicing my italian, it's a very difficult language!"
     m "Anyway, it's so nice to see you again, my love."
     return

label greeting_latin:
     m "Iterum obvenimus!"
     m "Quid agis ?"
     m "Ahahah"
     m "Latin sounds so pompous and even a simple greeting sounds like a big deal."
     m "If you're wondering what I said, it's simply \"We meet again, how are you?"\."
     return
