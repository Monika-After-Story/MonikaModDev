label yuri_exclusive2_1:
    scene bg club_day
    with wipeleft_scene
    "I'm really curious to talk to Yuri a little bit more..."
    "But at the same time, I would feel bad for distracting her from reading."
    "I catch a glimpse of the cover of her book."
    "It looks like the same book that she lent to me..."
    "More than that, she seems to be on the first few pages."
    play music t6 fadeout 1.0
    show yuri 4a at t11 zorder 2
    y "Ah..."
    "Crap--"
    "I think she noticed me looking at her..."
    "She sneaks another glance at me, and our eyes meet for a split second."
    y 4b "..."
    "But that only makes her hide her face deeper in her book."
    mc "Sorry..."
    mc "I was just spacing out..."
    "I mutter this, sensing I made her uncomfortable."
    y oneeye "Oh..."
    y "It's fine..."
    y "If I was focused, then I probably wouldn't have noticed in the first place."
    y "But I'm just re-reading a bit of this, so..."
    mc "That's the book that you gave me, right?"
    y "Mhm."
    y "I wanted to re-read some of it."
    y 2q "Not for any particular reason...!"
    mc "Just curious, how come you have two copies of the same book?"
    y "Ah..."
    y "Well, when I stopped at the bookstore yesterday--"
    y 3o "Ah, that's not what I meant..."
    y "I mean--"
    y 1w "I...just happened to buy two of them."
    mc "Ah, I see."
    "There's something fairly obvious here that Yuri isn't telling me, but I decide to let it go."
    mc "I'll definitely start reading it soon!"
    y 2u "I'm glad to hear..."
    y "Once it starts to pick up, you might have a hard time putting it down."
    y 2c "It's a very engaging and relatable story."
    mc "Is that so...?"
label yuri_exclusive2_1_ch22:
    mc "What's the story about, anyway?"
    y 1f "Well..."
    y "Mmm..."
    "I look at the cover of the book."
    "The book is titled \"Portrait of Markov\"."
    "There's an ominous-looking eye symbol on the front cover."
    y 1a "Basically, it's about this religious camp that was turned into a human experiment prison..."
    y "And the people trapped there have this trait that turns them into killing machines that lust for blood."
    y 1m "But the facility gets even worse, and they start selectively breeding people by cutting off their limbs and affixing them to--"
    y 1q "O-Oh, that might be a little bit of a spoiler..."
    y 3q "But anyway, I-I'm really into it!"
    y 3n "...The book, I mean!"
    y 3q "N-Not the thing about the limbs..."
    mc "That's kind of--!"
    "That's kind of dark, isn't it?"
    "Yuri made it sound like it was going to be a nice story, so that dark turn came from nowhere."
    y 1s "Ah..."
    y "Are you not a fan of that sort of thing, [player]?"
    mc "No, it's not that..."
    mc "I mean, I can definitely enjoy those kinds of stories, so don't worry."
    y 2u "I hope so..."
    "Yeah... I totally forgot that Yuri is into those things."
    "She's so shy and reclusive on the outside, but her mind seems to be completely different."
    y "It's just that this kind of story..."
    y 1a "It's the kind that challenges you to look at life from a strange new perspective."
    $ style.say_dialogue = style.normal
    y "When horrible things happen not just because someone wants to be evil..."
    $ style.say_dialogue = style.edited
    y "But because the world is full of horrible people, and we're all worthless anyway."
    y "Then, suddenlyyyyyyyyyyyyyyyyyyyyyy yyyyyyyyyyyyyyyyyyyy{nw}"
    $ style.say_dialogue = style.normal
    y 3v "I'm...I'm rambling, aren't I...?"
    y "Not again..."
    y 4b "I'm sorry..."
    mc "Hey, don't apologize...!"
    mc "I haven't lost interest or anything."
    y "Well..."
    y "I guess it's alright, then..."
    y 4a "But I feel like I should let you know that I have this problem..."
    $ style.say_dialogue = style.normal
    y "When I let things like books and writing fill my thoughts..."
    $ gtext = glitchtext(24)
    $ style.say_dialogue = style.edited
    y "my whole body gets incredibly [gtext]{nw}"
    $ style.say_dialogue = style.normal
    $ _history_list.pop()
    y "I kind of forget to pay attention to other people..."
    y 3t "So I'm sorry if I end up saying something strange!"
    y "And please stop me if I start talking too much!"
    mc "That's--"
    mc "I really don't think you need to worry..."
    mc "That just means you're passionate about reading."
    mc "The least I can do is listen."
    mc "It's a literature club, after all..."
    y 4a "Ah--"
    y "That's..."
    y "Well, that's true..."
    mc "In fact..."
    mc "I might as well get started reading it, right?"
    play sound "sfx/glitch3.ogg"
    y dragon "Y-Yes!"
    y 3n "I-I mean, you don't have to, but...!"
    mc "Ahaha, what are you saying?"
    y 3o "..."
    mc "Let me just get the book..."
    "I quickly retrieve the book that I had put into my bag."
    mc "Alright...it's fine if I sit here, right?"
    "I slip into the seat next to Yuri's."
    y 3n "Ah...!"
    y "Yeah..."
    mc "Are you sure?"
    mc "You seem a little apprehensive..."
    y "That's..."
    y 4b "I'm sorry..."
    y "It's not that I don't want you to!"
    y "It's just something I'm not very used to..."
    y "That is, reading in company with someone."
    mc "I see..."
    mc "Well, just tell me if I end up distracting you or anything."
    y "A-Alright..."
    show yuri at thide zorder 1
    hide yuri
    "I open the book and start the prologue."
    "I soon understand what Yuri means about reading in company."
    "It's as if I can feel her presence over my shoulder as I read."
    "It's not a particularly bad thing."
    "Maybe a little distracting, but the feeling is somewhat comforting."
    "Yuri is in the corner of my eye."
    "I realize that she's not actually looking at her own book."
    "I glance over."
    "It looks like she's reading from my book instead--"
    show yuri 3n at t11 zorder 2
    y "S-Sorry!"
    $ style.say_dialogue = style.normal
    y "I was just--!{nw}"
    $ style.say_dialogue = style.edited
    y "I was just{fast} bathing in the feeling of your body heat tttttttttttttheat eattttttt{nw}"
    $ style.say_dialogue = style.normal
    $ _history_list.pop()

    mc "Yuri, you really apologize a lot, don't you?"
    y "I...I do?"
    y 4a "I don't really mean to..."
    y "Sorry..."
    y 4c "I mean--!"
    mc "Ahaha."
    mc "Here, this should work, right?"
    "I slide my desk until it's up against Yuri's, then hold my book more between the two of them."
    y 2v "Ah..."
    y "I-I suppose so..."
    "Yuri timidly closes her own copy."
    "Once we each lean in a little bit, our shoulders are almost touching."
    "It feels like my left arm is in the way, so instead I use my right hand to hold the book open."
    mc "Ah, I guess that makes it kind of difficult to turn the page..."
    y "Here..."
    $ persistent.clear[2] = True
    scene y_cg1_base with dissolve_cg
    "Yuri takes her left arm and holds the left side of the book between her thumb and forefinger."
    mc "Ah..."
    "I do the same with my right arm, on the right side of the book."
    "That way, I turn a page, and Yuri slides it under her thumb after it flips to her side."
    "But in holding it like this..."
    "We're huddled even closer together than before."
    "It's actually kind of distracting me...!"
    "It's as if I can feel the warmth of Yuri's face, and she's in the corner of my vision..."
    show y_cg1_exp1 at cgfade
    y "...Are you ready?"
    mc "Eh?"
    y "To turn the page..."
    mc "Ah...sorry!"
    mc "I think I got a bit distracted for a second..."
    "I glance over at Yuri's face again, and our eyes meet."
    "I don't know how I'll be able to keep up with her..."
    y "Ah..."
    show y_cg1_exp2 at cgfade
    y "That's okay."
    y "You're not as used to reading, right?"
    y "I don't mind being patient if it takes you a bit longer..."
    y "It's probably the least I can do..."
    y "Since you've been so patient with me..."
    mc "Y-Yeah..."
    mc "Thanks."
    hide y_cg1_exp1
    hide y_cg1_exp2
    "We continue reading."
    "Yuri no longer asks me if I'm ready to turn the page."
    "Instead, I just assume that she finishes the page before me, so I turn it by my own volition."
    "We continue the first chapter in silence."
    "Even so, turning each page almost feels like an intimate exchange..."
    "My thumb gently letting go of the page, letting it flutter over to her side as she catches it under her own thumb."
    mc "Hey, Yuri..."
    mc "This might be a silly thought, but..."
    mc "The main character kind of reminds me of you a little bit."
    show y_cg1_exp3 at cgfade
    y "E-Eh??"
    y "N-No, I don't relate to this character at all!"
    y "Definitely not!"
    mc "Really...?"
    mc "I was just thinking the way she second-guesses things she says, and all that..."
    show y_cg1_exp1 at cgfade
    y "A-Ah..."
    y "That's what you were talking about..."
    hide y_cg1_exp3
    hide y_cg1_exp1
    show y_cg1_exp2 at cgfade
    y "Sorry..."
    y "I thought you meant...something else about her."
    mc "Something else...?"
    hide y_cg1_exp2
    show y_cg1_exp3 at cgfade
    y "N-Never mind!"
    y "We didn't even get that far yet..."
    y "So I don't know why that came into my head..."
    y "Ahaha!"
    mc "Yuri, are you feeling alright?"
    hide y_cg1_exp3
    show y_cg1_exp1 at cgfade
    y "Eh--?"
    "Yuri's been a little fidgety ever since we started reading..."
    mc "You can rest if you're feeling sick or something."
    mc "Your breathing is a little..."
    y "My breathing...?"
    hide y_cg1_exp1
    "Yuri puts her hands on her chest, as if to feel her heartbeat."
    y "I-I didn't...even notice..."
    show y_cg1_exp3 at cgfade
    y "...Anyway, I'm fine!"
    y "I just need some water...!"
    mc "Alright...don't push yourself."
    scene bg club_day
    with dissolve_cg
    "Yuri stands up and practically rushes out of the classroom."
    mc "What on Earth was that about...?"
    show monika 1d at t11 zorder 2
    m "[player]?"
    m "Did something happen just now?"
    mc "Eh?"
    mc "I have no idea..."
    mc "Yuri was acting a little strange, I guess..."
    m 1r "So you don't know anything..."
    mc "Sorry, I can't say I do."
    mc "Are you worried about her?"
    m 1a "Oh...no, not really."
    m "I was just making sure that you didn't do anything to her."
    mc "N-No, nothing!"
    m 5 "Ahaha, don't worry...I believe you, silly."
    m "Yuri just does this sometimes, so it's nothing alarming."
    mc "Alright...if you say so."
    m 2b "Anyway, why don't we start with sharing our poems with each other?"
    mc "Eh?"
    mc "Shouldn't we wait for Yuri?"
    m 2a "Well, she might be a while, so I just figured we'd get started without her."
    m "Is that okay?"
    mc "Yeah, I was just asking..."
    "I stand up."
    "I make a mental note of where I left off in the book, then slip it back into my bag."
    $ y_ranaway = True
    return

label yuri_exclusive2_2:
    $ y_exclusivewatched = True
    play music t6 fadeout 1.0
    scene bg club_day
    with wipeleft_scene
    mc "Hey, Yuri."
    show yuri 2f at t11 zorder 2
    y "Eh?"
    mc "Ah..."
    "I suddenly notice that Yuri is reading a different book from the one we've been reading together."
    mc "Sorry! I didn't mean to interrupt..."
    y 2m "Ah, no..."
    y "I was kind of just waiting for you..."
    show yuri 2a
    mc "Ah, if that's the case..."
    mc "Why don't we go ahead and get started?"
    y 2c "Yes, let's!"
label yuri_exclusive2_2_ch22:
    y 3a "Actually, I have a request..."
    y "...Do you mind if I make some tea first?"
    mc "Not at all."
    y 1c "Thanks very much."
    y 1a "If there's one thing that can make my reading time here any better, it's a nice cup of tea."
    y "Not to mention for yourself, as well."
    show yuri at thide zorder 1
    hide yuri
    "Yuri stands up and makes her way to the closet."
    "I follow and watch as she retrieves a small water pitcher from the shelf - the kind with a filter inside."
    show yuri 1f at t11 zorder 2
    y "Can you hold this for a second?"
    mc "Sure..."
    "Yuri hands me the water pitcher and also fetches an electric kettle."
    y "I'm going to plug this in at the teacher's desk, and then I'll go get some water."
    show yuri at thide zorder 1
    hide yuri
    "She walks past me and sets the kettle down on the teacher's desk."
    "I simply watch her movements."
    "To my surprise, the way she moves really contrasts her speaking mannerisms."
    "Especially because of her long legs, Yuri appears elegant and methodical."
    show yuri 1f at t11 zorder 2
    y "Okay, may I have the water pitcher?"
    y 1a "Thanks. I'll be right back."
    mc "Ah, I might as well walk with you..."
    y 1q "T-That's okay!"
    y "You stay here..."
    y "It won't take long."
    show yuri at thide zorder 1
    hide yuri
    "Pitcher in hand, Yuri hurries out of the classroom."
    show monika 2i at t11 zorder 2
    m "Ah..."
    m "Did Yuri leave you again?"
    mc "No, it's not like that this time."
    mc "She's just filling up the water pitcher to make tea."
    m 5 "Oh, okay!"
    m "Sorry for misunderstanding~"

    scene bg club_day
    with wipeleft_scene

    "..."
    "Ten minutes pass."
    "Yuri said it wouldn't take long..."
    "Is something holding her up?"
    "I'm bored just waiting here, so I decide to go look for her."
    scene bg corridor
    with wipeleft_scene
    $ currentpos = get_pos()
    play music "<from " + str(currentpos) + " loop 10.893>bgm/6o.ogg"
    mc "Let's see..."
    "The most logical place for Yuri to be would be the nearest water fountain..."
    $ y_name = "Yuri"
    "I start heading down the hallway."
    $ y_name = "???"
    y "Haah.....haah...."
    y "....Haah.....haah...."
    "...What's that noise?"
    "It's coming from around the corner..."
    "It sounds like breathing."
    y "Khhhhh--"
    "A sharp inhale, like someone is sucking the air through their teeth."
    "Are they in pain...?"
    "I reach the corner and peer around it."
    mc "Yuri...?"
    $ y_name = "Yuri"
    show yuri cuts at t11 zorder 2
    y "Kya--!"

    $ currentpos = 45.264 - (get_pos() / 2.0)
    $ audio.t6r = "<from " + str(currentpos) + " to 39.817 loop 0>bgm/6r.ogg"
    play music t6r
    show yuri at thide zorder 1
    hide yuri
    show noise at noise_alpha zorder 100
    show vignette at vignetteflicker(-2.030) zorder 100
    show layer master at rewind
    $ y_name = "???"
    mc "{cps=*3}Yuri...?{/cps}{nw}"
    "{cps=*3}I reach the corner and peer around it.{/cps}{nw}"
    "{cps=*3}Are they in pain...?{/cps}{nw}"
    "{cps=*3}A sharp inhale, like someone is sucking the air through their teeth.{/cps}{nw}"
    y "{cps=*3}Khhhhh--{/cps}{nw}"
    "{cps=*3}It sounds like breathing.{/cps}{nw}"
    "{cps=*3}It's coming from around the corner...{/cps}{nw}"
    "{cps=*3}...What's that noise?{/cps}{nw}"
    y "{cps=*3}....Haah.....haah....{/cps}{nw}"
    y "{cps=*3}Haah.....haah....{/cps}{nw}"
    $ y_name = "Yuri"
    "{cps=*3}I start heading down the hallway.{/cps}{nw}"
    "{cps=*3}The most logical place for Yuri to be would be the nearest water fountain...{/cps}{nw}"
    mc "{cps=*3}Let's see...{/cps}{nw}"
    window hide(None)
    window auto
    scene bg club_day
    show noise at noise_alpha zorder 100
    show vignette at vignetteflicker(-2.030) zorder 100
    show layer master at rewind
    "{cps=*3}I'm bored just waiting here, so I decide to go look for her.{/cps}{nw}"
    "{cps=*3}Is something holding her up?{/cps}{nw}"
    "{cps=*3}Yuri said it wouldn't take long...{/cps}{nw}"
    "{cps=*3}Ten minutes pass.{/cps}{nw}"
    "{cps=*3}...{/cps}{nw}"

    $ del _history_list[-37:]
    if poemwinner[0] == "yuri" and chapter == 3:
        jump yuri_exclusive2_2_ch23
    $ currentpos = 90.528 - (get_pos() * 2.0)
    $ audio.t6r = "<from " + str(currentpos) + " loop 10.893>bgm/6.ogg"
    play music t6r
    hide noise
    hide vignette
    show layer master
    show yuri 1a at t11 zorder 2
    y "I'm back."
    y "Thanks for waiting patiently."
    y "[player], do you like oolong tea?"
    mc "Ah, yeah."
    mc "Anything is fine."
    y "Very well."
    "Yuri sets the temperature on the kettle to 200 degrees."
    y 1f "Now it's time to get the teapot."
    mc "You really do this properly, don't you?"
    y 1u "Of course..."
    y "I shouldn't do any less when I'm making tea for others."
    mc "Even if I'm not an expert on tea or anything...?"
    y 2m "Huhu."
    y 2a "In that case, you'll only be even more impressed."
    mc "Ah...perhaps I will!"
    show yuri at thide zorder 1
    hide yuri
    "Yuri fetches the teapot and begins measuring the tea leaves."
    "To my surprise, she even starts humming a little to herself."
    show yuri 1c at t11 zorder 2
    mc "You must be in a good mood now..."
    y 1a "Is that so?"
    y "I was letting it show..."
    y "And you noticed."
    y 2u "I was doing a bit of thinking..."
    y "And I decided that I would try expressing myself a little bit more."
    y "It turns out it's not very hard for me to do..."
    y 1c "When it's you who's around, anyway."
    show yuri 1a
    mc "Ah..."
    mc "That's great, Yuri!"
    mc "Just don't push yourself too much."
    y 3u "You're always worrying about me, [player]..."
    y "It's very endearing."
    mc "That's..."
    "Yuri wasn't kidding..."
    "I don't even know if I can keep up with this...!"
    "I watch Yuri pour a cup of tea for each of us."
    y 1a "[player], I have another request."
    y "Do you mind if we sit on the floor today?"
    mc "Eh? Why's that?"
    y 1h "It's a little bit easier on my back..."
    y "I can read with my back against the wall rather than bending over at my desk."
    mc "Ah, sorry, I didn't realize."
    y 1a "No worries."
    y "I just have back pain fairly regularly, so I do my best to manage it."
    mc "Is that so?"
    mc "I wonder why that is..."
    y 1f "It's most likely because my--"
    y 1n "Ah--"
    y 1o "M-My..."
    mc "Your posture, right?"
    mc "Always hunched over like that while reading..."
    y 2p "Yes!"
    y 2q "I have terrible reading posture!"
    y "So that's why we should sit on the floor."
    mc "Fair enough."
    mc "I'll go ahead and get the book."
    show yuri at thide zorder 1
    hide yuri
    "I retrieve the book from my bag."
    mc "Ah, I have some chocolate as well..."
    "It's a bag of small chocolate candies."
    "I take it, since it'll go well with the tea."
    "Yuri and I then sit against the wall, teacups at our sides."
    "As if in sync, we assume the same reading position as last time, each holding one half of the book."
    "Except this time..."
    "Our bodies are even closer to each other."
    show yuri 2h at t11 zorder 2
    y "I can't see too well..."
    mc "--!"
    show yuri 2e at d11
    "Yuri slides closer until our shoulders are touching."
    "How am I supposed to focus on reading like this...?!"
    "Yuri was always kind of cute, but..."
    "When she's being less apprehensive, it's almost more than I can handle!"
    y 2f "Your teacup..."
    "Yuri hands me my teacup."
    "Holding it with my hand that's not holding the book, I end up in a position that makes it even harder to focus."
    "Because now I need to worry about making sure I don't accidentally touch her chest...!"
    "Meanwhile, Yuri hasn't noticed a single thing."
    "She wears her intense reading expression, and I can only presume the world around her has faded away."
    "I use all of my willpower to focus on reading."
    "..."
    "After a few minutes, I finally manage to relax a little."
    "I put the teacup between my legs and fumble with the chocolate wrapper."
    mc "Ah, sorry..."
    "I briefly let go of the book to finish opening the wrapper."
    mc "You can have as much as you want."
    y 2s "Ah, that's..."
    y "That's okay, I won't take any..."
    mc "Eh? Are you sure?"
    y 2v "Well..."
    y "If I touch it, then it might get smudges on the pages..."
    mc "Ah, you're right..."
    mc "I didn't even think about that."
    mc "My bad..."
    y 2a "No need to apologize."
    y "I'll hold the book, okay?"
    mc "Are you sure...?"
    y "Of course."
    $ persistent.clear[3] = True
    scene y_cg2_bg
    show y_cg2_base
    show y_cg2_details
    show y_cg2_nochoc
    show y_cg2_dust1
    show y_cg2_dust2
    show y_cg2_dust3
    show y_cg2_dust4
    with dissolve_cg
    "Yuri opens the book with both hands."
    "She holds it so that I don't have any harder of a time reading from it."
    "But as a result, her left arm is practically resting on top of my leg."
    mc "Well, in that case..."
    "Yuri is already totally focused on reading again."
    "I take a chocolate candy and pop it into my mouth."
    "Then, I take another chocolate..."
    "And I hold it up to Yuri."
    "She doesn't even look away from the book."
    "She simply parts her lips, as if this situation was completely natural."
    "But that means I can't stop here!"
    hide y_cg2_nochoc
    "I apprehensively place the chocolate in her mouth."
    "Just like that, Yuri closes her lips over it."
    y "Eh...?"
    show y_cg2_exp2
    "Yuri's expression suddenly breaks."
    y "Did..."
    y "Did I just..."
    "Yuri looks at me like she needs to confirm what just happened."
    show y_cg2_exp3
    show y_cg2_nochoc:
        alpha 0
        linear 0.5 alpha 1
    hide y_cg2_exp2
    y "U-Um..."
    y "[player]..."
    mc "S-Sorry!"
    mc "I guess I shouldn't have done that..." 
    stop music
    y "A-Ah..."
    "Yuri starts to breathe heavily."
    y "I..."
    y "I can't..."
    y "[player]..."
    "Suddenly, Yuri forcefully grabs my arm and jerks me to my feet."
    "My teacup gets knocked over."
    scene bg closet
    show yuri 2t at t11 zorder 2
    with wipeleft
    y "[player]..."
    play sound closet_close
    show dark zorder 100
    with wipeleft
    y "My heart..."
    y 2y6 "My heart won't stop pounding, [player]..."
    y "I can't calm down."
    y "I can't focus on anything anymore...!"
    y "Can you feel it, [player]?"
    "Yuri suddenly presses my hand against her chest."
    play music hb
    show layer master at heartbeat
    y 3t "Why is this happening to me?"
    y "I feel like I'm losing my mind..."
    y 3y4 "I can't make it stop."
    y 3y6 "It even makes me not want to read..."
    y "I just want..."
    y 3s "...to look..."
    y "...at you."
    hide yuri
    show yuri eyes
    pause 3.0
    y "...Haah..."
    pause 3.0
    y "...Haah..."
    pause 3.0
    y "...Haah..."
    pause 3.0
    play sound closet_open
    stop music
    show layer master
    hide yuripupils
    show yuri 1n at face
    with None
    show yuri 3n at t32 with None
    hide dark
    show monika 3l at f31 zorder 3
    with wipeleft
    m "U-Um..."
    m "It's...time to share poems..."




    return

label yuri_exclusive2_2_ch23:
    scene black
    with None
    $ audio.t6g = "<loop 10.893>bgm/6g.ogg"
    play music t6g
    pause 4.62
    scene bg corridor
    show yuri eyes_base
    pause 1.0
    show bg glitch:
        yoffset 480 ytile 2
        linear 0.25 yoffset 0
        repeat
    show yuri glitch at i11
    $ gtext = glitchtext(80)
    $ currentpos = get_pos()
    play music g1
    y "[gtext]{nw}"
    stop music
    scene bg corridor
    show yuri 2n at i11
    y "Um..."
    y "Wait..."
    y 2o "How did I..."
    y 2y6 "...Sorry, I just had a really weird déjà vu..."
    y "This hasn't happened before or anything...right?"
    y 2t "My head has been a little fuzzy lately..."
    y 3t "I hope it hasn't really been showing or anything!"
    y "I would hate for you to think I'm weird just after we started spending time together..."
    y "I mean..."
    show bg corridor:
        xoffset 0
        parallel:
            0.36
            xoffset 1
            repeat
        parallel:
            0.49
            xoffset 0
            repeat
    show black zorder 5:
        alpha 0.5
        parallel:
            0.36
            alpha 0.5
            repeat
        parallel:
            0.49
            alpha 0.475
            repeat

    play music t9
    y "Everyone has a few unusual things about them."
    y 1v "But expressing those things so soon after meeting someone is usually seen as inappropriate...or unlikeable."
    y "At least, that's what I've discovered."
    y "When I was a bit younger, I think I would come on really strongly and get a little too intense..."
    y "It made people not want to be around me."
    y 2w "So...I started hating those things about myself."
    y "My obsession with certain hobbies."
    y "And the way I can't control myself when I get too excited about something."
    y "So..."
    y 1v "I eventually stopped trying to talk to people."
    y "If nobody could ever like me for the things that matter most to me..."
    y 1u "...Then it's just easier if I close myself off."
    y 1h "But recently, something's been wrong."
    y "I don't know what it is."
    y 2y6 "But every time we come to the club, my heart starts to go crazy."
    y "Like it's going to rip out of my chest."
    y "It overwhelms me with energy and emotions that I can't let out."
    y "It's been making me do weird things."
    y 2t "I don't know why it's happening!"
    stop music
    y 1t "[player]..."
    y "Is it just me, or has Monika been acting a little off lately?"
    y 1v "She's always been a sweetheart ever since I joined the club..."
    y "But recently, I've been feeling something sharp whenever she's around."
    y 2y4 "I'm not crazy, right?"
    y 2y1 "Please tell me I'm not!"
    y "I couldn't say anything before, because she's always listening!"
    y 2y3 "But finally, we're alone..."
    y "Can we just stay here for a while?"
    y 1m "Yeah..."
    y "..."
    play music hb
    show layer master at heartbeat
    show yuri as yuri_eyes zorder 4:
        "yuri/eyesfull.png"
        i11
        alpha 0.0
        block:
            2.012 * 4 - 1.49
            alpha 1.0
            0.52
            alpha 0.0
            1.49
            repeat
    pause 2.0
    $ ad = 40.0
    $ ac = 1.0
    show monika 1 at malpha(ac / ad) onlayer front
    y 1s "I just want to stay here."
    $ ac += 0
    show monika 1 at malpha(ac / ad) onlayer front
    y "Just the two of us."
    $ ac += 0
    show monika 1 at malpha(ac / ad) onlayer front
    y "We can stay here until the club ends."
    $ ac += 0
    show monika 1 at malpha(ac / ad) onlayer front
    y 1m "And then we'll have the clubroom all to ourselves."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y "Nobody to interfere with our reading time."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y 1y4 "Nobody to make me feel like stabbing myself in the throat."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y 1q "Ahaha..."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y "That was a joke!"
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y "Just a joke."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y 1i "I do like knives, though..."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y "It sounds strange, but you wouldn't understand if you've never seen how beautiful they can be."
    $ ac += 0.5
    show monika 1 at malpha(ac / ad) onlayer front
    y 1f "I have an idea."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "Why don't you come to my house sometime?"
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1y6 "I can show you my collection."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "I've gotten them all from various artisans."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1a "I make sure to give them all their fair share of use."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1m "I don't want them to get lonely or anything..."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1y6 "Nobody deserves to be lonely."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1y4 "Nobody."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1c "And that's why I'm so happy you joined the Literature Club, [player]."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1a "Now we don't need to be lonely anymore."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "Because we have each other."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "Every day."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "That's all we need."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1y6 "You know what?"
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "Let's quit the Literature Club."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "There's no need for us to be around Monika's slimy tongue anymore."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1y4 "Not to mention that other pathetic child."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1s "We can walk home together every day after school."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "And read together."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1m "Eat together."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y "Sleep together."
    $ ac += 1
    show monika 1 at malpha(ac / ad) onlayer front
    y 1s "Doesn't that sound perfect?"
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    y "It's everything we could ever want."
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    y 1a "Isn't that why you joined the club in the first place?"
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    y "It's almost like it was fate."
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    y "Fate that we would meet each other."
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    y "And now we get the happy ending that I've patiently waited years for."
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    y "Will you do that with me, [player]?"
    $ ac += 2
    show monika 1 at malpha(ac / ad) onlayer front
    $ gtext = glitchtext(200)
    y "Will{space=60}[gtext]{nw}"
    hide monika onlayer front
    window hide(None)
    $ poemsread = 0
    $ y_gave = False
    play music t5
    scene bg club_day
    window show(None)
    window auto

    return