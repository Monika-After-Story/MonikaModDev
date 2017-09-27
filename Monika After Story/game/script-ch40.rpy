image sayori end-glitch:
    "sayori/end-glitch1.png"
    0.15
    "sayori/end-glitch2.png"
    0.15
    "sayori/end-glitch1.png"
    0.15
    "sayori/end-glitch2.png"
    1.00
    "sayori/end-glitch1.png"
    0.15
    "sayori/end-glitch2.png"
    0.15
    "sayori/end-glitch1.png"
    0.15
    "sayori/end-glitch2.png"

label ch40_main:
    $ s_name = "Sayori"
    stop music fadeout 2.0
    scene bg residential_day
    with dissolve_scene_full
    play music t2
    "It's an ordinary school day, like any other."
    "As usual, I'm surrounded by couples and friend groups walking to school together."
    "I always tell myself it's about time I meet some girls or something like that..."
    show sayori 1a at t11
    s "Hey, [player]..."
    "...Well, there already is one girl."
    "That girl is Sayori, my neighbor and good friend since we were children."
    "We used to walk to school together every day..."
    "...And recently, we've picked up that habit once again."
    s "[player], are you proud of me?"
    mc "Eh? For what?"
    s 1c "You know..."
    s "For waking up on time!"
    mc "Well, you've been doing that for a while now..."
    s "Uh-huh!"
    s 4h "But you never even said anything about it!"
    show sayori at s11
    s "Even though we walk to school together every day..."
    mc "Well, yeah..."
    mc "I always thought it was implied."
    mc "It's embarrassing to say out loud."
    s 1d "C'mon, please?"
    s "It's good motivation~"
    mc "Fine, fine..."
    mc "I'm proud of you, Sayori."
    show sayori at t11
    s 1q "Ehehe~"
    show sayori at thide zorder 1
    hide sayori
    "We cross the street together and make our way to school."
    "As we draw near, the streets become increasingly speckled with other students making their daily commute."
    show sayori 3a at t11 zorder 2
    s "By the way, [player]..."
    s "Have you decided on a club to join yet?"
    mc "A club?"
    mc "I told you already, I'm really not--"
    "I start to say what I always do - that I'm not interested in joining any clubs."
    "But something tells me Sayori would take more offense to that now."
    "After all, how could I tell her that clubs are a waste of time..."
    "...when she's starting a club of her very own?"
    mc "...Actually, yeah."
    mc "I think I've decided on a club."
    show sayori at h11
    s 1m "Really?!"
    s 1r "Which one? Tell me!"
    mc "Hmm..."
    mc "I think I'll keep it a surprise."
    s 5d "Boo..."
    s "You meanie."
    mc "Be patient, you'll find out soon enough."
    "I used to ask myself why I let myself get lectured by such a carefree girl."
    "But I started to realize that in a way, I envy her."
    "When Sayori puts her mind to something, she can accomplish great things."
    "So that's why I feel like I should do something special for her."

    scene bg class_day
    with wipeleft_scene

    "The school day is as ordinary as ever, and it's over before I know it."
    "After I pack up my things, I stand up, gathering my motivation."
    mc "Let's see..."
    stop music fadeout 2.0

    scene bg corridor
    with wipeleft_scene
    "I recall the room number of the club from a flier I saw."
    "I walk across the school and upstairs - a section of the school I rarely visit, being generally used for third-year classes and activities."
    "Before long, I find the room."
    "I timidly open the door in front of me."
    scene bg club_day
    with wipeleft
    play music t3
    mc "Hello...?"
    show sayori 1m at t32
    s "Ah!"
    s "[player]...?!"
    s 1c "W-What are you doing here?"
    mc "Well...I just--"
    "Eh? I glance around the room."
    show natsuki 3a at f31
    n "Huh."
    n "So you're the [player] that Sayori's always talking about?"
    show natsuki at t31
    show yuri 2t at f33
    y "T-Thank you for stopping by!"
    y 2m "It's a pleasure to meet you, [player]."
    y "We're the Literature Club."
    y 3v "I-I hope you enjoy your visit!"
    show yuri at t33
    show natsuki at f31
    n 3g "C'mon, Yuri..."
    n "No need to be so formal."
    n "He's gonna think we're really strict or something..."
    show natsuki at t31
    $ y_name = "Yuri"
    $ n_name = "Natsuki"
    show yuri at f33
    y 3q "Ah..."
    y "Sorry, Natsuki..."
    show yuri at t33
    "The tall one, whose name is apparently Yuri, seems to be quite shy compared to the others."
    "In comparison, the girl named Natsuki - despite her size - seems like the assertive one."
    mc "Well, it's nice to meet both of you."
    mc "I look forward to working with you."
    show sayori at f32
    s 1n "W-Working...?"
    s 1b "[player], don't tell me..."
    s "You're..."
    show sayori at t32
    mc "That's right."
    mc "The club I've decided to join is yours, Sayori."
    mc "The Literature Club."
    "Sayori's eyes light up."
    show sayori at f32
    s 1n "...No way."
    s 1s "No way!"
    show sayori at hf32
    s 4s "Aaaahhhhhh!"
    "Sayori wraps her arms around me, jumping up and down."
    show sayori at t32
    mc "H-Hey--"
    show natsuki at f31
    n 3y "Ehehe."
    n "Well, if Sayori is this happy, then I'm sure it won't be so bad to have you around."
    show natsuki 3a at t31
    show yuri at f33
    y 1s "Not to mention there's four of us now."
    y "That means we can become an officially-recognized club."
    show yuri at t33
    show sayori at f32
    s 1x "I don't know what to say!"
    s "We have to celebrate!"
    show sayori at t32
    show yuri at f33
    y 1m "Huhu."
    y "What an appropriate day for that, isn't it?"
    show yuri 1a at t33
    show sayori at f32
    s 1r "Yeah!"
    s 1x "After all, Natsuki decided to--"
    show sayori at t32
    show natsuki at f31
    n 1w "Hey, don't ruin the surprise!"
    show natsuki at t31
    show sayori at f32
    s 5a "Ehehe, sorry..."
    show sayori at t32
    show natsuki at f31
    n 1k "Everyone sit down at the table, okay?"
    show natsuki at t31
    show yuri at f33
    y 1a "How about I make some tea as well?"
    hide sayori
    hide natsuki
    hide yuri
    with wipeleft
    "The girls have a few desks arranged to form a table."
    "Natsuki and Yuri walk over to the corner of the room, where Natsuki grabs a wrapped tray and Yuri opens the closet."
    "Still feeling awkward, I take a seat next to Sayori."
    "Natsuki proudly marches back to the table, tray in hand."
    show natsuki 2z at t22 zorder 2
    n "Okaaay, are you ready?"
    n "...Ta-daa!"
    show sayori 4m at t21 zorder 2
    s "Uwooooah!"
    "Natsuki lifts the foil off the tray to reveal a dozen white, fluffy cupcakes decorated to look like little cats."
    "The whiskers are drawn with icing, and little pieces of chocolate were used to make ears."
    show sayori at f21
    s 4r "So cuuuute~!"
    show sayori at t21
    mc "Wow, those look amazing."
    show natsuki at f22
    n 2d "Ehehe. Well, you know."
    n "Just hurry and take one!"
    show natsuki at t22
    "Sayori grabs one first, then I follow."
    show sayori at f21
    s 4q "It's delicious!"
    show sayori at t21
    "Sayori talks with her mouth full and has already managed to get icing on her face."
    "I turn the cupcake around in my fingers, looking for the best angle to take a bite."
    show sayori at thide zorder 1
    hide sayori
    show natsuki 1c at t32 zorder 2
    "Natsuki is quiet."
    "I can't help but notice her sneaking glances in my direction."
    "Is she waiting for me to take a bite?"
    "I finally bite down."
    "The icing is sweet and full of flavor - I wonder if she made it herself."
    mc "This is really good."
    mc "Thank you, Natsuki."
    n 42c "W-Well...of course it is!"
    n "I'm a pro, after all!"
    n 42a "There's no need to thank me or anything..."
    show natsuki at thide zorder 1
    hide natsuki
    "As Natsuki struggles to accept the compliment, Yuri returns to the table, carrying a tea set."
    "She carefully places a teacup in front of each of us before setting down the teapot next to the cupcake tray."
    show yuri 1a at t11 zorder 2
    mc "You keep a whole tea set in this classroom?"
    y "Don't worry, the teachers gave us permission."
    y "After all, doesn't a hot cup of tea help you enjoy a good book?"
    mc "Ah... I-I guess..."
    show natsuki 2y at f31
    n "Ehehe. Already trying to impress our new member, Yuri?"
    show natsuki at t31
    show yuri at f11
    y 3n "Eh?! T-That's not..."
    show yuri at t11
    show natsuki at thide
    hide natsuki
    "Insulted, Yuri looks away."
    y 4b "I meant that, you know..."
    mc "I believe you."
    mc "Well, tea and reading might not be a pastime for me, but I at least enjoy tea."
    y 2u "I'm glad..."
    "Yuri faintly smiles to herself in relief."
    y 1a "So, [player], what kinds of things do you like to read?"
    mc "Well... Ah..."
    "Considering how little I've read these past few years, I don't really have a good way of answering that."
    mc "...Manga..."
    "I mutter quietly to myself, half-joking."
    show natsuki 1c at t41 zorder 2
    "Natsuki's head suddenly perks up."
    "It looks like she wants to say something, but she keeps quiet."
    show natsuki at thide zorder 1
    hide natsuki
    y 3u "N-Not much of a reader, I guess..."
    mc "...Well, that can change..."
    "What am I saying?"
    "I spoke without thinking after seeing Yuri's sad smile."
    mc "Anyway, what about you, Yuri?"
    y 1l "Well, let's see..."
    "Yuri traces the rim of her teacup with her finger."
    y 1a "My favorites are usually novels that build deep and complex fantasy worlds."
    y "The level of creativity and craftsmanship behind them is amazing to me."
    y 1f "And telling a good story in such a foreign world is equally impressive."
    "Yuri goes on, clearly passionate about her reading."
    "She seemed so reserved and timid since the moment I walked in, but it's obvious by the way her eyes light up that she finds her comfort in the world of books, not people."
    y 2m "But you know, I like a lot of things."
    y 2a "Don't feel intimidated if you don't read much, okay?"
    y "I'm certain we can find something that we have in common."
    show yuri at t22
    show natsuki 2c at f21
    n "Hey, Yuri..."
    show natsuki at t21
    show yuri at f22
    y 2f "Eh?"
    show yuri at t22
    show natsuki at f21
    n 2h "Well, about...you know, the first thing he said..."
    show natsuki at t21
    mc "Manga?"
    show yuri at f22
    y 2i "That's right..."
    y "Natsuki tends to read manga in the clubroom--"
    show yuri at t22
    show natsuki at f21
    n 1r "D-Don't just say it!!"
    "For some reason, Natsuki seems embarrassed about it."
    n 1q "Besides..."
    n "Manga...is literature too, you know?"
    n 1w "So...if [player] wants to read some of my manga, then don't try to stop him or anything!"
    show natsuki 1i at t21
    show yuri at f22
    y 1l "Natsuki..."
    y "I wouldn't do such a thing."
    y 1i "However, it could also be nice for us to diversify ourselves a little..."
    y "He can take this opportunity to try something new, as well."
    y 1s "Wouldn't you agree, [player]?"
    show yuri at t33
    show natsuki at t32
    show sayori 1l at f31
    s "M-Maybe--"
    "Sensing the tension, Sayori jumps in."
    s 1x "Maybe we can all try something new!"
    s 1l "I think it could be fun..."
    s 1c "And we'll all get to know each other a little bit better, too!"
    s 1l "I mean..."
    s "that's the kind of thing literature clubs do...right?"
    show sayori at t31
    show yuri at f33
    y 1v "..."
    y "I-I don't disagree or anything..."
    show yuri at t33
    show natsuki at f32
    n 2j "Yeah..."
    n "You're right as usual, President."
    show natsuki at t32
    show sayori at f31
    s 1q "Ehehe~"
    show sayori at t31
    show natsuki at f32
    n 2c "Guess that means I should try picking up a novel or something, huh...?"
    show natsuki at t32
    mc "Well, that would make two of us..."
    mc "I wouldn't mind doing it if I'm not the only one."
    show sayori at thide
    hide sayori
    show natsuki at f21
    show yuri at t22
    n 2y "Then as for Yuri..."
    show natsuki at t21
    show yuri at f22
    y 2n "Eh...?"
    y "I...I have to read manga...?"
    show yuri at t22
    show natsuki at f21
    n 4i "Jeez..."
    n 4h "You were the one who suggested we diversify!"
    n "You should be a little more open-minded..."
    n 4u "It's kind of hurtful..."
    show natsuki at t21
    show yuri at f22
    y 2t "Hurtful...?"
    y 2v "I-I didn't realize..."
    y "..."
    "With a guilty expression, Yuri thinks to herself."
    y 2w "I'm sorry for disrespecting your interests, Natsuki."
    y "If...if you're into it, then I'm sure it's a worthy form of literature."
    show yuri at t22
    show natsuki at f21
    n 5q "...Are you just saying that?"
    show natsuki at t21
    show yuri at f22
    y "No..."
    y "I've realized my error."
    y 2t "So, if you're willing to consider starting a novel..."
    y 2u "...Then I'll offer my gratitude by finding a manga to read as well."
    show yuri at t22
    show natsuki at f21
    n 1l "Really?!"
    n 12c "I-I mean..."
    n "It...makes me happy that you'd do that for me, Yuri."
    n 2c "You can trust me to find something that you'll really like, okay?"
    show natsuki at t21
    show yuri at f22
    y 1m "Same here..."
    y 1h "Perhaps I'll visit the bookstore after the club meeting."
    show yuri at t22
    show natsuki at f21
    n 1q "Just...just you?"
    show natsuki at t21
    show yuri at f22
    y 3q "A-Ah--"
    y 4a "Would you...like to come along with me?"
    show yuri at t22
    show natsuki at f21
    n 5s "Um..."
    n "If you don't mind..."
    show natsuki at t21
    show yuri at f22
    y 3t "Not at all!"
    y "I always go alone, so..."
    show yuri at t22
    show natsuki at f21
    n "Yeah, me too..."
    show natsuki at t21
    show sayori 4s at l41
    s "This is so cute~!"
    mc "Sayori, shut up..."
    show sayori at lhide
    hide sayori
    show natsuki at f21
    n 2j "I'll show you some manga there too, okay?"
    show natsuki at t21
    show yuri at f22
    y 1a "Yes."
    y "I look forward to it."
    show natsuki at thide
    show yuri at thide
    hide natsuki
    hide yuri
    "Natsuki and Yuri start to clean up the food."
    show sayori 1q at t11
    s "Ehehe~"
    s 1x "I guess the meeting's over, huh?"
    mc "Yeah, looks like it..."
    mc "It's nice to see everyone getting along."
    s 1q "Isn't it?"
    s 1d "I think everyone likes you too, [player]."
    mc "You think so...?"
    mc "Well, everyone always seems to get along a little better with you around, Sayori."
    s 1y "Aww, [player]~"
    s "Don't say something like that, it's embarrassing!"
    mc "Well, whatever."
    mc "I was surprised when you told me you were starting a club..."
    mc "But I think you're pulling it off just fine."
    s 1r "We're gonna make it the best club ever!"
    s 1x "Now that you joined, every day is gonna be so much fun."
    stop music fadeout 2.0
    s 1a "Hey, [player]..."
    s "I really want to thank you."
    s "I mean, I'm really happy that you joined the club and everything..."
    s "But the truth is, I already knew you were going to."
    s 1q "Ehehe~"
    s 1a "There's actually something else."
    $ if all(clear for clear in persistent.clear): persistent.clearall = True
    if persistent.clearall:
        call ch40_clearall from _call_ch40_clearall
    else:
        call ch40_clearnormal from _call_ch40_clearnormal
    window hide(None)
    window auto
    $ quick_menu = False
    return

    label ch40_clearnormal:
        show sayori 1a at t11 zorder 2
        s "I wanted to thank you for getting rid of Monika."
        play music hb
        show black:
            alpha 0.5
            parallel:
                0.36
                alpha 0.5
                repeat
            parallel:
                0.49
                alpha 0.475
                repeat
        show layer master at heartbeat
        s 1b "That's right..."
        s "I know everything that she did."
        s 1x "Maybe it's because I'm the President now."
        s "But I really know everything, [player]."
        s 1q "Ehehe~"
        s 1d "I know how hard you tried to make everyone happy."
        s "I know about all of the awful things that Monika did to make everyone really sad..."
        s 1b "But none of that matters anymore."
        s "It's just us now.{nw}"
        show screen tear(20, 0.1, 0.1, 0, 40)
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.25
        stop sound
        hide screen tear
        show room_glitch zorder 1:
            xoffset -5
            0.1
            xoffset 5
            0.1
            linear 0.1 alpha 0.6
            linear 0.1 alpha 0.8
            0.1
            alpha 0
        s "It's just us now.{fast}"
        hide room_glitch
        s 1d "And you made me the happiest girl in the whole world."
        s "I can't wait to spend every day like this..."
        s "With you."
        play sound "sfx/s_kill_glitch1.ogg"
        show room_glitch zorder 1:
            xoffset -10
            0.1
            xoffset 0
            0.1
            linear 0.1 alpha 0.6
            linear 0.1 alpha 0.8
            0.1
            alpha 1.0
        pause 0.3
        stop sound
        s 1q "Forever and ever..."
        hide sayori
        show sayori 1a at face onlayer screens zorder 101
        s "F"
        s "o"
        s "r"
        show screen tear(20, 0.1, 0.1, 0, 40)
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.25
        stop sound
        hide screen tear
        s "e"
        s "v"
        s "e"
        window show(None)
        stop music
        call screen dialog("No...", ok_action=Return())
        show layer master
        hide black
        show sayori end-glitch onlayer screens
        s "...Eh?"
        s "W-What's happening...?"
        call screen dialog("I won't let you hurt him.", ok_action=Return())
        s "Who..."
        s "I-It hurts--"
        show screen tear(20, 0.1, 0.1, 0, 40)
        window hide(None)
        play sound "sfx/s_kill_glitch1.ogg"
        hide sayori onlayer screens
        pause 0.35
        stop sound
        hide screen tear
        window show(None)
        s "Ah--"
        call screen dialog("I'm sorry... I was wrong.", ok_action=Return())
        call screen dialog("There's no happiness here after all...", ok_action=Return())
        call screen dialog("Goodbye, Sayori.", ok_action=Return())
        call screen dialog("Goodbye, [player].", ok_action=Return())
        call screen dialog("Goodbye, Literature Club.", ok_action=Return())
        $ gtext = glitchtext(120)
        s "[gtext]{nw}"
        show screen tear(20, 0.1, 0.1, 0, 40)
        window hide(None)
        play sound "sfx/s_kill_glitch1.ogg"
        pause 0.35
        stop sound
        hide screen tear
        scene black
        pause 3.0
        return

    label ch40_clearall:
        s "I wanted to thank you for spending so much time with us all."
        play music mend
        s 2d "You worked so hard to make each and every one of us happy."
        s "You comforted us through our hard times."
        s "And you helped us all get along with each other."
        s 1a "Do you get it, [player]?"
        s "Because I'm President now, I understand everything."
        s 1q "You really didn't want to miss a single thing in this game, did you?"
        s 1a "You saved and loaded so many times, just to make sure you could spend time with everyone."
        s "Only someone who truly cares about the Literature Club would go that far."
        s "But..."
        s 4d "All along, that's all I ever wanted."
        s "For everyone to be happy and care about each other."
        s 4q "Ahaha..."
        s 1t "It's kind of sad, you know?"
        s "After all you've done for us, there isn't much I can do for you in return."
        s "We've already reached the end of the game."
        s 1y "So..."
        s "This is where we say goodbye."
        s 1d "Thank you for playing {i}Doki Doki Literature Club{/i}."
        s "I'm going to miss you, [player]."
        s "Come visit sometime, okay?"
        s "We'll always be here for you."
        s 1t "We..."
        scene black with dissolve_cg
        s "We all love you."
        stop music fadeout 2.0
        scene black
        with Dissolve(2.0)
        return