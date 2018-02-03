
# we now will keep track of player wins / losses/ draws/ whatever
default persistent._mas_chess_stats = {"wins": 0, "losses": 0, "draws": 0}
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
                    self._button_save.disabled = True
                    self._button_giveup.disabled = True
                elif self.board.fullmove_number <= 4:
                    self._button_save.disabled = True

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
                            self._button_giveup.disabled = False

                            # enable button only after 4th move
                            if self.num_turns > 4:
                                self._button_save.disabled = False

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
                            if str(piece) == "k" and result == "0-1":
                                r.blit(highlight_red, (x, y))

                            # white won
                            elif str(piece) == "K" and result == "1-0":
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
                            self._button_save.disabled = True
                            self._button_giveup.disabled = True

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
    hide screen keylistener
    m 1b "You want to play chess? Alright~"
#   m 2a "Double click your king if you decide to surrender."
    m 1a "Get ready!"
    call demo_minigame_chess from _call_demo_minigame_chess
    return

label demo_minigame_chess:
    $ import chess.pgn # imperative for chess saving/loading
    $ import os # we need it for filework

    # NOTE: games CANNOT be deleted from here. maybe mention that if you
    # want to delete games, you have to delete them from the folder?

    # first, check for existing games
    $ pgn_files = os.listdir(mas_chess.CHESS_SAVE_PATH)
    $ loaded_game = None
    if pgn_files:
        python:
            # only allow valid pgn files
            pgn_games = list()
            for filename in pgn_files:
                in_prog_game = mas_chess.isInProgressGame(
                    filename,
                    mas_monika_twitter_handle
                )

                if in_prog_game:
                    pgn_games.append((
                        in_prog_game[0],
                        in_prog_game[1],
                        False,
                        False
                    ))

        # now check if we have any games to show
        if len(pgn_games) > 0:
            if len(pgn_games) == 1:
                $ game_s_dialog = "a game"
            else:
                $ game_s_dialog = "some games"

            python:
                # sort the games
                pgn_games.sort()
                pgn_games.reverse()

            # need to add the play new game option
            $ pgn_games.append(mas_chess.CHESS_MENU_NEW_GAME_ITEM)
            
            m 1a "We still have [game_s_dialog] in progress."
            show monika at t21
            $ renpy.say(m, "Pick a game you'd like to play.", interact=False)

            call screen mas_gen_scrollable_menu(pgn_games, mas_chess.CHESS_MENU_AREA, mas_chess.CHESS_MENU_XALIGN, mas_chess.CHESS_MENU_FINAL_ITEM)

            show monika at t11
            $ loaded_game = _return

            # check if user backs out
            if loaded_game == mas_chess.CHESS_MENU_FINAL_VALUE:
                m "Alright, maybe later?"
                return
            
            # check if user picked a game
            if loaded_game != mas_chess.CHESS_MENU_NEW_GAME_VALUE:

                # now figure out the player color
                if loaded_game.headers["White"] == mas_monika_twitter_handle:
                    $ player_color = ChessDisplayable.COLOR_BLACK
                else:
                    $ player_color = ChessDisplayable.COLOR_WHITE
                jump mas_chess_game_start

    # otherwise, new games only
    $ loaded_game = None
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

    python:
        ui.add(ChessDisplayable(player_color, pgn_game=loaded_game))
        results = ui.interact(suppress_underlay=True)

        # unpack results
        new_pgn_game, is_monika_winner, is_surrender, num_turns = results

        # game result header
        game_result = new_pgn_game.headers["Result"]

    #Regenerate the spaceroom scene
    #$scene_change=True #Force scene generation
    #call spaceroom from _call_spaceroom

    # check results
    if game_result == "*":
        # this should jump directly to (the twilight zone) the save game
        # name input flow.
        jump mas_chess_savegame

    elif game_result == "1/2-1/2":
        # draw
        m 3h "A draw? How boring..."
        $ persistent._mas_chess_stats["draws"] += 1

    elif is_monika_winner:
        $ persistent._mas_chess_stats["losses"] += 1
        if is_surrender and num_turns <= 4:
            m 1e "Come on, don't give up so easily."
        else:
            m 1b "I win!"

        if persistent.chess_strength>0:
            m 1j "I'll go a little easier on you next time."
            $persistent.chess_strength += -1
        else:
            m 1l "I really was going easy on you!"

    else:
        $ persistent._mas_chess_stats["wins"] += 1
        #Give player XP if this is their first win
        if not persistent.ever_won['chess']:
            $persistent.ever_won['chess'] = True
            $grant_xp(xp.WIN_GAME)

        m 2a "You won! Congratulations."
        if persistent.chess_strength<20:
            m 2 "I'll get you next time for sure!"
            $persistent.chess_strength += 1
        else:
            m 2b "You really are an amazing player!"
            m 3l "Are you sure you're not cheating?"

    # we only save a game if they put in some effort
    if num_turns > 4:
        menu:
            m "Would you like to save this game?"
            "Yes":
                label mas_chess_savegame:
                    python:
                        if loaded_game: # previous game exists
                            new_pgn_game.headers["Event"] = (
                                loaded_game.headers["Event"]
                            )
                        
                        # otherwise ask for name
                        else:
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
                        save_filename = (
                            new_pgn_game.headers["Event"] + 
                            mas_chess.CHESS_SAVE_EXT
                        )

                        # now setup the file path
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
            "No":
                # TODO: should there be dialogue here?
                pass

label mas_chess_playagain:
    menu:
        m "Do you want to play again?"

        "Yes":
            jump demo_minigame_chess
        "No":
            pass

label mas_chess_end:
    if is_monika_winner:
        m 2d "Despite its simple rules, chess is a really intricate game."
        m 1a "It's okay if you find yourself struggling at times."
        m 1j "Remember, the important thing is to be able to learn from your mistakes."
    elif game_result == "*":
        m 1a "TODO: okay lets play again soon"
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
