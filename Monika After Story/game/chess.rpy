#TODO: Fix label names. It's difficult to follow

# we now will keep track of player wins / losses/ draws/ whatever
default persistent._mas_chess_stats = {
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "practice_wins": 0,
    "practice_losses": 0,
    "practice_draws": 0
}

#Stores the chess difficulty, this is managed via levels and sublevels
#Key is the level (0-8) - corresponds to stockfish difficulty
#Value is the sublevel (1-5) - corresponds to stockfish depth
default persistent._mas_chess_difficulty = {0: 1}

# pgn as a string
default persistent._mas_chess_quicksave = ""

# dict containing action counts:
default persistent._mas_chess_dlg_actions = {}

# when we need to disable chess for a period of time
default persistent._mas_chess_timed_disable = None

# if the player modified the games 3 times but apologized
default persistent._mas_chess_3_edit_sorry = False

# if the player modified the games 3 times but did not apologize
default persistent._mas_chess_mangle_all = False

# skip file checks
default persistent._mas_chess_skip_file_checks = False

define mas_chess.CHESS_SAVE_PATH = "/chess_games/"
define mas_chess.CHESS_SAVE_EXT = ".pgn"
define mas_chess.CHESS_SAVE_NAME = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789"
define mas_chess.CHESS_PROMPT_FORMAT = "{0} | {1} | Turn: {2} | You: {3}"

# mass chess store
init python in mas_chess:
    import os
    import chess.pgn
    import store.mas_ui as mas_ui

    # if this is true, we quit game (workaround for confirm screen)
    quit_game = False

    # relative chess directory
    REL_DIR = "chess_games/"

    CHESS_MENU_WAIT_VALUE = "MATTE"
    CHESS_MENU_WAIT_ITEM = (
        _("I can't make this decision right now..."),
        CHESS_MENU_WAIT_VALUE,
        False,
        False,
        20
    )

    CHESS_NO_GAMES_FOUND = "NOGAMES"

    # files to delete
    del_files = (
        "chess.rpyc",
    )

    # files to glitch
    gt_files = (
        "definitions.rpyc",
        "event-handler.rpyc",
        "script-topics.rpyc",
        "script-introduction.rpyc",
        "script-story-events.rpyc",
        "zz_pianokeys.rpyc",
        "zz_music_selector.rpyc"
    )

    # temporary var for holding chess strength
    # [0]: True if this is set, False if not
    # [1]: value of the chess strength
    chess_strength = (False, 0)

    #Marker for ongoing game
    IS_ONGOING = '*'
    # for dlg flow, return value for continuing instead of jumping to new
    # game
    CHESS_GAME_CONT = "USHO"

    # for dlg flow, return value for using backup save instead of jumping to
    # new game
    CHESS_GAME_BACKUP = "foundyou"

    # for dlg flow, return value for using file save instead of jumping to new
    # game
    CHESS_GAME_FILE = "file"

    # currently loaded game, because we need some sort of gscope
    loaded_game_filename = None

    # dlg actions (for keeping count of things)
    # Quick Save LOST: the internal quick save got coruppted or modified, but
    #   assume corrupted.
    #   (Monika's fault)
    QS_LOST = 0

    # Quick File LOST (OF Course Not): the external quick save got removed,
    #   player denied removal
    #   (Player's fault)
    QF_LOST_OFCN = 1

    # Quick File LOST MAYBE: the external quick save got removed, player
    #   admitted to it
    #   (Player's fault)
    QF_LOST_MAYBE = 2

    # Quick File LOST ACciDeNT: the external quick save got removed, player
    #   said it was an accident.
    #   (Could be player's fault, or not)
    QF_LOST_ACDNT = 3

    # Quick File EDIT YES: the external quick save got edited, player admitted
    #   to it.
    #   (almost certainly player's fault)
    QF_EDIT_YES = 4

    # Quick File EDIT NO: the external quick save got edited, player lies
    #   (almost certanilky player's fault)
    QF_EDIT_NO = 5

    ##### dialogue constants

    # ofcnot
    DLG_QF_LOST_OFCN_ENABLE = True
    DLG_QF_LOST_OFCN_CHOICE = _("Of course not!")

    # maybe
    DLG_QF_LOST_MAY_ENABLE = True
    DLG_QF_LOST_MAY_CHOICE = _("Maybe...")

    # accident
    DLG_QF_LOST_ACDNT_ENABLE = True
    DLG_QF_LOST_ACDNT_CHOICE = _("It was an accident!")

    # base part of label for variable chess strength when monika wins
    DLG_MONIKA_WIN_BASE = "mas_chess_dlg_game_monika_win_{0}"

    # base part of label for variable chess strength when monika wins by
    # early surrender
    DLG_MONIKA_WIN_SURR_BASE = "mas_chess_dlg_game_monika_win_surr_{0}"

    # base part of label for variable chess strength when monika loses
    DLG_MONIKA_LOSE_BASE = "mas_chess_dlg_game_monika_lose_{0}"


## functions ==================================================================
    def _checkInProgressGame(pgn_game, mth):
        """
        Checks if the given pgn game is valid and in progress.

        IN:
            pgn_game - pgn game to check
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            SEE isInProgressGame
        """
        if pgn_game is None:
            return None

        if pgn_game.headers["Result"] != "*":
            return None

        # now which one is the player?
        if pgn_game.headers["White"] == mth:
            the_player = "Black"
        elif pgn_game.headers["Black"] == mth:
            the_player = "White"
        else: # monika must be a player
            return None

        # otherwise, we can now add this as an in progress game
        # first, though we need number of turns
        # this will store the number of turns in board.fullmove_number
        board = pgn_game.board()
        for move in pgn_game.main_line():
            board.push(move)

        return (
            CHESS_PROMPT_FORMAT.format(
                pgn_game.headers["Date"].replace(".","-"),
                pgn_game.headers["Event"],
                board.fullmove_number,
                the_player
            ),
            pgn_game
        )

    def isInProgressGame(filename, mth):
        """
        Checks if the pgn game with the given filename is valid and
        in progress.

        IN:
            filename - filename of the pgn game
            mth - monika twitter handle. pass it in since I'm too lazy to
                find context from a store

        RETURNS:
            tuple of the following format:
                [0]: Text to display on button
                [1]: chess.pgn.Game of the game
            OR NONE if this is not a valid pgn game
        """
        if filename[-4:] != CHESS_SAVE_EXT:
            return None

        pgn_game = None
        with open(
            os.path.normcase(CHESS_SAVE_PATH + filename),
            "r"
        ) as loaded_game:
            pgn_game = chess.pgn.read_game(loaded_game)

        return _checkInProgressGame(pgn_game, mth)

    def _increment_chess_difficulty():
        """
        Increments chess difficulty
        """
        level = store.persistent._mas_chess_difficulty.keys()[0]
        sublevel = store.persistent._mas_chess_difficulty.values()[0]

        if sublevel == 5 and level < 9:
            level += 1
            sublevel = 1

        elif sublevel < 5:
            sublevel += 1

        else:
            return

        store.persistent._mas_chess_difficulty = {level:sublevel}

    def _decrement_chess_difficulty():
        """
        Decrements chess difficulty
        """
        level = store.persistent._mas_chess_difficulty.keys()[0]
        sublevel = store.persistent._mas_chess_difficulty.values()[0]

        if sublevel == 1 and level < 0:
            level -= 1
            sublevel = 5

        elif sublevel > 1:
            sublevel -= 1

        else:
            return

        store.persistent._mas_chess_difficulty = {level: sublevel}

    def _get_player_color(loaded_game):
        """
        Gets player color

        IN:
            loaded_game - pgn representing the loaded game

        OUT:
            The player's color
        """
        if loaded_game.headers["White"] == store.mas_monika_twitter_handle:
            return store.chess.BLACK
        return store.chess.WHITE

label game_chess:
    m 1eub "You want to play chess? Alright~"

    #Do some var setup
    $ loaded_game = None
    $ failed_to_load_save = True

    if not renpy.seen_label("mas_chess_save_selected"):
        call mas_chess_save_migration

        # check if user selected a save
        if not _return:
            return

        # if the return is no games, jump to new game
        elif _return == mas_chess.CHESS_NO_GAMES_FOUND:
            jump .new_game_start

        # otherwise user has selected a save, which is the pgn game file.
        $ loaded_game = _return

    elif len(persistent._mas_chess_quicksave) > 0:
        # quicksave holds the pgn game in plaintext
        python:
            quicksaved_game = chess.pgn.read_game(
                StringIO.StringIO(persistent._mas_chess_quicksave)
            )

            quicksaved_game = mas_chess._checkInProgressGame(
                quicksaved_game,
                mas_monika_twitter_handle
            )

        # failure reading a saved game
        if quicksaved_game is None:
            $ failed_to_load_save = False

            if persistent._mas_chess_3_edit_sorry:
                call mas_chess_dlg_qf_edit_n_3_n_qs

                $ persistent._mas_chess_quicksave = ""

                if _return is not None:
                    return

            else:
                python:
                    import os
                    import struct

                    # load up the unfinished games and corrupt them
                    pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
                    if pgn_files:

                        # grab only unfnished games
                        valid_files = list()
                        for filename in pgn_files:
                            in_prog_game = mas_chess.isInProgressGame(
                                filename,
                                mas_monika_twitter_handle
                            )

                            if in_prog_game:
                                valid_files.append((filename, in_prog_game[1]))

                        # now break those games
                        if len(valid_files) > 0:
                            for filename,pgn_game in valid_files:
                                store._mas_root.mangleFile(
                                    mas_chess.CHESS_SAVE_PATH + filename,
                                    mangle_length=len(str(pgn_game))*2
                                )

                $ persistent._mas_chess_quicksave = ""

                # okay now begin dialogue
                call mas_chess_dlg_qs_lost

                # not None returns means we should quit from chess
                if _return is not None:
                    return

            jump .new_game_start

        # if player did bad, then we dont do file checks anymore
        if persistent._mas_chess_skip_file_checks:
            $ loaded_game = quicksaved_game[1]
            m "Let's continue our unfinished game."

            if loaded_game:
                $ player_color = mas_chess._get_player_color(loaded_game)
                jump .start_chess

        # otherwise, read the game from file
        python:
            quicksaved_game = quicksaved_game[1]

            quicksaved_filename = (quicksaved_game.headers["Event"] + mas_chess.CHESS_SAVE_EXT)
            quicksaved_filename_clean = (mas_chess.CHESS_SAVE_PATH + quicksaved_filename).replace("\\", "/")

            try:
                if os.access(quicksaved_filename_clean, os.R_OK):
                    quicksaved_file = mas_chess.isInProgressGame(
                        quicksaved_filename,
                        mas_monika_twitter_handle
                    )

                else:
                    store.mas_utils.writelog("Failed to access quickfile.\n")
                    quicksaved_file = None

            except Exception as e:
                store.mas_utils.writelog("QUICKFILE: {0}\n".format(e))
                quicksaved_file = None

        # failure reading the saved game from text
        if quicksaved_file is None:
            $ failed_to_load_save = False
            # save the filename of what the game should have been
            $ mas_chess.loaded_game_filename = quicksaved_filename_clean

            call mas_chess_dlg_qf_lost

            # should we continue or not
            if _return == mas_chess.CHESS_GAME_CONT:
                python:
                    try:
                        if os.access(quicksaved_filename_clean, os.R_OK):
                            quicksaved_file = mas_chess.isInProgressGame(
                                quicksaved_filename,
                                mas_monika_twitter_handle
                            )

                        else:
                            store.mas_utils.writelog("Failed to access quickfile.\n")
                            quicksaved_file = None

                    except Exception as e:
                        store.mas_utils.writelog("QUICKFILE: {0}\n".format(e))
                        quicksaved_file = None

                if quicksaved_file is None:
                    call mas_chess_dlg_qf_lost_may_removed
                    return

            # do we have a backup
            elif _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump mas_chess_game_load_check

            # otherwise we are contiuing or quitting
            else:
                # kill the quicksave
                $ persistent._mas_chess_quicksave = ""

                # check if nonNone, which means quit
                if _return is not None:
                    return

                # otherwise jump to new game
                jump .new_game_start

        python:
            # because quicksaved_file is different form isInProgress
            quicksaved_file = quicksaved_file[1]

            # check for game modifications
            is_same = str(quicksaved_game) == str(quicksaved_file)

        if not is_same:
            # TODO test this
            $ failed_to_load_save = False

            call mas_chess_dlg_qf_edit

            # do we use backup
            if _return == mas_chess.CHESS_GAME_BACKUP:
                $ loaded_game = quicksaved_game
                jump mas_chess_game_load_check

            # or maybe the file
            elif _return == mas_chess.CHESS_GAME_FILE:
                $ loaded_game = quicksaved_file
                jump mas_chess_game_load_check

            # kill the quicksaves
            python:
                persistent._mas_chess_quicksave = ""
                try:
                    os.remove(quicksaved_filename_clean)
                except:
                    pass

            # quit out of chess
            if _return is not None:
                return

            # otherwise jump to a new game
            jump .new_game_start

        # otherwise we are in good hands
        else:
            $ loaded_game = quicksaved_game

            if failed_to_load_save:
                # we successfully loaded the unfinished game and player did not
                # cheat
                m 1eua "We still have an unfinished game in progress."

            m 1efb "Get ready!"

    if loaded_game:
        python:
            player_color = mas_chess._get_player_color(loaded_game)

            practice_mode = loaded_game.headers.get("Practice", False)

        jump .start_chess

    label .new_game_start:
        pass

    #Otherwise first game flow
    m 3eua "Would you like to practice or play against me?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to practice or play against me?{fast}"

        "Practice.":
            $ practice_mode = True

        "Play.":
            $ practice_mode = False


    m "What color would suit you?{nw}"
    $ _history_list.pop()
    menu:
        m "What color would suit you?{fast}"

        "White.":
            $ player_color = chess.WHITE

        "Black.":
            $ player_color = chess.BLACK

        "Let's draw lots!":
            $ choice = random.randint(0, 1) == 0
            if choice:
                $ player_color = chess.WHITE
                m 2eua "Oh look, I drew black! Let's begin!"
            else:
                $ player_color = chess.BLACK
                m 2eua "Oh look, I drew white! Let's begin!"

        "Nevermind.":
            m 1ekc "...Alright, [player].{w=0.3} I was really looking forward to playing with you."
            m 1eka "We'll play another time though, right?"
            return

    label .start_chess:
        pass

    window hide None
    python:
        chess_displayable_obj = MASChessDisplayable(player_color, pgn_game=loaded_game, practice_mode=practice_mode)
        ui.add(chess_displayable_obj)
        results = ui.interact(suppress_underlay=True)

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results

        # game result header
        game_result = new_pgn_game.headers["Result"]

    label .chess_end:
        pass

    $ mas_gainAffection(modifier=0.5)
    # monika wins
    if is_monika_winner:
        $ persistent._mas_chess_stats["practice_losses" if practice_mode else "losses"] += 1

        #Monika wins by player surrender
        if is_surrender:
            m 1ekc "Don't give up so easily..."
            m 1eka "I'm sure if you keep trying, you can beat me."
            m 1ekc "..."
            m 1eka "I hope you don't get frustrated when you play with me."
            m 3ekb "It really means a lot to me that you keep playing if you do~"

        #Monika wins by checkmate
        else:
            m 1sub "I won, yay!~"

            #Some setup
            python:
                total_losses = persistent._mas_chess_stats.get("practice_losses", 0) + persistent._mas_chess_stats.get("losses", 0)
                total_wins = persistent._mas_chess_stats.get("practice_wins", 0) + persistent._mas_chess_stats.get("wins", 0)

            #Responses based on win rate
            if float(total_wins)/total_losses < 0.3:
                call mas_chess_dlg_game_monika_wins_often

            else:
                call mas_chess_dlg_game_monika_wins_sometimes

            m 1eua "Anyway..."

        #Monika plays a little easier
        $ mas_chess._decrement_chess_difficulty()

    #Always save in progress games unless they're over
    elif game_result == mas_chess.IS_ONGOING:
        jump mas_chess_savegame

    #Stalemate
    elif game_result == "1/2-1/2":
        m 1eka "Aw, looks like we have a stalemate."

        if not persistent.ever_won.get("chess"):
            m 3hub "But on the bright side, you're getting closer and closer to beating me, [player]~"

        else:
            m 1hua "Nice work on getting this far, [player]~"

        $ persistent._mas_chess_stats["practice_draws" if practice_mode else "draws"] += 1

    #Player wins
    else:
        $ persistent._mas_chess_stats["practice_wins" if practice_mode else "wins"] += 1

        #Give player XP if this is their first win
        if not persistent.ever_won['chess']:
            $ persistent.ever_won['chess'] = True

        # main dialogue
        if practice_mode:
            m 3hub "Congratulations [player], you won!"

            $ undo_count = new_pgn_game.headers.get("UndoCount", 0)
            if undo_count <= 5:
                m 1hua "You only undid [undo_count] times too, great job."

            elif undo_count <= 10:
                m 1eua "[undo_count] undos, not bad at all. If we keep practicing together, I'm sure we can lower that~"

            else:
                m 1eka "You undid [undo_count] moves though.{w=0.3} {nw}"
                extend 3eua "But I'm sure if we keep practicing, we can get that number lower."

            m 3hua "I'm proud of you, [player]!~"

        else:
            m 3hub "Great job, [player], you won!"
            m 3eua "No matter the outcome, I'll always enjoy playing with you."
            m 1hua "Let's play again soon, alright?"
            m 3hub "It makes me happy to see you win~"

        m 1eua "Anyway..."

        $ mas_chess._increment_chess_difficulty()

    # if you have a previous game, we are overwritting it regardless
    if loaded_game:
        call mas_chess_savegame(silent=True)
        jump .play_again

    #We only save a game if there's enough turns
    if num_turns > 4:
        m 1eua "Would you like to save this game?{nw}"
        $ _history_list.pop()
        menu:
            m "Would you like to save this game?{fast}"

            "Yes.":
                call mas_chess_savegame

            "No.":
                #If you surrender and don't save, it's probably safe to assume we don't want to play again
                if is_surrender:
                    return

    label .play_again:
        pass

    m 1eua "Would you like to play again?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to play again?{fast}"

        "Yes.":
            $ chess_ev = mas_getEV("mas_chess")
            if chess_ev:
                # each game counts as a game played
                $ chess_ev.shown_count += 1

            jump .new_game_start

        "No.":
            pass
    return

label mas_chess_savegame(silent=False):
    if loaded_game: # previous game exists
        python:
            new_pgn_game.headers["Event"] = (
                loaded_game.headers["Event"]
            )

            # filename
            save_filename = (
                new_pgn_game.headers["Event"] +
                mas_chess.CHESS_SAVE_EXT
            )

            # now setup the file path
            file_path = mas_chess.CHESS_SAVE_PATH + save_filename

            # the loaded game needs to be reset if it exists
            loaded_game = None

    # otherwise ask for name
    else:
        python:
            # get file name
            save_name = ""
            while len(save_name) == 0:
                save_name = renpy.input(
                    "Enter a name for this game:",
                    allow=mas_chess.CHESS_SAVE_NAME,
                    length=15
                )

            new_pgn_game.headers["Event"] = save_name

            # filename
            save_filename = save_name + mas_chess.CHESS_SAVE_EXT

            file_path = mas_chess.CHESS_SAVE_PATH + save_filename

            # file existence check
            is_file_exist = os.access(
                os.path.normcase(file_path),
                os.F_OK
            )

        # check if this file exists already
        if is_file_exist:
            m 1eka "We already have a game named '[save_name].'"

            m "Should I overwrite it?{nw}"
            $ _history_list.pop()
            menu:
                m "Should I overwrite it?{fast}"
                "Yes.":
                    pass

                "No.":
                    jump mas_chess_savegame

    python:
        with open(file_path, "w") as pgn_file:
            pgn_file.write(str(new_pgn_game))

        # internal save too if in progress
        if new_pgn_game.headers["Result"] == mas_chess.IS_ONGOING:
            persistent._mas_chess_quicksave = str(new_pgn_game)
        else:
            persistent._mas_chess_quicksave = ""

        # the file path to show is different
        display_file_path = mas_chess.REL_DIR + save_filename

    if not silent:
        m 1dsc ".{w=0.5}.{w=0.5}.{nw}"
        m 1hua "I've saved our game in '[display_file_path]'!"

        if not renpy.seen_label("mas_chess_savegame.pgn_explain"):
            label .pgn_explain:
                pass

            m 1esa "It's in a format called Portable Game Notation, you can open it in PGN viewers to help see where you made your mistakes."

            if game_result == mas_chess.IS_ONGOING:
                m 1lksdlb "It's possible to edit this file and change the outcome of the game...{w=0.5} {nw}"
                extend 1tsu "but I'm sure you wouldn't do that."

                m 1tku "Right, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Right, [player]?{fast}"
                    "Of course not.":
                        m 1hua "Yay~"

        if game_result == mas_chess.IS_ONGOING:
            m 1eub "Let's continue this game soon!"
    return

label mas_chess_cannot_work_embarrassing:
    m 1rksdla "..."
    m 3hksdlb "Well that's embarrassing, it seems I can't actually get chess to work on your system..."
    m 1ekc "Sorry about that, [player]."
    return

label mas_chess_dlg_game_monika_wins_often:
    m 1eka "Sorry you didn't win this time, [player]..."
    m 1ekc "I hope you'll at least keep trying though."
    m 1eua "Let's play again soon, okay?"
    return

label mas_chess_dlg_game_monika_wins_sometimes:
    m 1hub "That was really fun, [player]!"
    m 3eka "No matter the outcome, I always enjoy playing chess with you~"
    m 3hua "I bet if you keep practicing, you'll be even better than me someday!"

    #If the difficulty is above base level, we'll mention lowering it
    if persistent._mas_chess_difficulty != {0:1}:
        m 3eua "Until then though, I'll try and go a little easier on you."
    return

# label for new context for confirm screen
label mas_chess_confirm_context:
    call screen mas_chess_confirm
    $ store.mas_chess.quit_game = _return
    return

# label for chess save migration
label mas_chess_save_migration:
    python:
        import chess.pgn
        import os
        import store.mas_chess as mas_chess

        pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
        sel_game = (mas_chess.CHESS_NO_GAMES_FOUND,)

    if pgn_files:
        python:
            # only allow valid pgn files
            pgn_games = list()
            actual_pgn_games = list()
            game_dex = 0
            for filename in pgn_files:
                in_prog_game = mas_chess.isInProgressGame(
                    filename,
                    mas_monika_twitter_handle
                )

                if in_prog_game:
                    pgn_games.append((
                        in_prog_game[0],
                        game_dex,
                        False,
                        False
                    ))
                    actual_pgn_games.append((in_prog_game[1], filename))
                    game_dex += 1

            game_count = len(pgn_games)
            pgn_games.sort()
            pgn_games.reverse()

        # only show this if we even have multiple pgn games
        if game_count > 1:
            if renpy.seen_label("mas_chess_save_multi_dlg"):
                $ pick_text = _("You still need to pick a game to keep.")
            else:
                label mas_chess_save_multi_dlg:
                    m 1m "So I've been thinking, [player]..."
                    m "Most people who leave in the middle of a chess game don't come back to start a new one."
                    m 1n "It makes no sense for me to keep track of more than one unfinished game between us."
                    m 1p "And since we have [game_count] games in progress..."
                    m 1g "I have to ask you to pick only one to keep.{w=0.2} Sorry, [player]."
                    $ pick_text = _("Pick a game you'd like to keep.")

            show monika 1e at t21
            $ renpy.say(m, pick_text, interact=False)

            call screen mas_gen_scrollable_menu(pgn_games, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, mas_chess.CHESS_MENU_WAIT_ITEM)

            show monika at t11
            if _return == mas_chess.CHESS_MENU_WAIT_VALUE:
                # user backs out
                m 2dsc "I see."
                m 2eua "In that case, please take your time."
                m 1eua "We'll play chess again once you've made your decision."
                return False

            else:
                # user selected a game
                m 1eua "Alright."
                python:
                    sel_game = actual_pgn_games.pop(_return)
                    for pgn_game in actual_pgn_games:
                        game_path = os.path.normcase(mas_chess.CHESS_SAVE_PATH + pgn_game[1])
                        try:
                            os.remove(os.path.normcase(game_path))
                        except:
                            mas_utils.writelog("Failed to remove game at: {0}\n".format(game_path))

        # we have one game, so return the game
        elif game_count == 1:
            $ sel_game = actual_pgn_games[0]

# FALL THROUGH
label mas_chess_save_selected:
    return sel_game[0]


#### DIALOGUE BLOCKS BELOW ####################################################

### Quicksave lost:
label mas_chess_dlg_qs_lost:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QS_LOST] += 1
        qs_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QS_LOST]

    call mas_chess_dlg_qs_lost_start

    if qs_gone_count == 2:
        call mas_chess_dlg_qs_lost_2

    elif qs_gone_count == 3:
        call mas_chess_dlg_qs_lost_3

    elif qs_gone_count % 5 == 0:
        call mas_chess_dlg_qs_lost_5r

    elif qs_gone_count % 7 == 0:
        call mas_chess_dlg_qs_lost_7r

    else:
        call mas_chess_dlg_qs_lost_gen

    return _return

# quicksave lost start
label mas_chess_dlg_qs_lost_start:
    m 2lksdlb "Uh, [player]...{w=0.5} It seems I messed up in saving our last game, and now I can't open it anymore."
    return

# generic quicksave lost statement
label mas_chess_dlg_qs_lost_gen:
    m 1lksdlc "I'm sorry..."
    m 3eksdla "Let's start a new game instead."
    return

# 2nd time quicksave lost statement
label mas_chess_dlg_qs_lost_2:
    m 1lksdld "I'm really, really sorry, [player]."
    m "I hope you can forgive me."
    show monika 1ekc
    pause 1.0
    m 1dsc "I'll make it up to you..."
    m 3eua "...by starting a new game!"
    return

# 3rd time quicksave lost statement
label mas_chess_dlg_qs_lost_3:
    m 1lksdlc "I'm so clumsy, [player]...{w=0.3} I'm sorry."
    m 3eksdla "Let's start a new game instead."
    return

# 5th time recurring quicksave lost statement
label mas_chess_dlg_qs_lost_5r:
    m 2esc "This has happened [qs_gone_count] times now..."
    m 2tsc "I wonder if this is a side effect of {cps=*0.75}{i}someone{/i}{/cps} trying to edit the saves.{w=1}.{w=1}."
    m 1esd "Anyway..."
    m "Let's start a new game."
    show monika 1esc
    return

# 7th time recurring quicksave lost statement
label mas_chess_dlg_qs_lost_7r:
    jump mas_chess_dlg_qs_lost_3

### quickfile lost
# main label for quickfile lost flow
label mas_chess_dlg_qf_lost:
    python:
        import store.mas_chess as mas_chess

    call mas_chess_dlg_qf_lost_start from _mas_chess_dqfls

    m "Did you mess with the saves, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you mess with the saves, [player]?{fast}"
        "[mas_chess.DLG_QF_LOST_OFCN_CHOICE]" if mas_chess.DLG_QF_LOST_OFCN_ENABLE:
            call mas_chess_dlg_qf_lost_ofcn_start

        "[mas_chess.DLG_QF_LOST_MAY_CHOICE]" if mas_chess.DLG_QF_LOST_MAY_ENABLE:
            call mas_chess_dlg_qf_lost_may_start

        "[mas_chess.DLG_QF_LOST_ACDNT_CHOICE]" if mas_chess.DLG_QF_LOST_ACDNT_ENABLE:
            call mas_chess_dlg_qf_lost_acdnt_start

    return _return

# intro to quickfile lost
label mas_chess_dlg_qf_lost_start:
    m 2lksdla "Well,{w=0.3} this is embarrassing."
    m "I could have sworn that we had an unfinished game, but I can't find the save file."
    return

## of course not flow
label mas_chess_dlg_qf_lost_ofcn_start:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN]

    if qf_gone_count == 3:
        call mas_chess_dlg_qf_lost_ofcn_3

    elif qf_gone_count == 4:
        call mas_chess_dlg_qf_lost_ofcn_4

    elif qf_gone_count == 5:
        call mas_chess_dlg_qf_lost_ofcn_5

    elif qf_gone_count >= 6:
        call mas_chess_dlg_qf_lost_ofcn_6

    else:
        call mas_chess_dlg_qf_lost_ofcn_gen

    return _return

# generic ofcnot monika
label mas_chess_dlg_qf_lost_ofcn_gen:
    m 1lksdlb "Ah, yeah. You wouldn't do that to me."
    m "I must have misplaced the save files."
    m 1lksdlc "Sorry, [player]."
    m "I'll make it up to you..."
    m 1eua "by starting a new game!"
    return

# 3rd time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_3:
    m 2esc "..."
    m "[player],{w=0.2} did you..."
    m 2dsc "Nevermind."
    m 1esc "Let's play a new game."
    return

# 4th time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_4:
    jump mas_chess_dlg_qf_lost_ofcn_3

# 5th time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_5:
    $ mas_loseAffection()
    m 2esc "..."
    m "[player],{w=0.2} this is happening way too much."
    m 2dsc "I really don't believe you this time."
    pause 2.0
    m 2esc "I hope you're not messing with me."
    m "..."
    m 1esc "Whatever.{w=0.5} Let's just play a new game."
    return

# 6th time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_6:
    # TODO we need to have a separate version of this event if your affection
    # is high enough. Basically you should only reach the bad end if
    # you've been a dick for a while
    # TODO: this makes sense compared to the go_ham event since
    # its just throwing away stuff instead of cheating
    # disable chess forever!
    python:
        mas_loseAffection(modifier=10)
        #NOTE: Chess is automatically locked due to its conditional. No need to manually lock it here
        mas_stripEVL("mas_unlock_chess")
        #Workaround to deal with peeople who havent seen the unlock chess label
        persistent._seen_ever["mas_unlock_chess"] = True

    m 2dfc "..."
    m 2efc "[player],{w=0.3} I don't believe you."
    m 2efd "If you're just going to throw away our chess games like that..."
    m 6wfw "Then I don't want to play chess with you anymore!"
    return True

## maybe monika flow
label mas_chess_dlg_qf_lost_may_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_MAYBE]

    if qf_gone_count == 2:
        call mas_chess_dlg_qf_lost_may_2 from _mas_chess_dlgqflostmay2

    elif qf_gone_count >= 3:
        call mas_chess_dlg_qf_lost_may_3 from _mas_chess_dlgqflostmay3

    else:
        call mas_chess_dlg_qf_lost_may_gen from _mas_chess_dlgqflostmaygen

    return _return

# generic maybe monika
# NOTE: we do a check for the file every line
label mas_chess_dlg_qf_lost_may_gen:
    m 2ekd "[player]!{w=0.2} I should have known you were just messing with me!"
    jump mas_chess_dlg_qf_lost_may_filechecker

# generic maybe monika, found file
label mas_chess_dlg_qf_lost_may_gen_found:
    m 2eua "Oh!"
    m 1hua "There's the save.{w=0.2} Thanks for putting it back, [player]."
    m 1eua "Now we can continue our game."
    return store.mas_chess.CHESS_GAME_CONT

# 2nd time maybe monika
label mas_chess_dlg_qf_lost_may_2:
    m 2ekd "[player]!{w=0.2} Stop messing with me!"
    jump mas_chess_dlg_qf_lost_may_filechecker

# 2nd time maybe monika, found file
label mas_chess_dlg_qf_lost_may_2_found:
    jump mas_chess_dlg_qf_lost_may_gen_found

# maybe monika file checking parts
label mas_chess_dlg_qf_lost_may_filechecker:
    $ import os
    $ import store.mas_chess as mas_chess
    $ game_file = mas_chess.loaded_game_filename

    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_qf_lost_may_gen_found

    m 1eka "Can you put the save back so we can play?"
    if os.access(game_file, os.F_OK):
        jump mas_chess_dlg_qf_lost_may_gen_found

    show monika 1eua

    # loop for about a minute and check for file xistence
    python:
        renpy.say(m, "I'll wait a minute...", interact=False)
        file_found = False
        seconds = 0
        while not file_found and seconds < 60:
            if os.access(game_file, os.F_OK):
                file_found = True
            else:
                renpy.pause(1.0, hard=True)
                seconds += 1

    if file_found:
        m 1hua "Yay!{w=0.2} Thanks for putting it back, [player]."
        m "Now we can continue our game."
        show monika 1eua
        return mas_chess.CHESS_GAME_CONT

    # else:
    m 1ekd "[player]..."
    m 1eka "That's okay. Let's just play a new game."
    return

# 3rd time maybe monika
label mas_chess_dlg_qf_lost_may_3:
    $ persistent._mas_chess_skip_file_checks = True

    m 2ekd "[player]! That's--"
    m 2dkc "..."
    m 1esa "...not a problem at all."
    m "I knew you were going to do this again..."
    m 1hub "...so I kept a backup of our save!"
    # TODO: wink here please
    m 1eua "You can't trick me anymore, [player]."
    m "Now let's continue our game."
    return store.mas_chess.CHESS_GAME_BACKUP

# maybe monika, but player removed the file again!
label mas_chess_dlg_qf_lost_may_removed:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection(modifier=0.5)

    m 2wfw "[player]!"
    m 2wfx "You removed the save again."
    pause 0.7
    m 2rfc "Let's just play chess at another time, then."
    return True

## Accident monika flow
label mas_chess_dlg_qf_lost_acdnt_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_ACDNT]

    if qf_gone_count == 2:
        call mas_chess_dlg_qf_lost_acdnt_2 from _mas_chess_dlgqflostacdnt2

    elif qf_gone_count >= 3:
        call mas_chess_dlg_qf_lost_acdnt_3 from _mas_chess_dlgqflostacdnt3

    else:
        call mas_chess_dlg_qf_lost_acdnt_gen from _mas_chess_dlgqflostacdntgen

    return _return

# generic accident monika
label mas_chess_dlg_qf_lost_acdnt_gen:
    m 1eka "[player]..."
    m "That's okay.{w=0.3} Accidents happen."
    m 1eua "Let's play a new game instead."
    return

# 2nd accident monika
label mas_chess_dlg_qf_lost_acdnt_2:
    m 1eka "Again? Don't be so clumsy, [player]."
    m 1hua "But that's okay."
    m "We'll just play a new game instead."
    show monika 1eua
    return

# 3rd accident monika
label mas_chess_dlg_qf_lost_acdnt_3:
    $ persistent._mas_chess_skip_file_checks = True

    m 1eka "I had a feeling this would happen again."
    m 3hub "So I kept a backup of our save!"
    m 1eua "Now we can continue our game."
    return store.mas_chess.CHESS_GAME_BACKUP

### quickfile edited
# main label for quickfile edited flow
label mas_chess_dlg_qf_edit:
    call mas_chess_dlg_qf_edit_start

    m 2ekc "Did you edit the save file?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you edit the save file?{fast}"
        "Yes.":
            call mas_chess_dlg_qf_edit_y_start
        "No.":
            call mas_chess_dlg_qf_edit_n_start

    return _return

# intro to quickfile edited
label mas_chess_dlg_qf_edit_start:
    m 2lksdlc "[player]..."
    return

## Yes Edit flow
label mas_chess_dlg_qf_edit_y_start:
    python:
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_YES]

    if qf_edit_count == 1:
        call mas_chess_dlg_qf_edit_y_1 from _mas_chess_dlgqfedity1

    elif qf_edit_count == 2:
        call mas_chess_dlg_qf_edit_y_2 from _mas_chess_dlgqfedity2

    else:
        call mas_chess_dlg_qf_edit_y_3 from _mas_chess_dlgqfedity3

    return _return

# first time yes edit
label mas_chess_dlg_qf_edit_y_1:
    m 2dsc "I'm disappointed in you."
    m 1euc "But I'm glad that you were honest with me."

    # we want a timed menu here. Let's give the player 5 seconds to say sorry
    show screen mas_background_timed_jump(5, "mas_chess_dlg_qf_edit_y_1n")
    menu:
        "I'm sorry.":
            hide screen mas_background_timed_jump
            # light affection boost for being honest
            $ mas_gainAffection(modifier=0.5)
            m 1hua "Apology accepted!"
            m 1eua "Luckily, I still remember a little bit of the last game, so we can continue it from there."
            return store.mas_chess.CHESS_GAME_BACKUP
        "...":
            label mas_chess_dlg_qf_edit_y_1n:
                hide screen mas_background_timed_jump
                m 1lfc "Since that game's been ruined, let's just play a new game."
            return
    return # just in case

# 2nd time yes edit
label mas_chess_dlg_qf_edit_y_2:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection(modifier=0.5)

    m 2dfc "I am incredibly disappointed in you."
    m 2rfc "I don't want to play chess right now."
    return True

# 3rd time yes edit
label mas_chess_dlg_qf_edit_y_3:
    $ mas_loseAffection()
    $ persistent._mas_chess_skip_file_checks = True

    m 2dsc "I'm not surprised..."
    m 2esc "But I am prepared."
    m "I kept a backup of our game just in case you did this again."
    m 1esa "Now let's finish this game."
    return store.mas_chess.CHESS_GAME_BACKUP

## No Edit flow
label mas_chess_dlg_qf_edit_n_start:
    python:
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO] += 1
        qf_edit_count = persistent._mas_chess_dlg_actions[mas_chess.QF_EDIT_NO]

    if qf_edit_count == 1:
        call mas_chess_dlg_qf_edit_n_1 from _mas_chess_dlgqfeditn1

    elif qf_edit_count == 2:
        call mas_chess_dlg_qf_edit_n_2 from _mas_chess_dlgqfeditn2

    else:
        call mas_chess_dlg_qf_edit_n_3 from _mas_chess_dlgqfeditn3

    return _return

# 1st time no edit
label mas_chess_dlg_qf_edit_n_1:
    $ mas_loseAffection()

    m 1ekc "I see."
    m "The save file looks different than how I last remembered it, but maybe that's just my memory failing me."
    m 1eua "Let's continue this game."
    return store.mas_chess.CHESS_GAME_FILE

# 2nd time no edit
label mas_chess_dlg_qf_edit_n_2:
    $ mas_loseAffection(modifier=2)

    m 1ekc "I see."
    m "..."
    m "Let's just continue this game."
    return store.mas_chess.CHESS_GAME_FILE

# 3rd time no edit
label mas_chess_dlg_qf_edit_n_3:
    $ mas_loseAffection(modifier=3)
    m 2dfc "[player]..."
    m 2dftdc "I kept a backup of our game.{w=0.5} I know you edited the save file."
    m 2dftsc "I just-"
    $ _history_list.pop()
    m 6ektsc "I just{fast} can't believe you would cheat and {i}lie{/i} to me."
    m 6rktsc "..."

    # THE ULTIMATE CHOICE
    show screen mas_background_timed_jump(3, "mas_chess_dlg_qf_edit_n_3n")
    menu:
        "I'm sorry.":
            hide screen mas_background_timed_jump
            # light affection boost for apologizing
            $ mas_gainAffection(modifier=0.5)
            call mas_chess_dlg_qf_edit_n_3_s from _mas_chess_dlgqfeditn3s

        "...":
            label mas_chess_dlg_qf_edit_n_3n:
                hide screen mas_background_timed_jump
                call mas_chess_dlg_qf_edit_n_3_n from _mas_chess_dlgqfeditn3n

    return _return

# 3rd time no edit, sorry
label mas_chess_dlg_qf_edit_n_3_s:
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    $ persistent._mas_chess_3_edit_sorry = True
    $ persistent._mas_chess_skip_file_checks = True

    show monika 6ektsc
    pause 1.0
    show monika 2ektsc
    pause 1.0
    m "I forgive you, [player], but please don't do this to me again."
    m 2lktsc "..."
    return store.mas_chess.CHESS_GAME_BACKUP

# 3rd time no edit, sorry, edit qs
label mas_chess_dlg_qf_edit_n_3_n_qs:
    python:
        persistent._mas_chess_timed_disable = datetime.datetime.now()
        mas_loseAffection()

    m 2dfc "[player]..."
    m 2efc "I see you've edited my backup saves."
    m 2lfc "If you want to be like that right now, then we'll play chess some other time."
    return True

# 3rd time no edit, no sorry
label mas_chess_dlg_qf_edit_n_3_n:
    python:
        # forever remember
        persistent._mas_chess_mangle_all = True
        persistent.autoload = "mas_chess_go_ham_and_delete_everything"

    # TODO: similar to chess disable, we need 2 versions of this. With a certain
    # amount of affection, you really should get a 2nd chance.
    # i think what we can do here is do a large subtract off affection
    # (maybe like -200/300 or something) and then if you are below a certain
    # amount then you get the bad end, otherwise we jump to the
    # 3rd time no edit, sorry label.
    # TODO: actually i'm not 100% sure on this, lets leave it up to debate rn
    # TODO: actaully, we should change some of this dialogue to make it more
    # obvious that the player violated trust
    # TODO: also we should like do something here where if the player
    #  qutis during this time, we delete or jump into some other flow
    m 6ektsc "I can't trust you anymore."
    m "Goodbye, [player].{nw}"

    # do some permanent stuff
label mas_chess_go_ham_and_delete_everything:
    python:
        import store.mas_chess as mas_chess
        import store._mas_root as mas_root
        import os

        # basedir
        gamedir = os.path.normcase(config.basedir + "/game/")

        # try deleting files
        for filename in mas_chess.del_files:
            try:
                os.remove(gamedir + filename)
            except:
                pass

        # now glitch a bunch of files
        for filename in mas_chess.gt_files:
            mas_root.mangleFile(gamedir + filename)

        # delete her character file
        try:
            os.remove(
                os.path.normcase(config.basedir + "/characters/monika.chr")
            )
        except:
            pass

        # delete persistent values
        # TODO: SUPER DANGEROUS, make backups before testing
        mas_root.resetPlayerData()

    jump _quit

### chess has ended dialogue
# monika won
label mas_chess_dlg_game_monika_win_end:
    m 2eua "Despite its simple rules, chess is a really intricate game."
    m 1eua "It's okay if you find yourself struggling at times."
    m 1hua "Remember, the important thing is to be able to learn from your mistakes."
    return

# monika lost
label mas_chess_dlg_game_monika_lose_end:
    m 2eub "It's amazing how much more I have to learn even now."
    m 2eua "I really don't mind losing as long as I can learn something."
    m 1hua "After all, the company is good."
    return

# quick version of game in progress
label mas_chess_dlg_game_in_progress_end_quick:
    m 1eua "Okay, [player], let's continue this game soon."
    return

#### end dialogue blocks ######################################################

# confirmation screen for chess
screen mas_chess_confirm():

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Are you sure you want to give up?"):
                style "confirm_prompt"
                text_color mas_globals.button_text_idle_color
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action Return(True)
                textbutton _("No") action Return(False)

# promotion screen for chess
screen mas_chess_promote(player_color):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    # get the correct image pieces for our color
    $ imagedict = store.getPieceImages(player_color)

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Choose one"):
                style "confirm_prompt"
                text_color mas_globals.button_text_idle_color
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 10

                imagebutton idle imagedict['q'] action Return('q')
                imagebutton idle imagedict['r'] action Return('r')
                imagebutton idle imagedict['n'] action Return('n')
                imagebutton idle imagedict['b'] action Return('b')

label mas_chess_promote_context(player_color):
    call screen mas_chess_promote(player_color)
    $ store.mas_chess.promote = _return
    return

#START: Chess related functions
init python:
    import chess
    import chess.pgn
    import collections
    import subprocess
    import platform
    import random
    import pygame
    import threading
    import StringIO

    import os
    import time

    #For the buttons
    import store.mas_ui as mas_ui

    ON_POSIX = 'posix' in sys.builtin_module_names

    def enqueue_output(out, queue, lock):
        for line in iter(out.readline, b''):
            lock.acquire()
            queue.appendleft(line)
            lock.release()
        out.close()

    def get_mouse_pos():
        vw = config.screen_width * 10000
        vh = config.screen_height * 10000
        pw, ph = renpy.get_physical_size()
        dw, dh = pygame.display.get_surface().get_size()
        mx, my = pygame.mouse.get_pos()

        # converts the mouse coordinates from pygame to physical size
        # NEEDED FOR UI SCALING OTHER THAN 100%
        mx = (mx * pw) / dw
        my = (my * ph) / dh

        r = None
        # this part calculates the "true" position
        # it can handle weirdly sized screens
        if vw / (vh / 10000) > pw * 10000 / ph:
            r = vw / pw
            my -= (ph - vh / r) / 2
        else:
            r = vh / ph
            mx -= (pw - vw / r) / 2

        newx = (mx * r) / 10000
        newy = (my * r) / 10000

        return (newx, newy)

    # only add chess folder if we can even do chess
    if mas_games.is_platform_good_for_chess():
        # first create the folder for this
        try:
            file_path = os.path.normcase(config.basedir + mas_chess.CHESS_SAVE_PATH)

            if not os.access(file_path, os.F_OK):
                os.mkdir(file_path)
            mas_chess.CHESS_SAVE_PATH = file_path

        except:
            store.mas_utils.writelog("Chess game folder could not be created '{0}'\n".format(file_path))

    def getPieceImages(player_color):

        imagedict = {}
        piecelist = ["q","r","n","b"]

        jy = 1 if player_color else 0

        for piece in piecelist:

            jx = MASChessDisplayableBase.VECTOR_PIECE_POS[piece.upper()]

            pieceimage = LiveCrop((
                jx * MASChessDisplayableBase.PIECE_WIDTH,
                jy * MASChessDisplayableBase.PIECE_HEIGHT,
                MASChessDisplayableBase.PIECE_WIDTH,
                MASChessDisplayableBase.PIECE_HEIGHT
                ),
                MASChessDisplayableBase.PIECES_IMAGE
            )
            imagedict[piece] = pieceimage

        return imagedict

    #START: DISPLAYABLES AND RELATED CLASSES
    class MASChessDisplayableBase(renpy.Displayable):
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )

        #Put the static vars up here
        MONIKA_WAITTIME = 50
        MONIKA_DEPTH = 1
        MONIKA_OPTIMISM = 33
        MONIKA_THREADS = 1

        START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        PIECES_IMAGE = Image("mod_assets/games/chess/chess_pieces.png")
        BOARD_IMAGE = Image("mod_assets/games/chess/chess_board.png")
        PIECE_HIGHLIGHT_RED_IMAGE = Image("mod_assets/games/chess/piece_highlight_red.png")
        PIECE_HIGHLIGHT_GREEN_IMAGE = Image("mod_assets/games/chess/piece_highlight_green.png")
        PIECE_HIGHLIGHT_YELLOW_IMAGE = Image("mod_assets/games/chess/piece_highlight_yellow.png")
        PIECE_HIGHLIGHT_MAGENTA_IMAGE = Image("mod_assets/games/chess/piece_highlight_magenta.png")
        MOVE_INDICATOR_PLAYER = Image("mod_assets/games/chess/move_indicator_player.png")
        MOVE_INDICATOR_MONIKA = Image("mod_assets/games/chess/move_indicator_monika.png")

        VECTOR_PIECE_POS = {
            'K': 0,
            'Q': 1,
            'R': 2,
            'B': 3,
            'N': 4,
            'P': 5
        }

        # The sizes of some of the images.
        BOARD_BORDER_WIDTH = 15
        BOARD_BORDER_HEIGHT = 15
        PIECE_WIDTH = 57
        PIECE_HEIGHT = 57
        BOARD_WIDTH = BOARD_BORDER_WIDTH * 2 + PIECE_WIDTH * 8
        BOARD_HEIGHT = BOARD_BORDER_HEIGHT * 2 + PIECE_HEIGHT * 8
        INDICATOR_WIDTH = 60
        INDICATOR_HEIGHT = 96
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        BUTTON_X_SPACING = 10
        BUTTON_Y_SPACING = 10

        # calculate positions
        DRAWN_BOARD_X = int((1280 - BOARD_WIDTH) / 1.5)
        DRAWN_BOARD_Y = int((720 - BOARD_HEIGHT) / 3)
        DRAWN_BUTTON_X = DRAWN_BOARD_X + BUTTON_X_SPACING

        DRAWN_BUTTON_Y_MID = (BUTTON_HEIGHT + DRAWN_BOARD_Y)
        DRAWN_BUTTON_Y_BOT = 720 - (BUTTON_HEIGHT + DRAWN_BUTTON_Y_MID)
        DRAWN_BUTTON_Y_TOP = DRAWN_BUTTON_Y_MID - BUTTON_Y_SPACING - BUTTON_HEIGHT

        PROMOLIST = ["q","r","n","b","r","k"]

        #Button handling bits
        def __init__(
            self,
            player_color,
            pgn_game=None,
            starting_fen=None,
            buttons=None,
            player_move_prompt=None
        ):
            """
            MASChessDisplayableBase constructor

            IN:
                player_color - color the player is playing
                pgn_game - previous game to load (chess.pgn.Game)
                    if a starting_fen is provided alongside this, the fen is ignored
                    (Default: None)
                starting_fen - starting fen to use if starting a custom scenario
                    NOTE: This is not verified for validity
                    (Default: None)
                buttons - Dict representing button data
                    if not provided, no buttons will be controlled internally within the functions in this class
                    key:
                        variable name for the button
                    value:
                        conditional for the button to be active
                        NOTE: Not verified for validity
                    (Default: None)
                player_move_prompt - prompt to use to indicate player move
                    If not provided, no player prompt will be used
                    (Default: None)

            NOTE: Requires the following to be implemented for buttons to show:
                self._visible_buttons - list of MASButtonDisplayables which should be displayed during the game
                self._visible_buttons_winner - list of MASButtonDisplayables which should be displayed post game

            NOTE: The following function MUST be implemented in a class which inherits this:
                self.check_buttons
            """
            renpy.Displayable.__init__(self)

            #Some core vars
            self.num_turns = 0
            self.player_move_stack = list()
            self.monika_move_stack = list()

            #Store the buttons as we'll need to use this later
            self.buttons = dict() if buttons is None else buttons

            self.player_move_prompt = player_move_prompt
            #Now handle setup for potential engine
            self.additional_setup()

            #Separate handling of music menu open because the songs store is for main renpy interaction
            self.music_menu_open = False

            # Board for integration with python-chess.
            self.board = None

            #If we're basing off an existing pgn, let's load the relevant data
            if pgn_game:
                # load this game into the board, push turns
                self.board = pgn_game.board()
                for move in pgn_game.main_line():
                    self.board.push(move)

                # whose turn?
                self.current_turn = self.board.turn

                # colors?
                self.player_color = mas_chess._get_player_color(pgn_game)

                # last move
                last_move = self.board.peek().uci()
                self.last_move_src = (
                    ord(last_move[0]) - ord('a'),
                    ord(last_move[1]) - ord('1')
                )
                self.last_move_dst = (
                    ord(last_move[2]) - ord('a'),
                    ord(last_move[3]) - ord('1')
                )

                # and finally the fullmove number
                self.num_turns = self.board.fullmove_number

            else:
                #Start off with traditional board, or initialize with the starting fen if using a custom scenario
                self.board = chess.Board(fen=starting_fen) if starting_fen is not None else chess.Board()

                # stuff we need to save to the board
                self.today_date = datetime.date.today().strftime("%Y.%m.%d")

                #New board, so white goes first
                self.current_turn = chess.WHITE

                # setup player color
                self.player_color = player_color

                # setup last move
                self.last_move_src = None
                self.last_move_dst = None

            self.selected_piece = None
            self.possible_moves = set([])
            self.winner = None
            self.is_game_over = False

            # setup a pgn (could be None, in which case we are playing a fresh game)
            self.pgn_game = pgn_game

            #If it's Monika's turn, send her the board positions so that she can start analyzing.
            if not self.is_player_turn():
                self.start_monika_analysis()

            #Set buttons
            self.set_button_states()

        def __del__(self):
            self.stockfish.stdin.close()
            self.stockfish.wait()

        #START: NON-IMPLEMENTED FUNCTIONS
        def additional_setup():
            """
            Additional setup instructions for the displayable

            Implement to use an engine or add some other setup

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            It is only required to initialize a chess engine
            """
            return

        def start_monika_analysis(self):
            """
            Starts Monika's analysis of the board

            Implement to allow a chess engine to analyze the board and begin predicting moves

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            It is only required if and only if we want Monika to play using an engine rather than manually queued moves
            """
            return None

        def poll_monika_move(self):
            """
            Polls for a Monika move

            Implement to automate Monika's moves (use for an engine)

            NOTE: IMPLEMENTATION OF THIS IS OPTIONAL.
            It is only required if and only if we want Monika to play using an engine rather than manually queued moves
            """
            return None

        def check_buttons(self, ev, x, y, st):
            """
            Runs button checks/functions if pressed

            Should be implemnted as necessary for provided buttons

            NOTE: REQUIRED for displayables with buttons added, otherwise their actions will never execute
            """
            raise NotImplementedError("Function 'check_buttons' was not implemented.")

        #END: Non-implemented functions
        def handle_monika_move(self):
            """
            Handles Monika's move

            Re-implement as necessary to handle different contexts
            """
            # Poll Monika for moves if it's her turn
            if not self.is_game_over and not self.is_player_turn():
                #NOTE: This is done in the case of a more tutorial like design, in which moves are pushed through dialogue
                #Rather than by stockfish's pick

                #Queue a Moni move if this is implemented
                moni_move = self.poll_monika_move()
                if moni_move:
                    self.queue_monika_move(moni_move)

                if self.monika_move_stack:
                    #Grab the first item from the stack and push it
                    monika_move = self.monika_move_stack.pop(0)

                    if monika_move is not None:
                        #Now verify legality
                        monika_move_check = chess.Move.from_uci(monika_move)

                        if self.board.is_legal(monika_move_check):
                            self.last_move_src = (ord(monika_move[0]) - ord('a'), ord(monika_move[1]) - ord('1'))
                            self.last_move_dst = (ord(monika_move[2]) - ord('a'), ord(monika_move[3]) - ord('1'))
                            time.sleep(1.5)
                            self.board.push_uci(monika_move)

                            #'not self.current_turn' is the equivalent of saying the current turn is Black's turn, as chess.BLACK is False
                            if not self.current_turn:
                                self.num_turns += 1

                            #It's player's turn
                            self.current_turn = self.player_color
                            self.is_game_over = self.board.is_game_over()

                            #Set the buttons
                            self.set_button_states()

        def handle_player_move(self):
            """
            Handles the player's move

            Re-implement as necessary to modify for differing contexts
            """
            px, py = self.get_piece_pos()

            move_str = None

            if self.player_move_stack:
                move_str = self.player_move_stack.pop(0)

            elif px is not None and py is not None and self.selected_piece is not None:
                move_str = self.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) + self.coords_to_uci(px, py)
                piece_str = self.board.piece_at(self.selected_piece[1] * 8 + self.selected_piece[0]).symbol()

                #Promote if needed
                if piece_str.lower() == 'p' and (py == 0 or py == 7):
                    renpy.call_in_new_context("mas_chess_promote_context", self.player_color)
                    move_str += store.mas_chess.promote

            if move_str is None:
                return

            if chess.Move.from_uci(move_str) in self.possible_moves:
                #Add this undo
                self.move_history.append(self.board.fen())
                self.last_move_src = self.selected_piece
                self.last_move_dst = (px, py)
                self.queue_monika_move(move_str)
                self.board.push_uci(move_str)
                self.is_game_over = self.board.is_game_over()

                #'not self.current_turn' is the equivalent of current_turn == chess.BLACK, as chess.BLACK is False
                if not self.current_turn:
                    self.num_turns += 1

                self.current_turn = not self.current_turn

                if not self.is_game_over:
                    self.set_button_states()
                    self.start_monika_analysis()

        def set_button_states(self):
            """
            Sets the button states according to their conditionals.

            NOTE: CONDITIONALS ARE NOT VALIDATED FOR ERRORS
            """
            for button_obj_name, button_data in self.buttons.iteritems():
                if eval(button_data["conditional"], self.__dict__):
                    self.__dict__[button_obj_name].enable()
                else:
                    self.__dict__[button_obj_name].disable()

        def check_winner(self, current_move):
            if self.board.is_game_over():
                if self.board.result() == '1/2-1/2':
                    self.winner = None
                else:
                    self.winner = current_move

        def queue_player_move(self, move):
            """
            Queues a move to the player move stack

            IN:
                move in the form
            """
            self.player_move_stack.append(move)

        def queue_monika_move(self, move):
            """
            Queues a move to the Monika move stack

            IN:
                move in the form
            """
            self.monika_move_stack.append(move)

        def is_player_turn(self):
            """
            Checks if it's currently the player's turn
            """
            return self.player_color == self.current_turn

        # Renders the board, pieces, etc.
        def render(self, width, height, st, at):
            #SETUP
            def get_piece_render_for_letter(letter):
                """
                Gets the piece render for the given letter

                IN:
                    letter - representing the piece to get

                OUT:
                    subsurface representing the piece images
                """
                jy = 0 if letter.islower() else 1
                jx = MASChessDisplayableBase.VECTOR_PIECE_POS[letter.upper()]

                return pieces.subsurface((
                    jx * MASChessDisplayableBase.PIECE_WIDTH,
                    jy * MASChessDisplayableBase.PIECE_HEIGHT,
                    MASChessDisplayableBase.PIECE_WIDTH,
                    MASChessDisplayableBase.PIECE_HEIGHT
                ))

            def render_move(move):
                """
                Renders the move

                IN:
                    move - two length string representing the move
                """
                if move is not None and ix_orig == move[0] and iy_orig == move[1]:
                    renderer.blit(
                        highlight_magenta if self.is_player_turn() else highlight_green,
                        (x, y)
                    )


            #The Render object we'll be drawing into.
            renderer = renpy.Render(width, height)

            # Prepare the board as a renderer.
            board = renpy.render(MASChessDisplayableBase.BOARD_IMAGE, 1280, 720, st, at)

            # Prepare the pieces vector as a renderer.
            pieces = renpy.render(MASChessDisplayableBase.PIECES_IMAGE, 1280, 720, st, at)

            # Prepare the highlights as a renderers.
            highlight_red = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_RED_IMAGE, 1280, 720, st, at)
            highlight_green = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_GREEN_IMAGE, 1280, 720, st, at)
            highlight_yellow = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_YELLOW_IMAGE, 1280, 720, st, at)
            highlight_magenta = renpy.render(MASChessDisplayableBase.PIECE_HIGHLIGHT_MAGENTA_IMAGE, 1280, 720, st, at)

            # get the mouse pos
            mx, my = get_mouse_pos()

            #START: Turn/move handling
            #Firstly, handle Monika's move
            #We functionalize this such that it can be overridden under normal game circumstances
            self.handle_monika_move()

            #Since different buttons show during the game vs post game, we'll sort out what's shown here
            visible_buttons = list()
            if self.is_game_over:
                # point to the correct visible button list
                visible_buttons = [
                    (b.render(width, height, st, at), b.xpos, b.ypos)
                    for b in self._visible_buttons_winner
                ]

            else:
                # otherwise use the regular buttons list
                visible_buttons = [
                    (b.render(width, height, st, at), b.xpos, b.ypos)
                    for b in self._visible_buttons
                ]

            #(Re)draw the board.
            renderer.blit(board, (MASChessDisplayableBase.DRAWN_BOARD_X, MASChessDisplayableBase.DRAWN_BOARD_Y))
            indicator_position = (
                int((width - MASChessDisplayableBase.INDICATOR_WIDTH) / 2 + MASChessDisplayableBase.BOARD_WIDTH / 2 + 50),
                int((height - MASChessDisplayableBase.INDICATOR_HEIGHT) / 2)
            )

            # Draw the move indicator
            renderer.blit(
                renpy.render(
                    (
                        MASChessDisplayableBase.MOVE_INDICATOR_PLAYER
                        if self.is_player_turn() else
                        MASChessDisplayableBase.MOVE_INDICATOR_MONIKA
                    ),
                    1280, 720, st, at),
                indicator_position
            )

            #Draw the buttons
            for b in visible_buttons:
                renderer.blit(b[0], (b[1], b[2]))

            #Draw the pieces on the Board renderer.
            for ix in range(8):
                for iy in range(8):
                    iy_orig = iy
                    ix_orig = ix

                    #White
                    if self.player_color:
                        iy = 7 - iy

                    #Black
                    else:
                        #Black player should be reversed X
                        ix = 7 - ix

                    x = int(
                        (width - (MASChessDisplayableBase.BOARD_WIDTH - MASChessDisplayableBase.BOARD_BORDER_WIDTH * 2)) / 1.5
                        + ix * MASChessDisplayableBase.PIECE_WIDTH
                    )

                    y = int(
                        (height - (MASChessDisplayableBase.BOARD_HEIGHT - MASChessDisplayableBase.BOARD_BORDER_HEIGHT * 2)) / 3
                        + iy * MASChessDisplayableBase.PIECE_HEIGHT
                    )

                    render_move(self.last_move_src)
                    render_move(self.last_move_dst)

                    # Take care not to render the selected piece twice.
                    if (
                        self.selected_piece is not None
                        and ix_orig == self.selected_piece[0]
                        and iy_orig == self.selected_piece[1]
                    ):
                        renderer.blit(highlight_green, (x, y))
                        continue

                    piece = self.board.piece_at(iy_orig * 8 + ix_orig)

                    possible_move_str = None
                    blit_rendered = False

                    if self.possible_moves:
                        possible_move_str = "{0}{1}".format(
                            MASChessDisplayableBase.coords_to_uci(self.selected_piece[0], self.selected_piece[1]),
                            MASChessDisplayableBase.coords_to_uci(ix_orig, iy_orig)
                        )

                        if chess.Move.from_uci(possible_move_str) in self.possible_moves:
                            renderer.blit(highlight_yellow, (x, y))
                            blit_rendered = True

                        # force checking for promotion
                        if not blit_rendered and (iy == 0 or iy == 7):
                            index = 0
                            while (not blit_rendered and index < len(MASChessDisplayableBase.PROMOLIST)):
                                if (
                                    chess.Move.from_uci(possible_move_str + MASChessDisplayableBase.PROMOLIST[index])
                                    in self.possible_moves
                                ):
                                    renderer.blit(highlight_yellow, (x, y))
                                    blit_rendered = True

                                index += 1

                    if piece is None:
                        continue

                    if (
                        self.is_player_turn()
                        and mx >= x and mx < x + MASChessDisplayableBase.PIECE_WIDTH
                        and my >= y and my < y + MASChessDisplayableBase.PIECE_HEIGHT
                        and (
                            (MASChessDisplayableBase.piece_is_white(piece) and self.player_color)
                            or (not MASChessDisplayableBase.piece_is_white(piece) and not self.player_color)
                        )
                        and self.selected_piece is None
                        and not self.is_game_over
                    ):
                        renderer.blit(highlight_green, (x, y))

                    #Winner check
                    if self.is_game_over:
                        result = self.board.result()

                        # black won
                        if str(piece) == "K" and result == "0-1":
                            renderer.blit(highlight_red, (x, y))

                        # white won
                        elif str(piece) == "k" and result == "1-0":
                            renderer.blit(highlight_red, (x, y))

                    renderer.blit(get_piece_render_for_letter(str(piece)), (x, y))


            if self.is_player_turn() and not self.is_game_over:
                # Display the indication that it's the player's turn
                #prompt = renpy.render(MASChessDisplayableBase.PLAYER_MOVE_PROMPT, 1280, 720, st, at)
                if self.player_move_prompt and not renpy.get_screen("say"):
                    renpy.say(m, self.player_move_prompt, interact=False)
                    _history_list.pop()

                #pw, ph = prompt.get_size()
                #bh = (height - MASChessDisplayableBase.BOARD_HEIGHT) / 2
                #renderer.blit(prompt, (int((width - pw) / 2), int(MASChessDisplayableBase.BOARD_HEIGHT + bh + (bh - ph) / 2)))

            if self.selected_piece is not None:
                # Draw the selected piece.
                piece = self.board.piece_at(self.selected_piece[1] * 8 + self.selected_piece[0])
                #assert piece is not None
                px, py = get_mouse_pos()
                px -= MASChessDisplayableBase.PIECE_WIDTH / 2
                py -= MASChessDisplayableBase.PIECE_HEIGHT / 2
                renderer.blit(get_piece_render_for_letter(str(piece)), (px, py))

            # Ask that we be re-rendered ASAP, so we can show the next frame.
            renpy.redraw(self, 0)

            # Return the Render object.
            return renderer

        # Handles events.
        def event(self, ev, x, y, st):
            #Are we in mouse button things
            if ev.type in self.MOUSE_EVENTS:
                #Run button checks in a function which needs to be implemented
                ret_value = self.check_buttons(ev, x, y, st)

                if ret_value is not None:
                    return ret_value

            # Mousebutton down == possibly select the piece to move
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # continue
                px, py = self.get_piece_pos()
                if (
                    self.is_player_turn()
                    and px is not None
                    and py is not None
                    and self.board.piece_at(py * 8 + px) is not None
                    and (
                        (MASChessDisplayableBase.piece_is_white(self.board.piece_at(py * 8 + px))
                        and self.player_color)
                        or (not MASChessDisplayableBase.piece_is_white(self.board.piece_at(py * 8 + px))
                        and not self.player_color)
                    )
                ):

                    piece = str(self.board.piece_at(py * 8 + px))

                    self.possible_moves = self.board.legal_moves
                    self.selected_piece = (px, py)

            # Mousebutton up == possibly release the selected piece
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                self.handle_player_move()

                self.selected_piece = None
                self.possible_moves = set([])

            # KEYMAP workarounds:
            if ev.type == pygame.KEYUP:
                # music menu // muting
                if ev.key == pygame.K_m:
                    # muting
                    if ev.mod & pygame.KMOD_SHIFT:
                        mute_music()

                    elif not self.music_menu_open:
                        self.music_menu_open = True
                        select_music()

                    else: # the menu is already open
                        self.music_menu_open = False

                # volume increase
                if ev.key in [pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS]:
                    inc_musicvol()

                # volume decrease
                if ev.key in [pygame.K_MINUS, pygame.K_UNDERSCORE, pygame.K_KP_MINUS]:
                    dec_musicvol()

            raise renpy.IgnoreEvent()

        def get_piece_pos(self):
            """
            Gets the piece position of the current piece held by the mouse

            OUT:
                Tuple of coordinates (x, y) marking where the piece is
            """
            mx, my = get_mouse_pos()
            mx -= (1280 - (MASChessDisplayableBase.BOARD_WIDTH - MASChessDisplayableBase.BOARD_BORDER_WIDTH * 2)) / 2
            my -= (720 - (MASChessDisplayableBase.BOARD_HEIGHT - MASChessDisplayableBase.BOARD_BORDER_HEIGHT * 2)) / 2
            px = mx / MASChessDisplayableBase.PIECE_WIDTH
            py = my / MASChessDisplayableBase.PIECE_HEIGHT

            #White
            if self.player_color:
                py = 7 - py

            #Black
            else:
                #Black player should be reversed X
                px = 7 - px

            if py >= 0 and py < 8 and px >= 0 and px < 8:
                return (px, py)

            return (None, None)

        @staticmethod
        def piece_is_white(Piece):
            """
            Checks if the given piece is white

            IN:
                Piece - chess.Piece object to test

            OUT:
                True if piece is white, False otherwise
            """
            #Nonecheck for safety
            if Piece is None:
                return False
            #Otherwise we'll return the color
            return Piece.color

        @staticmethod
        def coords_to_uci(x, y):
            """
            Converts board coordinates to a uci move

            IN:
                x - x co-ord of the piece
                y - y co-ord of the piece

            OUT:
                the move represented in the uci form
            """
            x = chr(x + ord('a'))
            y += 1
            return "{0}{1}".format(x, y)

    class MASPiece(chess.Piece):
        """
        MASChessPiece

        An extension class of chess.Piece which also holds piece location in addition to color and symbol

        PROPERTIES:
            color - Color of the piece:
                True - white
                False - black
            symbol - letter symbol representing the piece. If capital, the piece is white
            posX - x position for this piece on the board
            posY - y position for this piece on the board
        """
        def __init__(
            self,
            color,
            symbol,
            posX,
            posY,
        ):
            """
            MAS Chess piece constructor

            IN:
                color - Color of the piece:
                    True - white
                    False - black
                symbol - letter symbol representing the piece. If capital, the piece is white
                posX - x position for this piece on the board
                posY - y position for this piece on the board
            """
            super(MASPiece, self).__init__(color, symbol)
            self.posX = posX
            self.posY = posY

        @staticmethod
        def fromPiece(piece, posX, posY):
            """
            Initializes a MASPiece from a chess.Piece object

            IN:
                piece - piece to base the MASPiece off of
                posX - x position of this piece
                posY - y position of this piece

            OUT:
                MASPiece
            """
            return MASPiece(piece.color, piece.symbol, posX, posY)

    class MASChessDisplayable(MASChessDisplayableBase):
        def __init__(
            self,
            player_color,
            pgn_game=None,
            starting_fen=None,
            practice_mode=False
        ):

            self.practice_mode = practice_mode
            self.undo_count = 0
            self.move_history = list()
            self.surrendered = False
            self.starting_fen = starting_fen

            #Init the 4 buttons
            self._button_save = MASButtonDisplayable.create_stb(
                _("Save"),
                True,
                MASChessDisplayableBase.DRAWN_BUTTON_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_TOP,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            self._button_giveup = MASButtonDisplayable.create_stb(
                _("Surrender"),
                True,
                MASChessDisplayableBase.DRAWN_BUTTON_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_MID,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            self._button_done = MASButtonDisplayable.create_stb(
                _("Done"),
                False,
                MASChessDisplayableBase.DRAWN_BUTTON_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_MID,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            self._button_undo = MASButtonDisplayable.create_stb(
                _("Undo"),
                True,
                MASChessDisplayableBase.DRAWN_BUTTON_X,
                MASChessDisplayableBase.DRAWN_BUTTON_Y_BOT,
                MASChessDisplayableBase.BUTTON_WIDTH,
                MASChessDisplayableBase.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            #Setup the visible buttons list
            self._visible_buttons = [
                self._button_save,
                self._button_undo,
                self._button_giveup
            ]

            self._visible_buttons_winner = [
                self._button_done
            ]

            #Init the base displayable
            super(MASChessDisplayable, self).__init__(
                player_color,
                pgn_game,
                starting_fen,
                buttons={
                    "_button_save": {
                        "conditional": (
                            "not is_game_over "
                            "and player_color == current_turn "
                            "and board.fullmove_number > 1"
                        )
                    },
                    "_button_giveup": {
                        "conditional": (
                            "not is_game_over "
                            "and player_color == current_turn "
                            "and board.fullmove_number > 1"
                        )
                    },
                    "_button_done": {
                        "conditional": "is_game_over is not None"
                    },
                    "_button_undo": {
                        "conditional": (
                            "not is_game_over "
                            "and practice_mode "
                            "and player_color == current_turn "
                            "and board.fullmove_number > 0 "
                            "and move_history"
                        )
                    }
                },
                player_move_prompt="It's your turn, [player]!"
            )

        def poll_monika_move(self):
            """
            Polls stockfish for a move for Monika to make

            OUT:
                move - representing the best move stockfish found
            """
            self.lock.acquire()
            res = None
            while self.queue:
                line = self.queue.pop()
                match = re.match(r"^bestmove (\w+)", line)
                if match:
                    res = match.group(1)
            self.lock.release()
            return res

        def start_monika_analysis(self):
            """
            Starts Monika's analysis of the board
            """
            self.stockfish.stdin.write("position fen {0}\n".format(self.board.fen()))
            self.stockfish.stdin.write("go depth {0}\n".format(persistent._mas_chess_difficulty.values()[0]))
            self.stockfish.stdin.write("go movetime {0}\n".format(self.MONIKA_WAITTIME))

        def additional_setup(self):
            """
            Additional stockfish setup to get the game going using it as Monika's engine
            """
            # Stockfish engine provides AI for the game.
            def open_stockfish(path, startupinfo=None):
                """
                Runs stockfish

                IN:
                    path - filepath to the stockfish application
                    startupinfo - startup flags
                """
                return subprocess.Popen(
                    os.path.join(renpy.config.gamedir, path).replace('\\', '/'),
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    startupinfo=startupinfo
                )

            # Launch the appropriate version based on the architecture and OS.
            if not mas_games.is_platform_good_for_chess():
                # This is the last-resort check, the availability of the chess game should be checked independently beforehand.
                renpy.jump("mas_chess_cannot_work_embarrassing")

            is_64_bit = sys.maxsize > 2**32

            if renpy.windows:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                self.stockfish = open_stockfish(
                    'mod_assets/games/chess/stockfish_8_windows_x{0}.exe'.format("64" if is_64_bit else "32"),
                    startupinfo
                )

            elif is_64_bit:
                fp = "mod_assets/games/chess/stockfish_8_{0}_x64".format("linux" if renpy.linux else "macosx")

                os.chmod(config.basedir + "/game/".format(fp), 0755)
                self.stockfish = open_stockfish(fp)

            #Set Monika's parameters
            self.stockfish.stdin.write("setoption name Skill Level value {0}\n".format(persistent._mas_chess_difficulty.keys()[0]))
            self.stockfish.stdin.write("setoption name Contempt value {0}\n".format(self.MONIKA_OPTIMISM))
            self.stockfish.stdin.write("setoption name Ponder value False\n")

            #And set up facilities for asynchronous communication
            self.queue = collections.deque()
            self.lock = threading.Lock()
            thrd = threading.Thread(target=enqueue_output, args=(self.stockfish.stdout, self.queue, self.lock))
            thrd.daemon = True
            thrd.start()

        def check_buttons(self, ev, x, y, st):
            """
            Runs button checks/functions if pressed
            """
            # inital check for winner
            if self.is_game_over:
                if self._button_done.event(ev, x, y, st):
                    # user clicks Done
                    return self._quitPGN(False)

            # inital check for buttons
            elif self.is_player_turn():
                if self._button_save.event(ev, x, y, st):
                    # user wants to save this game
                    return self._quitPGN(False)

                elif self._button_undo.event(ev, x, y, st):
                    #user wants to undo the last move
                    #NOTE: While the chess.Board object has a pop function, we cannot use it here due to the nature of saving these as
                    #pgn files. As such we pop somewhat inefficiently, but we do it such that the fen can always be used to restore
                    last_move_fen = self.move_history.pop(-1)

                    #Remove the last move since we've undone
                    old_board = self.board
                    old_board.move_stack = old_board.move_stack[:len(old_board.move_stack)-2]
                    old_board.stack = old_board.stack[:len(old_board.stack)-2]

                    #Update the board to the undo
                    self.board = chess.Board(fen=last_move_fen)

                    #Now transfer the move data
                    self.board.move_stack = old_board.move_stack
                    self.board.stack = old_board.stack
                    self.board.fullmove_number = old_board.fullmove_number - 1

                    #Redraw the board and increment the undo counter
                    renpy.redraw(self, 0)
                    self.undo_count += 1

                    self.set_button_states()
                    return None


                elif self._button_giveup.event(ev, x, y, st):
                    renpy.call_in_new_context("mas_chess_confirm_context")
                    if mas_chess.quit_game:
                        #user wishes to surrender
                        return self._quitPGN(True)

        def _quitPGN(self, giveup):
            """
            Generates a pgn of the board, and depending on if we are
            doing previous game or not, does appropriate header
            setting

            IN:
                giveup - True if the player surrendered, False otherwise

            RETURNS: tuple of the following format:
                [0]: chess.pgn.Game object of this game
                [1]: True if monika won, False if not
                [2]: True if player gaveup, False otherwise
                [3]: number of turns of this game
            """
            new_pgn = chess.pgn.Game.from_board(self.board)

            if giveup:
                #Player is playing white
                if self.player_color:
                    new_pgn.headers["Result"] = "0-1"
                #Player is playing black
                else:
                    new_pgn.headers["Result"] = "1-0"

            # monika's ingame name will be her twitter handle
            #Player plays white
            if self.player_color:
                new_pgn.headers["White"] = persistent.playername
                new_pgn.headers["Black"] = mas_monika_twitter_handle

            #Player plays black
            else:
                new_pgn.headers["White"] = mas_monika_twitter_handle
                new_pgn.headers["Black"] = persistent.playername

            # date, site, and fen
            new_pgn.headers["Site"] = "MAS"
            new_pgn.headers["Date"] = datetime.date.today().strftime("%Y.%m.%d")
            new_pgn.headers["FEN"] = self.starting_fen if self.starting_fen is not None else MASChessDisplayableBase.START_FEN
            new_pgn.headers["SetUp"] = "1"
            new_pgn.headers["Practice"] = self.practice_mode
            new_pgn.headers["MoveHist"] = self.move_history
            new_pgn.headers["UndoCount"] = self.undo_count

            return (
                new_pgn,
                (
                    (new_pgn.headers["Result"] == "1-0" and new_pgn.headers["White"] == mas_monika_twitter_handle)
                    or (new_pgn.headers["Result"] == "0-1" and new_pgn.headers["Black"] == mas_monika_twitter_handle)
                ),
                giveup,
                self.board.fullmove_number
            )
