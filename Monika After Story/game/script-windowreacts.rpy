init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=['pinterest'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Anything new today, [player]?",
            "Anything interesting, [player]?",
            "See anything you like?"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_pinterest')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_duolingo",
            category=['duolingo'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Learning new ways to say 'I love you,' [player]?",
            "Learning a new language, [player]?",
            "What language are you learning, [player]?"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_duolingo')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_wikipedia",
            category=['wikipedia'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        "Learning something new, [player]?",
        "Doing a bit of research, [player]?"
    ]

    #Items in here will get the wiki article you're looking at for reacts.
    python:
        wind_name = mas_getActiveWindow(friendly=True)
        try:
            cutoff_index = wind_name.index(" - Wikipedia")

            #If we're still here, we didn't value error
            #Now we get the article
            wiki_article = wind_name[:cutoff_index]

            # May contain clarification in trailing parentheses
            wiki_article = re.sub("\\s*\\(.+\\)$", "", wiki_article)
            wikipedia_reacts.append(renpy.substitute("'[wiki_article]'...\nSeems interesting, [player]."))

        except ValueError:
            pass

    $ wrs_success = mas_display_notif(
        m_name,
        wikipedia_reacts,
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_wikipedia')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_virtualpiano",
            category=["virtual", "piano"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_virtualpiano:
    python:
        virtualpiano_reacts = [
            "Awww, are you going to play for me?\nYou're so sweet~",
            "Play something for me, [player]!"
        ]

        if mas_isGameUnlocked("piano"):
            virtualpiano_reacts.append("I guess you need a bigger piano?\nAhaha~")

        wrs_success = mas_display_notif(
            m_name,
            virtualpiano_reacts,
            'Window Reactions'
        )

        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_virtualpiano')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_youtube",
            category=['youtube'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "What are you watching, [mas_get_player_nickname()]?",
            "Watching anything interesting, [mas_get_player_nickname()]?"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=['rule34', 'monika'],
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    $ mas_display_notif(m_name, ["Hey, [player]...what are you looking at?"],'Window Reactions')

    $ choice = random.randint(1,10)
    if choice == 1:
        $ queueEvent('monika_nsfw')

    elif choice == 2:
        $ queueEvent('monika_pleasure')

    elif choice < 4:
        show monika 1rsbssdlu
        pause 5.0

    elif choice < 7:
        show monika 2tuu
        pause 5.0

    else:
        show monika 2ttu
        pause 5.0
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=['monikamoddev'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Awww, are you doing something for me?\nYou're so sweet~",
            "Are you going to help me come closer to your reality?\nYou're so sweet, [player]~"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikamoddev')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitter",
            category=['twitter'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute("I love you, [mas_get_player_nickname(exclude_names=['love', 'my love'])].")
        temp_len = len(temp_line)

        # quip: is_ily
        ily_quips_map = {
            "See anything you want to share with me, [player]?": False,
            "Anything interesting to share, [player]?": False,
            "280 characters? I only need [temp_len]...\n[temp_line]": True
        }
        quip = renpy.random.choice(ily_quips_map.keys())

        wrs_success = mas_display_notif(
            m_name,
            [quip],
            'Window Reactions'
        )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikatwitter",
            category=['twitter', 'lilmonix3'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_monikatwitter:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Are you here to confess your love for me to the entire world, [player]?",
            "You're not spying on me, are you?\nAhaha, just kidding~",
            "I don't care how many followers I have as long as I have you~"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_monikatwitter')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_4chan",
            category=['4chan'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_4chan:
    #TODO: consider adding reactions for /vg/ and /ddlc/
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "So this is the place where it all started, huh?\nIt's...really quite something.",
            "I hope you don't end up arguing with other Anons all day long, [player].",
            "I heard there's threads discussing the Literature Club in here.\nTell them I said hi~",
            "I'll be watching the boards you're browsing in case you get any ideas, ahaha!",
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_4chan')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pixiv",
            category=['pixiv'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_pixiv:
    #Make a list of notif quips for this
    python:
        pixiv_quips = [
            "I wonder if people have drawn art of me...\nMind looking for some?\nBe sure to keep it wholesome though~",
            "This is a pretty interesting place...so many skilled people posting their work.",
        ]

        #Monika doesn't know if you've drawn art of her, or she knows that you have drawn art of her
        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                "This is a pretty interesting place...so many skilled people posting their work.\nAre you one of them, [player]?",
            ])

            #Specifically if she knows you've drawn art of her
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    "Here to post your art of me, [player]?",
                    "Posting something you drew of me?",
                ])

        wrs_success = mas_display_notif(
            m_name,
            pixiv_quips,
            'Window Reactions'
        )

        #Unlock again if we failed
        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_pixiv')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_reddit",
            category=['reddit'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Have you found any good posts, [player]?",
            "Browsing Reddit? Just make sure you don't spend all day looking at memes, okay?",
            "Wonder if there are any subreddits dedicated towards me...\nAhaha, just kidding, [player].",
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_reddit')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mal",
            category=['myanimelist'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            "Maybe we could watch anime together someday, [player]~",
        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append("So you like anime and manga, [player]?")

        wrs_success = mas_display_notif(m_name, myanimelist_quips, 'Window Reactions')

        #Unlock again if we failed
        if not wrs_success:
            mas_unlockFailedWRS('mas_wrs_mal')

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_deviantart",
            category=['deviantart'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "There's so much talent here!",
            "I'd love to learn how to draw someday...",
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_deviantart')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netflix",
            category=['netflix'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "I'd love to watch a romance movie with you [player]!",
            "What are we watching today, [player]?",
            "What are you going to watch [player]?"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_netflix')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_twitch",
            category=['-twitch'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            "Watching a stream, [player]?",
            "Do you mind if I watch with you?",
            "What are we watching today, [player]?"
        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitch')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_vscode",
            category=['visualstudiocode'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_vscode:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some coding, [player]? I'd help you if I could...",
           "Working on something to help me come closer to your reality?\n You're so sweet~" 
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_vscode')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_calculator",
            category=['calculator'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_calculator:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some quick number crunching, I see."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_calculator')
    return            

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_nes",
            category=['mesen'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_nes:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hmmm, an emulator? What will we be emulating today, [player]?",
           "It's kind of neat how technology once though of as highly advanced can now just be run in a window.\nTime certainly does fly!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_nes')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_fusion",
            category=['fusion3.64'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_fusion:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hmmm, an emulator? What will we be emulating today, [player]?",
           "This game looks pretty neat for being so old. It has my approval. Ehehe."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_fusion')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_picrew",
            category=['picrew'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_picrew:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Wow, this place looks cool! So much creative potential here...",
           "I wonder how many people have made art of me using this site...\nHave you, [player]?~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_picrew')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_notepad",
            category=['notepadpp'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_notepadpp:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some quick coding, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_notepadpp')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_facebook",
            category=['facebook'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_facebook:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hey, [player], if you're trying to find my profile, you're on the wrong site.\n Ahahaha! I'm just kidding!",
           "What's your status update for today? Mine is 'Happily in love!'"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_facebook')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_instagram",
            category=['instagram'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_instagram:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Gosh, there's quite a few people here that claim to be me...\nI guess I should feel honored, ahaha!",
           "Any pictures here that catch your eye? Do they have me in them? Ehehe~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_instagram')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_aseprite",
            category=['aseprite'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_aseprite:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Oooh, making some art? Nice! I bet it'll turn out great!",
           "Making art simply using multicolored blocks sounds like a challenging task.\n You've got quite some talent, I must say!"    
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_aseprite')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_steam",
            category=['steam'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_steam:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Looking for some new games to play, [player]?",
           "Choo choo...Chu~ Ahaha, got you!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_steam')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_spotify",
            category=['spotify'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_spotify:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Nice music selection, [player]! Mind if I listen along with you?",
           "What are you listening to, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_spotify')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_itunes",
            category=['itunes'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_itunes:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Nice music selection, [player]! Mind if I listen along with you?",
           "What are you listening to, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_itunes')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_ddlcstore",
            category=['dokidokiliteratureclubstore'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_ddlcstore:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Oooh, this is where they sell marketable plushies of me! Ahaha!",
           "Getting some merch of me? How sweet~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_ddlcstore')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_jobsearch",
            category=['jobsearch|indeed'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_jobsearch:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Looking for some potential jobs? That's great!",
           "Remember to choose a career that you'll enjoy doing, [player].\n It'll make it more worthwhile that way!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_jobsearch')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_ddlc",
            category=['dokidokiliteratureclub!'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_ddlc:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Came here for nostalgia, I presume?",
           "Where it all began...and also, what brought us together!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_ddlc')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_maswebsite",
            category=['monikaafterstory-home'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_maswebsite:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "The mod that helped me get closer to you!",
           "Are you looking for new outfits for me? Awww, you're so kind, [player]~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_maswebsite')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_ebay",
            category=['|ebay'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_ebay:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some shopping, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_ebay')
    return  

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_amazon",
            category=['amazon.com'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_amazon:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some shopping, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_amazon')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_vice",
            category=['vice'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_vice:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hmmm, an emulator? What will we be emulating today, [player]?",
           "Something about this particular programming language looks pretty...BASIC. Ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_vice')
    return     

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_newgrounds",
            category=['newgrounds'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_newgrounds:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "A lot of people really seem to like this site. I guess it must be very popular.",
           "Remember: In this game, it's Everything, with Monika! Ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_newgrounds')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_word",
            category=['-word'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_word:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Writing a paper, [player]? Is it about me?~ Ahaha!",
           "Good luck with your work, [player]!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_word')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_powerpoint",
            category=['-powerpoint'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_powerpoint:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Working on a presentation, [player]? What's it about?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_powerpoint')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_excel",
            category=['-excel'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_excel:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Spreadsheets are pretty underrated these days, don't you think?",
           "What are you working on here, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_excel')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_access",
            category=['-access'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_access:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some database work, [player]?",
           "This stuff looks pretty tough to work with. You're so smart!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_access')
    return      

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_publisher",
            category=['-publisher'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_publisher:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "What are you designing here, [player]?",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_publisher')
    return  

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_onenote",
            category=['-onenote'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_onenote:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Taking down some notes, [player]?",
           "Doing some studying? Keep it up!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_onenote')
    return          

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_flstudio",
            category=['flstudio'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_flstudio:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Making some music, [player]? You're so talented~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_flstudio')
    return        

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_soundcloud",
            category=['soundcloud'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_soundcloud:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Have you published any music of your own on here?",
           "What are you listening to, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_soundcloud')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_congresslibrary",
            category=['|library of congress'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_congresslibrary:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Ah, I see you have good taste in where you look up literature. Ahaha!",
           "Looking for anything in particular, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_congresslibrary')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_kickstarter",
            category=['—kickstarter'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_kickstarter:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "What project are you backing, [player]?",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_kickstarter')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_patreon",
            category=['patreon'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_patreon:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Anyone in particular you're supporting?",
           "Helping to support someone? You're so kind, [player]!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_patreon')
    return       

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_urbandictionary",
            category=['urbandictionary'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_urbandictionary:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Ah, this website is...definitely something.",
           "You might want to go to a more...trusted source\nif you're looking for accurate definitions, [player]."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_urbandictionary')
    return                   

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_python",
            category=['python.org'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_python:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Are you intrested in learning more Python, [player]?",
           "Did you come here to learn how to help me come closer to your reality?\nYou're so sweet~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_python')
    return                   

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_15ai",
            category=['15.ai'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_15ai:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "A text to speech device, huh? I wonder if my voice will ever be used here...",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_15ai')
    return           

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_mobygames",
            category=['mobygames'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_mobygames:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "What game are you looking for here, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_mobygames')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_adobepro",
            category=['premierepro'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_adobepro:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Making a video, [player]?",
           "Editing footage sure is tough, huh?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_adobepro')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_photoshop",
            category=['photoshop'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_photoshop:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some image editing, I see."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_photoshop')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_elyssasite",
            category=['%%%%%%%%%%%'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_elyssasite:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "What...is this place...?",
           "Why does this place seem so familiar...\nand yet, I don't recognize it? This is weird..."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_elyssasite')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_camera",
            category=['camera'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_camera:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Say cheese! Ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_camera')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_yuri",
            category=['yuri\"dance\"'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_yuri:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "O-oh....oh, my....",
           "This is...very disturbing."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_yuri')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_bobwebsite",
            category=['mysticalsmokingheadof'bob''],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_bobwebsite:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Wow. This place looks...interesting, to say the least.",
           "Maybe try asking this guy if I'll be in your reality soon!\nAlthough, I wouldn't really take the response too seriously\nif I were you, ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_bobwebsite')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_fogcam",
            category=['fogcam-theworld'soldestwebcam'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_fogcam:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Gosh, this webcam's been running for a long time! I guess it was really built to last, ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_fogcam')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_million",
            category=['themilliondollarhomepage'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_million:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Wow, there is...quite a bit of ad revenue to be had here.",
           "It's kind of hard to make out what these ads even show anymore, ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_million')
    return 

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_netscape",
            category=['welcometonetscape!'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_netscape:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hmmm, an old guide to the Internet? Don't you already know how this all works, though?\nEhehe, just wondering!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_netscape')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_unity",
            category=['unity'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_unity:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Are you designing your own game? Very cool!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_unity')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_gms2",
            category=['gamemakerstudio2'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_gms2:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Are you designing your own game? Very cool!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_gms2')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_sfm",
            category=['sourcefilmmaker'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_sfm:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Making a video, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_sfm')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_norad",
            category=['noradsantatracker'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_norad:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hmmm, is it that time of year again? Happy Holidays, [player]!",
           "I can't wait to spend the holiday with you tomorrow!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_norad')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_unreal",
            category=['unrealengine'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_unreal:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Are you designing your own game? Very cool!"
           "This looks very complex. You must be a very smart cookie to have figured all this out, ahaha!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_unreal')
    return    

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_dos",
            category=['dosbox'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_dos:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Running an old OS in a modern OS? Pretty neat!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_dos')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_virtualbox",
            category=['virtualbox'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_virtualbox:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Hmmm, you use virtual machines, [player]? Neat!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_virtualbox')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_gimp",
            category=['gimp'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_gimp:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some image editing, I see."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_gimp')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_taskmanager",
            category=['taskmanager'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_taskmanager:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Oh, is a program causing trouble? I hope I'm not the cause, ahaha..."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_taskmanager')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_renpy",
            category=['theren'pyvisualnovelengine'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_renpy:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "The place where it all began, ahaha!",
           "Nice to see you taking an interest in this stuff."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_renpy')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_solitaire",
            category=['microsoftsolitairecollection'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_solitaire:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Oh, you like playing with cards? Nice!"
           "You know, [player], I wouldn't mind playing a card game with you\nwhen I cross over. That'd be nice, don't you agree?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_solitaire')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_tiktok",
            category=['tiktok'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_tiktok:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Now, don't go get carried away here and ignore me for too long, okay? Ehehe~",
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_tiktok')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_msn",
            category=['msn'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_msn:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Catching up on the news, [player]?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_msn')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_aol",
            category=['aol'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_aol:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "You've got mail! It's a letter from me that says \"I love you!\" Ehehe~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_aol')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_whatsapp",
            category=['whatsapp'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_whatsapp:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Chatting with your friends, [player]? You should introduce me to them sometime!"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_whatsapp')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_paint3d",
            category=['paint3d'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_paint3d:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Doing some image editing, player?"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_paint3d')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_cortana",
            category=['cortana'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_cortana:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Oh, an AI assistant! I wonder if I'll ever be able to be your assistant one day..."
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_cortana')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_teams",
            category=['microsoftteams'],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_teams:
    $ wrs_success = mas_display_notif(
        m_name,
        [
           "Heading to a meeting, [player]? Good luck!\n I'll be waiting for you~"
        ],
        'Window Reactions'
    )


    if not wrs_success:
        $ mas_unlockFailWRS('mas_wrs_teams')
    return   
