default persistent._mas_songs_database = dict()

init -10 python in mas_songs:
    # Event database for songs
    song_db = {}

    #Song type constants
    #NOTE: TYPE_SHORT will never be picked in the random delegate, these are filters for that
    #TYPE_LONG songs should either be unlocked via a 'preview' song of TYPE_SHORT or (for ex.) some story event
    #TYPE_LONG songs would essentially be songs longer than 10-15 lines
    #NOTE: TYPE_LONG songs must have the same label name as their short song counterpart with '_long' added to the end so they unlock correctly
    #Example: the long song for short song monika_song_example would be monika_song_example_long
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
            conditional="store.mas_songs.hasUnlockedSongs()",
            action=EV_ACT_UNLOCK,
            aff_range=(mas_aff.NORMAL,None)
        )
    )

label monika_sing_song_pool:
    # what length of song do we want
    $ song_length = None
    # do we have both long and short songs
    $ have_both_types = False
    # song type string to use in the switch dlg
    $ switch_str = None

    m 1hua "Sure!"
    if mas_songs.hasUnlockedSongs(length="long") and mas_songs.hasUnlockedSongs(length="short"):
        $ have_both_types = True
        m 3eua "What type of song would you like me to sing?{nw}"
        $ _history_list.pop()
        menu:
            m "What type of song would you like me to sing?{fast}"

            "A short song.":
                $ song_length = "short"
                $ switch_str = "full"

            "A full song.":
                $ song_length = "long"
                $ switch_str = "short"

label monika_sing_song_pool_menu:
    show monika 1eua at t21
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

        renpy.say(m, "[which] song would you like me to sing?", interact=False)

    if have_both_types:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, switch, ret_back)
    else:
        call screen mas_gen_scrollable_menu(unlocked_song_list, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, ret_back)
    show monika at t11

    $ sel_song = _return

    if sel_song:
        if sel_song == "monika_sing_song_pool_menu":
            if song_length == "short":
                $ song_length = "long"
                $ switch_str = "short"
            else:
                $ song_length = "short"
                $ switch_str = "full"
            jump monika_sing_song_pool_menu
        else:
            $ pushEvent(sel_song, skipeval=True)
            m 3hub "Alright!"

    else:
        m 1eka "Alright, [player]."
        m 3eua "If you ever want me to sing to you, just let me know~"
    return

#START: Random song delegate
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sing_song_random",
            random=True,
            unlocked=False,
            rules={"skip alert": None}
        )
    )

label monika_sing_song_random:
    #We only want short songs in random. Long songs should be unlocked by default or have another means to unlock
    #Like a "preview" version of it which unlocks the full song in the pool delegate
    if mas_songs.hasRandomSongs():
        python:
            rand_song = renpy.random.choice(mas_songs.getRandomSongs())
            pushEvent(rand_song, skipeval=True, notify=True)
            mas_unlockEVL(rand_song, "SNG")

            # unlock the long version of the song
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
            prompt="Happy Just To Dance With You",
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
            prompt="All I Have To Do Is Dream",
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
            eventlabel="monika_song_stand_by_me",
            category=[store.mas_songs.TYPE_SHORT],
            prompt="Stand By Me",
            random=True,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label monika_song_stand_by_me(from_long=False):
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
            eventlabel="monika_song_stand_by_me_long",
            category=[store.mas_songs.TYPE_LONG],
            prompt="Stand By Me",
            random=False,
            unlocked=False,
            aff_range=(mas_aff.NORMAL,None)
        ),
        code="SNG"
    )

label monika_song_stand_by_me_long:
    call monika_song_stand_by_me(from_long=True)

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
