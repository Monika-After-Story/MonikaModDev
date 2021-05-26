init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=["Pinterest"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["Duolingo"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["- Wikipedia"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
        wind_name = mas_getActiveWindowHandle()
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
            category=["Virtual Piano"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["- YouTube"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=[r"(?i)(((r34|rule\s?34).*monika)|(post \d+:[\w\s]+monika)|(monika.*(r34|rule\s?34)))"],
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "skip_pause": None
            },
            show_in_idle=True
        ),
        code="WRS"
    )

label mas_wrs_r34m:
    python:
        mas_display_notif(m_name, ["Hey, [player]...what are you looking at?"],'Window Reactions')

        choice = random.randint(1,10)

        if choice == 1 and mas_isMoniNormal(higher=True):
            queueEvent('monika_nsfw')

        elif choice == 2 and mas_isMoniAff(higher=True):
            queueEvent('monika_pleasure')

        else:
            if mas_isMoniEnamored(higher=True):
                if choice < 4:
                    exp_to_force = "1rsbssdlu"
                elif choice < 7:
                    exp_to_force = "2tuu"
                else:
                    exp_to_force = "2ttu"
            else:
                if choice < 4:
                    exp_to_force = "1rksdlc"
                elif choice < 7:
                    exp_to_force = "2rssdlc"
                else:
                    exp_to_force = "2tssdlc"

            mas_moni_idle_disp.force_by_code(exp_to_force, duration=5)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_monikamoddev",
            category=["MonikaModDev"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["/ Twitter"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["- 4chan"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["- pixiv"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=[r"(?i)reddit"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["MyAnimeList"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["DeviantArt"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["Netflix"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["- Twitch"],
            rules={
                "notif-group": "Window Reactions",
                "skip alert": None,
                "keep_idle_exp": None,
                "skip_pause": None
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
            category=["- Visual Studio Code"],
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
            eventlabel="mas_wrs_picrew",
            category=["Picrew"],
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
            category=["- Notepad++"],
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
            category=["Facebook"],
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
            category=["Instagram"],
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
            category=["- Aseprite"],
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
            category=["Steam"],
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
            category=["Spotify"|"iTunes"],
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
            eventlabel="mas_wrs_ddlcstore",
            category=["Doki Doki Literature Club Store"],
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
            category=["| Indeed"],
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
            category=["Doki Doki Literature Club!"],
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
            category=["Monika After Story - home"],
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
            category=["| eBay"|"Amazon.com"],
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
            eventlabel="mas_wrs_newgrounds",
            category=["Newgrounds"],
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
            category=["- Word"],
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
            category=["- PowerPoint"],
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
            category=["- Excel"],
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
            category=["- Access"],
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
            category=["- Publisher"],
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
            category=["- OneNote"],
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
            category=["FL Studio"],
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
            category=["SoundCloud"],
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
            category=["| Library of Congress"],
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
            category=["— Kickstarter"],
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
            category=["Patreon"],
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
            category=["Urban Dictionary"],
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
            category=["Python.org"],
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
            eventlabel="mas_wrs_adobepro",
            category=["Premiere Pro"],
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
            category=["Photoshop"],
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
            eventlabel="mas_wrs_camera",
            category=["Camera"],
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
            eventlabel="mas_wrs_netscape",
            category=["Welcome to Netscape!"],
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
            category=["Unity"],
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
            category=["GameMaker Studio 2"],
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
            category=["Source Filmmaker"],
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
            eventlabel="mas_wrs_unreal",
            category=["Unreal Engine"],
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
            category=["DOSBox"],
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
            category=["VirtualBox"],
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
            category=["GIMP"],
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
            category=["Task Manager"],
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
            category=["The Ren'py Visual Novel Engine"],
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
            category=["Microsoft Solitaire Collection"],
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
            category=["TikTok"],
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
           "Hmmm, there's a lot of creative stuff being made here.\nDo you make content on here, [player]?", 
           "If I ever got on here, I bet you'd follow me in a heartbeat. Ehehe~"
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
            eventlabel="mas_wrs_whatsapp",
            category=["WhatsApp"],
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
            category=["Paint 3D"],
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
            category=["Cortana"],
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
            category=["Microsoft Teams"],
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
