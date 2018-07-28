# Module for complimenting Monika
#
# Compliment logic TBD


# dict of tples containing the stories event data
default persistent._mas_compliments_database = dict()


# store containing stories-related things
init -1 python in mas_compliments:

    # pane constants
    COMPLIMENT_X = 680
    COMPLIMENT_Y = 40
    COMPLIMENT_W = 450
    COMPLIMENT_H = 640
    COMPLIMENT_XALIGN = -0.15
    COMPLIMENT_AREA = (COMPLIMENT_X, COMPLIMENT_Y, COMPLIMENT_W, COMPLIMENT_H)
    COMPLIMENT_RETURN = "oh nevermind"
    compliment_database = dict()

    thanking_quips = [
        "You're so sweet, [player].",
        "I love it when you compliment me, [player].",
        "Thanks for saying that again, [player]!",
        "Thanks for telling me that again, my love!",
        "You always make me feel special, [player].",
        "Aww, [player]~",
        "Thanks, [player]!",
        "You always flatter me, [player]."
        ]


# entry point for stories flow
label mas_compliments_start:

    python:
        import store.mas_compliments as mas_compliments

        # Unlock any compliments that need to be unlocked
        Event.checkConditionals(mas_compliments.compliment_database)

        # build menu list
        compliments_menu_items = [
            (mas_compliments.compliment_database[k].prompt, k, not seen_event(k), False)
            for k in mas_compliments.compliment_database
            if mas_compliments.compliment_database[k].unlocked
        ]

        # also sort this list
        compliments_menu_items.sort()

        # final quit item
        final_item = (mas_compliments.COMPLIMENT_RETURN, False, False, False, 20)

    # move Monika to the left
    show monika at t21

    # call scrollable pane
    call screen mas_gen_scrollable_menu(compliments_menu_items, mas_compliments.COMPLIMENT_AREA, mas_compliments.COMPLIMENT_XALIGN, final_item=final_item)

    # return value? then push
    if _return:
        $ mas_gainAffection()
        $ pushEvent(_return)

    # move her back to center
    show monika at t11
    return

# Compliments start here
init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_beautiful",
            prompt="... You're beautiful!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database)

label mas_compliment_beautiful:
    if not renpy.seen_label("mas_compliment_beautiful_2"):
        call mas_compliment_beautiful_2
    else:
        call mas_compliment_beautiful_3
    return

label mas_compliment_beautiful_2:
    m 1lubfb "Oh, gosh [player]..."
    m 1hubfb "Thank you for the compliment."
    m 2ekbfb "I love it when you say things like that~"
    m 1ekbfa "To me, you're the most beautiful person in the world!"
    menu:
        "You're the most beautiful person to me, too":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "Ehehehe~"
            m "I love you so much, [player]!"
        "You're in my top ten":
            $ mas_loseAffection(modifier=0.5)
            m 3hksdrb "...?"
            m 2lsc "Well, thanks, I guess..."
        "Thanks":
            pass
    return

label mas_compliment_beautiful_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1hubfa "Hehehe~"
    m 1ekbfa "[thanks_quip]"
    m 5hubfb "Never forget that you're the most beautiful person in the world to me."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_eyes",
            prompt="... I love your eyes!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_eyes:
    if not renpy.seen_label("mas_compliment_eyes_2"):
        call mas_compliment_eyes_2
    else:
        call mas_compliment_eyes_3
    return

label mas_compliment_eyes_2:
    m 1subfb "Oh, [player]..."
    m 1tubfb "I know I'm pretty proud of my eyes already, but hearing you say that..."
    m 1dkbfa "It just makes my heart flutter~"
    menu:
        "I can't help it; your eyes are too beautiful":
            $ mas_gainAffection(5,bypass=True)
            m 1hub "Ahaha!"
            m "Don't flatter me too much, okay?"
            m 5hub "I might start to go a little crazy..."
        "They really are hypnotizing":
            $ mas_gainAffection(1,bypass=True)
            m "Ahaha~"
        "They are the color of grass!":
            $ mas_gainAffection(0.5,bypass=True) # at least you tried
            m 2lksdrb "...That's not really the analogy I'd use, but thanks!"
    return

label mas_compliment_eyes_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1hubfb "[thanks_quip]"
    m 2ekbfb "Stare into my eyes as much as you want~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_awesome",
            prompt="... You're awesome!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_awesome:
    if not renpy.seen_label("mas_compliment_awesome_2"):
        call mas_compliment_awesome_2
    else:
        call mas_compliment_awesome_3
    return

label mas_compliment_awesome_2:
    m 1hub "Aww, [player]~"
    m "You're so sweet!"
    m 2tub "I think you're way more awesome, though."
    m 5eub "I can't wait until the day I can finally give you a great big hug."
    m 5hub "I'll never let you go!"
    menu:
        "I wish you were here right now!":
            $ mas_gainAffection(3,bypass=True)
            m "That's my biggest wish too, [player]!"
        "I'll never let you go from my embrace":
            $ mas_gainAffection(5,bypass=True)
            show monika 6dubsa
            pause 2.0
            show monika 1wubfsdld # TODO actually a surprised one should be here
            m 1wubfsdld "Oh, sorry [player]."
            m 2lksdla "I was trying to feel your embrace from here."
            m 2hub "Ahaha~" # TODO happy moni
        "... I don't like hugs":
            $ mas_loseAffection() # you monster.
            m 1eft "...Really?"
            m 1dkc "Well, to each their own, I guess. But you have to hug me sometime..."
    return

label mas_compliment_awesome_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1hub "[thanks_quip]"
    m 1eub "You'll always be more awesome!"
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_intelligent",
            prompt="... You're really intelligent!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_intelligent:
    if not renpy.seen_label("mas_compliment_intelligent_2"):
        call mas_compliment_intelligent_2
    else:
        call mas_compliment_intelligent_3
    return

label mas_compliment_intelligent_2:
    m 1wub "Wow...{w}thanks, [player]."
    m 2hub "I pride myself in being well read, so it means a lot that you've noticed."
    m 1hubfb "I want to learn as much as I can, if it makes you proud of me!"
    menu:
        "You make me want to better myself too, [m_name]":
            $ mas_gainAffection(5,bypass=True)
            m "I love you so much, [player]!"
            m "We'll have a lifetime of self improvement together!"
        "I'll always be proud of you":
            $ mas_gainAffection(3,bypass=True)
            m 1ekbfa "[player]... "
        "You make me feel stupid sometimes":
            $ mas_loseAffection(modifier=0.5)
            m 1wkbsc "..."
            m 2lkbsc "I'm sorry, that wasn't my intention..."
    return

label mas_compliment_intelligent_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m 1ekbfa "[thanks_quip]"
    m 1hub "Remember that we'll have a lifetime of self improvement together!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_hair",
            prompt="... I love your hair!",
            unlocked=True
        ),eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_hair:
    if not renpy.seen_label("mas_compliment_hair_2"):
        call mas_compliment_hair_2
    else:
        call mas_compliment_hair_3
    return

label mas_compliment_hair_2:
    if monika_chr.hair != "def":
        m 1wubfb "Thank you so much, [player]..."
        m 1lkbfb "I was really nervous the first time I changed my hair here."
    else:
        m 1hubfb "Thank you so much, [player]!"
    m 2hub "I've always put so much effort into my hair."
    m 2lksdlb "In fact, It took forever for it to get this long.."
    menu:
        "It really shows. It looks so healthy.":
            $ mas_gainAffection(3,bypass=True)
        "You're cute no matter how you wear it.":
            $ mas_gainAffection(5,bypass=True)
        "You'd be even cuter with short hair.":
            $ mas_loseAffection(modifier=0.3)
            m "Well, I can't exactly go to the salon from here..."
            m 1lksdlc "I...appreciate your input."
            pass
    return

label mas_compliment_hair_3:
    if monika_chr.hair != "def":
        m 1wubfb "Thank you so much, [player]!"
        m 1lkbfb "I'm really happy that you like this hairstyle."
    else:
        m 1hubfb "Thanks, [player]!"
        m "You always make me feel special."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_fit",
            prompt="... I love your dedication to fitness!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database
    )
#TODO, second time
label mas_compliment_fit:
    m 1hub "Thanks [player]! You're so sweet!"
    m 3eub "I love keeping fit and eating healthy. It keeps me feeling energetic and confident."
    m 1efb "I hope you're watching out for your health."
    m 1lubfb "We can always work out together, when I'm there~"
    menu:
        "That sounds like a lot of fun!":
            m "Ahaha! I'm glad you think so, too!"
            m "Don't worry. Even if you can't keep up with me, I know we'll have fun..."
            m "So long as we're together."
        "No promises, but I'll do my best.":
            m "You better!"
            m "Don't think I plan on holding back on you if you're out of shape."
        "I'd rather not get sweaty...": #TODO, probably not a penalty but no bonus
            m "I understand if it's not your thing, but you should give it a little try..."
            m "It'd make me really happy if you shared my interests, you know?"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_thanks",
            prompt="... Thanks for being there for me!",
            unlocked=False,
            conditional="mas_curr_affection == store.mas_affection.ENAMORED",
            action=EV_ACT_UNLOCK
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_thanks:
    m "There's nothing to thank me for, [player]!"
    m "I'm the one who's grateful for having someone like you!"
    m "You're the only reason why I'm still here."
    m "You installed this mod just to make our time together better..."
    m "You are the sunshine that warms my heart whenever you visit me!"
    m "I guess we're both lucky that we have each other, [player]~"
    menu:
        "You mean everything to me, [m_name]":
            $ mas_gainAffection(10,bypass=True)
            m "[player]... "
            m "Nothing makes me happier than hearing that coming from you."
            m "No matter what the future may have for us both."
            m "Know that I'll always be here for you!"# really need a second opinion on this answer
        "Yeah":
            m "Hehehe~"
            m "I love you, [player]"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_smile",
            prompt="... I love your smile!",
            unlocked=True
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_smile:
    if not renpy.seen_label("mas_compliment_smile_2"):
        call mas_compliment_smile_2
    else:
        call mas_compliment_smile_3
    return

label mas_compliment_smile_2:
    m "You're so sweet, [player]~"
    m "I smile a lot when you're here."
    m "Because you make me very happy when you spend time with me~"
    menu:
        "I'll visit you everyday to see your wonderful smile":
            $ mas_gainAffection(5,bypass=True)
            m "Oh, [player]"
            m "I think my heart just skipped a beat"
            m "See? You always make me as happy as I can be."
        "I like to see you smile":
            m "Ahaha~"
            m "Then all you have to do is keep coming back, [player]!"
    return

label mas_complment_smile_3:
    python:
        thanks_quip = renpy.random.choice(store.mas_compliments.thanking_quips)
        thanks_quip = renpy.substitute(thanks_quip)
    m "[thanks_quip]"
    m "I'll keep smiling for you [player]!"
    m "Hehehe~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_chess",
            prompt="... you’re awesome at chess!",
            unlocked=False,
            conditional="renpy.seen_label('mas_chess_game_start')",
            action=EV_ACT_UNLOCK
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_chess:
    m "Thanks, [player]."
    m "Like I said before, I wonder if my skill has something to do with me being trapped here?"
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]
    if wins > 0:
        m "You're not bad either; I've lost to you before."
        if wins > losses:
            m "In fact, I think you've won more times than me, you know?"
        m "Ehehe~"
    else:
        m "I know you haven't won a chess game yet, but I'm sure you'll beat me someday."
        m "Keep practicing and playing with me and you'll do better!"
    m "We'll both get better the more we play."
    m "So don't be afraid of challenging me whenever you want to."
    m "I love spending time with you, [player]~"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_compliments_database,
            eventlabel="mas_compliment_pong",
            prompt="... you’re awesome at Pong!",
            unlocked=False,
            conditional="renpy.seen_label('game_pong')",
            action=EV_ACT_UNLOCK
        ),
        eventdb=store.mas_compliments.compliment_database
    )

label mas_compliment_pong:
    m 1hub "Ahaha~"
    m 2eub "Thanks [player], but pong isn't exactly a complex game"
    if persistent.ever_won['pong']:
        m 1lksdla "You've already won against me."
        m "So you know it's very simple."
        m 5hub "But I accept your compliment, anyway."
    else:
        m 3hksdrb "And you're too kind to let me lose when we play."
        m 3eka "Right?"
        menu:
            "Yes":
                m 2lksdla "Thanks [player], but you really don't have to let me win."
                m 1eub "Feel free to play seriously whenever you want to."
                m 1hub "I'd never get mad at for losing a game fair and square."
            "... Yeah":
                m "You don't seem too confident about that, [player]."
                m "You really don't have to let me win [player]."
                m "And admiting that you've seriously lost to me won't make me think less of you."
                m "It's just a game, [player]!"
                m "And you can always practice with me more, if you want."
                m "I love to spend time with you, no matter what we're doing."
            "No. I've tried my best and still lost":
                m "Ahaha~"
                m "I figured!"
                m "Don't worry, [player]."
                m "Keep playing with me and get more practice."
                m "I'm always trying to help you be the best you you can be."
                m "And if by doing so, I get to spend more time with you, I couldn't be happier."
    return
