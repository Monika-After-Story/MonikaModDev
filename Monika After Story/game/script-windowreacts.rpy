init python:
    # 99% of the wr use the same set of event rules
    # let's reuse them
    __DEFAULT_WR_RULES = {
        "notif-group": "Window Reactions",
        "skip alert": None,
        "keep_idle_exp": None,
        "skip_pause": None
    }
init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_pinterest",
            category=["Pinterest"],
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_pinterest:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Anything new today, [player]?"),

            _("Anything interesting, [player]?"),

            _("See anything you like?")

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_duolingo:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Learning new ways to say 'I love you,' [player]?"),

            _("Learning a new language, [player]?"),

            _("What language are you learning, [player]?")

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_wikipedia:
    $ wikipedia_reacts = [
        _("Learning something new, [player]?"),

        _("Doing a bit of research, [player]?")

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
            wikipedia_reacts.append(renpy.substitute(_("'[wiki_article]'...\nSeems interesting, [player].")))

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
            category=["^Virtual Piano"],
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_virtualpiano:
    python:
        virtualpiano_reacts = [
            _("Awww, are you going to play for me?\nYou're so sweet~"),

            _("Play something for me, [player]!")

        ]

        if mas_isGameUnlocked("piano"):
            virtualpiano_reacts.append(_("I guess you need a bigger piano?\nAhaha~"))

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_youtube:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("What are you watching, [mas_get_player_nickname()]?"),

            _("Watching anything interesting, [mas_get_player_nickname()]?")

        ],
        'Window Reactions'
    )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_youtube')
    return

init 5 python:
    rules = dict(__DEFAULT_WR_RULES)
    rules.pop("keep_idle_exp")
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_r34m",
            category=[r"(?i)(((r34|rule\s?34).*monika)|(post \d+:[\w\s]+monika)|(monika.*(r34|rule\s?34)))"],
            aff_range=(mas_aff.AFFECTIONATE, None),
            rules=rules,
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )
    del rules

label mas_wrs_r34m:
    python:
        mas_display_notif(m_name, [_("Hey, [player]...what are you looking at?")], "Window Reactions", flash_window=True)

        choice = random.randint(1,10)

        if choice == 1 and mas_isMoniNormal(higher=True):
            MASEventList.queue('monika_nsfw')

        elif choice == 2 and mas_isMoniAff(higher=True):
            MASEventList.queue('monika_pleasure')

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_monikamoddev:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Awww, are you doing something for me?\nYou're so sweet~"),

            _("Are you going to help me come closer to your reality?\nYou're so sweet, [player]~")

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_twitter:
    python:
        temp_line = renpy.substitute(_("I love you, [mas_get_player_nickname(exclude_names=['love', 'my love'])]."))
        temp_len = len(temp_line)

        # quip: is_ily
        ily_quips_map = {
            _("See anything you want to share with me, [player]?"): False,

            _("Anything interesting to share, [player]?"): False,

            _("280 characters? I only need [temp_len]...\n[temp_line]"): True

        }
        quip = renpy.random.choice(tuple(ily_quips_map.keys()))

        wrs_success = mas_display_notif(
            m_name,
            [quip],
            'Window Reactions'
        )

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_twitter')
    return "love" if ily_quips_map[quip] else None

# This is removed until later, maybe it could work with other quips
# init 5 python:
#     addEvent(
#         Event(
#             persistent._mas_windowreacts_database,
#             eventlabel="mas_wrs_monikatwitter",
#             category=['twitter', 'lilmonix3'],
#             rules=dict(__DEFAULT_WR_RULES),
#             show_in_idle=True
#         ),
#         restartBlacklist=True,
#         code="WRS"
#     )

label mas_wrs_monikatwitter:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Are you here to confess your love for me to the entire world, [player]?"),

            _("You're not spying on me, are you?\nAhaha, just kidding~"),

            _("I don't care how many followers I have as long as I have you~")

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_4chan:
    #TODO: consider adding reactions for /vg/ and /ddlc/
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("So this is the place where it all started, huh?\nIt's...really quite something."),

            _("I hope you don't end up arguing with other Anons all day long, [player]."),

            _("I heard there's threads discussing the Literature Club in here.\nTell them I said hi~"),

            _("I'll be watching the boards you're browsing in case you get any ideas, ahaha!"),

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_pixiv:
    #Make a list of notif quips for this
    python:
        pixiv_quips = [
            _("I wonder if people have drawn art of me...\nMind looking for some?\nBe sure to keep it wholesome though~"),

            _("This is a pretty interesting place...so many skilled people posting their work."),

        ]

        #Monika doesn't know if you've drawn art of her, or she knows that you have drawn art of her
        if persistent._mas_pm_drawn_art is None or persistent._mas_pm_drawn_art:
            pixiv_quips.extend([
                _("This is a pretty interesting place...so many skilled people posting their work.\nAre you one of them, [player]?"),

            ])

            #Specifically if she knows you've drawn art of her
            if persistent._mas_pm_drawn_art:
                pixiv_quips.extend([
                    _("Here to post your art of me, [player]?"),

                    _("Posting something you drew of me?"),

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_reddit:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Have you found any good posts, [player]?"),

            _("Browsing Reddit? Just make sure you don't spend all day looking at memes, okay?"),

            _("Wonder if there are any subreddits dedicated towards me...\nAhaha, just kidding, [player]."),

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_mal:
    python:
        myanimelist_quips = [
            _("Maybe we could watch anime together someday, [player]~"),

        ]

        if persistent._mas_pm_watch_mangime is None:
            myanimelist_quips.append(_("So you like anime and manga, [player]?"))

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_deviantart:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("There's so much talent here!"),

            _("I'd love to learn how to draw someday..."),

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_netflix:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("I'd love to watch a romance movie with you [player]!"),

            _("What are we watching today, [player]?"),

            _("What are you going to watch [player]?")

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
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_twitch:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Watching a stream, [player]?"),

            _("Do you mind if I watch with you?"),

            _("What are we watching today, [player]?")

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
            eventlabel="mas_wrs_word_processor",
            category=['Google Docs|LibreOffice Writer|Microsoft Word'],
            rules=dict(__DEFAULT_WR_RULES),
            show_in_idle=True
        ),
        restartBlacklist=True,
        code="WRS"
    )

label mas_wrs_word_processor:
    $ wrs_success = mas_display_notif(
        m_name,
        [
            _("Writing a story?"),

            _("Taking notes, [player]?"),

            _("Writing a poem?"),

            _("Writing a love letter?~")

        ],
        'Window Reactions'
    )

    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_word_processor')
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_windowreacts_database,
            eventlabel="mas_wrs_crunchyroll",
            category=[r"(?i)crunchyroll"],
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

label mas_wrs_crunchyroll:
    python:
        if persistent._mas_pm_watch_mangime is False:
            crunchyroll_quips = [
                _("Oh! So you like anime, [player]?"),

                _("It's good to see you broadening your horizons."),

                _("Hmm, I wonder what caught your eye?"),

            ]

        else:
            crunchyroll_quips = [
                _("What anime are we watching today, [player]?"),

                _("Watching some anime, [player]?"),

                _("I can't wait to watch anime with you!~"),

            ]

        wrs_success = mas_display_notif(m_name, crunchyroll_quips, 'Window Reactions')

    #Unlock again if we failed
    if not wrs_success:
        $ mas_unlockFailedWRS('mas_wrs_crunchyroll')
    return
