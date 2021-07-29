#------To do: Add a new apologize reason for not listening the lesson carefully?--------
define chesslevel_didntevenbegin = 1
define chesslevel_beginner = 2
define chesslevel_advancer = 3
define chesslevel_master = 4

define highlight_type_yellow = 1
define highlight_type_green = 2
define highlight_type_red = 3
define highlight_type_magenta = 4

default persistent._mas_pm_player_chesslevel = None
default persistent._mas_pm_chessteaching_materials_explained = False
default persistent._mas_pm_player_know_pgn = None
default persistent._mas_pm_player_know_stalemate = None
default persistent._mas_pm_player_know_terms = None

init 4 python in mas_chessteaching:
    import datetime
    import store.evhand as evhand
    def init_has_finished():
        """
        Check if 3 days have passed since the player asked "Can you teach me about chess".
        If it does, the function returns True.
        If not, it returns False. 
        The term "3 days" here refers to a change of date, not an absolute 72 hours.

        OUT:
            A Boolean. True or False.
        """
        event_data = evhand.event_database.get("monika_chesslesson_init", None)

        return(
            event_data is not None
            and event_data.last_seen is not None
            and event_data.timePassedSinceLastSeen_d(datetime.timedelta(days=3))
        )
    
    def player_is_good_at_chess():
        """
        This function checks if the player is "playing well" at chess.
        Both the Advancer level and the Master level will be considered "playing well".
        Otherwise, return false.

        OUT:
            A Boolean. Based on player's chess level to return.
        """
        return (persistent._mas_pm_player_chesslevel >= 3)
    
    def player_know_about_chess():
        """
        This function checks if the player has at least some knowledge of chess.
        Essentially, this function returns True as long as the player has not selected "I know nothing about chess".

        OUT:
            A Boolean. Based on player's chess level to return.
        """
        return (persistent._mas_pm_player_chesslevel >= 2)

label monika_chesslesson_answer_repeated:
    m 1rusdrb "Sorry, [mas_get_player_nickname()]..."
    m 1eua "But you have already chose that one."
    m 3hua "Pick another one!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_init",
            category=["chess lessons"],
            prompt="Can you teach me about Chess?",
            pool = True,
            aff_range=(mas_aff.HAPPY, None),# Only if Monika is not sad so she is willing to teach you.
            rules={"bookmark_rule": store.mas_bookmarks_derand.BLACKLIST},
            unlocked = True
        )
    )

label monika_chesslesson_init:
    $ wins = persistent._mas_chess_stats["wins"]
    $ losses = persistent._mas_chess_stats["losses"]

    m 1eub "You want me to teach you chess?"
    m 1hub "That's great!"

    if wins < losses:
        m 1tfu "Not a surprise since you lost more than won..."
        m 1hub "Ahaha!"
    elif wins == losses:
        m 1eua "Though I think our chess level is actually about the same..."
        m 1hua "It's still nice to say!"
    elif wins > losses:
        m 1lusdru "Though I am actually a little worried that my level may not be as good as yours..."
        m 3efa "But I will try my best!"
    

    m "..."
    m 1rtp "Anyways...{w=0.2}{nw}"
    extend 1etsdla "I'm not really ready today..."
    m 1htsdla "I have never tried to teach someone chess..."
    m 4hksdla "So I may need a few days to prepare your lessons...{w=0.1} Ehehe..."
    m 3eua "But still thanks for asking! I will be prepared soon!"
    m 1euc "And, before I went to ready your lessons..."
    m 3eud "I'd like to know, how is your chess level now?"
    m 3rusdra "You see, if I'm teaching a skillful player how to move pieces, then it must be really strange..."
    m 3rusdrb "...And if I'm teaching a beginner advanced chess, it's also unlogical..."
    m 1eua "So, [player]. How is your chess level now?{nw}"
    $ _history_list.pop()
    menu:
        m "So, [player]. How is your chess level now?{fast}"

        "I know nothing about chess.":
            $ persistent._mas_pm_player_chesslevel = chesslevel_didntevenbegin
            m 1euc "Oh... I see."
            m "So you didn't even begin to learn chess..."
            if wins < losses:
                m 1tfu "It's now even more reasonbale that you lost more than won..."
                m 1hub "Ahaha!"

        "Beginner.":
            $ persistent._mas_pm_player_chesslevel = chesslevel_beginner
            m 1eud "Beginner? That's what I expected..."

        "Advancer.":
            $ persistent._mas_pm_player_chesslevel = chesslevel_advancer
            m 1lud "Advancer? That's a little strange..."
            m 1tsu "Am I even {i}that{/i} good at chess in your eyes?"
            m 1hub "Ahaha! Then I have to try to be a {i}master{/i}!"

        "Master.":
            $ persistent._mas_pm_player_chesslevel = chesslevel_master
            m 1wud "Master...{w=1.0}{nw}"
            extend 1husdlb "I have to say, I am feeling oppressive..."
            if wins < losses:
                $ mas_gainAffection(1,bypass=True)
                m 1sub "So you are going easy on me all the time?"
                m 1hua "That's really sweet of you, {i}master{/i}~"
            elif wins = losses:
                m "But considering I've won about as many times as you have..."
                m "I guess there is still something I can teach you..."
            elif wins > losses:
                m "And this is actually logical...{w=0.6}{nw}"
                extend 1lusdla "Considering how many times you have beaten me..."
                m 1hksdla "Oh, gosh... It's even more oppressive now..."
                m 1efa "But don't worry! I'm still going to try my best!"
    
    if player_is_good_at_chess() == False:
        m 1eub "Then, in view of your statement that you are not very good at chess, let me confirm a few things in particular."
        m 3eua "Do you know what is {i}PGN format{/i}?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you know what is {i}PGN format{/i}?{fast}"
            "Yes, I know.":
                $ persistent._mas_pm_player_know_pgn = True
                m 3hua "Okay! Then I guess I don't need to prepare PGN lesson for you."
                m 1hub "Thanks for telling me that, [player]!"
            "Not really.":
                $ persistent._mas_pm_player_know_pgn = False
                m 1eub "Okay, then I will add that lesson into my list!"
        
        m 1eua "And, do you know the exact rules of stalemate?{nw}"
        $ _history_list.pop()
        menu:
            m "And, do you know the exact rules of stalemate?{fast}"
            "Yes, I know.":
                $ persistent._mas_pm_player_know_stalemate = True
                $ word = "another" if persistent._mas_pm_player_know_pgn else "a"
                m 1hua "Okay! Then this will be [word] lesson that I don't need to prepare."
            "Not really.":
                $ persistent._mas_pm_player_know_stalemate = False
                m 1hub "Not a problem! I'll teach you that one."
        
        m 3eub "One last thing, do you know basic chess terms?"
        m 3rtc "Like...{w=0.3}{nw}"
        extend 3rtd " {i}King Side{/i}, {i}Book Move{/i}, {i}Blunder{/i}, {i}Materials{/i} things?"
        m 3rtc "Do you know them?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you know them?{fast}"
            "Yes, I know.":
                $ persistent._mas_pm_player_know_terms = True
                m 1hua "Understood! Then I guess there is no need for me to prepare those lessons, ahaha!"
            "Not really.":
                $ persistent._mas_pm_player_know_terms = False
                m 1hub "That's fine, I will prepare a lesson of these terms for you!"

    m 1eua "Anyways, I will prepare them soon."
    m 1hua "Be ready!"

    m "OH, AND BY THE WAY."
    m "As it is still in the beta phase, you can now activate the Chess Lesson immediately for your convenience."
    m "Normally, you have to wait three days."
    m "So, do you want to activate them right now for testing?{nw}"
    menu:
        m "So, do you want to activate them right now for testing?{fast}"
        "Yes.":
            m "Then here we are."
            $ pushEvent("monika_chesslesson_init_finished",skipeval=True)
        "No.":
            m "Alright."

    # Hide this event.
    $ mas_hideEVL("monika_chesslesson_init", "EVE", lock=True, depool=True)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_init_finished",
            conditional = "mas_chessteaching.init_has_finished()",
            action = EV_ACT_PUSH
        )
    )

label monika_chesslesson_init_finished:
    m 1eub "Hey, [player]!"
    m 3eua "Remember that chess lesson I said I was going to give you?"
    m 3hua "I've got it all planned out!"
    m 3husdla "Although they are a bit messy...{w=0.4}{nw}"
    extend 3husdlb " and I don't have a strict order for them either."
    if persistent._mas_pm_player_chesslevel == chesslevel_master:
        m 3rusdlb "And considering that you're already a master at chess, I'm afraid these lessons seem rather useless to you..."
    elif persistent._mas_pm_player_chesslevel == chesslevel_advancer:
        m 3rusdlb "And considering that you say you've done quite a bit of work on chess, I hope you'll tolerate some of the more verbose aspects of my lesson."
    m 1eua "But anyway, if you see any lessons that interest you, just ask me."
    m 1esb "There are also some courses that I won't offer you right now...{w=0.2} I'm only going to talk to you about those advanced stuffs after you've taken certain classes."
    m 1hub "That's about all I have to say. If you want to have a class, you can start now!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_whatischess",
            category=["chess lessons"],
            prompt="What is Chess?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_whatischess:
    m 1hua "Alright, [player]!"
    m "Let us start your chess lesson~"
    m 3duc "Now, let me get the board ready.{w=0.1}.{w=0.1}.{w=0.1}{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        game = MASChessDisplayableBase(is_player_white=True)
        game.toggle_sensitivity()
        game.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m 1eub "As you can see, this is the chess board."
    m "And, did you find that the pieces have two colors?"
    m "Two colors of pieces stand for two players, of course.{w=0.1} One of players would play white, and the other player would play black."
    m "Both players need to manipulate their pieces to their advantage and win."

    # Make the board disappear. Let Monika back.
    $ game.hide()
    show monika at t11

    m 1rusdrb "Hmm... Chess is such a game, if only from a cold logical point of view."
    m 3rusdrb "Sorry for having only so limited words, but that's really how we can define chess..."
    m 1hua "Thanks for listening anyway!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_terms",
            category=["chess lessons"],
            prompt="Terms in chess",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and persistent._mas_pm_player_know_terms == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_terms:
    if mas_getEV("monika_chesslesson_terms").shown_count == 0:
        m 1hub "Well, [player], I've prepared a list about terms you may don't understand."
        m 1hua "Choose one you don't understand, and I'll explain that one for you!"
    else:
        m 1hub "Did you forget a term? Don't worry, [mas_get_player_nickname()]~"

    # Since the list is terribly long, let us use this menu.
    python:
        final_item = ("I've understood all of them now.", False, False, False, 20)
        menu_items = [
            ("Blunder", ".blunder", False, False),
            ("Book Move", ".battery", False, False),
            ("Battery", ".bookmove", False, False),
            ("Develop", ".develop", False, False),
            ("Finachetto", ".finachetto", False, False),
            ("File and Line",".fileandline",False,False),
            ("Fortress",".fortress",False,False),
            ("Gambit", ".gambit", False, False),
            ("Kind Side and Queen Side", ".side", False, False),
            ("Materials", ".materials", False, False),
            ("Stalemate", ".stalemate", False, False),
            ("Threefold Repetition", ".threefold", False, False),
            ("Underpromotion", ".underpromotion", False, False),
            ("Zugzwang", ".zugzwang", False, False)
        ]
    
    show monika 1eua at t21
    $ renpy.say(m, "Which one you don't know?{fast}", interact=False)
    call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)
    
    $ label = _return

    $ random_dialogue = random.choice(["So...","Anyways...","Now...", "This is what this term means. So...", "For now..."])

    while label:# "while label" means player didn't pick final_item.
        call expression "monika_chesslesson_terms" + label

        $ renpy.say(m, "Is there anyone you still don't know?{fast}", interact=False)
        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        $ label = _return

        $ random_dialogue = random.choice(["So...","Anyways...","Now...", "This is what this term means. So...", "For now..."])

    # If the player exit the while loop, it means they chose the "I've understood all of them now".
    jump monika_chesslesson_terms_end

    label .blunder:
        m 1eub "Blunder means a really bad move."
        python:
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/5k2/3q4/3P4/4P3/4K3/8/8 b - - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 1eua "Like this game, it's black to move."
        m 3eub "Black has a queen, while white has only two pawns. It's obvious that white is in a huge disadvantage."
        m 3eua "There are many ways black can checkmate white, but let's say black is a beginner and they play this move:{w=0.3}{nw}"
        python:
            game.queue_move("d6d5")
            game.handle_monika_move()
        extend 3hua " obviously again, this is losing a winning position."
        python:
            game.queue_move("e4d5")
            game.handle_player_move()
        m 1eua "After white takes the queen, black no longer has a chance to win."
        m 1eub "For move like this one, we call it a blunder."
        m 1hua "Easy to understand, right?"
        $ game.hide()
        m 1eua "[random_dialogue]"
        return
    
    label .bookmove:
        m 1eud "Oh, this concept. It is often misunderstood by many people."
        m 1luc "A book move does not mean that a move is so good that it will be recorded in a book."
        m 3eud "The book move is always an opening move, and it means this move is something that was included in textbook."
        m 3eua "Or say, a book move is an opening move which is considered standard."
        m 1eub "For example...{w=0.3}{nw}"
        python:
            game = MASChessDisplayableBase(is_player_white=True)
            game.toggle_sensitivity()
            game.show()
        extend 1eua " In openings, the most popular choice would be move the e2 pawn."
        python:
            game.queue_move("e2e4")
            game.handle_player_move()
        m 1eub "This is the the most classic first move, has been studied for thousands of years, called {i}King's Pawn Opening{/i}."
        m 1eua "So this is a book move."
        python:
            game.queue_move("e7e5")
            game.handle_monika_move()
        m "And this response, is also pretty classic. So this is also a book move."
        $ game.hide()
        m "[random_dialogue]"
        return
    
    label .battery:
        m 1eud "Oh, battery? This is a relatively advanced concept."
        m 3eua "This concept refers to a configuration of chess pieces."
        m 3eub "When you stack up pieces that have the same attack path, it's called a battery."
        python:
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="r4rk1/pp1b1ppp/2p5/3p4/3P4/qPPQ4/P4PPP/R2B1RK1 w - - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 3eua "See this game. Notice the b1-h7 diagonal."
        python:
            game.request_highlight_diagonal("b1","h7",0.3)
            renpy.pause(0.5)
        m 4lub "This diagonal is being controlled by the white queen."
        m 4esb "If white move their bishop to c2 square, then this is a battery move!"
        python:
            game.queue_move("d1c2")
            game.handle_player_move()
            renpy.pause(1)
            game.request_highlight_diagonal("b1","h7",0.3,highlight_type_red)
            renpy.pause(0.5)
        m 4lsa "It's like charging the queen, so people called move like this {i}battery{/i}."
        m 1lub "After the queen is charged, if black does not block this attack path, the queen will move to h7 on the next turn, which is a checkmate."
        m 1hua "That's what battery is for--{w=0.3}to \"charge\" a piece!"
        $ game.hide()
        m 1eua "[random_dialogue]"
        return
    
    label .develop:
        m 1eub "Develop the term means move pieces to a position where they can be useful."
        python:
            game = MASChessDisplayableBase(is_player_white=True)
            game.toggle_sensitivity()
            game.show()
        m 1ltc "I don't know if you're aware of one thing, that's chess pieces are usually not very useful in their initial position."
        m 1esd "For example, the two bishops.{w=0.3}{nw}"
        python:
            game.request_highlight_diagonal("c1","h6")
            game.request_highlight_diagonal("a6","f1")
        extend 1esc " They are almost completely useless in the initial position for they are blocked."
        m 1esa "And two knights are the same.{w=0.3}{nw}"
        python:
            game.remove_highlight_all()
            game.request_highlight_common_format("a3")
            game.request_highlight_common_format("c3")
            game.request_highlight_common_format("d2")
            game.request_highlight_common_format("e2")
            game.request_highlight_common_format("f3")
            game.request_highlight_common_format("h3")
        extend 1eub " These squares that they can control can not help control the central area."
        m 1eua "Therefore, it is necessary to move the pieces into a positive position."
        python:
            game.hide()
            game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pppppppp/8/8/2PPPP2/1PNB1N2/PB4PP/R2Q1RK1 w kq - 0 1")
            game.toggle_sensitivity()
            game.show()
        m "See this position. In this game, black didn't lose any piece, but black is in a huge disadvantage."
        m 3eub "The reason is obvious. The white pieces have been mobilized, and the black side has not moved at all."
        m 3eua "The process of moving pieces out is called \"develop\"."
        $ game.hide()
        m 1eua "[random_dialogue]"
        return

    label .finachetto:
        m 1eub "Finachetto the term means a special position of bishops."
        python:
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="rnbqk1nr/ppppppbp/6p1/8/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 1esa "In this game, notice the bishop on g7 square.{nw}"
        python:
            game.request_highlight_common_format("g7")
        extend 1esb " {w=0.3}That's a finachetto bishop."
        m 1eub "When a bishop is a finachetto one, this bishop is probably highly useful for it can control the most long diagonal on the board."
        m 3eua "And this bishop is hard to remove, too, because there are three pawns protecting it."
        m 1eua "About the exact advantage of finachetto, since this is only a lesson to introduce, I'm not going to talk about it further."
        m 1hub "If you're interested, let us learn this position later!"
        $ game.hide()
        m 1eua "[random_dialogue]"
        return
    
    label .fileandline:
        m 1eub "Oh, file and line?"
        m 1rusdlb "As what you can probably guess, the word file in chess, of course, doesn't mean a document. It means a vertical column!"
        m 1esa "Line, on the other hand, means a horizontal column."
        python:
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/8/8/8/8/8 w - - 0 1")
            game.toggle_sensitivity()
            game.show()
        #TODO: Implements letters and numbers on the board
        m 1eub "Let us look at this board I made for us which we've been using all the time."# Here we assume that Monika made the chessboard in MAS.
        m 1esb "I've added letters and numbers on it, which you've perhaps already found."
        m 3eub "These letters, {i}abcdefgh{/i}, are the symbol of files."
        m 3eua "To refer to them, we can say a-file, b-file or something like these."
        m 3hua "And lines, neturally, were presented by numbers."
        m 1eub "So we can refer to them with this format: Line 1, Line 2, things like these."
        $ game.hide()
        m 1eua "[random_dialogue]"
        return
    
    label .fortress:
        m 1eub "The fortress is something kind of a trick that you can use when you're in a endgame with disadvantage."
        python:
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/6k1/8/4R3/2KP4/6q1 b - - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 3esa "See this game. White has a queen, while black has only a rook."
        m "Things seem pretty hopeless, right?"
        m 3tuu "But actually white can not win this game if black play correctly."
        m 3eub  "This is kind of unexpected, isn't it? Let us just see how things are going to turn our if both two players are playing the best move."
        show monika 1lua
        python:
            game.queue_move("g1g4")
            game.handle_player_move()
            renpy.pause(1)
            game.queue_move("e3c3")
            game.handle_monika_move()
            renpy.pause(1)
            game.queue_move("g4e4")
            game.handle_player_move()
            renpy.pause(1)
            game.queue_move("c2c1")
            game.handle_monika_move()
            renpy.pause(1)
            game.queue_move("e4h1")
            game.handle_player_move()
            renpy.pause(1)
            game.queue_move("c1c2")
            game.handle_monika_move()
            renpy.pause(1)
            game.queue_move("h1e4")
            game.handle_player_move()
            renpy.pause(1)
            game.queue_move("c2d1")
            game.handle_monika_move()
            renpy.pause(1)
            game.queue_move("e4h1")
            game.handle_player_move()
            renpy.pause(1)
            game.queue_move("d1e2")
            game.handle_monika_move()
            renpy.pause(1)
            game.queue_move("h1g2")
            game.handle_player_move()
            renpy.pause(1)
            game.queue_move("e2d1")
            game.handle_monika_move()
            renpy.pause(2)
        m 2lub "Did you find the point?"
        m 2hua "Yes, it's impossible for white to win if black played correctly, but it's also impossible for black to win if white played correctly."
        m 2hub "White's two pieces form a fortress that prevents white from being checkmate, so black can only check, but never checkmate."
        m 2ltc "Though, this technique is considered a trick by some players, so there are someone who don't like it."
        m 2esd "But you want me to tell you? There's nothing in the rules of chess that says you can't do that."
        m 2esb "In fact, this compulsive draw is also an expression of chess skill, isn't it?"
        $ game.hide()
        m 1eua "[random_dialogue]"
        return

    label .gambit:
        m 3esa "Gambit is an important skill."
        m 3esb "When you see your opponent suddenly and strangely hand you a piece--{w=0.2}often seen in openings--{w=0.2}Beware! This could be a gambit!"
        python:
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2")
            game.toggle_sensitivity()
            game.show()
            game.queue_move("c2c4")
            game.handle_player_move()
        m 1eub "The game in front of your eyes is a famous opening called {b}Queen's Gambit{/b}."
        if seen_event("monika_chesslesson_opening_queen_gambit"):
            m 1esa "Remember this one? I taught it to you before!"
        else:
            m 1esb "I've prepared a full lesson about this opening, so we can have a more detailing discussion later."
            m 1esa "As for now, let us just foucs on gambit the concept."
        m 1eub "In this opening, white just pushed the c2 pawn to c4, which might seems strange."
        python:
            game.queue_move("d5c4")
            game.handle_monika_move()
        m 1esd "It's true that black can capture this pawn, and there seems like nothing can recapture black's pawn."
        m 1esa "But it's only 'seems like'. The fact is that white can always recapture this pawn or force black to cost a few turns to protect it!"
        python:
            game.queue_move("e2e3")
            game.handle_player_move()
        m 1lub "Here, white moved a pawn forward, which also opened a diagonal."
        python:
            game.request_highlight_diagonal("a6","f1")
        m 1lua "Black doesn't have a very good way to protect this pawn."
        m 1eub "Also, if black does end up taking the time to protect the pawn, then white is bound to take the lead elsewhere."
        m 1hua "So, you get the idea now. Gambit refers to a move in which one gives up some of one's pieces in order to gain an advantage in elsewhere."
        $ game.hide()
        m 1eua "[random_dialogue]"
        return

    label .side:
        m 1esa "King Side and Queen Side, literally, the side where the king is or the side where the queen is."
        python:
            game = MASChessDisplayableBase(is_player_white=True)
            game.toggle_sensitivity()
            game.show()
        m 1lub "E-file to h-file is the king side,{w=0.3}{nw}"
        python:
            game.request_highlight_file('e',highlight_type_green)
            game.request_highlight_file('f',highlight_type_green)
            game.request_highlight_file('g',highlight_type_green)
            game.request_highlight_file('h',highlight_type_green)
        extend 1lua " and the a-file to d-file, as what you can guess,{w=0.3}{nw}"
        python:
            game.request_highlight_file('a')
            game.request_highlight_file('b')
            game.request_highlight_file('c')
            game.request_highlight_file('d')
        extend 1eua " is the queen side."
        m 1esb "Note that they never change. It's not that this range changes as the game progresses and the positions of the king and queen change."
        python:
            game.hide()
            game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqk2r/1p2ppbp/p2p1np1/8/3NP3/2N1B3/PPPQ1PPP/2KR1B1R b kq - 3 8")
            game.toggle_sensitivity()
            game.show()
        m 1lub "Like this position. Although the king has moved, the king is on the queen side instead of the king side now."
        m 3esd "You may find this rule puzzling, but this is the term."
        m 1duc "I can't explain to you in a few words why...{w=0.3}{nw}"
        extend 1eua " But if you keep studying chess, you'll see that it's reasonable."
        $ game.hide()
        m "[random_dialogue]"
        return

    label .materials:
        m 1eub "Materials the word means the power of pieces, you could say."
        m 1eua "The more pieces a player has, and the more powerful the pieces, the stronger their materials will be."
        m 3eub "For example, if one player has 8 queens and another has only 5 rook, it is clear that the former has better materials than the latter."
        m 1eua "[random_dialogue]"
        return
    
    label .stalemate:
        m 1esd "Stalemate is the third way to end a chess game."
        m 1esc "When a stalemate happens, it means no one is the winner, and no one is the loser too."
        m 1eub "It occurs when the opponent's king is not attacked at the moment, but the opponent's king must be attacked after the move, and the opponent can not move other pieces except the king."
        m 1eua "There are many reasons why an opponent cannot move a piece other than the king. For example, they may have only one king and no other pieces."
        python:
            game = MASChessDisplayableBase(is_player_white=True, starting_fen = "7K/8/3b2k1/3b4/8/8/8/8 w - - 0 1")
            game.toggle_sensitivity()
            game.show()
            game.request_highlight_diagonal("d6","f8",color = highlight_type_red)
            game.request_highlight_diagonal("d5","g8",color = highlight_type_red)
        m 1eub "Like this position. It's white to move, but white has no any legal move, so this is a stalemate."
        m 1hua "I made a full lesson of this because it worth a discussion. We can focus on this in that class."
        m 1hub "For now, this brief introduction should be enough."
        $ game.hide()
        m 1eua "[random_dialogue]"
        return

    label .threefold:
        m 3eub "Threefold Repetition is a chess rule and it's really important."
        m 1eua "When the same position is presented again and again, the third time, the game is decided as a draw."
        python:
            game = MASChessDisplayableBase(is_player_white=True, starting_fen = "1kb5/1pp5/8/8/8/8/8/R4KB1 w - - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 1lub "In this game, black is not so good, but their opponent don't know the threefold repetition rule."
        m 1lua "So the following moves were played."
        python:
            game.queue_move("g1a7")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("b8a8")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("a7g1")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("a8b8")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("g1a7")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("b8a8")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("a7g1")
            game.handle_player_move()
            renpy.pause(0.5)
            game.queue_move("a8b8")
            game.handle_player_move()
            renpy.pause(2)
        m 1lub "Now, since the exact repeat position has been presented three times, the game will be judged a draw."
        m 1eua "White could have used the advantage of an extra rook to win the game, but only ended up having a draw."
        m 1eua "That's the example of this term."
        m 1eub "Notice that this rule requires the exact same position. Even a tiny difference won't be allowed to reach this draw."
        m 3eub "For example, even though the positions of the pieces are completely unchanged, the king loses the possibility of castling in one repetition."
        m 3eua "Then, this is not seen as quite the same."
        $ game.hide()
        m 1eua "[random_dialogue]"
        return

    label .underpromotion:
        m 1eud "You know pawns can promote to a queen, and queen is the most powerful piece."
        m 1euc "But there is some cases that you musn't promote to a queen, otherwise this is not the best move. Sometimes it will even ruin your chance to win."
        python:
            game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/3P1k1P/2q5/8/8/8/5K2/6R1 w - - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 1eub "Like this position, it's white to move, do you think it's the best to promote to a queen?"
        m 1eka "Well, that's not really bad, and white can win after that promotion, too."
        m 1eud "But what if white promoted to a knight?"
        python:
            game.queue_move("d7d8n")
            game.handle_player_move()
        m 1esa "Then, since the opponent has to escape from the check firstly, we can take the queen."
        m 1esb "Isn't this a easier way to win?"
        $ game.hide()
        m 1eua "[random_dialogue]"
        return

    label .zugzwang:
        m 1eub "Zugzwang is a German word. It's a tactic."
        m 1rusdlb "Now that you're asking about it, let me say something in passing. I was actually planning to give you a separate lesson on this, you know?"
        m 1rusdla "But Zugzwang is a relatively \"not-that-important\" tactic, and it can take quite a bit of time to prepare a single lesson."
        m 1rksdlc "And I don't want to keep you waiting too long..."
        m 1husdlb "So my final decision is to introduce them here, I hope you don't mind, ehehe~"
        m 1hub "Anyway, what Zugzwang is referring to is \"a bad move that has to be played\"."
        python:
            game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/2Kp4/3Pk3/8/8/8/8 w - - 0 1")
            game.toggle_sensitivity()
            game.show()
        m 1lud "It's white to move now, but white would wish they can skip their turn."
        m 1luc "Guess why?"
        m 1lua "This is because no matter how white moves their king, they are bound to lose their pawn."
        m 1eua "And to lose a pawn means to lose the possibility of winning in this endgame."
        python:
            game.queue_move("c6c7")
            game.handle_player_move()
        m 3eub "Unfortunately, rules are rules, and the rule is that players can't skip their turn. White has to move the king helplessly."
        python:
            game.queue_move("e5d5")
            game.handle_monika_move()
        m 3lua "Then, black happily take the pawn, which means black is already winning as long as they played correctly."
        m 1lub"Similarly, if black moves first here, then it's white to win."
        m 1eub "This \"reluctant but must bad move\" is called zugzwang."
        $ game.hide()
        m 1eua "[random_dialogue]"
        return
    return

label monika_chesslesson_terms_end:
    show monika at t11
    m 1eub "Okay!"
    m 1hub "If there is any term you somehow forget, feel free to ask me again!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_whenwin",
            category=["chess lessons"],
            prompt="How to win a game?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_whenwin:
    m 3duc "Hold on, let me get the board ready.{w=0.1}.{w=0.1}.{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/3k4/8/8/1R3K2/6R1 w - - 0 1")
        game.toggle_sensitivity()
        game.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m 2eub "Now look at the board! You can see that the black is at a huge disadvantage, right?"
    m "Yes, black has only king {i}one{/i} piece, but white has two rooks still!"
    m 2eud "But, is white win {i}now{/i}?"
    m 2esu "Actually, not yet."
    m 2esd "That's the question we're going to ask:{w=0.1} When will we win in Chess?"
    m 2eub "The answer is, when the opponent's king is {i}checkmated{/i}."
    m "If an opponent is {i}checkmated{/i}, his king is now in a position where he can be attacked, and he can't get out of the situation even after his turn."
    m 2esu "That's {i}checkmate{/i}!"
    m 2lsc "Now,let us checkmate black.{w=0.1}.{w=0.1}.{nw}"

    # Make a ton of moves.
    python:
        game.queue_move("b2b4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("d5c5")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("b4h4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("c5d5")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("g1g5")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("d5e6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("h4h6")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("e6f7")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("h6a6")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("f7e7")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("g5g7")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("e7f8")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("g7b7")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("f8g8")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("a6a8")
        game.handle_player_move()
        renpy.pause(0.5)

    m 2esb "Black is now {i}checkmated{/i}!"
    m 2eub "To understand why, let us see this.{w=0.1}.{w=0.1}.{w=0.1}{nw}"

    #Highlight the lines that rooks are attacking.
    python:
        for i in ['a','b','c','d','e','f','g','h']:
            game.request_highlight("{0}{1}".format(i, 1))
            renpy.pause(0.01)
        for i in ['a','b','c','d','e','f','g','h']:
            game.request_highlight("{0}{1}".format(i, 2))
            renpy.pause(0.01)
        
        renpy.pause(0.5)
    
    m "See? White has two rooks to control two lines.{w=0.1} Black's king is now being attacked.{w=0.1}.{w=0.1}.{nw}"
    extend 2euu "And there is no way black can get out of this now!"
    m 2etu "Wherever black is going, black is still being attacked!"
    m "This is a {i}checkmate{/i}--{w=0.1}And now, we won the game."
    m 1eub "And this checkmate is the famous {i}\"Two Rook Mate\"{/i},{w=0.2} I'm going to introduce it in other lessons."
    m "For now, I think it's enough for today."
    
    # Make the board disappear. Let Monika back to where she was.
    $ game.hide()
    show monika at t11

    m 1hua "Thanks for listening~"

    return 

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_basic_pawn",
            category=["chess lessons"],
            prompt="Pawn - Basic",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_basic_pawn:
    m 1eub "Different from what many beginners think, pawn is actually the most complicated chess piece."
    m 1hua "So, if you find it a little hard, that's fine."
    m 3duc "Now, just let me get the board...{w=0.3}{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        game = MASChessDisplayableBase(is_player_white=True)
        game.toggle_sensitivity()
        game.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m 2hub "Here we are!"
    m 2eub "Pawns are important pieces in chess, too."
    m "Every time a game starts, your strong pieces are protected by eight pawns."
    m 2rusdlb "It's not hard to imagine what if we have no pawns to protect us, but our opponent keep them still..."
    m 2rusdla "Opponent will soon free their strong pieces into a good position, and launched an unscrupulous attack on our pieces..."
    m "But pawns are not only a protector. {i}Pawns can move and attack, too{/i}!"
    m 2eub "Pawns can {i}only move directly in front of themselves{/i}...{w=0.5} Well, {i}except a special positon{/i}. I will talk about this later."
    m 2eua "If a pawn never moved before, then this pawn can move 2 squares as its first movement."
    m 2hua "But if you don't want to let it move 2 squares, then it's still okay. You can let it move 1 square only."
    m 2lua "So, now focus on the d2 pawn...{w=1.0}{nw}"

    python:
        game.request_highlight("{0}{1}".format('d', 6))
        renpy.pause(0.5)
        game.request_highlight("{0}{1}".format('d', 5))
        renpy.pause(2)
    
    m 2lub "These two highlighted squares is this pawn's movable range."
    m 2lua "Now, let us choose two move 2 squares.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    python:
        game.remove_highlight("{0}{1}".format('d', 5))
        game.remove_highlight("{0}{1}".format('d', 6))
        game.queue_move("d2d4")
        game.handle_player_move()
        renpy.pause(2)

    m 2lub "Okay, this pawn moved now!"
    m 2etc "But you are probably wondering, what's the point of this?"
    m "Since pawn is probably a protector, so are we simply moving this pawn to a position where can protect us better?"
    m 2esu "Not really!{w=1.0} Remeber what I said? {i}Pawns can fight too{/i}!"
    m 2lsu "Let me gave you an example.{w=0.1}.{w=0.1}.{w=0.3}{nw}"

    python:
        game.queue_move("e7e5")
        game.handle_monika_move()
        renpy.pause(2)

    m 2esb "Here we are! The opponent moved e7 pawn to e5, which is abandoning this pawn!"
    m 2lsu "To see why, let us see where can our pawn move now..."

    python:
        game.request_highlight("{0}{1}".format('e',4))
        game.request_highlight("{0}{1}".format('d',4))
        renpy.pause(2)

    m 2tsu "You are probably wondering, {i}how is this happening?{w=0.5} Isn't pawns only able to move directly in front of themselves?{/i}"
    m 2eub "This is the exception!{w=0.1} When a pawn's diagonal front is next to an opponent's piece, it can remove that piece and replace it!"
    m 2lua "So we can now take this e5 pawn like this:{w=0.5}{nw}"

    python:
        game.remove_highlight("{0}{1}".format('e',4))
        game.remove_highlight("{0}{1}".format('d',4))
        game.queue_move("d4e5")
        game.handle_player_move()
        renpy.pause(2)

    m 2eub "This is how pawn fights!{w=1.0}{nw}"
    extend 2hksdrb "Though it's strange to understand...{w=1.0}{nw}"
    m 2rusdrb  "Maybe this fact can help you to understand: In Roman marching lines, one soldier held a huge shield and the other an offensive weapon."
    m "So a soldier usually kills his enemy from a sideswipe."
    m 2eua "Anyways, let us back to the board..."
    m 2eub "Pawns also have a special move called {i}En Passant{/i}, a french name."
    m "If the opponent's pawn moved 2 squares as its first move, and this movement make this pawn beside your pawn after finished..."
    m 2esb "Then you can move your pawn to the back of the pawn that your opponent just moved, and remove that pawn."
    m 2esc "But there is a special rule..."
    m "If you want to do {i}En Passant{/i}, you have to take pawns immediately after the opponent's move, otherwise you lose your chance."
    m 1rsc "This may be explained by... The first time a pawn moves two squares, it's on a rush march, unprepared, and your pawn is there to ambush it."
    m "If you don't ambush it right away, it will rest and make you lose the chance of a sneak attack."
    m 1rssdlu "...Man, chess is really complicated in a way!"
    m 1lsb "Anyways, let us look at this example:{w=1.0}{nw}"

    python:
        game.queue_move("f7f5")
        game.handle_monika_move()
        renpy.pause(2)
    
    m 3lsb "Because this pawn moved two squares, and that pawn is just at the hand of your pawn..."
    m "We can do the {i}En Passant{/i} now."
    
    python:
        game.queue_move("e5f6")
        game.handle_player_move()
        renpy.pause(2)

    m 2eua "See?{w=1.0} And now, let us cancel this movement,{w=1.0}{nw}"
    extend 2duc "take another movement...{w=1.0}{nw}"
    
    python:
        # Make the old one disappear, and get a new one to "cancel this movement".
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="rnbqkbnr/pppp2pp/8/4Pp2/8/8/PPP1PPPP/RNBQKBNR w KQkq f6 0 3")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)

        game.queue_move("f2f4")
        game.handle_player_move()
        renpy.pause(1)

        game.queue_move("g7g6")
        game.handle_monika_move()
        renpy.pause(1)
    
    m 2eub "We moved another pawn! And the opponent moved another pawn, too!"
    m 2eud "Even though it's our turn now, we can not take the f5 pawn by \"En Passant\" anymore!"
    m 2eub "This is the special rule of \"En Passant\", we must take that pawn immediately, otherwise we can not take that pawn anymore."
    m "We can only move forward now."
    m 3eub "And, there is still another special rule of pawns..."
    m 3hksdra "...Don't worry, this is the last special rule of pawns, I promise."
    m 3lksdra "To see this special rule, let us keep moving forward...{w=1.0}{nw}"

    python:#Keep moving forward till the pawn reached the last line
        game.queue_move("e5e6")
        game.handle_player_move()
        renpy.pause(1)

        game.queue_move("g6g5")
        game.handle_monika_move()
        renpy.pause(1)

        game.queue_move("e6e7")
        game.handle_player_move()
        renpy.pause(1)

        game.queue_move("g5g4")
        game.handle_monika_move()
        renpy.pause(2)

    m 2eua "Okay, let us pause here..."
    m 2wud "The pawn is going to reach the last line!{w=0.3} Is this pawn going to be useless then?"
    m 2euu "Actually, no.{w=1.0} In fact, this pawn is about to play to its full value:"

    python:
        game.queue_move("e7f8q")
        game.handle_player_move()
    
    m 2etu "..."
    m "I know what you are thinking about:{w=1.0}{nw}"
    extend 2ltd "{i}What is this now? Did my eyes cheat on me?{/i}"
    m 2esb "Relax, [mas_get_player_nickname()]~ This is the last special rule: {i}Promotion{/i}."
    m "When a pawn reaches the last line, it can be promoted into any piece except pawn and king."
    if seen_event("monika_chesslesson_intro_basic_queen"):
        m 3esb "And as I told you, queen is the most powerful piece."
    else:
        m 3esb "Queen is the most powerful piece."
    extend " So we usually make our pawns queens."
    m 3rsd "Well, I don't have a very good realistic interpretation of this rule...{w=1.0}{nw}"
    extend 3esb "But this rule is easy to remember, right?"

    # Make the board disappear. Let Monika back to where she was.
    $ game.hide()
    show monika at t11

    m 1hua "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_basic_bishop",
            category=["chess lessons"],
            prompt="Bishop - Basic",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_basic_bishop:
    m 1eub "In this lesson we're going to talk about bishops."
    m 1eua "Bishops are powerful pieces in chess and can be quite a threat when used well."
    m 1eub "But for now, let us simply learn how to move bishops."
    
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "2b2b2/8/8/8/8/8/8/2B2B2 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    
    m 1lub "This is the chess board after removing all the pieces except the bishop."
    m 3eub "There are two kinds of bishops, light-squared bishops and dark-squared bishops."
    m 3eud "None of the other pieces will be distinguished between bright and dark squares, so why should the bishop?"
    m 1esa "It has to do with the way they move."
    m 1esd "Bishops can only move diagonally, so if you were to ask me to mark the moveable square of the current 4 bishops...{w=0.3}{nw}"
    python:
        game.request_highlight_diagonal("a3","c1")
        game.request_highlight_diagonal("c1","h6")
        game.request_highlight_diagonal("a6","c8",color = highlight_type_green)
        game.request_highlight_diagonal("c8","h3",color = highlight_type_green)
        game.request_highlight_diagonal("a6","f1")
        game.request_highlight_diagonal("f1","h3")
        game.request_highlight_diagonal("a3","f8",color = highlight_type_green)
        game.request_highlight_diagonal("f8","h6",color = highlight_type_green)
    extend 1lsc " that would be something like this."
    m 1eub "Now that I've highlighted it, I want to let you notice one thing.{w=0.3} {i}On a chess board, the squares on the same diagonal line are always the same color{/i}."
    m 1eua "So, in conclusion, if a bishop starts out on a light square, it will always only be on a light square."
    m 1hua "The same is true of the dark-squared bishop, of course."
    m 3eub "The advantage of this classification is that you can immediately know which pieces are likely to be threatened by that bishop."
    m 1eub "For example...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "3B1B2/B1B5/5B2/3k4/1B6/6B1/3B4/B5B1 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    
    $ temp_nickname = mas_get_player_nickname()# Make sure the nickname is persistent while questioning.

    extend 1efa " Pop quiz!{w=0.5}{nw}"
    extend 1efa " [temp_nickname], do you think it is possible for the white to attack the black king?{w=0.2}{nw}"
    $ _history_list.pop()
    #TODO: If the player doesn't answer for more than five seconds, the question ends. After all, this is a 'pop quiz'.
    #      I looked at mas_background_timed_jump, but I found it need a few extra labels to reach this effect. 
    menu:
        m "For example... Pop quiz! [temp_nickname], do you think it is possible for the white to attack the black king?{fast}"
        "Yes.":
            m 1etsdrb "Hmm...{w=0.2} Sorry, [player], but you picked the wrong answer."
        "No.":
            $ mas_gainAffection()
            m 1hub "Yes, that's the correct answer!"
    m 3eub "Notice, in this case, that all bishops{w=0.2}--notice, I says all--{w=0.2}of the opponent are dark-sqaured bishops."
    m 1eub "This means that the opponent cannot have any attack ability against the light-squared pieces!"
    m 1hua "Now you should be able to see the use of the distinction between light and dark for bishops."
    m 1eua "Finally, note that bishops, like all chess pieces except knights, cannot go over a piece to reach the other side of that piece."
    m 1lub "Another example...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/8/3B4/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    extend 3lub  " At the moment, if we were to highlight the bishop's moveable squares, it would be...{w=0.3}{nw}"
    python:
        game.request_highlight_diagonal("a1","h8")
        game.request_highlight_diagonal("a7","g1")
    extend 1eua " these squares."
    m 1eud "However, if we place any piece, say a pawn, on one of the diagonals, the situation immediately changes."
    m 1luc "Let's place a pawn here...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/5p2/8/3B4/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        game.request_highlight_diagonal("a1","h8")
        game.request_highlight_diagonal("a7","g1")
    extend 1lud " then the bishop's moveable range should be crossed out a few squares,{w=0.3}{nw}"
    python:
        game.remove_highlight_common_format("g7")
        game.remove_highlight_common_format("h8")
    extend 1eua " like this."
    m 3eub "This is because the bishop cannot directly go over a piece to the other side."
    m 1eub "Given that the pawn is a black pawn and the bishop is a white bishop, the bishop can take that pawn's place in this turn, and then move in the next turn."
    m 1eua "These should suffice for a basic introduction to the bishop."
    m 1hua "Remember:{w=0.2} {i}bishops can only move diagonally and cannot go directly over pieces{/i}."
    show monika at t11
    $ game.hide()
    m 1hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_basic_knight",
            category=["chess lessons"],
            prompt="Knight - Basic",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_basic_knight:
    m 1eub "In this lesson, we're going to focus on the knight."
    m 1eud "Knight is the only special case of chess in which it is possible to cross over a piece to attack another piece."
    m 1eua "Let me explain it in detail.{w=0.3}{nw}"
    extend 1duc " Firstly, let me set the chessboard...{w=0.5}{nw}"
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/3N4/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 1eub "The knight moves two squares in any non-diagonal direction and then one square in the vertical direction of that direction."
    m 1hua "This concept may sound particularly strange, so let me explain it more specifically for you."
    python:
        game.request_highlight_common_format("e5")
        game.request_highlight_common_format("f5")
    m 1lub "Let's take moving to the right for example. First of all, move to the right two spuares."
    m 1lua "Then, the direction perpendicular to the \"right\" is, of course, up or down."
    python:
        game.request_highlight_common_format("f6")
    m 1eub "In this case, let us choose to go up, so our final position is f6 square."
    python:
        game.remove_highlight_all()
    m 1hua "The same goes for the other direction.{w=0.3}{nw}"
    python:
        game.request_highlight_common_format("d6")
        game.request_highlight_common_format("d7")
    extend 1eub " For example, if we choose to start with the direction up this time, we'll move up two squares."
    m 3eub "Then, the vertical direction in the \"up\" direction is naturally left or right, so we can choose to go left or right one square."
    python:
        game.request_highlight_common_format("c7")
    m 3lub "If we choose to the left, then, of course, the final target is c7 square."
    m 3eud "Note that after moving two squares, you {i}cannot{/i} choose not to move one square in the vertical direction."
    m 2luc "So, if I were to highlight all the squares on the chessboard that the knight could now move...{w=0.2}{nw}"
    python:
        game.remove_highlight_all()
        game.request_highlight_common_format("b4")
        game.request_highlight_common_format("b6")
        game.request_highlight_common_format("c3")
        game.request_highlight_common_format("c7")
        game.request_highlight_common_format("e7")
        game.request_highlight_common_format("e3")
        game.request_highlight_common_format("f6")
        game.request_highlight_common_format("f4")
    extend 1eua " it would be this."
    m 1eud "This type of movement is also named as \"L-shaped movement\"."
    m 1hua "Maybe this name will help you remember it better."
    m 1eub "And then, back to what we were talking about. As I mentioned at the beginning of this lesson, the knight is the only special case where you can move over another piece."
    m 1duc "Hold on...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/2ppp3/2pNp3/2ppp3/2q5/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 1eub "Take this situation. The knight was closely surrounded by black pawns."
    m 1eud "But that can not prevent the knight from moving."
    m 1rtd "If you ask me why knights are so special..."
    m 1rtc "My personal understanding is to think of the chess board as a battlefield, and the knight is an elite riding a warhorse on the battlefield."
    m 1euc "Thanks to their horses, they can easily jump through enemy lines to get where they want."
    m 1hksdrb "...Well, I said that, but I'm not sure. It's perhaps all for game play."
    $ game.hide()
    show monika at t11
    m 1hua "Anyways, this should suffice to say a brief introduction to the knights."
    m 1hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_basic_rook",
            category=["chess lessons"],
            prompt="Rook - Basic",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_basic_rook:
    m 1eub "Rooks are powerful pieces in chess."
    m 1lub "Just a second.{w=0.1} Let me set the chessboard out...{w=0.3}{nw}"
    show monika 1lua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/3R4/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 3eub "Rook is the second most powerful chess piece after queen."
    python:
        game.request_highlight_line(5)
        game.request_highlight_file('d')
    m 3lub "See these highlighted squares?"
    m 3eua "They are all within the control of the rook at this point."
    m 1eub "Rooks can move any number of squares horizontally or vertically, as long as there is nothing blocking them in the path."
    m 1eua "In other words, rooks can move to any square in its current file or line if no block in their path."
    m "In this case, line 5 and d-File."
    m 1eud "If there is a piece in their movable path that blocks them, they must first remove that piece from that position or they cannot directly reach the other side."
    m 1duc "Let me put a few pieces on the chessboard to illustrate the point...{w=0.5}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/3p4/8/1p1R2n1/3b4/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        game.request_highlight_common_format("d5",highlight_type_green)
        game.request_highlight_common_format("c5")
        game.request_highlight_common_format("d6")
        game.request_highlight_common_format("e5")
        game.request_highlight_common_format("f5")
        game.request_highlight_common_format("b5",highlight_type_red)
        game.request_highlight_common_format("d7",highlight_type_red)
        game.request_highlight_common_format("d4",highlight_type_red)
        game.request_highlight_common_format("g5",highlight_type_red)
    extend 1lub " Okay, see? Since there are pieces in its moveable path, it will be blocked by them, so its range of motion should now look like this."
    m 1eua "In general, the rook's way of moving is relatively easy to understand."
    if seen_event("monika_chesslesson_intro_basic_king"):
        m 1rtd "The only thing that might be a little complicated is the castle...{w=0.2}{nw}"
        extend 1rua " but you've already learned that in king's introduction."
    else:
        m 1rtd "But there is a special movement which I didn't mention...{w=0.2} It's called {i}castle{/i}."
        m 1esd "Castle is a special case of chess. It is the only move in which two pieces can be moved simultaneously."
        m 1esc "And by \"two pieces\", I mean the rook and the king."
        m 1rtd "Because of its strategic significance...{w=0.2}{nw}"
        extend 1eub " Personally, I think it should have been included in king's introduction."
        m 1hua "If you want to learn what castle is, let's introduce it to you in other lesson!"
    $ game.hide()
    show monika at t11
    m 1hua "These should be a brief introduction to rook."
    m 1hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_basic_king",
            category=["chess lessons"],
            prompt="King - Basic",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_basic_king:
    m 1esd "King is the most important chess piece."
    m 1esc "It doesn't matter how many pieces you capture or how good your previous moves are, they won't decide the winner."
    m 3esd "As long as your king is attacked and there is no way you can recover from the attack, you are lost."
    m 1eua "This \"attack on the opponent's king\" move is called a \"check\"."
    m 1eub "If the attack not only attacks the opponent's king, but also makes it impossible for it to escape, it's called a \"checkmate\"."
    m 1esb "But, of course, king is certainly not completely worthless. Kings also have their own way of moving."
    m 1duc "Just let me get the board here...{w=0.3}{nw}"
    show monika 1lua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/3K4/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 1eub "The king can move to any square around it."
    m 1rtc "So, if you want me to highlight the king's current range of movement...{w=0.3}{nw}"
    python:
        game.request_highlight_common_format("c6")
        game.request_highlight_common_format("c5")
        game.request_highlight_common_format("c4")
        game.request_highlight_common_format("d6")
        game.request_highlight_common_format("d4")
        game.request_highlight_common_format("e6")
        game.request_highlight_common_format("e5")
        game.request_highlight_common_format("e4")
    extend 1eub " it would be these."
    m 1eub "In addition, the king can never move to a square that is currently being controlled by the opponent."
    m 1eua "In other words, you can't just send your king into an opponent's attack."
    m 1esb "In general, the movement of the king is quite simple."
    m 1rtc "But the king also had a special move."
    if seen_event("monika_chesslesson_intro_basic_rook") and mas_getEV("monika_chesslesson_intro_basic_king").shown_count == 0:
        m 3eud "As I mentioned to you in the introduction to rooks, this special move called {i}castle{/i}."
    else:
        m 3eud "This special move called {i}castle{/i}. A move that moves both a king and a rook."
    m 3eua "It is the only special case of chess that allows you to move two pieces at the same time."
    m 1eub "In order to \"castle\", the following conditions must be met simultaneously."
    m 1eua "{i}1. Both king and the rook you are going to move never move in this game.{/i}"
    m "{i}2. There are no pieces between the king and the rook.{/i}"
    m "{i}3. The king cannot be under attack at this point --{w=0.3} in other words, the castle cannot be used as a means of escaping check.{/i}"
    m "{i}4. After the castle is over, the king cannot be under attack by the opponent.{w=0.2} And in this castle, squares that your king going to pass can't being attacked.{/i}"
    m 1eub "Once all of these conditions are met, you can move your king two squares towards the rook that satisfies the condition, and then move the rook over to the other side of the king and close to the king."
    m 1eua "This stuff sounds pretty complicated, so let me give you a concrete example."
    m 1duc "Wait a moment...{w=0.3}{nw}"
    show monika 1eua
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 3 3")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 2eub "This game is a famous opening called {i}Italian Game{/i}. I will give a special lesson on the details of the Italian Game in the future."
    m 2eua "In Italian Game, white promptly dispatched its king side knight and bishop. This satisfies castle's condition 2: {i}There are no pieces between the king and the rook.{/i}"
    m 2rtc "Although in Italian Game, it's usually black's turn up to this point, but for the sake of learning about castle, let's just assume it's still white's turn."
    m 2esb "Since white meets all four conditions, white can now play the castle move."
    m 4eub "Firstly, {i}move your king two squares towards the rook{/i}, so the situation turns into...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQ2KR w kq - 3 3")
        game.toggle_sensitivity()
        game.show()
    extend 4eua " this."
    m 4eub "Secondly, {i}move the rook over to the other side of the king and close to the king{/i}.{w=0.3} It would be...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQ1RK1 w kq - 3 3")
        game.toggle_sensitivity()
        game.show()
    extend 4hua " this."
    m 2hub "This is what castle looks like."
    m 2eub "Of course, since there are two rooks, there are also two possibilities for castle. One is the King Side Castle, and the other is the Queen Side Castle."
    m 2eua "King Side Castle is also called as short-castle, and the Queen Side Castle was called as long-castle."
    m 2rtc "As to why one is called long and one is called short...{w=0.3}{nw}"
    extend 2eub " Well, that's an interesting reason, but it's not that relevant to this lesson, so we'll leave that out for now."
    m 2eua "The current one is King Side Castle because you moved the rook on the king side."
    m 4eub "As for Queen Side Castle? Well, it's the same way!"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bq1rk1/pp2ppbp/2np1np1/8/3NP3/2N1BP2/PPPQ2PP/R3KB1R w KQ - 1 9")
        game.toggle_sensitivity()
        game.show()
    m 4eua "This is a common situation in the {i}Dragon Variation{/i} of {i}Sicilian Defense{/i}."
    m "Sicilian Defense is also a very popular opening in chess, and I will teach you a lesson on it in the future."
    m 1eub "Anyway, as you can see, at this point, white also satisfies all the conditions for the castle."
    m 4hub "So, the same thing--{w=0.3}move the king two squares,{w=0.2} move the rook over,{w=0.2}{nw}"
    python:
        game.queue_move("e1c1")
        game.handle_player_move()
    extend 4eua " done."
    m 1etd "Now, after introducing what it is, you might be wondering, what's the point of this so-called castle?"
    m 1esb "Castle has two main points. First of all, one thing is clear: Chess is often a very intense game, especially in the competition of the center."
    m 3esa "Either king side or queen side, castle takes the king closer to the edge of the board, and usually, after the castle, the king is protected by several unmoved pawns in front of it."
    m 4esb "Castle also brought the rook, a hard-to-develop chess piece, closer to center. And the center, where competition is fierce and the situation is open, is a good place for rook to perform."
    m 1esb "So castle is usually very popular, and has been used in many opening games."
    m 1rsd "Then, if you want to ask me which is better, King Side Castle or Queen Side Castle...{w=0.3}{nw}"
    extend 1eub " right now, I can only roughly say that there is no absolute answer. We'll talk more about it in the future."
    show monika at t11
    $ game.hide()
    m 1hua "I think these are enough for a lesson."
    m 1hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_basic_queen",
            category=["chess lessons"],
            prompt="Queen - Basic",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished') and mas_chessteaching.player_know_about_chess() == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_basic_queen:
    m 1eua "Talking about queen, queen is the most powerful piece in chess."
    m 1eub "Just let me get the board, then I can show you how powerful it is."
    m 1duc "...{w=0.3}{nw}"
    show monika at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/3Q4/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    extend 1hua " Alright!"
    m 1hub "As the most powerful piece, the queen can move any number of squares in any direction!"
    m 1duc "So, if you want me to mark the moveable range...{w=0.3}{nw}"
    python:
        game.request_highlight_line(5)
        game.request_highlight_file('d')
        game.request_highlight_diagonal("a8","h1")
        game.request_highlight_diagonal("a2","g8")
    extend 3eub " it would be these squares!"
    m 3hub "Slant or straight, the queen can go!"
    m 1esb "But, of course, like all chess pieces with the exception of the knight, the queen cannot go direct over a piece."
    m 1lub "In other words, if we put a pawn in this position,{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/3Q1P2/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        game.request_highlight_line(5)
        game.request_highlight_file('d')
        game.request_highlight_diagonal("a8","h1")
        game.request_highlight_diagonal("a2","g8")
    extend 1lua " then the queen's mobility would be limited."
    m 1lud "Its moveable range would turn into...{w=0.3}{nw}"
    python:
        game.remove_highlight_common_format("g5")
        game.remove_highlight_common_format("h5")
    extend 1eua " these."
    m 1eub "Now that I've finished talking about how it moves, I want to make a couple of points by the way."
    m 1rtc "On why the queen is so powerful...{w=0.3}{nw}"
    extend 1esd " There are some interesting historical reasons to tell you about."
    m 1esb "The name of the piece now known as Queen has actually been changed many times. For a time, this piece corresponds to the name of Minister."
    m 1esa "I've also heard it used to be called General or Lawyer."
    m 1esc "On why the name changed to queen...{w=0.3} There doesn't seem to be an accurate study. Personally, I think it's the rise of women's rights theory."
    m 1essdla "Anyway, I haven't done a lot of research on this, and maybe I'm wrong. You can check it out later."
    m 1eub "Now, let's talk about the point of being part of a board game."
    m 1ltd "There are many beginners like to move the queen as early as possible, which is not quite right."
    m 3esd "Admittedly, the queen is a very big threat to opponent, but in opening, the game is not completely open."
    m 3esc "What is the queen to do at this time? Just to come out and exchange one or two unimportant pieces?"
    m 3eua "I'll show you a game to tell you you why move queen early doesn't work."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/ppp1pppp/8/3p4/8/4P3/PPPP1PPP/RNBQKBNR w KQkq d6 0 2")
        game.toggle_sensitivity()
        game.show()
    m 1eub "Let's say white is a impatient boy who loves to use the queen."
    python:
        game.queue_move("d1h5")
        game.handle_player_move()
    m 3eub "This beginner immediately called out his queen on the second move, thinking he could make his mark."
    m 1esd "This is also a common thought for many beginners. They thought that the queen, who was such a powerful piece, should be called out immediately, and would be of great use."
    m 1eub "This boy's opponent, however, is not in a hurry, and knows that the queen's chances of checkmating in the opening game are limited to situations in which the opponent is unskilled."
    m 1eua "So, the opponent played a knight move.{w=0.3}{nw}"
    python:
        game.queue_move("g8f6")
        game.handle_monika_move()
    extend 1eub " This move brings the knight into battle and attacks the queen."
    m 1esa "The boy saw things are not too well, so he wanted to take the queen back."
    python:
        game.queue_move("h5f3")
        game.handle_player_move()
    m 1eub "This idea was nothing wrong, but he was not reconciled to this, so he did not take the queen back completely, but only backed away a few squares."
    m 1eta "What he didn't realize, however, was that putting the queen in such a position would prevent his knight from coming out."
    m 1etb "And his opponent? The opponent has already moved the knight to a good position, developed materials. The queen did nothing but escaping."
    m 1eua "He spent one turn moving his queen, the other running the queen away, giving his opponent plenty of time to develop."
    m 1rud "Of course, this example is not the best...{w=0.3} But anyway, that's the bad thing about sending the queen too early."
    m 1esd "That is, {i}the queen usually can't do anything, the player just wastes the precious turn{/i}."
    m 1etb "Oh, you may also have seen someone move the queen early and you lost pretty terrible, that's usually because they know you're not a very good player so they can take risky moves."
    m 1hua "Anyway, my personal advice is--{w=0.3}don't move the queen too soon."
    show monika at t11
    $ game.hide()
    m 1hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_opening_basic_idea",
            category=["chess lessons"],
            prompt="Opening: Basic idea",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_opening_basic_idea:
    m 2eud "This lesson will be a lesson really need to listen carefully, [player]."
    m 2euc "And this lesson will not be a short one."
    m 2eua "So, I want to make sure that you have enough time right now, so that you don't get distracted while you're listening."
    m "Do you think you have enough time now?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you think you have enough time now?{fast}"
        "Yes.":
            m 2hua "Great!"
            m 2eub "Then we may begin this lesson now."
        "No.":
            m 2eka "Well, then let us learn this later!"
            m "After all, it is much more effective to listen to one class carefully than to listen to ten classes carelessly."
            m 2hub "But anyways, thanks for asking a lesson!"
            return
    m 2eud "Oh, and, before I begin, I want to mark a few statements."
    m 7eud "Learning the opening is not just about memorizing moves and moves mechanically. The focus is on understanding them."
    m 7euc "Also, learning about openings tends to benefit you not just in the opening phase, but in all aspects."
    m 7esd "The idea of opening through thousands of years of research has been quite thorough, so the existing recognized opening is mostly the embodiment of good thinking."
    m 7eua "I hope you keep these points in mind and realize the use of learning openings."
    m 2eua "Now, let's get down to the main."
    show monika at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True)
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 2eub "This is what it looks like at the beginning of each game."
    m 2esa "What should we do?"
    m 2esb "The answer is, {i}develop materials, control center{/i}."
    m 2eua "{i}Develop materials{/i} the term basically stands for move your pieces to a good position that can make the most of them."
    m 2eua "As for {i}control center{/i}, this is pretty self-evident."
    m 4esb "This sentence can be said to be the basic principle of opening.{w=0.3} {i}Develop materials, control center{/i}. Remember it well, it's really useful!"
    m 2eub "You may have already found that the first half of the sentence and the second half are actually in a sense the same."
    m 2eua "When you develop materials, you basically are putting them in places where you can control as much of squares as possible."
    m 2etd "But, why do we want to control as many squares as possible?"
    m 2rtd "I don't know if you've ever experienced this situation...{w=0.3}{nw}"
    extend 2eud " the game looks okay, you don't have a material disadvantage, but you just don't know what to do. Nothing seemed to make sense."
    m 2euc "This is usually because your opponent is controlling too many squares."
    m 2hua "If you can control many squares as well, your opponent will be severely restricted too! At the same time, you can build on this advantage...{w=0.3}{nw}"
    extend 2wub " It's a snowball effect!"
    m 7eud "Though, first thing we need to notice is that control squares should be control {i}central{/i} squares."
    m 7lub "Why central? See this.{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/8/8/8/8/1N6 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    extend 7eub " Here is a knight in its initial position. How many squares can it control?"
    python:
        game.request_highlight_common_format("a3")
        game.request_highlight_common_format("c3")
        game.request_highlight_common_format("d2")
    m 7hua "The answer is 3 squares, a3, c3, d2."
    m 2eub "And then imagine the knight taking a turn to move out.{w=0.3}{nw}"
    python:
        game.remove_highlight_all()
        game.queue_move("b1c3")
        game.handle_player_move()
    extend 2etb " Now, how many squares does it control?"
    python:
        game.request_highlight_common_format("a2")
        game.request_highlight_common_format("a4")
        game.request_highlight_common_format("b1")
        game.request_highlight_common_format("b5")
        game.request_highlight_common_format("d5")
        game.request_highlight_common_format("d1")
        game.request_highlight_common_format("e4")
        game.request_highlight_common_format("e2")
    m 2eua "It turns into 8 squares now. This is because the knight is closer to the center now."
    m "Knights are more powerful in center!"
    m 2hua "Actually, not only knights, but also others are probably more powerful in the center."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/8/8/8/8/Q7 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 2eub "Taking the queen as another example. In the corner, the queen controls 21 sqaures.{w=0.3}{nw}"
    python:
        game.request_highlight_file('a')
        game.request_highlight_line(1)
        game.request_highlight_diagonal("a1","h8")
    extend 2eua " 21 squares, indeed, it's powerful. But what if the queen is in center?"
    python:
        game.queue_move("a1d4")
        game.handle_player_move()
        game.remove_highlight_all()
        game.request_highlight_line(4)
        game.request_highlight_file('d')
        game.request_highlight_diagonal("a1","h8")
        game.request_highlight_diagonal("a7","g1")
    m 2hua "Then it's 27 squares! Isn't this a more powerful position?"
    m 2eub "The same goes for the other pieces, and I think you can figure that out for yourself, so I'm not going to give you more example."
    m 2eua "Now let's go back to the opening.{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True)
        game.toggle_sensitivity()
        game.show()
    extend 2esb " Since pieces are probably more powerful in the center, we should try to control the center."
    m 2esa "And if the target is to control the center, what should we do?"
    m 2esb "The option is not only, but the most popular choice is to move pawns."
    m 2esa "Foucs on pawns, we should especially look at d2{nw}"
    python:
        game.request_highlight_common_format("d2")
    extend " pawn and e2{nw}"
    python:
        game.request_highlight_common_format("e2")
    extend " pawn."
    m 2esb "These two pawns are {i}central pawns{/i}. They are really important in the competition of center!"
    m 2rtc "Though, there is a huge difference between these two pawns, like, the d-file pawn has a queen as the defense, while the e-file is weaker than d-file pawn."
    m 2rtd "As such, e2 pawn or d2 pawn openings are often very different...{w=0.3}{nw}"
    extend 2esb " You will feel that in the future."
    m 2esa "To identify them, the d2 pawn is also called Queen's Pawn, and the e2 pawn is King's Pawn."
    m 2eub "Generally speaking, we think it is better to use these two pawns in the opening."
    m 2eua "This is because, you know, pawns are not very valueable pieces after all, but they do control two central squares!"
    python:
        game.remove_highlight_all()
        game.queue_move("e2e4")
        game.handle_player_move()
    m 2lub "See this? We played e4, which controls two central squares,{w=0.3}{nw}"
    python:
        game.request_highlight_common_format("d5")
    extend " d5 square and{nw}"
    python:
        game.request_highlight_common_format("f5")
    extend 2lua " f5 square."
    m 2hua "This seems like an unremarkable move, but it actually immediately controls two central squares!"
    m 2eud "Oh, by the way, we just moved the king's pawn, right?"
    m 2rtd "As I told you, there is king's pawn and queen's pawn...{w=0.3}{nw}"
    extend 2eud " So which one should we move as the first move?"
    m 2esd " In fact, it was a very controversial topic at old time and still is today."
    m 7esd "{i}Bobby Fischer{/i}, a former world champion, thought the king's pawn is the best choice."
    m 2esa "My personal advice is the same. Moving the king's pawn is the best first move."
    m 2rusdla "Of course, this is just my advice, you'll think about it a lot more in the future, and your thinking is not necessarily worse than mine."
    m 2eub "Anyways, after this move I just played, the game turns into King's Pawn Opening."
    m "The first thing this pawn did is to control two central squares, we have already talked about it."
    m 4lua "Something you may haven't noticed is that it frees up the light-squared bishop. This potentially sets the stage for the bishop's development."
    m 4eud "Oh, speaking of this, the activity of bishops is important too, you know? But many beginners will blindly keep pushing pawns, which ruined the activity of bishops."
    m 4eua "To avoid this, always remember that the principle is develop materials {i}and{/i} control center, never one or the other."
    m 2rtc "Simply control the center is not enough, if the cost of controlling the center is to keep your materials out of development, then it'd even be better not to control it at all."
    m 2eua "Then switch to black's view.{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=False, starting_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        game.toggle_sensitivity()
        game.show()
    extend 2etd " How should black side respond to this step?"
    m 2eua "Black's goal is the same as white's, to control the center. So black usually pushes a pawn as well."
    python:
        game.queue_move("e7e5")
        game.handle_player_move()
    m 4eub "For example, e5 is a good choice. This move also controls two central squares, there is nothing wrong with this move."
    m 4hua "Of course, this is certainly not the only option.{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=False, starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        game.toggle_sensitivity()
        game.show()
    extend 4esd " Like this c5 move. This response may come as a surprise to you right?"
    python:
        game.request_highlight_common_format("d4",highlight_type_green)
        game.request_highlight_common_format("b4",highlight_type_green)
    m 4rtc "If you didn't expect this, I can probably guess the reason. Because so far I've told you we should move central pawns to control center."
    m 4esb "Then again, always remember, opening principle is one and only one sentence, and that is {i}develop materials, control center{/i}, not {i}move central pawns{/i}."
    m 2esd "Indeed, b4 the square doesn't seem to be {i}that central{/i}, but it creates a potential space for development."
    m 2esc "The c5 response was well known as the {b}Sicilian Defense{/b}, one of the most popular openings in the world."
    m 2dsc "This move seems mundane, but there is a very deep tactical idea behind it...{w=0.3}{nw}"
    extend 2esb " I'll make a whole class on this opening later, for now, you don't need to understand it."
    m 2eua "Let's go back to white's point of view.{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        game.toggle_sensitivity()
        game.show()
    extend 2eub " Now how should white side respond?"
    m 2hua "The options are immense!{w=0.3}{nw}"
    python:
        game.queue_move("g1f3")
        game.handle_player_move()
    extend 2esb " For example, white can choose to develop knight."
    m 2eub "On the one hand, it develops materials, on the other hand, it strengthens the control of center."
    m 2eua "So here is another personal advice to beginner:{w=0.3} If you don't know what to do, then develop materials."
    m 2hua "Putting your knights or bishops into battlefield may not be a excellent move, but it's usually not a bad one, too."
    m 2eub "Back to the game. As I said, the options are extremely diverse, so white has a lot of options other than developing this knight."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        game.toggle_sensitivity()
        game.show()
        game.queue_move("d2d4")
        game.handle_player_move()
    m 2eua "White can immediately push the d2 pawn into a direct attack. Then the opponent must respond and begin a fierce fight for the center."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        game.toggle_sensitivity()
        game.show()
        game.queue_move("c2c4")
        game.handle_player_move()
    m 2hua "Or this, isn't this a reinforcement to the competition for the center?"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        game.toggle_sensitivity()
        game.show()
        game.queue_move("f1c4")
        game.handle_player_move()
    m "Or develop the bishop right now? This move develops materials, also makes it own sense."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2")
        game.toggle_sensitivity()
        game.show()
        game.queue_move("b1c3")
        game.handle_player_move()
    m "Or who said we can't develop another knight?"
    m 2eua "All these moves have their own sense, all more or less develop materials and control center."
    m "As long as an opening move satisfies 'develop materials' or 'control center', there is always something to be said for it."
    m 2esc "In fact, this kind of thinking works not only for the beginning, but also later."
    m 4esd "Remember, before you play a move, ask yourself, why am I doing this? What's the target of this move? Does this move put my pieces in a better position?"
    m 4etd "If even yourself don't know what you're doing, how can it not be a big blunder?"
    m 4etb "Of course, I know what you're thinking. You are thinking, in fact, you also want to know the sense of each move, but you don't know how to judge, right?"
    m 2hua "That's what learning openings can do. Remember what I said at the beginning of this lesson?"
    m 2hub "{i}The idea of opening through thousands of years of research has been quite thorough, so the existing recognized opening is mostly the embodiment of good thinking.{/i}"
    m 2eua "I have prepared many famous opening lessons for you, [mas_get_player_nickname()], such as {b}Italian Game{/b}, {b}Sicilian Defense{/b}, {b}French Defense{/b}, {b}Queen's Gambit{/b}..."
    m 2hsb "Savor the ideas behind these openings! Trust me, while they are just openings, learning them will benefit your overall situation."
    $ game.hide()
    show monika at t11
    m 2eua "This lesson is just a general introduction to opening."
    m "I know we've only covered some ideas so far, we haven't seen many moves, but the expectations of this lesson are only a basic understanding of the beginning in the first place."
    m 2eub "Again: Try to learn openings. They really are much more important than you think."
    m 1hua "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_opening_italian_game",
            category=["chess lessons"],
            prompt="Opening: Italian Game",
            pool=True,
            conditional="seen_event('monika_chesslesson_opening_basic_idea')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_opening_italian_game:#UNFINISHED
    m 1eub "Italian Game is one of the most common openings, you could say."
    m 1eua "Hold on, I am going to get the board here..."
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True)
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m "In Italian Game, white plays e4 to begin a King's Pawn Opening game.{w=0.3}{nw}"
    python:
        game.queue_move("e2e4")
        game.handle_player_move()
    extend " Then black responds e5,{w=0.2}{nw}"
    python:
        game.queue_move("e7e5")
        game.handle_monika_move()
    extend " pretty normal."
    m "White then plays Nf3,{w=0.3}{nw}"
    python:
        game.queue_move("g1f3")
        game.handle_player_move()
    extend " another netrual move to develop materials and control center."
    m "Since this knight attacks the e5 pawn, black would protect this pawn with Nc6,{w=0.3}{nw}"
    python:
        game.queue_move("b8c6")
        game.handle_monika_move()
    extend " which is also a move to control center and develop materials."
    m "And here, white plays Bc4,{w=0.3}{nw}"
    python:
        game.queue_move("f1c4")
        game.handle_player_move()
    extend " which starts the Italian Game."
    m "From now on, this game is Italian Game."
    m ""
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_opening_sicilian_defense",
            category=["chess lessons"],
            prompt="Opening: Sicilian Defense",
            pool=True,
            conditional="seen_event('monika_chesslesson_opening_basic_idea')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_opening_sicilian_defense:
    m 1duc "Hold on a second...{w=0.5}{nw}"
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 1eub "Sicilian Defense is the most popular response to e4 the move in the world, you could say."
    m 1eua "As I told you before, the King's Pawn Opening is the most popular opening in chess."
    m 3eua "And Sicilian Defense is the dominant response to that opening."
    python:
        game.queue_move("c7c5")
        game.handle_monika_move()
    m 2lub "In Sicilian Defense, black played c5, a very subtle response."
    m 2eua "I have told you that the goal of the opening is to develop materials and control the center."
    m 2esa "So does this black's response achieve that goal?"
    m 2hua "Let us take a view of this board.{nw}{w=0.2}"
    extend 2esb " In this current situation, black does not immediately start a battle with white.{w=0.3}{nw}"
    python:
        game.request_highlight_common_format("d4")
        game.request_highlight_common_format("b4")
    extend 2eub " Instead, black played c5 to control another two central squares."
    m 2hub "I don't know if you can feel it, but it's really a very subtle idea!"
    m 2rtc "After this, the variations is extremely numerous..."
    m 1eud "There are many variations of this opening, for example, Open Sicilian, Closed Sicilian, Alapin Variation, French Variation, Dragon Variation...{w=0.3} It's too many to count."
    m 1euc "Even many chess grandmasters can't claim to have mastered this opening."
    m 1husdra "However, don't worry, this opening is available to all from grandmasters to beginners. Beginners can learn only the main variations of these, but also enough to deal with many matches."
    m 1rtd "I can't say that I really know too much about this opening too...{w=0.3}{nw}"
    extend 1eub " But if you're interested, I'll find time to study them and give you a separate lesson on them later."
    m 1eua "For today, let's just talk about the most common variation: Open Sicilian."
    python:
        game.remove_highlight_all()
        game.queue_move("g1f3")
        game.handle_player_move()
    m 3eub "In Open Sicilian, White developed the knight. It was a natural move to develop materials, control center."
    m 2eua "Black, naturally, goes the same way.{w=0.3}{nw}"
    python:
        game.queue_move("b8c6")
        game.handle_monika_move()
    extend 2eub " Nc6, develop black's materials, control the center, too."
    m 2eua "Then, the white directly hit the center, with d4, start a fierce battle."
    python:
        game.queue_move("d2d4")
        game.handle_player_move()
        renpy.pause(1)
    m 2hua "From here, this is the Open Sicilian variation."
    m 4eua "Generally speaking, after this, black would like to play cxd4,{w=0.5}{nw}"
    python:
        game.queue_move("c5d4")
        game.handle_monika_move()
    extend 4lub " then white responds Nxd4,{w=0.3}{nw}"
    python:
        game.queue_move("f3d4")
        game.handle_player_move()
    extend 4eub " recapture this pawn."
    m 4rusdra "After that, there are so many different possibilities again...{w=0.3} I won't talk about them, because I'm afraid I'm not qualified to talk about them at all."
    m 1eub "Let's just briefly analyze the situation."
    m 3etd "First of all, white loses a pawn, and black loses a pawn too. So, are they in the same situation?"
    m 1hua "Of course not. The positions of the pieces on both sides are quite different."
    m 1esd "What white lost is a central pawn, and for black, it's not a central pawn. Black still keeps two central pawns."
    m 1esc "But white gained a position leading--{w=0.3}Notice white has a pawn in center at this point, while black has no pawn in center."
    m 1eua "So the conclusion is--{w=0.3}As with all openings, neither side is in a obvious disadvantage or advantage."
    m 1eub "Black has a potentially strong competitiveness, but white is ahead and has the initiative."
    m 3eua "This is also characteristic of most of the other variations of Sicilian Defense."
    m 1eub "In general, despite the word defense in its name, Sicilian Defense usually turns into a quite fierce combat."
    if mas_seenLabels("monika_chesslesson_points_3"):
        m 1esa "I've told you before that I personally don't think Sicilian Defense is suitable for beginners, and that's one of the reasons--{w=0.3}it's intense, and beginners can lose pretty badly."
    else:
        m 1esa "So I don't really recommend this opening to beginners."
    $ game.hide()
    show monika at t11
    m 2eub "All in all, Sicilian Defense was a very popular, but also a very complicated opening."
    m 2eua "I will also have some spare time in the near future to take a closer look at the numerous variations of Sicilian Defense, and we will talk more about them later."
    m "As for now, these should be enough."
    m 2hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_advance_bishop",
            category=["chess lessons"],
            prompt="Bishop - Advanced",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_advance_bishop:
    m 1eua "Chess players usually have heard two words frequently:{w=0.2}\"Bad Bishop\" and \"Good Bishop\"."
    m 1etd "But what's the difference between them?{w=0.2}{nw}"
    extend 1eub " Let us find them out today!"
    m 3duc "Hold on a second..."

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r2q1rk1/1b3ppp/p1pbpn2/2pp4/Q2P4/2P1PNB1/PP1N1PPP/R3K2R w KQ - 2 11")
        game.toggle_sensitivity()
        game.show()

    #Give player a few second to look at the board.
    pause 2.0

    m 2euu "Say, [player], do you think there is a bad bishop in this game?{nw}"
    $ _history_list.pop()
    menu:
        m "Say, [player], do you think there is a bad bishop in this game?{fast}"
        "Yes.":
            m 2eub "Yes, there is! The light-squared bishop of black is a bad bishop."
        "No.":
            m 2tuu "Oh, are you sure?"
            m 2tub "Sorry [mas_get_player_nickname()], but there is one bad bishop on b7 square."
    
    m 2eua "As you can see, this bishop's mobility was severely curtailed."
    m "It controls only four squares now: a6, c6, a8, c8."
    m 2eub "Not to mention the fact that a8 and c8 don't need to be controlled at all, it's obviously impossible for white to attack there now."
    m 4esu "In situations like this, what is the difference between this bishop and a...{w=0.8}{nw}"
    extend 4eub "\" tall pawn\"?"
    m 4hub "Ahaha!"
    m 2eub "While this is obvious at a glance, many beginners still don't realize it."
    m 2ruc "They often used the bishop as a tall pawn, which makes their bishops are not being used as they should be."
    m 2eub "Now, let us consider if this bad bishop \"magically\" just moved to f5, is this bishop a bad bishop anymore?"
    m "Of course not!{w=0.2}{nw}"
    extend 4eub " In that case, the bishop would be in an extremely powerful position, controlling so many squares that white would become the one in disadvantage!"
    m 2eub "We would name bishops like this one as \"Good Bishop\"."
    m 2esb "Talking about good or bad bishops, in fact, whether the bishop is in a favorable position is also an important consideration of whether the situation is agressive."
    m "Such as French Defense, which is also a popular beginning, was considered as a passive choice."
    m 2dsa "...{w=0.2}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3")
        game.toggle_sensitivity()
        game.show()
    if seen_event("monika_chesslesson_french_defense") is True:
        extend 2lsb "As you can see, French Defense is known for its unbreakable,{w0.2} but, in fact, the defender has created a bad bishop for itself."
    else:
        extend 2lsb "The current opening in front of you eyes is the French Defense, which is known for its unbreakable.{w=0.2} But, in fact, the defender has created a bad bishop for itself."
    m 2esb "Which bishop is the bad one?{nw}"
    $ _history_list.pop()
    menu:
        m "Which bishop is the bad one?{fast}"
        "The light-squared one.":
            m 2hub "Yes, you are right!{nw}"
            extend 2lub " That bishop is blocked by e6 pawn, which makes it hard to be activated!"

        "The dark-squared one.":
            m 2etd "The dark one?{nw}"
            extend 2etu " Hmmm...{w=0.2} I'm afraid that's not the correct answer."
            python:
                for i in range(3,9,1):
                    game.request_highlight("{0}{1}".format( chr( ord('a')+i-3), 9-i))
            m 2esd "This dark-squared bishop is on the a3-f8 dignaol, which means it controls 5 squares now."
            m 2esc "So this is not a real bad bishop."
            python:
                for i in range(3,9,1):
                    game.remove_highlight("{0}{1}".format( chr( ord('a')+i-3), 9-i))
            m 1lsb "Instead, I think the light-squared one is the bad one."
            m 1esb "This light-squared bishop is blocked by e6 pawn, which makes it's hard to activate this bishop."

    m 2lsa "And since the light-squared bishop is locked, its main function was to stay in its original position to reinforce the defense line."
    m 2esa "Thus, the defender is little passive, while the attacker can be agressive to find a chance to break the defense."
    m 2rtc "However, at the expense of a bishop's mobility to create a line of defense is also really strong.{w=0.2}{nw}"
    extend 2etd " So it's not a bad opening at all."
    m 2dtsdrb "...{w=0.6}{nw}"
    extend 2rtsdrb "Wait a second, we are not going to talk about openings today, right?"
    m 2eusdrb "Sorry to digress a little bit.{w=0.2} Let's get back to the bishop."
    m 2eub "The role that bishop plays in chess usually is a pin that can control squares from a far distance."
    m "Unlike rooks, which are almost impossible to enter into battle in openings. Bishops can be activated in several turns."
    m 4eub "Before rooks were activated, bishops and queen were the only long-distance controlling materials in the game."
    m 2lsb "There is also a really strong position of bishops called \"{i}Fianchetto{/i}\". This is the perfect interpretation of \"long distance controller\"."
    m 2lsa "Hold on...{w=0.5}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqk1nr/ppppppbp/6p1/8/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 1 3")#Modern Defense fen
        game.toggle_sensitivity()
        game.show()
    extend 2esb "This is the famous Modern Defense, which made a {i}Finachetto{/i}."

    if seen_event("monika_chesslesson_modern_defense") is False:
        m 2eua "Since I haven't taught you Modern Defense, let us have a brief introduction of that opening...{w=1.0}{nw}"
        python:
            game.hide()
            game = MASChessDisplayableBase(is_player_white=True)
            game.toggle_sensitivity()
            game.show()

        m 2lub "In this opening, white plays e4 as the first move, {w=0.2}{nw}"
        python:
            game.queue_move("e2e4")
            game.handle_player_move()
        extend "and black played g6, {w=0.2}{nw}"
        python:
            game.queue_move("g7g6")
            game.handle_monika_move()
        extend 2esa "which looks very confused. We will talk about this move which seems like broke the basic principle of opening later."

        m 2lsa "White then plays d4 to control 4 central squares. {w=0.3}{nw}"
        python:
            game.queue_move("d2d4")
            game.handle_player_move()
        extend 2lsb " And now, the key point of this opening is going to appear:"

        python:
            game.queue_move("f8g7")
            game.handle_monika_move()
            renpy.pause(2)
        
        m 2esb "A {i}Finachetto{/i} appeared! That's why Black's previous step didn't control the center."
        m 4lsb "This bishop enjoys a powerful diagonal:"
    else:
        m 2eub "Since I have taught you the Modern Defense, you should actually have some knowledge of Finachetto already."
        m 4lsb "Yes, this bishop controls so many squares:"
    
    python:
        i = 0
        while i<=7:
            game.request_highlight("{0}{1}".format(chr(ord('a')+i),8-i))
            i+=1
            renpy.pause(0.1)
        renpy.pause(1)
    
    m 2wub "The a1-h8 diagonal is just so powerful!{w=0.2} It across the center and is extremely intimidating, which is the soul of Modern Defense."
    m 2eub "As you can see, it's not easy to take that bishop down. {w=0.1}"
    extend 2wsd " It was protected by a formation of three pawns, as if it were in a fortress!"
    m 2rsd "What's more, without the drawbacks of most other protections, this bishop in the fortress is still extremely flexible."
    m 2esc "This was almost the most powerful position of bishops:{w=0.2} {i}Protected, safe, but agressive{/i}."
    m 2eud "As a result, white's control of the center is not as strong as it seems, and black can always fight for the center later under Finachetto's protection."
    m 4eub "Like most terms in chess, Finachetto also has two case: \"King Side Finachetto\" and \"Queen Side Finachetto\"."
    m "The current one in front of your eyes is the King Side Finachetto. It's one of the most powerful situations of bishops."
    m 2eub "However, without doubt, this is not the only great move bishop can do."
    m 1rud "Finachetto is just the best example of the Bishop's \"long-distance pin\".{w=0.2}{nw}"
    extend 1eud " Though it's really powerful once it's formed, it takes two steps to form it after all."
    m 3eub "In fact, as long as the bishops were placed on a long, open diagonal, they are good bishops already."
    m 1eub "After all, an important criterion for judging the position of a chess piece is how many squares it controls."
    m "If a bishop is trapped, like we talked about at the beginning of this lesson, it's just a \"tall pawn\"."
    m "But if they can stay on a long, open diagonal, they can take control of a dozen squares at once and become a thorn in the side of their opponents."
    m 1hub "So, the conclusion of this lesson is:"
    m 1hua "{i}Try not to have your bishop cordoned off behind other pieces. Unless you want the bishop to be a strong defender of those pieces.{/i}"
    m "Thanks for listening!"

    $ game.hide()
    show monika at t11
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_intro_advance_pawn",
            category=["chess lessons"],
            prompt="Pawn - Advanced",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_intro_advance_pawn:
    m 1eua "We mentioned before that pawns can fight, too."
    m 1euc "That's kind of only a sketch, you could say."
    m 1luc "To be more detailed, there are many things pawns can do."
    if seen_event("monika_chesslesson_opening_basic_idea"):
        m 1lud "Like control center, which you already learnt in opening lesson."
    m 1eub "There are a couple of useful pawn configurations that you have to know."
    m 1eua "Oh, just let me get the board so I can teach you.{w=0.2} Hold on...{w=0.3}{nw}"
    show monika at t11
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/6n1/4P3/3P4/2P5/8/8/8 b - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m 3eub "This is the {b}Pawn Chain{/b} structure, a very common one."
    m 3eua "A pawn chain can be very long, like 5 pawns, or very short, only 2 pawns is enough, too."
    m 1eub "The point of the pawn chain is that it's often hard to tear them down."
    m 1eua "Like, the game that just in front of your eyes, black has a knight able to attack the e6 pawn."
    m 1eub "But it's obvious that after this attack, the knight will be removed too."
    m "This is the characteristic of a pawn chain, that every pawn in the chain is protected by the next pawn--{w=0.3}{nw}"
    extend 1eua " except, of course, for the last pawn, which has no protection."
    m 2eua "So, the last pawn--{w=0.3}also called the backward pawn--{w=0.3}is the weak point in the pawn chain."
    m 2eub "In general, we think that pawn chains are a good structure. It's strong, helps control a lot of squares, and is great at blocking rooks."
    m 3eua "Another common structure is {b}Pawn Wall{/b},{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/3ppp2/8/3PPP2/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    extend 3eub " which is particularly effective in endgames."
    m 3eua "In this positionn you see, there is a pawn wall on both sides. So whichever side moves first will lose its pawn."
    m 2eub "It is common to use this structure to prevent your opponent's pawn from advancing in endgame."
    m 2euc "But, notice that these pawns have no protection from each other, so they're actually kind of breakable to pieces like rook."
    m 2eud "There are many other structures too, and I've seen a lot of people tell beginners about most of them at once...{w=0.3}{nw}"
    extend 2rtc " Personally, I don't think that's good."
    m 2eud "Pawn structure is a major question in chess, and you usually have to go to the master level to know a lot about it."
    m 1eua "So I prefer to let you experience more pawn structures in actual match."
    m 1eub "However, there are a few common kinds of pawn that I should mention."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "6k1/pp3ppp/8/8/8/PP1P4/5PPP/6K1 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        game.request_highlight_common_format("d3")
    m "This d3 pawn is the {b}passed pawn{/b}, a pawn who is generally considered a great threat, especially in endgame."
    m 1eub "A passed pawn means a pawn has no opponent's pawns in front of it or on adjacent files, which means, this pawn is having a great chance at promoting!"
    m 3eub "Passed pawns are much more powerful than you might think, sometimes even at the risk of losing materials to create or protect passed pawns is acceptable."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/7p/5kp1/4p3/p3rPRP/3K2P1/8/8 b - - 1 43")
        game.toggle_sensitivity()
        game.show()
    m 1eub "Like this one. It was a famous game of the last century, and is now regarded as a brilliant move."
    m 1eua "Efim Geller, a former grandmaster, plays the black. Now it was his turn, and guess what he did?"
    show monika 1lud
    python:
        game.queue_move("f6g7")
        game.handle_monika_move()
        renpy.pause(1)
    m 2wuo "He completely ignored white's threat to take the rook! Why is that?"
    m 2hub "If we look at what happens next in this game, we'll see that black's move was a brilliant one."
    python:
        game.queue_move("h4h5")
        game.handle_player_move()
        renpy.pause(1)
    m 2eua "You may also have a hard time understanding why white didn't immediately remove the rook, but instead moved the h-file pawn."
    m 2eub "In fact, white has realized how clever black's move was and is trying to give rook room to move out to stop the a-file passed pawn."
    m 2eua "But it was too late.{w=0.3}{nw}"
    python:
        game.queue_move("a4a3")
        game.handle_monika_move()
    extend 2hub " After this pawn move, it's so obvious that there is no way white can prevent this passed pawn from promoting."
    m 2eua "That's why black simply moved the king without any thought of protecting rook--{w=0.3}{nw}"
    extend 2hua "White is already struggling to deal with the passed pawn, who has the mood for rook?"
    m 2eub "If white simply removes a rook, it is effectively giving the other side a queen at the cost of a rook."
    m 2luc "Indeed, it's a little late for white to deal with the pawn even if white doesn't remove the rook."
    m 2lud "But that's another question to discuss, and if white deals with it immediately, it will at least cost the opponent a few more turns."
    m 2eub "Now you can see how terrible a passed pawn in the endgame can be--{w=0.3}after all, a passed pawn in the endgame is almost a potential queen!"
    m 2eua "Another common type of pawn is called {b}Isolated Pawn{/b}."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "2krr3/1pp2ppp/p1n2n2/2b1P3/8/1BP2N2/PP3PPP/R1N3KR b - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m "In this game, the e5 pawn{nw}"
    python:
        game.request_highlight_common_format("e5")
    extend " is an isolated pawn."
    m 2eub "The so-called isolated pawn, understood literally, means that a pawn is isolated. There is no other pawn on its adjacent files to support it."
    m 1eua "Generally, we consider isolated pawn as a weak pawn, and it is easy to be attacked as a breakthrough point."
    m 1etc "But that's not to say it's absolutely bad...{w=0.3}{nw}"
    extend 1esa " For example, actually a passed pawn is mostly also an isolated pawns, too."
    m 1eub "In the endgame, having an isolated pawn is often a good thing--{w=0.3}{nw}"
    extend 2rssdru "because it's usually the passed pawn, puff!"
    m 1esd "However, in middlegames or openings, an isolated pawn is often a big problem. Your opponent will quickly use this breakthrough point to destroy your defense."
    m 1esa "The last one I want to talk about is a structure where a lot of beginners might even consider it as a good structure."
    m 1eub "That's {b}Doubled Pawns{/b}."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbq1rk1/p1pp1ppp/1p2pn2/8/2PP4/P1P1P3/5PPP/R1BQKBNR w KQ - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 1eua "See the c4 pawn and the c3 pawn,{w=0.3}{nw}"
    python:
        game.request_highlight_common_format("c4",highlight_type_red)
        game.request_highlight_common_format("c3",highlight_type_red)
    extend " they are the doubled pawns."
    m 1eub "Doubled pawns, obviously, mean two pawns from the same player appear on the same file."
    m 1esa "Also, there is another concept, {b}Tripled Pawns{/b}, I think I don't need to explain it for it's self-evident."
    m 1esb "Why do we say that doubled pawns are bad? The reason is underlying."
    m 3esb "In a structure like doubled pawns, both two pawns are usually unprotected, because they are the one who supposed to protect each other!"
    m 3esa "The pawn that overlaps is usually the other pawn's original adjacent pawn."
    m 3hua "Hence its second disadvantage--{w=0.2}the possibility that it has broken a potential pawn chain or some other good structures."
    m 1etd "Of course, nothing is absolute. Sometimes a double is not so bad."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bq1rk1/ppp2ppp/2n1np2/3p4/1b1P4/2NQBN2/PPP1BPPP/2KR3R w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 1lsd "Like this situation, is there a doubled pawn?{w=0.3} Of course there is, that's the f6 pawn."
    m 1esd "But is this pawn weak?"
    m 1esc "It's not! This pawn is protected by the g7 pawn, so although it is a double pawn, it is not really weak."
    m 1rtd "However, it's true that the tripled pawns I just mentioned is pretty bad in almost all cases...{w=0.3}{nw}"
    m 1rtc "And the tetra pawn, not to mention. I can't even think for a moment under what circumstances a tetra pawn might be good."
    m 1rssdrb "So I guess there is something absolute too?"
    m 1eua "All in all, the question of the structure of pawns is a very profound knowledge."
    m 1eub "And today I can only give you some of the most basic knowledge since it's too much to introduce them all at once."
    m 1eua "I hope this lesson has given you a little bit of a better sense of how to use pawns."
    m 1hub "Thanks for listening!"
    $ game.hide()
    show monika at t11
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_pgn",
            category=["chess lessons"],
            prompt="PGN standard",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_pgn:
    $ ev = mas_getEV("monika_chesslesson_pgn")
    if ev.shown_count > 0:
        m 1eub "Do you want to go through the whole lesson again, or do you want to go straight to the test, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want to go through the whole lesson again, or do you want to go straight to the test, [player]?{fast}" 
            "I want to go through the whole lesson again.":
                m 1hua "Okay!"
            "Straight to test.":
                m 1tfb "UNFINISHED?"
                return
    
    m 1eua "In chess community, there is a very important recording standard called PGN standard."
    m 1eub "The full name is {i}\"Portable Game Notation\"{/i}."

    # To know if the player saved a pgn before.
    $ pgn_saved = True if renpy.seen_label("mas_chess_savegame") else False
    
    if pgn_saved == True and ev.shown_count == 0:
        m 1eud "And since you have already asked me to save games in our \"chess_games\" folder, I think you probably have known something about PGN."
        m 1etc "So now I'm not really sure if you need this lesson..."
        m 3etd "Do you know PGN standard well already?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you know PGN standard well already?{fast}"
            "Yes.":
                m 1essdlb "Oh, then I'm sorry to tell you so much you already know things..."
                m 1essdla "...I guess I'll probably end this lesson here then?"
                m "..."
                m 1hua "Thanks for listening anyway!"
                return#End this lesson now.
            "Not really.":
                m 1esb "Okay, then let me explain this standard for you...{w=0.5}{nw}"
    else:
        m 1esb "Now, let us get the board here...{w=0.5}{nw}"
    
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2.0)
    
    m "Alright.{w=0.1} Let us firstly talk about how to record pawns."
    m "In this game, white just pushed the e2 pawn to e4."
    m 1eua "This move is recorded as \"e4\"."
    m 1lua "Let me give you one more example...{w=0.5}{nw}"

    python:
        game.queue_move("d7d5")
        game.handle_monika_move()
        renpy.pause(2.0)
    
    m 1lub "And now, black just pushed the d7 pawn to d5."
    m "This move is recorded as \"d5\"."
    m 1eua "Have you noticed any patterns?"
    m 1hua "If you haven't, don't worry, it's logical.{w=0.2} After all, this is a little hard to understand."
    m 1esa "When we're refering a pawn, we refer to it by its file index."
    m 1esb "In \"e4\" the move, the letter \"e\" means we are pushing the e-file pawn."
    m 2esb "And it's white moving, white has only one pawn can move to line 4 now."
    m 2esa "So we simply record this move as \"e4\"."
    m 2lsb "And in \"d5\" the move, black is pushing the d-file pawn, so we uses the letter \"d\" to refer to that pawn."
    m 2etc "At this point, you may think of a question:{w=0.5}{nw}"
    extend 2etd " it is possible for pawns to switch to other files, such as capturing, then how to record it?"
    m 2lsc "Let us see this example:"

    python:
        game.queue_move("e4d5")
        game.handle_player_move()
        renpy.pause(2.0)
    
    m 2esa "In this move, white's pawn captures black's pawn and moves from e4 to d5."
    m 2esb "Because this captor pawn was originally on the e-file, so we firstly write a letter \"e\" down to indicate that \"This is a move of e-file pawn\"."
    m 7esb "And this pawn did a capture job, so we secondly write another letter \"x\"."
    m "It's because that {i}the letter \"x\" in PGN standard is standing for capturing{/i}."
    m 2eua "Now, the capture target is on the d5 square, so we write the target square down: \"d5\"."
    m 2hua "Done!{w=0.3} The full record of this move is \"exd5\"."
    m 2eua "You might are curious about how to record the promotions of pawns.{w=1.0}{nw}"
    extend 2lua " Let us look at this example:"

    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/1P6/8/8/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1.0)
    
    m 2lub "In this position, there is a white pawn on b7 square ready to promote."
    m 4lua "Let us play that move."

    python:
        game.queue_move("b7b8q")
        game.handle_player_move()
        renpy.pause(2.0)
    
    m 4eua "Now let us consider how to record this move."
    m 2eub "Firstly, this is a b-file pawn moving, so we write the letter \"b\" down as the beginning."
    m "And it moved to square b8, b8 is on the b-file too, this move didn't change the file of that pawn.{w=0.3} So we write the number \"8\" down."
    m 2esa "Now let's think about how to represent \"promotion\"."
    m 2esd "If there is only one possible promotion in chess, and that is to be queen, there is no special record required."
    m 2rsd "We can just finish the record as \"b8\" here.{w=0.3} After all, in that possibility, people would see the record of a pawn reached the last line and know that it must have become a queen."
    m 2esd "But the problem is that there isn't only one possible promotion.{w=0.2} There are four possibilities. Queen, Rook, Bishop or Knight."
    m 2esc "So it is necessary to write down what this pawn became."
    m 2lsb "At this point, the pawn became a queen, so we write \"=Q\" to record it was promoted to a queen."
    m 2hua "Done!{w=0.5} The full record of this promotion is \"b8=Q\"."
    m 2hub "And as what you can guess, if the pawn has just been prmoted to a bishop instead of a queen, then it is recorded as \"b8=B\"."
    m 2hua "And for knight situation, it is \"b8=N\", for rook situation, it is \"b8=R\"."
    m 2eub "Now, what if a pawn is promoted while capturing a piece?"
    m 2lub "Let me give you another example:"

    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "3q4/2P5/8/8/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2.0)
    
    m 7lub "In this position, white is going to play this move:"

    python:
        game.queue_move("c7d8q")
        game.handle_player_move()
        renpy.pause(2.0)
    
    m 2eub "How to record this? Let's first ignore the action of \"promote\"."
    m "From the previous explanation, it is not difficult to understand that the record of \"capture\" part should be written as \"cxd8\"."
    m 2esa "And then, it promoted to a queen, so we added \"=Q\"."
    m 2hsa "So the full record is \"cxd8=Q\"."
    m 2rua "Hmm...{w=0.2}{nw}"
    extend 2rusdlb" Though so far we've only covered the pawn movement, we haven't covered any other pieces at all,{w=0.2}{nw}"
    extend 4esb " but don't worry! With these in mind, you can quickly understand the following."
    m 2duc "Hold on, let me set another position on the board...{w=1.0}{nw}"

    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "4R3/8/8/2R5/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    
    show monika 2eua
    pause 2.0
    
    m 2eub "When we're talking about a piece that is pawn, we simply use the file index it is in to refer to it."
    m 2rud "But this does not apply for pieces that are not pawns."
    m 2eud "If we're recording a piece which is not a pawn, then we must firstly write down the piece type."
    m 2eub "Like, if it's a Rook moving, then uses letter \"R\" to refer to it."
    m "For knights, \"N\".{w=0.2}\nAnd \"K\" for King,{w=0.1} \"Q\" for Queen,{w=0.1} \"B\" for Bishops."
    m 2eua "After we recorded which type of piece is moving, we write down its target square."
    
    python:
        game.queue_move("c5c3")
        game.handle_player_move()
    
    m 2lub "Like this move.{w=0.3} Since it's a rook moving, so we firstly write the letter \"R\" down."
    m 4lub "And then, this rook moved to c3 square, so we then write the \"c3\" down."
    m 4hua "Done again!{w=0.3} The full record is \"Rc3\", which means \"Rook moved to c3 square\"."
    m 2eub "In this case, we don't need to write down the starting position of the rook because we have the target position."
    m 2eua "Obviously, in the current situation, the white has only one rook able to move to c3, that's the c5 rook."
    m 2eud "{i}One case where we need to keep track of the initial position is when the player who is moving has more than one piece from even only one type, and all of them can move to the target square.{/i}"
    m 2luc "Like this...{w=0.5}{nw}"
    
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "2R5/8/8/2R5/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()

    extend 2lud " The c6 square is reachable for both two rooks, so we can't just write \"Rc6\" for it does not specify which rook is moving."

    python:
        game.queue_move("c5c6")
        game.handle_player_move()
    
    m 2eud "So if white played this move,{w=0.4}{nw}"
    extend 2etd " how can we record it?"
    m 2esc "In any case, it's a Rook moving.{w=0.3} So let's write the letter \"R\" down."
    m 2esd "However, it's not like previous now.{w=0.5} Simply writing down the target square obviously doesn't tell us which rook is moving, so we'll have to write down the initial position."
    m 2etd "So we should record this move as \"Rc5c6\"?"
    m 1eud "Actually, there is no need.{w=0.5}{nw}"
    extend 1eub " An important tenet of the PGN specification is {i}to keep the record length as short as possible while keeping the information clear{/i}."
    m "In this position, we can ignore the c-file information and just write down \"5\" the line information to mark the location."
    m 1hua "So the final result is \"R5c6\"."

    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/8/8/8/8/R6R w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    
    m 1lub "And now, in this situation, if we want to move the a1 rook to d1,{w=0.4}{nw}"
    
    python:
        game.queue_move("a1d1")
        game.handle_player_move()
    
    extend 2eub " then we should record this as \"Rad1\" instead of \"R1d1\" for it's the file information that matters, not the line information now."
    m 2rud "Of course, there are also very extreme cases where we need to write out all the information."
    m 2duc "Hold on...{w=0.5}{nw}"

    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/1QQQQQ2/1Q3Q2/1Q3Q2/1Q3Q2/1QQQQQ2/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    
    m 2lud "This one.{w=0.5}{nw}"
    extend 2wud " There are many queens that can move to d4 square at the same time! And writing line information or file information alone is not enough to ensure the clarity of the record!"
    m 2lud "So, if we moved like this,{w=0.3}{nw}"
    
    python:
        game.queue_move("b6d4")
        game.handle_player_move()
    
    extend 2eud " Then we have no choice but to write down the initial position completely. The final result is \"Qb6d4\"."
    m 2eub "Of course, this is a very, very rare situation. In practice, we usually just write the line message or the file message, and that would be enough."
    m "Now let's talk about capturing from pieces that are not pawns.{w=0.3}{nw}"
    extend 2duc " Hold on...{w=0.5}{nw}"
    
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "5k2/8/2N5/4q3/8/4R3/8/1K6 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1.0)
    
    m 2eub "It's white's turn now.{w=0.2} White could capture this queen with rook,{w=0.2}{nw}"
    extend 2lub " like this:{w=1.5}{nw}"

    python:
        game.queue_move("e3e5")
        game.handle_player_move()
        renpy.pause(1.0)
    
    m 2lua "To record this move, first of all, since this is a rook move, let's write down the letter \"R\"."
    m 2lub "And it's a capture move, so we then write down the letter \"x\"."
    m "We don't need to write down what we captured."
    m 2eub "All we need to do is write down the target's position, because once we write down the position, we know who's on that square due to a series of previous PGN records."
    m 2hua "So this record is: \"Rxe5\"."
    m 2eua "If we have multiple rooks that can capture it at the same time, then, as we mentioned earlier, before writing down the letter \"x\" to indicate the capture, say which rook it is."

    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/8/R2q3R/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    
    m 2lub "Like now, if we moved the a-file rook to capture this d5 queen,{w=0.6}{nw}"

    python:
        game.queue_move("a5d5")
        game.handle_player_move()
    
    extend 4lub " then it's recorded as \"Raxd5\"."
    $ game.hide()

    m 2eub "And now, this lesson is finally going to end. Only two special rules need to be noted."
    m 2eua "{i}If a move successfully checked a player, write a \"+\" at the end of the record to indicate that the move checked.{/i}"
    m 2duc "Let me take another example...{w=0.5}{nw}"

    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "8/8/4K2k/8/8/8/1R6/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()

    m 2lud "Now, if white moved the rook to h2, then it's a check."
    m 2eud "The record should have been written as \"Rh2\", but now it checks another player, so it should be written as \"Rh2+\"."
    m "And then, another special rule is, {i}if a move successfully checkmated a player, write a \"#\" at the end of the record to indicate that the move checkemated.{/i}"
    m 2duc "Let me set another situation on the board...{w=1.0}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "7k/5Q2/6K1/8/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 2lub "Okay. Now white is ready to play the deadly move:{w=0.5} Queen to g7, which ends this game."
    m 2eub "Since the move is going to checkmate the opponent, this move is supposed to be recorded as \"Qg7#\"."
    $ game.hide()
    m 1hua "That's all we need to say."
    extend 1eub " If you don't mind, I can give you some questions to solve so we can ensure you've learned it correctly."
    m "Do you have the time now?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you have the time now?{fast}"
        "Yes, come on.":
            m 1hua "Okay!"
            m "Here we go!"
            #jump monika_chesslesson_pgn_question1
            m 1eud "..."
            m 1euc "UNFINISHED."
        "Sorry, maybe another time.":
            m 1eua "It's okay, [player]."
            m 1eub "Whenever you want to come, just ask me about this lesson again."
            m 1hua "For now, take your time, [player]~"
            show monika at t11
            m "Thanks for listening!"
            return
    show monika at t11
    return

label monika_chesslesson_pgn_question1:
    m 1hua "Question 1!"
    show monika at t21#DEBUG USE.
    python:
        piece_type = random.choice(['Q','B','N','P','R','K'])
        piece_type = 'B'#DEBUG USE.
        piece_position_file = random.choice(['a','b','c','d','e','f','g','h'])
        piece_position_line = random.randint(1,8)
        fen_to_start = ""
        for i in range(1,9,1):
            if i == 9-piece_position_line:
                fen_to_start += str(ord(piece_position_file) - ord('a')) if str(ord(piece_position_file) - ord('a') -1) != "0" else ""
                fen_to_start += piece_type
                fen_to_start += str(7 - ord(piece_position_file) + ord('a')) if str(7 - ord(piece_position_file) + ord('a')) != "0" else ""
                fen_to_start += "/"
            else:
                fen_to_start += "8/"
        
        fen_to_start = fen_to_start[:-1]# Delete the last '/' we inserted.
        fen_to_start += " w - - 0 1"

        if piece_type == 'Q':
            if random.randint(1,2) == 1:
                # Random result 1: Non-Diagonal move.
                if random.randint(1,2) == 1:
                    # Sub-Random result 1: Move to up or down.
                    target_position_line_available = [1,2,3,4,5,6,7,8]
                    target_position_line_available.pop(piece_position_line-1)
                    target_position_line = random.choice(target_position_line_available)
                    target_position_file = piece_position_file
                else:
                    # Sub-Random result 2: Move to left or right.
                    target_position_line = piece_position_line
                    target_position_file_available = ['a','b','c','d','e','f','g','h']
                    target_position_file_available.remove(piece_position_file)
                    target_position_file = random.choice(target_position_file_available)
            else: 
                # Random result 2: Diagonal move.
                target_position_line_available = [1,2,3,4,5,6,7,8]
                target_position_line_available.pop(piece_position_line-1)
                target_position_line = random.choice(target_position_line_available)
                target_position_file = chr(ord(piece_position_file) + (target_position_line - piece_position_line) * random.choice([-1,1]))
        elif piece_type == 'R':
            if random.randint(1,2) == 1:
                target_position_line_available = [1,2,3,4,5,6,7,8]
                target_position_line_available.pop(piece_position_line-1)
                target_position_line = random.choice(target_position_line_available)
                target_position_file = piece_position_file
            else:
                target_position_line = piece_position_line
                target_position_file_available = ['a','b','c','d','e','f','g','h']
                target_position_file_available.remove(piece_position_file)
                target_position_file = random.choice(target_position_file_available)
        elif piece_type == 'B':
            target_position_line_available = [1,2,3,4,5,6,7,8]
            target_position_line_available.pop(piece_position_line-1)
            #for i in range(0,7,1):
                #if target_position_line_available[i] - piece_position_line > 
            target_position_line = random.choice(target_position_line_available)
            target_position_file = chr(ord(piece_position_file) + (target_position_line - piece_position_line) * random.choice([-1,1]))
        elif piece_type == 'N':
            target_position_file = 1
        elif piece_type == 'P':
            renpy.pause(1.0)
        else:
            # piece_type == 'K'   situation.
            target_position_file = piece_position_file
            target_position_line = piece_position_line
            while target_position_file == piece_position_line and target_position_file == piece_position_file:
                target_position_line = chr(ord(piece_position_line) + random.randint(-1,1))
                target_position_file = chr(ord(piece_position_file) + random.randint(-1,1))

        game = MASChessDisplayableBase(is_player_white = True, starting_fen = fen_to_start)
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2.0)
        move_goingtoplay = piece_position_file + str(piece_position_line) + target_position_file + str(target_position_line)
    m "target_position_line_available: [target_position_line_available]"
    m "target_position_line: [target_position_line]"
    m "[move_goingtoplay]"
    python:
        game.queue_move(move_goingtoplay)
        game.handle_player_move()
        renpy.pause(2.0)
    
        player_answer = "" # The variblae to store what played typed.
        correct_answer = piece_type + target_position_file + str(target_position_line) # The correct answer.
        corrected = False # True if the play answered correctly.
        failure_time = 0 # How many times did the player fail?
        failure_wronganswer = False # Ever the player replied a wrong answer(Type empty answer won't set this to True.)

    while corrected == False:
        $ player_answer = mas_input(
            "How should we record this move?",
            length=7,
            screen_kwargs={"use_return_button": False}
        )
    
        if player_answer != correct_answer:
            $ failure_time += 1
            if failure_time >= 5:
                m 1hksdla "..."
                m 1lksdla "Okay, [player], I guess you're not in the mood today."
                m 1eksdla "That's alright! People have bad days after all."
                m 1eub "For now, let us do something else to make you in a better mood, okay, [player]?"
                $ corrected = True# Set corrected as True to break the while loop.
            elif not player_answer:
                # Player didn't answer anything at all.
                m 1eksdla "Ehehe...{w=0.5} [player]."
                m 1eka "You didn't even answer a single word."
                m 1eub "Try again!"
                show monika 1eua
            else:
                $ extra_word = "still " if failure_wronganswer else ""
                $ failure_wronganswer = True
                m 1euc "Oops.{w=0.3}{nw}"
                extend 1eka" Sorry [player], but that's [extra_word]not the correct answer."
                m 3ekb "Try again?"
                show monika 1eua
        else:
            m 3hub "Yes, that's right!"
            if failure_time == 0:
                m 1huu "I know you can answer this without any failure~"
                m 1nuu "You are a really smart student,{w=0.3}{nw}"
                extend 1hub " ahaha!"
                $ mas_gainAffection()
            m 4hub "Now let us go to the next question!"
            $ corrected = True
        
    show monika at t11
    $ game.hide()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_pgn_file",
            category=["chess lessons"],
            prompt="PGN standard - Record a full game",
            pool=True,
            conditional="seen_event('monika_chesslesson_pgn')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_pgn_file:#UNFINISHED.
    m "UNFINISHED."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_stalemates",
            category=["chess lessons"],
            prompt="Stalemate",
            pool=True,
            conditional="persistent._mas_pm_player_know_stalemate == False",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_stalemates:
    m 1eua "As we all know, both win or lose are a result of a chess game."
    m 1euc "But what you may don't know is that there is a third way."
    m 3eud "And that's the stalemate. The third way to end a chess game."
    m 1euc "When a game came to stalemate, it means no one lost or won. In other words, it's kind of a draw."
    m 1etd "But when will a game come to stalement?"
    m 1eub "Hold on, let me get a game for you."
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/k2K4/2Q5/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m 1eua "The situation was supposed to be a sure win for white, but white made a big blunder."
    m 3lub "That's king to c6.{w=0.3}{nw}"
    python:
        game.queue_move("d6c6")
        game.handle_player_move()
    extend 3wud " This move immediately ruined the good situation!"
    m 1eta "Why? Let us enter the black's view."
    m 1etd "White just played a move, so now it's black's turn. Now, the question is, what move should black play?"
    m 1eud "Notice the point now? That is the black doesn't have any legal moves at all!"
    m 3eud "All five squares around the king are now controlled by white, so wherever the king goes, he is actively within attack range of his opponent!"
    m 1rtd "And the rule of chess is that you must never actively make your king within the attack range of your opponent."
    m 1euc "That's why black doesn't have any legal moves."
    m 3eub "Then again, this is different with a checkmate. When a checkmate happens, it means that not only the opponent can not make the king safe, but also the king is being attacked at that time."
    m 3eua "As for stalemate, the problem is the opponent only can not make the king safe {i}after{/i} this move, but the king is safe {i}now{/i}."
    m 1rusdla "Hmm...{w=0.3}{nw}"
    extend 1husdla " Maybe this sounds complicating to you?"
    m "Do you understand this term now?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you understand this term now?{fast}"
        "Yes, I do.":
            m 1hub "Great! Then let us continue our lesson."
        "I'm confused.":
            m 1lusdla "Well...{w=0.3}{nw}"
            extend 1rusdla " Hmm...{w=0.3}{nw}"
            extend 1hub " Oh, I got another idea to explain it!"
            python:
                game.hide()
                game = MASChessDisplayableBase(is_player_white=True,starting_fen="1K6/6R1/5R2/7k/5R2/8/8/8 b - - 0 1")
                game.toggle_sensitivity()
                game.show()
                renpy.pause(1)
            m 3eub "In this situation, white's rooks are controlling all the squares near the black king."
            python:
                game.request_highlight_file('g',highlight_type_red)
                game.request_highlight_line(6,highlight_type_red)
                game.request_highlight_line(4,highlight_type_red)
            m 2esb "But it's important to note that at this moment, the black king is not under attack. In other words, he is safe at this point."
            m 2esa "It is only after it has taken a move that it is under attack. Until it takes a move, it's always safe."
            m "So this is a stalemate."
            m 2esb "If we add a rook to the board that can attack it now, the situation is different!"
            python:
                game.hide()
                game = MASChessDisplayableBase(is_player_white=True,starting_fen="1K6/6R1/5R2/4R2k/5R2/8/8/8 b - - 0 1")
                game.toggle_sensitivity()
                game.show()
                game.request_highlight_file('g',highlight_type_red)
                game.request_highlight_line(6,highlight_type_red)
                game.request_highlight_line(4,highlight_type_red)
                game.request_highlight_line(5,highlight_type_red)
            m 2esa "Just here and now, the black king is under attack. You don't need it to move. It's already attacked."
            m 2hub "So this is not a stalemate, but a checkmate."
            m 2hua "I think you get it by now, right?"
    m 1eub "There are a lot of beginners who are very unhappy with this rule."
    m 1euc "Indeed, it is clear that there is a huge advantage, their own advantage makes the other side without any legal move, it seems that this should be judged to win."
    m 3eud "But you have to know that without this rule, many famous chess game in history would not exist."
    m 3eub "There are many famous games in history, in order to avoid a stalemate, out of many wonderful moves."
    m 1eua "In addition, it may also be a manifestation of culture."
    m 1eub "In European culture, a desperate surrender is not shameful. Losers are not considered traitors."
    m 1hua "Finally, if your opponent can use this to get a draw at the end of the game, can't you?"
    m 3hua "If you are the side with disadvantage, you can also get a draw this way."
    m 3eua "So I really don't think this is a bad rule."
    m 1eub "Of course, if you really think this rule is silly, I totally accept your idea!"
    m 1eua "All you have to do is tell me to use casual rules."
    m 1lusdla "Of course, given that so many people agree this rule, I'd still suggest you follow it to make sure you know how to against anyone else in the future."
    m 1hub "Thanks for listening!"
    show monika at t11
    $ game.hide()
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_tactic_fork",
            category=["chess lessons"],
            prompt="Basic tatic: Fork",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_tactic_fork:
    m 1eub "The fork, as they are called in chess, are one of the basic tactics."
    m 1eua "This tactic means using a piece to attack two or more of your opponent's pieces simultaneously."
    m 1eub "To explain this tactic in detail, let's look at a puzzle that I'm going to show you."
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="rnb1kbnr/ppp2ppp/8/3N4/q7/8/PPPQ1PPP/R1B1KBNR w KQkq - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 1lub "If you were white, what would you do now?"
    m 3eua "The best solution is the only one, and that is to put the bishop in b5 square."
    python:
        game.queue_move("f1b5")
        game.handle_player_move()
    m 1esd "This move may seems like crazy, like abandoning the bishop."
    m 1esa "But this is actually a pretty good move.{w=0.3}{nw}"
    python:
        game.request_highlight_diagonal("a4","e8",color = highlight_type_red)
    extend 1lsa " Firstly, notice that both the queen and the king are being attacked by whtie's bishop--{w=0.3}which is, a {i}fork{/i} tactic."
    m 1esb "So there is no way black can just ignore this bishop, simply move the queen away."
    m 1eua "Soon, we'll see why black would want to ignore it."
    python:
        game.remove_highlight_all()
        game.queue_move("a4b5")
        game.handle_monika_move()
    m 1eub "Black has removed white's bishop, but this move puts their pieces in a very unfavorable position."
    python:
        game.queue_move("d5c7")
        game.handle_player_move()
        renpy.pause(1)
    m 1wub "A triple-fork!{w=0.2}{nw}"
    extend 1wsb "The rook,{w=0.1}{nw}"
    $ game.request_highlight_common_format("a8", highlight_type_red)
    extend " the queen,{w=0.1}{nw}"
    $ game.request_highlight_common_format("b5", highlight_type_red)
    extend " and the king.{w=0.1}{nw}"
    $ game.request_highlight_common_format("e8", highlight_type_red)
    extend 1wub " all of them are being attacked now!"
    m 1hub "Of the 3 pieces under attack, there is no doubt that the king must escape since the survival of the king is above the survival of all the other pieces."
    python:
        game.remove_highlight_common_format("e8")
        game.queue_move("e8e7")
        game.handle_monika_move()
    m 3eub "Then the round is white again. The white will of course choose to remove the opponent's queen,{w=0.3}{nw}"
    python:
        game.remove_highlight_all()
        game.queue_move("c7b5")
        game.handle_player_move()
    extend 3hua " which forms a winning game to white."
    m 1eub "In this case, our forkers are knight and bishop. Knight in particular for it created a triple-fork."
    m 1eua "In fact, indeed, it's knights who fork the most in real games."
    m 1hksdla "Though, I haven't looked it up, that's only how I feel."
    if persistent._mas_pm_player_chesslevel == chesslevel_master:
        m 1hksdlb "...Then again, considering that you're a master at chess, perhaps you know it isn't that so."
    m 1eub "However, of course, knights are not the only forker!"
    m 1eua "Many newcomers have actually been attacked with a certain move which used the fork tactic."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="r2qk2r/ppp2ppp/2n1bn2/4p3/3PP3/2N2N2/PPP2PPP/R1BQK2R w KQkq - 3 3")
        game.toggle_sensitivity()
        game.show()
    m 1tta "In fact, I think you've probably been in this situation..."
    m 1eub "You know who is going to play the fork tactic?"
    m 1etu "Maybe a surprise, but it's the pawn."
    python:
        game.queue_move("d4d5")
        game.handle_player_move()
        renpy.pause(1)
        game.request_highlight_common_format("c6",highlight_type_red)
        game.request_highlight_common_format("e6",highlight_type_red)
        renpy.pause(1)
    m 1eub "Black is certainly suffering from this pawn which attacks the knight and the bishop at the same time."
    m 1hua "Needless to say, whatever black is going to do, black is losing a piece."
    m 1eua "Some have called this fork \"one of the most painful moments in chess\".{w=0.3}{nw}"
    extend 1eub " And I think it's true!"
    m 1hua "Fork of this kind usually happens really unexpected, even people who have been playing chess for years occasionally fall into this tactic by accident!"
    m 1hub "So, again--{w=0.3}never underestimate pawns, they often can be quite a headache!"
    m 1eua "Also, in future games, it's best to see if you are falling into this trap before moving your knight or bishop~"
    m 1hub "Ahaha!"
    show monika at t11
    $ game.hide()
    m 1hua "These should be a basic introduction to fork the tactic."
    m 1hub "Thanks for listening!"
    # TODO: Add some tests here?
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_tactic_discovered_attack",
            category=["chess lessons"],
            prompt="Basic tatic: Discovered Attack",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_tactic_discovered_attack:
    m 3eub"{i}Discovered attack{/i} is a tactic when the attack path of a piece is blocked by another piece, but then you suddenly move that piece away, revealing the attacker."
    m 3duc "Hold on a few seconds...{w=0.3}{nw}"
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r4rk1/4bpp1/p3pn1p/8/3q4/3B1Q2/1P3PPP/RNBR2K1 w - - 0 18")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m 1eub "This is a game I once played."
    m 1eua "In this situation, I found a best move that gave me an overwhelming advantage."
    m 1hua "Before I show this move, I want you to think about it for a moment and see if you can figure it out for yourself."
    m 1eub "Let me know when you're done.{nw}"
    # TODO: Allowing the player to move around the board, like in Puzzle Mode?
    $ _history_list.pop()
    menu:
        m "Let me know when you're done.{fast}"
        "I'm done.":
            pass
    m 1hub "If the move you come up with is to push the bishop to h7 square, then, congratulations, that's the best move!"
    python:
        game.queue_move("d3h7")
        game.handle_player_move()
    m 3esb "This is where the {i}discovered attack{/i} tactic is used. We removed the bishop and revealed the rook."
    python:
        game.request_highlight_file('d')
        game.request_highlight_diagonal("g8","h7")
    m 3eub "Notice that while the rook can attack the queen, the bishop also attacks the opponent's king."
    m 1lub "The opponent must escape the check first like this,{nw}"
    python:
        game.remove_highlight_diagonal("g8","h7")
        game.queue_move("g8h7")
        game.handle_monika_move()
    extend 1lua "{w=0.3} or with knight, but it doesn't matter.{w=0.5}{nw}"
    python:
        game.queue_move("d1d4")
        game.handle_player_move()
    extend 1eub " Since it's our turn now, I can take the queen down now."
    m 1hua "In the end, I lost a bishop, the opponent lost a queen. Without doubt, the opponent is already losing."
    m 1eua "So after serveral more turns, my opponent resigned."
    m 3esb "The lightspot about this tactic is that it can create multiple threats simultaneously--{w=0.3}which is usually impossible to solve."
    m 1duc "Another example is...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=False, starting_fen = "8/4r3/4nk2/3B3R/5b2/5P2/5K2/8 b - - 1 1")
        game.toggle_sensitivity()
        game.show()
    extend 1eua " this."
    m 1eub "In this case, the optimal solution for black is to move the bishop to e3 square."
    python:
        game.queue_move("f4e3")
        game.handle_player_move()
    m 1eua "As you probably have guessed, this was not a pointless abandonment, but a meaningful sacrifice."
    python:
        game.queue_move("f2e3")
        game.handle_monika_move()
    m 1eub "After the opponent's king takes the bishop, it's on the same file as rook."
    m 1lub "So we can play a very nice Discovered Attack tactic,{w=0.3}{nw}"
    python:
        game.queue_move("e6g7")
        game.handle_player_move()
    extend 1lsa " knight to g7, which reveals the black rook to attack the white king and attacks the white rook at the same time, very clever."
    m 1eub "At this point, there is no need to say more. The situation is obviously a winning one for black."
    m 2eub "Also, in this example, the piece black revealed attacks the opponent's king, so this move can be further classified as {i}Discovered Check{/i}."
    m 2esd "On this basis, there is a further class called {i}Double Check{/i}."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bqkb1r/ppp3pp/2n2p2/8/4N3/5N2/PPPP1PPP/R1BQR1K1 w kq - 1 5")
        game.toggle_sensitivity()
        game.show()
    m 1esb "See this game. There is a Double Check for white, can you find it?"
    m 1esa "..."
    m 1hub "If you've found knight to d6, well, you've done a good job!"
    m 1esb "Oh, don't worry, knight to f6 is also a double check, but d6 is the best one if we're going to consider the following chase."
    m 1esa "In this lesson, we're going to talk about double check in isolation. About the following moves, that's not the point. So I'm not going to introduce them."
    m 1lub "Anyway, after this move,{w=0.3}{nw}"
    python:
        game.queue_move("e4d6")
        game.handle_player_move()
    extend 1lua " white reveals rook as the attacker, attacking king."
    m 3hub "At the same time, the newly removed knight moves into another position to attack the king. This is called a double check!"
    m 3hua "What's scary about Double Check is that it's very aggressive.{w=0.3}{nw}"
    extend 3wub " Black can't defuse this attack by simply removing the knight or just blocking the rook! The only option is to move the king!"
    m 1eua "Of course, as you might have guessed, there is also a move called a Double Attack, which is actually similar to this move, except the target is not king but another piece."
    m 1esa "Since it's so similar to this move, I'm not going to ramble."
    m 1hua "Anyway, these are the Discovered Attack tactic."
    m "The characteristic of this tactic is to {i}create multiple dangers at the same time, keep the opponent powerless of answering{/i}."
    $ game.hide()
    show monika at t11
    m 1hub "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_tactic_pin",
            category=["chess lessons"],
            prompt="Basic tatic: Pin",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_tactic_pin:
    m 3eub "The so-called {i}pin{/i} is when one of your pieces has a blocker in its attack path, and the blocker has another piece behind it."
    m 3eua "Let me give you an example so you can see."
    show monika at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bqk2r/pppp1ppp/2n2n2/2b1p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    if seen_event("monika_chesslesson_italian_game"):
        m 2eub "Do you remember the Italian Opening I told you about? This is a common situation in Italian Game."
    else:
        m 2eub "This situation is a common development of an opening game called the {i}Italian Game{/i}."
        if seen_event("monika_chesslesson_intro_basic_king"):
            m 2eua "I mentioned it to you earlier in the introduction to the king, as you may remember."
            m 2eub "If so, you should also remember that I told you that I would give a separate lesson on it in the future."
            m 4eua "Anyways, if you're worrying about what's this opening, there is no need. I'm going to teach you in future."
            m 2hua "For now, let us just focus on the current board."
        else:
            m 2hua "I'll make a separate lesson on this opening in the future, so don't worry, just watch the current board for now."
    m 2eua "In this case, can you guess who is pinning?"
    m 2hua "The answer is the bishop on g5 square."
    python:
        game.request_highlight_diagonal("d8","g5",0.2,highlight_type_red)
        renpy.pause(0.5)
    m 2esb "See? The queen of black is on the same diagonal as the knight, and the knight acts as a barrier to keep the bishop from attacking the queen."
    m 2esa "If you were black, would you move the knight at this point? Apparently not."
    m 2eub "Speaking of this, there are two types of pins."
    m 2esa "{i}Relative Pin{/i} and {i}Absolute Pin{/i}."
    m 2eub "Relative pin means that the pin will make it look not desirable to move that barrier, but it can be done anyway."
    m 2eua "For example, the current pin in front of your eyes is relative pin. It is not reasonable to move the knight, but it is possible."
    m 2eub "And as for absolute pin...{w=0.3} I'll give you another example."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "4k3/3q4/8/8/1KB4R/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 2lub "This game doesn't look very good for White, does it? But white could turn that around in one move."
    python:
        game.queue_move("c4b5")
        game.handle_player_move()
        renpy.pause(1)
        game.request_highlight_diagonal("b5","e8",0.2,highlight_type_red)
        renpy.pause(0.5)
    m 2eua "An absolute pin. This queen cannot be moved because it is against the rules of chess--{w=0.3}you cannot actively expose your king to opponent's attack."
    m 2eub "Black has few moves, one of which can be an active attack."
    python:
        game.remove_highlight_all()
        game.queue_move("d7b5")
        game.handle_monika_move()
    m 2hua "I don't need to say much about the follow-up. White takes the queen, and then white has one more rook than black."
    m 3eub "This game turns into {i}One Rook Mate{/i} the endgame pattern."
    if seen_event("monika_chesslesson_mate_one_rook"):
        m 3hua "I've taught you One Rook Mate, so you know, it's already a win for white."
    else:
        m 3hua "In this endgame, as long as the side with the rook does the right move, the checkmate is guaranteed. As a result, the white side has now won for sure."
    m 1eub "This is an example of using an absolute pin."
    m 1esb "As you can see, the beauty of the pin tactic is that it limits the movement of a piece."
    m 1eub "Let's take the example that we did at the beginning of this lesson."
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True, starting_fen = "r1bqk2r/pppp1ppp/2n2n2/2b1p1B1/2B1P3/3P1N2/PPP2PPP/RN1QK2R w KQkq - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 1esb "Obviously, it is hard to imagine that the bishop, who is now acting as the pin in this situation, could have any direct effect on the contest for the centre."
    m 1esa "However, another obvious fact is that knights play a big role in the competition for the center. So, by preventing the knight from moving, the bishop is also helping to compete for the center."
    m 1hub "This is also a kind of charm of pin the tactic, ahaha!"
    $ game.hide()
    show monika at t11
    m 1hua "Thanks for listening~"
    return

default persistent._mas_pm_chessteaching_player_know_two_rook_mate = None
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_mate_two_rook",
            category=["chess lessons"],
            prompt="Two Rook Mate",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_mate_two_rook:
    if mas_getEV("monika_chesslesson_mate_two_rook").shown_count > 0:
        m 1eub "Do you want to go straight to the test, or do you want to hear me lecture again?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want to go straight to the test, or do you want to hear me lecture again?{fast}"
            "To the test.":
                m 1hua "Okay!"
                m 1dsc "Hold on...{w=0.3}{nw}"
                show monika 1eua at t21
                jump monika_chesslesson_mate_two_rook_test
            "Please teach me again.":
                pass
    m 1hua "Okay, today we are going to talk about {i}Two Rook Mate{/i}."
    m 1hub "Two Rook Mate is actually the easiest mate situation in chess, so don't worry, this one would a easy one to learn!"
    m 1lub "Okay, let me get the board here..."
    #Let Monika move to left so we have enough room for board.
    show monika at t21

    # Call the board.
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/3k4/8/8/1R3K2/6R1 w - - 0 1")
        game.toggle_sensitivity()
        game.show()

    #Give player a few seconds to look at the board
    pause 2.0

    if seen_event("monika_chesslesson_whenwin"):
        m 1eub "Remember this situation?"
        m 3eub "Yes, it's the situation that we mentioned before!"
    m 1lub "This is what Two Rook Mate looks like--{w=0.2}One player has two rooks, and the other one has only the king."
    m 1eub "When we're playing the Two Rook Mate, if you're the attakcer, then your job is to push the opponent's king to the boundary of board."
    m 1eua "To understand why must we push the king to the side of board, let us assume that we didn't push the king to the boundary of board."
    m 1dsc "Hold on...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/3K4/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1.0)
        game.request_highlight_common_format("c4")
        game.request_highlight_common_format("c5")
        game.request_highlight_common_format("c6")
        game.request_highlight_common_format("d4")
        game.request_highlight_common_format("d6")
        game.request_highlight_common_format("e4")
        game.request_highlight_common_format("e5")
        game.request_highlight_common_format("e6")

    
    m 2lub "When a king is on a non-boundary part of the board, its range of movement is {i}8{/i} squares."
    m 2lsb "And,{w=0.2}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="3K4/8/8/8/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    extend 4lsb " if the king is on the borderline,{w=0.2}{nw}"
    python:
        game.request_highlight_common_format("c8")
        game.request_highlight_common_format("c7")
        game.request_highlight_common_format("d7")
        game.request_highlight_common_format("e8")
        game.request_highlight_common_format("e7")
    extend 4esb " it has only {i}5{/i} squares to go."
    m 4esa "Then, one thing that is clear is, one single rook can only control a maximum of 3 squares around the king at any one time."
    m 2lsa "Let me add one rook to the board to be clearer...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="3K4/7r/8/8/8/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        game.request_highlight_line(7)
        game.request_highlight_file('h')
    extend 2eub " Okay! See the movable range of this rook?"
    m 2etc "Though it controls a dozen of squares, but it's the squares next to the king that really matter."
    m 2ltd "In this situation, this rook controls 3 squares next to the king:{w=0.2} c7, d7, e7."
    m 2eub "So it's not hard to understand why I said a rook can only control a maximum of 3 squares around the king at any one time now."
    m 4eub "One rook can control a maximus of 3 squares, so two rooks, without doubt, can only control a maximum of 6 squares."
    m 4eua "And remember what I said? If a king is not on the boundary, then the king can move to 8 squares."
    m 4eud "That's a number bigger than two rooks can control! The king can always find a safe square that rooks are not controlling!"
    m 1eud "So, it's a must to push the king to the boundary."
    m 1eub "And about how to push the king to the boundary? Well, it's easy!"
    m 1lub "Let us back to the beginning of this lesson firstly...{w=0.5}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/3k4/8/8/1R3K2/6R1 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2.0)
        game.queue_move("g1g4")
        game.handle_player_move()
        renpy.pause(1.0)
    
    m 3lub "Firstly, white moved one rook to control line 4."
    python:
        game.request_highlight_line(4)
    m 3eub "See? There is no way black can let the king enter the line 4 now."
    m 2eua "And, of course, black can not just let the king enter the line 6, because line 6 is closer to the boundary."
    m 2eub "For more turns to survive, black should stay on the line 5."
    python:
        game.queue_move("d5e5")
        game.handle_monika_move()
        renpy.pause(1.0)
    m 2esb "But this won't change the final outcome. White could always moving another rook into the pushing process."
    python:
        game.queue_move("b2b5")
        game.handle_player_move()
        renpy.pause(1.0)
        game.request_highlight_line(5)
    m 2wsb "Notice that both the line 5 and the line 4 are being controlled by white now!"
    m 2lsb "Black must flee to line 6."
    python:
        game.queue_move("e5f6")
        game.handle_monika_move()
        renpy.pause(1.0)
    m 2lsa "Black is already giving it all. This is the best move black can play."
    m 2lsb "Now, white will simply keep limiting black's space..."
    show monika 2lsa
    python:
        game.queue_move("g4a4")
        game.handle_player_move()
        renpy.pause(1.0)
        game.queue_move("f6e6")
        game.handle_monika_move()
        renpy.pause(1.0)
        game.queue_move("a4a6")
        game.handle_player_move()
        game.remove_highlight_line(4)
        game.request_highlight_line(6)
        renpy.pause(1.0)
        game.queue_move("e6d7")
        game.handle_monika_move()
        renpy.pause(1.0)
        game.queue_move("b5b7")
        game.handle_player_move()
        game.remove_highlight_line(5)
        game.request_highlight_line(7)
        renpy.pause(1.0)
        game.queue_move("d7c8")
        game.handle_monika_move()
        renpy.pause(1.0)
        game.queue_move("a6a7")
        game.handle_player_move()
        game.remove_highlight_line(6)
        renpy.pause(1.0)
        game.queue_move("c8d8")
        game.handle_monika_move()
        renpy.pause(1.0)
    m 2esb "It's white's turn now. Black is on the boundary, unable to move to the line 7 for it was controlled by the rook on b7 square."
    m 2esu "So now, white can simply attack the line 8,{w=0.2}{nw}"
    python:
        game.queue_move("a7a8")
        game.handle_player_move()
        game.request_highlight_line(8)
    extend 2hsu "{i} Checkmate{/i}."
    $ game.hide()
    m 2hub "This is how Two Rook Mate works. The easiest checkmate endgame in chess."
    $ nickname = mas_get_player_nickname()# Make sure the nickname won't be different just due to switch into menu.
    m 2eub "If you're free now, I can set up a game like this for you right now to test."
    m 1eua "Ready for test, [nickname]?{nw}"
    $ _history_list.pop()
    menu:
        m "Ready for test, [nickname]?{fast}"
        "Yes.":
            m 1hua "Okay!"
            m 1hub "Then let us go!"
            jump monika_chesslesson_mate_two_rook_test
        "Not really.":
            m 1eka "Ahh, that's of course okay."
            m 3esb "If you want to test this checkmate endgame, just ask me again, okay?"
            m 3hub "For now, take your time, [player]~"
    
    $ game.hide()
    show monika at t11
    m 1hua "Thanks for listening!"
    return

label monika_chesslesson_mate_two_rook_test:
    python:
        space_king = random.randint(1,6)# Make the king position random to make sure this is not a repeative test.
        game = MASChessDisplayable(is_player_white = True, starting_fen = "8/8/8/8/" + str(space_king) + "k" + str(7-space_king) + "/R7/7R/2K5 w - - 0 1")
        game.show()
        game._visible_buttons.remove(game._button_save)
        results = game.game_loop()
        game.hide()

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results
        game_result = new_pgn_game.headers["Result"]
    
    if is_monika_winner:
        #Monika wins
        if is_surrender:
            # Monika wins by surrender from player
            m 2etd "Giving up, [player]?"
            m 2etb "Well, it's okay!"
            m 2rtc "But, still, I personally think that Two Rook Mate isn't a tough one...{w=0.2}{nw}"
            extend 2etd " Perhaps you should try to stay to the end next time?"
            m 1hub "If you still don't know how to do the Two Rook Mate, don't hesitate to ask me again!"
            m 1hua "I'm always willing to teach you~"
        else:
            #Player lost -- Which is impossible. Player must cheat on the game to reach this.
            m 2dsd "..."
            m 2dsu "You know it right?"
            m 2csu "This isn't a possible dialogue."
    elif game_result == "1/2-1/2":
        #stalemate.
        m 2essdla "..."
        m 2essdlb "Well, it seems that you may not have succeeded in understanding the lesson..."
        m 2esb "But don't worry, [player]!"
        m 2hub "That's not to say it's your fault. Maybe it's just because I didn't speak clearly enough, or just because you were not in the mood today."
        m 2eka "You can go relax now, get up and go for a walk or something, and we'll come back to this class later, okay?"
    else:
        #Player passed the test.
        m 2hub "Congrats! It seems like you've known Two Rook Mate well now!"
        m 2hua "I'm so glad I taught you something, ehehe~"
        m 2esu "But don't be too proud, after all, this is just the simplest of all the checkmate endgame..."
        m 2hub "Ahaha!"
        m 2hua "Since you're good at Two Rook Mate now, do you mind to learn the One Rook Mate now?{nw}"
        $ _history_list.pop()
        menu:
            m "Since you're good at Two Rook Mate now, do you mind to learn the One Rook Mate now?{fast}"
            "Yes, come on.":
                m "Okay!"
                jump monika_chesslesson_mate_one_rook
            "Maybe another time.":
                m "Alright, [player]."
                m "Then if you want to pick that lesson later, you can always directly ask me for One Rook Mate lesson, okay?"
                m "Thanks for listening!"
        $ persistent._mas_pm_chessteaching_player_know_two_rook_mate = True
    show monika at t11
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_mate_one_rook",
            category=["chess lessons"],
            prompt="One Rook Mate",
            pool=True,
            conditional="persistent._mas_pm_chessteaching_player_know_two_rook_mate == True",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_mate_one_rook:
    if mas_getEV("monika_chesslesson_mate_one_rook").shown_count > 0:
        m 1eub "Do you want to go straight to the test, or do you want to hear me lecture again?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want to go straight to the test, or do you want to hear me lecture again?{fast}"
            "To the test.":
                m 1hua "Okay!"
                m 1dsc "Hold on...{w=0.3}{nw}"
                show monika 1eua at t21
                jump monika_chesslesson_mate_one_rook_test
            "Please teach me again.":
                m 1hua "Fine!"
    m 1eub "One Rook Mate is an easy endgame, but it's a bit harder than Two Rook Mate."
    m 1lub "Let us see...{w=0.3}{nw}"
    show monika 1lua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/3k4/7R/8/1K6/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2.0)
    m 1eub "Remember what we said in Two Rook Mate lesson?"
    m 2eub "If we want to checkmate the opponent, then we should firstly push the king to the corner so we can limit its mobility."
    m 2eud "But how can we achieve this goal now?"
    m 2rud "In Two Rook Mate, if we want to push the king to the corner, the method is very simple."
    m "First, we use a rook to control a line so that the king can't move down. Then we use another rook to attack the line where the king is currently."
    m 2eud "But now? We have no another rook."
    $ game.request_highlight_line(5)
    m 2lud "Now, our rook blocks the possibility of the king moving closer to the center."
    m 2luc "Once it attacks the king directly now, then it's the opponent's turn. The king can always escape to the side of our attack line that is good for it."
    python:
        game.remove_highlight_line(5)
        game.queue_move("h5h6")
        game.handle_player_move()
        game.request_highlight_line(6)
        renpy.pause(1.0)
        game.queue_move("d6d5")
        game.handle_monika_move()
        renpy.pause(1.0)
    m 2wud "See? The king can always escape from our attacking!"
    m 1eud "So the One Rook Mate is a unsolvable proposition?"
    m 1eua "No.{w=0.3}{nw}"
    extend 1eub " In fact, there is a solution. When it comes to this solution, I have to tell you a main point of the endgames."
    $ extra_word = "!"
    if seen_event("monika_chesslesson_exchange_principle"):
        $ extra_word = ", and the king's combat capability worths 3 value points!"
        m 3eua "Do you remember what I told you in Exchange Principle the lesson?"
        m 2esd "Although, due to the particularity of the king, its value can be regarded as infinite."
        m 2esb "But if we don't consider its special position, just treat it as a normal chess piece, its combat capability is worth 3."
    else:
        m 2esb "I hope you haven't overlooked the obvious fact that we have a king besides the rook."
        m 2esu "And the king's fighting ability is not ordinary. It can control all the squares around it at the same time, which is also a combat power that can not be ignored."
    m 2eub "In endgames, even a tiny advantage is very important. Simply a slight advantage can often be extended to an overwhelming advantage."
    m 2esb "We usually don't move king, that's because we want it to be as safe as possible.{w=0.4}{nw}"
    extend 2etb " But now?{w=0.2}{nw}"
    extend 2etu " Is there anything in the situation that can threaten it?"
    m 2hua "It's time to bring it to the battlefield, too!"
    m 2esb "So, the point I want to say is, {i}in endgames, remember that the king can fight[extra_word]{/i}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/3k4/7R/8/1K6/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
    m 2eua "Now let us back to beginning, start thinking about how to push the king of our opponent to the boundary."
    m 2rud "Although the king can't control a whole line...{w=0.4}{nw}"
    extend 2eud " But, actually, we don't need to control a whole line in the first place."
    m 2eub "All we need is to make it impossible for our opponent's king to cross the blockade. So we just need to control 3 squares."
    python:
        game.request_highlight_common_format("c5")
        game.request_highlight_common_format("d5")
        game.request_highlight_common_format("e5")
        renpy.pause(0.5)
    m 2lub "Look at the 3 squares I have highlighted. If we are controlling these three squares now, after we move the rook to line 6, the opponent can only flee to the border, not to the other side."
    m 1eub "Isn't that exactly what a king can do? Therefore, let's take the king to this position and control those 3 squares."
    python:

        game.queue_move("b3c4")
        game.handle_player_move()
        renpy.pause(2.0)
    m 1esd "But then we will soon realize another problem. Our king can't get to that position in just one turn. Even if it is in a moment, after we move past, it is the opponent's turn."
    m 1lsd "Now, for example, opponents can escape like this.{w=0.4}{nw}"
    python:
        game.remove_highlight_common_format("c5")
        game.remove_highlight_common_format("d5")
        game.remove_highlight_common_format("e5")
        game.queue_move("d6e6")
        game.handle_monika_move()
    extend 1esd " So what now?"
    m 1esu "This problem is actually simple. If the opponent is running away, we will chase the opponent all the way."
    python:
        game.queue_move("c4d4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("e6f6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("d4e4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("f6g6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("h5a5")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("g6f6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("e4f4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("f6e6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("f4e4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("e6d6")
        game.handle_monika_move()
        renpy.pause(0.5)
    m 1esb "Chasing and chasing and chasing...{w=0.3} It seems that this will be an endless cycle, but notice that the chessboard is limited.{w=0.5}{nw}"
    extend 1tsu " The opponent has to go back eventually."
    m 1tsb "Let us just see a few more turns."
    show monika 1tsa
    python:
        game.queue_move("e4d4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("d6e6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("d4e4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("e6f6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("e4f4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("f6g6")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("f4g4")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("g6h6")
        game.handle_monika_move()
        renpy.pause(0.5)
    m 1tsb "{i}Try running again?{/i}{w=0.4} You can now say that to your opponent now."
    m 1esb "Notice you're controlling g5 square and h5 square now, the opponent's king can't move to line 5."
    m 1eub "Now that the blockade has been handed over to the king, let's move our rook and push it up a line!"
    show monika 1eua
    python:
        game.queue_move("a5a6")
        game.handle_player_move()
        renpy.pause(2)
    m "Have no choice but escape to the corner, the opponent fled."
    python:
        game.queue_move("h6h7")
        game.handle_monika_move()
        renpy.pause(2)
    m 1efb "Then we'll catch up, again!"
    show monika 1efa
    python:
        game.queue_move("g4g5")
        game.handle_player_move()
        renpy.pause(1)
    m 1esb "In order to survive a few more turns, the opponent has no choice but to try to move to the center first."
    python:
        game.queue_move("h7g7")
        game.handle_monika_move()
        renpy.pause(1)
    m 1efa "But nothing can change...{w=0.2}{nw}"
    extend 1efb " We march!"
    python:
        game.queue_move("a6a7")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("g7g8")
        game.handle_monika_move()
        renpy.pause(1)
    m 1euu "Now, the opponent has no space to flee. Let's move the king and continue to block its escape route!"
    python:
        game.queue_move("g5f6")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("g8h8")
        game.handle_monika_move()
        renpy.pause(0.5)
        game.queue_move("f6g6")
        game.handle_player_move()
        renpy.pause(0.5)
        game.queue_move("h8g8")
        game.handle_monika_move()
        renpy.pause(0.5)
    m 1hua "It's time to win!{w=0.2}{nw}"
    extend 1esu " The opponent no longer has room to escape, and the turn is ours now. We just need to simply push the rook to the line where the opponent's king is, that is,{w=0.4}{nw}"
    extend 1efu " {i}Checkmate{/i}!"
    python:
        game.queue_move("a7a8")
        game.handle_player_move()
        renpy.pause(1)
        game.request_highlight_common_format("f7")
        game.request_highlight_common_format("g7")
        game.request_highlight_common_format("h7")
    m 3esb "Notice that all the movable paths of the opponent's king are blocked by us, and there is no escape means for it, so this is a {i}Checkmate{/i}!"
    m 3hua "This is the general appearance of One Rook Mate."
    m "Obviously, it is a little more difficult than Two Rook Mate, but our idea is the same:{w=0.2}{nw}"
    extend 1eub " {i}force the opponent to the corner to limit the king's mobility, and then checkmate.{/i}"
    m 1eua "That's actually the idea for most of the endgame."
    if persistent._mas_pm_player_chesslevel == chesslevel_advancer or persistent._mas_pm_player_chesslevel == chesslevel_master:
        m 1rusdlb "Of course, you should have seen it for a long time: in this game, there are many better ways to finish the game faster."
        m 1eusdlb "But I think that's a clearer way of thinking... And considering that you play chess well, you should also know how to solve this kind of endgame more efficiently."
        m "I don't have to talk about the faster solutions that you already know, right?"
        m 1hua "So I'd like to thank you even more for being here!"
        $ extra_word = "a master" if persistent._mas_pm_player_chesslevel == chesslevel_master else "an advancer"
        m 1etd "Oh, by the way, even if you're [extra_word], maybe you'd like to brush up on your old knowledge too?"
        m 2esb "Would you like to test your One Rook Mate knowledge?{nw}"
        $ _history_list.pop()
        menu:
            m "Would you like to test your One Rook Mate knowledge?{fast}"
            "Yes.":
                m 2hua "Okay!"
                jump monika_chesslesson_mate_one_rook_test
            "No.":
                m 2ekb "Oh, alright!"
                m 2rssdlb "It's reasonable not to want to relearn something you've tested in the field countless times before after all..."
                m 2esb "But just in case that you want to test someday, rememver you can always ask me again!"
                m 2hua "Thanks for listening~"
    else:
        m 2rsd "Oh, and by the way, we actually had a lot of opportunities to end this game faster."
        m 2lsd "Like this position...{w=0.3}{nw}"
        python:
            game.hide()
            game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/6k1/R7/5K2/8/8/8 w - - 6 4")
            game.toggle_sensitivity()
            game.show()
        extend 2esd " At this point, white could play Rf5, you know?"
        if seen_event("monika_chesslesson_pgn") == False:
            m 2eub "Speaking of \"Rf5\", it's a format to record moves, called PGN format."
            m 2eua "Rf5 stands for \"Rook move to f5\"."
            m "If you want to know more about the PGN format, I have prepared another lesson for you, and you can attend that lesson later."
            m 2eub "Now, back to our current class."
        m 2lub "If white played Rf5, then, the situation is like this."
        show monika 2lua
        python:
            game.queue_move("a5f5")
            game.handle_player_move()
            renpy.pause(1)
            game.request_highlight_common_format("g5")
            game.request_highlight_common_format("h5")
            game.request_highlight_common_format("f6")
            game.request_highlight_common_format("f7")
            game.request_highlight_common_format("f8")
            renpy.pause(1)
        m 2eua "Notice that we are immediately confining our opponent's king to a very small space."
        m 2eub "We left only 6 squares for the opponent to go."
        m 2hub "From now on, even if the opponent uses the best moves, we will only need 6 turns to win."
        m 2eub "This kind of sudden change of thinking is not easy to teach, but you can learn it later in the actual chess game."
        m 2euu "For example, now..."
        m 2efu "It's time for a final exam!{nw}"
        $ game.hide()
        $ _history_list.pop()
        menu:
            m "It's time for a final exam!{fast}"
            "Come on.":
                m 2hua "Okay!"
                jump monika_chesslesson_mate_one_rook_test
            "Maybe another time.":
                m 2eub "Alright, [player]."
                m 2eua "Just ask me about it later if you want to test it."
                m 2hua "For now, thanks for listening!"
    show monika at t11
    return

label monika_chesslesson_mate_one_rook_test:
    python:
        space_king = random.randint(1,6)
        space_rook = random.randint(1,6)
        game = MASChessDisplayable(is_player_white = True, starting_fen = "8/8/"+str(space_king)+"k"+str(7-space_king)+"/8/"+str(space_rook)+"R"+str(7-space_rook)+"/3K4/8/8 w - - 0 1")
        game.show()
        game.stockfish.stdin.write("setoption name Skill Level value 20\n")
        game._visible_buttons.remove(game._button_save)
        results = game.game_loop()
        game.hide()

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results
        game_result = new_pgn_game.headers["Result"]
    
    if is_monika_winner:
        #Monika wins
        if is_surrender:
            # Monika wins by surrender from player
            m 2etd "Giving up, [player]?"
            m 2etb "Well, it's okay!"
            m 2rtc "Indeed, One Rook Mate is a bit of a difficult proposition..."
            m "If you're not sure whether you've mastered this lesson, let's go over the lesson again, shall we?"
            m 1hua "I'm always willing to teach you~"
        else:
            #Player lost -- Which is impossible. Player must cheat on the game to reach this.
            m 2dsd "..."
            m 2dsu "You know it right?"
            m 2csu "This isn't a possible dialogue."
    elif game_result == "1/2-1/2":
        #stalemate.
        m 2essdla "..."
        m 2essdlb "Well, it seems that you may not have succeeded in understanding the lesson..."
        m 2esb "But don't worry, [player]!"
        m 2hub "That's not to say it's your fault. Maybe it's just because I didn't speak clearly enough, or just because you were not in the mood today."
        m 2eka "You can go relax now, get up and go for a walk or something, and we'll come back to this class later, okay?"
    else:
        #Player passed the test.
        m 2hub "Congrats! It seems like you've known One Rook Mate well now!"
        m 2hua "I'm so glad I taught you something, ehehe~"
        m "If you are interested in any other endgame, always ask me!"
        m "It is always a great pleasure for me to be able to teach someone I love~"
    show monika at t11
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_mate_queen",
            category=["chess lessons"],
            prompt="Queen Mate",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_mate_queen:
    if mas_getEV("monika_chesslesson_mate_queen").shown_count > 0:
        m 1eub "Do you want to go straight to the test, or do you want to hear me lecture again?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want to go straight to the test, or do you want to hear me lecture again?{fast}"
            "To the test.":
                m 1hua "Okay!"
                m 1dsc "Hold on...{w=0.3}{nw}"
                show monika 1eua at t21
                jump monika_chesslesson_mate_queen_test
            "Please teach me again.":
                m 1hua "Fine!"
    if seen_event("monika_chesslesson_mate_one_rook") or seen_event("monika_chesslesson_mate_two_rook") or seen_event("monika_chesslesson_mate_bishops"):
        m 1eub "Queen Mate is another important endgame pattern in chess."
    else:
        m 1eub "Queen Mate is an important endgame pattern in chess."
    m 1eud "It's not as easy as Two Rook Mate, but at least easier than One Rook Mate."
    if seen_event("monika_chesslesson_mate_one_rook"):
        m 1uhsdlb "So if you had some trouble understanding One Rook Mate before, don't worry.{w=0.2} This One is a little easier than that One."
    m 1duc "Now, let me get pieces set...{w=0.5}{nw}"
    show monika 1lua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/4k3/2Q5/3K4/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 1eud "The queen is the most powerful piece in chess, and can control countless squares at the same time."
    m 1euc "But even so, we can't checkmate in no momnent with the current situation."
    m 1eud "For example, let's move the queen to d4 square."
    show monika 1lud
    python:
        game.queue_move("c4d4")
        game.handle_player_move()
        renpy.pause(1)
        game.request_highlight_common_format("d5")
        game.request_highlight_common_format("d6")
        game.request_highlight_common_format("e4")
        game.request_highlight_common_format("f4")
        game.request_highlight_common_format("f6")
        renpy.pause(1)
    m 3eud "King that is in center has a range of 8 squares, and even though our queen is now completely close to it, we still haven't been able to attack all 8 squares at once."
    m 2ruc "These 5 squares that I've highlighted, that's the limit of the queen's control."
    if seen_event("monika_chesslesson_mate_one_rook"):
        m 2eub "Since you have learnt One Rook Mate, you've probably got the idea to solve this problem."
        m 2eua "Yes, push the king to the corner."
    else:
        m 2esb "But pay attention to the choice of words I just used."
        m 2esa "\"King that is in center\", the point is \"in center\"."
        m "If the king isn't in center, then its mobility is damaged."
        m 2esb "So the question at this stage is how to bring the king into a corner."
    m 2eub "Fortunately, with the power of the queen, it's fairly easy to do this."
    m 2lub "Now, for example, what squares does the queen control?"
    python:
        game.remove_highlight_common_format("d5")
        game.remove_highlight_common_format("d6")
        game.remove_highlight_common_format("e4")
        game.remove_highlight_common_format("f4")
        game.remove_highlight_common_format("f6")
        game.request_highlight_file('d')
        game.request_highlight_line(4)
        game.request_highlight_diagonal("a1","h8")
        game.request_highlight_diagonal("a7","g1")
    m 2wub "Almost every nook and cranny! Such is the power of a queen!"
    m 2eub "The opponent's king only has two choices to escape, e6 or f5. Let's take f5 as an example to see how to pursue."
    show monika 2lua
    python:
        game.queue_move("e5f5")
        game.handle_monika_move()
        renpy.pause(1)
        game.remove_highlight_file('d')
        game.remove_highlight_diagonal("a1","h8")
        game.remove_highlight_diagonal("a7","g1")
        game.queue_move("d4e4")
        game.handle_player_move()
        game.request_highlight_file('e')
        game.request_highlight_diagonal("b1","h7")
        renpy.pause(1)
    m 2lfb "One step back, and we're on its heels!"
    m 2efa "Opponents still have no choice but to keep running!"
    show monika 2eua
    python:
        game.queue_move("f5g5")
        game.handle_monika_move()
        renpy.pause(1)
    m 2etd "And then here, we have to have a little bit of an interlude."
    m 3etd "We had always dared to put our queen next to our opponent's king, because our queen had the king beside it to guard it."
    m "But now? We mustn't get too excited and move the queen straight to f4. In that case, the opponent can remove our queen. The winning game becomes a stalemate."
    m 2esd "We must first move our king over, and bring our queen closer to absolute safety."
    m 2lsd "So one of the correct move in this situation would be:{w=0.8}{nw}"
    show monika 2lsc
    python:
        game.queue_move("d3e3")
        game.handle_player_move()
        renpy.pause(1)
    m "The opponent, on the other hand, must not sit still. They must actively try to get a safer position."
    python:
        game.queue_move("g5f6")
        game.handle_monika_move()
        renpy.pause(1)
    m 2lsb "Then, we will continue the chase."
    show monika 2lsa
    python:
        game.queue_move("e3f4")
        game.handle_player_move()
        renpy.pause(1)
    m 2esb "Once again, the opponent will flee."
    m 4esb "We just keep catching up."
    show monika 2esa
    python:
        game.queue_move("f6f7")
        game.handle_monika_move()
        renpy.pause(1)
        game.queue_move("f4f5")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("f7g8")
        game.handle_monika_move()
        renpy.pause(1)
        game.queue_move("f5f6")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("g8h8")
        game.handle_monika_move()
        renpy.pause(1)
        game.remove_highlight_line(4)
        game.remove_highlight_diagonal("b1","h7")
        game.queue_move("e4e7")
        game.handle_player_move()
        game.request_highlight_line(7)
        game.request_highlight_diagonal("a3","f8")
        renpy.pause(2)
        game.queue_move("h8g8")
        game.handle_monika_move()
        renpy.pause(1)
    m 4lsb "In the end, there was no room to escape, so we moved the queen over and {i}Checkmate{/i}."
    show monika 4lsa
    python:
        game.remove_highlight_file('e')
        game.remove_highlight_diagonal("a3","f8")
        game.remove_highlight_line(7)
        game.queue_move("e7g7")
        game.handle_monika_move()
        renpy.pause(1)
    m 2hub "This is the idea of Queen Mate."
    if seen_event("monika_chesslesson_mate_one_rook"):
        m 2eub "Remember One Rook Mate you learnt before?"
        m 2eud "In fact, in the final analysis, Queen Mate is the same idea with other endgames, which is to corner the king, then checkmate."
    else:
        m 2eub "Further, this is the idea behind almost any endgame:"
        extend 2eua " corner the king and checkmate."
    m 2rud "If you want me to say that there is any point to this mate...{w=0.4}{nw}"
    extend 2eud " {i}Remember to avoid stalemate{/i}."
    m 2euc "Yes, avoid stalemate. This is actually a common beginner's mistake."
    m 2eud "I just said, don't put your queen near your opponent's king without the king's protection."
    m 2husdrb "That's an example of a stalemate, but that mistake is so obvious that most people can avoid it."
    m 2eusdrb "In fact, in this proposition, there are many kinds of possibilities to draw, beginners to draw chess is more than common..."
    m 2eud "Let me give you one example."
    show monika 2eua
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/8/2Q5/k2K4/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m 2esd "See this? What do you want to play now?"
    m 1rsd "Obviously, we can move the king closer to prepare for the Checkmate."
    m 1lsd "So let's play this move...{w=0.4}{nw}"
    python:
        game.queue_move("d3c3")
        game.handle_player_move()
    extend 1esd " Alright, so what now?"
    m 1esc "..."
    m 1esd "If you're wondering what your opponent is going to do, then you've probably discovered a terrible truth."
    python:
        game.request_highlight_common_format("a2")
        game.request_highlight_common_format("b2")
        game.request_highlight_common_format("b3")
        game.request_highlight_common_format("b4")
        game.request_highlight_common_format("a4")
    m 1wsd "All squares around the opponent's king are under our control."
    m "But have we attacked our opponent's king now?"
    m 1wso "No! The opponent's king is not under attack at this time!"
    m "So what can the opponent do now? Not anywhere! No matter what it chooses to do, going to any square is a direct attack from us!"
    m 1wsd "This is a {i}stalemate{/i} now!"
    m 2etc "It should have been a sure win, but that careless move ruined it..."
    m 2etd "If you think that's all there is to it, no. There's one more common case that I'll mention."
    show monika 2ltc
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/8/8/4K3/5Q2/7k w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m 2etd "It's white's turn now, what should white do?"
    m 2esc "Let me tell you straight to the conclusion.{w=0.2}{nw}"
    extend 2esd " As long as you don't move your queen to a position further from the opponent's king, you are taking the wrong way."
    python:
        game.request_highlight_common_format("f1")
        game.request_highlight_common_format("g2")
        game.request_highlight_common_format("h2")
        game.request_highlight_common_format("g1")
    m 2lsd "You see these 4 highlighted squares?"
    m 2lsc "This situation must be the white side all the way after the black side, the black side just escaped again after the formation of the situation."
    m 2esd "Now, black had nowhere else to go, and if white wanted to move their king, it would be an immediate stalemate."
    m 2esc "White's only option was to move the queen out of the way and make room for black to move."
    m 1rsd "Then look for another chance to checkmate the black."
    m 1eua "Let me show you how to deal with this situation."
    python:
        game.remove_highlight_common_format("f1")
        game.remove_highlight_common_format("g2")
        game.remove_highlight_common_format("h2")
        game.remove_highlight_common_format("g1")
        game.queue_move("f2e2")
        game.handle_player_move()
        renpy.pause(1)
    m 1eub "The first is to take a step back and give the opponent a space."
    m 3eub "Note that our goal is to avoid a draw, not \"let your opponent be free\".{w=0.3} So we should move only one square."
    show monika 2lua 
    python:
        game.queue_move("h1g1")
        game.handle_monika_move()
        renpy.pause(1)
        game.queue_move("e3f3")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("g1h1")
        game.handle_monika_move()
        renpy.pause(1)
    m 2lub "Since the opponent has only two squares to move, they have to switch between them repeatedly."
    m 2eub "When it had to wait for failure, we moved the king slowly."
    m 2eua "Finally, when it comes to situations like this, we {i}Checkmate{/i}."
    python:
        game.queue_move("e2g2")
        game.handle_player_move()
        renpy.pause(1)
    m 2husdra "As you may have noticed by now, the possibility of a stalemate in this proposition is quite large, so it is not hard to understand why many beginners draw."
    m 2rusdra "It is also impossible to systematically incorporate them all into the lesson..."
    m 2rusdrb "Because they are...{w=0.4}{nw}"
    extend 2eub " the kind of things that are more likely to be felt in the actual game."
    m 2esa "So now..."
    $ game.hide()
    m 2efb "Time for a real game!{nw}"
    $ _history_list.pop()
    menu:
        m "Time for a real game!{fast}"
        "Okay, come on!":
            m 2eub "Then, here we are!"
            jump monika_chesslesson_mate_queen_test
        "Maybe another time.":
            m 2eta "Alright."
            m 1eub "If you want to test later, just ask me, okay?"
            m 1hua "Thanks for listening~"
    show monika at t11
    return

label monika_chesslesson_mate_queen_test:
    python:
        game = MASChessDisplayable(is_player_white = True, starting_fen = "8/8/8/4k3/8/1Q6/2K5/8 w - - 0 1")
        game.show()
        game._visible_buttons.remove(game._button_save)
        game.stockfish.stdin.write("setoption name Skill Level value 20\n")
        results = game.game_loop()
        game.hide()

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results
        game_result = new_pgn_game.headers["Result"]
    
    if is_monika_winner:
        #Monika wins
        if is_surrender:
            # Monika wins by surrender from player
            m 2etd "Giving up, [player]?"
            m 2etb "Hopefully you're not just finding yourself stuck in a phase..."
            m 2rtc "After all, when I first learned this proposition, I did not know what to do at the end."
            m "If you're not sure whether you've mastered this lesson, let's go over the lesson again, shall we?"
            m 1hua "I'm always willing to teach you~"
        else:
            #Player lost -- Which is impossible. Player must cheat on the game to reach this.
            m 2dsd "..."
            m 2dsu "You know it right?"
            m 2csu "This isn't a possible dialogue."
    elif game_result == "1/2-1/2":
        #stalemate.
        m 2essdla "..."
        m 2essdlb "Oh my gosh, it looks like the chance of this endgame's stalemate is really high."
        m 2esb "But don't worry, [player]!"
        m 2hub "That's not to say it's your fault. Maybe it's just because I didn't speak clearly enough, or just because you were not in the mood today."
        m 2eka "You can go relax now, get up and go for a walk or something, and we'll come back to this class later, okay?"
    else:
        #Player passed the test.
        m 2hub "Congrats! It seems like you've known Queen Mate well now!"
        m 2hua "I'm so glad I taught you something, ehehe~"
        m "If you are interested in any other endgame, always ask me!"
        m "It is always a great pleasure for me to be able to teach someone I love~"
    show monika at t11
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_mate_bishops",
            category=["chess lessons"],
            prompt="Two Bishops Mate",
            pool=True,
            conditional="seen_event('monika_chesslesson_mate_one_rook')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_mate_bishops:#UNFINISHED
    if mas_getEV("monika_chesslesson_mate_bishops").shown_count > 0:
        m 1eub "Do you want to go straight to the test, or do you want to hear me lecture again?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you want to go straight to the test, or do you want to hear me lecture again?{fast}"
            "To the test.":
                m 1hua "Okay!"
                m 1dsc "Hold on...{w=0.3}{nw}"
                show monika 1eua at t21
                jump monika_chesslesson_mate_bishops_test
            "Please teach me again.":
                m 1hua "Fine!"
    
    m 1eub "Two Bishops Mate is another endgame pattern in chess."
    m 1eud "And, it's a difficult one."
    m 1euc "Especially compared to the Two Rook Mate you have learned, the difficulty of this one is simply high terrible."
    m 3eud "You're probably already having a hard time with the One Rook Mate, right?{w=0.3}{nw}"
    extend 3rusdrb " But this is even harder than that."
    m 3eusdrb "So, what I want to express is..."
    m 2eua "It's perfectly normal if you can't learn it, because it's a tough one."
    m 1euc "Moreover, this endgame itself is rare.{w=0.2}{nw}"
    extend 1rtc " People don't usually face a endgame like this at all."
    m 3etd "I looked at this endgame for a whole day or two before I figured out how to solve it, when I was studying chess myself."
    m 3husdlb "...{w=0.2}Well, I won't keep you in suspense.{w=0.2} Let's just get started."
    m 2duc "Hold on...{w=0.4}{nw}"
    show monika 2luc at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/8/4k3/8/8/2B1KB2 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 2eud "I taught you earlier in other endgame patterns that we have to corner the opponent's king in the endgame to checkmate."
    m 2etd "After all, even a powerful queen cannot complete a checkmate in the center of the board."
    m 1rtc "Not to mention two bishops who were obviously weaker than a queen."
    m 1eua "So this endgame is firstly a question of how to push the king to a corner."
    m "What we are seeing now is the most ideal situation for black. Black's king is in the center, far from boundary, and white's bishops were not activated too."
    m "But even so, it is not impossible to push the king to corner."
    m "The first thing we should do is to bring our king closer to the opponent's king."
    python:
        game.queue_move("e1e2")
        game.handle_player_move()
    m "When it comes to the opponent's turn, the opponent has a lot of choices, so let's analyze them one by one."
    python:
        game.queue_move("")
    return 

default persistent._mas_pm_chessteaching_player_know_two_bishop_mate = False
label monika_chesslesson_mate_bishops_test:#DIALOGUE UNFINISHED
    python:
        game = MASChessDisplayable(is_player_white = True, starting_fen = random.choice(["8/8/8/2KB4/3B4/8/4k3/8 w - - 0 1","8/8/2k1B3/4B3/2K5/8/8/8 w - - 0 1","8/8/2K1B3/4B3/1k6/8/8/8 w - - 0 1","8/4k3/8/5K2/2B5/2B5/8/8 w - - 0 1"]))
        game.show()
        game._visible_buttons.remove(game._button_save)
        game.stockfish.stdin.write("setoption name Skill Level value 20\n")
        results = game.game_loop()
        game.hide()

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results
        game_result = new_pgn_game.headers["Result"]
    
    if is_monika_winner:
        #Monika wins
        if is_surrender:
            # Monika wins by surrender from player
            m 2eka "Giving up, [player]?"
            m 2ekb "Well, that's nothing wrong! It's not an easy proposition after all."
            m 2esb "Just remember, if you want to learn it again, feel free to ask me!"
            m 1hua "I'm always willing to teach you~"
        else:
            #Player lost -- Which is impossible. Player must cheat on the game to reach this.
            m 2dsd "..."
            m 2dsu "You know it right?"
            m 2csu "This isn't a possible dialogue."
    elif game_result == "1/2-1/2":#DIALOGUE UNFININSHED.
        #stalemate.
        m 2essdla "..."
        m 2essdlb "Oh my gosh, it looks like the chance of this endgame's stalemate is really high."
        m 2esb "But don't worry, [player]!"
        m 2hub "That's not to say it's your fault. Maybe it's just because I didn't speak clearly enough, or just because you were not in the mood today."
        m 2eka "You can go relax now, get up and go for a walk or something, and we'll come back to this class later, okay?"
    else:
        #Player passed the test.
        if mas_getEV("monika_chesslesson_mate_bishops_test").shown_count <= 1:
            if persistent._mas_pm_chessteaching_player_know_two_bishop_mate == False:
                m "Wow! Gosh, you are really learning fast!"
                m "Although I know you can reach anything you want...{w=0.2} But I was surprised to see how quickly you solved this proposition!"
                m "Even should say I have a little sigh not as good as you..."
                m "Ahaha!"
            else:
                m "Even another victory, [player]?"
                m "Ahaha, you are really talented!"
        else:
            if persistent._mas_pm_chessteaching_player_know_two_bishop_mate == False:
                m "Congratulations! It seems that you have succeeded in learning the endgame after several failures!"
                m "This endgame is really hard, so this is really something to celebrate!"
            else:
                m "Oh, another win!"
                m "The endgame seems to have left a deep impression on you, huh?"
                m "Ahaha!"
        m "Anyways, if you are interested in any other endgame, always ask me!"
        m "It is always a great pleasure for me to be able to teach someone I love~"
        $ persistent._mas_pm_chessteaching_player_know_two_bishop_mate = True
    show monika at t11
    return


###
#Let's put this endgame on hold.
#This endgame is just so difficult that many grandmasters don't even consider learning it.
#Maybe I'll finish it some day when I'm free, but for now, just leave it there.
#
#init 5 python:
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_chesslesson_mate_bishop_and_knight",
#            category=["chess lessons"],
#            prompt="Bishop and Knight Mate",
#            pool=True,
#            conditional="seen_event('monika_chesslesson_mate_bishops')",
#            action=EV_ACT_UNLOCK,
#            rules={"no_unlock":None}
#        )
#    )
###

label monika_chesslesson_mate_bishop_and_knight:
    m 3esd "{i}Bishop and Knight mate{/i} is the most, most difficult of all mate endgames."
    m 3wsd "It's not a level of difficulty that beginners can learn at all! You have to be a professional player of chess to understand it!"
    m 2esc "Moreover, in actual game, it is almost impossible to face this kind of endgame."
    m 2rtd "I haven't really counted, but what you want me to say...{w=0.2}{nw}"
    extend 2esd " I'm guessing there's only one out of hundreds of Bishop and Knight Mate."
    m 2rssdra "To be honest, I can't even say that I really know how to play this endgame..."
    if persistent._mas_pm_player_chesslevel == chesslevel_beginner or _mas_pm_player_chesslevel == chesslevel_didntevenbegin:
        m 2eksdra "So..."
        m 2eka "I don't despise you, but I really think you might not be right for this class."
        m "After all, you said, your level on chess is not high..."
        m 2esd "I mean, it could possibly be a waste of your time..."
        m 2esc "Do you still want to learn this one?{nw}"
        $ _history_list.pop()
        menu:
            m "Do you still want to learn this one?{fast}"
            "Yes.":
                m 2hub "Well, I'll try my best to explain the endgame to you!"
            "No.":
                m 2eka "Okay, [player]."
                m 2ekb "Ah, just don't feel like it's because you're incompetent."
                m 2esa "This endgame is just too difficult."
                m 2hub "If you think you want to learn later, just ask me again, okay?"
                return
    elif persistent._mas_pm_player_chesslevel == chesslevel_advancer:
        m 2esd "But, you've told me before that you have a certain amount of expertise in chess."
        m 2esa "So I think you should be able to understand this lesson..."
        m 2hssdra "But even if you don't, let's not feel bad. That's not your problem."
        m 2eub "Now, let us begin!"
    else:
        m 2lusdla "I know you said you were a master at chess...{w=0.3}{nw}"
        extend 2esd " But I've heard that there is a lot of masters who don't know how to play this endgame."
        m 2esc "So I think this class is one of the few things I can teach you...{w=0.2}{nw}"
        extend 2hssdlb " Ehehe?"
        m 2esb "Anyways, let us begin the lesson."
    m "Let's set up the chessboard...{w=0.5}{nw}"
    show monika at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="8/4N3/3B4/2K5/4k3/8/8/8 w - - 1 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m "The current game in front of your eyes is what the Bishop and Knight Mate looks like."
    m "You've already heard me talk about Two Bishop Mate, so you know that in endgame, the first thing we should do is put the opponent's king into a corner."
    m "Is was already difficult enough to corner king in Two Bishop Mate."
    m "Here, it's even harder."
    m "Let's think about how we can corner it."
    if condition:
        m ""
    python:
        game.request_highlight_common_format("")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_exchange_principle",
            category=["chess lessons"],
            prompt="Exchange - The basic idea",
            pool=True,
            conditional="seen_event('monika_chesslesson_init_finished')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_exchange_principle:
    m 1eua "If you sometimes struggle with how to determine whether or not to exchange, then this lesson is for you."
    m 1duc "Firstly, let me get the board...{w=0.3}{nw}"
    show monika 1eua at t21
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="1kr5/8/8/5B2/5KR1/8/8/8 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m 1eud "You see this situation?"
    m 1euc "It's white to move now, and there is a chance for white to remove black's rook with the bishop."
    m 2rud "No doubt, when white's bishop removes the rook, the king of the black will remove the bishop too."
    m 2eud "So this question turns into another question:{w=0.3}{nw}"
    extend 2etd " Is it worth to exchange a rook with a bishop?"
    m 2eua "What do you say, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you say, [player]?{fast}"
        "I think it's worth.":
            m 2hub "Yes, you're right!"
            m 2hua "In fact, this is not just worth, this is a winning move!"
        "I think white can play some else move.":
            m 2eusdra "Hmm...{w=0.2}{nw}"
            extend 2eusdrb "Well, sorry, [player].{w=0.2} But, this is actually the best move."
    m 2eub "If white exchanged that rook with the bishop, then the situation changes to this:{w=0.2}{nw}"
    show monika 2lua
    python:
        game.queue_move("f5c8")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("b8c8")
        game.handle_monika_move()
        renpy.pause(1)
    m 2eub "White has a rook in addition to the king, and black has only one king."
    m 3eub "Even if a person who don't know much about chess can tell that white is in a winning position."
    if seen_event("monika_chesslesson_mate_one_rook"):
        m 3eua "To be more exact, in that situation, this game turns into One Rook Mate the endgame."
        m 1eua "And you know that the attacker of One Rook Mate is going to win, this is set in stone already.."
    else:
        m 3eua "In that situation, this games turns into {i}One Rook Mate{/i} the endgame."
        m 1eub "That's an important endgame pattern in chess."
        m 1hua "If you don't know much about that endgame, I'm willing to teach you~"
        m 1eub "In this endgame, as long as there are no big blunders, the player with a rook wins."
    m 1eua "So the conclusion is, it's worth exchanging a bishop for a rook. At least in this case."
    m 1esd "Now, the question is, is it always worth exchanging a bishop for a rook?"
    m 1esb "The answer is, it's worth it in almost all cases."
    m 2esa "To explain this answer, we need to mention the forces of each piece."
    m 2rsd "Apparently, no one who knew even a little about chess would ever exchange a queen for a pawn."
    m 2esd "And when you ask them why, the answer may be different, but the basic idea is the same."
    m 2esc "That is, {i}a queen can do far more things than a pawn{/i}."
    m 2esd "This sense is self-evident.{w=0.2} Similarly, you'll rarely see a rook exchange pawn because {i}rooks can do far more things than pawns{/i}."
    m 2etd "But now there is another problem.{w=0.2}{nw}"
    extend 2etc " If you trade 3 pawns for one rook, is it worth it?"
    m 1rtc "Or, 5 pawns for a queen?"
    m 1esd "Of course, these two problems need to be analyzed in detail.{w=0.2}{nw}"
    extend 1esb " There are cases where it's not worth it, but I would say that in most cases it's worth it to trade 5 pawns for a queen or 3 pawns for a rook."
    m 1esa "For a long time, people calculated the force of the pieces in chess."
    m 1esb "The final conclusion is..."
    m 1eua "{i}Taking pawns as the base unit, denote it as value 1.{w=0.2}Then, a knight is worth 3, and a bishop is worth 3, too. A rook is worth 5, and a queen is worth 9.{/i}"
    m 1esd "But, that conclusion, of course, has been rethought in recent years."
    m 2rsd "The current consensus is that the queen's value should be higher, like 10 or something.{w=0.2}{nw}"
    extend 2lsc " Bishops should be slightly higher than knights, like 3.1 or so."
    m 2lssdrb "But this view is still controversial...{w=0.2}{nw}"
    extend 2esb " For now, let's go with: pawn value 1, knight and bishop value 3, rook value 5, queen value 9."
    m 2etd "The special case is the king."
    m 1etd "King has a special meaning in chess. Once it is checkmated, the game is lost."
    m 1rtc "So, in some sense, the king's value should be infinite."
    m 1duc "But if you don't consider this issue, just consider its combat capability...{w=0.3}{nw}"
    extend 1eud " It's worth about 3."
    m 1eub "Now that we know this conclusion, we can easily answer the previous two questions."
    m 3eub "3 pawns are worth 3 and one rook is worth 5. After the exchange, the other player loses more materials. So it's worth it."
    m 3hua "5 pawns are worth 5 and a queen is worth 9. After the exchange, the player that loses the queen also loses more materials and is therefore worth it, too."
    m 3eka "This may sound obvious, but it's actually very useful.{w=0.2}{nw}"
    extend 3esa " It specifically quantifies the value of each piece, allowing people to use rigorous logical calculations to know if it's worth it."
    m 2rsd "And of course, material forces can not be the only criterion..."
    m 2esd "Sometimes even if you lose a piece to a play, but other pieces are in a particularly advantageous position after the play, then it may be worth it."
    if mas_seenLabels("monika_chesslesson_points_2"):
        m 2husdlb "Hmm...{w=0.2}{nw}"
        extend 1lusdlb " That reminds me of something I once told you."
        m 1lksdla "You remember what I said?{w=0.2} These principles in chess are always followed by a condition like \"usually so\", and here it is."
        m 1eka "If you remember, then you usually also remember that I said this is to make sure that the beginner doesn't at least make a terrible mistake."
        m 1essdrb "Oh, gosh, chess is complicated, isn't it?"
        m 1hssdrb "Ahaha..."
        m 1esb "But don't worry!"
    m 1esa "As for the further principle of exchange, I plan to teach you about it in another lesson in the future."
    m 1esb "For now, we can use this conclusion for the time being."
    m 1hub "Remember:{w=0.2} {i}a pawn is worth 1, a bishop is worth 3, a knight is also worth 3, a rook is worth 5, and a queen is worth 9. Just considering combat ability, a king is worth 3{/i}."
    $ game.hide()
    show monika at t11
    m 1hua "This should be enough for a basic idea lesson."
    m "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_exchange_principle_advance",
            category=["chess lessons"],
            prompt="Exchange - Sacrificial exchange",
            pool=True,
            conditional="seen_event('monika_chesslesson_exchange_principle')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_exchange_principle_advance:#UNFINISHED
    m "In this lesson we are going to talk about further considerations when making a balance."
    m "As I said before, there are many other factors besides the material forces that are considered when making a piece."
    m "Well, it's not quite exact."
    m "In fact, there are only two elements to judge the superiority of the situation, that is, the position of materials and material forces."
    m "After all, the only winning condition in chess is to checkmate the opponent."
    m "It doesn't matter how many pieces you successfully removed from your opponent, or how many pieces you still have."
    m "Just a moment, I'll bring up a game of chess...{w=0.5}{nw}"
    show monika at t11
    python:
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="2k5/4R1R1/8/2n5/q4q2/7r/1K4b1/1b2n2r w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(2)
    m "See? This is one example."
    m "Now it's White's turn. Who do you think has the advantage?{nw}"
    $ _history_list.pop()
    menu:
        m "Now it's White's turn. Who do you think has the advantage?{fast}"
        "The white side.":
            m "Yes, you're right."
        "The black side.":
            m "Hmm...{w=0.2} Sorry [mas_get_player_nickname()], but that's the wrong answer. "
    m "In fact, the white side doesn't even have an advantage, it has a overwhelming advantage."
    m "The black's material forces almost completely overwhelms the white's material forces, but that doesn't help."
    m "White simply needed to move a rook to win the game."
    m "Let us see...{w=0.2}{nw}"
    python:
        game.queue_move("g7g8")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("f4f8")
        game.handle_monika_move()
        renpy.pause(1)
        game.queue_move("g8f8")
        game.handle_player_move()
        renpy.pause(1)
        game.queue_move("a4e8")
        game.handle_monika_move()
        renpy.pause(1)
        game.queue_move("f8e8")
        game.handle_player_move()
        renpy.pause(1)
    m "Black has no way of reversing this result. It was a losing game for black."
    m "The reason is simple. Black's pieces are out of position."
    m "If Black had a line 8 rook, the situation would be completely different."
    m "It doesn't even have to be a rook, even if it's a bishop or a knight, then black is a sure win."
    m "But unfortunately no ifs.{w=0.2} The fact of the matter is that the position of black's pieces is just that bad. Material forces advantage is just useless."
    m "So, sometimes, if there's a move that even if it looks silly, even if it's going to lose materials, as long as it's going to help you get a perfect piece position, go for it."
    m "And about how to know the position of a piece is good or bad..."
    m "I do have a series of lessons devoted to them. I will not speak here, that will be too wordy and too fragmentary..."
    m "But here I can talk about one special case:{w=0.2} {i}sacrificial exchange{/i}."
    m "Oh, hold on...{w=0.3}{nw}"
    python:
        game.hide()
        game = MASChessDisplayableBase(is_player_white=True,starting_fen="1knb4/3r2r1/2Q3q1/p7/K1N1p1bp/1PR3p1/8/6B1 w - - 0 1")
        game.toggle_sensitivity()
        game.show()
        renpy.pause(1)
    m "Now it's white's turn. Before I begin, I want to ask, who do you think has the advantage?{nw}"
    $ _history_list.pop()
    menu:
        m "Now it's white's turn. Before I begin, I want to ask, who do you think has the advantage?{fast}"
        "White.":
            m "Yes, white is in a winning position."
        "Black.":
            m "Not really...{w=0.3}{nw}"
            extend " In fact, it's white winning now."
            m "Still, it's normal if you didn't see it."
            m "Because if white wants to win, white has only one chance, that's now."
    m "I mentioned at the beginning of this lesson that position can sometimes be more important than materials."
    m "White is having an disadvantage on materials in this match, but they have an excellent position."
    m "If White realizes this, the only way to win is to move the queen into c8 square."
    python:
        game.queue_move("c6c8")
        game.handle_player_move()
        renpy.pause(1)
    m "This move may seem crazy, but it's a good example of a sacrificial exchange."
    m "Let's see.{w=0.2}{nw}"
    python:
        game.queue_move("b8c8")
        game.handle_monika_move()
    extend " Black's only legal move at this point is to use the king to remove the queen, otherwise it cannot escape the check."
    m "Now, the reason for going out of this sacrificial exchange will be shown."
    python:
        game.queue_move("c4d6")
        game.handle_player_move()
        renpy.pause(1)
    if seen_event("monika_chesslesson_tactic_discovered_attack"):
        m "White used the {i}discoverd attack{/i} tactic that I told you about."
    else:
        m "White uses a tactic called {i}discovered attack{/i}."
        m "The basic idea of this tactic is to suddenly move your B piece in the attack path of your A piece to a different place so that the attack path of A piece is clear."
        m "If you're interested in it, I've got a whole lesson just for it."
        m "But for now, let's get back to this match."
    m "In this case, the white rook and the knight attacked the black's king at the same time."
    m "So, black cannot escape this check by removing the knight or blocking the rook's path with the bishop."
    m "The only legal move is to escape the king to b8 square."
    python:
        game.queue_move("c8b8")
        game.handle_monika_move()
        renpy.pause(1)
    m "By this point, the end was clear.{w=0.2} Move the rook to c8,{w=0.2}{nw}"
    python:
        game.queue_move("c3c8")
        game.handle_player_move()
        renpy.pause(1)
    extend " checkmate. Game end."
    if _mas_pm_player_chesslevel == chesslevel_beginner or _mas_pm_player_chesslevel == chesslevel_didntevenbegin:
        m "Just to make sure you understand why the king can't escape to a7,{w=0.2}{nw}"
        $ game.request_highlight_diagonal("a7","g1")
        extend " notice that there is a bishop on g1 square."
    m ""
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_epilogue",
            category=["chess lessons"],
            prompt="Epilogue",
            pool=True,
            conditional="mas_seenLabels(['monika_chesslesson_opening_basic_idea','monika_chesslesson_mate_bishops','monika_chesslesson_key_point_1','monika_chesslesson_key_point_2'],seen_all = True)",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_epilogue:
    $ count = mas_getEV("monika_chesslesson_epilogue").shown_count
    if count != 0:
        m "Not reconciled, so head for a rematch?"
        m "Ahaha, come on!"
        jump monika_chesslesson_finalexam
    m 1eka "Ah, this should be the epilogue of our lessons."
    m 1dkb "Time really flies, doesn't it? You've learned so much in the blink of an eye."
    m 1dka "..."
    m 1eua "To conclude, let me talk about the world of chess today."
    m 1eub "Since the end of the last century, the cutting edge of chess research has been not humans, but AIs."
    m 1euc "Today, the AI in chess is far more powerful than humans."
    m 1eud "For example, stockfish, the most powerful chess engine, has an ELO rating of over 3,700."
    m 1esd "And the current world champion, Magnus Carlsen, only has an ELO rating of around 2,880."
    m 1esc "That said, even the best of the human race would have no chance against the AI."
    m "And, thanks to the extremely powerful computing power of computers, the field of chess research in recent years has also been greatly improved."
    m 1esd "As a result, some people say chess has reached its end for mankind. There's not much left for humans to study."
    m 1dkc "..."
    m 2ekd "And you know what I think about it? I kind of feel the same way, actually."
    m 2esd "Six or seven hundred years ago, when the study of chess was still very immature, new ideas of opening and endgame theory appeared again and again."
    m "But by now, the opening theory was so well developed that it was hard to imagine anything new being proposed."
    m 2lsc "And the computational power of the human brain is numbered. Perhaps an ELO rating of around 2,900 is the limit..."
    m 2eksdla "Well, this may be a bit of a discouragement..."
    m 2esd "Because this fact runs counter to one of the human pursuits--{w=0.3}{i}Infinity{/i}."
    m 2dsc "But the cold truth is that infinity could never have existed...{w=0.3}"
    m 2dsd "Like, take the theory of entropy...{w=0.3}{nw}"
    extend 2hksdrb " Oh, wait, we're not here to talk about philosophy, are we?"
    m 2esd "Going back to chess, although human beings do have limits, we haven't really touched them yet, have we?"
    m 2esa "As I told you, my ELO rating is around 2200, which is far from the first in the world."
    m 2esb "Maybe the best of humanity can't get any better, but we can. For us, it's not over yet."
    m 2hua "Besides, even if we do eventually hit the limit, so what?"
    m 2tsu "Then we stand together on the top of the world, looking at the people who are still struggling, and together shout: {i}How boring{/i}~"
    m 2esbla "Our chess lessons may be over, but our story is far from over, [mas_get_player_nickname()]."
    m 2dsblu "..."
    m 2esbsu "..."
    m 2esb "Oh, right. Speaking of this, technically speaking, we're not really finished here. It's just the end of a phase."
    m 2hub "I might come up with a lot of complementary lessons in the future, like more variations on some openings, or some interesting creative moves."
    m 2eub "But that's for another story."
    m 2esa "At the end of this stage, you know what I want to say?"
    m 2dsa "..."
    m 2estpa "...Thank you."
    m 2eutpd "I've actually benefited a lot from my time teaching you, not just at chess, but also elsewhere."
    m 2hua "For the first time, I knew how wonderful it was to teach so many things."
    m 2ektua "As you can see, I've always been considered the perfect person. So rarely do I really talk to someone with such frankness and ease."
    m "...{w=0.3}{nw}"
    extend 2husdrb " Oh, I didn't mean to cry."
    m 2euu "It's just that...{w=0.3}{nw}"
    extend 2eku " thank you very much."
    m 2dku "..."
    m 2eua "..."
    m 2efb "Ahaha, but don't think I'm going to go easy on you at chess for this!"
    m 2tfb "After all, I'm really looking forward to seeing how far my dear student have learned..."
    m 2tfa "So..."
    jump monika_chesslesson_finalexam
    return

label monika_chesslesson_finalexam:
    $ mas_gainAffection(modifier=0.5)
    window hide None
    show monika at t21
    python:
        temp = store.persistent._mas_chess_difficulty# Create a backup to set them back later.
        store.persistent._mas_chess_difficulty = (11,10)# In the final exam, Monika used her full power.

        quick_menu = False
        game = MASChessDisplayable(
            is_player_white = random.choice([True,False]),# In real chess match, you can't choose your color, and so do here.
            pgn_game=None,
            practice_mode=False,
            starting_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            casual_rules=False# And since real chess match never use the casual rules, we don't enable it.
        )
        game._visible_buttons.remove(game._button_save)
        game._visible_buttons.remove(game._button_giveup)
        game._visible_buttons.remove(game._button_draw)
        game.show()
        results = game.game_loop()

        game.hide()
        quick_menu = True
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results
        game_result = new_pgn_game.headers["Result"]

        store.persistent._mas_chess_difficulty = temp# Set difficulty back.

    if is_monika_winner:
        if count == 0:
            m 1hub "Ahaha, looks like my student is still having a long way to go."
            m 1hua "..."
            m 1eub "I'm just kidding! That's my best recent game!"
            m 1rtd "Because in my eyes this is a kind of...{w=0.3}{nw}"
            extend 1ltsdrb "graduation exams or something? So I just played harder than I've ever played before."
            m 1husdrb "Don't feel too bad, ahaha!"
            m 1eub "Ask me again if you want to retake this exam!"
        else:
            m 1hub "I won again~"
            m 1tuu "Don't feel too bad, [player]~ After all, your girlfriend and teacher is just too talented~"
            m 1eub "If you want to retake, feel free to ask me!"
    elif game_result == "1/2-1/2":
        if count == 0:
            m 1eka "Ah, a stalemate."
            m 1eub "I was really trying in that game, you know?"
            m 1husdrb "I should even say I never played this hard before because this is kind of your graduation exam..."
            m 1hub "Way to go, [player]!"
            m 1eub "If you want to retake this exam, feel free to ask me!"
        else:
            m 1eka "Stalemate?"
            m 1eub "Well! On the bright side, it means you're going to beat me soon!"
            m "If you want to retake this exam, feel free to ask me!"
    else:
        m 1wud "Wow..."
        m 1wuo "You really did beat me..."
        m "..."
        m 1sub "Oh, my gosh, you're really good at chess!"
        m 1tuu "You're a professional chess player, right?"
        m "Hmm...{w=0.3}{nw}"
        extend 1rtu " maybe you're even a grandmaster?"
        m 1etu "Or maybe you just have a really good teacher...?"
        m 1hub "Ahaha! All kidding aside, you really are a wiz, [player]!"
        m 1hua "Congratulations, you graduated!"
        m 1eua "Well, then..."
        m 1kua "What else should we do today, {i}master{/i}?"
    return
