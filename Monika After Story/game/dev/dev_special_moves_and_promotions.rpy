init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_chess_moves_test",
            category=["dev"],
            prompt="CHESS SPECIAL MOVES AND PROMOTIONS",
            pool=True,
            unlocked=True
        )
    )

label dev_chess_moves_test:

    m 1eua "What do you want to test?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you want to test?{fast}"

        "White promotion.":
            $ player_color = chess.WHITE
            $ starting_fen = "8/PPPPPPPP/8/8/8/8/8/k6K w - - 0 1"

        "Black promotion.":
            $ player_color = chess.BLACK
            $ starting_fen = "k6K/8/8/8/8/8/pppppppp/8 w - - 0 1"

        "White castling.":
            $ player_color = chess.WHITE
            $ starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"

        "Black castling.":
            $ player_color = chess.BLACK
            $ starting_fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        "White en passant.":
            $ player_color = chess.BLACK
            $ starting_fen = "8/8/8/3pP3/8/8/8/k6K w - d6 0 1"

        # "Black en passant.":
        #     $ player_color = chess.BLACK
        #     $ starting_fen = "k6K/8/8/8/3Pp3/8/5Pp1/8 b - d6 0 1"

    $ chess_displayable_obj = MASChessDisplayable(player_color=player_color, starting_fen=starting_fen, practice_mode=True)

    $ ui.add(chess_displayable_obj)

    $ ui.interact(suppress_underlay=True)

    m 1eua "Do you want to test anything else?"
    $ _history_list.pop()
    menu:
        m "Do you want to test anything else?{fast}"

        "Yes.":
            jump dev_chess_fen_test

        "No.":
            return
