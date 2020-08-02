
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_shiritori_rules",
            category=["games"],
            prompt="Rules of shiritori",
            conditional="renpy.seen_label('mas_unlock_shiritori')",
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
    m "Note: also add allowed word types here once we're clear on that - no proper nouns, no abrreviations, no one-letters, etc."
    return

label player_loss(reason=""):
    if reason == "letter":
        m "That's the wrong letter, you know."
    elif reason == "invalid":
        m "I don't think that's a real word."
    elif reason == "used":
        m "Wait a second, [last_word_p_raw]?"
        if last_word_p in recent_words:
            m "That one was played just a second ago!"
        else:
            m "I'm pretty sure one of us already used that one."
    elif reason == "timeout":
        m "...And you're out of time."
    else:
        m "This isn't supposed to happen."

    $ loss_quips = [
    "Sorry, but it's your loss.",
    "Your loss, [player].",
    "Looks like I win, ahaha~",
    "It's my win, [player]."
    ]
    $ loss_quip = renpy.substitute(renpy.random.choice(loss_quips))
    m "[loss_quip]" # smug expression
    return


label monika_loss(reason = ""):
    # Monika can only lose via word repetition or turn exhaustion (ie time limit rule), the other two are silly
    if reason == "used":
        m "Wait, that one already got used, didn't it?"
    elif reason == "timeout":
        m "I...can't think of anything."
        m "This is embarrassing, ahaha~"
    else:
        m "This isn't supposed to happen either."

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

screen shiritori_input(prompt, timeout, use_return_button=False, return_button_prompt="Nevermind.", return_button_value="cancel_input"):
    # this is literally just the input screen with a timer slapped on it
    style_prefix "input"

    window:
        if use_return_button:
            textbutton return_button_prompt:
                style "choice_button"
                align (0.5, 0.5)
                ypos -263
                action Return(return_button_value)

        vbox:
            align (0.5, 0.5)
            spacing 30

            text prompt style "input_prompt"
            input id "input"

    timer timeout action Return("timeout")

# entry point
label game_shiritori:
    m "You wanna play shiritori? Okay~"
    m "Cities only or full dictionary?"
    $ _history_list.pop()
    menu:
        m "Cities only or full dictionary?{fast}"

        "Cities only":
            m "Cities it is."
            $ game_variant = "cities"

        "Full":
            m "The whole vocabulary then."
            $ game_variant = "full"

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
        if game_variant == "full":
            with open("shiritori_dictionary_full.json") as dff:
                dictionary_full = json.load(dff)
            with open("shiritori_dictionary_monika.json") as dmf:
                dictionary_monika = json.load(dmf)

        elif game_variant == "cities":
            with open("shiritori_dictionary_cities.json") as dff:
                dictionary_full = json.load(dff)
                dictionary_monika = json.load(dff)

        timelimit = 10
        shiritori_loop = True
        # all the words used in current game
        used_words = set()
        # last 10 words - serves as Monika's short-term memory to avoid immediately repeating a word
        recent_words = set()

    # if Monika has the first turn
    if monika_first:
        python:
            # get a random word from Monika's pool
            first_letter = renpy.random.choice("abcdefghijklmnopqrstuvwxyz")
            last_word_m = renpy.random.choice(dictionary_monika[first_letter])
            # add first word to used and recent
            used_words.add(last_word_m)
            recent_words.add(last_word_m)
        m "[last_word_m]"

    # main loop
    while shiritori_loop:
        python:
        # get player input
            last_word_p_raw = mas_input(
                "Input your next word",
                allow = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .'-",
                length=20,
                screen = "shiritori_input",
                screen_kwargs = {timeout:timelimit}
                ).strip(' \t\n\r').lower()
            last_word_p = last_word_p_raw.lower()

        # check for timeout
        if _return == "timeout":
            call player_loss(reason = "timeout")
            $ shiritori_loop = False

        # check if starting with correct letter
        if last_word_p[0] != last_word_m[-1]:
            call player_loss(reason = "letter")
            $ shiritori_loop = False

        # check against dictionary
        elif last_word_p not in dictionary_full[last_word_p[0]]:
            call player_loss(reason = "invalid")
            $ shiritori_loop = False

        # check against used words
        elif last_word_p in used_words:
            call player_loss(reason = "used")
            $ shiritori_loop = False

        else:
            # update used word sets
            python:
                used_words.add(last_word_p)
                recent_words.add(last_word_p)
                if len(recent_words) > 10:
                    recent_words.pop()

            # Monika's turn
            m "Hmm..."
            $ last_word_m_invalid = True

            # TODO Monika's loss via turn exhaustion here
            # if [exhaustion]:
            #   pause timelimit
            #   call monika_loss(reason = "timeout")
            #   $ shiritori_loop = False

            # getting Monika's next word
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
                call monika_loss(reason = "used")
                $ shiritori_loop = False

            else:
                # update used word sets
                python:
                    used_words.add(last_word_m)
                    recent_words.add(last_word_m)
                    if len(recent_words) > 10:
                        recent_words.pop()

    return
