image yuri half = "images/yuri/1l.png"
image yuri_half2:
    "images/yuri/1r.png"
    block:
        xoffset -360
        linear 0.2 xoffset -280
        repeat

label ch22_main:
    scene bg club_day2
    with dissolve_scene_half
    play music t6
    "Another day passes, and it's time for the club meeting already."
    "I've gotten a little more comfortable here over the past couple days."
    "Entering the clubroom, the usual scene greets me."
    if renpy.random.randint(0,2) == 0:
        show yuri half zorder 2 at i11
        show yuri_half2 zorder 1 at i11
    else:
        show yuri 1s zorder 2 at t11
    y "Welcome back, [player]..."
    hide yuri_half2
    mc "Ah, hi Yuri..."
    "I'm not sure if it's me, or if it's Yuri's expression..."
    "But the weight of yesterday's quarrel still hangs in the air a little."
    y 2v "U-Um..."
    "Yuri glances over her shoulder, looking around the room."
    "Natsuki is reading manga at a desk."
    "And surprisingly, Monika isn't here yet."
    "Suddenly, Yuri takes my arm and pulls me to the corner of the room."
    show bg closet
    show yuri 2t zorder 2 at t11
    with wipeleft
    y "About yesterday..."
    y "I..."
    y 2v "I really need to apologize."
    y "Nothing like that has ever happened before..."
    y 2t "And...something just came over me, I guess..."
    y "I wasn't acting mentally sound."
    y 2w "Please don't think we're usually like this!"
    y "Not just me, but Natsuki as well..."
    show yuri 2t
    mc "Yuri..."
    mc "I'm happy that you were considerate and apologized."
    mc "You don't have to worry too much."
    mc "Even though I've only been here a couple days, I could tell something was off yesterday..."
    mc "Maybe we were just a little extra sensitive because it was our first time sharing poems."
    mc "But whatever it was..."
    mc "It didn't make me think any less of you."
    mc "I had already decided that there's no way you can be a bad person."
    mc "And now that you're apologizing, I know you really didn't mean it."
    y 3t "A-Ah..."
    y "[player]..."
    y 3u "Don't say those kinds of things so frankly..."
    y "They make me a little too happy."
    y 1s "I'm really glad that you're such an understanding person..."
    y "And I'm really glad that you joined this club."
    y "Everything is a little bit brighter with you around, and--"
    y 1t "Ah--"
    y 4c "Sorry, what am I saying right now...?"
    y "I just--"
    show natsuki 2c zorder 3 at f33
    n "Hey, have you guys seen Monika?"
    show natsuki zorder 2 at t33
    show yuri 3n at h32
    y "Ah--!"
    mc "No, I haven't..."
    mc "I was also kind of wondering where she was."
    show natsuki zorder 3 at f33
    n 5g "Man..."
    n 5c "Yuri, I'm guessing you haven't, either?"
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 4a "..."
    "Yuri is clearly taken aback by how calmly Natsuki is addressing her."
    y "N-No, I haven't..."
    show yuri zorder 2 at t32
    show natsuki zorder 3 at f33
    n 1u "Jeez, this isn't like her at all."
    n "I know it's stupid, but I can't help but worry a little bit..."
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 2t "..."
    show yuri zorder 2 at t32
    show natsuki 1h zorder 3 at f33
    n "What?"
    n "Why're you looking at me like that?"
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y "U-Um..."
    y "Natsuki, about yesterday..."
    y 3w "I-I just wanted to apologize!"
    y "I promise I didn't mean any of the things I said!"
    y 3t "And I'll do my best to stay under control from now on..."
    y "So--"
    show yuri zorder 2 at t32
    show natsuki zorder 3 at f33
    n 2c "Yuri, what the heck are you talking about?"
    n "Did you do something yesterday?"
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 3f "...Eh?"
    show yuri zorder 2 at t32
    show natsuki zorder 3 at f33
    $ style.say_dialogue = style.normal
    n 2a "Jeez..."
    $ style.say_dialogue = style.edited
    n "Whatever's on your mind, I'm sure it was nothing."
    n "I don't even remember anything bad happening."
    n "You're the kind of person who worries too much about the little things, aren't you?"
    $ style.say_dialogue = style.normal
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 2o "..."
    y "B-But..."
    show yuri zorder 2 at t32
    if renpy.random.randint(0, 3) == 0:
        $ style.say_dialogue = style.edited
        show natsuki mouth as nm zorder 3 at i33
        show n_moving_mouth zorder 3:
            xoffset 400
        n 2a "mibulls sailcloth blindsight lifeline anan rectipetality faultlessly offered scleromalacia neighed catholicate"
        hide nm
        hide n_moving_mouth
        $ style.say_dialogue = style.normal
    show natsuki zorder 3 at f33
    n 2j "I'll accept your apology anyway, if it helps you feel better about it."
    n "Besides, it's kinda nice to hear, since I was always afraid you secretly hated me or something like that."
    n 2z "Ehehe."
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 3q "N-No, not at all...!"
    y "I don't hate you..."
    show yuri zorder 2 at t32
    show natsuki zorder 3 at f33
    n 2l "Ahaha."
    n "Well, you're kind of weird, but I don't hate you either."
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 3t "..."
    "Natsuki turns to me."
    show yuri zorder 2 at t32
    show natsuki zorder 3 at f33
    n 2a "You're still on trial, though."
    show natsuki zorder 2 at t33
    mc "Hey...!"
    "Suddenly, the door swings open."
    show monika 1g at l41
    m "Sorry! I'm super sorry!"
    mc "Ah, there you are..."
    show monika zorder 3 at f41
    m "I didn't mean to be late..."
    m "I hope you guys weren't worried or anything!"
    show monika zorder 2 at t41
    mc "Nah..."
    mc "Well, Natsuki was."
    show natsuki zorder 3 at f33
    n 1p "I-I was not!!"
    show natsuki zorder 2 at t33
    show monika zorder 3 at f41
    m 1k "Ahaha."
    show monika zorder 2 at t41
    show natsuki zorder 3 at f33
    n 1s "...What took you so long, anyway?"
    show natsuki zorder 2 at t33
    show monika zorder 3 at f41
    m 1e "Ah..."
    m "Well, my last period today was study hall."
    m "To be honest, I kind of just lost track of time..."
    m "Ahaha..."
    show monika zorder 2 at t41
    show natsuki zorder 3 at f33
    n 2c "That makes no sense, though."
    n "You would have heard the bell ring, at least."
    show natsuki zorder 2 at t33
    show monika zorder 3 at f41
    m 1m "I must not have heard it, since I was practicing piano..."
    show monika zorder 2 at t41
    show yuri zorder 3 at f32
    y 1e "Piano...?"
    y "I wasn't aware you played music as well, Monika."
    show yuri zorder 2 at t32
    show monika zorder 3 at f41
    m 1l "Ah, don't give me more credit than I deserve."
    m 1m "I guess I've been practicing for a while, but I'm still not really good yet."
    show monika zorder 2 at t41
    show yuri zorder 3 at f32
    y 1a "Still..."
    y "That must require a lot of dedication."
    y "So, I'm still impressed."
    show yuri zorder 2 at t32
    show monika zorder 3 at f41
    m 5 "Aw, well thanks, Yuri~"
    show monika zorder 2 at t41
    show natsuki zorder 3 at f33
    n 2d "You should play something for us sometime!"
    show natsuki zorder 2 at t33
    show monika zorder 3 at f41
    m "Ahaha, that's..."
    "Monika looks at me."
    m 1a "Well, I am working on writing a song, but it's not quite done yet..."
    m "Maybe once I get a little bit better, I will."
    show monika zorder 2 at t41
    mc "That sounds cool."
    mc "I look forward to it."
    show monika zorder 3 at f41
    m 1b "Is that so?"
    m "In that case..."
    m "I won't let you down, [player]."
    show yuri zorder 1 at thide
    show natsuki zorder 1 at thide
    hide yuri
    hide natsuki
    show monika 5 zorder 2 at t11
    "Monika smiles sweetly."
    mc "Ah..."
    mc "I didn't mean any pressure or anything like that!"
    m 1a "Ahaha, don't worry."
    m "I was hoping that I could share it with you, anyway."
    m "I guess that's why I've been practicing so much recently."
    mc "I see..."
    "I'm not sure if Monika was referring to the whole club, or just me..."
    mc "In that case, best of luck."
    m 1j "Thanks~!"
    m 1a "So, I didn't miss anything, did I?"
    mc "Not...not really."
    show monika zorder 1 at thide
    hide monika
    "I choose not to bring up anything that the three of us talked about."
    "Besides, Natsuki has already run off into the closet."
    show yuri 2q zorder 2 at t11
    y "[player]..."
    y "Um..."
    y "Since your compliments put me in a good mood..."
    y "I was wondering if you would like to spend some time together today."
    y 3o "I mean--in the club!"
    if poemwinner[0] == "natsuki":
        $ y_appeal = 1
        mc "Ah, I suppose so."
        mc "I don't think I could say no to you, after you gave that book to me."
        mc "Well, I guess I need to make sure Natsuki isn't waiting for me."
        mc "After we finished reading yesterday, she--"
        if n_appeal >= 2:
            y 3r "She's fine!"
            $ style.say_dialogue = style.normal
            y 3h "She's reading over there. See?"
            $ style.say_dialogue = style.edited
            y 3f "Don't think about her so much."
            y "She's used to being ignored."
            y "Come on, we're going over there."
            $ style.say_dialogue = style.normal
            window hide(None)
            $ currentpos = get_pos()
            stop music
            scene black
            window auto
            $ pause(2.0)
            play music "<from " + str(currentpos) + " loop 10.893>bgm/6.ogg"
            jump ch22_main2
        else:
            y 3r "S-She's fine!"
            y 3h "She's reading over there."
            y 3y6 "So it's okay, right?"
            mc "Ah--"
            mc "In that case, I don't see any problem..."
    else:
        $ y_appeal = 2
        mc "Yeah, definitely."
        mc "I planned on it anyway."
    show yuri zorder 2 at h11
    y 3y5 "Okay!"
    y "Can we start now?"
    y "Let's find a place to sit--"
    y 3n "A-Ah--"
    y "I'm being a little forceful, aren't I...?"
    y 4c "I'm sorry!"
    y "My heart...just won't stop pounding, for some reason..."
    mc "Don't worry about it."
    mc "If anything, it's nice to see you have so much energy."
    y 3q "Y-Yeah!"
    y "But..."
    y 3j "I need to try to calm down."
    y "I won't be able to focus on reading like this..."
    mc "Take your time."
    "Yuri takes a deep breath, then pulls a copy of the book out of her bag."
label ch22_main2:
    if n_poemappeal[1] == 1:
        $ n_poemappeal[1] = 0
    $ poemwinner[1] = "yuri"


    scene bg club_day2
    show yuri 3a at i11
    with wipeleft
    $ nextscene = "yuri_exclusive2_" + str(eval("y_appeal")) + "_ch22"
    call expression nextscene

    return

label ch22_end:
    stop music fadeout 1.0
    scene black
    with wipeleft_scene
    call screen confirm("You have unlocked a special poem.\nWould you like to read it?", Return(True), Return(False))
    if _return:
        call expression "poem_special_" + str(persistent.special_poems[1])
        scene black with Dissolve(1.0)
    else:
        pass
    if not faint_effect and renpy.random.randint(0,2) == 0:
        $ faint_effect = True
    else:
        $ faint_effect = None
    scene bg club_day2
    show monika 4b zorder 2 at t32
    if faint_effect:
        show layer master at dizzy(0.5, 1.0)
        show layer screens at dizzy(0.5, 1.0)
        show expression Solid("ff0000") as i1 onlayer front:
            additive 1.0
        show expression Solid("#440000") as i2 onlayer front:
            additive 0.4
        show veins onlayer front:
            additive 0.5
    with wipeleft_scene
    if faint_effect:
        play music t3g3
    else:
        play music t3
    if renpy.random.randint(0,2) == 0:
        $ config.mouse = {"default": [
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head.png", 0, 0),
                                    ("gui/mouse/s_head.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head2.png", 0, 0),
                                    ("gui/mouse/s_head.png", 0, 0),
                                    ]}



    m "Okay, everyone!"
    m "We're all done reading each other's poems, right?"
    $ config.mouse = None
    m "We have something we need to go over today, so if everyone could come sit at the front of the room..."
    show natsuki 3c zorder 3 at f31
    n "Is this about the festival?"
    show natsuki zorder 2 at t31
    show monika 1j zorder 3 at f32
    m "Well, sort of~"
    show monika 1a zorder 2 at t32
    show natsuki 1m zorder 3 at f31
    n "Ugh. Do we really have to do something for the festival?"
    n "It's not like we can put together anything good in just a few days."
    n "We'll just end up embarrassing ourselves instead of getting any new members."
    if faint_effect:
        $ currentpos = get_pos() + 2.0
        stop music fadeout 2.0
        show black onlayer front:
            alpha 0.0
            linear 2.0 alpha 1.0
    show natsuki zorder 2 at t31
    show yuri 2g zorder 3 at f33
    y "That's a concern of mine as well."
    if faint_effect:
        hide black onlayer front
        hide veins onlayer front
        hide i1 onlayer front
        hide i2 onlayer front
        show layer master
        show layer screens
        play music "<from " + str(currentpos) + " loop 4.618>bgm/3.ogg"
    y "I don't really do well with last-minute preparations..."
    show yuri zorder 2 at t33
    show monika zorder 3 at f32
    m 1b "Don't worry so much!"
    m "We're going to keep it simple, okay?"
    m 2a "Look..."
    m 2m "I know everyone's been a little more...lively...ever since [player] joined and we've started with some club activities."
    m 2d "But this isn't the time for us to become complacent."
    m "We still only have four members..."
    m 2a "And the festival is our only real chance to find more, you know?"
    show monika zorder 2 at t32
    show natsuki zorder 3 at f31
    n 5g "What's so great about getting new members, anyway?"
    n "We already have enough to be considered an official club."
    n "More members will just mean everything gets noisier and more difficult to manage."
    show natsuki zorder 2 at t31
    show monika zorder 3 at f32
    m 1g "Natsuki..."
    m "I don't think you're looking at it the right way at all."
    m "Don't you want to share your passion with as many people as you can?"
    m 3e "To inspire them to find the same feelings that brought you here in the first place?"
    m "The Literature Club should be a place where people can express themselves like they can't do anywhere else."
    m "It should be a place so intimate that you never want to leave."
    m 2e "I know you feel that way, too."
    m 2b "I know we all do!"
    m "So that's why we should work hard and put something together for the festival...even if it's something small!"
    m "Right, [player]?"
    show monika 2a zorder 2 at t32
    mc "Ah..."
    show natsuki zorder 3 at f31
    n 42c "Oh, come on!"
    n "You can't take advantage of [player] to agree with you just because he doesn't know how to say no to anything."
    stop music fadeout 1
    n 1c "Look, Monika."
    n "Do you really think any of us here joined the club with other people in mind?"
    n "Yuri never even talked until [player] joined."
    n 2b "As for me, I just like it better here than I do at home."
    n "And [player] isn't even passionate about literature in the first place."
    n "And that's everyone."
    n 4w "Sorry, but you're really the only one who's so interested in finding new members."
    n "The rest of us are fine like this."
    n 4q "I know you're President and all, but you should really consider our opinions for once."
    show natsuki zorder 2 at t31
    show monika zorder 3 at f32
    m 1g "..."
    "Monika is clearly taken aback by Natsuki's words."
    play music t9
    m 1m "That's...not true at all."
    m 2m "I'm sure Yuri and [player] want to get more members too..."
    m 2p "...Right?"
    show monika zorder 2 at t32
    show yuri zorder 3 at f33
    y 4b "..."
    show yuri zorder 2 at t33
    mc "..."
    "I don't know about Yuri, but I'm kind of indifferent."
    "If I showed as much enthusiasm as Monika wanted, then I would probably be lying."
    "Still, if it's up to me to rescue this situation..."
    mc "Um--"
    show monika zorder 3 at f32
    m 1i "No."
    m "Natsuki's right, isn't she?"
    m 1g "This club..."
    m "It's nothing more than a place for a few people to hang out."
    m 1r "Why did I think that everyone here saw it the same way as I did?"
    show monika zorder 2 at t32
    mc "But that doesn't mean that we're against getting new members or anything..."
    show monika zorder 3 at f32
    m 1i "[player], why did you even join this club?"
    m "What were you hoping to get out of it?"
    show monika zorder 2 at t32
    mc "Well--"
    "That's not really something I can be honest about, is it?"
    show monika zorder 3 at f32
    m 1p "In fact..."
    m "If I remember, you weren't even given a choice not to join."
    show monika zorder 1 at thide
    hide monika
    "Monika sits down and stares at her desk."
    m "What's the point of all this, anyway?"
    m "What if starting this club was a mistake?"
    mc "..."
    show yuri zorder 3 at f33
    y 2g "Now you've done it, Natsuki..."
    show yuri zorder 2 at t33
    show natsuki zorder 3 at f31
    n 1p "What, me?"
    n 1s "I just spoke my mind..."
    n "Is it a crime to be honest?"
    show natsuki zorder 2 at t31
    show yuri zorder 3 at f33
    y 2l "It's not about being honest."
    y "It's about word choice."
    y 2h "Besides, you have no right to speak for everyone else in the club like that..."
    show yuri zorder 2 at t33
    show natsuki zorder 3 at f31
    n 1e "You don't understand at all!"
    n 5s "I just..."
    n "I just want a place that feels nice to hang out with a few friends."
    n 5u "Is there a problem with the club being that for me?"
    n "There aren't...there aren't many other places like that for me..."
    n 5x "And now Monika wants to take it away from me!"
    show natsuki zorder 2 at t31
    mc "She's not taking anything away--"
    show natsuki zorder 3 at f31
    n 1g "No, [player]."
    n "It's not the same."
    n 1q "It won't be the same with the direction she wants to take it."
    n "If I wanted that, then I could have just joined any other stupid club."
    n 12d "But this one..."
    n "I mean..."
    n 12e "At least for a little bit of time..."
    n "Things were nice."
    "Natsuki starts packing up her things."
    n 12d "I'm going home."
    n "I feel like...I don't belong here right now."
    show natsuki zorder 2 at t31
    show yuri zorder 3 at f33
    y 3t "Natsuki..."
    show natsuki zorder 1 at thide
    hide natsuki
    "Natsuki ignores Yuri and walks right out of the classroom."
    show yuri zorder 2 at t11
    y 3v "..."
    y "This is bad..."
    y "I don't know what to do..."
    mc "Well..."
    mc "Do you have an opinion on the festival?"
    y 4b "I-I don't know..."
    $ style.say_dialogue = style.normal
    y "I'm kind of indifferent, I guess..."
    show black zorder 3
    show y_glitch_head zorder 3:
        xpos 630 ypos -50 zoom 2.0
    $ style.say_dialogue = style.edited
    $ currentpos = get_pos() / 2.07
    play music "<from " + str(currentpos) + " loop 1.532>bgm/9g.ogg"
    y "Who cares about that obnoxious brat?"
    $ style.say_dialogue = style.normal
    $ currentpos = get_pos() * 2.07
    play music "<from " + str(currentpos) + " loop 3.172>bgm/9.ogg"
    hide black
    hide y_glitch_head
    y "I mean, I like how nice and quiet the club is right now..."
    y "And I'm just...happy with you here..."
    y 2t "But still!"
    y "I'm the Vice President..."
    y "It's not right for me to ignore my responsibilities like that..."
    show black zorder 3
    show y_glitch_head zorder 3:
        xpos 430 ypos -450 zoom 4.5
    $ style.say_dialogue = style.edited
    $ currentpos = get_pos() / 2.07
    play music "<from " + str(currentpos) + " loop 1.532>bgm/9g.ogg"
    y "Nobody would cry if she killed herself."
    $ style.say_dialogue = style.normal
    $ currentpos = get_pos() * 2.07
    stop music
    $ pause(0.5)
    play sound "sfx/stab.ogg"
    show blood_eye zorder 3:
        pos (710,380) zoom 2.5
    $ pause(0.75)
    stop sound
    play music "<from " + str(currentpos) + " loop 3.172>bgm/9.ogg"
    hide black
    hide y_glitch_head
    hide blood_eye
    y 2l "I should do my best to consider everyone's perspective and make the decision that's right for the club."
    y 1t "But what about you, [player]?"
    y "What do you want to get out of this club?"
    "Yuri repeats the same question as Monika."
    "I decide giving an indirect answer is better than nothing."
    mc "...I think the most important thing is for everyone to get along..."
    mc "...And for the club to provide something that you can't get anywhere else."
    mc "I don't think it's about how many members, but rather the quality of each member."
    mc "That's what will end up making the Literature Club a special place."
    y 1u "I see..."
    y "I really agree with you."
    show blood_eye2 zorder 3:
        pos (568, 165)
    y 1f "Each member contributes their own qualities in a special way."
    y "With each change in members, the identity of the club as a whole will change, too."
    y 1h "I don't think that's necessarily a bad thing."
    y "Stepping out of your comfort zone once in a while..."
    y 1a "So if you would like to help Monika with the festival, then I'm on your side as well."
    hide blood_eye2
    mc "Alright."
    mc "Well, maybe we can all talk to Natsuki tomorrow..."
    "Yuri nods."
    show monika 1g zorder 3 at f21
    show yuri zorder 2 at t22
    m "Hey, Yuri..."
    show monika zorder 2 at t21
    show yuri zorder 3 at f22
    y 1t "Eh?"
    show yuri zorder 2 at t22
    show monika zorder 3 at f21
    m 1p "Um, I know things were a little awkward yesterday..."
    m "But I feel like you deserve to know that I still think you're a wonderful vice president."
    m 1e "And also, a wonderful friend."
    show monika zorder 2 at t21
    show yuri zorder 3 at f22
    y 3s "M-Monika..."
    show yuri zorder 2 at t22
    show monika zorder 3 at f21
    m 2e "I want to do everything I can to make this the best club ever."
    m "Okay?"
    show monika zorder 2 at t21
    show yuri zorder 3 at f22
    y "...Me too."
    show yuri zorder 2 at t22
    show monika zorder 3 at f21
    m 1a "Yeah..."
    m "Let's all go home for today."
    m "We'll talk about the festival tomorrow."
    show monika zorder 2 at t21
    show yuri zorder 3 at f22
    y 1m "Okay."
    y "I look forward to it."
    y 1a "Shall we go, [player]?"
    show yuri zorder 2 at t22
    show monika zorder 3 at f21
    m 1d "Um--"
    m 1p "Please don't take this the wrong way, but..."
    m "I'm going to chat a little bit with [player] before we leave."
    m 1d "Just to see what he thinks of his time here and all that..."
    m "It's important to me, as President."
    show monika zorder 2 at t21
    show yuri zorder 3 at f22
    y 2v "..."
    "Yuri looks a little troubled, but she doesn't protest."
    y 2t "Okay."
    y 2s "I trust your judgment, Monika."
    y "In that case, I'll see the two of you tomorrow."
    show yuri zorder 2 at t22
    show monika zorder 3 at f21
    m 1j "See you tomorrow~"
    show yuri zorder 1 at thide
    hide yuri
    "Monika waves as Yuri exits the classroom."

    show monika 2a zorder 2 at t11
    m "Phew..."
    m 2e "Things have been a bit hectic lately, haven't they?"
    show darkred:
        additive 0.2
        alpha 0
        linear 20 alpha 1.0
    show noise:
        alpha 0
        linear 20 alpha 0.1
    m "[player], I just wanted to make sure you're enjoying your time at this club."
    m "I would really hate to see you unhappy."
    m 2m "I feel kind of like I'm responsible for that, as President..."
    stop music
    m 4e "And I really do care about you...you know?"
    m "I don't like seeing the other girls give you a hard time."
    m 4r "With how mean Natsuki is and everything..."
    m 4m "And Yuri being a little bit...you know."
    m 5a "Ahaha..."
    m "Sometimes it feels like you and I are the only real people here."
    m "You know what I mean?"
    m 1g "But it's weird, because in all the time you've been here, we've hardly gotten to spend any time together."
    m 1n "Ah...I mean..."
    m "I guess it's technically only been a couple days..."
    m 1l "Sorry, I didn't mean to say something weird!"
    m 1e "There are just some things I've been hoping to talk about with you..."
    m "Things I know only you could understand."
    stop music fadeout 3.0
    show black onlayer front:
        alpha 0.0
        0.25
        linear 3.0 alpha 1.00
    m "So that's why--\"{space=5000}{w=0.75}{nw}"
    m 1g "Wait, not yet!\"{space=5000}{w=0.5}{nw}"
    m "No!\"{space=5000}{w=0.5}{nw}"
    m "Stop it!\"{space=5000}{w=1.0}{nw}"
    window hide(None)
    window auto
    hide black onlayer front





    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
