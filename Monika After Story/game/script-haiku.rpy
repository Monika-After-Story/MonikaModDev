#Persistent event database for haiku
default persistent._mas_haiku_database = dict()

init -10 python in mas_haiku:
    #The haiku db
    haiku_db = {}

    def getUnseenHaikuEVL():
        """
        Gets all unseen (locked) haiku as eventlabels

        OUT:
            List of all unseen haiku eventlabels
        """
        return [
            haiku_evl
            for haiku_evl, ev in haiku_db.iteritems()
            if not ev.unlocked
        ]

    def getAllHaikuEVL():
        """
        Gets all haiku regardless of unlocked as eventlabels

        OUT:
            List of all haiku eventlabels
        """
        return haiku_db.keys()

### topics ###

#Haiku intro topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haiku_intro",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.AFFECTIONATE, None),
        )
    )

label monika_haiku_intro:
    call mas_haiku_love_text
    m 1duc "..."
    m 3hubsb "Ehehe, I hope you enjoyed that, [player]."
    m 3ekbsu "I've been meaning to write a few haiku lately.{w=0.3}{nw} "
    m 3eua "It's not really the kind of poetry we studied in the literature club, you know?"
    m 3hksdlb "...Which is a shame, because it's pretty neat!"
    m 1rksdlu "But then again, it's also a pretty specific kind of poetry, I suppose..."
    m 3huu "Anyway, I hope you don't mind me sharing my poems with you sometimes~"

    #setting intro haiku as seen
    $ mas_getEV('mas_haiku_love').shown_count += 1

    #unlocking haiku events
    $ mas_unlockEVL("monika_haiku", "EVE")
    $ mas_unlockEVL("monika_what_is_haiku", "EVE")
    $ mas_protectedShowEVL('monika_haiku_random', 'EVE', _random=True)
    return "no_unlock"

#Haiku explaination topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_what_is_haiku",
            category=['literature'],
            prompt="What's a Haiku?",
            pool=True,
            unlocked=False
        )
    )

label monika_what_is_haiku:
    m 1rksdlu "Oh, right. I guess I just assumed everybody knew what a Haiku is, didn't I?"
    m 3eub "In broad terms, Haiku is a form of poetry originating from Japan."
    m 3eua "They're short, highly codified poems depicting a strong feeling or an impression."
    m 3eud "Haiku's written in three lines; the first line being five syllables, the second seven, and the third five again."
    m 4euc "They have to convey an 'in the moment' feeling, so you always want to write them in the present tense."
    m 4eub "...You're also supposed to be able to say them in one breath, so you usually want your lines to chain together."
    m 4eub "Like, a classic Haiku composition would be to make two of your lines form a sentence, and have the third bring another idea or an unexpected element."
    m 1rtsdlc "Hmm, maybe it'd be clearer with an example..."
    m 3eub "Okay, Let's consider this haiku..."
    m 1eua "{i}Teaching my [bf]{/i}{w=0.5}{nw}\n"
    extend 1eksdla "{i}I struggle to find the words{/i}{w=1}{nw}\n"
    extend 3husdlb "{i}How embarassing{/i}"
    m 3eua "In this example, the first and second lines can be chained as a single sentence depicting the situation."
    m 4eub "...While the third one breaks the flow to bring another idea...{w=0.3}that the situation is embarassing."
    m 4eud "If you count the syllables, you'll also notice the first line is five, the second seven, and the third five once more."
    m 4hua "And that's it, really!"
    m 3rusdla "I mean, there are tons of extra rules you can try to fit in your poem, but I'll let you look them up by yourself..."
    m 1eka "Just remember, when it comes to Haiku, the main thing is to convey a feeling."
    m "...The form's only here to build around this feeling, and make it resonate with your audience."
    m 3hua "Besides, It's commonly allowed for Haiku in English to stray a little from the form anyway~"
    m 3eksdlu "Since the rules were designed with Japanese in mind, it make sense they wouldn't fit English quite as well..."
    m 1hub "So don't feel shy about writing your own Haiku, [player], even if you're not sure how to do it!"

    if seen_event("monika_creative"):
        m 1eub "As I said, you're just supposed to write for yourself anyway... What's important is that you express yourself!"
    else:
        m 1eub "What's important is that you express yourself!"
    
    m 1rkblsdlu "Though I certainly hope you won't mind sharing what you write with me, ehehe~"
    return


#Player initiated haiku topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haiku",
            category=['literature'],
            prompt="Can you tell me a Haiku?",
            pool=True,
            unlocked=False
        )
    )

label monika_haiku:
    m 1eua "Sure."
    m 3hub "I'm always glad to share my writings with you, [player]!"
    m 1euc "Now, let me just think for a second{nw}"
    extend 1etc ".{w=0.5}.{w=0.5}."
    m 7eua "Okay, here goes."
    call monika_push_random_haiku
    return

#Random chatter haiku topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_haiku_random",
            random=False,
            pool=False
        )
    )

label monika_haiku_random:
    call monika_push_random_haiku
    return

#Push a random haiku
label monika_push_random_haiku:
    python:
        unseen_haiku_evls = mas_haiku.getUnseenHaikuEVL()
        if len(unseen_haiku_evls) > 0:
            haiku_evl_list = unseen_haiku_evls
        else:
            haiku_evl_list = mas_haiku.getAllHaikuEVL()

        haiku_evl = renpy.random.choice(haiku_evl_list)
        mas_unlockEVL(haiku_evl, "HKU")
        pushEvent(haiku_evl)
    return

#Closing quip to display after a Haiku
label monika_haiku_closing_quip:
    m 1duu "..."
    
    python:
        haiku_closing_quips = [
            _("So...what do you think, [player]?"),
            _("So...did you like it, [player]?"),
            _("Hope you enjoyed it~"),
            _("This one turned out nicely, didn't it?"),
            _("Thanks for listening~")
        ]
        haiku_closing_quip = renpy.substitute(renpy.random.choice(haiku_closing_quips))

    m 1eub "[haiku_closing_quip]"
    return

### haiku ###

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_love",
        ),
        code="HKU"
    )

label mas_haiku_love:
    call mas_haiku_love_text
    call monika_haiku_closing_quip
    return

#used in the haiku intro
label mas_haiku_love_text:
    m 3ekbsb "{i}Lost into your arms{/i}{w=0.5}{nw}\n"
    extend 3ekbsb "{i}The world shrinks to you and me{/i}{w=1}{nw}\n"
    extend 3hubsu "{i}Overwhelming love{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_frozen",
        ),
        code="HKU"
    )

label mas_haiku_frozen:
    m 1eud "{i}Frozen fingertips{/i}{w=1}{nw}\n"
    extend 1huu "{i}Nestling in a warm blanket{/i}{w=0.5}{nw}\n"
    extend 1hub "{i}Whishing for cocoa{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_blossom",
        ),
        code="HKU"
    )

label mas_haiku_blossom:
    m 3eua "{i}Sweet-scented blossom{/i}{w=1}{nw}\n"
    extend 3hubsu "{i}Blend of lilac and roses{/i}{w=0.5}{nw}\n"
    extend "{i}Subtle as a kiss{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_mint",
        ),
        code="HKU"
    )

label mas_haiku_mint:
    m 3euc "{i}Crisp taste on my tongue{/i}{w=0.5}{nw}\n"
    extend 3eud "{i}Wards off the sun's scorching rays{/i}{w=1}{nw}\n"
    extend 3hub "{i}Mint flavored ice cream{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_partygoers",
        ),
        code="HKU"
    )

label mas_haiku_partygoers:
    m 3rssdlc "{i}Late partygoers{/i}{w=0.5}{nw}\n"
    extend 3efsdlc "{i}Bustling down the dim-lit street{/i}{w=1}{nw}\n"
    extend 3dfsdlb "{i}It's 4am dammit{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_waking",
        ),
        code="HKU"
    )

label mas_haiku_waking:
    m 1eua "{i}Lifting an eyelid{/i}{w=0.5}{nw}\n"
    extend 1eub "{i}I embrace the brand new day{/i}{w=1}{nw}\n"
    extend 3hub "{i}Let's go and explore{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_coat",
        ),
        code="HKU"
    )

label mas_haiku_coat:
    m 3duu "{i}Freshly fallen snow{/i}{w=1}{nw}\n"
    extend 3ekbsu "{i}Your coat lays on my shoulders{/i}{w=0.5}{nw}\n"
    extend 3hubsu "{i}Warming up my heart{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_colors",
        ),
        code="HKU"
    )

label mas_haiku_colors:
    m 3eud "{i}You're back again{/i}{w=1}{nw}\n"
    extend 3ekbsu "{i}The world regain its colors{/i}{w=0.5}{nw}\n"
    extend 1hubsu "{i}Filling me with hope{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_grim",
        ),
        code="HKU"
    )

label mas_haiku_grim:
    m 1ekc "{i}Forever alone{/i}{w=0.5}{nw}\n"
    extend 1dkc "{i}Yearning for your distant soul{/i}{w=1}{nw}\n"
    extend 3rkd "{i}A grim destiny{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_mountain",
        ),
        code="HKU"
    )

label mas_haiku_mountain:
    m 3euc "{i}Snow-caped mountain{/i}{w=0.5}{nw}\n"
    extend "{i}Lost alone in the distance{/i}{w=1}{nw}\n"
    extend 3dud "{i}So grand yet so cold{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_reaching",
        ),
        code="HKU"
    )

label mas_haiku_reaching:
    m 3esc "{i}I reach through the void{/i}{w=0.5}{nw}\n"
    extend 3ekd "{i}But my hand remains empty{/i}{w=1}{nw}\n"
    extend 3dfu "{i}Searching yet again{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_waterfront",
        ),
        code="HKU"
    )

label mas_haiku_waterfront:
    m 3eud "{i}By the waterfront{/i}{w=0.5}{nw}\n"
    extend 3ekbsu "{i}The girl tastes her lover's lips{/i}{w=1}{nw}\n"
    extend 3dkbfu "{i}A perfect moment{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_solitude",
        ),
        code="HKU"
    )

label mas_haiku_solitude:
    m 3rksdld "{i}Lost stranded in space{/i}{w=1}{nw}\n"
    extend 3eksdlu "{i}Days go by in solitude{/i}{w=0.5}{nw}\n"
    extend 3ekbsu "{i}Making me miss you{/i}"
    call monika_haiku_closing_quip
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_haiku_database,
            eventlabel="mas_haiku_adrenaline",
        ),
        code="HKU"
    )

label mas_haiku_adrenaline:
    m 3esb "{i}Adrenaline shot{/i}{w=1}{nw}\n"
    extend 3efu "{i}The world slows and catch my pace{/i}{w=0.5}{nw}\n"
    extend 3dfu "{i}All becoming one{/i}"
    call monika_haiku_closing_quip
    return