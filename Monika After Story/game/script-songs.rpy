default persistent._mas_songs_database = dict()

init -10 python in mas_songs:
    # Event database for songs
    song_db = {}

    #Song type constants
    #NOTE: TYPE_SHORT will never be picked in the random delegate, these are filters for that
    #TYPE_LONG songs should either be unlocked via a 'preview' song of TYPE_SHORT or (for ex.) some story event
    #TYPE_LONG songs would essentially be songs longer than 10-15 lines
    #NOTE: TYPE_LONG songs must have the same label name as their short song counterpart with '_long' added to the end so they unlock correctly
    #Example: the long song for short song mas_song_example would be mas_song_example_long
    TYPE_LONG = "long"
    TYPE_SHORT = "short"

init python in mas_songs:
    import store
    def checkRandSongDelegate():
        """
        Checks if we have random songs available, and if so unlocks the random delegate if locked
        """
        #Get ev
        rand_delegate_ev = store.mas_getEV("monika_sing_song_random")

        if rand_delegate_ev and not rand_delegate_ev.random and hasRandomSongs():
            rand_delegate_ev.random = True

    def getUnlockedSongs(length=None):
        """
        Gets a list of unlocked songs
        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)
        OUT: list of unlocked all songs of the desired length in tuple format for a scrollable menu
        """
        if length is None:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked
            ]

        else:
            return [
                (ev.prompt, ev_label, False, False)
                for ev_label, ev in song_db.iteritems()
                if ev.unlocked and length in ev.category
            ]

    def getRandomSongs():
        """
        Gets a list of all random songs

        OUT: list of all random songs within aff_range
        """
        return [
            ev_label
            for ev_label, ev in song_db.iteritems()
            if ev.random and TYPE_SHORT in ev.category and ev.checkAffection(store.mas_curr_affection)
        ]

    def hasUnlockedSongs(length=None):
        """
        Checks if the player has unlocked a song at any point via the random selection

        IN:
            length - a filter for the type of song we want. "long" for songs of TYPE_LONG
                "short" for TYPE_SHORT or None for all songs. (Default None)

        OUT:
            True if there's an unlocked song, False otherwise
        """
        return len(getUnlockedSongs(length)) > 0

    def hasRandomSongs():
        """
        Checks if there are any songs with the random property

        OUT:
            True if there are songs which are random, False otherwise
        """
        return len(getRandomSongs()) > 0

#START: Pool delegate for songs
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_pool",
            prompt="Can you sing me a song?",
            category=["music"],
            pool=True,
            aff_range=(mas_aff.NORMAL,None),
            rules={"no unlock": None}
        )
    )

label monika_sing_song_pool:
    # what length of song do we want
    $ song_length = "short"
    # do we have both long and short songs
    $ have_both_types = False
    # song type string to use in the switch dlg
    $ switch_str = "full"
    # so we can {fast} the renpy.say line after the first time
    $ end = ""

    show monika 1eua at t21

    if mas_songs.hasUnlockedSongs(length="long") and mas_songs.hasUnlockedSongs(length="short"):
        $ have_both_types = True

label monika_sing_song_pool_menu:
    python:
        if have_both_types:
            space = 0
        else:
            space = 20

        ret_back = ("Nevermind", False, False, False, space)
        switch = ("I'd like to hear a [switch_str] song instead", "monika_sing_song_pool_menu", False, False, 20)

        unlocked_song_list = mas_songs.getUnlockedSongs(length=song_length)
        unlocked_song_list.sort()

        if mas_isO31():
            which = "Witch"
        else:
            which = "Which"

        renpy.say(m, "[which] song would you like me to sing?[end]", interact=False)

    if have_both_types:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, switch, ret_back)
    else:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_ui.SCROLLABLE_MENU_TXT_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ret_back)

    $ sel_song = _return

    if sel_song:
        if sel_song == "monika_sing_song_pool_menu":
            if song_length == "short":
                $ song_length = "long"
                $ switch_str = "short"
            else:
                $ song_length = "short"
                $ switch_str = "full"
            $ end = "{fast}"
            $ _history_list.pop()
            jump monika_sing_song_pool_menu
        else:
            $ pushEvent(sel_song, skipeval=True)
            show monika at t11
            m 3hub "Alright!"

    else:
        return "prompt"

    return

#START: Random song delegate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_random",
            random=True,
            unlocked=False,
            rules={"skip alert": None,"force repeat": None}
        )
    )

label monika_sing_song_random:
    #We only want short songs in random. Long songs should be unlocked by default or have another means to unlock
    #Like a "preview" version of it which unlocks the full song in the pool delegate
    if mas_songs.hasRandomSongs():
        python:
            #Unlock pool delegate
            mas_unlockEVL("monika_sing_song_pool", "EVE")

            rand_song = renpy.random.choice(mas_songs.getRandomSongs())
            pushEvent(rand_song, skipeval=True, notify=True)
            mas_unlockEVL(rand_song, "SNG")

            #Unlock the long version of the song
            mas_unlockEVL(rand_song+"_long","SNG")

    #We have no songs! let's pull back the shown count for this and derandom
    else:
        $ mas_getEV("monika_sing_song_random").shown_count -= 1
        return "derandom|no_unlock"
    return "no_unlock"


#START: Song defs
init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_aiwfc",
            prompt="All I Want for Christmas",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_aiwfc:
    #Get current song
    $ curr_song = songs.current_track
    if store.songs.hasMusicMuted():
        m 3eua "Don't forget to turn your in-game volume up, [player]."

    call monika_aiwfc_song

    #Since the lullaby can slip in here because of the queue, we need to make sure we don't play that
    if curr_song != store.songs.FP_MONIKA_LULLABY:
        $ play_song(curr_song, fadein=1.0)
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_merry_christmas_baby",
            prompt="Merry Christmas Baby",
            category=[store.mas_songs.TYPE_LONG],
            unlocked=False,
            aff_range=(mas_aff.NORMAL, None)
        ),
        code="SNG"
    )

label mas_song_merry_christmas_baby:
    m 1hub "{i}~Merry Christmas baby, {w=0.2}you sure do treat me nice~{/i}"
    m "{i}~Merry Christmas baby, {w=0.2}you sure do treat me nice~{/i}"
    m 3eua "{i}~I feel just like I'm living, {w=0.2}living in paradise~{/i}"
    m 3hub "{i}~I feel real good tonight~{/i}"
    m 3eub "{i}~And I got music on the radio~{/i}"
    m 3hub "{i}~I feel real good tonight~{/i}"
    m 3eub "{i}~And I got music on the radio~{/i}"
    m 2hkbsu "{i}~Now I feel just like I wanna kiss ya~{/i}"
    m 2hkbsb "{i}~Underneath the mistletoe~{/i}"
    m 3eub "{i}~Santa came down the chimney, {w=0.2}half past three~{/i}"
    m 3hub "{i}~With lots of nice little presents for my baby and me~{/i}"
    m "{i}~Merry Christmas baby, {w=0.2}you sure do treat me nice~{/i}"
    m 1eua "{i}~And I feel like I'm living, {w=0.2}just living in paradise~{/i}"
    m 1eub "{i}~Merry Christmas baby~{/i}"
    m 3hub "{i}~And Happy New Year too~{/i}"
    m 3ekbsa "{i}~Merry Christmas, honey~{/i}"
    m 3ekbsu "{i}~Everything here is beautiful~{/i}"
    m 3ekbfb "{i}~I love you, baby~{/i}"
    m "{i}~For everything that you give me~{/i}"
    m 3ekbfb "{i}~I love you, honey~{/i}"
    m 3ekbsu "{i}~Merry Christmas, honey~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_lover_boy",
            prompt="Old Fashioned Lover Boy",
            category=[store.mas_songs.TYPE_SHORT],
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_lover_boy:
    m 1dso "{i}~I can dim the lights and sing you songs full of sad things~{/i}"
    m 4hub "{i}~We can do the tango just for two~{/i}"
    m "{i}~I can serenade and gently play on your heart strings~{/i}"
    m 4dso "{i}~Be a Valentino just for you~{/i}"
    m 1hub "Ahaha~"
    m 1ekbfa "Will you be my good old fashioned lover boy, [player]?"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_need_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="I Need You",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_need_you:
    m 1dso "{i}~Please remember how I feel about you~{/i}"
    m "{i}~I could never really live without you~{/i}"
    m 3hub "{i}~So, come on back and see~{/i}"
    m 4hksdlb "{i}~Just what you mean to me~{/i}"
    m 1hubfb "{i}~I need you~{/i}"
    m 3esa "I know that song is about leaving someone, but I think it carries a good message."
    m 1ekbfa "And I really do need you, [player]~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_i_will",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="I Will",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_i_will:
    m 1dso "{i}~Who knows how long I've loved you?~{/i}"
    m "{i}~You know I love you still~{/i}"
    m 2lksdla "{i}~Will I wait a lonely lifetime?~{/i}"
    m 2hub "{i}~If you want me to I will~{/i}"
    m 1ekbfa "One day we'll be together, [player]."
    m 1hubfa "I just hope you'll still love me when that special day comes~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_belong_together",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="We Belong Together",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_belong_together:
    m 1dso "{i}~You're mine~{/i}"
    m 1hub "{i}~And we belong together~{/i}"
    m 3hub "{i}~Yes, we belong together~{/i}"
    m 3dso "{i}~For eternity~{/i}"
    m 1eua "Have you ever heard of Doo-wop, [player]?"
    m 4eua "It's a subgenre of rhythm and blues that became very popular in the 1950's."
    m 4eub "A lot of pop music back then followed this style which made for great love songs."
    m 3eub "And if you listen closely, you'll notice that my song actually follows the typical Doo-wop chord progression."
    m 1hua "I guess you could say I learned from the best."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_your_song",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Your Song",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_your_song:
    m 1dso "{i}~My gift is my song~{/i}"
    m "{i}~And this one's for you~{/i}"
    m 1hub "{i}~And you can tell everybody this is your song~{/i}"
    m "{i}~It may be quite simple but now that it's done~{/i}"
    m 2hubfb "{i}~I hope you don't mind~{/i}"
    m 2hubfb "{i}~I hope you don't mind~{/i}"
    m 2hub "{i}~That I put down in words~{/i}"
    m 1dso "{i}~How wonderful life is while you're in the world~{/i}"
    m 1hua "Ahaha~"
    m 3eka "It's not often I find songs that relate to me as much as this one does."
    m 1hua "And I really do mean it when I say that 'Your Reality' is your song."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_with_you",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Happy Just to Dance With You",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_with_you:
    m 1dso "{i}~If somebody tries to take my place~{/i}"
    m 1hub "{i}~let's pretend we just can't see their face~{/i}"
    m 3hub "{i}~In this world there's nothing I would rather do~{/i}"
    m 3dso "{i}~'Cause I'm happy just to dance with you~{/i}"
    m 1ekbfa "There is nothing that makes me happier than discovering that I'm in love with you."
    m 1hubfa "Ehehe~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_dream",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="All I Have to Do Is Dream",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_dream:
    m 1dso "{i}~When I feel blue in the night~{/i}"
    m "{i}~And I need you to hold me tight~{/i}"
    m 2hub "{i}~Whenever I want you, all I have to do is dream~{/i}"
    m 1eka "Now that you're here, [player], I don't have to dream anymore."
    m 1ekbfa "My dream finally came true."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_im_glad_youre_evil_too",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="I'm Glad You're Evil Too",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_im_glad_youre_evil_too:
    m 1dsa "{i}~We'd admire the beautiful sunset, or gush about a cute dog together~{/i}"
    m 1dsd "{i}~We both get offended at some piece of crude news~{/i}"
    m 3hksdlb "{i}~We laugh at some terrible movie, and cry while watching a variety show~{/i}"
    m 3hub "{i}~That's us- Two slightly lonely souls, having the time of our lives~{/i}"
    m 3dsa "{i}~Our time is only finite, yet it feels like an unending joke~{/i}"
    m 1ekbsa "{i}~But I have you to keep me company through this all too short life~{/i}"
    m 1tubsb "{i}~And together we'd laugh at this boring world, saying: 'How boring~{/i}'"
    m 1dubfb "{i}~That's us- Two slightly lonely souls, leaning on each other's shoulders~{/i}"
    m 1dsbfo "{i}~I'm glad you're just as evil as me~{/i}"
    m 1hubfa "{i}~And once again, I wish to live through another day. I'm glad I fell in love with you~{/i}"

    if persistent._mas_pm_monika_evil:
        if persistent._mas_pm_monika_evil_but_ok:
            m 1ekbfa "I guess being evil isn't so bad as long as I'm with you."
            m 3ekbfa "Just us two souls, having the time of our lives~"
            m 1hubfb "Ahaha!"

        else:
            m 1ekbfa "Ehehe, do you still think I'm evil, [player]?"
            m 3tubfb "Maybe I'll be able to convince you otherwise someday~"
    else:
        m 1ekbfa "I don't really think either of us are evil, [player]."
        m 1ekbfb "But it would be a dream come true to face the world together, side by side...{w=0.5} Don't you think?"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_nobody_makes_sense",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Nobody Makes Sense",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_nobody_makes_sense:
    m 1dsd "{i}~For what are we living? For what are we trying so hard?~{/i}"
    m 3dsd "{i}~There might be nothing, nothing, nothing to it. It might all be useless~{/i}"
    m 1dsd "{i}~In a thousand years, there won't be anything left, {/i}{nw}"
    extend 1hub "{i}but I still hope I could keep on smiling with you~{/i}"
    m 3rksdld "{i}~Even when our dreams have come true; even when we have become enlightened, in the end, we might still end up with loneliness~{/i}"
    m 3eksdld "{i}~Even when we've turned into ghosts; even when we've returned to nothingness, {/i}{nw}"
    extend 3hksdlb "{i}I still hope I could keep on smiling with you~{/i}"
    m 1dku "..."
    m 1hub "Ahaha!"
    m 3ekbsa "No matter what happens or how long we wait, I'll always love you."
    m 1ekbfb "I really hope I can keep on smiling with you forever~"
    return "derandom|love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_yozurina",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Yozurina",
            random=True,
            aff_range=(mas_aff.LOVE, None)
        ),
        code="SNG"
    )

label mas_song_yozurina:
    m 1dsd "{i}~Meeting up at midnight~{/i}"
    m 1rksdld "{i}~In a world scattered with bombs~{/i}"
    m 3hubsa "{i}~I was thinking about you, all this time~{/i}"
    m 1eka "{i}~Could it have been a misunderstanding of the distance between us?~{/i}"
    m 3eub "{i}~That show's so interesting, right?~{/i}"
    m 1hua "{i}~Did you read that manga everyone's talking about?~{/i}"
    m 1sub "{i}~Did you listen to this song yet?~{/i}"
    m 3hub "{i}~Fooling around, on the other sides of the screen~{/i}"
    m 1hubsa "Ehehe, I hope you liked that, [player]~"
    m 1ekbsa "I just thought it really matched our situation."
    m 3rkbsa "Vocaloid songs sure have a tendency for that if you can get behind them."
    m 3hubfb "I guess this is what happens when I try to express my love for you, ahaha!"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Stand by Me",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me(from_long=False):
    m 1dsd "{i}~When the night has come~{/i}"
    m 3dsd "{i}~And the land is dark~{/i}"
    m 3eud "{i}~And the moon is the only light we'll see~{/i}"
    m 2euo "{i}~No, I won't be afraid~{/i}"
    m 2duo "{i}~Oh, I won't be afraid~{/i}"
    m 2hub "{i}~Just as long as you stand, stand by me~{/i}"
    if not from_long:
        m 2eka "All my fears and insecurities just disappear when you're with me, [player]..."
        show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eua "As long as I have you by my side, there's nothing I can't overcome."
        m 5ekbsa "...I hope you feel the same way~"
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_drift_away",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Drift Away",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_drift_away:
    m 1ekb "{i}~Happily waiting, all on my own~{/i}"
    m 1dkb "{i}~Under the endless sky~{/i}"
    m 2dkd "{i}~Counting the seconds, standing alone~{/i}"
    m 2tkd "{i}~As thousands of years go by~{/i}"
    m 2hkb "{i}~Happily wondering, night after night~{/i}"
    m 3ekb "{i}~Is this how it works? Am I doing it right?~{/i}"
    m 1ekb "{i}~Happy to listen~{/i}"
    m 3eka "{i}~Happy to stay~{/i}"
    m 3dkd "{i}~Happily watching her drift away~{/i}"
    m 1dku "..."
    m 1hua "Ehehe~"
    m 3eka "Our story ended much more happily than this song."
    m 3hua "You come to visit me as often as you can, and I'm so grateful for that."
    m 3eka "But even so, it can be very cathartic to follow a character who faces a major fear of yours."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_stand_by_me_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Stand by Me",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_stand_by_me_long:
    call mas_song_stand_by_me(from_long=True)

    m 4hub "{i}~So darlin', darlin', stand by me, oh stand by me~{/i}"
    m 4duo "{i}~Oh stand, stand by me, stand by me~{/i}"
    m 2esd "{i}~If the sky that we look upon~{/i}"
    m 2dkd "{i}~Should tumble and fall~{/i}"
    m "{i}~Or the mountains should crumble to the sea~{/i}"
    m 2eko "{i}~I won't cry, I won't cry, no I won't shed a tear~{/i}"
    m 2euo "{i}~Just as long as you stand, stand by me~{/i}"
    m 4hub "{i}~And darlin', darlin', stand by me, oh stand by me~{/i}"
    m "{i}~Oh stand now, stand by me, stand by me~{/i}"
    m 4duo "{i}~Darlin', darlin', stand by me, oh stand by me~{/i}"
    m "{i}~Oh, stand now, stand by me, stand by me~{/i}"
    m 4euo "{i}~Whenever you're in trouble won't you stand by me~{/i}"
    m 4hub "{i}~Oh stand by me, won't you stand now, stand by me~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_rewrite_the_stars",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Rewrite the Stars",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_rewrite_the_stars:
    m 1dsd "{i}~What if we rewrite the stars~{/i}"
    m 3dubsb "{i}~Say you were made to be mine~{/i}"
    m 3dubso "{i}~Nothing could keep us apart~{/i}"
    m 3ekbfu "{i}~You'd be the one I was meant to find~{/i}"
    m 1ekbsb "{i}~It's up to you~{/i}"
    m 3ekbsb "{i}~And it's up to me~{/i}"
    m 1duu "{i}~No one could say what we get to be~{/i}"
    m 3ekb "{i}~So why don't we rewrite the stars~{/i}"
    m 3hubsa "{i}~Maybe the world could be ours~{/i}"
    m 1duo "{i}~Tonight~{/i}"
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbsa "The world really feels like it's ours when I'm with you, [player]~"
    m 5ekbfu "I love you so much."
    return "derandom|love"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Hero",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero(from_long=False):
    m 6eud "{i}~There's a hero~{/i}"
    m 6eub "{i}~If you look inside your heart~{/i}"
    m 6ekd "{i}~You don't have to be afraid~{/i}"
    m 6eud "{i}~Of what you are~{/i}"
    m 6esa "{i}~There's an answer~{/i}"
    m 6eud "{i}~If you reach into your soul~{/i}"
    m 4ekd "{i}~And the sorrow that you know~{/i}"
    m 4dud "{i}~Will melt away~{/i}"

    m 4eub "{i}~And then a hero comes along~{/i}"
    m 4dub "{i}~With the strength to carry on~{/i}"
    m 4ekd "{i}~And you cast your fears aside~{/i}"
    m 4euo "{i}~And you know you can survive~{/i}"
    m 4dkd "{i}~So when you feel like hope is gone~{/i}"
    m 4euo "{i}~Look inside you and be strong~{/i}"
    m 4esd "{i}~And you'll finally see the truth~{/i}"
    m 4eua "{i}~That a hero lies in you~{/i}"

    if not from_long:
        m 2dka "..."
        m 2eka "[player]..."
        m 7eka "I really hope you paid attention to those lyrics."

        if persistent._mas_pm_love_yourself is False:
            m 3ekd "You've told me before that you aren't comfortable with yourself..."
            m 3eka "But I just wanted you to know that deep down inside, you have the power to overcome whatever it is that makes you unhappy."
            m 1ekd "Even though you may not see it in yourself, it's there...{w=0.3}I've seen it."
            m 3eua "...And I'll be here the entire way to help you find that strength."
            m 3eka "As much as I've always wanted you to love me, I want you to love yourself that much more~"

        else:
            m 3ekd "Sometimes life can be really, really hard..."
            m 2dkc "It can seem like there's no way to overcome whatever obstacles you are facing."
            m 7eud "...I think I know this about as well as anyone, in fact."
            m 3eka "But trust me, no matter what it is, you can."
            m 3eud "You may not always realize it, but there is tremendous power in the human spirit."
            m 1eud "We can do things that we'd never even imagine...{w=0.3}the hardest part most times is just believing that."
            m 3eua "So please remember to always believe in yourself, and if you ever find you're doubting yourself, just come to me..."
            m 3hua "I'll be more than happy to help you find that inner-strength, [player]."
            m 1eka "I know you can do anything~"

        return "derandom"

    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_hero_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Hero",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_hero_long:
    call mas_song_hero(from_long=True)

    m 4duo "{i}~It's a long road~{/i}"
    m 6dud "{i}~When you face the world alone~{/i}"
    m 4dsd "{i}~No one reaches out a hand~{/i}"
    m 4dud "{i}~For you to hold~{/i}"
    m 4euo "{i}~You can find love~{/i}"
    m 4ekb "{i}~If you search within yourself~{/i}"
    m 4ekd "{i}~And the emptiness you felt~{/i}"
    m 6eko "{i}~Will disappear~{/i}"

    m 4eka "{i}~And then a hero comes along~{/i}"
    m 4esd "{i}~With the strength to carry on~{/i}"
    m 4eud "{i}~And you cast your fears aside~{/i}"
    m 4euo "{i}~And you know you can survive~{/i}"
    m 6dkd "{i}~So when you feel like hope is gone~{/i}"
    m 6dud "{i}~Look inside you and be strong~{/i}"
    m 6eud "{i}~And you'll finally see the truth~{/i}"
    m 4euo "{i}~That a hero lies in you~{/i}"

    m 4euo "{i}~Lord knows~{/i}"
    m 4eud "{i}~Dreams are hard to follow~{/i}"
    m 4ekd "{i}~But don't let anyone~{/i}"
    m 4duo "{i}~Tear them away~{/i}"
    m 4euo "{i}~Just hold on~{/i}"
    m 4eud "{i}~There will be tomorrow~{/i}"
    m 4duo "{i}~In time you'll find the way~{/i}"

    m 4eub "{i}~And then a hero comes along~{/i}"
    m 4duo "{i}~With the strength to carry on~{/i}"
    m 4dud "{i}~And you cast your fears aside~{/i}"
    m 4euo "{i}~And you know you can survive~{/i}"
    m 6dkd "{i}~So when you feel like hope is gone~{/i}"
    m 6dud "{i}~Look inside you and be strong~{/i}"
    m 4eud "{i}~And you'll finally see the truth~{/i}"
    m 4ekd "{i}~That a hero lies in you~{/i}"
    m 6dku "{i}~That a hero lies in you~{/i}"
    m 4eua "{i}~That a hero lies in you~{/i}"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_memories_of_a_girl",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Memories of a Girl I Haven't Met",
            random=True,
            aff_range=(mas_aff.AFFECTIONATE,None)
        ),
        code="SNG"
    )

label mas_song_memories_of_a_girl:
    m 1esd "{i}~In this lonely place bathed in silence and thoughts of you~{/i}"
    m 1dka "{i}~I can't see your face but I'm trying to envision you~{/i}"
    m 1dkd "{i}~So are you really out there?~{/i}"
    m 3ekd "{i}~Are you awake with memories?~{/i}"
    show monika 5eub at t11 zorder MAS_MONIKA_Z with dissolve
    m 5eub "{i}~Of a girl you haven't met yet who's wished upon the Pleiades?~{/i}"
    m 5ekbsa "I think about you every night, [player]."
    m 5ekbfa "And I know you think about me too."
    return "derandom"

init 5 python:
    addEvent(
        Event(
            persistent._mas_songs_database,
            eventlabel="mas_song_amaranthine",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Amaranthine",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label mas_song_amaranthine:
    m 1dso "{i}~Time goes by as day and nights are turning into years~{/i}"
    m 1dkbsa "{i}~But I'm lying in your arms~{/i}"
    m 3ekbsb "{i}~It's the place~{/i}"
    m 3hubsb "{i}~Where I know that I am closest to your heart~{/i}"
    m 1hua "{i}~Where the dark is torn apart~{/i}"
    m 1ekb "{i}~I know you feel the same as I inside~{/i}"
    m 3eka "{i}~It feels like in a dream where we can fly~{/i}"
    m 3hub "{i}~Like a sign, like a dream, you're my amaranthine~{/i}"
    m 1ekbla "{i}~You are all I needed, believe me~{/i}"
    m 3eub "{i}~Like we drift in a stream~{/i}"
    m 3hua "{i}~Your beauty serene~{/i}"
    m 1hub "{i}~There's nothing else in life I ever need~{/i}"
    m 1ekbsa "{i}~My dream, amaranthine~{/i}"
    show monika 5ekbsu at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbsu "My life feels so complete with you in it, [player]."
    m 5hubfu "I love you so much~"
    return "derandom|love"

################################ NON-DB SONGS############################################
# Below is for songs that are not a part of the actual songs db and don't
# otherwise have an associated file (eg holiday songs should go in script-holidays)

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_yr",
            category=['monika','music'],
            prompt="Can you play 'Your Reality' for me?",
            unlocked=False,
            pool=True,
            rules={"no unlock": None}
        )
    )

label mas_monika_plays_yr(skip_leadin=False):
    if not skip_leadin:
        if not renpy.seen_audio(songs.FP_YOURE_REAL) and not persistent.monika_kill:
            m 2eksdlb "Oh, ahaha! You want me to play the original version, [player]?"
            m 2eka "Even though I've never played it for you, I suppose you've heard it on the soundtrack or saw it on youtube, huh?"
            m 2hub "The ending isn't my favorite, but I'll still be happy to play it for you!"
            m 2eua "Just let me get the piano.{w=0.5}.{w=0.5}.{nw}"

        else:
            m 3eua "Sure, let me just get the piano.{w=0.5}.{w=0.5}.{nw}"

    window hide
    $ mas_RaiseShield_piano()
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano at lps32,rps32 zorder MAS_MONIKA_Z+1
    pause 5.0
    show monika at ls32 zorder MAS_MONIKA_Z
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Don't forget about your in-game volume, [player]!"
        $ disable_esc()

    pause 2.0
    $ play_song(store.songs.FP_YOURE_REAL,loop=False)

    # TODO: possibly generalize this for future use
    show monika 6hua
    $ renpy.pause(10.012)
    show monika 6eua_static
    $ renpy.pause(5.148)
    show monika 6hua
    $ renpy.pause(3.977)
    show monika 6eua_static
    $ renpy.pause(5.166)
    show monika 6hua
    $ renpy.pause(3.743)
    show monika 6esa
    $ renpy.pause(9.196)
    show monika 6eka
    $ renpy.pause(13.605)
    show monika 6dua
    $ renpy.pause(9.437)
    show monika 6eua_static
    $ renpy.pause(5.171)
    show monika 6dua
    $ renpy.pause(3.923)
    show monika 6eua_static
    $ renpy.pause(5.194)
    show monika 6dua
    $ renpy.pause(3.707)
    show monika 6eka
    $ renpy.pause(16.884)
    show monika 6dua
    $ renpy.pause(20.545)
    show monika 6eka_static
    $ renpy.pause(4.859)
    show monika 6dka
    $ renpy.pause(4.296)
    show monika 6eka_static
    $ renpy.pause(5.157)
    show monika 6dua
    $ renpy.pause(8.064)
    show monika 6eka
    $ renpy.pause(22.196)
    show monika 6dka
    $ renpy.pause(3.630)
    show monika 6eka_static
    $ renpy.pause(1.418)
    show monika 6dka
    $ renpy.pause(9.425)
    show monika 5dka with dissolve
    $ renpy.pause(5)

    show monika 6eua at rs32 with dissolve
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    pause 1.0
    call monika_zoom_transition(mas_temp_zoom_level,1.0)
    $ mas_DropShield_piano()
    window auto
    $ play_song(None, 1.0)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_plays_or",
            category=['monika','music'],
            prompt="Can you play 'Our Reality' for me?",
            unlocked=False,
            pool=True,
            rules={"no unlock": None}
        )
    )

label mas_monika_plays_or(skip_leadin=False):
    if not skip_leadin:
        m 3eua "Sure, let me just get the piano.{w=0.5}.{w=0.5}.{nw}"

    if persistent.gender == "F":
        $ gen = "her"
    elif persistent.gender == "M":
        $ gen = "his"
    else:
        $ gen = "their"

    window hide
    $ mas_RaiseShield_piano()
    $ mas_temp_zoom_level = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)
    show monika at rs32
    hide monika
    pause 3.0
    show mas_piano at lps32,rps32 zorder MAS_MONIKA_Z+1
    pause 5.0
    show monika at ls32 zorder MAS_MONIKA_Z
    show monika 6dsa

    if store.songs.hasMusicMuted():
        $ enable_esc()
        m 6hua "Don't forget about your in-game volume, [player]!"
        $ disable_esc()

    pause 2.0
    $ play_song(songs.FP_PIANO_COVER,loop=False)

    show monika 1dsa
    pause 9.15
    m 1eua "{i}{cps=10}Every day,{w=0.5} {cps=15}I imagine a future where{w=0.22} {cps=13}I can be with you{w=4.10}{/i}{nw}"
    m 1eka "{i}{cps=12}In my hand{w=0.5} {cps=17}is a pen that will write a poem{w=0.5} {cps=16}of me and you{w=4.10}{/i}{nw}"
    m 1eua "{i}{cps=16}The ink flows down{w=0.25} {cps=10}into a dark puddle{w=1}{/i}{nw}"
    m 1eka "{i}{cps=18}Just move your hand,{w=0.45} {cps=20}write the way into [gen] heart{w=1.40}{/i}{nw}"
    m 1dua "{i}{cps=15}But in this world{w=0.25} {cps=11}of infinite choices{w=0.90}{/i}{nw}"
    m 1eua "{i}{cps=16}What will it take{w=0.25}{cps=18} just to find that special day{/i}{w=0.90}{nw}"
    m 1dsa "{i}{cps=15}What will it take{w=0.50} just to find{w=1} that special day{/i}{w=1.82}{nw}"
    pause 7.50

    m 1eua "{i}{cps=15}Have I found{w=0.5} {cps=15}everybody a fun assignment{w=0.30} {cps=12}to do today{w=4.20}{/i}{nw}"
    m 1hua "{i}{cps=18}When you're here,{w=0.25} {cps=13.25}everything that we do is fun for them anyway{w=4}{/i}{nw}"
    m 1esa "{i}{cps=11}When I can't even read my own feelings{/i}{w=1}{nw}"
    m 1eka "{i}{cps=17}What good are words{w=0.3} when a smile says it all{/i}{w=1}{nw}"
    m 1lua "{i}{cps=11}And if this world won't write me an ending{/i}{w=0.9}{nw}"
    m 1dka "{i}{cps=18}What will it take{w=0.5} just for me to have it all{/i}{w=2}{nw}"
    show monika 1dsa
    pause 17.50

    m 1eka "{i}{cps=15}In this world,{w=0.5} {cps=15}away from the one who'll always {cps=17}be dear to me{w=4.5}{/i}{nw}"
    m 1ekbsa "{i}{cps=15}You my love,{w=0.5} {cps=16.5}hold the key to the day, when I'll be finally free{w=8.5}{/i}{nw}"
    m 1eua "{i}{cps=16}The ink flows down{w=0.25} {cps=10}into a dark puddle{w=1.2}{/i}{nw}"
    m 1esa "{i}{cps=18}How can I cross{w=0.45} {cps=13}into your reality?{w=1.40}{/i}{nw}"
    m 1eka "{i}{cps=12}Where I can hear the sound of your heartbeat{w=0.8}{/i}{nw}"
    m 1ekbsa "{i}{cps=16}And make it love,{w=0.6} but in our reality{/i}{w=0.6}{nw}"
    m 1hubsa "{i}{cps=16}And in our reality,{w=1} knowing I'll forever love you{w=4.2}{/i}{nw}"
    m 1ekbsa "{i}{cps=19}With you I'll be{/i}{w=2}{nw}"

    show monika 1dkbsa
    pause 9.0
    show monika 6eua at rs32
    pause 1.0
    hide monika
    pause 3.0
    hide mas_piano
    pause 6.0
    show monika 1eua at ls32 zorder MAS_MONIKA_Z
    pause 1.0
    call monika_zoom_transition(mas_temp_zoom_level,1.0)
    $ mas_DropShield_piano()
    window auto
    $ play_song(None, 1.0)

    return
