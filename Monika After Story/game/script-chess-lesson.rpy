#------To do: Add a new apologize reason for not listening the lesson carefully--------
#
#
#Like Python Tips or Writing Tips, no wonder this file will be a long one.
#So, in order not to increase the size of the topic file, 
#which already had more than 10,000 lines, I decided to open a separate one.
#
#This file contains 30 lessons of Chess:
#    1. What is Chess?(Done)
#    2. How to move a Pawn?(DONE)
#    3. How to move a Bishop?
#    4. How to move a Knight?
#    5. How to move a Rook?
#    6. How to move a Queen?
#    7. How to move a King?
#    8. When will we win a game?(DONE)
#    9. Key Points in Chess - 1 (What should you do in opening)(DONE)
#    10. Key Points in Chess - 2 (How to form a good position of pieces)
#    11. Popular Beginnings (Includes: Italian Game, Scilian Defense, etc. Gave them only a brief introduction.)(DONE)
#    12. Advanced Chess - Make the best of a Pawn
#    13. Advanced Chess - Make the best of a Bishop(DONE)
#    14. Advanced Chess - Make the best of a Knight
#    15. Advanced Chess - Make the best of a Rook
#    16. Advanced Chess - Make the best of a Queen
#        (There is no lesson about how to make the best of a King, because the controlling of a king is far advanced. Only master would learn it.)
#    17. Basic Tacs - Sacrificing-To-Win
#    18. Basic Tacs - Discovered Attacking
#    19. Basic Tacs - Break the defense
#    20. Basic Tacs - Avoid draw game
#    21. Popular Beginnings - Italian Game
#    22. Popular Beginnings - Scilian Defense
#    23. Popular Beginnings - Queen's Gamebit
#    24. Popular Beginnings - French Defense
#    25. Popular Beginnings - Dutch Defense
#    26. Key Checkmate - Two Rooks Mate
#    27. Key Checkmate - One Rook Mate
#    28. Key Checkmate - Queen Mate
#    29. Key Checkmate - Two Bishops Mate
#    30. Key Checkmate - King and Pawn Mate
#        (There is no Two Knights Mate because two knights can not checkmate.)
#
#
define chesslevel_didntevenbegin = 1
define chesslevel_beginner = 2
define chesslevel_advancer = 3
define chesslevel_master = 4
default persistent._mas_pm_player_chesslevel = None
default persistent._mas_pm_chessteaching_materials_explained = False

init 4 python:
    def highlight_diagonal_request(start_square_letter_ascii, start_square_number, end_square_letter_ascii, end_square_number,pause_time = None):

        range_start = min(start_square_number, end_square_number)
        range_end = max(start_square_number, end_square_number)+1
        letter_start_ascii = min(start_square_letter_ascii, end_square_letter_ascii)

        for i in range(range_start, range_end, 1):
            chess_teaching_disp.request_highlight("{0}{1}".format( chr(letter_start_ascii+i-range_start), 9-i))
            if not pause_time is None:
                renpy.pause(pause_time)
        return
    
    def highlight_diagonal_remove(start_square_letter_ascii, start_square_number, end_square_letter_ascii, end_square_number,pause_time = None):
        range_start = min(start_square_number, end_square_number)
        range_end = max(start_square_number, end_square_number)+1
        letter_start_ascii = min(start_square_letter_ascii, end_square_letter_ascii)

        for i in range(range_start, range_end, 1):
            chess_teaching_disp.remove_highlight("{0}{1}".format( chr(letter_start_ascii+i-range_start), 9-i))
            if not pause_time is None:
                renpy.pause(pause_time)
        return

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
    m 4hksdla "So I may need a few days to prepare your lessones...{w=0.1} Ehehe..."
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
                m "And this is actually logical...{w=1.0}{nw}"
                extend 1lusdla "Considering how many times you have beaten me..."
                m 1hksdla "Oh, gosh... It's even more oppressive now..."
                m 1efa "But don't worry! I'm still going to try my best!"
    
    m 1eua "Anyways, I will prepare your chess lessons soon."
    m 1hua "Be ready!"

    # Hide this event.
    $ mas_hideEVL("monika_chesslesson_init", "EVE", lock=True, depool=True)

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_1",
            category=["chess lessons"],
            prompt="What is Chess?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_1:#1. What is chess?
    m 1hua "Alright, [player]!"
    m "Let us start your chess lesson~"
    m 3duc "Now, let me get the board ready.{w=0.1}.{w=0.1}.{w=0.1}{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m 1eub "As you can see, this is the chess board."
    m "And, did you find that the pieces have two colors?"
    m "Two colors of pieces stand for two players, of course.{w=0.1} One of players would play white, and the other player would play black."
    m "Both players need to manipulate their pieces to their advantage and win."

    # Make the board disappear. Let Monika back.
    $ chess_teaching_disp.hide()
    show monika at t11

    m 1rusdrb "Hmm... Chess is such a game, if only from a cold logical point of view."
    m 3rusdrb "Sorry for having only so limited words, but that's really how we can define chess..."
    m 1hua "Thanks for listening anyway!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_8",
            category=["chess lessons"],
            prompt="How to win a game?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_8:#8. When will we win a game?
    m 3duc "Hold on, let me get the board ready.{w=0.1}.{w=0.1}.{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen="8/8/8/3k4/8/8/1R3K2/6R1 w - - 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

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
        chess_teaching_disp.queue_move("b2b4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("d5c5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("b4h4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("c5d5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("g1g5")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("d5e6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("h4h6")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("e6f7")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("h6a6")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("f7e7")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("g5g7")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("e7f8")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("g7b7")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("f8g8")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(0.5)
        chess_teaching_disp.queue_move("a6a8")
        chess_teaching_disp.handle_player_move()
        renpy.pause(0.5)

    m 2esb "Black is now {i}checkmated{/i}!"
    m 2eub "To understand why, let us see this.{w=0.1}.{w=0.1}.{w=0.1}{nw}"

    #Highlight the lines that rooks are attacking.
    python:
        for i in ['a','b','c','d','e','f','g','h']:
            chess_teaching_disp.request_highlight("{0}{1}".format(i, 1))
            renpy.pause(0.01)
        for i in ['a','b','c','d','e','f','g','h']:
            chess_teaching_disp.request_highlight("{0}{1}".format(i, 2))
            renpy.pause(0.01)
        
        renpy.pause(0.5)
    
    m "See? White's too rooks control two lines.{w=0.1} Black's king is now being attacked.{w=0.1}.{w=0.1}.{nw}"
    extend 2euu "And there is no way black can get out of this now!"
    m 2etu "Wherever black is going, black is still being attacked!"
    m "This is a {i}checkmate{/i}--{w=0.1}And now, we won the game."
    m 1eub "And this checkmate is the famous {i}\"Two Rooks Checkmate\"{/i},{w=0.2} I'm going to introduce it in other lessons."
    m "For now, I think it's enough for today."
    
    # Make the board disappear. Let Monika back to where she was.
    $ chess_teaching_disp.hide()
    show monika at t11

    m 1hua "Thanks for listening~"

    return 

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_2",
            category=["chess lessons"],
            prompt="How to move a pawn?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_2:#2.How to move a pawn?
    m 3duc "Alright, let us talk about pawns today.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

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
        chess_teaching_disp.request_highlight("{0}{1}".format('d', 6))
        renpy.pause(0.5)
        chess_teaching_disp.request_highlight("{0}{1}".format('d', 5))
        renpy.pause(2)
    
    m 2lub "These two highlighted squares is this pawn's movable range."
    m 2lua "Now, let us choose two move 2 squares.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('d', 5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('d', 6))
        chess_teaching_disp.queue_move("d2d4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)

    m 2lub "Okay, this pawn moved now!"
    m 2etc "But you are probably wondering, what's the point of this?"
    m "Since pawn is probably a protector, so are we simply moving this pawn to a position where can protect us better?"
    m 2esu "Not really!{w=1.0} Remeber what I said? {i}Pawns can fight too{/i}!"
    m 2lsu "Let me gave you an example.{w=0.1}.{w=0.1}.{w=0.3}{nw}"

    python:
        chess_teaching_disp.queue_move("e7e5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)

    m 2esb "Here we are! The opponent moved e7 pawn to e5, which is abandoning this pawn!"
    m 2lsu "To see why, let us see where can our pawn move now..."

    python:
        chess_teaching_disp.request_highlight("{0}{1}".format('e',4))
        chess_teaching_disp.request_highlight("{0}{1}".format('d',4))
        renpy.pause(2)

    m 2tsu "You are probably wondering, {i}how is this happening?{w=0.5} Isn't pawns only able to move directly in front of themselves?{/i}"
    m 2eub "This is the exception!{w=0.1} When a pawn's diagonal front is next to an opponent's piece, it can remove that piece and replace it!"
    m 2lua "So we can now take this e5 pawn like this:{w=0.5}{nw}"

    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('e',4))
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.queue_move("d4e5")
        chess_teaching_disp.handle_player_move()
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
        chess_teaching_disp.queue_move("f7f5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 3lsb "Because this pawn moved two squares, and that pawn is just at the hand of your pawn..."
    m "We can do the {i}En Passant{/i} now."
    
    python:
        chess_teaching_disp.queue_move("e5f6")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)

    m 2eua "See?{w=1.0} And now, let us cancel this movement,{w=1.0}{nw}"
    extend 2duc "take another movement...{w=1.0}{nw}"
    
    python:
        # Make the old one disappear, and get a new one to "cancel this movement".
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen="rnbqkbnr/pppp2pp/8/4Pp2/8/8/PPP1PPPP/RNBQKBNR w KQkq f6 0 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)

        chess_teaching_disp.queue_move("f2f4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(1)

        chess_teaching_disp.queue_move("g7g6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(1)
    
    m 2eub "We moved another pawn! And the opponent moved another pawn, too!"
    m 2eud "Even though it's our turn now, we can not take the c5 pawn by \"En Passant\" anymore!"
    m 2eub "This is the special rule of \"En Passant\", we must take that pawn immediately, otherwise we can not take that pawn anymore."
    m "We can only move forward now."
    m 3eub "And, there is still another special rule of pawns..."
    m 3hksdra "...Don't worry, this is the last special rule of pawns, I promise."
    m 3lksdra "To see this special rule, let us keep moving forward...{w=1.0}{nw}"

    python:#Keep moving forward till the pawn reached the last line
        chess_teaching_disp.queue_move("e5e6")
        chess_teaching_disp.handle_player_move()
        renpy.pause(1)

        chess_teaching_disp.queue_move("g6g5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(1)

        chess_teaching_disp.queue_move("e6e7")
        chess_teaching_disp.handle_player_move()
        renpy.pause(1)

        chess_teaching_disp.queue_move("g5g4")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)

    m 2eua "Okay, let us pause here..."
    m 2wud "The pawn is going to reach the last line!{w=0.3} Is this pawn going to be useless then?"
    m 2euu "Actually, no.{w=1.0} In fact, this pawn is about to play to its full value:"

    python:
        chess_teaching_disp.queue_move("e7f8q")
        chess_teaching_disp.handle_player_move()
    
    m 2etu "..."
    m "I know what you are thinking about:{w=1.0}{nw}"
    extend 2ltd "{i}What is this now? Did my eyes cheat on me?{/i}"
    m 2esb "Relax, [mas_get_player_nickname()]~ This is the last special rule: {i}Promotion{/i}."
    m "When a pawn reaches the last line, it can be promoted into any piece except pawn and king."
    #TODO: say "You know, queen is the most powerful piece" after player have seen the lesson of queen.
    m 3esb "Since queen is the most powerful piece, we usually make our pawns queens."
    m 3rsd "Well, I don't have a very good realistic interpretation of this rule...{w=1.0}{nw}"
    extend 3esb "But this rule is easy to remember, right?"

    # Make the board disappear. Let Monika back to where she was.
    $ chess_teaching_disp.hide()
    show monika at t11

    m 1hua "Thanks for listening~"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_keypoint_1",
            category=["chess lessons"],
            prompt="Key Points 1",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_keypoint_1:#Key Point 1 - The basic principle of opening
    m 3eub "Okay, today we are going to talk about some key points in chess!"
    m "And this one would be...\"The Key Point of Opening\"!"
    m 1eua "Hold on, let me get the board ready...{w=1.0}{nw}"

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m 2eub "Okay, so we are at the position where every game starts now!"
    m "Even if you don't understand the openings, you can see that people always start a chess game by moving a pawn."
    m 2ruc "...Well, not exactly.{w=1.0}{nw}"
    extend 2rud "There is a special opening called {i}Alkehine's Defense{/i}, which moves a knight as an opening."
    m 2eub "But one thing can be sure: {i}Almost{/i} every game started by moving a pawn."
    m "Why? Is this a rule of chess? Of course not!"
    m "For understanding this, let us consider: What can we do if we don't move a pawn?"
    m "Firstly, there is no way our bishops, rooks, queen or king can move! Neither of them can directly reach the other side of the other piece!"
    m 2eua "So, we can only move knights then...{w=1.0}{nw}"

    python:
        chess_teaching_disp.queue_move("g1f3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2.0)

    m 2etd "Is this {i}Alkehine's Defense{/i}?{w=0.5}{nw}"
    extend 2etb "No! Notice the full name: \"Alkehine's {i}Defense{/i}\"!"
    m 2lua "To see why we must move knight as a defense, not a beginning,{w=0.5} see this:{w=1.0}{nw}"

    python:
        chess_teaching_disp.queue_move("d7d5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2.0)
    
    m 2ltd "The question now appears: Did our knight directly attack this pawn at all?"
    m 2ltc "No! Yes, if this pawn keep moving foward, then it's in our knight's movable range."
    m 2etd "But why should the opponent do it? Opponent is not a fool!"
    m 2eub "Black now has already open a gap, which means the light-squared bishop can move now!"
    m 2ekb "And, not only that, but also the black can move knights too..."
    m 2eub "...But actually, white is not really in a disadvantage now."
    m 2lub "You see, though white didn't directly create threaten to this pawn,{w=0.5} but this f3 knight still threat these two squares:{w=1.0}{nw}"
    
    python:
        chess_teaching_disp.request_highlight("{0}{1}".format('d',5))
        chess_teaching_disp.request_highlight("{0}{1}".format('e',4))
        renpy.pause(2.0)

    m 3lub "So if it's black's turn now, black can not move the e7 pawn to e5, or move the d4 pawn to d5, those pawns are at a risk of being attacked."
    m 3hub "Even though white didn't create directly threaten, white created potential threaten."
    m 2euc "But,what if we are still unwilling to move our pawns?"
    m 2lud "Let us see if we move another knight here...{w=1.0}{nw}"

    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('e',4))
        chess_teaching_disp.queue_move("b1c3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2.0)
    
    m 2luc "This is not a good move. Why? Let us see this..."

    python:
        chess_teaching_disp.queue_move("c7c5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2.0)
    
    m 2eud "Black can move another pawn, and now, white's space is really limited."
    m 2luc "Let us see how many squares black's pawns are controlling now..."

    python:
        chess_teaching_disp.request_highlight("{0}{1}".format('b',5))
        chess_teaching_disp.request_highlight("{0}{1}".format('c',5))
        chess_teaching_disp.request_highlight("{0}{1}".format('d',5))
        chess_teaching_disp.request_highlight("{0}{1}".format('e',5))

    m 2wud "4 squares, that's 4 squares, and they are central squares!"
    m 2wuo "Even though white want to move d2 pawn to d4, it's not that safe anymore!"
    m "Black is directly attacking the d4 square!"
    m 2rksdrc "What's worse, black can still move knights or bishops, or even queen..."
    m 2rsd "Though, white moved our knights, and knights is controlling some squares too..."
    m 2esb "So white is still having a chance to win. White is only in a tiny disadvantage now."
    m 2etc "But why should we have a tiny disadvantage from the beginning? That's of course not good."
    m "So the conclusion is...{w=0.5}{nw}"
    extend 2rtc "We can not say that move a knight as the beginning is bad, but it's not the best."
    m 2eub "Now, hearing this, I think you can also understand a basic principle of chess opening:"
    m 3esb "{i}Control as many central squares as you can, and develop your materials to a good position.{/i}"
    if persistent._mas_pm_chessteaching_materials_explained is False:
        $persistent._mas_pm_chessteaching_materials_explained = True
        m 3rsc "Oh, talking about {i}materials{/i} the word, it stands for \"Knights, Bishops, Rooks and Queen\"."
        m 3esd "They are all \"flexible\" pieces, you could say."
    m 2etc "Since a knight can probably control only 2 central squares, and a pawn can do the same effect too..."
    m 2etd "People would probably move the pawn, instead of moving knights."
    m 2esd "And then, we develop our knights to protect our pawn, or attack opponent's pawn."
    m 2esa "As for the rest, then it's really various. You may develop a bishop, or push another pawn, or something else...{w=0.3}{nw}"
    extend 2esb "It's infinite!"
    m 2duc "Now, let us back to the start...{w=1.0}{nw}"

    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('b',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('c',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('e',5))

        # Make the old one disappear, and get a new one to "back to the start".
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)
    
    m 2lub "This time, let us move a pawn."
    m "Since the principle is to control as many as central squares, we should focus on the d2 pawn and the e2 pawn."
    m 2lua "Both they are {i}central pawns{/i}, and both they are powerful pieces for us to compete at the center."
    m 2lud "But there is actually a difference between these two central pawns..."
    m 2eud "The e-file pawn has no queen to protect it. But the d-file has. If opponent attacks the d-file pawn, the queen could be a part of defense of it."
    m 2eub "In this example, let us move e2 pawn to e4...{w=1.0}{nw}"

    python:
        chess_teaching_disp.queue_move("e2e4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)

        chess_teaching_disp.request_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.request_highlight("{0}{1}".format('f',4))
    
    m 7eua "Alright! Since we are controlling the f5 square, there is no way opponent can move f7 pawn to f5 now!"
    m 2lud "As for d7 to d5...{w=0.5}{nw}"
    extend 2eud "This is actually possible."
    m "Remember? The d-file has a queen as its defense, if black now move d7 to d5, and we play exd5..."
    m "Black will play Qxd5 to recapture this pawn. So, black didn't lose a pawn in this opening."
    m 2eub "This is the famous {i}\"Scandinavian Defense\"{/i}, we will introduce this opening in future."
    m 2lua "As for now, let us set to another possblity...{w=1.0}{nw}"

    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.remove_highlight("{0}{1}".format('f',4))
        chess_teaching_disp.queue_move("e7e5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 2lub "Two pawns are facing to each other! Because the pawns can only tilt forward to attack, both two pawns are stuck!"
    m 2eub "So black is now controlling two central squares now. Just like white."
    m "For white, there is no way we can let black get this position so easily...{w=0.5}{nw}"
    extend 2lua "White will probably play:{w=1.0}{nw}"
    
    python:
        chess_teaching_disp.queue_move("g1f3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    
    m 2eub "This move is a good book move. The knight is brought into fight, having a good position, which activated this knight."
    m 2hub "At the same time, this knight attacks e5 square, add pressure on that pawn."
    m 2lua "Black, of course, would protect this pawn.{w=0.2} One of the popular choice is pushing the knight.{w=1.0}{nw}"

    python:
        chess_teaching_disp.queue_move("b8c6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 3lub "Black also activated black's knight, and defense the e5 pawn."
    m 3wsb "The following possbilities are infinite... White can activate another knight, or activate the light-squared bishop, or move another pawn, or..."
    m 1hsa "So you have understood what's the principle of opening now."
    m 1eub "Remember: {i}Control as many as central squares as you can, and activate your materials{/i}. That's the principle of opening."

     # Make the board disappear. Let Monika back to where she was.
    $ chess_teaching_disp.hide()
    show monika at t11

    m 1eua "That's enough for now."
    m 1hua "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_popular_openings",
            category=["chess lessons"],
            prompt="Popular Openings",
            pool=True,
            conditional="mas_seenLabels(['monika_chesslesson_keypoint_1'])",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_popular_openings:
    m 2eub "Okay, today we are going to talk about popular openings!"
    m 2luc "Let me get the board here..."

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m 2lub "Okay, so we are looking at the beginning of every game now!"
    m 2eub "Since I have taught you the basic principle of opening{w=0.5}{nw}"
    extend 2euc "--Oh, wait, do you still remember the principle I told you?{nw}"
    $ principle_remember = True
    $ materials_remember = True
    $ _history_list.pop()

    menu:
        m "Since I have taught you the basic principle of opening{w=0.5}--Oh, wait, do you still remember the principle I told you?{fast}"
        "Yes.":
            $ mas_gainAffection()
            m 2hub "That's great!"

        "...Sorry, I forgot.":
            $ principle_remember = False
            m 2eka "Aww, that's okay, [player]."
            m 2eub "Remember, the principle of opening is:{w=0.2}{i}Control as many as central squares as you can, and activate your materials{/i}."
            m 2rusdlb "And... just for sure. Do you still remember what the word \"materials\" stands for?{nw}"
            $ _history_list.pop()

            menu:
                m "And... just for sure. Do you still remember what the word \"materials\" stands for?{fast}"
                "Yes.":
                    m 2hub "Oh, that's good. Now let us back to our board..."
                "...Sorry again.":
                    $ materials_remember = False
                    $ mas_loseAffection(0.1) # Lose a bit of affection.
                    m 2rksdlb "..."
                    m 2rksdla "Well, it's okay! We all started somewhere."
                    m 2eusdlb "Materials stands for \"flexible pieces\"."
                    m 2eub "That include: Knights, Bishops, Rooks and Queen."
                    m "Anyways, let us back to our board..."
    
    m 4lub "Due to the principle of opening,{w=0.5} white would play e4 to control both the d5 and f5 squares:{w=1.0}{nw}"

    python:
        chess_teaching_disp.queue_move("e2e4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(1)
        chess_teaching_disp.request_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.request_highlight("{0}{1}".format('f',4))
        renpy.pause(1)
    
    m 1lub "Like what I said before... Black can response with d5:{w=1.0}{nw}"
    
    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.remove_highlight("{0}{1}".format('f',4))
        chess_teaching_disp.queue_move("d7d5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 1esu "But, still, like what I said before, black is not losing a pawn."
    m 1esb "Yes, white can capture this d5 pawn with exd5:{w=1.0}{nw}"

    python:
        chess_teaching_disp.queue_move("e4d5")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    
    m 3lub "But soon, black can recapture this pawn back with Qxd5:{w=1.0}{nw}"
    
    python:
        chess_teaching_disp.queue_move("d8d5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)

    m 2eub "This is known as \"{i}Scandinavian Defense{/i}\".{w=0.5} One of the popular responses to e4."
    m 2eua "And now, let us go to another popular response to e4: \"{i}Sicilian Defense{/i}\"."
    m 2duc "Firstly, let us cancel these movements...{w=1.0}{nw}"

    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)

    m 2eud "Alright. Since the principle of opening is not \"Attack your opponent's pawn\", why must black against white Immediately?"
    m 2lub "Black may play c5, which controls both the b4 and d4 squares."
    m "Let us see:{w=0.2}{nw}"

    python:
        chess_teaching_disp.queue_move("c7c5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(1)
        chess_teaching_disp.request_highlight("{0}{1}".format('b',5))
        chess_teaching_disp.request_highlight("{0}{1}".format('d',5))
        renpy.pause(1)
    
    m 2eub "See? Black also controls two central squares, there is nothing wrong with this!"
    m 2eub "Now, let us see another popular response to e4."
    m 2duc "Again, firstly, back to the e4 movement...{w=0.5}{nw}"

    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('b',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',5))

        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)

    m 2eub "Still, following the principle \"Control as many as squares you can\", black may also play e5 to make both two players's pawn stuck."

    python:
        chess_teaching_disp.queue_move("e7e5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 2esb "This is the beginning of many famous openings... Like \"{i}Italian Game{/i}\", \"{i}Vienna Game{/i}\", \"{i}Center Game{/i}\"..."
    m 2rssdlb "Since it would be too verbose to go into detail about these openings, I am going to introduce them in other lessons...{w=1.0}{nw}"
    extend 2eub "For now, let's just remember this e5 response to e4."
    m 4eub "These e4 beginnings are also all named as \"King's Pawn Opening\" for they moved the pawn in front of king."
    m 2etc "Now, what if white play d4 as the opening, not e4?"
    m 2duc "Let us set that position on board...{w=1.0}{nw}"

    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)
    
    extend 2lub " Okay, since this is also a beginning with central pawn, we may consider this situation with the experience of King's Pawn Opening."
    m 2lua "Let us consider to play f5, which is similar to \"{i}Sicilian Defense{/i}\" in a way."

    python:
        chess_teaching_disp.queue_move("f7f5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 2eub "This is known as \"{i}Dutch Defense{/i}\", which seems like a reverse version of the \"{i}Sicilian Defense{/i}\"."
    m 2euc "But there is actually a huge difference between these two defenses... We will introduce them in other lessons."
    m 2duc "Now, back to d4...{w=1.0}{nw}"

    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)

    extend 2esb "What can black do except the Dutch Defense?{nw}"
    $ _history_list.pop()
    call monika_chesslesson_popular_openings_question(c5_chose = False, d5_chose = False, e5_chose = False, nc6_chose = False, nf6_chose = False)
    
    # Make the board disappear. Let Monika back to where she was.
    $ chess_teaching_disp.hide()
    show monika at t11

    m 1eud "Anyways, though there are many choices of opening, and we are far from introducing all of them now..."
    m 1eub "But one thing can be sure:{w=0.1} {i}most of openings are started by moving a pawn, and most of the time, this pawn would be central pawn.{/i}"
    m 1hub "I hope this lesson taught you how to response those central pawns's movement for a little."
    m 3hub "This lesson could actually be described as another lesson of \"What should you do in opening\"."
    m 1eua "I also hope this lesson gave you a better understanding of the basic principle of opening."
    if principle_remember is False:
        m 1rud "...Wait a second, you do know the principle of opening now, right?{nw}"
        $ _history_list.pop()
        menu:
            m "...Wait a second, you do know the principle of opening now, right?{fast}"
            "Yes.":
                m 1hua "That's great! Then, keep that principle in mind, [mas_get_player_nickname()]!"
            "...Actually no.":
                # Did you just listen all the time?
                m 1rusdlc "..."
                m 1rusdlb "Then you must be a forgettable guy, ahaha..."
                m 1ekb "It's okay, I won't blame you...{w=0.5}{nw}"
                extend 3eub "The basic principle of opening is:{i}Control as many as central squares as you can, and activate your materials{/i}."
                if materials_remember is False:
                    m 1hua "Alright, I think this is enough--{w=0.2}{nw}"
                    extend 3rud "Oh, wait a second again... Do you still remember the word \"Materials\"?{nw}"
                    $ _history_list.pop()
                    menu:
                        m "Alright, I think this is enough--Oh, wait a second again... Do you still remember the word \"Materials\"?{fast}"
                        "Yes.":
                            m 1hua "Oh, that's nice!"
                            m "Now..."
                        "My bad.":
                            $ mas_loseAffection(modifier=0.5)
                            m 2hksdlb ".{w=0.2}.{w=0.2}.{w=0.2}.{w=0.2}.{w=0.2}."
                            m 2lksdlb "...{w=0.5}{nw}"
                            # Monika tried her best to make the situation not awkward.
                            extend 2esb "I am so glad that you are able to admit you forgot a point!"
                            m 2hub "Many students don't know this nowadays... You are a student who is good at asking questions, which is very encouraging!"
                            m 3ekb "But please keep this point in mind too: Materials stand for \"flexible pieces\", which include Rooks, Knights, Bishops and Queen."
    m 1eua "I think these words are enough for a brief introduction of openings."
    m 1hua "Thanks for listening!"
    return

label monika_chesslesson_popular_openings_question(c5_chose, d5_chose, e5_chose, nc6_chose, nf6_chose):
    while (c5_chose is False) or (d5_chose is False) or (e5_chose is False) or (nc6_chose is False) or (nf6_chose is False):
        m "Let us back to d4...What can black do except Dutch Defense?{fast}"
        menu:
            "c5.":
                call monika_chesslesson_popular_openings_answer_c5(c5_chose)
                $ c5_chose = True
            "d5.":
                call monika_chesslesson_popular_openings_answer_d5(d5_chose)
                $ d5_chose = True
            "e5.":
                call monika_chesslesson_popular_openings_answer_e5(e5_chose)
                $ e5_chose = True
            "Nc6":
                call monika_chesslesson_popular_openings_answer_nc6(nc6_chose)
                $ nc6_chose = True
            "Nf6":
                call monika_chesslesson_popular_openings_answer_nf6(nf6_chose)
                $ nf6_chose = True
            "I think there is no good movement now.":
                if d5_chose is True and nf6_chose is True:# You did find every good move.
                    if (c5_chose is False and e5_chose is False and nc6_chose is False):
                        # You didn't pick any bad move:
                        m 2ssb "Wow, you are right! There is no good movement now!"
                        m 3ssb "These moves: c5, e5 or nc6... None of them is a good move!"
                        if(persistent._mas_pm_player_chesslevel is chesslevel_master):
                            m 3hsu "So you really are a master on chess, huh?"
                            m 3hssdlb "...Man, I hope my lessons didn't sound too stupid to you."
                        m 2eub "Since you didn't pick anyone of them, I think you know why they are bad then."
                        m "So I am not going to analyse them."
                        return
                    else:
                        # You picked one or more bad move:
                        m 1ruc "Well, though you chose a few bad move, it's okay."
                        m 1eub "We all started somewhere, right?"
                        return
                else:
                    m 1tuu "Hmm~{w=0.2} Really? I don't think so..."
                    m 1tub "Try to find the good movement!"
                    m 1tsb "My Sweet Tip: They are possbily more than one~"
                    m 1esb "So..."
                    # After this "So...", since this is a while loop, Monika will ask question again, which is back to line 866.
    
    #You have tried every choice, so we break the while and get here:
    m 2rssdrb "Oh, wait a second... I don't actually think there is another good option anymore."
    m "Because you have chose every of them now."
    return

label monika_chesslesson_popular_openings_answer_c5(c5_chose):
        if c5_chose is True:
            call monika_chesslesson_answer_repeated
            return
        
        m 1esc "Oh, c5?"
        m 1rssdlu "This is not good at all..."
        if (persistent._mas_pm_player_chesslevel is chesslevel_advancer) or (persistent._mas_pm_player_chesslevel is chesslevel_master):
            m 1esd "Considering you are not bad at chess, this is usually not your really answer..."
            m 3esb "Pick another one!"
            return#End this immediately, because player is an advancer or master, it's not so possible that player can not figure out why is this bad.

        m 2euc "To see why this is not good, let us play c5 the move...{w=1.0}{nw}"

        python:
            chess_teaching_disp.queue_move("c7c5")
            chess_teaching_disp.handle_monika_move()
            renpy.pause(2)

        m 2eub "See? This c5 pawn is under attack of white's d4 pawn!"
        m 2wud "And after white capture this pawn, black has no way to recapture it back!"
        m "And if you think that's the only thing white can do, then you're wrong..."
        m 2lud "White can play d5, push the pawn forward to one more square!"
        m 2luc "And if white did so, then the situation would be like this:{w=1.0}{nw}"

        python:
            chess_teaching_disp.queue_move("d4d5")
            chess_teaching_disp.handle_player_move()
            renpy.pause(1)
            chess_teaching_disp.request_highlight("{0}{1}".format('c',3))
            chess_teaching_disp.request_highlight("{0}{1}".format('e',3))
            renpy.pause(1)
        
        m 2eud "White now limits black so hard..."
        m "Black can not play Nc6 now, otherwise the knight will be removed immediately!"
        m 2luc "Also, the ability of black to fight center is serverly damage..."
        m 2lud "Because d5 is also impossible for black now, which means black has no way to push a d-file pawn to center."
        m 2eud "And white can then play e4, which push another central pawn to gather even more space and protect the d5 pawn..."
        m 2euc "Needless to say, black is in a disadvantage now. Though, this is only a beginning, so it's not that vital to lose the game."
        m 2eud "If Black's skill is better than White, Black can still win...{w=0.2}{nw}"
        extend 2etd "But why should black make themselves in a disadvantage?"
        m 2eub "Let us cancel these movement, and, try another one, [player]!"

        python:
            chess_teaching_disp.hide()
            chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
            chess_teaching_disp.toggle_sensitivity()
            chess_teaching_disp.show()
            renpy.pause(1)
        return

label monika_chesslesson_popular_openings_answer_d5(d5_chose):
    if d5_chose is True:
        call monika_chesslesson_answer_repeated
        return
    
    m 2eub "d5? Oh, this is not bad! Let us see...{w=0.5}{nw}"

    python:
        chess_teaching_disp.queue_move("d7d5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)

    m 4lub "Just like the e5 response to e4, this d5 response to d4 make both two pawns stuck!"
    m 4eub "As for the following movements, they are various too... Include \"{i}Queen's Gambit{/i}\", \"{i}Levitsky Attack{/i}\"..."
    m 2eua "Now, let us back to see if there is other options..."

    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(1)
    return 

label monika_chesslesson_popular_openings_answer_e5(e5_chose):
    if e5_chose is True:
        call monika_chesslesson_answer_repeated
        return
    m 2eud "e5? Oh, I can probably guess why you're taking this move..."
    python:
        chess_teaching_disp.queue_move("e7e5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m "Dutch Defense is simliar to Scilian Defense, after all..."
    m 2euc "And this one is simliar to Scandinavian Defense, right?"
    m 2hub "Well, I'm so glad that you think by analogy...{w=1.0}{nw}"
    extend 2hksdrb "But this one is not that same with Scandinavian Defense..."
    m 2eud "The key point of Scandinavian Defense was that the defenders didn't actually lose a pawn."
    m 2rud "After attacker capture that pawn, defender can always recapture attacker's pawn..."
    m 2ruc "But that's because attacker captured a d-file pawn, which has a queen as a defender..."
    m 2etc "This e5 pawn is on e-file,which has no queen to defense it..."
    m 1ltc "So the attacker can capture that pawn without being recaptured:{w=2.0}{nw}"

    python:
        chess_teaching_disp.queue_move("d4e5")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    
    m 1esd "See? There is no way we can recapture this pawn now..."
    m 1etd "We may get this chance in future, but it's at least not for now..."
    m 1rsd "Not to mention this chance is actually depending on the opponent..."
    m 1ekd "So, sorry, but this is not a good move."
    m 2luc "Alright, let us set the board back, and pick another one...{w=1.0}{nw}"
    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(1)
    return

label monika_chesslesson_popular_openings_answer_nc6(chose_nc6):
    if nc6_chose is True:
        call monika_chesslesson_answer_repeated
        return
    
    m 2eub "You'd like to play Nc6? Oh, let us do this and see if it's a good move..."
    python:
        chess_teaching_disp.queue_move("b8c6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m 2lua "This knight controls 3 squares: b4, {nw}"
    $ chess_teaching_disp.request_highlight("{0}{1}".format('b',5))
    extend "{w=0.2}d4, {nw}"
    $ chess_teaching_disp.request_highlight("{0}{1}".format('d',5))
    extend "{w=0.2}e5. {nw}"
    $ chess_teaching_disp.request_highlight("{0}{1}".format('e',4))

    extend 2euc "So is this a good move then?"

    m 2eud "Not really...{w=0.5} The attack on d4 could be ignored to white for now. Because if the knight capture d4 pawn, then the queen of white is going to capture this knight."
    m 2euc "A pawn only value 1, and a knight value 3. It's not an ideal exchange."
    m 2rud "So this knight didn't really add pressure to white's central pawn now. White does not need to spend time defending that pawn and can move on to others to control more squares."
    m 2lub "An ideal move for white would be e4.{w=1.0}{nw}"
    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('b',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('e',4))
        chess_teaching_disp.queue_move("e2e4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m 2eua "Now, how many squares white are controlling?"
    m 2luc "Let us see...{w=0.5}{nw}"
    python:
        chess_teaching_disp.request_highlight("{0}{1}".format('c',4))
        chess_teaching_disp.request_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.request_highlight("{0}{1}".format('e',4))
        chess_teaching_disp.request_highlight("{0}{1}".format('f',4))
    extend 2wsd "Four central squares! There is no way black can accept this!"
    m 2esd "If black has a good move to regain the center back, then black is still okay."
    m 2esc "But the problem is...{w=0.5} There is no a promising way to regain this center."
    m 1rsd "Needless to say, black is now in a disadvantage."
    m 1eud "Black can win the game, still. It's not a fatal mistake."
    m 1etd "But if black could avoid this from the beginning, then why not?"
    m 1eua "This is why it's not ideal for black to play Nc6."
    m 2lub "Now, let us back to start, to see if there is another good move..."
    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(1)
    return

label monika_chesslesson_popular_openings_answer_nf6(nf6_chose):
    if nf6_chose is True:
        call monika_chesslesson_answer_repeated
        return

    m 2euc "Nf6?{w=0.2}{nw}"
    extend 2eub "Alright, let us move that knight to see whether this is a good move or not."
    python:
        chess_teaching_disp.queue_move("g8f6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(1)
    
    m 2lua "This knight controls 3 squares:{w=0.1} d5, {nw}"
    $ chess_teaching_disp.request_highlight("{0}{1}".format('d',4))
    extend "{w=0.2}e4, {nw}"
    $ chess_teaching_disp.request_highlight("{0}{1}".format('e',5))
    extend "{w=0.2}g4. {nw}"
    $ chess_teaching_disp.request_highlight("{0}{1}".format('g',5))
    extend 2esb "This would be an ideal move!"

    m "Because, this knight is forbidding white from play d4, and add an attack chance on d5!"
    m 2eub "Actually, it's not only a chance of attack, but also a defense of d5!"
    m 4eub "Let us consider that if black play d5 next turn, isn't black's d5 pawn under double defense?"
    m 2eub "This double defense is made by both the queen and knight."
    m 2eua "If this pawn was captured, then we may use our knight to recapture that captor first."
    m 2eub "And then, if the opponent recapture our knight, then we can use our queen to recapture the recaptor..."
    m 2husdrb "...Ehehe...{w=0.5} Is this clear to you?{nw}"

    $ _history_list.pop()
    menu:
        m "...Ehehe...{w=0.5} Is this clear to you?{fast}"
        "Yes.":
            m 2hua "Great! I was worrying about I am saying something complicated..."
        
        "I am confused.":
            m 2husdrb "...Well, you see. Let us imagine that there is a d5 pawn."
            m 2eub "Firstly, if the opponent uses... Piece A, let us call this piece this name."
            m "If the opponent uses Piece A to capture our d5 pawn, then..."
            m "Our knight is protecting this square, so our knight can take this Piece A down..."
            m "And then, if the opponent uses another piece{nw}"
            extend 2rub "- Let us say Piece B - capture our knight..."
            m 2eub "Then our queen is also protecting that square, so our queen will remove the Piece B from the board."
            m 2hksdlb "...Is this clear to you now?{nw}"
            $ _history_list.pop()
            menu:
                m "...Is this clear to you now?{fast}"
                "Yes.":
                    m 2hub "Yay! I'm so happy that I helped you have a better understanding!"
                    m 2eua "Now, let us back to the current board."

                "I'm even more confused.":
                    m 2hksdrb ".{w=0.1}.{w=0.1}."
                    m 2rksdrb "...{w=0.5}..."
                    m 2eksdrb "Well, I don't know how to describe it better... Sorry, [mas_get_player_nickname()]..."
                    m 2lksdrb "...Maybe you can try to play another round of chess with me later to understand this?"
                    m 3lksdrb "As for now, let us back to the current board..."
    
    m 2eub "The conclusion is, Nf6 is a good move. This move activate the knight, and add pressure to the center..."
    m 2eua "Now, let us recover the board, to see if there is a better option..."
    python:
        chess_teaching_disp.remove_highlight("{0}{1}".format('d',4))
        chess_teaching_disp.remove_highlight("{0}{1}".format('e',5))
        chess_teaching_disp.remove_highlight("{0}{1}".format('g',5))
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(1)
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_italian_game",
            category=["chess lessons"],
            prompt="Italian Game",
            pool=True,
            conditional="seen_event('monika_chesslesson_popular_openings')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_italian_game:#UNFINISHED
    m "Today we are going to talk about \"{i}Italian Game{/i}\", which is one of the most popular beginnings nowadays."
    m "Hold on, I am going to get the board here..."

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

    #Give player a few seconds to look at the board
    pause 2.0

    m "Italian Game is a King Pawn's Opening, which means white should move the e2 pawn first."
    m "Now, let us play this move.{w=1.0}{nw}"
    python:
        chess_teaching_disp.queue_move("e2e4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m "Then, black plays e5 to control two central squares too.{w=1.0}{nw}"
    python:
        chess_teaching_disp.queue_move("e7e5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    m "White then plays Nf3, develop knight to a good position, and attacks the e5 pawn at the same time."
    python:
        chess_teaching_disp.queue_move("g1f3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m "There is no way black can give up this pawn, so black would play Nc6 to protect this pawn and devlop the knight at the same time too."
    python:
        chess_teaching_disp.queue_move("b8c6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    m "And then, it's white's turn. White will play Bc4 to activate the light-squared bishop."
    python:
        chess_teaching_disp.queue_move("f1c4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m "This is the famous \"Italian Game\". Let us analyze this current situation to figure out why would both players play this opening."
    m "Firstly, notice this c4 bishop. Let us highlight squares that are controlled by this bishop."
    python:
        i = 1
        while i<=8:
            i+=1
            chess_teaching_disp.request_highlight("{0}{1}".format(chr(ord('a')+i-2),9-i))
            renpy.pause(0.1)
    m "This bishop is enjoying a2-h8 the strong diagonal!"
    m "To see why is this a strong diagonal, let us consider what if black play d5 now."
    python:
        chess_teaching_disp.queue_move("d7d5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m "This black's d5 pawn has only one protector, the queen."
    m "But white has to attacker on d5, the e4 pawn and the c4 bishop."
    m "White could play exd5."
    python:
        chess_teaching_disp.queue_move("e4d5")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m "Black must not recapture this pawn, at least now."
    m "The reason is not hard to see: The only way black to recapture this pawn now is Qxd5, which is actually abandoning the queen."
    m "And even if black not capture this pawn, black is in a disadvantage. Black has lost the ability to control the center."
    m "Due to white's controlling of the center, White soon mobilizes pieces power and unleashes a fierce storm of attacks on Black."
    m "Now, let us back to Italian Game."
    python:
        i = 1
        while i<=8:
            i+=1
            chess_teaching_disp.remove_highlight("{0}{1}".format(chr(ord('a')+i-2),9-i))
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(2)
    
    m "Italian Game, of course, just like other openings, both two players are not in obvious advantage or disadvantage."
    m "Though white got a powerful diagonal, black can also got this diagonal too."
    m "Black would play Bc5 to get the same powerful diagonal."
    python:
        chess_teaching_disp.queue_move("f8c5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    m "This is the \"{i}Giuoco Piano Game{/i}\" now, one of the varieties of Italian Game."
    m "White would play c3, which might be confusing at the first glance to beginners."
    python:
        chess_teaching_disp.queue_move("c2c3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m "But if you take further considerations, then you will soon understand,{w=0.5} this is a preparation of d4."
    m "You see, after this c3 move, white has 3 attack chance on d4."
    m "They are: c3 pawn"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_sicilian_defense",
            category=["chess lessons"],
            prompt="Sicilian Defense",
            pool=True,
            conditional="seen_event('monika_chesslesson_popular_openings')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_sicilian_defense:#UNFINISHED
    m "Hold on a second...{w=1.0}{nw}"
    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True, starting_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

    #Give player a few second to look at the board.
    pause 2.0

    $ word = "This"
    m "Sicilian Defense, also, is a King's Pawn Opening."
    if seen_event("monika_chesslesson_italian_game"):
        m "But Sicilian Defense is not like Italian Game or others, which is a balance opening."
        $ word = "Instead, this"
    m "[word] opening is a imbalance opening, which responses the e4 with c5:"

    python:
        chess_teaching_disp.queue_move("c7c5")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
    
    m "This game now turns into Sicilian Defense."
    m "Due to the imbalance, usually, it won't be long for the Sicilian Defense to enter middle game."
    m "This opening is the most complicated in chess... Not even a few grandmasters can claim to have mastered it."
    m "Let us take a view of this board.{nw}{w=0.2}"
    extend " In this current situation, black does not immediately collide with white. Instead, black played c5 to control another two central squares."
    m "To develop materials, and control more central squares, one of the best choice of white is Nf3."

    python:
        chess_teaching_disp.queue_move("g1f3")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    
    m "This is known as {i}Open Sicilian{/i}. Of course, there is another variation called Closed Sicilian, let us talk about this later."
    m "Back to Open Sicilian, things are getting various now."
    m "Black's choices include d6, e6, g6, Nc6...{w=0.5}{nw}"
    extend " Since it's too much to talk, and I'm afraid I'm not qualified to talk about all the possibilities, let us talk about Nc6, the most popular choice."
    
    python:
        chess_teaching_disp.queue_move("b8c6")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)

    m "Now, what do you think of white?"
    m "What should white do?{nw}"
    $ _history_list.pop()
    call monika_chesslesson_sicilian_defense_question1
    return

label monika_chesslesson_sicilian_defense_question1:
    while (qustion1_bb5_chose is False) or (question1_d4_chose is False) or (question1_nc3_chose is False) or (question1_b3_chose is False):
        m "What should white do?{fast}"
        menu:
            "Bb5.":
                call monika_chesslesson_sicilian_defense_question1_answer_bb5(question1_bb5_chose)
                $ question1_bb5_chose = True
            "d4.":
                call monika_chesslesson_sicilian_defense_question1_answer_d4(question1_d4_chose)
                $ question1_d4_chose = True
            "Nc3.":
                call monika_chesslesson_sicilian_defense_question1_answer_d4(question1_nc3_chose)
                $ question1_nc3_chose = True
            "b3.":
                call monika_chesslesson_sicilian_defense_question1_answer_d4(question1_b3_chose)
                $ question1_b3_chose = True
            "I think there is no good move now.":
                return
    return

label monika_chesslesson_sicilian_defense_question1_answer_bb5(question1_bb5_chose):
    if question1_bb5_chose is True:
        call monika_chesslesson_answer_repeated
        return
    python:
        chess_teaching_disp.queue_move("f1b5")
        chess_teaching_disp.handle_player_move()
    m "Oh, Bb5, the only chance that allows white to attack black's knight right now."
    m "This is known as \"Nyezhmetdinov-Rossolimo Attack\", one of the common variations of Sicilian Defense."
    m "Do you understand why did white play this move?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you understand why did white play this move?{fast}"
        "Yes.":
            m "Okay, then let us talke about pros and cons of this choice."
            m "Pros are that we added more pressure on black's knight, prevented black from forming a solid pawn chain easily and provided a chance to castle."
            m "Cons are this knight is protected solidly by two pawns, it's not easy to take this knight down without exchange."
            m "This move is not bad. Now, let us see if there are other options."
        "No.":
            m "Then, I'm going to explain this choice for you."
            m "This bishop move provided a chance to castle, white can play catious O-O to enjoy a long game."
            m "Meanwhile, this move is trying to exchange the black's knight, which is equivalent to tear black's defense down, so black is not easy to form a solid pawn chain."
            m "{i}What makes a pawn chain really solid is never just pawns themselves, but materials that support the pawn chain{/i}."
            m "Without this knight, this pawn chain is not {i}that{/i} solid anymore."
            m "So the conclusion is that this move is a book move, not good or bad."
            m "Now, let us see if there are other options..."
    python:
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "r1bqkbnr/pp1ppppp/2n5/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
        renpy.pause(1)
    return

label monika_chesslesson_sicilian_defense_question1_answer_d4(question1_d4_chose):
    if question1_d4_chose is True:
        call monika_chesslesson_answer_repeated
        return
    
    python:
        chess_teaching_disp.queue_move("d2d4")
        chess_teaching_disp.handle_player_move()
    
    m "Yes, d4 is the most popular choice of Open Siclian."
    m "With d4, white immediately attacks the center of black, and then, things like these follow:"
    python:
        chess_teaching_disp.queue_move("c5d4")
        chess_teaching_disp.handle_monika_move()
        renpy.pause(2)
        chess_teaching_disp.queue_move("f3d4")
        chess_teaching_disp.handle_player_move()
        renpy.pause(2)
    m "Black captures d4 pawn, then, white recaptures this pawn so that white doesn't lose a pawn."
    m "It's not hard to understand that black can not capture white's knight without exchange now, because the queen of white is protecting it."
    m "Let us take a view of this situation: "
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_makethebest_bishop",
            category=["chess lessons"],
            prompt="How to make the best of a bishop?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_makethebest_bishop:
    m 1eua "Chess players usually have heard two words frequently:{w=0.2}\"Bad Bishop\" and \"Good Bishop\"."
    m 1etd "But what's the difference between them?{w=0.2}{nw}"
    extend 1eub " Let us find them out today!"
    m 3duc "Hold on a second..."

    #Let Monika move to left so we have enough room for board.
    show monika 1eua at t21

    # Call the board.
    python:
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True, starting_fen = "r2q1rk1/1b3ppp/p1pbpn2/2pp4/Q2P4/2P1PNB1/PP1N1PPP/R3K2R w KQ - 2 11")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()

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
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3")
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    if seen_event("monika_chesslesson_french_defense") is True:
        extend 2lsb "As you can see, French Defense is known for its unbreakable,{w0.2} but, in fact, the defender has created a bad bishop for itself."
    else:
        extend 2lsb "The current opening in front of you eyes is the French Defense, which is known for its unbreakable.{w=0.2} But, in fact, the defender has created a bad bishop for itself."
    m 2esb "Which bishop is the bad one?{nw}"
    menu:
        m "Which bishop is the bad one?{fast}"
        "The light-squared one.":
            m 2hub "Yes, you are right!{nw}"
            extend 2lub " That bishop is blocked by e6 pawn, which makes it's hard to activate!"

        "The dark-squared one.":
            m 2etd "The dark one?{nw}"
            extend 2etu " Hmmm...{w=0.2} I'm afraid that's not the correct answer."
            python:
                for i in range(3,9,1):
                    chess_teaching_disp.request_highlight("{0}{1}".format( chr( ord('a')+i-3), 9-i))
            m 2esd "This dark-squared bishop is on the a3-f8 dignaol, which means it controls 5 squares now."
            m 2esc "So this is not a real bad bishop."
            python:
                for i in range(3,9,1):
                        chess_teaching_disp.remove_highlight("{0}{1}".format( chr( ord('a')+i-3), 9-i))
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
        chess_teaching_disp.hide()
        chess_teaching_disp = MASChessDisplayableBase(is_player_white=True,starting_fen = "rnbqk1nr/ppppppbp/6p1/8/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 1 3")#Modern Defense fen
        chess_teaching_disp.toggle_sensitivity()
        chess_teaching_disp.show()
    extend 2esb "This is the famous Modern Defense, which made a {i}Finachetto{/i}."

    if seen_event("monika_chesslesson_modern_defense") is False:
        m 2eua "Since I haven't taught you Modern Defense, let us have a brief introduction of that opening...{w=1.0}{nw}"
        python:
            chess_teaching_disp.hide()
            chess_teaching_disp = MASChessDisplayableBase(is_player_white=True)
            chess_teaching_disp.toggle_sensitivity()
            chess_teaching_disp.show()

        m 2lub "In this opening, white plays e4 as the first move, {w=0.2}{nw}"
        python:
            chess_teaching_disp.queue_move("e2e4")
            chess_teaching_disp.handle_player_move()
        extend "and black played g6, {w=0.2}{nw}"
        python:
            chess_teaching_disp.queue_move("g7g6")
            chess_teaching_disp.handle_monika_move()
        extend 2esa "which looks very confused. We will talk about this move which seems like broke the basic principle of opening later."

        m 2lsa "White then plays d4 to control 4 central squares. {w=0.3}{nw}"
        python:
            chess_teaching_disp.queue_move("d2d4")
            chess_teaching_disp.handle_player_move()
        extend 2lsb " And now, the key point of this opening is going to appear:"

        python:
            chess_teaching_disp.queue_move("f8g7")
            chess_teaching_disp.handle_monika_move()
            renpy.pause(2)
        
        m 2esb "A {i}Finachetto{/i} appeared! That's why Black's previous step didn't control the center."
        m 4lsb "This bishop enjoys a powerful diagonal:"
    else:
        m 2eub "Since I have taught you the Modern Defense, you should actually have some knowledge of Finachetto already."
        m 4lsb "Yes, this bishop controls so many squares:"
    
    python:
        i = 0
        while i<=7:
            chess_teaching_disp.request_highlight("{0}{1}".format(chr(ord('a')+i),8-i))
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

    # Make the board disappear. Let Monika back to where she was.
    $ chess_teaching_disp.hide()
    show monika at t11
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="TEST_ONLY",
            category=["chess lessons"],
            prompt="TEST ONLY",
            pool=True,
        )
    )
label TEST_ONLY:
    if seen_event("monika_chesslesson_init") is True:
        m "SEE THIS STANDS FOR YOU HAVE SEEN CHESS LESSON INIT ALREADY."
    if seen_event("monika_chesslesson_keypoint_1") is True:
        m "SEE THIS STANDS FOR YOU HAVE SEEN KEY POINT 1 ALREADY."
    if seen_event("monika_chesslesson_popular_openings") is True:
        m "SEE THIS STANDS FOR YOU HAVE SEEN POPULAR OPENINGS ALREADY."

    m "TEST END."
    return
