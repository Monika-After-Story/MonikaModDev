"""TODOs:
    Difficulty scaling
        Time limit
        Monika's turn limit
    Write proper dlg
    Get, sanitize and format dictionaries
    Option to add missing words to dictionary - exploitable, but worth it imo
"""

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_shiritori_rules",
            category=["games"],
            prompt="Rules of shiritori",
            conditional="store.mas_games.getGameEVByPrompt("shiritori").unlocked",
            action=EV_ACT_UNLOCK,
            pool=True,
            rules={"no unlock": None}
        )
    )

label monika_shiritori_rules:
    m "Shiritori is a word game. The rules are very simple."
    m "The players take turns saying words in a certain pattern."
    m "The pattern being that the first letter of a new word must be the same as the last letter of the last word said."
    m "The losing conditions are:"
    m "Using a word that fails to follow the pattern."
    m "Trying to use something that isn't a word."
    m "Using a word that's already been used."
    m "And failing to answer within a given time limit."
    return

label player_loss_letter:
    m "That's the wrong letter, you know."
    call player_loss_final
    return

label player_loss_used:
    m "Wait a second, [last_word_p_raw]?"
    if last_word_p in recent_words:
        m "That one was played just a second ago!"
    else:
        m "I'm pretty sure one of us already used that one."
    call player_loss_final
    return

label player_loss_invalid:
    m "I don't think that's a real word."
    call player_loss_final
    return

label player_loss_timeout:
    m "...And you're out of time."
    call player_loss_final
    return

label player_loss_final:
    $ loss_quips = [
    "Sorry, but it's your loss.",
    "Your loss, [player].",
    "Looks like I win, ahaha~",
    "It's my win, [player]."
    ]
    $ loss_quip = renpy.substitute(renpy.random.choice(loss_quips))
    m "[loss_quip]" # smug expression
    return

label monika_loss_used:
    m "Wait, that one already got used, didn't it?"
    call monika_loss_final
    return

label monika_loss_final:
    $ win_quips = [
    "Guess it's my loss then.",
    "Looks like you win, [player].",
    "You won, [player]. Congratulations.",
    "You won, well done.",
    "gg no re"
    ]
    $ win_quip = renpy.substitute(renpy.random.choice(win_quips))
    m "[win_quip]"
    return

# entry point
label game_shiritori:
    m "You wanna play shiritori?"

    # 1st turn decision
    m "Do you want to start or should I?"
    $ _history_list.pop()
    menu:
        m "Do you want to start or should I?{fast}"

        "I'll start":
            m "Okay, go ahead."
            $ monika_first = False
        "You start":
            m "Okay then, I'll start."
            $ monika_first = True
        "Random":
            if random.randint(1,2) == 1:
                m "Okay, you go first."
                $ monika_first = False
            else:
                m "Okay, I'll start."
                $ monika_first = True

    python:
        # build dictionaries - do we want this here or on init?
        with open("dictionary_full.json") as dff:
            dictionary_full = json.load(dff)
        with open("dictionary_monika.json") as dmf:
            dictionary_full = json.load(dmf)

        shiritori_loop = True
        # all the words used in current game
        used_words = []
        # last 10 words - serves as Monika's short-term memory to avoid immediately repeating a word
        recent_words = []

    # if Monika has the first turn
    if monika_first:
        python:
            # get a random word from Monika's pool
            first_letter = renpy.random.choice("abcdefghijklmnopqrstuvwxyz")
            last_word_m = renpy.random.choice(dictionary_monika[first_letter])
            # add first word to used and recent
            used_words.append(last_word_m)
            recent_words.append(last_word_m)
        m "[last_word_m]"

    # main loop
    while shiritori_loop:
        python:
        # get player input
            last_word_p_raw = mas_input(
                "Input your next word",
                allow = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
                length=20
                ).strip(' \t\n\r').lower()
            last_word_p = last_word_p_raw.lower()

        # check if starting with correct letter
        if last_word_p[0] != last_word_m[-1]:
            call player_loss_letter
            shiritori_loop = False

        # check against dictionary
        elif last_word_p not in dictionary_full[last_word_p[0]]:
            call player_loss_invalid
            shiritori_loop = False

        # check against used words
        elif last_word_p in used_words:
            call player_loss_used
            shiritori_loop = False

        else:
            # add last word to used
            used_words.append(last_word_p)
            # update recent words
            recent_words.append(last_word_p)
            if len(recent_words) > 10:
                del recent_words[0]

            # Monika's turn
            m "Hmm..."
            $ last_word_m_invalid = True
            while last_word_m_invalid:
                if renpy.random.randint(1,10) == 1:
                    # small chance to have Monika pull from the full vocab
                    $ last_word_m = renpy.random.choice(dictionary_full[last_word_p[-1]])
                else:
                    $ last_word_m = renpy.random.choice(dictionary_monika[last_word_p[-1]])

                # checking if recently played
                if last_word_m not in recent_words:
                    $ last_word_m_invalid = False

            m "[last_word_m]"
            # checking if used
            if last_word_m in used_words:
                call monika_loss_used
                shiritori_loop = False

    return
