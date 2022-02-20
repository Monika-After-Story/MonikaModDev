
            
            
            
init python:
    import pygame
    import re
    import copy
    
    class MASConnect4Displayable(renpy.Displayable):
        # pygame events
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )
        
        # variables to indicate Monika and player's pins/turn
        EMPTY = 0
        AI_PIECE = 1
        PLAYER_PIECE = 2

        PLAYER = 0
        AI = 1
        
        WINDOW_LENGTH = 4
        
        # indicate the board's rows columns
        CEL_COL = 7
        CEL_ROW = 6
        
        BOARD_EMPTY = [[EMPTY for j in range(CEL_COL)] for i in range(CEL_ROW)]
        
        # the  board's dimensions
        BOARD_BORDER_WIDTH = 15
        BOARD_BORDER_HEIGHT = 15
        CEL_WIDTH = 60
        CEL_HEIGHT = 60
        BOARD_WIDTH = BOARD_BORDER_WIDTH * 2 + CEL_WIDTH * CEL_COL
        BOARD_HEIGHT = BOARD_BORDER_HEIGHT * 2 + CEL_HEIGHT * CEL_ROW
        
        # offset for board's position
        DISP_X_OFFSET = 200
        DISP_Y_OFFSET = 200
        
        BOARD_X_POS = int(1280 - BOARD_WIDTH - DISP_X_OFFSET)
        BOARD_Y_POS = int(720 - BOARD_HEIGHT - DISP_Y_OFFSET)
        
        # position of the upper left most cel
        CEL_BASE_X_POS = BOARD_X_POS + BOARD_BORDER_WIDTH
        CEL_BASE_Y_POS = BOARD_Y_POS + BOARD_BORDER_HEIGHT
        
        # dimensions of buttons the player use to drop pins on their turn (AKA col button)
        COL_BUTTON_WIDTH = 60
        COL_BUTTON_HEIGHT = 53
        COL_BUTTON_X_SPACING = 5
        COL_BUTTON_Y_SPACING = 7
        COL_BUTTON_X_DISTANCE = int(COL_BUTTON_WIDTH + COL_BUTTON_X_SPACING)
        
        # menu button dimensions
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        BUTTON_X_SPACING = 10
        BUTTON_Y_SPACING = 10
        BUTTON_Y_DISTANCE = int(BUTTON_HEIGHT + BUTTON_Y_SPACING)
        
        # col button position
        COL_BUTTON_X = int(BOARD_X_POS + BOARD_WIDTH / 2 - COL_BUTTON_WIDTH / 2)
        COL_BUTTON_Y = int(BOARD_Y_POS - COL_BUTTON_HEIGHT - COL_BUTTON_Y_SPACING)
        
        # menu button position
        BUTTON_X = BOARD_X_POS + BOARD_WIDTH + BUTTON_X_SPACING
        BUTTON_Y = BOARD_Y_POS + BOARD_HEIGHT - BUTTON_HEIGHT
        
        # images definition
        AI_IMAGE = Image("mod_assets/games/connect4/monika_pin.png")
        PLAYER_IMAGE = Image("mod_assets/games/connect4/player_pin.png")
        BOARD_IMAGE = Image("mod_assets/games/connect4/connect4_board.png")
        WIN_TILE_IMAGE = Image("mod_assets/games/connect4/win_tile.png")
        COL_BUTTON_IDLE_IMAGE = Image("mod_assets/games/connect4/arrow_down_idle.png")
        COL_BUTTON_HOVER_IMAGE = Image("mod_assets/games/connect4/arrow_down_hover.png")
        COL_BUTTON_INSENSITIVE_IMAGE = Image("mod_assets/games/connect4/arrow_down_insensitive.png")
        
        def __init__(self, first_turn, depth):
            # prepare the Displayable
            super(MASConnect4Displayable, self).__init__()
            
            # init the variables
            self.game_over = False
            self.quit_game = False
            self.turn = first_turn
            self.board = copy.deepcopy(self.BOARD_EMPTY)
            self.winner = False
            self.win_tiles = set()
            self.depth = depth
            
            # init col buttons
            self._col_buttons = list()
            for i in range(self.CEL_COL):
                button = MASButtonDisplayable(
                    Null(),
                    Null(),
                    Null(),
                    Frame(self.COL_BUTTON_IDLE_IMAGE, Borders(0, 0, 0, 0)),
                    Frame(self.COL_BUTTON_HOVER_IMAGE, Borders(0, 0, 0, 0)),
                    Frame(self.COL_BUTTON_INSENSITIVE_IMAGE, Borders(0, 0, 0, 0)),
                    MASConnect4Displayable.COL_BUTTON_X + MASConnect4Displayable.COL_BUTTON_X_DISTANCE * (i - 3),
                    MASConnect4Displayable.COL_BUTTON_Y,
                    MASConnect4Displayable.COL_BUTTON_WIDTH,
                    MASConnect4Displayable.COL_BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound,
                    return_value=i
                )
                self._col_buttons.append(button)
                
            # init menu buttons
            self._button_quit = MASButtonDisplayable.create_stb(
                _("Quit"),
                True,
                MASConnect4Displayable.BUTTON_X,
                MASConnect4Displayable.BUTTON_Y,
                MASConnect4Displayable.BUTTON_WIDTH,
                MASConnect4Displayable.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
                
            self._button_done = MASButtonDisplayable.create_stb(
                _("Done"),
                False,
                MASConnect4Displayable.BUTTON_X,
                MASConnect4Displayable.BUTTON_Y,
                MASConnect4Displayable.BUTTON_WIDTH,
                MASConnect4Displayable.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )
            
            self._visible_buttons = [
                self._button_quit
            ]
            
            self._visible_buttons_winner = [
                self._button_done
            ]
        
        def render(self, width, height, st, at):
            """
            This function shows the board into the screen
            """
            render = renpy.Render(width, height)
            
            # prepare the board as renderer
            board = renpy.render(MASConnect4Displayable.BOARD_IMAGE, 1280, 720, st , at)
            
            # prepare col buttons as renderers
            # (they look the same, but their return values are different on init, thus, they are put in a list)
            col_buttons = [
                (b.render(width, height, st, at), b.xpos, b.ypos)
                for b in self._col_buttons
            ]
            
            # prepare menu buttons as renderers
            visible_buttons = list()
            if self.game_over:
                visible_buttons = [
                    (b.render(width, height, st, at), b.xpos, b.ypos)
                    for b in self._visible_buttons_winner
                ]
            else:
                visible_buttons = [
                    (b.render(width, height, st, at), b.xpos, b.ypos)
                    for b in self._visible_buttons
                ]
            
            # draw the board
            render.blit(board, (MASConnect4Displayable.BOARD_X_POS, MASConnect4Displayable.BOARD_Y_POS))
            
            if self.win_tiles:
                # prepare winning tile highlight as renderer
                win_tile = renpy.render(MASConnect4Displayable.WIN_TILE_IMAGE, 1280, 720, st , at)
                
                # draw winning tile highlights
                for t in self.win_tiles:
                    y, x = ((-int(t[0])+5) * MASConnect4Displayable.CEL_WIDTH, int(t[1]) * MASConnect4Displayable.CEL_HEIGHT)
                    render.blit(win_tile, (MASConnect4Displayable.CEL_BASE_X_POS + x, MASConnect4Displayable.CEL_BASE_Y_POS + y))
            
            for i in self.board:
                if self.PLAYER_PIECE in i:
                    # prepare the pins as renderer
                    player_pin = renpy.render(MASConnect4Displayable.PLAYER_IMAGE, 1280, 720, st , at)
                    break
            
            for i in range(len(self.board)):
                if self.PLAYER_PIECE in self.board[i]:
                    # draw the player pins
                    for j in range(len(self.board[i])):
                        y, x = ((-i+5) * MASConnect4Displayable.CEL_WIDTH, j * MASConnect4Displayable.CEL_HEIGHT)
                        if self.board[i][j] == self.PLAYER_PIECE:
                            render.blit(player_pin, (MASConnect4Displayable.CEL_BASE_X_POS + x, MASConnect4Displayable.CEL_BASE_Y_POS + y))
            
            for i in self.board:
                if self.AI_PIECE in i:
                    # prepare the AI pins as renderer
                    ai_pin = renpy.render(MASConnect4Displayable.AI_IMAGE, 1280, 720, st , at)
            
            for i in range(len(self.board)):
                if self.AI_PIECE in self.board[i]:
                    # draw the AI pins
                    for j in range(len(self.board[i])):
                        y, x = ((-i+5) * MASConnect4Displayable.CEL_WIDTH, j * MASConnect4Displayable.CEL_HEIGHT)
                        if self.board[i][j] == self.AI_PIECE:
                            render.blit(ai_pin, (MASConnect4Displayable.CEL_BASE_X_POS + x, MASConnect4Displayable.CEL_BASE_Y_POS + y))
                    
            # draw col buttons
            for b in col_buttons:
                render.blit(b[0], (b[1], b[2]))
                
            # draw menu buttons
            for b in visible_buttons:
                render.blit(b[0], (b[1], b[2]))
            
            renpy.redraw(self, 0)
            return render
            
        def set_button_states(self):
            """
            Disable/enable buttons according to other variables
            """
            if not self.game_over and self.turn == self.PLAYER:
            
                for b in range(len(self._col_buttons)):
                    if self.board[5][b] == self.EMPTY:
                        self._col_buttons[b].enable()
                    else:
                        self._col_buttons[b].disable()
                
                self._button_quit.enable()
                
                self._button_done.disable()
                
            else:
            
                for b in self._col_buttons:
                    b.disable()
                
                self._button_quit.disable()
                
                self._button_done.enable()
            
        def event(self, ev, x, y, st):
            """
            Function for events. Is called internally by renpy on its own (i guess)
            """
            if ev.type in self.MOUSE_EVENTS:
                ret_value = None
                for b in self._col_buttons:
                    if type(b.event(ev, x, y, st)) is int:
                        ret_value = b.event(ev, x, y, st)
                        
                        row = self.get_next_open_row(self.board, ret_value)
                        self.drop_piece(self.board, row, ret_value, self.PLAYER_PIECE)
                        
                        return "mouse_button_up"
                
                if self._visible_buttons or self._visible_buttons_winner:
                    ret_value = self.check_buttons(ev, x, y, st)

                if ret_value is not None:
                    return ret_value
                    
            return None
            
        def check_buttons(self, ev, x, y, st):
            """
            Checks if menu buttons are pressed
            """
            if self.game_over:
                if self._button_done.event(ev, x, y, st):
                    self.quit_game = True
                    return (self.winner, 0)
                    
            elif self.turn == self.PLAYER:
                if self._button_quit.event(ev, x, y, st):
                    self.quit_game = True
                    return (self.winner, 1)

        def show(self):
            """
            Shows this displayable
            """
            ui.layer("minigames")
            ui.implicit_add(self)
            ui.close()

        def hide(self):
            """
            Hides this displayable
            """
            ui.layer("minigames")
            ui.remove(self)
            ui.close()
                
        def player_move(self):
            """
            Player makes a move
            """
            interact = ui.interact(type="minigame")
            return interact
            
        def ai_move(self):
            col, minimax_score = self.minimax(self.board, self.depth, -float("inf"), float("inf"), True)

            if self.is_valid_location(self.board, col):
                row = self.get_next_open_row(self.board, col)
                self.drop_piece(self.board, row, col, self.AI_PIECE)
                
        def game_loop(self):
            """
            The game loop where things happen
            """
            while not self.quit_game:
                self.set_button_states()
                
                if self.turn == self.AI and not self.game_over:
                    renpy.pause(1.5)
                    self.ai_move()
                else:
                    interact = self.player_move()
                
                    if self.quit_game:
                        return interact

                self.turn += 1
                self.turn = self.turn % 2
                
                # evaluate the board if there's any win
                player_win = self.winning_move(self.board, self.PLAYER_PIECE)
                if player_win:
                    self.winner = self.PLAYER_PIECE
                    self.win_tiles = player_win
                    self.game_over = True
                ai_win = self.winning_move(self.board, self.AI_PIECE)
                if ai_win:
                    self.winner = self.AI_PIECE
                    self.win_tiles = ai_win
                    self.game_over = True
        
        

        def drop_piece(self, board, row, col, piece):
            board[row][col] = piece

        def is_valid_location(self, board, col):
            return board[self.CEL_ROW-1][col] == 0

        def get_next_open_row(self, board, col):
            for r in range(self.CEL_ROW):
                if board[r][col] == 0:
                    return r

        def winning_move(self, board, piece):
            """
            Check if there's a win on the board. Returns the tiles where that win is found
            """
            # check horizontal locations for win
            for c in range(self.CEL_COL-3):
                for r in range(self.CEL_ROW):
                    if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        return (str(r)+str(c), str(r)+str(c+1), str(r)+str(c+2), str(r)+str(c+3))

            # check vertical locations for win
            for c in range(self.CEL_COL):
                for r in range(self.CEL_ROW-3):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        return (str(r)+str(c), str(r+1)+str(c), str(r+2)+str(c), str(r+3)+str(c))

            # check positively sloped diaganols
            for c in range(self.CEL_COL-3):
                for r in range(self.CEL_ROW-3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return (str(r)+str(c), str(r+1)+str(c+1), str(r+2)+str(c+2), str(r+3)+str(c+3))

            # check negatively sloped diaganols
            for c in range(self.CEL_COL-3):
                for r in range(3, self.CEL_ROW):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return (str(r)+str(c), str(r-1)+str(c+1), str(r-2)+str(c+2), str(r-3)+str(c+3))
            
            return False

        def evaluate_window(self, window, piece):
            """
            Evaluate an individual window. Used in tandem with score_position()
            """
            score = 0
            opp_piece = self.PLAYER_PIECE
            if piece == self.PLAYER_PIECE:
                opp_piece = self.AI_PIECE

            if window.count(piece) == 4:
                score += 100
            elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
                score += 5
            elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
                score += 2

            if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
                score -= 4

            return score

        def score_position(self, board, piece):
            """
            Is used by the AI when looking ahead of a possible move to score the whole board
            """
            score = 0

            # score center column
            center_array = list()
            for i in board:
                center_array.append(int(i[self.CEL_COL//2]))
            center_count = center_array.count(piece)
            score += center_count * 3

            # score Horizontal
            for r in range(self.CEL_ROW):
                row_array = [int(i) for i in list(board[r])]
                for c in range(self.CEL_COL-3):
                    window = row_array[c:c+self.WINDOW_LENGTH]
                    score += self.evaluate_window(window, piece)

            # score Vertical
            for c in range(self.CEL_COL):
                col_array = list()
                for i in board:
                    col_array.append(int(i[c]))
                for r in range(self.CEL_ROW-3):
                    window = col_array[r:r+self.WINDOW_LENGTH]
                    score += self.evaluate_window(window, piece)

            # score posiive sloped diagonal
            for r in range(self.CEL_ROW-3):
                for c in range(self.CEL_COL-3):
                    window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                    score += self.evaluate_window(window, piece)

            for r in range(self.CEL_ROW-3):
                for c in range(self.CEL_COL-3):
                    window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                    score += self.evaluate_window(window, piece)

            return score

        def is_terminal_node(self, board):
            """
            Determines if theres any win on the board or if there is still possible move to be made
            """
            return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

        def minimax(self, board, depth, alpha, beta, maximizingPlayer):
            """
            minimax() is a recursive function used to evaluate every possible step ahead on the board.
            The amount of step ahead to evaluate is determined by the depth parameter.
            """
            valid_locations = self.get_valid_locations(board)
            is_terminal = self.is_terminal_node(board)
            if depth == 0 or is_terminal:
                if is_terminal:
                    if self.winning_move(board, self.AI_PIECE):
                        return (None, 100000000000000)
                    elif self.winning_move(board, self.PLAYER_PIECE):
                        return (None, -10000000000000)
                    else: # game is over, no more valid moves
                        return (None, 0)
                else: # depth is zero
                    return (None, self.score_position(board, self.AI_PIECE))
            if maximizingPlayer:
                value = -float("inf")
                column = random.choice(valid_locations)
                for col in valid_locations:
                    row = self.get_next_open_row(board, col)
                    b_copy = copy.deepcopy(board)
                    self.drop_piece(b_copy, row, col, self.AI_PIECE)
                    new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        column = col
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return column, value

            else: # minimizing player
                value = float("inf")
                column = random.choice(valid_locations)
                for col in valid_locations:
                    row = self.get_next_open_row(board, col)
                    b_copy = copy.deepcopy(board)
                    self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                    new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        column = col
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
                return column, value

        def get_valid_locations(self, board):
            valid_locations = []
            for col in range(self.CEL_COL):
                if self.is_valid_location(board, col):
                    valid_locations.append(col)
            return valid_locations
        
    
    
label game_connect4:
    m 2esa "Wanna play connect 4?"
    $ connect4_play_again = True
    while connect4_play_again:
        m 3eub "First, let's flip a coin."
        $ choice = random.randint(0, 1) == 0
        if choice:
            $ connect4_first_turn = 0
            m 2eua "Oh, looks like you go first, [player]."
        else:
            $ connect4_first_turn = 1
            m 2eua "Looks like I go first, [player]."
        m 2hua "Let's start~!"
        
        label start_connect4:
            pass
            
        window hide None
        show monika 1eua at t21
        python:
            quick_menu = False
            
            # The AI Difficulty #
            connect4_depth = 4
            
            connect4_displayable_obj = MASConnect4Displayable(connect4_first_turn, connect4_depth)
            connect4_displayable_obj.show()
            results = connect4_displayable_obj.game_loop()
            connect4_displayable_obj.hide()
            
            quick_menu = True
            
            connect4_winner, connect4_ending = results
            
        label .connect4_end:
            pass

        show monika at t11
                
        if connect4_winner == MASConnect4Displayable.AI_PIECE:
            m 2wub "I won!"
            m 2tsa "Better luck next time, [player]."
            
        elif connect4_winner == MASConnect4Displayable.PLAYER_PIECE:
            m 2wub "Oh, you won."
            m 2tfa "You're lucky this time."
        
        # if the game ends with no winner, player either quits before the game ends or it's a draw
        else:
            if connect4_ending == 0:
                m 2wud "Oh, it's a draw."
                m 2rksdlb "I mean, I saw it coming, but it's quite a rare circumstance."
            elif connect4_ending == 1:
                m 6ekc "Oh? You want to quit?"
                m 6eksdld "But I was having so much fun, [player]."
                m 1gksdlc "Oh well..."
                m 1eka "Let's play again some time."
                $ connect4_play_again = False
        
        # we check for connect4_ending again because the quit ending doesn't prompt this question
        if connect4_ending == 0:
            m 2eua "Do you want to play again?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want to play again?{fast}"
                
                "Yes.":
                    pass
                "No.":
                    m "Alright, then."
                    m 1eka "Let's play again some time."
                    $ connect4_play_again = False
    return
            
            
            
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_unlock_connect4",
            conditional="store.mas_xp.level() >= 0",
            # action=EV_ACT_QUEUE,
            action=EV_ACT_PUSH,
            # aff_range=(mas_aff.AFFECTIONATE, None)
            aff_range=(None, None)
        )
    )

label mas_unlock_connect4:
    m 2hua "Hey! I've got something exciting to tell you!"
    m 2eua "I've finally added connect 4 for us to play, [player]."
    $ mas_unlockGame("connect 4")
    return



















