
# we now will keep track of player wins / losses/ draws/ whatever
default persistent._mas_chess_stats = {"wins": 0, "losses": 0, "draws": 0}

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

define mas_chess.CHESS_SAVE_PATH = "/chess_games/"
define mas_chess.CHESS_SAVE_EXT = ".pgn"
define mas_chess.CHESS_SAVE_NAME = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789"
define mas_chess.CHESS_PROMPT_FORMAT = "{0} | {1} | Turn: {2} | You: {3}"

# mass chess store
init 1 python in mas_chess:
    import os
    import chess.pgn

    # if this is true, we quit game (workaround for confirm screen)
    quit_game = False

    # relative chess directory
    REL_DIR = "chess_games/"

    # other mas constants (menu related)
    CHESS_MENU_X = 680
    CHESS_MENU_Y = 40
    CHESS_MENU_W = 560
    CHESS_MENU_H = 640
    CHESS_MENU_XALIGN = -0.05
    CHESS_MENU_AREA = (CHESS_MENU_X, CHESS_MENU_Y, CHESS_MENU_W, CHESS_MENU_H)

    CHESS_MENU_NEW_GAME_VALUE = "NEWGAME"
    CHESS_MENU_NEW_GAME_ITEM = (
        "Play New Game",
        CHESS_MENU_NEW_GAME_VALUE,
        True,
        False
    )

    CHESS_MENU_FINAL_VALUE = "NONE"
    CHESS_MENU_FINAL_ITEM = (
        "Nevermind",
        CHESS_MENU_FINAL_VALUE,
        False,
        False,
        20
    )

    CHESS_MENU_WAIT_VALUE = "MATTE"
    CHESS_MENU_WAIT_ITEM = (
        "I can't make this decision right now...",
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
    DLG_QF_LOST_OFCN_CHOICE = "Of course not!"

    # maybe
    DLG_QF_LOST_MAY_ENABLE = True
    DLG_QF_LOST_MAY_CHOICE = "Maybe..."

    # accident
    DLG_QF_LOST_ACDNT_ENABLE = True
    DLG_QF_LOST_ACDNT_CHOICE = "It was an accident!"

    ## if player is locked out of chess
    DLG_CHESS_LOCKED = "mas_chess_dlg_chess_locked"

    # base part of label for variable chess strength when monika wins
    DLG_MONIKA_WIN_BASE = "mas_chess_dlg_game_monika_win_{0}"

    # base part of label for variable chess strength when monika wins by 
    # early surrender
    DLG_MONIKA_WIN_SURR_BASE = "mas_chess_dlg_game_monika_win_surr_{0}"

    # base part of label for variable chess strength when monika loses
    DLG_MONIKA_LOSE_BASE = "mas_chess_dlg_game_monika_lose_{0}"

    ##### monika loses quips #####
    # these are all mean
    # first, lets take all the text based ones and group them
    # 1q
    _monika_loses_line_quips = (
        "Hmph.{w} You were just lucky today.",
        "...{w}I'm just having an off day.",
        "Ah, so you {i}are{/i} capable of winning...",
        "I guess you're not {i}entirely{/i} terrible.",
        "Tch-",
        "Winning isn't everything, you know...",
        "Ahaha,{w} I was just letting you win since you kept losing so much.",
        ( # thanks syn
            "Ahaha, surely you don't expect me to believe that you beat me " +
            "fairly, especially for someone at your skill level.{w} Don't " +
            "be so silly, [player]."
        ),
        "Oh, you won.{w} I should have taken this game seriously, then."
        # TODO: look into more of these
    )

    # add those line quips
    monika_loses_mean_quips = MASQuipList()
    for _line in _monika_loses_line_quips:
        monika_loses_mean_quips.addLineQuip(_line)

    # now add the glitch text quip
    monika_loses_mean_quips.addGlitchQuip(40, 2, 3, True)

    ##### monika wins quips #####
    # these are all mean
    # first, lets generate line quips
    # 1k expressions
    _monika_wins_line_quips = (
        "Ahaha, do you even know how to play chess?", # use this for surrenders too
        "Are you {i}that{/i} bad? I wasn't even taking this game seriously."
    )

    # zdd those line quips
    monika_wins_mean_quips = MASQuipList()
    for _line in _monika_wins_line_quips:
        monika_wins_mean_quips.addLineQuip(_line)

    # generate label quips
    _monika_wins_label_quips = (
        "mas_chess_dlg_game_monika_win_rekt",
    )

    # add the label ones
    for _label in monika_wins_label_quips:
        monika_wins_mean_quips.addLabelQuip(_label)

    ##### monika wins by early surrender quips #####
    # these are all mean
    # first, lets generate line quips
    _monika_wins_surr_line_quips = (
        _monika_wins_line_quips[0],
        (
            "Figures you'd give up. You're not one to see things all the " +
            "way through."
        ),
    )

    # add those line quips
    monika_wins_surr_mean_quips = MASQuipList()
    for _line in _monika_wins_surr_line_quips:
        monika_wins_surr_mean_quips.addLineQuip(_line)

    # generate label quips
    _monika_wins_surr_label_quips = (
        "mas_chess_dlg_game_monika_win_surr_resolve",
        "mas_chess_dlg_game_monika_win_surr_trying"
    )

    # add the label ones
    for _label in monika_wins_surr_label_quips:
        monika_wins_surr_mean_quips.addLabelQuip(_label)

## functions ==================================================================

    def __initDLGActions():
        """
        Initailizes the DLG actions dict and updates the persistent 
        appriorpately

        ASSUMES:
            renpy.game.persistent._mas_chess_dlg_actions
        """
        # dlg actions dict
        # NOTE: this is a way of allowing for dict expansion without fancy 
        # update scripts. 
        dlg_actions = {
            QS_LOST: 0,
            QF_LOST_OFCN: 0,
            QF_LOST_MAYBE: 0,
            QF_LOST_ACDNT: 0,
            QF_EDIT_YES: 0,
            QF_EDIT_NO: 0
        }
        
        # check to ensure persistent is updated
        if len(dlg_actions) != len(renpy.game.persistent._mas_chess_dlg_actions):
            dlg_actions.update(renpy.game.persistent._mas_chess_dlg_actions)
            renpy.game.persistent._mas_chess_dlg_actions = dlg_actions


    def __initMASChess():
        """
        Initializes mas chess stuff that needs to be initalized
        """
        __initDLGActions()


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


init 2018 python in mas_chess:
    # run init function
    __initMASChess()

init:
    python:
        import chess
        import chess.pgn
        import subprocess
        import platform
        import random
        import pygame
        import threading
        import collections
        import os

        ON_POSIX = 'posix' in sys.builtin_module_names

        def enqueue_output(out, queue, lock):
            for line in iter(out.readline, b''):
                lock.acquire()
                queue.appendleft(line)
                lock.release()
            out.close()

        def is_morning():
            return (datetime.datetime.now().time().hour > 6 and datetime.datetime.now().time().hour < 18)

        class ArchitectureError(RuntimeError):
            pass

        def is_platform_good_for_chess():
            import platform
            import sys
            if sys.maxsize > 2**32:
                return platform.system() == 'Windows' or platform.system() == 'Linux' or platform.system() == 'Darwin'
            else:
                return platform.system() == 'Windows'

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

        # chess exception
        class ChessException(Exception):
            def __init__(self, msg):
                self.msg = msg
            def __str__(self):
                return self.msg

        # only add chess folder if we can even do chess
        if is_platform_good_for_chess():
            # first create the folder for this
            try: 
                file_path = os.path.normcase(
                    config.basedir + mas_chess.CHESS_SAVE_PATH
                )
                if not os.access(file_path, os.F_OK):
                    os.mkdir(file_path)
                mas_chess.CHESS_SAVE_PATH = file_path
            except: 
                raise ChessException(
                    "Chess game folder could not be created '{0}'".format(
                        file_path
                    )
                )

        class ChessDisplayable(renpy.Displayable):
            COLOR_WHITE = True
            COLOR_BLACK = False
            MONIKA_WAITTIME = 1500
            MONIKA_OPTIMISM = 33
            MONIKA_THREADS = 1

            MOUSE_EVENTS = (
                pygame.MOUSEMOTION,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEBUTTONDOWN
            )

            def __init__(self, player_color, pgn_game=None):
                """
                player_color - player color obvi
                pgn_game - previous game to load (chess.pgn.Game)
                """
                import sys

                renpy.Displayable.__init__(self)

                # Some displayables we use.
                self.pieces_image = Image("mod_assets/chess_pieces.png")
                self.board_image = Image("mod_assets/chess_board.png")
                self.piece_highlight_red_image = Image("mod_assets/piece_highlight_red.png")
                self.piece_highlight_green_image = Image("mod_assets/piece_highlight_green.png")
                self.piece_highlight_yellow_image = Image("mod_assets/piece_highlight_yellow.png")
                self.piece_highlight_magenta_image = Image("mod_assets/piece_highlight_magenta.png")
                self.move_indicator_player = Image("mod_assets/move_indicator_player.png")
                self.move_indicator_monika = Image("mod_assets/move_indicator_monika.png")
                self.player_move_prompt = Text(_("It's your turn, [player]!"), size=36)
                self.num_turns = 0
                self.surrendered = False           

                # The sizes of some of the images.
                self.VECTOR_PIECE_POS = {
                    'K': 0,
                    'Q': 1,
                    'R': 2,
                    'B': 3,
                    'N': 4,
                    'P': 5
                }
                self.BOARD_BORDER_WIDTH = 15
                self.BOARD_BORDER_HEIGHT = 15
                self.PIECE_WIDTH = 57
                self.PIECE_HEIGHT = 57
                self.BOARD_WIDTH = self.BOARD_BORDER_WIDTH * 2 + self.PIECE_WIDTH * 8
                self.BOARD_HEIGHT = self.BOARD_BORDER_HEIGHT * 2 + self.PIECE_HEIGHT * 8
                self.INDICATOR_WIDTH = 60
                self.INDICATOR_HEIGHT = 96
                self.BUTTON_WIDTH = 120
                self.BUTTON_HEIGHT = 35
                self.BUTTON_X_SPACING = 10
                self.BUTTON_Y_SPACING = 10

                # hotkey button displayables
                button_idle = Image("mod_assets/hkb_idle_background.png")
                button_hover = Image("mod_assets/hkb_hover_background.png")
                button_no = Image("mod_assets/hkb_disabled_background.png")

                # hotkey button text
                # idle style/ disabled style:
                button_text_save_idle = Text(
                    "Save",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#000",
                    outlines=[]
                )
                button_text_giveup_idle = Text(
                    "Give Up",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#000",
                    outlines=[]
                )
                button_text_done_idle = Text(
                    "Done",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#000",
                    outlines=[]
                )

                # hover style
                button_text_save_hover = Text(
                    "Save",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#fa9",
                    outlines=[]
                )
                button_text_giveup_hover = Text(
                    "Give Up",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#fa9",
                    outlines=[]
                )
                button_text_done_hover = Text(
                    "Done",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#fa9",
                    outlines=[]
                )

                # calculate positions
                self.drawn_board_x = int((1280 - self.BOARD_WIDTH) / 2)
                self.drawn_board_y=  int((720 - self.BOARD_HEIGHT) / 2)
                drawn_button_x = (
                    1280 - self.drawn_board_x + self.BUTTON_X_SPACING
                )
                drawn_button_y_top = (
                    720 - (
                        (self.BUTTON_HEIGHT * 2) + 
                        self.BUTTON_Y_SPACING +
                        self.drawn_board_y
                    )
                )
                drawn_button_y_bot = (
                    720 - (self.BUTTON_HEIGHT + self.drawn_board_y)
                )

                # now the actual 3 buttons
                self._button_save = MASButtonDisplayable(
                    button_text_save_idle,
                    button_text_save_hover,
                    button_text_save_idle,
                    button_idle,
                    button_hover,
                    button_no,
                    drawn_button_x,
                    drawn_button_y_top,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                self._button_giveup = MASButtonDisplayable(
                    button_text_giveup_idle,
                    button_text_giveup_hover,
                    button_text_giveup_idle,
                    button_idle,
                    button_hover,
                    button_no,
                    drawn_button_x,
                    drawn_button_y_bot,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound
                )
                self._button_done = MASButtonDisplayable(
                    button_text_done_idle,
                    button_text_done_hover,
                    button_text_done_idle,
                    button_idle,
                    button_hover,
                    button_no,
                    drawn_button_x,
                    drawn_button_y_bot,
                    self.BUTTON_WIDTH,
                    self.BUTTON_HEIGHT,
                    hover_sound=gui.activate_sound,
                    activate_sound=gui.activate_sound
                )

                # the visible buttons list
                self._visible_buttons = [
                    self._button_save,
                    self._button_giveup
                ]
                self._visible_buttons_winner = [
                    self._button_save,
                    self._button_done
                ]

                # Stockfish engine provides AI for the game.
                # Launch the appropriate version based on the architecture and OS.
                if not is_platform_good_for_chess():
                    # This is the last-resort check, the availability of the chess game should be checked independently beforehand.
                    raise ArchitectureError('Your operating system does not support the chess game.')

                def open_stockfish(path,startupinfo=None):
                    return subprocess.Popen([renpy.loader.transfn(path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,startupinfo=startupinfo)

                is_64_bit = sys.maxsize > 2**32
                if platform.system() == 'Windows':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    if is_64_bit:
                        self.stockfish = open_stockfish('mod_assets/stockfish_8_windows_x64.exe',startupinfo)
                    else:
                        self.stockfish = open_stockfish('mod_assets/stockfish_8_windows_x32.exe',startupinfo)
                elif platform.system() == 'Linux' and is_64_bit:
                    os.chmod(config.basedir + '/game/mod_assets/stockfish_8_linux_x64',0755)
                    self.stockfish = open_stockfish('mod_assets/stockfish_8_linux_x64')
                elif platform.system() == 'Darwin' and is_64_bit:
                    os.chmod(config.basedir + '/game/mod_assets/stockfish_8_macosx_x64',0755)
                    self.stockfish = open_stockfish('mod_assets/stockfish_8_macosx_x64')

                # Set Monika's parameters
                self.stockfish.stdin.write("setoption name Skill Level value %d\n" % (persistent.chess_strength))
                self.stockfish.stdin.write("setoption name Contempt value %d\n" % (self.MONIKA_OPTIMISM))

                # Set up facilities for asynchronous communication
                self.queue = collections.deque()
                self.lock = threading.Lock()
                thrd = threading.Thread(target=enqueue_output, args=(self.stockfish.stdout, self.queue, self.lock))
                thrd.daemon = True
                thrd.start()

                # NOTE: DEBUG
                # Use this starting FEN line to do board testing
#                DEBUG_STARTING_FEN = "qk6/p7/8/8/8/8/7P/QK6 w - - 0 1"
                #These ones are for easy victory for white or black
#                DEBUG_STARTING_FEN_WHITE = "4k3/R7/8/1p5R/8/3Q4/8/4K3 w - - 0 1"
#                DEBUG_STARTING_FEN_BLACK = "4k3/8/r7/1p3P2/3q4/8/7r/4K3 w - - 0 1"

                # handlign promo
                self.promolist = ["q","r","n","b","r","k"]

                # separate handling of music menu open because the songs store
                # is for main renpy interaction
                self.music_menu_open = False

                # Board for integration with python-chess.
                # NOTE: DEBUG
                # Use this line (and comment the one following this one) to
                # use DEBUG FEN
#                self.board = chess.Board(fen=DEBUG_STARTING_FEN)
                #
                self.board = None
                # NOTE: we now check for a previous unfinished game before
                # setting up board
                if pgn_game:
                    # load this game into the board, push turns
                    self.board = pgn_game.board()
                    for move in pgn_game.main_line():
                        self.board.push(move)

                    # whose turn?
                    if self.board.turn == chess.WHITE:
                        self.current_turn = self.COLOR_WHITE
                    else:
                        self.current_turn = self.COLOR_BLACK

                    # colors?
                    if pgn_game.headers["White"] == mas_monika_twitter_handle:
                        self.player_color = self.COLOR_BLACK
                    else:
                        self.player_color = self.COLOR_WHITE

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
                    # start off with traditional board
                    self.board = chess.Board()

                    # stuff we need to save to the board 
                    self.today_date = datetime.date.today().strftime("%Y.%m.%d")
                    self.start_fen = self.board.fen()
                    
                    # other game setup
                    self.current_turn = self.COLOR_WHITE

                    # setup player color
                    self.player_color = player_color

                    # setup last move
                    self.last_move_src = None
                    self.last_move_dst = None

                self.selected_piece = None
                self.possible_moves = set([])
                self.winner = None
                self.last_clicked_king = 0.0

                # special button coordinates
                self.drawn_button_x = 0
                self.drawn_button_y_top = 0
                self.drawn_button_y_bot = 0

                # setup a pgn (could be None, in which case we are playing a
                # fresh game)
                self.pgn_game = pgn_game

                # If it's Monika's turn, send her the board positions so that she can start analyzing.
                if player_color != self.current_turn:
                    self.start_monika_analysis()
                    self._button_save.disable()
                    self._button_giveup.disable()
                elif self.board.fullmove_number <= 4:
                    self._button_save.disable()

            def start_monika_analysis(self):
                self.stockfish.stdin.write("position fen %s" % (self.board.fen()) + '\n')
                self.stockfish.stdin.write("go movetime %d" % self.MONIKA_WAITTIME + '\n')

            def poll_monika_move(self):
                self.lock.acquire()
                res = None
                while self.queue:
                    line = self.queue.pop()
                    match = re.match(r"^bestmove (\w+)", line)
                    if match:
                        res = match.group(1)
                self.lock.release()
                return res

            def __del__(self):
                self.stockfish.stdin.close()
                self.stockfish.wait()

            @staticmethod
            def coords_to_uci(x, y):
                x = chr(x + ord('a'))
                y += 1
                return str(x) + str(y)

            def check_winner(self, current_move):
                if self.board.is_game_over():
                    if self.board.result() == '1/2-1/2':
                        self.winner = 'none'
                    else:
                        self.winner = current_move

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
                    if self.player_color == self.COLOR_WHITE:
                        new_pgn.headers["Result"] = "0-1"
                    else:
                        new_pgn.headers["Result"] = "1-0"

                if self.pgn_game:
                    # exisitng game, transfer data over
                    new_pgn.headers["Site"] = self.pgn_game.headers["Site"]
                    new_pgn.headers["Date"] = self.pgn_game.headers["Date"]
                    new_pgn.headers["White"] = self.pgn_game.headers["White"]
                    new_pgn.headers["Black"] = self.pgn_game.headers["Black"]
                    
                    old_fen = self.pgn_game.headers.get("FEN", None)
                    if old_fen:
                        new_pgn.headers["FEN"] = old_fen
                        new_pgn.headers["SetUp"] = "1"

                else:
                    # new game stuff only:
                    # monika's ingame name will be her twitter handle
                    if player_color == self.COLOR_WHITE:
                        new_pgn.headers["White"] = persistent.playername
                        new_pgn.headers["Black"] = mas_monika_twitter_handle
                    else:
                        new_pgn.headers["White"] = mas_monika_twitter_handle
                        new_pgn.headers["Black"] = persistent.playername

                    # date, site, and fen
                    # MAS is malaysia but who cares
                    new_pgn.headers["Site"] = "MAS" 
                    new_pgn.headers["Date"] = self.today_date
                    new_pgn.headers["FEN"] = self.start_fen
                    new_pgn.headers["SetUp"] = "1"

                return (
                    new_pgn,
                    (
                        (
                            new_pgn.headers["Result"] == "1-0"
                            and new_pgn.headers["White"] == mas_monika_twitter_handle
                        ) or (
                            new_pgn.headers["Result"] == "0-1"
                            and new_pgn.headers["Black"] == mas_monika_twitter_handle
                        )
                    ),
                    giveup,
                    self.board.fullmove_number
                )


            def _inButton(self, x, y, button_x, button_y):
                """
                Checks if the given mouse coordinates is in the given button's
                area.

                IN:
                    x - x coordinate
                    y - y coordinate
                    button_x - x coordinate of the button
                    button_y - y coordinate of the button

                RETURNS:
                    True if the mouse coords are in the button,
                    False otherwise
                """
                return (
                    button_x <= x <= button_x + self.BUTTON_WIDTH
                    and button_y <= y <= button_y + self.BUTTON_HEIGHT
                )

            # Renders the board, pieces, etc.
            def render(self, width, height, st, at):

                # Poll Monika for moves if it's her turn
                if self.current_turn != self.player_color and not self.winner:
                    monika_move = self.poll_monika_move()
                    if monika_move is not None:
                        self.last_move_src = (ord(monika_move[0]) - ord('a'), ord(monika_move[1]) - ord('1'))
                        self.last_move_dst = (ord(monika_move[2]) - ord('a'), ord(monika_move[3]) - ord('1'))
                        self.board.push_uci(monika_move)
                        if self.current_turn == self.COLOR_BLACK:
                            self.num_turns += 1
                        self.current_turn = self.player_color
                        self.winner = self.board.is_game_over()

                        # we assume buttons were disabled prior to here
                        # (not Done though)
                        if not self.winner:
                            self._button_giveup.enable()

                            # enable button only after 4th move
                            if self.num_turns > 4:
                                self._button_save.enable()

                # The Render object we'll be drawing into.
                r = renpy.Render(width, height)

                # Prepare the board as a renderer.
                board = renpy.render(self.board_image, 1280, 720, st, at)

                # Prepare the pieces vector as a renderer.
                pieces = renpy.render(self.pieces_image, 1280, 720, st, at)

                # Prepare the highlights as a renderers.
                highlight_red = renpy.render(self.piece_highlight_red_image, 1280, 720, st, at)
                highlight_green = renpy.render(self.piece_highlight_green_image, 1280, 720, st, at)
                highlight_yellow = renpy.render(self.piece_highlight_yellow_image, 1280, 720, st, at)
                highlight_magenta = renpy.render(self.piece_highlight_magenta_image, 1280, 720, st, at)

                # get the mouse pos 
                mx, my = get_mouse_pos()

                
                # if the mouse is over a button, render that button
                # differently
                # winner?
                visible_buttons = list()
                if self.winner:

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

                # Draw the board.
                r.blit(board, (self.drawn_board_x, self.drawn_board_y))
                indicator_position = (int((width - self.INDICATOR_WIDTH) / 2 + self.BOARD_WIDTH / 2 + 50),
                                      int((height - self.INDICATOR_HEIGHT) / 2))

                # Draw the move indicator
                if self.current_turn == self.player_color:
                    r.blit(renpy.render(self.move_indicator_player, 1280, 720, st, at), indicator_position)
                else:
                    r.blit(renpy.render(self.move_indicator_monika, 1280, 720, st, at), indicator_position)

                # draw the buttons
                for b in visible_buttons:
                    r.blit(b[0], (b[1], b[2]))

                def get_piece_render_for_letter(letter):
                    jy = 0 if letter.islower() else 1
                    jx = self.VECTOR_PIECE_POS[letter.upper()]
                    return pieces.subsurface((jx * self.PIECE_WIDTH, jy * self.PIECE_HEIGHT,
                                              self.PIECE_WIDTH, self.PIECE_HEIGHT))

                # Draw the pieces on the Board renderer.
                for ix in range(8):
                    for iy in range(8):
                        iy_orig = iy
                        ix_orig = ix
                        if self.player_color == self.COLOR_WHITE:
                            iy = 7 - iy
                        else: # black player should be reversed X
                            ix = 7 - ix
                        x = int((width - (self.BOARD_WIDTH - self.BOARD_BORDER_WIDTH * 2)) / 2  + ix * self.PIECE_WIDTH)
                        y = int((height - (self.BOARD_HEIGHT - self.BOARD_BORDER_HEIGHT * 2)) / 2 + iy * self.PIECE_HEIGHT)

                        def render_move(move):
                            if move is not None and ix_orig == move[0] and iy_orig == move[1]:
                                if self.player_color == self.current_turn:
                                    r.blit(highlight_magenta, (x, y))
                                else:
                                    r.blit(highlight_green, (x, y))

                        render_move(self.last_move_src)
                        render_move(self.last_move_dst)

                        # Take care not to render the selected piece twice.
                        if (self.selected_piece is not None and
                            ix_orig == self.selected_piece[0] and
                            iy_orig == self.selected_piece[1]):
                            r.blit(highlight_green, (x, y))
                            continue

                        piece = self.board.piece_at(iy_orig * 8 + ix_orig)

                        possible_move_str = None
                        blit_rendered = False
                        if self.possible_moves:
                            possible_move_str = (ChessDisplayable.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) +
                                                 ChessDisplayable.coords_to_uci(ix_orig, iy_orig))
                            if chess.Move.from_uci(possible_move_str) in self.possible_moves:
                                r.blit(highlight_yellow, (x, y))
                                blit_rendered = True

                            # force checking for promotion
                            if not blit_rendered and (iy == 0 or iy == 7):
                                index = 0
                                while (not blit_rendered
                                        and index < len(self.promolist)):

                                    if (chess.Move.from_uci(
                                        possible_move_str + self.promolist[index])
                                        in self.possible_moves):
                                        r.blit(highlight_yellow, (x, y))
                                        blit_rendered = True

                                    index += 1

                        if piece is None:
                            continue

                        if (mx >= x and mx < x + self.PIECE_WIDTH and
                            my >= y and my < y + self.PIECE_HEIGHT and
                            bool(str(piece).isupper()) == (self.player_color == self.COLOR_WHITE) and
                            self.current_turn == self.player_color and
                            self.selected_piece is None and
                            not self.winner):
                            r.blit(highlight_green, (x, y))

                        if self.winner:
                            result = self.board.result()

                            # black won
                            if str(piece) == "K" and result == "0-1":
                                r.blit(highlight_red, (x, y))

                            # white won
                            elif str(piece) == "k" and result == "1-0":
                                r.blit(highlight_red, (x, y))
                               
                        r.blit(get_piece_render_for_letter(str(piece)), (x, y))


                if self.current_turn == self.player_color and not self.winner:
                    # Display the indication that it's the player's turn
                    prompt = renpy.render(self.player_move_prompt, 1280, 720, st, at)
                    pw, ph = prompt.get_size()
                    bh = (height - self.BOARD_HEIGHT) / 2
                    r.blit(prompt, (int((width - pw) / 2), int(self.BOARD_HEIGHT + bh + (bh - ph) / 2)))

                if self.selected_piece is not None:
                    # Draw the selected piece.
                    piece = self.board.piece_at(self.selected_piece[1] * 8 + self.selected_piece[0])
                    assert piece is not None
                    px, py = get_mouse_pos()
                    px -= self.PIECE_WIDTH / 2
                    py -= self.PIECE_HEIGHT / 2
                    r.blit(get_piece_render_for_letter(str(piece)), (px, py))

                # Ask that we be re-rendered ASAP, so we can show the next frame.
                renpy.redraw(self, 0)


                # Return the Render object.
                return r

            # Handles events.
            def event(self, ev, x, y, st):
 
                # check muouse position
                if ev.type in self.MOUSE_EVENTS:
                    # are we in mouse button things

                     # inital check for winner
                    if self.winner:
                        
                        if self._button_done.event(ev, x, y, st):
                            # user clicks Done
                            return self._quitPGN(False)

                    # inital check for buttons
                    elif self.current_turn == self.player_color:
                        
                        if self._button_save.event(ev, x, y, st):
                            # user wants to save this game
                            return self._quitPGN(False)

                        elif self._button_giveup.event(ev, x, y, st):
                            renpy.call_in_new_context("mas_chess_confirm_context")
                            if mas_chess.quit_game:
                                # user wishes to surrender (noob)
                                return self._quitPGN(True)
                   
                def get_piece_pos():
                    mx, my = get_mouse_pos()
                    mx -= (1280 - (self.BOARD_WIDTH - self.BOARD_BORDER_WIDTH * 2)) / 2
                    my -= (720 - (self.BOARD_HEIGHT - self.BOARD_BORDER_HEIGHT * 2)) / 2
                    px = mx / self.PIECE_WIDTH
                    py = my / self.PIECE_HEIGHT
                    if self.player_color == self.COLOR_WHITE:
                        py = 7 - py
                    else: # black player should be reversed X
                        px = 7 - px
                    if py >= 0 and py < 8 and px >= 0 and px < 8:
                        return (px, py)
                    return (None, None)

                # Mousebutton down == possibly select the piece to move
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:

                    # NOTE: DEBUG
#                    mxx, myy = get_mouse_pos()
#                    mxp, myp = pygame.mouse.get_pos()
#                    with open("chess_debug", "a") as debug_file:
#                        debug_file.write("["+str(mxx)+","+str(myy)+"] " +
#                        "("+str(mxp)+","+str(myp)+") \n")

                    # continue
                    px, py = get_piece_pos()
                    if (
                            px is not None 
                            and py is not None 
                            and self.board.piece_at(py * 8 + px) is not None 
                            and bool(str(self.board.piece_at(py * 8 + px)).isupper()) 
                                == (self.player_color == self.COLOR_WHITE) 
                            and self.current_turn == self.player_color
                        ):

                        piece = str(self.board.piece_at(py * 8 + px))

                        # NOTE: following commeneted out because we added
                        # a surrender button
#                            if piece.lower() == 'k' and piece.islower() == (self.player_color == self.COLOR_BLACK):
#                                if st - self.last_clicked_king < 0.2:
#                                    self.winner = 'monika'
#                                    self.winner_confirmed = True
#                                    self.surrendered = True
#                                self.last_clicked_king = st

                        # NOTE: The following is commented out because it
                        # broke the ability to promote units. We keep it
                        # here for reference, tho
#                            src = ChessDisplayable.coords_to_uci(px, py)

#                            all_moves = [chess.Move.from_uci(src + ChessDisplayable.coords_to_uci(file, rank))
#                                                                for file in range(8)
#                                                                for rank in range(8)]
#                            legal_moves = set(self.board.legal_moves).intersection(all_moves)
#                            p_legal_moves = set(self.board.pseudo_legal_moves).intersection(all_moves)
#                            self.possible_moves = legal_moves.union(p_legal_moves)
                        self.possible_moves = self.board.legal_moves
                        self.selected_piece = (px, py)

                # Mousebutton up == possibly release the selected piece
                if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                    px, py = get_piece_pos()
                    if px is not None and py is not None and self.selected_piece is not None:
                        move_str = self.coords_to_uci(self.selected_piece[0], self.selected_piece[1]) + self.coords_to_uci(px, py)

                        piece = str(
                            self.board.piece_at(
                                self.selected_piece[1] * 8 +
                                self.selected_piece[0]
                            )
                        )

                        if piece.lower() == 'p' and (py == 0 or py == 7):
                            move_str += "q"
                        if chess.Move.from_uci(move_str) in self.possible_moves:
                            self.last_move_src = self.selected_piece
                            self.last_move_dst = (px, py)
                            self.board.push_uci(move_str)
#                            self.check_winner('player')
                            self.winner = self.board.is_game_over()
                            if self.current_turn == self.COLOR_BLACK:
                                self.num_turns += 1
                            self.current_turn = not self.current_turn
                            if not self.winner:
                                self.start_monika_analysis()

                            # disable the buttons when your turn is done
                            self._button_save.disable()
                            self._button_giveup.disable()

                    self.selected_piece = None
                    # NOTE: DEBUG
                    # Use these file write statements to display legal moves
#                    with open("chess_debug", "a") as debug_file:
#                        for item in set(self.board.legal_moves):
#                            debug_file.write(item.uci() + "\n")
#
#                    with open("chess_debug_2", "a") as debug_file:
#                        for item in set(self.board.pseudo_legal_moves):
#                            debug_file.write(item.uci() + "\n")
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
                    if (ev.key == pygame.K_PLUS
                            or ev.key == pygame.K_EQUALS
                            or ev.key == pygame.K_KP_PLUS):
                        inc_musicvol()

                    # volume decrease
                    if (ev.key == pygame.K_MINUS
                            or ev.key == pygame.K_UNDERSCORE
                            or ev.key == pygame.K_KP_MINUS):
                        dec_musicvol()

                raise renpy.IgnoreEvent()

label game_chess:
    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclgc
        return

    hide screen keylistener

    m 1b "You want to play chess? Alright~"
#   m 2a "Double click your king if you decide to surrender."
#    m 1a "Get ready!"
    call demo_minigame_chess from _call_demo_minigame_chess
    return

label demo_minigame_chess:
    $ import store.mas_chess as mas_chess
    $ loaded_game = None
    $ ur_nice_today = True

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dcldmc
        return

    if not renpy.seen_label("mas_chess_save_selected"):
        call mas_chess_save_migration from _mas_chess_savemg

        # check if user selected a save
        if not _return:
            return

        # if the return is no games, jump to new game
        elif _return == mas_chess.CHESS_NO_GAMES_FOUND:
            jump mas_chess_new_game_start

        # otherwise user has selected a save, which is the pgn game file.
        $ loaded_game = _return

        # NOTE: debug this
#        $ persistent._mas_chess_quicksave = str(loaded_game)

    elif len(persistent._mas_chess_quicksave) > 0:
        # quicksave holds the pgn game in plaintext
        python:
            import StringIO # python 2 
            import chess.pgn

            quicksaved_game = chess.pgn.read_game(
                StringIO.StringIO(persistent._mas_chess_quicksave)
            )

            quicksaved_game = mas_chess._checkInProgressGame(
                quicksaved_game,
                mas_monika_twitter_handle
            )

        # failure reading a saved game
        if quicksaved_game is None:
            $ ur_nice_today = False

            if persistent._mas_chess_3_edit_sorry:
                call mas_chess_dlg_qf_edit_n_3_n_qs from _mas_chess_dlgqfeditn3nqs

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
                call mas_chess_dlg_qs_lost from _mas_chess_dql_main

                # not None returns means we should quit from chess
                if _return is not None:
                    return

            jump mas_chess_new_game_start

        # otherwise, read the game from file
        python:
            quicksaved_game = quicksaved_game[1]

            quicksaved_filename = (
                quicksaved_game.headers["Event"] + mas_chess.CHESS_SAVE_EXT
            )
            quicksaved_filename_clean = (
                mas_chess.CHESS_SAVE_PATH + quicksaved_filename
            ).replace("\\", "/")

            try:
                if renpy.file(quicksaved_filename_clean):
                    quicksaved_file = mas_chess.isInProgressGame(
                        quicksaved_filename,
                        mas_monika_twitter_handle
                    )
                else:
                    quicksaved_file = None
            except:
                quicksaved_file = None

        # failure reading the saved game from text
        if quicksaved_file is None:
            $ ur_nice_today = False
            # save the filename of what the game should have been
            python:
                import os

                mas_chess.loaded_game_filename = quicksaved_filename_clean

            call mas_chess_dlg_qf_lost from _mas_chess_dql_main2

            # should we continue or not
            if _return == mas_chess.CHESS_GAME_CONT:
                python:
                    try:
                        if renpy.file(quicksaved_filename_clean):
                            quicksaved_file = mas_chess.isInProgressGame(
                                quicksaved_filename,
                                mas_monika_twitter_handle
                            )
                        else:
                            quicksaved_file = None
                    except:
                        quicksaved_file = None

                if quicksaved_file is None:
                    call mas_chess_dlg_qf_lost_may_removed from _mas_chess_dqlqfr
                    return

                # otherwise we have a chess game here
                $ quicksaved_file = quicksaved_file[1]

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
                jump mas_chess_new_game_start

        python:
            # check for game modifications
            is_same = str(quicksaved_game) == str(quicksaved_file)

        if not is_same:
            # TODO test this
            $ ur_nice_today = False

            call mas_chess_dlg_qf_edit from _mas_chess_dql_main3

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
            jump mas_chess_new_game_start

        # otherwise we are in good hands
        else:
            # TODO test this

            $ loaded_game = quicksaved_game

            if ur_nice_today:
                # we successfully loaded the unfinished game and player did not
                # cheat
                m 1a "We still have an unfinished game in progress."
            m "Get ready!"

label mas_chess_game_load_check:

    if loaded_game:
        # now figure out the player color
        if loaded_game.headers["White"] == mas_monika_twitter_handle:
            $ player_color = ChessDisplayable.COLOR_BLACK
        else:
            $ player_color = ChessDisplayable.COLOR_WHITE
        jump mas_chess_game_start

label mas_chess_new_game_start:
    # otherwise, new games only
    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclngs
        return

    menu:
        m "What color would suit you?"

        "White":
            $ player_color = ChessDisplayable.COLOR_WHITE
        "Black":
            $ player_color = ChessDisplayable.COLOR_BLACK
        "Let's draw lots!":
            $ choice = random.randint(0, 1) == 0
            if choice:
                $ player_color = ChessDisplayable.COLOR_WHITE
                m 2a "Oh look, I drew black! Let's begin!"
            else:
                $ player_color = ChessDisplayable.COLOR_BLACK
                m 2a "Oh look, I drew white! Let's begin!"

label mas_chess_game_start:
    window hide None

    if persistent._mas_chess_timed_disable is not None:
        call mas_chess_dlg_chess_locked from _mas_chess_dclgs
        return

    python:
        ui.add(ChessDisplayable(player_color, pgn_game=loaded_game))
        results = ui.interact(suppress_underlay=True)

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results

        # game result header
        game_result = new_pgn_game.headers["Result"]

        # reset chess strength if avaiable
        if mas_chess.chess_strength[0]:
            persistent.chess_strength = mas_chess.chess_strength[1]
            mas_chess.chess_strength = (False, 0)

    #Regenerate the spaceroom scene
    #$scene_change=True #Force scene generation
    #call spaceroom from _call_spaceroom

    # TODO: we need to modify dialogue based on mas_3_edit_sorry

    # check results
    if game_result == "*":
        # this should jump directly to (the twilight zone) the save game
        # name input flow.
        call mas_chess_dlg_game_in_progress from _mas_chess_dlggameinprog

        jump mas_chess_savegame

    elif game_result == "1/2-1/2":
        # draw
        call mas_chess_dlg_game_drawed from _mas_chess_dlggamedrawed
        $ persistent._mas_chess_stats["draws"] += 1

    elif is_monika_winner:
        $ persistent._mas_chess_stats["losses"] += 1
        if is_surrender and num_turns <= 4:
           
            # main dialogue
            call mas_chess_dlg_game_monika_win_surr from _mas_chess_dlggmws

        else:
            # main dialogue
            call mas_chess_dlg_game_monika_win from _mas_chess_dlggmw

        # make monika a little easier
        $ persistent.chess_strength -= 1

    else:
        $ persistent._mas_chess_stats["wins"] += 1

        #Give player XP if this is their first win
        if not persistent.ever_won['chess']:
            $persistent.ever_won['chess'] = True
            $grant_xp(xp.WIN_GAME)

        # main dialogue
        call mas_chess_dlg_game_monika_lose from _mas_chess_dlggml

        $ persistent.chess_strength += 1

    # transitional dialogue setup
    m 1a "Anyway..."

    # if you have a previous game, we are overwrititng it regardless
    if loaded_game:
        jump mas_chess_savegame

    # we only save a game if they put in some effort
    if num_turns > 4:
        menu:
            m "Would you like to save this game?"
            "Yes":
                jump mas_chess_savegame
            "No":
                # TODO: should there be dialogue here?
                pass

label mas_chess_playagain:
    menu:
        m "Do you want to play again?"

        "Yes":
            jump mas_chess_new_game_start
        "No":
            pass

label mas_chess_end:
    if is_monika_winner:
        m 2d "Despite its simple rules, chess is a really intricate game."
        m 1a "It's okay if you find yourself struggling at times."
        m 1j "Remember, the important thing is to be able to learn from your mistakes."
    elif game_result == "*":
        # TODO: this really should be better
        m 1a "Okay, [player], let's continue this game soon."
    else:
        m 2b "It's amazing how much more I have to learn even now."
        m 2a "I really don't mind losing as long as I can learn something."
        m 1j "After all, the company is good."

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
                $ pick_text = "You still need to pick a game to keep."
            else:
                label mas_chess_save_multi_dlg:
                    m 1m "So I've been thinking, [player]..."
                    m "Most people who leave in the middle of a chess game don't come back to start a new one."
                    m 1n "It makes no sense for me to keep track of more than one unfinished game between us."
                    m 1p "And since we have [game_count] games in progress..."
                    m 1g "I have to ask you to pick only one to keep.{w} Sorry, [player]."
                    $ pick_text = "Pick a game you'd like to keep."
            show monika 1e at t21
            $ renpy.say(m, pick_text, interact=False)
            
            call screen mas_gen_scrollable_menu(pgn_games, mas_chess.CHESS_MENU_AREA, mas_chess.CHESS_MENU_XALIGN, mas_chess.CHESS_MENU_WAIT_ITEM)

            show monika at t11
            if _return == mas_chess.CHESS_MENU_WAIT_VALUE:
                # user backs out
                m 2q "I see."
                m 2a "In that case, please take your time."
                m 1a "We'll play chess again once you've made your decision."
                return False
            else:
                # user selected a game
                m 1a "Alright." 
                python:
                    sel_game = actual_pgn_games.pop(_return)
                    for pgn_game in actual_pgn_games:
                        try:
                            os.remove(os.path.normcase(
                                mas_chess.CHESS_SAVE_PATH + pgn_game[1]
                            ))
                        except:
                            pass

        # we have one game, so return the game
        else:
            $ sel_game = actual_pgn_games[0]

# FALL THROUGH
label mas_chess_save_selected: 
    return sel_game[0]

label mas_chess_savegame:
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
            m 1e "We already have a game named '[save_name]'."
            menu:
                m "Should I overwrite it?"
                "Yes":
                    pass
                "No":
                    jump mas_chess_savegame

    python:
       
        with open(file_path, "w") as pgn_file:
            pgn_file.write(str(new_pgn_game))

        # internal save too
        persistent._mas_chess_quicksave = str(new_pgn_game)

        # the file path to show is different
        display_file_path = mas_chess.REL_DIR + save_filename

    m 1q ".{w=0.5}.{w=0.5}.{w=0.5}{nw}"
    m 1j "I've saved our game in '[display_file_path]'!"

    if not renpy.seen_label("mas_chess_pgn_explain"):

        label mas_chess_pgn_explain:
            m 1a "It's in a format called Portable Game Notation."
            m "You can open this file in PGN viewers."

            if game_result == "*": # ongoing game
                m 1n "It's possible to edit this file and change the outcome of the game,{w} but I'm sure you wouldn't do that."
                m 1e "Right, [player]?"
                menu:
                    "Of course not":
                        m 1j "Yay~"

    if game_result == "*":
        jump mas_chess_end

    jump mas_chess_playagain


#### DIALOGUE BLOCKS BELOW ####################################################

### Quicksave lost:
label mas_chess_dlg_qs_lost:
    python: 
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QS_LOST] += 1
        qs_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QS_LOST]
        
    call mas_chess_dlg_qs_lost_start from _mas_chess_dqsls
    
    if qs_gone_count == 2:
        call mas_chess_dlg_qs_lost_2 from _mas_chess_dlgqslost2

    elif qs_gone_count == 3:
        call mas_chess_dlg_qs_lost_3 from _mas_chess_dlgqslost3

    elif qs_gone_count % 5 == 0:
        call mas_chess_dlg_qs_lost_5r from _mas_chess_dlgqslost5r

    elif qs_gone_count % 7 == 0:
        call mas_chess_dlg_qs_lost_7r from _mas_chess_dlgqslost7r

    else:
        call mas_chess_dlg_qs_lost_gen from _mas_chess_dlgqslostgen

    return _return

# quicksave lost start
label mas_chess_dlg_qs_lost_start:
    m 2n "Uh, [player]...{w} It seems I messed up in saving our last game,"
    m "and now I can't open it anymore."
    return

# generic quicksave lost statement
label mas_chess_dlg_qs_lost_gen:
    m 1o "I'm sorry..."
    m "Let's start a new game instead."
    return

# 2nd time quicksave lost statement
label mas_chess_dlg_qs_lost_2:
    m 1p "I'm really, really sorry, [player]."
    m "I hope you can forgive me."
    show monika 1f
    pause 1.0
    m 1q "I'll make it up to you..."
    m 1a "by starting a new game!"
    return

# 3rd time quicksave lost statement
label mas_chess_dlg_qs_lost_3:
    m 1o "I'm so clumsy, [player]...{w} I'm sorry."
    m "Let's start a new game instead."
    return

# 5th time recurring quicksave lost statement
label mas_chess_dlg_qs_lost_5r:
    m 2h "This has happened [qs_gone_count] times now..."
    m "I wonder if this is a side effect of {cps=*0.75}{i}someone{/i}{/cps} trying to edit the saves.{w=1}.{w=1}.{w=1}"
    m 1i "Anyway..."   
    m "Let's start a new game."
    show monika 1h
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

    menu:
        m "Did you mess with the saves, [player]?"
        "[mas_chess.DLG_QF_LOST_OFCN_CHOICE]" if mas_chess.DLG_QF_LOST_OFCN_ENABLE:
            call mas_chess_dlg_qf_lost_ofcn_start from _mas_chess_dlgqflostofcnstart

        "[mas_chess.DLG_QF_LOST_MAY_CHOICE]" if mas_chess.DLG_QF_LOST_MAY_ENABLE:
            call mas_chess_dlg_qf_lost_may_start from _mas_chess_dlgqflostmaystart

        "[mas_chess.DLG_QF_LOST_ACDNT_CHOICE]" if mas_chess.DLG_QF_LOST_ACDNT_ENABLE:
            call mas_chesS_dlg_qf_lost_acdnt_start from _mas_chess_dlgqflostacdntstart

    return _return

# intro to quickfile lost
label mas_chess_dlg_qf_lost_start:
    m 2m "Well,{w} this is embarrassing."
    m "I could have sworn that we had an unfinished game, but I can't find the save file."
    return

## of course not flow
label mas_chess_dlg_qf_lost_ofcn_start:
    python: 
        import store.mas_chess as mas_chess
        persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN] += 1
        qf_gone_count = persistent._mas_chess_dlg_actions[mas_chess.QF_LOST_OFCN]

    if qf_gone_count == 3:
        call mas_chess_dlg_qf_lost_ofcn_3 from _mas_chess_dlgqflostofcn3

    elif qf_gone_count == 4:
        call mas_chess_dlg_qf_lost_ofcn_4 from _mas_chess_dlgqflostofcn4

    elif qf_gone_count == 5:
        call mas_chess_dlg_qf_lost_ofcn_5 from _mas_chess_dlgqflostofcn5

    elif qf_gone_count >= 6:
        call mas_chess_dlg_qf_lost_ofcn_6 from _mas_chess_dlgqflostofcn6

    else:
        call mas_chess_dlg_qf_lost_ofcn_gen from _mas_chess_dlgqflostofcngen

    return _return

# generic ofcnot monika
label mas_chess_dlg_qf_lost_ofcn_gen:
    m 1n "Ah, yeah. You wouldn't do that to me."
    m "I must have misplaced the save files."
    m 1o "Sorry, [player]."
    m "I'll make it up to you..."
    m 1a "by starting a new game!"
    return

# 3rd time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_3:
    m 2h "..."
    m "[player],{w} did you..."
    m 2q "Nevermind."
    m 1h "Let's play a new game."
    return

# 4th time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_4:
    jump mas_chess_dlg_qf_lost_ofcn_3

# 5th time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_5:
    m 2h "..."
    m "[player],{w} this is happening way too much."
    m 2q "I really don't believe you this time."
    pause 2.0
    m 2h "I hope you're not messing with me."
    m "..."
    m 1h "Whatever.{w} Let's just play a new game."
    return 

# 6th time you ofcn monika
label mas_chess_dlg_qf_lost_ofcn_6:
    # disable chess forever!
    m 2h "..."
    m "[player],{w} I don't believe you."
    # TODO: we need an angry monika
    m 2i "If you're just going to throw away our chess games like that,"
    m "then I don't want to play chess with you anymore."
    $ persistent.game_unlocks["chess"] = False
    # workaround to deal with peeople who havent seen the unlock chess label
    $ persistent._seen_ever["unlock_chess"] = True
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
    m 2g "[player]!{w} I should have known you were just messing with me!"
    jump mas_chess_dlg_qf_lost_may_filechecker

# generic maybe monika, found file
label mas_chess_dlg_qf_lost_may_gen_found:
    m 2a "Oh!"
    m 1j "There's the save.{w} Thanks for putting it back, [player]."
    m 1a "Now we can continue our game."
    return store.mas_chess.CHESS_GAME_CONT

# 2nd time maybe monika
label mas_chess_dlg_qf_lost_may_2:
    m 2g "[player]!{w} Stop messing with me!"
    jump mas_chess_dlg_qf_lost_may_filechecker

# 2nd time maybe monika, found file
label mas_chess_dlg_qf_lost_may_2_found:
    jump mas_chess_dlg_qf_lost_may_gen_found

# maybe monika file checking parts
label mas_chess_dlg_qf_lost_may_filechecker:
    $ import store.mas_chess as mas_chess
    $ game_file = mas_chess.loaded_game_filename

    if renpy.exists(game_file):
        jump mas_chess_dlg_qf_lost_may_gen_found

    m 1e "Can you put the save back so we can play?"
    if renpy.exists(game_file):
        jump mas_chess_dlg_qf_lost_may_gen_found

    show monika 1a

    # loop for about a minute and check for file xistence
    python:
        renpy.say(m, "I'll wait a minute...", interact=False)
        file_found = False
        seconds = 0
        while not file_found and seconds < 60:
            if renpy.exists(game_file):
                file_found = True
            else:
                renpy.pause(1.0, hard=True)
                seconds += 1

    if file_found:
        m 1j "Yay!{w} Thanks for putting it back, [player]."
        m "Now we can continue our game."
        show monika 1a
        return mas_chess.CHESS_GAME_CONT

    # else:
    m 1g "[player]..."
    m 1e "That's okay. Let's just play a new game."
    return

# 3rd time maybe monika
label mas_chess_dlg_qf_lost_may_3:
    m 2g "[player]! That's-"
    m 1 "Not a problem at all."
    m "I knew you were going to do this again,"
    m 1k "so I kept a backup of our save!"
    # TODO: wink here please
    m 1a "You can't trick me anymore, [player]."
    m "Now let's continue our game."
    return store.mas_chess.CHESS_GAME_BACKUP

# maybe monika, but player removed the file again!
label mas_chess_dlg_qf_lost_may_removed:
    # TODO; angery monika here
    m 2h "[player]!"
    m 2q "You removed the save again."
    pause 0.7
    m "Let's just play chess at another time, then."
    $ import datetime
    $ persistent._mas_chess_timed_disable = datetime.datetime.now()
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
    m 1e "[player]..."
    m "That's okay.{w} Accidents happen."
    m 1a "Let's play a new game instead."
    return

# 2nd accident monika
label mas_chess_dlg_qf_lost_acdnt_2:
    m 1e "Again? Don't be so clumsy, [player]."
    m 1j "But that's okay."
    m "We'll just play a new game instead."
    show monika 1a
    return

# 3rd accident monika
label mas_chess_dlg_qf_lost_acdnt_3:
    m 1e "I had a feeling this would happen again."
    m 3k "So I kept a backup of our save!"
    m 1a "Now we can continue our game."
    return store.mas_chess.CHESS_GAME_BACKUP

### quickfile edited
# main label for quickfile edited flow
label mas_chess_dlg_qf_edit:
    python:
        import store.mas_chess as mas_chess

    call mas_chess_dlg_qf_edit_start from _mas_chess_dlgqfeditstart

    show monika 2f
    menu:
        m "Did you edit the save file?"
        "Yes":
            call mas_chess_dlg_qf_edit_y_start from _mas_chess_dlgqfeditystart
        "No":
            call mas_chess_dlg_qf_edit_n_start from _mas_chess_dlgqfeditnstart

    return _return

# intro to quickfile edited
label mas_chess_dlg_qf_edit_start:
    m 2o "[player]..."
    return

## Yes Edit flow
label mas_chess_dlg_qf_edit_y_start:
    python: 
        import store.mas_chess as mas_chess
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
    m 2q "I'm disappointed in you."
    m 1c "But I'm glad that you were honest with me."

    # we want a timed menu here. Let's give the player 5 seconds to say sorry
    show screen mas_background_timed_jump(5, "mas_chess_dlg_qf_edit_y_1n")
    menu:
        "I'm sorry":
            hide screen mas_background_timed_jump
            m 1j "Apology accepted!"
            m 1a "Luckily, I still remember a little bit of the last game, so we can continue it from there."
            return store.mas_chess.CHESS_GAME_BACKUP
        "...":
            label mas_chess_dlg_qf_edit_y_1n:
                hide screen mas_background_timed_jump
                m "Since that game's been ruined, let's just play a new game."
            return
    return # just in case

# 2nd time yes edit
label mas_chess_dlg_qf_edit_y_2:
    m 2q "I am incredibly disappointed in you."
    m "I don't want to play chess right now."
    python:
        import datetime
        persistent._mas_chess_timed_disable = datetime.datetime.now()
    return True

# 3rd time yes edit
label mas_chess_dlg_qf_edit_y_3:
    m 2q "I'm not surprised..."
    m 2h "But I am prepared."
    m "I kept a backup of our game just in case you did this again."
    m 1 "Now let's finish this game."
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
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
    m 1f "I see."
    m "The save file looks different than how I last remembered it, but maybe that's just my memory failing me."
    m 1a "Let's continue this game."
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    return store.mas_chess.CHESS_GAME_FILE

# 2nd time no edit
label mas_chess_dlg_qf_edit_n_2:
    m 1f "I see."
    m "..."
    m "Let's just continue this game."
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20
    return store.mas_chess.CHESS_GAME_FILE

# 3rd time no edit
label mas_chess_dlg_qf_edit_n_3:
    m 2q "[player]..."
    m 2h "I kept a backup of our game.{w} I know you edited the save file."
    m "I just-"
    m "I just{fast} can't believe you would cheat and {i}lie{/i} to me."
    m 2o "..."
    
    # THE ULTIMATE CHOICE
    show screen mas_background_timed_jump(3, "mas_chess_dlg_qf_edit_n_3n")
    menu:
        "I'm sorry":
            hide screen mas_background_timed_jump
            call mas_chess_dlg_qf_edit_n_3_s from _mas_chess_dlgqfeditn3s

        "...":
            label mas_chess_dlg_qf_edit_n_3n:
                hide screen mas_background_timed_jump
                call mas_chess_dlg_qf_ediit_n_3_n from _mas_chess_dlgqfeditn3n

    return _return

# 3rd time no edit, sorry
label mas_chess_dlg_qf_edit_n_3_s:
    show monika 2h
    pause 1.0
    show monika 2
    pause 1.0
    m "I forgive you, [player], but please don't do this to me again."
    m "..."
    $ store.mas_chess.chess_strength = (True, persistent.chess_strength)
    $ persistent.chess_strength = 20   
    $ persistent._mas_chess_3_edit_sorry = True
    return store.mas_chess.CHESS_GAME_BACKUP

# 3rd time no edit, sorry, edit qs
label mas_chess_dlg_qf_edit_n_3_n_qs:
    m 2q "[player]..."
    m 2h "I see you've edited my backup saves."
    m "If you want to be like that right now, then we'll play chess some other time."
    python:
        import datetime
        persistent._mas_chess_timed_disable = datetime.datetime.now()
    return True

# 3rd time no edit, no sorry
label mas_chess_dlg_qf_edit_n_3_n:
    m 2h "I can't trust you anymore."
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
#        mas_root.resetPlayerData()

        # forever remember
        persistent._mas_chess_mangle_all = True
        
    jump _quit

## general dialogue
# if chess is locked
label mas_chess_dlg_chess_locked:
    m 1q "..."
    m "I don't feel like playing chess right now."
    return

### endgame dialogue
# dialogue has 2 sets, one for friendly, one for not.
# in some cases, we jump to the other because we dont care

# in progress game
label mas_chess_dlg_game_in_progress:
    if persistent._mas_chess_3_edit_sorry:
        # mean dialogue
        pass
    else:
        # friendly dialogue
        pass
    return

# draw game
label mas_chess_dlg_game_drawed:
    if persistent._mas_chess_3_edit_sorry:
        m 2h "A draw?"
        m 2q "Hmph."
        m 2h "I'll beat you next time."
    else:
        m 3h "A draw? How boring..."
    return

## monika wins
# monika win pre dialogue
label mas_chess_dlg_game_monika_win_pre:
    m 1b "I win!"
    return

# main monika win label
label mas_chess_dlg_game_monika_win:
    python:
        import store.mas_chess as mas_chess

    # regardless of mode, call the pre dialogue
    call mas_chess_dlg_game_monika_win_pre from _mas_chess_dlggmwpre

    # bad players get rekt by monika
    if persistent._mas_chess_3_edit_sorry:
        
        # pull a quip and say it
        $ t_quip, v_quip = mas_chess.monika_wins_mean_quips.quip()

        # check quip type
        if t_quip == MASQuipList.TYPE_LABEL:
            # this is a label, call it
            call expression v_quip from _mas_chess_dlggmw3esl

        else: # assume its a line
            # this is a line, call it using 1k expression
            m 1k "[v_quip]"

    else:
        python:
            # clean chess strength so its within bounds
            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif t_chess_str > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_WIN_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmwcsl

    return

## monika wins quips
label mas_chess_dlg_game_monika_win_rekt:
    m 1k "Ahaha~"
    m "Maybe you should stick to checkers."
    m 1 "I doubt you'll ever beat me."
    return

# winning, chess strength 0
label mas_chess_dlg_game_monika_win_0:
    jump mas_chess_dlg_game_monika_win_2

# winning, chess strength 1
label mas_chess_dlg_game_monika_win_1:
    jump mas_chess_dlg_game_monika_win_2

# winning, chess strength 2
label mas_chess_dlg_game_monika_win_2:
    m 1l "I really was going easy on you!"
    return

# winning, chess strength 3
label mas_chess_dlg_game_monika_win_3:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 4
label mas_chess_dlg_game_monika_win_4:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 5
label mas_chess_dlg_game_monika_win_5:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 6
label mas_chess_dlg_game_monika_win_6:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 7
label mas_chess_dlg_game_monika_win_7:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 8
label mas_chess_dlg_game_monika_win_8:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 9
label mas_chess_dlg_game_monika_win_9:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 10
label mas_chess_dlg_game_monika_win_10:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 11
label mas_chess_dlg_game_monika_win_11:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 12
label mas_chess_dlg_game_monika_win_12:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 13
label mas_chess_dlg_game_monika_win_13:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 14
label mas_chess_dlg_game_monika_win_14:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 15
label mas_chess_dlg_game_monika_win_15:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 16
label mas_chess_dlg_game_monika_win_16:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 17
label mas_chess_dlg_game_monika_win_17:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 18
label mas_chess_dlg_game_monika_win_18:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 19
label mas_chess_dlg_game_monika_win_19:
    jump mas_chess_dlg_game_monika_win_20

# winning, chess strength 20
label mas_chess_dlg_game_monika_win_20:
    m 1j "I'll go a little easier on you next time."
    return      

## monika wins by early surrender
# monika win by early surrender dialogue start
label mas_chess_dlg_game_monika_win_surr_pre:
    m 1e "Come on, don't give up so easily."
    return

# main monika win by earlt surrenders label
label mas_chess_dlg_game_monika_win_surr:
    python:
        import store.mas_chess as mas_chess

    # bad players get rekt by monika
    if persistent._mas_chess_3_edit_sorry:
        
        # pull a quip and say it
        $ t_quip, v_quip = mas_chess.monika_wins_surr_mean_quips.quip()

        # check quip type
        if t_quip == MASQuipList.TYPE_LABEL:
            # this is a label, call it
            call expression v_quip from _mas_chess_dlggmws3esl

        else: # assume its a line
            # this is a line, call it using 1k expression
            m 1k "[v_quip]"

    else:
        # only the non bad players get the encouragement from monika
        call mas_dlg_game_monika_win_surr_pre from _mas_chess_dlggmwspre

        python:
            # clean chess strength so its within bounds
            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif t_chess_str > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_WIN_SURR_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmwscsl

    return

## monika wins by early surrender quips
# poor resolve
label mas_chess_dlg_game_monika_win_surr_resolve:
    m 1k "Giving up is a sign of poor resolve..."
    m 1h "I don't want a [bf] who has poor resolve."
    return

# have you tried
label mas_chess_dlg_game_monika_win_surr_trying:
    m 1k "Have you considered {i}actually trying{/i}?"
    m 1 "I hear it is beneficial to your mental health."
    return

# winning by surrender, chess strength 0
label mas_chess_dlg_game_monika_win_surr_0:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 1
label mas_chess_dlg_game_monika_win_surr_1:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 2
label mas_chess_dlg_game_monika_win_surr_2:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 3
label mas_chess_dlg_game_monika_win_surr_3:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 4
label mas_chess_dlg_game_monika_win_surr_4:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 5
label mas_chess_dlg_game_monika_win_surr_5:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 6
label mas_chess_dlg_game_monika_win_surr_6:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 7
label mas_chess_dlg_game_monika_win_surr_7:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 8
label mas_chess_dlg_game_monika_win_surr_8:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 9
label mas_chess_dlg_game_monika_win_surr_9:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 10
label mas_chess_dlg_game_monika_win_surr_10:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 11
label mas_chess_dlg_game_monika_win_surr_11:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 12
label mas_chess_dlg_game_monika_win_surr_12:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 13
label mas_chess_dlg_game_monika_win_surr_13:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 14
label mas_chess_dlg_game_monika_win_surr_14:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 15
label mas_chess_dlg_game_monika_win_surr_15:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 16
label mas_chess_dlg_game_monika_win_surr_16:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 17
label mas_chess_dlg_game_monika_win_surr_17:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 18
label mas_chess_dlg_game_monika_win_surr_18:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 19
label mas_chess_dlg_game_monika_win_surr_19:
    jump mas_chess_dlg_game_monika_win_surr_20

# winning by surrender, chess strength 20
label mas_chess_dlg_game_monika_win_surr_20:
    # nothint for now
    return      

## monika loses
# monika lose label start dialogue
label mas_chess_dlg_game_monika_lose_pre:
    m 2a "You won! Congratulations."
    return

# main monika lose label
label mas_chess_dlg_game_monika_lose:
    python:
        import store.mas_chess as mas_chess

    # bad players get rekt by monika
    if persistent._mas_chess_3_edit_sorry:
        
        # pull a quip and say it
        $ t_quip, v_quip = mas_chess.monika_loses_mean_quips.quip()

        # check quip type
        if t_quip == MASQuipList.TYPE_LABEL:
            # this is a label, call it
            call expression v_quip from _mas_chess_dlggml3esl

        else: # assume its a line
            # this is a line, call it using 1q expression
            m 1q "[v_quip]"

    else:
        # only the non bad players get congrats
        call mas_chess_dlg_game_monika_lose_pre from _mas_chess_dlggmlp

        python:
            # clean chess strength so its within bounds
            if persistent.chess_strength < 0:
                persistent.chess_strength = 0
            elif t_chess_str > 20:
                persistent.chess_strength = 20

            chess_strength_label = mas_chess.DLG_MONIKA_LOSE_BASE.format(
                persistent.chess_strength
            )

        call expression chess_strength_label from _mas_chess_dlggmlcsl

    return

# losing, chess strength 0
label mas_chess_dlg_game_monika_lose_0:
    jump mas_chess_dlg_game_monika_lose_2

# losing, chess strength 1
label mas_chess_dlg_game_monika_lose_1:
    jump mas_chess_dlg_game_monika_lose_2

# losing, chess strength 2
label mas_chess_dlg_game_monika_lose_2:
    m 1a "I have to admit, I put less pressure on you than I could have..."
    m "I hope you don't mind! I'll be challenging you more as you get better."
    return

# losing, chess strength 3
label mas_chess_dlg_game_monika_lose_3:
    m 1a "I'll get you next time for sure!"
    return

# losing, chess strength 4
label mas_chess_dlg_game_monika_lose_4:
    m 1a "You played pretty well this game."
    return

# losing, chess strength 5
label mas_chess_dlg_game_monika_lose_5:
    jump mas_chess_dlg_game_monika_lose_6

# losing, chess strength 6
label mas_chess_dlg_game_monika_lose_6:
    m 1a "This game was quite stimulating!"
    return

# losing, chess strength 7
label mas_chess_dlg_game_monika_lose_7:
    m 3a "Excellently played, [player]!"
    return      

# losing, chess strength 8
label mas_chess_dlg_game_monika_lose_8:
    jump mas_chess_dlg_game_monika_lose_10

# losing, chess strength 9
label mas_chess_dlg_game_monika_lose_9:
    jump mas_chess_dlg_game_monika_lose_10

# losing, chess strength 10
label mas_chess_dlg_game_monika_lose_10:
    m 1b "You're quite a strong chess player!"
    return      

# losing, chess strength 11
label mas_chess_dlg_game_monika_lose_11:
    jump mas_chess_dlg_game_monika_lose_12

# losing, chess strength 12
label mas_chess_dlg_game_monika_lose_12:
    m 1d "You're a very challenging opponent, [player]!"
    return      

# losing, chess strength 13
label mas_chess_dlg_game_monika_lose_13:
    jump mas_chess_dlg_game_monika_lose_19

# losing, chess strength 14
label mas_chess_dlg_game_monika_lose_14:
    jump mas_chess_dlg_game_monika_lose_19

# losing, chess strength 15
label mas_chess_dlg_game_monika_lose_15:
    jump mas_chess_dlg_game_monika_lose_19

# losing, chess strength 16
label mas_chess_dlg_game_monika_lose_16:
    # ee for good chess players
    m 2n "I-{w=1}It's not like I let you win or anything, b-{w=1}baka!"
    return      

# losing, chess strength 17
label mas_chess_dlg_game_monika_lose_17:
    jump mas_chess_dlg_game_monika_lose_19

# losing, chess strength 18
label mas_chess_dlg_game_monika_lose_18:
    jump mas_chess_dlg_game_monika_lose_19

# losing, chess strength 19
label mas_chess_dlg_game_monika_lose_19:
    m 3d "Wow! You're amazing at chess."
    m "You could be a professional chess player!"
    return      

# losing, chess strength 20
label mas_chess_dlg_game_monika_lose_20:
    m 3d "Wow!"
    m 1m "Are you sure you're not cheating?"
    return      

#### end dialogue blocks ######################################################

# confirmation screen for chess
screen mas_chess_confirm():

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Are you sure you want to give up?"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action Return(True)
                textbutton _("No") action Return(False)
