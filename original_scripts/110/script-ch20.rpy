label ch20_from_ch10:
    scene bg residential_day
    with dissolve_scene_half
    play music t2
    jump ch20_main2

label ch20_main:
    stop music fadeout 2.0
    scene bg residential_day
    with dissolve_scene_full
    play music t2

label ch20_main2:
    "It's an ordinary school day, like any other."
    "Mornings are usually the worst, being surrounded by couples and friend groups walking to school together."
    "Meanwhile, I've always walked to school alone."
    "I always tell myself it's about time I meet some girls or something like that..."
    "But I have no motivation to join any clubs."
    "I'm perfectly content just getting by on the average while spending my free time on games and anime."
    "There's always the anime club, but it's not like there would be any girls in it anyway..."
    
    scene bg class_day
    with wipeleft_scene

    "The school day is as ordinary as ever, and it's over before I know it."
    "After I pack up my things, I stare blankly at the wall, looking for an ounce of motivation."
    mc "Clubs..."
    "There really aren't any that interest me."
    "Besides, most of them would probably be way too demanding for me to want to deal with."
    "I guess I have no choice but to start with the anime club..."

    $ m_name = "???"

    m "...[player]?"
    window hide(None)
    show monika g2 at t11 zorder 2
    pause 0.75
    show screen tear(20, 0.1, 0.1, 0, 40)
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.25
    stop sound
    hide screen tear
    window show(None)
    show monika 1 at t11 zorder 2
    mc "...Monika?"
    $ m_name = "Monika"
    m 1b "Oh my goodness, I totally didn't expect to see you here!"
    m 5 "It's been a while, right?"
    mc "Ah..."
    mc "Yeah, it has."
    "Monika smiles sweetly."
    "We do know each other - well, we rarely talked, but we were in the same class last year."
    "Monika was probably the most popular girl in class - smart, beautiful, athletic."
    "Basically, completely out of my league."
    "So, having her smile at me so genuinely feels a little..."
    mc "What did you come in here for, anyway?"
    m 1a "Oh, I've just been looking for some supplies to use for my club."
    m 1d "Do you know if there's any construction paper in here?"
    m "Or markers?"
    mc "I guess you could check the closet."
    mc "...You're in the debate club, right?"
    m 5 "Ahaha, about that..."
    m "I actually quit the debate club."
    mc "Really? You quit?"
    m "Yeah..."
    m 2e "To be honest, I can't stand all of the politics around the major clubs."
    m "It feels like nothing but arguing about the budget and publicity and how to prepare for events..."
    m "I'd much rather take something I personally enjoy and make something special out of it."
    mc "In that case, what club did you decide to join?"
    m 1b "Actually, I'm starting a new one!"
    m "A literature club!{nw}"
    show screen tear(20, 0.1, 0.1, 0, 40)
    window hide(None)
    play sound "sfx/s_kill_glitch1.ogg"
    pause 0.25
    stop sound
    hide screen tear
    window show(None)
    m "A literature club!{fast}"
    window auto
    mc "Literature...?"
    "That sounds kind of...dull?"
    mc "How many members do you have so far?"
    m 5 "Um..."
    m "Ahaha..."
    m "It's kind of embarrassing, but there are only three of us so far."
    m "It's really hard to find new members for something that sounds so boring..."
    mc "Well, I can see that..."
    m 3d "But it's really not boring at all, you know!"
    m "Literature can be anything. Reading, writing, poetry..."
    m 3e "I mean, one of my members even keeps her manga collection in the clubroom..."
    mc "Wait...really?"
    m 2k "Yeah, it's funny, right?"
    m 2e "She always insists that manga is literature, too."
    m "I mean, she's not wrong, I guess..."
    m "And besides, a member's a member, right?"
    "...Did Monika say \"she\"?"
    "Hmm..."
    m 1a "Hey, [player]..."
    m "By any chance...are you still looking for a club to join?"
    mc "Ah--"
    mc "I mean, I guess so, but..."
    m "In that case..."
    m 5 "Is there any chance you could do me a big favor?"
    m "I won't ask you to join, but..."
    m "If you could at the very least visit my club, it would make me really happy."
    m "Please?"
    mc "Um..."
    "Well, I guess I have no reason to refuse..."
    "Besides, how could I ever refuse someone like Monika?"
    mc "Sure, I guess I could check it out."
    m 1k "Aah, awesome!"
    m 1b "You're really sweet, [player], you know that?"
    mc "I-It's nothing, really..."
    m 1a "Shall we go, then?"
    m "I'll look for the materials another time - you're more important."

    stop music fadeout 2.0

    scene bg corridor
    with wipeleft_scene

    "And thus, today marks the day I sold my soul to Monika and her irresistible smile."
    "I timidly follow Monika across the school and upstairs - a section of the school I rarely visit, being generally used for third-year classes and activities."
    "Monika, full of energy, swings open the classroom door."

    scene bg club_day2
    with wipeleft
    play music t3

    if renpy.random.randint(0, 2) == 0:
        show monika g1 at l31
    else:
        show monika 3b at l31
    m "I'm back~!"
    m "And I brought a guest with me!"
    show yuri 2t at t33 zorder 2
    if not config.skipping:
        show screen invert(0.15, 0.3)
    y "Eh?"
    y "A...a guest?"
    show natsuki 4c at t32 zorder 2
    n "Seriously? You brought a boy?"
    n "Way to kill the atmosphere."
    show monika 3m at f31 zorder 3
    m "Don't be mean, Natsuki..."
    m 3b "...But anyway, welcome to the club, [player]!"
    show monika 3a at t31 zorder 2
    mc "..."
    "All words escape me in this situation."
    "This club..."
    "{i}...is full of incredibly cute girls!!{/i}"

    show natsuki at f32 zorder 3
    n 5c "So, let me guess..."
    n "You're Monika's boyfriend, right?"
    show natsuki at t32 zorder 2
    mc "Wha--"
    mc "No, I'm not!"
    show yuri at f33 zorder 3
    y 2l "Natsuki..."
    $ n_name = 'Natsuki'
    "The girl with the sour attitude, whose name is apparently Natsuki, is one I don't recognize."
    "Her small figure makes me think she's probably a first-year."

    show yuri at t33 zorder 2
    show monika at f31 zorder 3
    m 2l "A-Anyway, this is Natsuki, energetic as usual..."
    m 2b "And this is Yuri, the Vice President!"
    $ y_name = 'Yuri'
    show monika 2a at t31 zorder 2
    show yuri at f33 zorder 3
    y 4 "I-It's nice to meet you..."
    "Yuri, who appears comparably more mature and timid, seems to have a hard time keeping up with someone like Natsuki."
    show yuri at t33 zorder 2
    mc "Yeah... It's nice to meet both of you."
    show monika at f31 zorder 3
    m 1a "So, I ran into [player] in a classroom, and he decided to come check out the club."
    m "Isn't that great?"
    show monika at t31 zorder 2
    show natsuki at f32 zorder 3
    n 4e "Wait! Monika!"
    n "Didn't I tell you to let me know in advance before you brought anyone new?"
    n 4q "I was going to...well, you know..."
    show natsuki at t32 zorder 2
    show monika at f31 zorder 3
    m 1e "Sorry, sorry!"
    m "I didn't forget that, but I just happened to run into him."
    show monika at t31 zorder 2
    show yuri at f33 zorder 3
    y 1a "In that case, I should at least make some tea, right?"
    show yuri at t33 zorder 2
    show monika at f31 zorder 3
    m 1b "Yeah, that would be great!"
    m "Why don't you come sit down, [player]?"
    hide monika
    hide natsuki
    hide yuri
    with wipeleft
    "The girls have a few desks arranged to form a table."
    "Yuri walks to the corner of the room and opens the closet."
    "Meanwhile, Monika and Natsuki sit across from each other."
    "Still feeling awkward, I take a seat next to Monika."
    show monika 1a at t11 zorder 2
    m "So, I know you didn't really plan on coming here..."
    m "But we'll make sure you feel right at home, okay?"
    m 1j "As president of the Literature Club, it's my duty to make the club fun and exciting for everyone!"
    mc "I'm surprised there aren't more people in the club yet."
    mc "It must be hard to start a new club."
    m 3b "You could put it that way."
    m "Not many people are very interested in putting out all the effort to start something brand new..."
    m "Especially when it's something that doesn't grab your attention, like literature."
    m "You have to work hard to convince people that you're both fun and worthwhile."
    m "But it makes school events, like the festival, that much more important."
    m 2k "I'm confident that we can all really grow this club before we graduate!"
    m "Right, Natsuki?"
    show monika at t22 zorder 2
    show natsuki 4q at t21 zorder 2
    n "Well..."
    n "...I guess."
    "Natsuki reluctantly agrees."
    "Such different girls, all interested in the same goal..."
    "Monika must have worked really hard just to find these two."
    "Yuri returns to the table, carrying a tea set."
    "She carefully places a teacup in front of each of us before setting down the teapot in the middle."
    show natsuki at thide zorder 1
    show monika at thide zorder 1
    hide natsuki
    hide monika
    show yuri 1a at t21 zorder 2
    mc "You keep a whole tea set in this classroom?"
    y "Don't worry, the teachers gave us permission."
    y "After all, doesn't a hot cup of tea help you enjoy a good book?"
    mc "Ah... I-I guess..."
    show monika 4a at f22 zorder 3
    m "Ehehe, don't let yourself get intimidated, Yuri's just trying to impress you."
    show monika at t22 zorder 2
    show yuri at hf21
    y 3n "Eh?! T-That's not..."
    "Insulted, Yuri looks away."
    y 4b "I meant that, you know..."
    show yuri at t21 zorder 2
    mc "I believe you."
    mc "Well, tea and reading might not be a pastime for me, but I at least enjoy tea."
    show yuri at f21 zorder 3
    y 2u "I'm glad..."
    show yuri at t21 zorder 2
    "Yuri faintly smiles to herself in relief."
    show monika at thide zorder 1
    hide monika
    show yuri 1a at t32 zorder 2
    y "So, [player], what kinds of things do you like to read?"
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
    y "Stories with deep psychological elements usually immerse me as well."
    y 2a "Isn't it amazing how a writer can so deliberately take advantage of your own lack of imagination to completely throw you for a loop?"
    y "Anyway, I've been reading a lot of horror lately..."
    mc "Ah, I read a horror book once..."
    "I desperately grasp something I can relate to at the minimal level."
    "At this rate, Yuri might as well be having a conversation with a rock."
    show monika 1j at f33 zorder 3
    m "Ahaha. I'd expect that from you, Yuri."
    m 1a "It suits your personality."
    show monika at t33 zorder 2
    show yuri at f32 zorder 3
    y 1a "Oh, is that so?"
    y "Really, if a story makes me think, or takes me to another world, then I really can't put it down."
    y "Surreal horror is often very successful at changing the way you look at the world, if only for a brief moment."
    show yuri at t32 zorder 2
    show natsuki 5q at f31 zorder 3
    n "Ugh, I hate horror..."
    show natsuki at t31 zorder 2
    show yuri at f32 zorder 3
    y 1f "Oh? Why's that?"
    show yuri at t32 zorder 2
    show natsuki at f31 zorder 3
    n 5c "Well, I just..."
    "Natsuki's eyes dart over to me for a split second."
    n 5q "Never mind."
    show natsuki at t31 zorder 2
    show monika at f33 zorder 3
    m 1a "That's right, you usually like to write about cute things, don't you, Natsuki?"
    show monika at t33 zorder 2
    show natsuki 1o at f31 zorder 3
    n "W-What?"
    n "What gives you that idea?"
    show natsuki at t31 zorder 2
    show monika at f33 zorder 3
    m 3b "You left a piece of scrap paper behind last club meeting."
    m "It looked like you were working on a poem called--"
    show monika at t33 zorder 2
    show natsuki 1p at f31 zorder 3
    n "Don't say it out loud!!"
    n "And give that back!"
    show natsuki at t31 zorder 2
    show monika at f33 zorder 3
    m 1j "Fine, fine~"
    show monika 1a at t33 zorder 2
    mc "Natsuki, you write your own poems?"
    show natsuki at f31 zorder 3
    n 1c "Eh? Well, I guess sometimes."
    n "Why do you care?"
    show natsuki at t31 zorder 2
    mc "I think that's impressive."
    mc "Why don't you share them sometime?"
    show natsuki at f31 zorder 3
    n 5q "N-No!"
    "Natsuki averts her eyes."
    n "You wouldn't...like them..."
    show natsuki at t31 zorder 2
    mc "Ah...not a very confident writer yet?"
    show yuri at f32 zorder 3
    y 2f "I understand how Natsuki feels."
    y "Sharing that level of writing takes more than just confidence."
    y 2k "The truest form of writing is writing to oneself."
    y "You must be willing to open up to your readers, exposing your vulnerabilities and showing even the deepest reaches of your heart."
    show yuri at t32 zorder 2
    show monika 2a at f33 zorder 3
    m "Do you have writing experience too, Yuri?"
    m "Maybe if you share some of your work, you can set an example and help Natsuki feel comfortable enough to share hers."
    show yuri at s32
    y 3o "..."
    mc "I guess it's the same for Yuri..."
    "We all sit in silence for a moment."
    show monika at f33 zorder 3
    m 5a "Hey, I just got an idea!"
    m "How about this?"
    show monika at t33 zorder 2
    show natsuki 2k at f31 zorder 3
    show yuri 3e at f32 zorder 3
    ny "...?"
    "Natsuki and Yuri look quizzically at Monika."
    show natsuki at t31 zorder 2
    show yuri at t32 zorder 2
    show monika at f33 zorder 3
    m 2b "Let's all go home and write a poem of our own!"
    m "Then, next time we meet, we'll all share them with each other."
    m "That way, everyone is even!"
    show monika 2a at t33 zorder 2
    show natsuki at f31 zorder 3
    n 5q "U-Um..."
    show natsuki at t31 zorder 2
    show yuri 3v at f32 zorder 3
    y "..."
    show yuri at t32 zorder 2
    show monika 2m at f33 zorder 3
    m "Ah..."
    m "I mean, I thought it was a good idea..."
    show monika at t33 zorder 2
    show yuri at f32 zorder 3
    y 2l "Well..."
    y "...I think you're right, Monika."
    y 2f "We should probably start finding activities for all of us to participate in together."
    y 2h "I did decide to take on the responsibility of Vice President, after all..."
    y "I need to do my best to nurture the club as well as its members."
    y 2a "Besides, now that we have a new member..."
    y "It seems like a good step for us to take."
    y "Do you agree as well, [player]?"
    show yuri at t32 zorder 2
    mc "Hold on...there's still one problem."
    show monika at f33 zorder 3
    m 1d "Eh? What's that?"
    "Now that we've reached the most important topic, I bluntly come forth with what's been on my mind the entire time."
    show monika at t33 zorder 2
    mc "I never said I would join this club!"
    mc "Monika may have convinced me to stop by, but I never made any decision."
    mc "I still have other clubs to look at, and...um..."
    show monika 1g
    show natsuki 4g
    show yuri 2e
    "I lose my train of thought."
    "All three girls stare back at me with dejected eyes."
    show monika at s33
    m 1p "B-But..."
    show yuri at s32
    y 2v "I'm sorry, I thought..."
    show natsuki at s31
    n 5s "Hmph."
    mc "Eh...?"
    "The girls exchange glances before Monika turns back to me."
    show monika at f33 zorder 3
    m 1m "I...guess I need to tell you the truth, [player]."
    m "The thing is..."
    m 1p "...We don't have enough members yet to form an official club."
    m "We need four..."
    m "And I've been trying really, really hard to find new members."
    m "And if we don't find one more before the festival..."
    show monika at t33 zorder 2
    mc "..."
    "I...I'm defenseless against these girls."
    "How am I supposed to make a clear-headed decision when it's like this?"
    "I would feel terrible for letting everyone down in this situation..."
    "And besides, the club itself seems pretty relaxed..."
    "So, if writing poems is the price I need to pay in order to spend every day with these beautiful girls..."
    mc "...Right."
    mc "Okay, I've decided, then."
    mc "I'll join the Literature Club."
    show monika 1e at t33 zorder 2
    show yuri 3f at t32 zorder 2
    show natsuki 1k at t31 zorder 2
    "One by one, the girls' eyes light up."
    show monika at f33 zorder 3
    m "Oh my goodness, really?"
    m "Do you really mean that, [player]?"
    show monika at t33 zorder 2
    mc "Yeah..."
    mc "It could be fun, right?"
    show yuri at f32 zorder 3
    y 1m "You really did scare me for a moment..."
    show yuri at t32 zorder 2
    show natsuki at f31 zorder 3
    n 5q "I mean, if you really just left after all this, I would be super pissed."
    show natsuki at t31 zorder 2
    show monika at f33 zorder 3
    m "[player], I'm so happy..."
    m 1k "We can become an official club now!"
    m 1e "Thank you so much for this. You're really amazing."
    m "I'll do everything I can to give you a great time, okay?"
    show monika at t33 zorder 2
    mc "Ah...thanks, I guess."
    show yuri at thide zorder 1
    show natsuki at thide zorder 1
    show monika at t11 zorder 2
    hide yuri
    hide natsuki
    m 3b "Okay, everyone!"
    m "I think with that, we can officially end today's meeting on a good note."
    m "Everyone remember tonight's assignment:"
    m "Write a poem to bring to the next meeting, so we can all share!"
    "Monika looks over at me once more."
    m 1a "[player], I look forward to seeing how you express yourself."
    show monika 5 at hop
    m "Ehehe~"
    mc "Y-Yeah..."
    show monika at thide zorder 1
    hide monika
    "Can I really impress the class star Monika with my mediocre writing skills?"
    "I already feel the anxiety welling up inside me."
    "Meanwhile, the girls continue to chit-chat as Yuri cleans up the tea set."
    mc "I guess I'll be on my way, then..."
    show monika 5a at t11 zorder 2
    m "Okay!"
    m "I'll see you tomorrow, then."
    m "I can't wait!"

    scene bg residential_day
    with wipeleft_scene

    "With that, I depart the clubroom and make my way home."
    "The whole way, my mind wanders back and forth between the three girls:"
    show natsuki 4a at t31 zorder 2
    "Natsuki,"
    show yuri 1a at t32 zorder 2
    "Yuri,"
    show monika 1a at t33 zorder 2
    "and, of course, Monika."
    "Will I really be happy spending every day after school in a literature club?"
    "Perhaps I'll have the chance to grow closer to one of these girls..."
    hide natsuki
    hide yuri
    hide monika
    with wipeleft
    "Alright!"
    "I'll just need to make the most of my circumstances, and I'm sure good fortune will find me."
    "And I guess that starts with writing a poem tonight..."

    stop music fadeout 2.0
    scene black with dissolve_scene_full
    $ config.skipping = False
    $ config.allow_skipping = False
    $ allow_skipping = False

    call screen confirm("You have unlocked a special poem.\nWould you like to read it?", Return(True), Return(False))
    if _return:
        call expression "poem_special_" + str(persistent.special_poems[0])
    else:
        pass

    return