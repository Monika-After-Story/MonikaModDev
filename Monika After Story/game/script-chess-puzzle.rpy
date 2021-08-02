define CHESSPUZZLE_NUMBER = 1
define CHESSPUZZLE_PLAYERISWHITE = 1
define CHESSPUZZLE_PLAYERISBLACK = 2
define CHESSPUZZLE_RESULT_PLAYER_PASSED = 1
define CHESSPUZZLE_RESULT_PLAYER_GIVE_UP = 2



$ config.developer = True
$ config.console = True

default persistent._mas_player_puzzlelevel = 800

init 5 python:
    #-------
    # This list is used to store difficulty value scores for puzzles.
    # The more difficult a puzzle is, the higher its difficulty score.
    # The 0th element of this list corresponds to the score of the 1st puzzle, the 1st element corresponds to the score of the 2nd puzzle, and so on.
    # Increasing the length of this list allows the puzzle system to expand the search area when selecting the pool of puzzles.
    # Generally speaking, we consider puzzles to be between 400 and 2600 score.
    # Because this score represents "the lowest ELO rating of the person who solves the puzzle."
    #
    # Reference:
    #    400 points for someone who knows little or nothing about chess.
    #    800 is for beginners.
    #    1500 is an advancer.
    #    A master with a score above 2000.
    #    A score of 2400 or above is considered a grandmaster.
    #    The current ELO rating for the strongest human in the world is around 2800.
    #
    # Suggestion:
    #   Use insert()  the function to add elements instead of append() the function.
    #   Because insert() requires the position of the element, which helps people quickly figure out which element it is.
    #-------
    mas_list_puzzle = list()
    mas_list_puzzle.insert(0,2200)
    mas_list_puzzle.insert(1,476)
    mas_list_puzzle.insert(2,1283)

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_chesslesson_puzzles_start",
            category=["chess lessons"],
            prompt="Can you show me a chess puzzle?",
            pool=True,
            conditional="seen_event('monika_chesslesson_init')",
            action=EV_ACT_UNLOCK,
            rules={"no_unlock":None}
        )
    )

label monika_chesslesson_puzzles_start:
    if mas_isMoniUpset(higher=True):
        $ event = mas_getEV("monika_chesslesson_puzzles_start")
        if event.shown_count == 0:
            # Set player's chess puzzle level based on their chess level:
            if persistent._mas_pm_player_chesslevel == chesslevel_master:
                $ persistent._mas_player_puzzlelevel = 2000
            elif persistent._mas_pm_player_chesslevel == chesslevel_advancer:
                $ persistent._mas_player_puzzlelevel = 1500
            elif persistent._mas_pm_player_chesslevel == chesslevel_beginner:
                $ persistent._mas_player_puzzlelevel = 800
            else:
                $ persistent._mas_player_puzzlelevel = 400
            m 1eud "Chess puzzles?"
            m 1sub "I'm so glad you asked!"
            m 3sub "Solving puzzles of chess is an important way to improve your chess level."
            m 1hub "So, in order to help you improve at chess, I will certainly give you puzzles!"
            m 1eub "I will also try to explain puzzles if you can't understand them."
            m 1tuu "You can even ask for some hints if it's too hard for you, [mas_get_player_nickname()]~"
            if persistent._mas_pm_player_chesslevel is chesslevel_master:
                m 1rusdlb "I don't think it's possbile for you, though, considering your accomplishments in chess."
                m 1eusdlb "You are a {i}master{/i}, after all..."
            elif persistent._mas_pm_player_chesslevel is chesslevel_advancer:
                m 1euc "However, given that you also have a good understanding of chess, it is unlikely that this will happen much..."
            m 1eud "Anyways, one last thing to note is..."
            m "I'm not really at the top of chess, so I can't think of too many chess puzzles right off the bat..."
            m 1eub "But I promise, I will spend part of my spare time to think of a puzzle!"
            m "I'll also show you a few that you've already seen, because you know something new when you review the past after all."
            m 1hub "Alright, let us get your first puzzle..."
        else:
            m 1eub "Head to another one? Ehehe~"
            # Monika turns her eyes to one side when she thinks, 
            # but not only to one side. 
            # However, she does have a tendency to look at right. 
            # She has a 2/3 chance to look at right, 1/3 chance to look at left,
            # which is consistent with real human thinking habits.
            if renpy.random.randint(1,3) == 1:
                m 1rsa "Hmmm...{w=0.5}{nw}"
            else:
                m 1lsa "Hmmm...{w=0.5}{nw}"
            m 4hub "This one!"

        jump monika_chesslesson_puzzles_choicer

    elif mas_isMoniDis():
        m 2ekc "Sorry, [player], but I'm really not in the mood to think about a puzzle right now."
        m 2rkc "...It takes too much thought to think of this kind of thing, and I am in a very disordered mood recently..."
        m 2eka "I promise when my head clears a little, we'll be able to solve the puzzle together, okay?"
        m 1eka "Sorry again.{w=0.3} I hope you are not angry for this."
    elif mas_isMoniBroken():
        m 6wkc "..."
        m 6ckc "..."
        if ranom.randint(1,5) == 1:
            m 6rktpu "I think you are the most complicated puzzle already. There is no need to get another one."
    return

label monika_chesslesson_puzzles_choicer:
    # This label choose a random puzzle label and jump to that label.
    # Firstly gain a little affection for asking a puzzle.
    $ mas_gainAffection(modifier = 0.5)

    # Secondly let Monika move to left so we have enough room.
    show monika at t21

    # Thirdly start the choice.
    python:
        delta = dict()

        for i in range(1,len(mas_list_puzzle),1):
            delta[str(i)] = abs(mas_list_puzzle[i] - persistent._mas_player_puzzlelevel) 

        random_number = random.randint(1,2600)
        delta.sort(reverse = True)

        for i in range(1,len(mas_list_puzzle),1):
            if random_number > delta[i-1]:
                renpy.jump()
    return

label monika_chesslesson_puzzles_result_complete:
    # Change the player's puzzle score based on their performance.
    $ chess_puzzle.score_settlement()

    if persistent._mas_player_puzzlelevel < 800:
        # At this level(didn't even begin to learn chess), player need more encouragement than constructive proposal.
        if chess_puzzle.incorrect_total == 0:
            m "Wow, you correctly solved this puzzle without one single incorrect move!"
            m "Keep trying, I'm pretty sure you can get better and better at chess~"
            m "Now..."
        elif chess_puzzle.incorrect_total < 5:
            $ temp = 's' if chess_puzzle.incorrect_total > 1 else ''
            m "Puzzle solved!"
            m "And you made only [chess_puzzle.incorrect_total] incorrect move[temp] too!"
            m "Way to go, [player]!"
            m "Anyway..."
        else:
            m "Puzzle solved!"
            m "Not bad. Though you chose a few bad moves, it's still a nice one!"
            m "Anyway..."
    elif persistent._mas_player_puzzlelevel <= 1500:
        # At this level(beginner), player should start hearing some advice.
        if chess_puzzle.incorrect_total == 0:
            m 2hua "Puzzle solved!{w=0.3}{nw}"
            extend 2wub " Wow, you seems solved it easily!"
            m 2tuu "It feels so good to solve puzzles this easily, right?"
            m 2hub "Ahaha~"
        elif chess_puzzle.incorrect_total < 5:
            $ temp = 's' if chess_puzzle.incorrect_total > 1 else ''
            m 2hua "Puzzle solved!"
            m 4hub "Only [chess_puzzle.incorrect_total] incorrect move[temp], that's impressive!"
        else:
            m "Puzzle solved!"
            m "Though, considering how many wrong moves you've made, I suggest you do some special training sometime."
    elif persistent._mas_player_puzzlelevel <= 2000:
        # At this level(advancer), player is a skillful person in chess already. So Monika started sharing ideas with the player.
        m ""
    else:
        # At this level(master), player is really good at chess, player is even possible to be a grandmaster.
        # Monika will be genuinely surprised, because this is a really very high level.
        m ""
    m 3eub "Would you like another one?{nw}"
    $ chess_puzzle.hide()
    $ _history_list.pop()
    menu:
        m "Would you like another one?{fast}"
        "Yes.":
            m 2hua "Okay!"
            jump monika_chesslesson_puzzles_choicer
        "No.":
            m "Then maybe another time."
    return

label monika_chesslesson_puzzles_result_giveup:
    m 1eka "Giving up?"
    if chess_puzzle.num_moves == 0:
        if chess_puzzle.incorrect_total == 0:
            m 1rusdrb "But you didn't even pick a single move..."
        elif chess_puzzle.incorrect_total <= 5:
            m 3eka "We don't have to be so negative...{w=0.3}{nw}"
            extend 3eub " also many try a few times can find out how to move?"
            m 2eub "What do you say, [player]?{nw}"
            $ _history_list.pop()
            menu:
                m "What do you say, [player]?{fast}"
                "Let us continue.":
                    m 2hua "Okay!"
                    $chess_puzzle.quit_game = False
                    $chess_puzzle.game_loop()
                "Let's stop here.":
                    pass
        else:
            m 2eka "Indeed, it's frustrating to try so many times and still not be able to solve it..."
    elif chess_puzzle.num_moves_total - chess_puzzle.num_moves < 6:
        m "I personally suggest you to try a few more times...{w=0.2}"
        extend 2tuu " Plot tip, this puzzle will soon be over."
        m 2eua "Would you continue?{nw}"
        $ _history_list.pop()
        menu:
            m "Would you continue?{fast}"
            "Okay, let's do it.":
                m 2hub "Okay!"
                $chess_puzzle.quit_game = False
                $chess_puzzle.game_loop()
            "Let's stop here.":
                pass
    
    show monika at t11
    $ chess_puzzle.hide()
    m 1hub "Well, nothing wrong with that! Some puzzles are just too diffcult after all."
    m 3hub "If you ever want to see some more puzzles, feel free to ask me!"
    m 1hua "And, thanks for asking a puzzle~"
    return

label monika_chesslesson_puzzles_wrong_default:
    m 2eksdla "Sorry, [player]..."
    m 2eksdlb "But I can't even see any point in this move."
    m 2ekb "Try again?"
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_hint_default(asked):
    if asked == False:
        m 2eud "Hint?"
        m 2eka "Well, of course I'd love to tip you off, but I think it's all too obvious what to do in the current situation..."
        m 2rksdra "If I could say anything, it would be to just say the answer."
        m 2hub "So, [mas_get_player_nickname()], think about this situation again!"
    else:
        m 2euc "...Hmm, so you really find this current situation difficult?"
        m 2hksdlb "But it is so strange to tell the answer directly..."
        m 3eka "...Why don't you think about it for another second?"
    python:
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_1:
    show monika at t21
    python:
        chess_puzzle = MASChessDisplayable_Puzzle(is_player_white=False, starting_fen = "8/2ppppp1/rpR4k/8/8/6p1/5pP1/7K b - - 0 1")
        chess_puzzle.num_moves_total = 10
        chess_puzzle.puzzle_id = 1
        chess_puzzle.reaction_add(
            turn_number = 1,
            correct_move = "d7d6",
            correct_response = "c6d6",
            incorrect_move = ["d7c6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 2,
            correct_move = "f7f6",
            correct_response = "d6f6",
            incorrect_move = ["e7d6","monika_chesslesson_puzzles_1_wrong","c7d6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 3,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7f6","monika_chesslesson_puzzles_1_wrong","e7f6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 4,
            correct_move = "h7g8",
            correct_response = "h6h8",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 5,
            correct_move = "g8f7",
            correct_response = "h8f8",
            incorrect_move = ["g8h8","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        # HERE UNFINISHED START
        chess_puzzle.reaction_add(
            turn_number = 6,
            correct_move = "f7e6",
            correct_response = "f8h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 7,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 8,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 9,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 10,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 11,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 12,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 13,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 14,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 15,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 16,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.reaction_add(
            turn_number = 17,
            correct_move = "h6h7",
            correct_response = "f6h6",
            incorrect_move = ["g7h6","monika_chesslesson_puzzles_1_wrong","h7h6","monika_chesslesson_puzzles_1_wrong"],
            hint = "monika_chesslesson_puzzles_1_hint"
        )
        chess_puzzle.show()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_1_hint(asked):
    if asked == False:
        m "Oh, you'd like to have a hint?"
        m "Okay!"
    else:
        m "Did you forget?"
        m "Well, let me just mention you again."
    m "Firstly, this puzzle is pretty diffcult, this is indeed."
    $ chess_puzzle.toggle_sensitivity()
    $ chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_1_wrong:
    m 1rusdlb "..."
    m 2eka "Okay, sorry, but you made a common mistake with this puzzle."
    m 2eud "Mind you, if we simply took off the opponent's rook in this way..."
    m 2wud "Are we attacking the opponent's king now?"
    m 2wuo "No! So, we took away our opponent's only moveable piece without attacking their king!"
    m "Notice that the opponent's king has no legal moves, so now it's a stalemate!"
    m 2eka "Of course, I have to say, this situation is a very tough one..."
    m 2duu "So, if you don't know what to do...{w=0.2}{nw}"
    extend 2nuu " Let's ask your dear girlfriend."
    m 2hub "Ahaha!"
    m 2hua "Anyways, let us back to the board."
    python:
        chess_puzzle.num_moves-=1
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_2:
    python:
        chess_puzzle = MASChessDisplayable_Puzzle(is_player_white=True, starting_fen = "6k1/5ppp/8/1P1B4/P3R3/1r6/p6r/3K4 w - - 0 1")
        chess_puzzle.num_moves_total = 1
        chess_puzzle.puzzle_id = 2
        chess_puzzle.reaction_add(
            turn_number = 1,
            correct_move = "e4e8",
            correct_response = "",
            incorrect_move = ["d5b3","monika_chesslesson_puzzles_2_wrong1","d5f7","monika_chesslesson_puzzles_2_wrong2"],
            hint = "monika_chesslesson_puzzles_2_hint"
        )
        chess_puzzle.show()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_2_wrong1:
    m 2eud "Oh, removing the rook?"
    m 2husdrb "Well, I know this seems like a clever choice...{w=0.3}{nw}"
    extend 4lusdrb " but in fact,{w=0.3}{nw}"
    python:
        chess_puzzle.queue_move("a2a1q")
        chess_puzzle.handle_manual_move()
    extend 4lksdrb " it doesn't help. The opponent will promote the pawn into a queen, which is a checkmate."
    m 2hua "So, let us try to find a better move."
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.undo_move()
        chess_puzzle.be_player_turn()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_2_wrong2:
    m 2etd "Attack the king with the bishop... I see."
    m 2rtd "You want to check the opponent's king to give the white side one more turn of living space, right?"
    m 1eub "Well, if that's what you're thinking, then you're doing fine, and it does fight for a turn of survival."
    m 1eka "The problem is, the black king can immediately remove your bishop, and after that, there's nothing you can do about the coming checkmate."
    m 1hub "There is one move we can take to turn things around! Try and find it."
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_2_hint(asked):
    if asked == False:
        m 4esb "I wonder if you have noticed a fact..."
    else:
        m 2eka "Did you forget, [player]?"
        m 2eub "There is a fact that you should notice."
    m 4esa "That is, the opponent's king is actually in an extremely dangerous situation at this time."
    m 2eua "We have a one-move checkmate."
    m 2eub "In fact, there are only two ways for us to attack our opponent's king now."
    m 2euu "Can you guess which one?"
    m 2hub "Ahaha, try to find it on your own!"
    python:
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3:
    python:
        chess_puzzle = MASChessDisplayable_Puzzle(is_player_white=False, starting_fen = "3r1rk1/pp3ppp/1q2b3/6N1/1n2Q3/8/PPP1B1PP/2KR3R b - - 6 17")
        chess_puzzle.num_moves_total = 5
        chess_puzzle.puzzle_id = 3
        chess_puzzle.reaction_add(
            turn_number = 1,
            correct_move = "b4a2",
            correct_response = "c1b1",
            incorrect_move = ["g7g6","monika_chesslesson_puzzles_3_wrong1_1","d8d1","monika_chesslesson_puzzles_2_wrong1_2"],
            hint = "monika_chesslesson_puzzles_3_hint1"
        )
        chess_puzzle.reaction_add(
            turn_number = 2,
            correct_move = "a2c3",
            correct_response = "b1c1",
            incorrect_move = ["g7g6","monika_chesslesson_puzzles_3_wrong2_1","d8d1","monika_chesslesson_puzzles_2_wrong2_2"],
            hint = "monika_chesslesson_puzzles_3_hint2"
        )
        chess_puzzle.reaction_add(
            turn_number = 3,
            correct_move = "c3e4",
            correct_response = "",
            incorrect_move = [],
            hint = "monika_chesslesson_puzzles_hint_default"
        )
        chess_puzzle.show()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3_wrong1_1:
    m 2euc "Hmm...{w=0.2}{nw}"
    extend 2eud " If I'm right, you're worried about the queen's checkmate threat, aren't you?"
    m 2eub "This move does prevent the threat. That's true. But there is one move we can make that will be overwhelming."
    m 2hub "Try and find it!"
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3_wrong1_2:
    m 2eud "Exchange the rook with your opponent...{w=0.2} I see."
    m 2eua "It's not a bad move, but we have a much better move than this."
    m 2eub "Try and find it!"
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3_wrong2_1:
    m 2rtd "..."
    m 2eka "Since black is already attacking, it would be strange to suddenly turn around and make such a negative move."
    m 2eub "Try again?"
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3_wrong2_2:
    m 2hub "Well played, this is a pretty good move!"
    m 2hua "However, to make sure you understand each of these ideas, let's try another solution."
    python:
        chess_puzzle.num_moves -= 1
        chess_puzzle.undo_move()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3_hint1(asked):
    if asked == False:
        m 2hua "Want a hint? Okay!"
    else:
        m 2eua "Well, let me recall this hint."
    m 2euc "At first glance, the focus seems to be on the h7 square. White may checkmate black with queen in the next turn."
    m 2rsd "So, many people will want to make sure their king is safe first. That's understandable."
    m 4esa "But I'd like you to notice that white king is no much safer than black king."
    m 3esb "Given that it's black's turn right now, maybe black should have taken the initiative?"
    m 2hub "Think about it!"
    python:
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.game_loop()
    return

label monika_chesslesson_puzzles_3_hint2(asked):
    if seen_event("monika_chesslesson_tactic_pin"):
        m 3eub "Do you remember how I taught you about the {i}pin{/i} tactic?"
    else:
        m 2eub "Notice one thing. The pawn on b2 cannot leave b-file, because white's queen is in b-file too, and that pawn is the only barrier between the queen and the king."
        m 2eua "Putting white in such a position where it is impossible to move a piece is called {i}pin{/i}."
        m 2hua "That's a basic tactic in chess, and I have a special lesson of it for you."
    m 2eua "Given that the pawn can't move, can we do something about it?"
    m 2eub "Go for it!"
    python:
        chess_puzzle.toggle_sensitivity()
        chess_puzzle.game_loop()
    return
