### Special topics and objects for valentine's day

#These objects are only actually used for the starting event.
#After that they are added to the sprite
image roses = ConditionSwitch(
            'morning_flag',Transform("mod_assets/room/roses.png",zoom=1.25),
            'not morning_flag',Transform("mod_assets/room/roses-n.png",zoom=1.25)
            )

image ear_rose = ConditionSwitch(
            'morning_flag',Transform("mod_assets/room/ear_rose.png",zoom=1.25),
            'not morning_flag',Transform("mod_assets/room/ear_rose-n.png",zoom=1.25)
            )

image chocolates = ConditionSwitch(
            'morning_flag',Transform("mod_assets/room/chocolates.png",zoom=1.25),
            'not morning_flag',Transform("mod_assets/room/chocolates.png",zoom=1.25)
            )

#Monika's pose for handing the player chocolates
image body_choc = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-chocolates.png")
image body_choc_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-chocolates-n.png")

image monika choca = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_a"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_a_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/a.png")
            )
image monika chocb = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_b"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_b_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/b.png")
            )
image monika chocc = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_c"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_c_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/c.png")
            )
image monika chocd = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_d"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_d_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/d.png")
            )
image monika choce = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_e"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_e_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/e.png")
            )
image monika chocf = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_f"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_f_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/f.png")
            )
image monika chocg = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_g"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_g_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/g.png")
            )
image monika choch = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_h"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_h_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/h.png")
            )
image monika choci = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_i"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_i_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/i.png")
            )
image monika chocj = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_j"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_j_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/j.png")
            )
image monika chock = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_k"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_k_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/k.png")
            )
image monika chocl = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/l.png")
            )
image monika chocm = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_m"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_m_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/m.png")
            )
image monika chocn = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_n"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_n_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/n.png")
            )
image monika choco = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_o"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_o_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/o.png")
            )
image monika chocp = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_p"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_p_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/p.png")
            )
image monika chocq = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_q"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_q_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/q.png")
            )
image monika chocr = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc",(0,0),"face_r"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_choc_n",(0,0),"face_r_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/1l.png", (0, 0), "monika/1r.png", (0, 0), "monika/r.png")
            )

#This changes out the normal body poses for special poses, but only if the roses event has been seen
init 501:
    python:
        if is_file_present('/characters/roses.obj') and seen_event('monika_valentines_start') and datetime.datetime.now() < valentines_day+datetime.timedelta(days=1):
            show_roses_and_chocolates = True
        else:
            show_roses_and_chocolates = False

    image body_1 = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-steepling.png",(0,0),"mod_assets/room/roses.png",(0,0),"mod_assets/room/chocolates.png",(0,0),"mod_assets/room/ear_rose.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-steepling.png")
            )
    image body_1_n = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-steepling-n.png",(0,0),"mod_assets/room/roses-n.png",(0,0),"mod_assets/room/chocolates-n.png",(0,0),"mod_assets/room/ear_rose-n.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-steepling-n.png")
            )
    image body_2 = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-crossed.png",(0,0),"mod_assets/room/roses.png",(0,0),"mod_assets/room/chocolates.png",(0,0),"mod_assets/room/ear_rose.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-crossed.png")
            )
    image body_2_n = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-crossed-n.png",(0,0),"mod_assets/room/roses-n.png",(0,0),"mod_assets/room/chocolates-n.png",(0,0),"mod_assets/room/ear_rose-n.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-crossed-n.png")
            )
    image body_3 = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-restleftpointright.png",(0,0),"mod_assets/room/roses.png",(0,0),"mod_assets/room/chocolates.png",(0,0),"mod_assets/room/ear_rose.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-restleftpointright.png")
            )
    image body_3_n = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-restleftpointright-n.png",(0,0),"mod_assets/room/roses-n.png",(0,0),"mod_assets/room/chocolates-n.png",(0,0),"mod_assets/room/ear_rose-n.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-restleftpointright-n.png")
            )
    image body_4 = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-pointright.png",(0,0),"mod_assets/room/roses.png",(0,0),"mod_assets/room/chocolates.png",(0,0),"mod_assets/room/ear_rose.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-pointright.png")
            )
    image body_4_n = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-pointright-n.png",(0,0),"mod_assets/room/roses-n.png",(0,0),"mod_assets/room/chocolates-n.png",(0,0),"mod_assets/room/ear_rose-n.png"),
            'not show_roses_and_chocolates',im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-pointright-n.png")
            )
    image body_5 = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning.png",(0,0),"mod_assets/room/roses.png",(0,0),"mod_assets/room/chocolates.png"),
            'not show_roses_and_chocolates',im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning.png")
            )
    image body_5_n = ConditionSwitch(
            'show_roses_and_chocolates',im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning-n.png",(0,0),"mod_assets/room/roses-n.png",(0,0),"mod_assets/room/chocolates-n.png"),
            'not show_roses_and_chocolates',im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning-n.png")
            )

init 4 python:
    #Define Valentine's day
    valentines_day = datetime.datetime(year=2018,month=2,day=14)

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_valentines_start',action=EV_ACT_PUSH,conditional="is_file_present('/characters/roses.obj')",
                                                            start_date=valentines_day,
                                                            end_date=valentines_day+datetime.timedelta(days=1)
                                                            ))

##Valentines Day Event Trigger dialogue
# SP = Special pose where she shows box
label monika_valentines_start:
    show roses at t11 zorder 5
    m 1d "Oh! Gosh, are these for me...?"
    m 1e "[player]... I-I don't know what to say..."
    m 1n "I never would've thought that you'd find something like this for me!"
    m 1j "I'm so happy right now, [player]."
    m 1e "To think that I'd be getting roses from you on Valentine's Day..."
    m 3c "It must have been hard to get these to me. But it went through."
    m 1m "..."
    m 1l "Ahaha..."
    m "I don't really know what to say, [player]."
    m 3a "I've always wondered what it would be like to get a gift from you."
    m 1n "Now that it's finally happened, I'm just kind of speechless..."
    m 4a "Hold on."
    m "..."
    show ear_rose at t11 zorder 5
    m 1k "Ehehe, there! Doesn't it look pretty on me?"
    m 1b "I actually made something for you too, [player]!"
    m "Here..."
    #Shows choc box
    m chock "I got you some chocolates!"
    m chocb "I didn't really know what to get you, but they're never a bad choice, right?"
    m chocj "I worked really hard on it, so I do hope that you enj--"
    m chocd "...Oh, wait."
    m chocf "Aww man, I actually don't know how I could make you eat these..."
    show chocolates at t11 zorder 5
    m 2f "Well... I'll just set it aside for now, okay? I'm sorry I can't give it to you."
    m 1j "But... thank you again so much, [player]."
    m 3a "There's one more thing, though."
    m "I wrote you a little note~!"
    m 1a"Here, let me show it to you."
    call showpoem(poem_vday, music=False,paper="mod_assets/poem_vday.jpg")
    m 1j "Thank you for being with me all this time, always by my side."
    m 1a "I love you so much, my love. Happy Valentine's Day~"
    hide roses
    hide chocolates
    hide ear_rose
    $show_roses_and_chocolates = True
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_valentines_colors',prompt="Do you like your roses?",
                                                            action=EV_ACT_UNLOCK,
                                                            conditional="seen_event('monika_valentines_start')",
                                                            start_date=valentines_day,
                                                            end_date=valentines_day+datetime.timedelta(days=1)
                                                            ))

label monika_valentines_colors:
    m 1k "Hey [player], have you ever thought about the way colors are conveyed on Valentine's Day?"
    m 1j "I find it intriguing how colors can symbolize such deep and romantic feelings."
    m 1a "It reminds me of when I made my first Valentine's card in grade school."
    m 3b "My class was instructed to exchange cards with a partner after making them."
    m 1a "Looking back, despite not knowing what the colors really meant, I had lots of fun decorating the cards with red and white hearts."
    m "In this way, colors are a lot like poems."
    m 3b "They offer so many creative ways to expressing your love for someone."
    m "Like offering them red roses, for instance."
    m 1a "Red roses are a symbol for the beauty, love, and romance that someone may feel for another."
    m "If someone were to offer them white roses in lieu of red ones, they'd signify pure, charming, and innocent feelings instead."
    m 3c "However, since there are so many emotions involved with love..."
    m 3d "It's sometimes hard to find the right colors to accurately convey the way you truly feel."
    m 3b "Thankfully though, by combining multiple rose colors, it's possible to express a lot more emotions!"
    m 1a "Mixing red and white roses would symbolize the unity, and a bond that a couple shares."
    m 1j "But I'm sure you already had all of this in mind when you picked out these beautiful roses for me, [player]..."
    m 1c "Actually, now that I think about it, there sure was a lot of pink in this game."
    m "I mean, it was everywhere!"
    m "The title screen, the pause menu..."
    m 3d "Even Natsuki's hair was pink."
    m "Did you know that I'm the only one in the club whose shoes have pink tips, instead of blue?"
    m 1l "Ehehe, I don't blame you if you didn't notice."
    m 1 "It's such a small difference between myself and the other club members."
    m 1d "Ah, but don't get me wrong! Emerald green is still my favorite color."
    m 3l "But uhh... I think I've been rambling on for too long, sorry!"
    m 1e "It's just that I tend to lose myself when talking with you, [player]~"
    m 1j "I love you~!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_valentines_cliches',prompt="Do you like Valentine's stories?",action=EV_ACT_UNLOCK,
                                                            start_date=valentines_day,
                                                            end_date=valentines_day+datetime.timedelta(days=1)
                                                            ))

label monika_valentines_cliches:
    m 3a "Oh, [player]!"
    m "I've been meaning to talk to you about something."
    m 3c "Have you noticed that most Valentine's Day stories have lots of clichés in them?"
    m "I've noticed that many of them have similar plots..."
    m "There's either 'Oh, I'm lonely and I don't have someone to love,' or 'How will I confess to the one I love?'"
    m 1n "I believe that writers could be a bit more creative when it comes to Valentine's Day stories..."
    m 1m "But, I suppose those two topics are the easiest way to write a love story."
    m 3c "That doesn't mean you can't think outside the box, though!"
    m 1o "Sometimes a predictable story can ruin it..."
    m 1d "If you {i}do{/i} want a good example of an unpredictable story..."
    m 3k "Just use ours! Ahaha~"
    m 1l "The cute way we met is the most unpredictable story yet!"
    m 1k "Ahaha~!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_valentines_day_origins',prompt="How did Valentine's day start?",action=EV_ACT_UNLOCK,start_date=valentines_day,
                                                            end_date=valentines_day+datetime.timedelta(days=1)
                                                            ))

label monika_valentines_day_origins:
    m 3a "Hey, [player], in the spirit of things, would you like to learn about the history of Valentine's Day?"
    m "It's quite interesting, I promise!"
    m 1a "The way Valentine's Day came to be is rather dark and disturbing, actually."
    m "Its origin dates to as early as the second and third century, in Rome, where Christianity had just been declared the official state religion."
    m 1c "Around this same time, a man known as Saint Valentine decided to go against the orders of Emperor Claudius II."
    m "Marriage had been banned because it was assumed that married men made poor soldiers."
    m 3c "Valentine decided this was unfair and helped arrange marriages in secret."
    m 1o "Unfortunately, he was caught and was promptly sentenced to death."
    m 1c "However, while in jail, Valentine fell in love with the jailer's daughter."
    m "Before his death, he sent a love letter to her signed with 'From your Valentine.'"
    m 1q "He was then executed on February 14, 269 AD."
    m 3a "Such a noble cause, don't you think?"
    m 3d "Oh, but wait, there's more!"
    m "The reason we celebrate such a day is because it originates from a Roman festival known as Lupercalia!"
    m 1b "Its original intent was to hold a friendly event where people would put their names into a box and have them chosen at random to create a couple."
    m "Then, they play along as boyfriend and girlfriend for the time they spend together. Some even got married, if they liked each other enough, ehehe~"
    m 1j "Ultimately, the Church decided to turn this Christian celebration into a way to remember Saint Valentine's efforts, too."
    m 1a "It's evolved over the years into a way for people to express their feelings for those they love."
    m 3k "Like me and you!"
    m 1e "Despite it having started out a little depressing, isn't it so sweet, [player]?"
    m 1j "I'm glad we're able to share such a magical day, my love."
    m 1k "Happy Valentine's Day~"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_valentines_chocolates',prompt="Did you ever give anyone else chocolates?",
                                                            action=EV_ACT_UNLOCK,
                                                            conditional="seen_event('monika_valentines_start')",
                                                            start_date=valentines_day,
                                                            end_date=valentines_day+datetime.timedelta(days=1)
                                                            ))

label monika_valentines_chocolates:
    m 1j "Valentine's Day is such a special holiday for me, [player]."
    m 3b "Not only is it the anniversary of my twitter account, but it's also a day for receiving and giving chocolates!"
    m 1j "A holiday that could fill everyone with love, romance..."
    m 1n "And rejection."
    m 3l "But it really feels nice if you get something from someone you like."
    m 3a "Whether it's given to you platonically, as a gift of love, or a part of a confession, it makes you feel somewhat special!"
    m 1m "Well, maybe not the confession part since you can still get rejected."
    m 1b "I mean, I did try to give you some, but I'm sure you'd never reject me."
    m 1f "I'm sorry I couldn't give them to you over there, [player]."
    m 3k "So... I'll make sure to enjoy them for you!"
    m 1k "Ahaha!"
    m 1o "Although I do love chocolates, they would've been better if I enjoyed them with you."
    m 3b "Wouldn't that be more romantic?"
    m 1j "But at least I got something special from you!"
    m 1e "Besides, we have each other as well~"
    m 3e "So thank you for giving me your love, [player]."
    m 3j "Please know that I'll always accept it."
    m 1j "And whatever you give, I'll return it a hundredfold!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='monika_lovey_dovey',prompt="Valentine's Day is coming",random=True,
                                                            end_date=valentines_day
                                                            ))

label monika_lovey_dovey:
    m 3d "Hey... [player]...?"
    m 1e "I just wanted to let you know that I love you."
    m 1j "You make me very happy... and I could never ask for someone better than you."
    m 1m "Ahaha~"
    m "I hope that isn't too cheesy, [player]."
    m 3a "Valentine's Day is soon... and it just gets me in a good mood because I know I have you by my side."
    m 1e "I mean what I said."
    m "I love and care for you so much..."
    m 1j "And thank you for caring for me."
    m 1k "Ehehe~"
    return

init 5 python:
    #Push this greeting if it's valentine's day
    if datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0) == valentines_day and not seen_event("monika_valentines_greeting"):
        greetings_list=["monika_valentines_greeting"]

label monika_valentines_greeting:
    m 1j "Hi there, [player]!"
    m 1c "Hmm...?"
    m 1f "What's wrong?"
    m "You seem really glum today."
    m 1g "Is everything alright?"
    m 1o "..."
    m 1l "Cheer up!"
    m 3e "Today's Valentine's day after all."
    m "It's not like you're heartbroken or anything like that right?"
    menu:
        "No":
            m 1j "Great!"
            m 1a "In that case, let's forget about our problems for today, ok?"
            m 3l "I wouldn't want my sweetheart to be sad on such a special occasion."
            m 1 "Today's a day where we celebrate our love for each other, [player]."
            m 1k "So please let me spoil you with my love! Ehehe~"
        "Yes...":
            m 1f "Oh, [player], I'm so sorry to hear that."
            m 1p "Aww man, and on such a special day too..."
            m 1f "If I could, I'd give you a hug right now, and console you."
            m 3f "Please know that I'm here for you!"
            m "No matter how many times you get hurt, I'm always here to fix your heart."
            m 2o "But as much as I love you, [player], don't keep breaking it chasing someone else!"
            m 2e "Your beloved, faithful girlfriend will always be at your side, after all~"
            m 2l "It'll be water under the bridge soon, so no worries."
            m 4 "I'm your one and only!"
            m 1j "So here's to us, for a lovey-dovey, long lasting relationship."
            m 1k "I love you, [player]~!"
    return
