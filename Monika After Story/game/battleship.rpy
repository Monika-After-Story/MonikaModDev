# # # MAS BATTLESHPS YO


# GAME PERSISTENT VARIABLES
default persistent._mas_game_battleship_stats = {
    "Monika": {
        "total_shots": 0,
        "total_hits": 0,
        "best_attack": store.mas_battleship.Grid.WIDTH * store.mas_battleship.Grid.HEIGHT,
        "best_defence": 0,
    },
    "Player": {
        "total_shots": 0,
        "total_hits": 0,
        "best_attack": store.mas_battleship.Grid.WIDTH * store.mas_battleship.Grid.HEIGHT,
        "best_defence": 0,
    },
}
default persistent._mas_game_battleship_wins = {"Monika": 0, "Player": 0}
default persistent._mas_game_battleship_abandoned = 0
default persistent._mas_game_battleship_player_ship_dataset = {
    (col, row): 0
    for row in range(store.mas_battleship.Grid.HEIGHT)
    for col in range(store.mas_battleship.Grid.WIDTH)
}
default persistent._mas_game_battleship_dataset_counter = 0
default persistent._mas_pm_has_battleship_debug = False


# GAME SCREEN STYLES
style mas_battleship_main_vbox is vbox:
    xalign 1.0
    xoffset -mas_battleship.Battleship.GRID_SPACING
    yalign 0.0
    yoffset mas_battleship.Battleship.GRID_SPACING
    xmaximum 2*mas_battleship.Battleship.GRID_WIDTH + mas_battleship.Battleship.GRID_SPACING
    ymaximum config.screen_height
    xfill False
    yfill False
    spacing mas_battleship.Battleship.GRID_SPACING

style mas_battleship_top_vbox is vbox:
    spacing mas_battleship.Battleship.GRID_SPACING

style mas_battleship_current_turn_frame is frame:
    xalign 0.0
    xminimum 200

style mas_battleship_text is text

style mas_battleship_text_dark is text:
    color "#FD5BA2"

style mas_battleship_top_buttons_frame is frame:
    xalign 1.0

style mas_battleship_top_buttons_hbox is hbox:
    spacing 0

style mas_battleship_game_frame is frame:
    background None
    padding (0, 0, 0, 0)
    xsize mas_battleship.Battleship.GRID_WIDTH * 2 + mas_battleship.Battleship.GRID_SPACING
    ysize mas_battleship.Battleship.GRID_HEIGHT
    xalign 0.0

style mas_battleship_instruction_frame is frame:
    xalign 1.0
    xsize mas_battleship.Battleship.GRID_WIDTH
    ysize mas_battleship.Battleship.GRID_HEIGHT

style mas_battleship_instruction_vbox is vbox:
    spacing 15
    align (0.5, 0.5)

style mas_battleship_instruction_text is text:
    xalign 0.5
    text_align 0.5

style mas_battleship_instruction_text_dark is text:
    xalign 0.5
    text_align 0.5
    color "#FD5BA2"

style mas_battleship_scoreboard_frame is frame:
    background None
    padding (0, 0, 0, 0)
    # HACK: without ymaximum this frame keeps expanding, even though it knows its children size and had yfill False
    # probably a bug in renpy
    ymaximum 0
    yfill False
    xalign 0.0

style mas_battleship_player_score_frame is frame:
    xalign 0.0
    xminimum 132

style mas_battleship_monika_score_frame is frame:
    xalign 0.0
    xoffset mas_battleship.Battleship.GRID_WIDTH + mas_battleship.Battleship.GRID_SPACING
    xminimum 132


# GAME SCREEN
screen mas_battleship_ui(game):
    layer "minigames"

    vbox:
        style "mas_battleship_main_vbox"

        vbox:
            style "mas_battleship_top_vbox"

            frame:
                style "mas_battleship_current_turn_frame"

                vbox:
                    python:
                        if game.is_player_turn():
                            turn = store.player
                        else:
                            turn = _("Monika")

                        target = game.get_hovering_square()

                    text _("Turn: [turn]"):
                        style "mas_battleship_text"
                    text _("Target: [target]"):
                        style "mas_battleship_text"

            frame:
                style "mas_battleship_top_buttons_frame"

                hbox:
                    style "mas_battleship_top_buttons_hbox"

                    textbutton _("Ready"):
                        action Function(game.set_phase_action)
                        sensitive game.is_sensitive and game.is_in_preparation() and game.can_start_action()

                    textbutton _("Randomize"):
                        action Function(game.build_and_place_player_ships)
                        sensitive game.is_sensitive and game.is_in_preparation()

                    textbutton _("Give up"):
                        action [
                            Function(game.mark_player_gaveup),
                            Function(game.set_phase_done),
                        ]
                        sensitive not game.is_done()

        frame:
            style "mas_battleship_game_frame"

            add game:
                xalign 1.0

            if game.is_in_preparation() or game.did_player_cancel_game():
                frame:
                    style "mas_battleship_instruction_frame"

                    vbox:
                        style "mas_battleship_instruction_vbox"

                        text _("Click and drag to move a ship"):
                            style "mas_battleship_instruction_text"
                        text _("Press {i}R{/i} or {i}Shift{/i}+{i}R{/i} to rotate a ship"):
                            style "mas_battleship_instruction_text"
                        text _("Press {i}Randomize{/i} to reposition the ships"):
                            style "mas_battleship_instruction_text"
                        text _("Press {i}Ready{/i} to start the game"):
                            style "mas_battleship_instruction_text"
                        text _("Click on a square to shoot"):
                            style "mas_battleship_instruction_text"

        if not game.is_in_preparation() and not game.did_player_cancel_game():
            frame:
                style "mas_battleship_scoreboard_frame"

                frame:
                    style "mas_battleship_player_score_frame"

                    vbox:
                        python:
                            ph = game.get_player_hits_count()
                            pm = game.get_player_misses_count()
                        text _("Hits: [ph]"):
                            style "mas_battleship_text"
                        text _("Misses: [pm]"):
                            style "mas_battleship_text"

                frame:
                    style "mas_battleship_monika_score_frame"

                    vbox:
                        python:
                            mh = game.get_monika_hits_count()
                            mm = game.get_monika_misses_count()
                        text _("Hits: [mh]"):
                            style "mas_battleship_text"
                        text _("Misses: [mm]"):
                            style "mas_battleship_text"


# GAME FLOW LABELS
label mas_battleship_game_start:
    window hide
    $ HKBHideButtons()
    $ disable_esc()
    # There's some weird issue when right clicking multiple times during Monika's turn
    # We just get stuck, probably some issue due to window_hide MAS uses is spawning a new context
    # Unsure, but let's just disable it
    $ mas_hotkeys.no_window_hiding = True

    $ mas_battleship.game = mas_battleship.Battleship()
    # $ renpy.start_predict(mas_battleship.game)
    $ mas_battleship.game.build_and_place_monika_ships()
    $ mas_battleship.game.build_and_place_player_ships()

    show monika 1eua at t31
    show screen mas_battleship_ui(mas_battleship.game)

    pause 0.5

    $ mas_battleship.game.pick_first_player()
    $ rng = random.random()
    if mas_battleship.game.is_player_turn():
        if rng < 0.25:
            m 3eub "Your turn is first, [mas_get_player_nickname()]."
        elif rng < 0.5:
            m 3eua "You'll shoot first."
        elif rng < 0.75:
            m 3eua "You got first turn, [player]"
        else:
            m 3eua "Your turn."
    else:
        if rng < 0.25:
            m 3hub "First turn is mine~"
        elif rng < 0.50:
            m 3eua "I take first turn."
        elif rng < 0.75:
            m 3eua "I have first turn."
        else:
            m 3eua "I'll be playing first."
    $ del rng

    m 1eub "Position your ships."
    show monika 1eua

    $ mas_battleship.game.is_sensitive = True

    # FALL THROUGH

label mas_battleship_game_loop:
    # NOTE: the while cycle is out of the game_loop function to properly work with rollback for devs
    while not mas_battleship.game.is_done():
        $ mas_battleship.game.game_loop()

    pause 1.0
    # FALL THROUGH

label mas_battleship_game_end:
    python:
        if mas_battleship.game.get_turn_count() > 1:
            mas_battleship.collect_player_data(mas_battleship.game)
        mas_battleship.update_stats(mas_battleship.game)

        moni_wins = mas_battleship.get_monika_wins()
        player_wins = mas_battleship.get_player_wins()
        rng = random.random()

    if mas_battleship.game.is_player_winner():
        $ mas_battleship.increment_player_wins()

        if player_wins > 5 and player_wins > moni_wins and rng < 0.3:
            m 1hua "Another win for you!"
            m 3hub "Well done, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"

        else:
            m 1hub "Congrats, [player]!{w=0.2} {nw}"
            extend 3hub "You won~"

    elif mas_battleship.game.is_monika_winner():
        $ mas_battleship.increment_monika_wins()

        if moni_wins > 5 and moni_wins > player_wins and rng < 0.3:
            m 3hub "Yet another win for me!"
            m 1hua "Ehehe~"

        else:
            m 1wub "I won!"
            m 1tuu "Better luck next time, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]~"
            m 1hua "Ehehe~"

    elif mas_battleship.game.did_player_giveup():
        if mas_battleship.game.get_turn_count() <= 1:
            m 2etc "But we didn't even get started."
            m 7eka "In any case, if you change your mind again, let me know."
            m 1ekb "I'm always happy to play a game with you."

        else:
            $ mas_battleship.increment_player_surrenders()
            $ mas_battleship.increment_monika_wins()

            if mas_battleship.game.get_turn_count() < 20:
                m 2ekc "Giving up so early, [player]?"
                m 7ekb "I think we were going for a really interesting game there."

            else:
                m 2ekc "Aww, giving up, [player]?"
                m 7ekd "I really wanted to finish this one."

            m 1eka "Let's finish the game next time?"

    else:
        $ mas_battleship.log_err("invalid game phase when reached mas_battleship_game_end label")
        m 2wuo "[player], you shouldn't be able to see this! Is it a bug?"

    # Only suggest to play again if player finished last game
    if mas_battleship.game.is_player_winner() or mas_battleship.game.is_monika_winner():
        $ play_again_question = random.choice((
            _("How about we play more?"),
            _("Would you like to play another game?"),
            _("Let's play again?"),
            _("Let's play more?"),
        ))
        m 3eua "[play_again_question]{nw}"
        $ _history_list.pop()
        menu:
            m "[play_again_question]{fast}"

            "Sure.":
                show monika 1hua
                $ mas_battleship.visit_game_ev()
                jump mas_battleship_game_start

            "Maybe later.":
                m 1eua "Alright."

    hide screen mas_battleship_ui
    # $ renpy.stop_predict(mas_battleship.game)
    show monika at t11

    $ mas_battleship.game = None

    $ mas_hotkeys.no_window_hiding = False
    $ enable_esc()
    $ HKBShowButtons()
    window auto

    return


# GAME IMPLEMENTATION
init -30 python in mas_battleship:
    import math as meth

    # @renpy.atl_warper
    def _water_transform_warper(t):
        """
        Custom warper for time interpolation
        Based on: https://easings.net/#easeInOutBack
        Graph: https://www.desmos.com/calculator/wwt6eqizfb
        """
        c1 = -3.8
        c2 = c1 * 1.525

        if t < 0.5:
            return (meth.pow(2*t, 2) * ((c2 + 1)*2*t - c2)) / 2.0

        else:
            return (meth.pow(2*t - 2, 2) * ((c2 + 1)*(t*2 - 2) + c2) + 2) / 2.0

init -20:
    transform mas_battleship_water_transform(width, height):
        animation

        subpixel True
        anchor (0.0, 0.0)

        block:
            crop (0, 0, width//2, height//2)
            linear 30.0 crop (width//8, height//16, width//2, height//2)
            warp mas_battleship._water_transform_warper 70.0 crop (width//2, height//2, width//2, height//2)
            repeat

init -10 python in mas_battleship:
    import datetime
    import random
    import pygame
    import math as meth
    import itertools

    from collections import (
        OrderedDict,
        Counter,
    )
    from renpy import store
    from store import (
        persistent,
        Image,
        Transform,
        ConditionSwitch,
    )
    from store.mas_utils import (
        mas_log,
        weightedChoice,
    )

    # The game object, will be set on game start
    game = None

    def log_err(msg):
        """
        Logs an error during the Battleship game

        IN:
            msg - str - err msg
        """
        mas_log.error("Battleship: {}".format(msg))


    class ShipType(object):
        """
        Represent available ship types for the game
        TODO: replace with real enum
        """
        CARRIER = 0
        BATTLESHIP = 1
        SUBMARINE = 2
        CRUISER = 3
        DESTROYER = 4


    def _update_accuracy(game):
        persistent._mas_game_battleship_stats["Monika"]["total_shots"] += game.get_monika_hits_count() + game.get_monika_misses_count()
        persistent._mas_game_battleship_stats["Monika"]["total_hits"] += game.get_monika_hits_count()
        persistent._mas_game_battleship_stats["Player"]["total_shots"] += game.get_player_hits_count() + game.get_player_misses_count()
        persistent._mas_game_battleship_stats["Player"]["total_hits"] += game.get_player_hits_count()

    def _update_best_monika_game(game):
        if not game.is_monika_winner():
            return

        attack = persistent._mas_game_battleship_stats["Monika"]["best_attack"]
        new_attack = game.get_monika_hits_count() + game.get_monika_misses_count()
        if new_attack < attack:
            persistent._mas_game_battleship_stats["Monika"]["best_attack"] = new_attack

        defence = persistent._mas_game_battleship_stats["Monika"]["best_defence"]
        new_defence = game._monika.get_total_ship_health_remaining()
        if new_defence > defence:
            persistent._mas_game_battleship_stats["Monika"]["best_defence"] = new_defence

    def _update_best_player_game(game):
        if not game.is_player_winner():
            return

        attack = persistent._mas_game_battleship_stats["Player"]["best_attack"]
        new_attack = game.get_player_hits_count() + game.get_player_misses_count()
        if new_attack < attack:
            persistent._mas_game_battleship_stats["Player"]["best_attack"] = new_attack

        defence = persistent._mas_game_battleship_stats["Player"]["best_defence"]
        new_defence = game._player.get_total_ship_health_remaining()
        if new_defence > defence:
            persistent._mas_game_battleship_stats["Player"]["best_defence"] = new_defence

    def update_stats(game):
        _update_accuracy(game)
        _update_best_monika_game(game)
        _update_best_player_game(game)

    def _get_accuracy_for(key):
        if key not in ("Monika", "Player"):
            return 0.0
        shots = persistent._mas_game_battleship_stats[key]["total_shots"]
        hits = persistent._mas_game_battleship_stats[key]["total_hits"]
        if shots == 0:
            return 0.0
        return round(float(hits) / shots, 3)

    def get_monika_accuracy():
        return _get_accuracy_for("Monika")

    def get_player_accuracy():
        return _get_accuracy_for("Player")

    def _get_best_scores_for(key):
        if key not in ("Monika", "Player"):
            return (Grid.WIDTH * Grid.HEIGHT, 0)

        return (
            persistent._mas_game_battleship_stats[key]["best_attack"],
            persistent._mas_game_battleship_stats[key]["best_defence"],
        )

    def get_best_monika_scores():
        return _get_best_scores_for("Monika")

    def get_best_player_scores():
        return _get_best_scores_for("Player")

    def increment_monika_wins():
        persistent._mas_game_battleship_wins["Monika"] += 1

    def increment_player_wins():
        persistent._mas_game_battleship_wins["Player"] += 1
        if not persistent._mas_ever_won["battleship"]:
            persistent._mas_ever_won["battleship"] = True

    def increment_player_surrenders():
        persistent._mas_game_battleship_abandoned += 1

    def get_monika_wins():
        return persistent._mas_game_battleship_wins.get("Monika", 0)

    def get_player_wins():
        return persistent._mas_game_battleship_wins.get("Player", 0)

    def get_player_surrenders():
        return persistent._mas_game_battleship_abandoned

    def get_total_games():
        return get_monika_wins() + get_player_wins()

    def get_player_winrate():
        total_games = get_total_games()
        if total_games == 0:
            return 0.0
        return round(float(get_player_wins()) / total_games, 3)

    def collect_player_data(game):
        for square in game._player.grid.iter_squares_with_ships():
            persistent._mas_game_battleship_player_ship_dataset[square] += 1

        # NOTE: https://www.desmos.com/calculator/yucpu8wgux
        # F = 0.5
        # G = 16
        # P = 5*1 + 4*2 + 3*3 + 2*4 = 30
        # f0 = p0
        # fn+1 = F * (fn + P*G)
        persistent._mas_game_battleship_dataset_counter += 1
        if persistent._mas_game_battleship_dataset_counter >= 16:
            persistent._mas_game_battleship_dataset_counter = 0
            for square, value in persistent._mas_game_battleship_player_ship_dataset.iteritems():
                persistent._mas_game_battleship_player_ship_dataset[square] = int(value * 0.5)

    def visit_game_ev():
        with store.MAS_EVL("mas_battleship") as game_ev:
            if game_ev.unlocked:
                game_ev.shown_count += 1
                game_ev.last_seen = datetime.datetime.now()


    class Battleship(renpy.display.core.Displayable):
        """
        Event handler, render, and main logic for the game
        """
        ### Size and coords constants
        # Single complete grid with frame aka a "ship screen" for one player, we have 2 of these
        GRID_HEIGHT = 378
        GRID_WIDTH = GRID_HEIGHT
        # Spacing between players' "ship screens"
        GRID_SPACING = 5

        SQUARE_HEIGHT = 32
        SQUARE_WIDTH = SQUARE_HEIGHT

        # The frame around the ship grid which has the coordinates printed
        OUTER_FRAME_THICKNESS = 20
        # The grid between squares
        INNER_GRID_THICKNESS = 2

        MAIN_GRID_ORIGIN_X = 0
        MAIN_GRID_ORIGIN_Y = 0
        MAIN_GRID_ORIGIN = (MAIN_GRID_ORIGIN_X, MAIN_GRID_ORIGIN_Y)
        TRACKING_GRID_ORIGIN_X = MAIN_GRID_ORIGIN_X + GRID_WIDTH + GRID_SPACING
        TRACKING_GRID_ORIGIN_Y = MAIN_GRID_ORIGIN_Y
        TRACKING_GRID_ORIGIN = (TRACKING_GRID_ORIGIN_X, TRACKING_GRID_ORIGIN_Y)

        GAME_ASSETS_FOLDER = "/mod_assets/games/battleship/"

        ### Grid sprites
        # Grid background
        GRID_BACKGROUND = ConditionSwitch(
            "not store.mas_globals.dark_mode", Image(GAME_ASSETS_FOLDER + "grid/background.png"),
            "True", Image(GAME_ASSETS_FOLDER + "grid/background_d.png"),
        )
        # The outer frame around the squares with coordinates printed
        GRID_FRAME = ConditionSwitch(
            "not store.mas_globals.dark_mode", Image(GAME_ASSETS_FOLDER + "grid/frame.png"),
            "True", Image(GAME_ASSETS_FOLDER + "grid/frame_d.png"),
        )
        # The grid that separates squares
        GRID_FOREGROUND = ConditionSwitch(
            "not store.mas_globals.dark_mode", Image(GAME_ASSETS_FOLDER + "grid/grid.png"),
            "True", Image(GAME_ASSETS_FOLDER + "grid/grid_d.png"),
        )

        # HACK: The animated sprite is blinking at the edges, probably due to incorrect blitting and pixel smudging
        # I come up with a hack: we render this layer 2px bigger and overlap its edges with the grid frame
        WATER_LAYER_OFFSET = 2

        # Animated water
        WATER_LAYER = store.Transform(
            store.mas_battleship_water_transform(
                child=Image(GAME_ASSETS_FOLDER + "water_loop.png"),
                width=1024,
                height=1024,
            ),
            # TODO: replace with xysize in r8
            size=(GRID_HEIGHT - OUTER_FRAME_THICKNESS*2 + WATER_LAYER_OFFSET*2, GRID_WIDTH - OUTER_FRAME_THICKNESS*2 + WATER_LAYER_OFFSET*2),
        )

        # Not actual fow, just darker overlay for Monika's grid
        FOG_OF_WAR = store.Solid("#32323280", xsize=GRID_WIDTH - OUTER_FRAME_THICKNESS*2, ysize=GRID_HEIGHT - OUTER_FRAME_THICKNESS*2)

        ### Indicators
        SQUARE_HOVER = ConditionSwitch(
            "not store.mas_globals.dark_mode", Image(GAME_ASSETS_FOLDER + "indicators/hover.png"),
            "True", Image(GAME_ASSETS_FOLDER + "indicators/hover_d.png"),
        )
        SQUARE_CONFLICT = Image(GAME_ASSETS_FOLDER + "indicators/conflict.png")
        SQUARE_HIT = Image(GAME_ASSETS_FOLDER + "indicators/hit.png")
        SQUARE_MISS = Image(GAME_ASSETS_FOLDER + "indicators/miss.png")

        ### Ships sprites
        SHIP_TYPE_TO_SPRITE = {
            ShipType.CARRIER: Image(GAME_ASSETS_FOLDER + "ships/carrier.png"),
            ShipType.BATTLESHIP: Image(GAME_ASSETS_FOLDER + "ships/battleship.png"),
            ShipType.SUBMARINE: Image(GAME_ASSETS_FOLDER + "ships/submarine.png"),
            ShipType.CRUISER: Image(GAME_ASSETS_FOLDER + "ships/cruiser.png"),
            ShipType.DESTROYER: Image(GAME_ASSETS_FOLDER + "ships/destroyer.png"),
        }
        # Used for prediction
        _SHIP_SPRITES = list(SHIP_TYPE_TO_SPRITE.itervalues())
        # Used for sunked ships
        GREYOUT_MATRIX = store.im.matrix.desaturate() * store.im.matrix.brightness(-0.25)

        # Currently only support this, but technically easily extendable for custom setups
        SHIP_PRESET_CLASSIC = (
            ShipType.CARRIER,
            ShipType.BATTLESHIP,
            ShipType.BATTLESHIP,
            ShipType.SUBMARINE,
            ShipType.CRUISER,
            ShipType.CRUISER,
            ShipType.DESTROYER,
            ShipType.DESTROYER,
            ShipType.DESTROYER,
            ShipType.DESTROYER,
        )

        MONIKA_TURN_DURATION = 0.05

        class GamePhase(object):
            """
            Types of Game phases
            TODO: turn this into enum
            """
            PREPARATION = 0
            ACTION = 1
            DONE = 2

        class WinState(object):
            """
            Types of win conditions
            TODO: turn this into enum
            """
            UNKNOWN = 0
            PLAYER_WON = 1
            MONIKA_WON = 2
            PLAYER_GAVEUP = 3

        def __init__(self):
            super(Battleship, self).__init__()

            self._last_mouse_x = 0
            self._last_mouse_y = 0

            self.is_sensitive = False

            self._turn = 0
            self._turn_flag = False
            self._phase = self.GamePhase.PREPARATION
            self._win_state = self.WinState.UNKNOWN

            self._hovered_square = None # type: tuple[int, int] | None
            self._dragged_ship = None # type: Ship | None
            self._grid_conflicts = [] # type: list[tuple[int, int]]
            self._debug_heatmap = False
            self._debug_no_quips = False
            self._debug_no_pause = False
            self._debug_monika_ships = False

            self._ship_sprites_cache = {} # type: dict[tuple[ShipType, Ship.Orientation, bool], renpy.Displayable]

            self._player = Player()
            self._monika = AIPlayer(dataset=persistent._mas_game_battleship_player_ship_dataset)

        def pick_first_player(self):
            """
            Decides who will shoot in the first turn, sets the flag
            """
            self._turn_flag = random.random() < 0.5

        def _switch_turn(self):
            """
            Switches turn between Monika and player
            """
            self._turn_flag ^= True
            self._turn += 1

        def get_turn_count(self):
            return self._turn

        def is_player_turn(self):
            return self._turn_flag

        def is_monika_turn(self):
            return not self.is_player_turn()


        def mark_player_won(self):
            self._win_state = self.WinState.PLAYER_WON

        def mark_monika_won(self):
            self._win_state = self.WinState.MONIKA_WON

        def mark_player_gaveup(self):
            self._win_state = self.WinState.PLAYER_GAVEUP

        def is_player_winner(self):
            return self._win_state == self.WinState.PLAYER_WON

        def is_monika_winner(self):
            return self._win_state == self.WinState.MONIKA_WON

        def did_player_giveup(self):
            return self._win_state == self.WinState.PLAYER_GAVEUP

        def did_player_cancel_game(self):
            return self.did_player_giveup() and self.get_turn_count() == 0


        def get_player_hits_count(self):
            return self._player.total_hits()

        def get_player_misses_count(self):
            return self._player.total_misses()

        def get_monika_hits_count(self):
            return self._monika.total_hits()

        def get_monika_misses_count(self):
            return self._monika.total_misses()


        def can_start_action(self):
            """
            Checks if all players' ships are placed and valid

            OUT:
                bool
            """
            for player in (self._player, self._monika):
                if player.grid.has_conflicts():
                    return False

                preset_ships = Counter(self.SHIP_PRESET_CLASSIC)
                grid_ships = Counter(ship.type for ship in player.iter_ships())

                if preset_ships != grid_ships:
                    return False

            return True

        def is_in_preparation(self):
            """
            Returns True if the players are positioning their ships

            OUT:
                bool
            """
            return self._phase == self.GamePhase.PREPARATION

        def is_in_action(self):
            """
            Returns True if the game is in active phase

            OUT:
                bool
            """
            return self._phase == self.GamePhase.ACTION

        def is_done(self):
            """
            Returns True if at least one player has lost all of their ships

            OUT:
                bool
            """
            return self._phase == self.GamePhase.DONE

        def set_phase_action(self):
            """
            Changes the game phase to action

            NOTE: returning a non-None value is important, this way we end the interaction
            from the screen action

            OUT:
                bool
            """
            if self.is_in_action() or not self.can_start_action():
                return False

            self._phase = self.GamePhase.ACTION
            return True

        def set_phase_done(self):
            """
            Changes the game phase to done

            NOTE: returning a non-None value is important, this way we end the interaction
            from the screen action

            OUT:
                bool
            """
            self._phase = self.GamePhase.DONE
            self._hovered_square = None
            self.is_sensitive = False
            return True


        @staticmethod
        def _update_screens():
            """
            Request renpy to update all screens
            """
            renpy.restart_interaction()

        @staticmethod
        def square_coords_to_human_readable(coords):
            """
            Returns a human-readable name of the square

            IN:
                coords - tuple[int, int] - the square coordinates

            ASSUMES:
                the coordinates are correct

            OUT:
                str - like "A1" or "J10"
            """
            UNICOED_CODE_POINT_OFFSET = 65
            Y_AXIS_OFFSET = 1

            x, y = coords

            return "{}{}".format(
                chr(x + UNICOED_CODE_POINT_OFFSET),
                y + Y_AXIS_OFFSET,
            )

        def get_hovering_square(self):
            """
            Returns a human-readable name of the square
            that the player is hovering mouse above

            OUT:
                str - like "A1" or "J10"
            """
            if not self._hovered_square:
                return "n/a"

            return self.square_coords_to_human_readable(self._hovered_square)


        @staticmethod
        def _get_monika_expr():
            """
            Returns current Monika's expression

            OUT:
                str | None - str will be of format like "1eua", "idle", etc
            """
            # NOTE: There's no renpy.get_attributes() in r6.12, so I will make one myself
            # TODO: Don't forget to remove in r8
            layer = renpy.exports.default_layer(None, "monika")

            if not renpy.showing("monika", layer):
                return None

            ctx = renpy.game.context()
            if not ctx:
                return None

            attrs = ctx.images.get_attributes(layer, "monika")
            if not attrs:
                return None

            return attrs[0]

        def monika_say(self, what, expr=None, restore_expr=True, should_invoke=False):
            """
            Calls renpy say allowing Monika speak during the game

            IN:
                what - str - what Monika will say
                expr - str | None - the expression to show if any
                restore_expr - bool - if an expr was given and this parameter is True,
                    then after the dialogue the expression will return to the previous one
                should_invoke - bool - if True, the call will be made in new context allowing execution mid interaction
            """
            previous_is_sensitive = self.is_sensitive
            self.is_sensitive = False

            prev_expr = None
            if expr:
                prev_expr = self._get_monika_expr()
                renpy.show("monika {}".format(expr))

            if should_invoke:
                renpy.invoke_in_new_context(renpy.say, store.m, what, interact=True)
            else:
                renpy.say(store.m, what, interact=True)

            if expr and prev_expr and restore_expr:
                renpy.show("monika {}".format(prev_expr))

            self.is_sensitive = previous_is_sensitive


        def build_and_place_player_ships(self, should_use_dataset=False):
            """
            Builds and places ships for the player

            NOTE: returning a non-None value is important, this way we end the interaction
            from the screen action

            IN:
                should_use_dataset - bool - whether we use player ship dataset to place ships
                    Default: False

            OUT:
                bool - success or not
            """
            if not self.is_in_preparation():
                return False

            self._player.grid.clear()
            if should_use_dataset:
                weights = persistent._mas_game_battleship_player_ship_dataset
            else:
                weights = None
            self._player.grid.place_ships(Ship.build_ships_from_preset(self.SHIP_PRESET_CLASSIC), weights=weights)
            self._grid_conflicts[:] = self._player.grid.get_conflicts()

            return True

        def build_and_place_monika_ships(self):
            """
            Builds and places ships for monika
            """
            self._monika.grid.clear()
            self._monika.grid.place_ships(Ship.build_ships_from_preset(self.SHIP_PRESET_CLASSIC))

        @classmethod
        def _grid_coords_to_screen_coords(cls, coords, grid_origin):
            """
            Converts grid coordinates into screen coordinates

            IN:
                coords - tuple[int, int] - coordinates on the grid
                grid_origin - tuple[int, int] - screen x y coordinates of the grid origin

            OUT:
                tuple with coords
            """
            x, y = coords
            grid_origin_x, grid_origin_y = grid_origin
            return (
                grid_origin_x + cls.OUTER_FRAME_THICKNESS + x * (cls.INNER_GRID_THICKNESS + cls.SQUARE_WIDTH),
                grid_origin_y + cls.OUTER_FRAME_THICKNESS + y * (cls.INNER_GRID_THICKNESS + cls.SQUARE_HEIGHT),
            )

        @classmethod
        def _screen_coords_to_grid_coords(cls, x, y, grid_origin):
            """
            Converts screen coordinates into grid coordinates

            IN:
                x - x coordinate on the screen
                y - y coordinate on the screen
                grid_origin - tuple[int, int] - screen x y coordinates of the grid origin

            OUT:
                tuple with coords,
                or None if the given coords are outside the grid
            """
            grid_origin_x, grid_origin_y = grid_origin
            # First check if we're within this grid
            if not (
                grid_origin_x + cls.OUTER_FRAME_THICKNESS <= x <= grid_origin_x + cls.GRID_WIDTH - cls.OUTER_FRAME_THICKNESS
                and grid_origin_y + cls.OUTER_FRAME_THICKNESS <= y <= grid_origin_y + cls.GRID_HEIGHT - cls.OUTER_FRAME_THICKNESS
            ):
                return None

            return (
                int((x - grid_origin_x - cls.OUTER_FRAME_THICKNESS - (int(x - grid_origin_x - cls.OUTER_FRAME_THICKNESS) / cls.SQUARE_WIDTH) * cls.INNER_GRID_THICKNESS) / cls.SQUARE_WIDTH),
                int((y - grid_origin_y - cls.OUTER_FRAME_THICKNESS - (int(y - grid_origin_y - cls.OUTER_FRAME_THICKNESS) / cls.SQUARE_HEIGHT) * cls.INNER_GRID_THICKNESS) / cls.SQUARE_HEIGHT),
            )

        def _get_ship_sprite(self, ship):
            """
            Returns a sprite for a ship using cache system (generates if needed, retrives if already generated)

            IN:
                ship - Ship - the ship obj to get a sprite for

            OUT:
                Transform - ship sprite
            """
            key = (ship.type, ship.orientation, ship.is_alive())

            if key not in self._ship_sprites_cache:
                # NOTE: Sprites are headed up, but in our system 0 degrees is right, NOT up
                # so we need to adjust the angle to avoid rotation
                angle = ship.orientation - Ship.Orientation.UP
                sprite = self.SHIP_TYPE_TO_SPRITE[ship.type]
                if not ship.is_alive():
                    # TODO: use transform matrices in r8
                    sprite = store.im.MatrixColor(sprite, self.GREYOUT_MATRIX)

                self._ship_sprites_cache[key] = Transform(
                    child=sprite,
                    xanchor=0.5,
                    yanchor=self.SQUARE_HEIGHT // 2,
                    offset=(self.SQUARE_HEIGHT // 2, self.SQUARE_HEIGHT // 2),
                    transform_anchor=True,
                    rotate_pad=False,
                    subpixel=True,
                    rotate=angle,
                )

            return self._ship_sprites_cache[key]

        def render(self, width, height, st, at):
            """
            Render method for this disp
            """
            # Define our main render
            main_render = renpy.Render(2*self.GRID_WIDTH + self.GRID_SPACING, self.GRID_HEIGHT)

            # # # Render grids
            # Predefine renders
            grid_background_render = renpy.render(self.GRID_BACKGROUND, width, height, st, at)
            grid_frame_render = renpy.render(self.GRID_FRAME, width, height, st, at)
            grid_foreground_render = renpy.render(self.GRID_FOREGROUND, width, height, st, at)
            water_layer_render = renpy.render(self.WATER_LAYER, width, height, st, at)
            # Now blit 'em
            main_render.subpixel_blit(grid_background_render, self.MAIN_GRID_ORIGIN)
            main_render.subpixel_blit(
                water_layer_render,
                (
                    self.MAIN_GRID_ORIGIN_X + self.OUTER_FRAME_THICKNESS - self.WATER_LAYER_OFFSET,
                    self.MAIN_GRID_ORIGIN_Y + self.OUTER_FRAME_THICKNESS  - self.WATER_LAYER_OFFSET,
                ),
            )
            main_render.subpixel_blit(grid_frame_render, self.MAIN_GRID_ORIGIN)
            main_render.subpixel_blit(grid_foreground_render, self.MAIN_GRID_ORIGIN)

            # Render Monika's grid only during the game phase
            if self.is_in_action() or (self.is_done() and not self.did_player_cancel_game()):
                main_render.subpixel_blit(grid_background_render, self.TRACKING_GRID_ORIGIN)
                main_render.subpixel_blit(
                    water_layer_render,
                    (
                        self.TRACKING_GRID_ORIGIN_X + self.OUTER_FRAME_THICKNESS - self.WATER_LAYER_OFFSET,
                        self.TRACKING_GRID_ORIGIN_Y + self.OUTER_FRAME_THICKNESS - self.WATER_LAYER_OFFSET,
                    ),
                )
                main_render.subpixel_blit(grid_frame_render, self.TRACKING_GRID_ORIGIN)
                main_render.subpixel_blit(grid_foreground_render, self.TRACKING_GRID_ORIGIN)

            # Render conflicts
            if self.is_in_preparation():
                if self._grid_conflicts:
                    error_mask_render = renpy.render(self.SQUARE_CONFLICT, width, height, st, at)
                    for coords in self._grid_conflicts:
                        x, y = self._grid_coords_to_screen_coords(coords, self.MAIN_GRID_ORIGIN)
                        main_render.subpixel_blit(error_mask_render, (x, y))

            # Render player's ships
            for ship in self._player.iter_ships():
                ship_sprite = self._get_ship_sprite(ship)
                x, y = self._grid_coords_to_screen_coords(ship.bow_coords, self.MAIN_GRID_ORIGIN)
                main_render.place(ship_sprite, x, y)

            # # # Render things that only relevant during the game
            if not self.is_in_preparation():
                # Render Monika's ships
                for ship in self._monika.iter_ships():
                    if not ship.is_alive() or self._debug_monika_ships:
                        ship_sprite = self._get_ship_sprite(ship)
                        x, y = self._grid_coords_to_screen_coords(ship.bow_coords, self.TRACKING_GRID_ORIGIN)
                        main_render.place(ship_sprite, x, y)


                main_render.place(self.FOG_OF_WAR, self.TRACKING_GRID_ORIGIN_X + self.OUTER_FRAME_THICKNESS, self.TRACKING_GRID_ORIGIN_Y + self.OUTER_FRAME_THICKNESS)

                # Render hits
                hit_mark_render = renpy.render(self.SQUARE_HIT, width, height, st, at)
                for coords in self._player.iter_hits():
                    x, y = self._grid_coords_to_screen_coords(coords, self.TRACKING_GRID_ORIGIN)
                    main_render.subpixel_blit(hit_mark_render, (x, y))

                for coords in self._monika.iter_hits():
                    x, y = self._grid_coords_to_screen_coords(coords, self.MAIN_GRID_ORIGIN)
                    main_render.subpixel_blit(hit_mark_render, (x, y))

                # Render misses
                miss_mark_render = renpy.render(self.SQUARE_MISS, width, height, st, at)
                for coords in self._player.iter_misses():
                    x, y = self._grid_coords_to_screen_coords(coords, self.TRACKING_GRID_ORIGIN)
                    main_render.subpixel_blit(miss_mark_render, (x, y))

                for coords in self._monika.iter_misses():
                    x, y = self._grid_coords_to_screen_coords(coords, self.MAIN_GRID_ORIGIN)
                    main_render.subpixel_blit(miss_mark_render, (x, y))

                if not self.is_done():
                    # Render hovering mask
                    if self._hovered_square is not None:
                        hover_mask_render = renpy.render(self.SQUARE_HOVER, width, height, st, at)
                        x, y = self._grid_coords_to_screen_coords(self._hovered_square, self.TRACKING_GRID_ORIGIN)
                        main_render.subpixel_blit(hover_mask_render, (x, y))

            # # # Render things that only relevant during ship building
            elif self.is_in_preparation():
                # Render hovering mask
                if self._hovered_square is not None:
                    hover_mask_render = renpy.render(self.SQUARE_HOVER, width, height, st, at)
                    x, y = self._grid_coords_to_screen_coords(self._hovered_square, self.MAIN_GRID_ORIGIN)
                    main_render.subpixel_blit(hover_mask_render, (x, y))

                # Render the ship that's currently dragged (if any)
                if self._dragged_ship is not None:
                    ship_sprite = self._get_ship_sprite(self._dragged_ship)
                    if Ship.Orientation.is_vertical(self._dragged_ship.orientation):
                        x_offset = 0
                        y_offset = self._dragged_ship.get_drag_offset_from_bow() * self.SQUARE_HEIGHT

                    else:
                        x_offset = self._dragged_ship.get_drag_offset_from_bow() * self.SQUARE_WIDTH
                        y_offset = 0

                    main_render.place(
                        ship_sprite,
                        (self._last_mouse_x - self.SQUARE_WIDTH / 2 + x_offset),
                        (self._last_mouse_y - self.SQUARE_HEIGHT / 2 + y_offset)
                    )

            if self._debug_heatmap:
                for coords, color in self._monika.get_heatmap_colors().iteritems():
                    heat_overlay = store.Solid(color.replace_opacity(0.8), xsize=32, ysize=32)
                    x, y = self._grid_coords_to_screen_coords(coords, self.MAIN_GRID_ORIGIN)
                    color_render = renpy.render(heat_overlay, width, height, st, at)
                    main_render.subpixel_blit(color_render, (x, y))

                    temp = str(round(self._monika.heatmap[coords], 3))
                    txt = store.Text(temp, color=(0, 0, 0, 255), size=12, outlines=())
                    txt_render = renpy.render(txt, width, height, st, at)
                    main_render.subpixel_blit(txt_render, (x, y))

            return main_render

        def _redraw_now(self):
            """
            Requests redraw ASAP
            """
            renpy.redraw(self, 0)

        def _handle_preparation_events(self, ev, x, y, st):
            # # # The player pressed the rotation key
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
                # If the player's dragging a ship, rotate it
                if self._dragged_ship is not None:
                    if ev.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT):
                        self._dragged_ship.orientation -= 90
                    else:
                        self._dragged_ship.orientation += 90

                    self._redraw_now()
                    raise renpy.IgnoreEvent()

                # If the player's pressed the keybinding for rotating while hovering over a ship, rotate it
                else:
                    coords = self._screen_coords_to_grid_coords(x, y, self.MAIN_GRID_ORIGIN)
                    if coords is None:
                        return None

                    ship = self._player.grid.get_ship_at(coords)
                    if ship is None:
                        return None

                    if ev.mod in (pygame.KMOD_LSHIFT, pygame.KMOD_RSHIFT):
                        angle = -90
                    else:
                        angle = 90

                    ship.rotate(angle, coords)
                    self._player.grid.update()
                    self._grid_conflicts[:] = self._player.grid.get_conflicts()

                    self._redraw_now()
                    raise renpy.IgnoreEvent()

            # # # The player moves the mouse, we may need to update the screen
            elif ev.type == pygame.MOUSEMOTION:
                # Continue to update the screen while the player's dragging a ship
                if self._dragged_ship is not None:
                    self._redraw_now()

                coords = self._screen_coords_to_grid_coords(x, y, self.MAIN_GRID_ORIGIN)
                if coords != self._hovered_square:
                    self._hovered_square = coords
                    self._redraw_now()
                    self._update_screens()
                    raise renpy.IgnoreEvent()

            # # # The player clicks on a ship and starts dragging it
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                coords = self._screen_coords_to_grid_coords(x, y, self.MAIN_GRID_ORIGIN)
                if coords is None:
                    return None

                ship = self._player.grid.get_ship_at(coords)
                if ship is None:
                    return None

                self._player.grid.remove_ship(ship)
                self._grid_conflicts[:] = self._player.grid.get_conflicts()
                ship.drag_coords = coords
                self._dragged_ship = ship

                self._redraw_now()
                raise renpy.IgnoreEvent()

            # # # The player releases the mouse button and places the ship on the grid
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if self._dragged_ship is None:
                    return None

                coords = self._screen_coords_to_grid_coords(x, y, self.MAIN_GRID_ORIGIN)
                if coords is not None:
                    # Let's get dragging offsets
                    if Ship.Orientation.is_vertical(self._dragged_ship.orientation):
                        x_offset = 0
                        y_offset = self._dragged_ship.get_drag_offset_from_bow()

                    else:
                        x_offset = self._dragged_ship.get_drag_offset_from_bow()
                        y_offset = 0

                    # Repack the tuple appying the offsets
                    coords = (coords[0] + x_offset, coords[1] + y_offset)
                    # Set new coords for the ship
                    self._dragged_ship.bow_coords = coords
                    # Reset drag point
                    self._dragged_ship.drag_coords = coords

                # NOTE: If the ship is out of grid, we will return it where it was when player started dragging it
                self._player.grid.place_ship(self._dragged_ship)
                # Check for invalid placement
                self._grid_conflicts[:] = self._player.grid.get_conflicts()
                self._dragged_ship = None

                self._redraw_now()
                raise renpy.IgnoreEvent()

        def _handle_action_events(self, ev, x, y, st):
            # # # The player moves the mouse, we may need to update the screen for hover events
            if ev.type == pygame.MOUSEMOTION:
                coords = self._screen_coords_to_grid_coords(x, y, self.TRACKING_GRID_ORIGIN)
                if coords != self._hovered_square:
                    self._hovered_square = coords
                    self._redraw_now()
                    self._update_screens()
                    raise renpy.IgnoreEvent()

            # # # The player releases the mouse button potentially shooting
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                if self.is_monika_turn():
                    return None

                coords = self._screen_coords_to_grid_coords(x, y, self.TRACKING_GRID_ORIGIN)
                if coords is None:
                    return None

                if self._player.has_shot_at(coords):
                    return None

                self.register_player_shot(coords)

                self._switch_turn()
                return True

            return None

        def _handle_debug_events(self, ev, x, y, st):
            if (
                ev.type == pygame.KEYDOWN
                and ev.mod == (pygame.KMOD_LALT | pygame.KMOD_RSHIFT)
                and renpy.config.developer
            ):
                changed = False
                if ev.key == pygame.K_h:
                    self._debug_heatmap ^= True
                    changed = True

                elif ev.key == pygame.K_m:
                    self._debug_monika_ships ^= True
                    changed = True

                elif ev.key == pygame.K_q:
                    self._debug_no_quips ^= True
                    changed = True

                elif ev.key == pygame.K_p:
                    self._debug_no_pause ^= True
                    changed = True

                if changed:
                    persistent._mas_pm_has_battleship_debug = True
                    raise renpy.IgnoreEvent()

        def event(self, ev, x, y, st):
            """
            Event handler
            TODO: support playing with just a keyboard
            """
            # Update internal mouse coords
            self._last_mouse_x = x
            self._last_mouse_y = y

            # If this executes, it skips the event, no further processing happens
            self._handle_debug_events(ev, x, y, st)

            # When disabled we only process mouse motions
            if not self.is_sensitive and ev.type != pygame.MOUSEMOTION:
                return None

            if self.is_in_preparation():
                return self._handle_preparation_events(ev, x, y, st)

            elif self.is_in_action():
                return self._handle_action_events(ev, x, y, st)

            return None

        def handle_monika_turn(self):
            """
            Logic for playing Monika turn
            """
            if not self.is_in_action():
                log_err("called Battleship.handle_monika_turn while in {} phase, the game hasn't started yet".format(self._phase))
                return

            if self.is_player_turn():
                log_err("called Battleship.handle_monika_turn, but it's player's turn")
                return

            coords = self._monika.pick_square_for_attack(self._player)
            if coords is None:
                log_err("AIPlayer.pick_square_for_attack returned None")
                self._switch_turn()
                return

            if self._monika.has_shot_at(coords):
                log_err("AIPlayer.pick_square_for_attack returned a square that Monika already shot at")
                self._switch_turn()
                return

            quip = None
            if not self._debug_no_quips:
                quip = self._monika.pick_turn_start_quip(self._player, coords)
                if quip is not None:
                    self.monika_say(quip[1], quip[0])

            if quip is None and not self._debug_no_pause:
                renpy.pause(self.MONIKA_TURN_DURATION)

            self.register_monika_shot(coords)
            self._switch_turn()

        def handle_player_turn(self):
            """
            Logic for playing Player turn
            """
            # NOTE: We pretty much always want to start an interaction for stuff like mouse motion and whatnot
            ui.interact(type="minigame")

        def register_monika_shot(self, square):
            """
            Registers a shot from Monika and checks for her win cond

            IN:
                square - tuple[int, int] - the square to shoot at

            ASSUMES:
                - the square is valid
                - the game isn't over
            """
            if not self.is_monika_turn():
                log_err("called Battleship.register_monika_shot, but it's player's turn")
                return

            ship = self._player.grid.get_ship_at(square)
            if ship is None:
                self._monika.register_miss(square)
                self._redraw_now()

            else:
                self._monika.register_hit(square)
                ship.take_hit()

                # Redraw here after adding hit/miss and changing ship hp,
                # so if Monika reacts, we can see the updated state of the board
                self._redraw_now()

                self._monika.on_opponent_ship_hit(ship)

                if not ship.is_alive():
                    self._monika.on_opponent_ship_destroyed(ship)

                    if self._player.has_lost_all_ships():
                        self.set_phase_done()
                        self.mark_monika_won()

                    elif not self._debug_no_quips:
                        quip = self._monika.pick_sunk_ship_quip(self._player, ship)
                        if quip is not None:
                            self.monika_say(quip[1], quip[0])

                elif not self._debug_no_quips:
                    quip = self._monika.pick_hit_ship_quip(self._player, ship)
                    if quip is not None:
                        self.monika_say(quip[1], quip[0])

        def register_player_shot(self, square):
            """
            Registers a shot from the player and checks for their win cond

            IN:
                square - tuple[int, int] - the square to shoot at

            ASSUMES:
                - the square is valid
                - the game isn't over
            """
            if not self.is_player_turn():
                log_err("called Battleship.register_player_shot, but it's Monika's turn")
                return

            ship = self._monika.grid.get_ship_at(square)
            if ship is None:
                self._player.register_miss(square)
                self._redraw_now()

            else:
                self._player.register_hit(square)
                ship.take_hit()

                self._redraw_now()

                self._player.on_opponent_ship_hit(ship)

                if not ship.is_alive():
                    self._player.on_opponent_ship_destroyed(ship)

                    if self._monika.has_lost_all_ships():
                        self.set_phase_done()
                        self.mark_player_won()

                    elif not self._debug_no_quips:
                        quip = self._monika.pick_lost_ship_quip(self._player, ship)
                        if quip is not None:
                            self.monika_say(quip[1], quip[0], should_invoke=True)

        def game_loop(self):
            """
            Game loop, switches between Monika's and player handlers
            """
            if self.is_monika_turn() and self.is_in_action():
                self.handle_monika_turn()

            self._monika.on_game_loop_cycle(self._player)

            if not self.is_done():
                self.handle_player_turn()

            self._player.on_game_loop_cycle(self._monika)

        def visit(self):
            return [
                self.GRID_BACKGROUND,
                self.GRID_FRAME,
                self.GRID_FOREGROUND,
                self.WATER_LAYER,
                self.FOG_OF_WAR,
                self.SQUARE_HOVER,
                self.SQUARE_CONFLICT,
                self.SQUARE_HIT,
                self.SQUARE_MISS,
            ] + self._SHIP_SPRITES


    class Grid(object):
        """
        Represents a field/screen for battleship placement
        """
        HEIGHT = 10
        WIDTH = HEIGHT

        class SquareState(object):
            """
            Types of grid square consts
            TODO: turn this into enum
            """
            EMPTY = 0
            SHIP = 1
            SPACING = 2
            CONFLICT = 3

            @classmethod
            def get_all(cls):
                return (cls.EMPTY, cls.SHIP, cls.SPACING, cls.CONFLICT)

        def __init__(self):
            """
            Constructor
            """
            # Coordinates: square state
            self._square_states = {
                (col, row): self.SquareState.EMPTY
                for row in range(self.HEIGHT)
                for col in range(self.WIDTH)
            } # type: dict[tuple[int, int], SquareState]
            # Coordinates: ships
            self._ships_grid = {coords: [] for coords in self._square_states.iterkeys()} # type: dict[tuple[int, int], list[Ship]]
            # All ships on the grid
            self._ships = []

        @property
        def total_ships(self):
            return len(self._ships)

        def iter_ships(self):
            """
            Returns an iterator over the ships on this grid

            OUT:
                iterator over the list of ships
            """
            return iter(self._ships)

        def clear(self):
            """
            Clears this grid
            """
            for coords in self._square_states:
                self._square_states[coords] = self.SquareState.EMPTY

            for ships in self._ships_grid.itervalues():
                ships[:] = []

            self._ships[:] = []

        def is_within(self, coords):
            """
            Returns whether or not the coordinates are within the grid

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                bool
            """
            x, y = coords
            return (0 <= x < self.WIDTH) and (0 <= y < self.HEIGHT)

        def _get_square_at(self, coords):
            """
            Returns the state of a square

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                int as one of states,
                or None if the given coordinates are out of this grid
            """
            return self._square_states.get(coords, None)

        def is_empty_at(self, coords):
            """
            Checks if the square at the given coordinates is empty
            (has no ship nor spacing for a ship)

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                bool - True if free, False otherwise
            """
            return self._get_square_at(coords) == self.SquareState.EMPTY

        def is_spacing_at(self, coords):
            """
            Checks if the square at the given coordinates is occupied by ship spacing

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                bool - True if free, False otherwise
            """
            return self._get_square_at(coords) == self.SquareState.SPACING

        def is_ship_at(self, coords):
            """
            Checks if the square at the given coordinates is occupied by a ship

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                bool - True if free, False otherwise
            """
            return self._get_square_at(coords) == self.SquareState.SHIP

        def is_empty_or_spacing_at(self, coords):
            """
            Checks if the square at the given coordinates has no ship

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                bool - True if free, False otherwise
            """
            return self.is_empty_at(coords) or self.is_spacing_at(coords)

        def _set_square_at(self, coords, value):
            """
            Set a square to a new state
            This will do nothing if the given coords are outside of this grid

            IN:
                coords - tuple[int, int] - coordinates
                value - new state for the square
            """
            if (
                coords not in self._square_states
                or value not in self.SquareState.get_all()
            ):
                return

            self._square_states[coords] = value

        def iter_squares_with_ships(self):
            """
            Returns all squares that have ships

            OUT:
                Iterator[tuple[int, int]]
            """
            for coords, state in self._square_states.iteritems():
                if state == self.SquareState.SHIP:
                    yield coords

        def get_ship_at(self, coords):
            """
            Returns a ship at the given coordinates

            NOTE: If for some reason we have more than one ship in the square,
                this will return the one that was added last

            IN:
                coords - tuple[int, int] - coordinates

            OUT:
                Ship | None - the ship or None if nothing found
            """
            ships = self._ships_grid.get(coords, None)
            if ships:
                return ships[-1]

            return None

        def has_conflicts(self):
            """
            Returns True if there's ships on the grid that were placed incorrectly

            OUT:
                bool
            """
            for coords, square_state in self._square_states.iteritems():
                if square_state == self.SquareState.CONFLICT:
                    return True
            return False

        def get_conflicts(self):
            """
            Returns a list of coordinates of ships that were placed incorrectly

            OUT:
                list with coordinates
            """
            return [
                coords
                for coords, square_state in self._square_states.iteritems()
                if square_state == self.SquareState.CONFLICT
            ]

        def update(self):
            """
            Goes through this grid and sets its squares again
            """
            ships = tuple(self._ships)

            self.clear()

            for ship in ships:
                self.place_ship(ship)

        def remove_ship(self, ship):
            """
            Removes a ship from this grid

            IN:
                ship - ship to remove
            """
            for ships in self._ships_grid.itervalues():
                if ship in ships:
                    ships.remove(ship)

            if ship in self._ships:
                self._ships.remove(ship)

            self.update()

        def find_place_for_ship(self, ship, weights=None):
            """
            Tries to find a place for a ship

            IN:
                ship - Ship - a ship to place
                weights - dict[tuple[int, int], int] | None - weights for each square of the grid,
                    this makes it possible to make some square more or less desirable for placement

            OUT:
                tuple[int, int] | None - coordinates for the bow of this ship
                    or None if no free space was found
            """
            ship_length = ship.length
            # List with all free lines where we could place this ship on and their weights
            available_lines_and_weights = [] # type: list[ tuple[ list[tuple[int, int]], int ] ]
            # Swap columns with rows for horizontal lines
            should_mirror_coords = Ship.Orientation.is_horizontal(ship.orientation)

            def add_line(line):
                """
                Calculates weight for the given line and adds that data to the list of all lines

                IN:
                    line - list[tuple[int, int]]

                ASSUMES:
                    available_lines_and_weights
                    weights
                """
                line_weight = 1
                if weights is not None:
                    for square in line:
                        line_weight += weights[square]
                available_lines_and_weights.append((line, line_weight))

            for column in range(self.WIDTH):
                # A potential line where the ship would fit
                # TODO: I don't think we actually have to store every point on the line,
                # it's enough to know just start/end and maybe length, could be an optimisation
                line = [] # type: list[tuple[int, int]]
                for row in range(self.HEIGHT):
                    if should_mirror_coords:
                        square = (row, column)
                    else:
                        square = (column, row)

                    # If this square is free, add it to the line
                    if self.is_empty_at(square):
                        line.append(square)

                    # Otherwise we got all free squares we could
                    else:
                        # See if we can fit our ship in this line
                        if len(line) >= ship_length:
                            add_line(line)
                        # Reset the list before continuing iterating
                        line = []

                # Reached the end of this column, check if the ship would fit the line
                if len(line) >= ship_length:
                    add_line(line)

            # Return None if we couldn't find a place for this ship
            if not available_lines_and_weights:
                return None

            # Pick the line we'll use
            line = weightedChoice(available_lines_and_weights)
            if len(line) == ship_length:
                offset = 0

            # Pick where ship will start at the line (in case the line is longer than the ship)
            # If no weights provided, use randrange
            elif weights is None:
                offset = random.randint(0, len(line) - ship_length)

            else:
                # List of points from the picked line we can start at and their weight
                offsets_and_weights = [] # list[ tuple[ tuple[int, int], int ] ]
                # Calculate weight for offset 0
                weight = 1
                for i in range(ship_length):
                    weight += weights[line[i]]
                offsets_and_weights.append((0, weight))

                # Calculate weights for other offsets using 2 pointers
                l = 0
                r = ship_length
                while r < len(line):
                    weight = weight - weights[line[l]] + weights[line[r]]
                    offsets_and_weights.append((l+1, weight))
                    l += 1
                    r += 1

                offset = weightedChoice(offsets_and_weights)

            # Mirror the offset if the ship is facing in positive direction on the plane
            if ship.orientation in (Ship.Orientation.DOWN, Ship.Orientation.RIGHT):
                offset += ship_length - 1

            return line[offset]

        def place_ship(self, ship):
            """
            Places a ship at the coordinates of its bow,
            sets the appropriate state for the squares under the ship and adds
            the ship to the ship map

            NOTE: this makes no checks whether or not we can place the ship on the given pos

            IN:
                ship - ship to place
            """
            ship_squares, spacing_squares = ship.get_squares()

            is_ship_within_grid = True
            for square in ship_squares:
                # We have to iterate twice, if at least one square is out of bounds,
                # we want to mark all of them as conflict, so the player knows something is wrong
                if not self.is_within(square):
                    is_ship_within_grid = False
                    break

            for square in ship_squares:
                if is_ship_within_grid and self.is_empty_at(square):
                    square_state = self.SquareState.SHIP
                else:
                    square_state = self.SquareState.CONFLICT

                self._set_square_at(square, square_state)

                # If the ship was placed incorrectly, then its coords may be out of this grid
                if square in self._ships_grid:
                    self._ships_grid[square].append(ship)

            for square in spacing_squares:
                # If empty, set spacing
                # if spacing, keep it
                # if there's a ship, set conflict
                # if conflict, keep it
                if self.is_empty_or_spacing_at(square):
                    square_state = self.SquareState.SPACING

                else:
                    square_state = self.SquareState.CONFLICT

                self._set_square_at(square, square_state)

            # Also add to the main list
            self._ships.append(ship)

        def place_ships(self, ships, weights=None):
            """
            Places ships on this grid at random positions and orientation

            NOTE: This does respect ship placement

            ASSUMES:
                1. the grid is empty
                2. it's possible to fit all the given ships

            IN:
                ships - list[Ship] - ships to place
                weights - dict[tuple[int, int], int] | None - weights for each square of the grid,
                    this makes it possible to make some square more or less desirable for placement
            """
            orientations = Ship.Orientation.get_all()

            while True:
                for ship in ships:
                    ship.orientation = random.choice(orientations)
                    coords = self.find_place_for_ship(ship, weights=weights)

                    # If we got appropriate coords, place the ship
                    if coords is not None:
                        ship.bow_coords = coords
                        self.place_ship(ship)

                    # Otherwise try another orientation
                    else:
                        ship.rotate_around_bow(90)
                        coords = self.find_place_for_ship(ship, weights=weights)

                        # Try with the new coords
                        if coords is not None:
                            ship.bow_coords = coords
                            self.place_ship(ship)

                        # Otherwise start from the beginning
                        else:
                            log_err("Grid.place_ships failed to find correct positions for ships, this could indicate a bug")
                            self.clear()
                            break

                # If we haven't interrupted the inner loop, then we're done
                else:
                    return


    class Ship(object):
        """
        Represents a ship on the grid
        """
        class Orientation(object):
            """
            Orientation consts
            TODO: turn this into enum
            """
            UP = 270
            RIGHT = 0
            DOWN = 90
            LEFT = 180

            @classmethod
            def get_all(cls):
                return (cls.UP, cls.RIGHT, cls.DOWN, cls.LEFT)

            @classmethod
            def is_vertical(cls, value):
                return value in (cls.UP, cls.DOWN)

            @classmethod
            def is_horizontal(cls, value):
                return value in (cls.RIGHT, cls.LEFT)

        _SHIP_TYPE_TO_LENGTH = {
            ShipType.CARRIER: 5,
            ShipType.BATTLESHIP: 4,
            ShipType.SUBMARINE: 3,
            ShipType.CRUISER: 3,
            ShipType.DESTROYER: 2,
        }

        def __init__(self, ship_type):
            """
            Constructor for new ship

            IN:
                ship_type - int - ship type
            """
            self.bow_coords = (0, 0)
            self._type = ship_type
            self._orientation = self.Orientation.UP
            self.drag_coords = (0, 0)
            self._health = self.length # Set last

        def __repr__(self):
            return "<{0}: (at: {1}, type: {2}, hp: {4})>".format(
                type(self).__name__,
                self.bow_coords,
                self.type,
                self.health,
            )

        @property
        def length(self):
            return self._SHIP_TYPE_TO_LENGTH[self.type]

        @property
        def type(self):
            return self._type

        @property
        def orientation(self):
            return self._orientation

        @orientation.setter
        def orientation(self, value):
            """
            Prop setter for orientation
            NOTE: this assumes that we rotate the ship around its bow
            NOTE: allowed angles are 0, 90, 180, and 270
            """
            value %= 360

            if (
                value == self._orientation
                or value % 90 != 0
            ):
                return

            self._orientation = value

        @property
        def health(self):
            return self._health

        def is_alive(self):
            return self._health > 0

        def take_hit(self):
            if self.is_alive():
                self._health -= 1

        @staticmethod
        def _apply_rotation_matrix(point, cos, sin, origin_point, is_positive):
            """
            Rotates a point using rotation matrix

            IN:
                point - tuple[int, int] - point coordinates
                cos - number - rotation angle cosine
                sin - number- rotation angle sine
                origin_point - tuple[int, int] - coordinates of the point to rotate around
                is_positive - whether or not the rotation angle is positive
            """
            x, y = point
            origin_x, origin_y = origin_point
            factor = 1 if is_positive else -1
            new_x = origin_x + (x - origin_x) * cos - factor * (y - origin_y) * sin
            new_y = origin_y + (y - origin_y) * cos + factor * (x - origin_x) * sin

            return (new_x, new_y)

        @classmethod
        def _rotate_point(cls, point, angle, origin_point):
            """
            Rotates a point using rotation matrix

            IN:
                point - tuple[int, int] - point coordinates
                angle - int - rotation angle
                origin_point - tuple[int, int] - coordinates of the point to rotate around
            """
            # Get the rotation direction
            is_positive = angle >= 0
            angle = meth.radians(angle)
            # Get cos and sin, always round for safety since negative nums go up and -0.9(9) is 0, not -1
            cos = int(round(meth.cos(angle)))
            sin = int(round(meth.sin(angle)))
            # Rotate
            return cls._apply_rotation_matrix(
                point=point,
                cos=cos,
                sin=sin,
                origin_point=origin_point,
                is_positive=is_positive,
            )

        def _rotate_bow(self, angle, origin_point):
            """
            Rotates this ship's bow around the given origin
            NOTE: this doesn't update the orientation and drag_point props, assuming these will be set afterwards

            IN:
                angle - int - angle to rotate by
                    NOTE: in degrees
                    NOTE: assumes it was sanitized to be between 0-270
                origin_point - tuple[int, int] - coordinates of the point to rotate around
            """
            if self.bow_coords == origin_point:
                # Don't rotate around itself
                return

            self.bow_coords = self._rotate_point(
                point=self.bow_coords,
                angle=angle,
                origin_point=origin_point,
            )

        def rotate(self, angle, origin_point):
            """
            Rotates this ship around a point

            IN:
                angle - int - angle to rotate by
                    NOTE: in degrees
                origin_point - tuple[int, int] - coordinates of the point to rotate around
            """
            angle %= 360
            # Sanity check
            if angle == 0 or angle % 90 != 0:
                log_err("Ship.rotate got invalid angle param: {}".format(angle))
                return

            self._rotate_bow(angle, origin_point)
            self._orientation += angle
            self._orientation %= 360

        def rotate_around_bow(self, angle):
            """
            Rotates this ship around its bow

            IN:
                angle - int - angle to rotate by
                    NOTE: in degrees
            """
            self.rotate(angle, self.bow_coords)

        def get_drag_offset_from_bow(self):
            """
            Returns offset from where the player drags the ship to its bow

            We could cache this, but it's not used a lot and C functions are fast enough anyway
            """
            # Calculate the vector
            offset = meth.hypot(self.bow_coords[0]-self.drag_coords[0], self.bow_coords[1]-self.drag_coords[1])
            # Invert the vector if needed
            angle = meth.radians(self.orientation)
            offset *= meth.cos(angle) + meth.sin(angle)
            return int(round(offset))

        def get_squares(self):
            """
            Returns squares occupied by this ship

            OUT:
                tuple[tuple[int], tuple[int]]
                    - first tuple is the ship squares
                    - second tuple is the spacing squares
            """
            base_x, base_y = self.bow_coords
            length = self.length

            ship = []
            spacing = []

            if self.orientation == self.Orientation.UP:
                ship_xs = itertools.repeat(base_x, length)
                ship_ys = range(base_y, base_y+length)
                ship.extend(zip(ship_xs, ship_ys))

                for y in (base_y - 1, base_y + length):
                    spacing.append((base_x, y))

                for i in range(length):
                    y = base_y + i
                    spacing.append((base_x - 1, y))
                    spacing.append((base_x + 1, y))

            elif self.orientation == self.Orientation.RIGHT:
                ship_xs = range(base_x, base_x-length, -1)
                ship_ys = itertools.repeat(base_y, length)
                ship.extend(zip(ship_xs, ship_ys))

                for x in (base_x - length, base_x + 1):
                    spacing.append((x, base_y))

                for i in range(length):
                    x = base_x - i
                    spacing.append((x, base_y - 1))
                    spacing.append((x, base_y + 1))

            elif self.orientation == self.Orientation.DOWN:
                ship_xs = itertools.repeat(base_x, length)
                ship_ys = range(base_y, base_y-length, -1)
                ship.extend(zip(ship_xs, ship_ys))

                for y in (base_y + 1, base_y - length):
                    spacing.append((base_x, y))

                for i in range(length):
                    y = base_y - i
                    spacing.append((base_x - 1, y))
                    spacing.append((base_x + 1, y))

            else:
                ship_xs = range(base_x, base_x+length)
                ship_ys = itertools.repeat(base_y, length)
                ship.extend(zip(ship_xs, ship_ys))

                for x in (base_x - 1, base_x + length):
                    spacing.append((x, base_y))

                for i in range(length):
                    x = base_x + i
                    spacing.append((x, base_y - 1))
                    spacing.append((x, base_y + 1))

            return (tuple(ship), tuple(spacing))

        def copy(self):
            """
            Returns a copy of this ship

            OUT:
                Ship - new ship with the same params as this one
            """
            ship = Ship(self.type)
            ship.bow_coords = self.bow_coords
            ship.orientation = self.orientation
            ship._health = self._health
            ship.drag_coords = self.drag_coords

            return ship

        @classmethod
        def build_ships_from_preset(cls, ship_preset):
            """
            Builds multiple ships using the given set

            IN:
                ship_preset - Iterable[ShipType] - iterable of ship types to build

            OUT:
                list[Ship] - built ships
            """
            return [cls(ship_type) for ship_type in ship_preset]


    class Player(object):
        """
        Meat battleship player
        """
        def __init__(self):
            """
            Constructor
            """
            self.grid = Grid()

            # Sets of tuples with coordinates
            self._hits = set()
            self._misses = set()

        def __repr__(self):
            return "<{0}: (ships: {1}, hits: {2}, misses: {3})>".format(
                type(self).__name__,
                list(self.iter_ships()),
                sorted(self._hits),
                sorted(self._misses),
            )

        def iter_ships(self):
            """
            Returns an iterator of ships
            """
            return self.grid.iter_ships()

        def get_total_alive_ships(self):
            """
            Returns a number of ships that are "alive"

            OUT:
                int
            """
            counter = 0
            for ship in self.iter_ships():
                if ship.is_alive():
                    counter += 1

            return counter

        def get_total_ship_health_remaining(self):
            return sum(ship.health for ship in self.iter_ships())

        def has_lost_all_ships(self):
            """
            Checks whether or not the player has lost all their ships

            OUT:
                bool
            """
            for ship in self.iter_ships():
                if ship.is_alive():
                    return False

            return True

        def register_hit(self, square):
            """
            Adds a successful hit for this player

            IN:
                square - tuple[int, int] - x and y coordinates
            """
            self._hits.add(square)

        def register_miss(self, square):
            """
            Adds a "successful" miss for this player

            IN:
                square - tuple[int, int] - x and y coordinates
            """
            self._misses.add(square)

        def has_shot_at(self, square):
            """
            Returns True if this player has shot at the given coordinates

            IN:
                square - tuple[int, int] - x and y coordinates

            OUT:
                bool
            """
            return square in self._misses or square in self._hits

        def total_hits(self):
            return len(self._hits)

        def total_misses(self):
            return len(self._misses)

        def iter_hits(self):
            """
            Returns iterator over this player hits

            OUT:
                iterator over the set of hits
            """
            return iter(self._hits)

        def iter_misses(self):
            """
            Returns iterator over this player misses

            OUT:
                iterator over the set of misses
            """
            return iter(self._misses)

        def on_opponent_ship_hit(self, ship):
            """
            Callback should be called when we hit a ship

            IN:
                ship - Ship - the ship we hit
            """
            pass

        def on_opponent_ship_destroyed(self, ship):
            """
            Callback should be called when we destroyed a ship with one of the shots

            IN:
                ship - Ship - destroyed opponent ship
            """
            pass

        def on_game_loop_cycle(self, opponent):
            """
            Callback should be called every game loop cycle regardless of turn order

            IN:
                opponent - Player - another player
            """
            pass


    class _Quip(object):
        """
        A set of possible expressions and dialogue lines to pick from

        This automatically adds {w=}{nw} to the lines, so player don't have to click for each quip
        """
        def __init__(self, exprs, lines):
            """
            Creates a new quip

            IN:
                exprs - an iterable of expressions (str) that can be used with this quip
                    NOTE: can be passed as a single str if there's just one option
                lines - an iterable of str that can be displayed in dialogue
                    NOTE: can be passed as a single str if there's just one option
            """
            if isinstance(exprs, str):
                exprs = (exprs,)

            if isinstance(lines, str):
                lines = (lines,)

            if not exprs:
                raise ValueError("must provide at least one expression")
            if not lines:
                raise ValueError("must provide at least one line")

            self.exprs = exprs
            self.lines = lines

        def pick(self):
            """
            Picks an expr and a line from this quip

            OUT:
                tuple[str, str] - expr and dlg line
            """
            if len(self.exprs) == 1:
                expr = self.exprs[0]
            else:
                expr = random.choice(self.exprs)

            if len(self.lines) == 1:
                line = self.lines[0]
            else:
                line = random.choice(self.lines)

            return (expr, line)

    class _QuipSet(object):
        def __init__(self, *quips):
            """
            Creates a new quip set

            IN:
                quips - _Quip objects
            """
            if not quips:
                raise ValueError("must provide at least one quip")

            self.quips = quips

        def pick(self):
            """
            Picks a quip from this set

            OUT:
                tuple[str, str] - expr and dlg line
            """
            if len(self.quips) == 1:
                quip = self.quips[0]
            else:
                quip = random.choice(self.quips)

            return quip.pick()

    class BaseAIPlayer(Player):
        """
        Base class for a steal and circuits battleship player
        """

        _LINES_TURN_START_COMMON_0 = (
            _("Where are your ships I wonder.{w=0.1}.{w=0.1}.{w=0.1}"),
            _("Where could your ships be.{w=0.1}.{w=0.1}.{w=0.1}"),
            _("Where are your ships.{w=0.1}.{w=0.1}.{w=0.1}"),
            _("I wonder where your ships are.{w=0.1}.{w=0.1}.{w=0.1}"),
        )
        # Monika has many ships, player has more than 1 ship
        TURN_START_TEASE = _QuipSet(
            _Quip(
                exprs=("1mta", "2mta", "1mtu", "2mtu"),
                lines=_LINES_TURN_START_COMMON_0,
            ),
        )
        # Monika has a few ships, player has more than 1
        TURN_START_NORM = _QuipSet(
            _Quip(
                exprs=("1lta", "2lta"),
                lines=_LINES_TURN_START_COMMON_0,
            ),
            _Quip(
                exprs=("1lua", "2lua", "1luu", "2luu"),
                lines=(
                    _("Let's see.{w=0.1}.{w=0.1}.{w=0.1}"),
                    _("Hmmm.{w=0.1}.{w=0.1}.{w=0.1}"),
                ),
            ),
        )
        # Monika has 1-2 ships, player has more than 1
        TURN_START_LOOKS_BAD = _QuipSet(
            _Quip(
                exprs=("2ltsdra", "2ltsdla"),
                lines=(
                    _LINES_TURN_START_COMMON_0
                    + (
                        _("[player], I'm your girlfriend after all...{w=0.3}you could go a little bit easier on me~"),
                        _("Hmmm.{w=0.1}.{w=0.1}.{w=0.1}"),
                        _("What do I do here..."),
                    )
                ),
            ),
            _Quip(
                exprs=("2etsdra", "2eksdlu", "2ltsdra", "2ltsdla"),
                lines=_("[player], I'm your girlfriend after all...{w=0.3}you could go a little bit easier on me~"),
            ),
        )
        # Monika has some ships, player has just one
        TURN_START_FINISH_HIM = _QuipSet(
            _Quip(
                exprs=("1mta", "2mta", "1mtu", "2mtu"),
                lines=(
                    _("Where is your last ship I wonder.{w=0.1}.{w=0.1}.{w=0.1}"),
                    _("Where could your last ship be.{w=0.1}.{w=0.1}.{w=0.1}"),
                    _("Where's your last ship.{w=0.1}.{w=0.1}.{w=0.1}"),
                    _("I wonder where is your last ship is.{w=0.1}.{w=0.1}.{w=0.1}"),
                ),
            ),
        )
        # Monika announces where she shoots next
        TURN_START_SHOT_ANNOUNCE = _QuipSet(
            _Quip(
                exprs=("1lta", "1lua"),
                lines=(
                    _("Maybe {square}..."),
                    _("Hmmm.{{w=0.1}}.{{w=0.1}}.{{w=0.1}} Let's try {square}."),
                    _("What are you hiding at.{{w=0.1}}.{{w=0.1}}.{{w=0.1}}{square}?"),
                ),
            ),
        )

        # Monika sunked first ship
        SUNK_SHIP_NORM = _QuipSet(
            _Quip(
                exprs=("1efu", "2efu", "1tfu", "2tfu", "1huu", "2huu"),
                lines=(
                    _("Ehehe, got this one~"),
                    _("Got your ship!"),
                    _("Sunk!"),
                    _("Oops, sunk~"),
                ),
            ),
        )
        # Monika sunked a few ships
        SUNK_SHIP_MULTIPLE = _QuipSet(
            _Quip(
                exprs=("1efu", "2efu", "1tfu", "2tfu", "1huu", "2huu"),
                lines=(
                    _("Another one goes~"),
                    _("Another one!"),
                    _("Looks like you lost another one~"),
                ),
            ),
        )

        LOST_SHIP_NORM = _QuipSet(
            _Quip(
                exprs=("2etp", "2rtp"),
                lines=(
                    _("Aww..."),
                    _("That's unfortunate..."),
                    _("Unlucky..."),
                    _("You got this one."),
                    _("{i}*Sigh*{/i}...{w=0.2} Sunk!"),
                ),
            ),
        )

        def __init__(self):
            """
            Constructor for AI player
            """
            super(BaseAIPlayer, self).__init__()
            self._turns_without_quip = 0
            self._targeting_ship_down = False

        def _pick_quip(self, quip, should_escape=False):
            """
            Picks a quip to show

            IN:
                quip - _Quip | _QuipSet - the quip to use
                should_escape - bool - whether or not to escape added tags (in case of formatting)

            OUT:
                tuple[str, str] - the expr and dlg to show
            """
            expr, dlg = quip.pick()

            if should_escape:
                suffix = "{{w=1.0}}{{nw}}"
            else:
                suffix = "{w=1.0}{nw}"

            return (expr, dlg + suffix)

        def _should_do_quip(self):
            """
            Checks if we should say a quip

            ASSUMES:
                the quip will be said if this method returns True,
                this is because it mutates the inner state every time it's called

            OUT:
                bool
            """
            # 13% if didn't say anything last 6 turns
            if self._turns_without_quip >= 6:
                chance = 0.13
            # 3% if did a quip last turn
            elif self._turns_without_quip == 0:
                chance = 0.03
            # 7% otherwise
            else:
                chance = 0.07
            if random.random() > chance:
                self._turns_without_quip += 1
                return False

            self._turns_without_quip = 0
            return True

        def pick_turn_start_quip(self, opponent, next_attack_coords):
            """
            Returns a quip for Monika's turn start

            IN:
                opponent - Player - the other player
                next_attack_coords - tuple[int, int] - coords for the next Monika's shot

            OUT:
                tuple[str, str] | None - the expression and the line or None
            """
            if self._targeting_ship_down:
                # We don't say anything if we're killing a ship,
                # it looks weird to say "where's your ship" while actively shooting at it
                # However if in the future we get a separete quip for that, we could move this check down
                # and use that quip instead of silence
                return None

            if not self._should_do_quip():
                return None

            player_ships_count = opponent.get_total_alive_ships()
            monika_ships_count = self.get_total_alive_ships()
            ship_diff = player_ships_count - monika_ships_count

            if ship_diff >= 2 and monika_ships_count <= 2 and random.random() > 0.15:
                return self._pick_quip(self.TURN_START_LOOKS_BAD)

            if player_ships_count == 1 and (monika_ships_count > 1 or random.random() > 0.25):
                return self._pick_quip(self.TURN_START_FINISH_HIM)

            if random.random() < 0.1:
                expr, what = self._pick_quip(self.TURN_START_SHOT_ANNOUNCE, should_escape=True)
                what = what.format(square=Battleship.square_coords_to_human_readable(next_attack_coords))
                return (expr, what)

            if ship_diff <= -1 and monika_ships_count >= 2:
                return self._pick_quip(self.TURN_START_TEASE)

            return self._pick_quip(self.TURN_START_NORM)

        def pick_hit_ship_quip(self, opponent, ship):
            """
            Returns a quip for when Monika hit a ship with her shot

            IN:
                opponent - Player - the other player
                ship - Ship - ship that got hit

            OUT:
                tuple[str, str] | None - the expression and the line or None
            """
            if not self._should_do_quip():
                return None

        def pick_sunk_ship_quip(self, opponent, ship):
            """
            Returns a quip for when Monika has sunked a ship

            IN:
                opponent - Player - the other player
                ship - Ship - sunked ship

            OUT:
                tuple[str, str] | None - the expression and the line or None
            """
            if not self._should_do_quip():
                return None

            if opponent.grid.total_ships != opponent.get_total_alive_ships() and random.random() < 0.4:
                return self._pick_quip(self.SUNK_SHIP_MULTIPLE)

            return self._pick_quip(self.SUNK_SHIP_NORM)

        def pick_lost_ship_quip(self, opponent, ship):
            """
            Returns a quip for when the player sunk Monika's ship

            IN:
                opponent - Player - the other player
                ship - Ship - sunked ship

            OUT:
                tuple[str, str] | None - the expression and the line or None
            """
            if not self._should_do_quip():
                return None

            return self._pick_quip(self.LOST_SHIP_NORM)

        def on_opponent_ship_hit(self, ship):
            super(BaseAIPlayer, self).on_opponent_ship_hit(ship)
            self._targeting_ship_down = True

        def on_opponent_ship_destroyed(self, ship):
            super(BaseAIPlayer, self).on_opponent_ship_destroyed(ship)
            self._targeting_ship_down = False

        def pick_square_for_attack(self, opponent):
            """
            AI picks a square for the next shot

            opponent - Player - the other player

            OUT:
                tuple[int, int] - coordinates of the square to shoot
            """
            raise NotImplementedError()

    class AIPlayer(BaseAIPlayer):
        """
        AI player that utilises probabilities in finding ships and targeting them down

        Credits to Nick Berry for the idea that become the core of this implementation

        ASSUMES:
            ships are from 2 to 5 squares long
            ships have spacing between them
        """
        def __init__(self, dataset):
            """
            Constructor

            IN:
                dataset - dict[tuple[int, int], int] | None - dataset of player grid
            """
            super(AIPlayer, self).__init__()
            self.dataset = dataset # type: dict[tuple[int, int], int] | None
            self.heatmap = {} # type: dict[tuple[int, int], int|float]
            # High weight means we rely more on where player puts their ships
            # and rely less on the current state of the board (skip misses/hits/where a ship truly fits)
            self.dataset_weight = 0.5
            self.dead_ships_squares = set() # type: set[tuple[int, int]]
            # We split the board into 2 types of squares
            self._remaining_white_squares = Grid.WIDTH * Grid.HEIGHT // 2
            self._remaining_black_squares = self._remaining_white_squares

        def _is_white_square(self, square):
            x, y = square
            is_x_even = x % 2 == 0
            is_y_even = y % 2 == 0
            return not (is_x_even ^ is_y_even)

        def register_hit(self, square):
            super(AIPlayer, self).register_hit(square)

            if self._is_white_square(square):
                self._remaining_white_squares -= 1
            else:
                self._remaining_black_squares -= 1

        def register_miss(self, square):
            super(AIPlayer, self).register_miss(square)

            if self._is_white_square(square):
                self._remaining_white_squares -= 1
            else:
                self._remaining_black_squares -= 1

        @staticmethod
        def _interpolate_num(a, b, f):
            """
            Interpolates a number from A to B using time fraction F

            IN:
                a - float - the start value of the number
                b - float - the final value of the number
                f - float - the time fraction, must be within [0.0, 1.0]

            OUT:
                float
            """
            return a + (b - a)*f

        def _get_max_temp(self):
            """
            Finds the maximum temp on the heatmap

            OUT:
                int - value of the max temperature
            """
            max_temp = -1
            for coords, temp in self.heatmap.iteritems():
                if temp > max_temp:
                    max_temp = temp

            if max_temp == -1:
                log_err("_get_max_temp failed to find max temperature coordinates")

            return max_temp

        def _get_max_temp_squares(self):
            """
            Finds the squares with the maximum temp on the heatmap

            OUT:
                tuple[tuple[int, int]] - tuple of coordinates with max temp (in case there's multiple)
            """
            max_temp = -1
            max_temp_coords = []
            for coords, temp in self.heatmap.iteritems():
                if temp > max_temp:
                    max_temp = temp
                    max_temp_coords[:] = [coords]
                elif temp == max_temp:
                    max_temp_coords.append(coords)

            if not max_temp_coords:
                log_err("_get_max_temp_squares failed to find max temperature coordinates")

            return tuple(max_temp_coords)

        def get_heatmap_colors(self):
            """
            Returns a dict coordinates: colour, used to render the heatmap
            for debugging

            OUT:
                dict[tuple[int, int], Color]
            """
            if not self.heatmap:
                return {}
            max_temp = self._get_max_temp()

            color_map = {}
            for coords, temp in self.heatmap.iteritems():
                if max_temp > 0:
                    fraction = float(temp) / max_temp
                else:
                    fraction = 0.0
                # red > yellow
                h = self._interpolate_num(0.0, 0.139, fraction**3)
                # gets more bleak/white
                s = self._interpolate_num(1.0, 0.0, fraction**10)
                # black > color as per hue
                v = self._interpolate_num(0.0, 1.0, store._warper.easein_quint(fraction))

                color_map[coords] = store.Color(hsv=(h, s, v))

            return color_map

        def _update_heatmap(self, opponent_grid):
            """
            Analyzes opponent grid using dealt hits and misses, and refills the heatmap
            NOTE: This is a heavy function, mind when you call it

            IN:
                opponent_grid - Grid - the grid of another player
            """
            ### START: internal utility functions
            def increment_temp(heatmap, squares, amount):
                """
                Increases temperature for the given points

                IN:
                    heatmap - dict[tuple[int, int], int] - heatmap to update
                    squares - Sequence[tuple[int, int]] - tuple of x,y coordinates for the ship
                    amount - int - temp increase

                OUT:
                    int - total temp increment across all the squares
                """
                total = 0
                for sqr in squares:
                    if sqr not in heatmap:
                        heatmap[sqr] = 0
                    if sqr not in self._hits:
                        heatmap[sqr] += amount
                        total += amount

                return total

            def is_ship_alive_at(square, grid):
                """
                Checks if there's a ship that's still active

                IN:
                    square - tuple[int, int] - the coordinates on the grid to check
                    grid - Grid - the grid where the ship presumably is

                ASSUMES:
                    We shoot at that square before (see Player.hits), otherwise it's cheating!

                OUT:
                    bool
                """
                ship = grid.get_ship_at(square)
                if ship is None:
                    log_err("_update_heatmap.is_ship_alive_at is called for a square with no ship")
                    return False
                return ship.is_alive()

            def has_hit_above(square, grid):
                """
                Checks if there's a succesful hit above the given square

                IN:
                    square - tuple[int, int] - the base square
                    grid - Grid - the grid to check for hits

                OUT:
                    bool
                """
                x, y = square
                if y > 0:
                    square_above = (x, y-1)
                    return square_above in self._hits and is_ship_alive_at(square_above, grid)
                return False

            def has_hit_to_right(square, grid):
                x, y = square
                if x + 1 < grid.WIDTH:
                    square_to_the_right = (x+1, y)
                    return square_to_the_right in self._hits and is_ship_alive_at(square_to_the_right, grid)
                return False

            def has_hit_below(square, grid):
                x, y = square
                if y + 1 < grid.HEIGHT:
                    square_below = (x, y+1)
                    return square_below in self._hits and is_ship_alive_at(square_below, grid)
                return False

            def has_hit_to_left(square, grid):
                x, y = square
                if x > 0:
                    square_to_the_left = (x-1, y)
                    return square_to_the_left in self._hits and is_ship_alive_at(square_to_the_left, grid)
                return False

            def get_temp_increment(squares, grid, is_vertical):
                """
                Returns temperature for the given points, the points are forming a line where
                a ship could fit. By default a square has temp of 1 for each ship it could contain.
                If there's successful hits along the line, we give extra temperature, if there's
                hits around or misseson the line, then there couldn't be a ship and we give it solid cold 0

                IN:
                    squares - Sequence[tuple[int, int]] - tuple of x,y coordinates for the ship
                    grid - Grid - the grid for which we fill the heatmap
                    is_vertical - bool - is this position vertical or horizontal

                OUT:
                    int - temperature for the points
                """
                bonus_temp = 0
                for i, coords in enumerate(squares):
                    # Known ship spacing, skip
                    if coords in self.dead_ships_squares:
                        return 0

                    # Known empty square, skip
                    if coords in self._misses:
                        return 0

                    # We previously hit a ship at this location?
                    if coords in self._hits:
                        # It's dead, skip
                        if not is_ship_alive_at(coords, grid):
                            return 0
                        # It's alive, prioritise finishing it
                        bonus_temp += 1000 * len(squares)

                    if i == 0:
                        # If there's hits before/around this ship bow, then this placement is impossible due to spacing between ships
                        if is_vertical:
                            if has_hit_above(coords, grid) or has_hit_to_left(coords, grid) or has_hit_to_right(coords, grid):
                                return 0
                        else:
                            if has_hit_to_left(coords, grid) or has_hit_above(coords, grid) or has_hit_below(coords, grid):
                                return 0

                    elif i == len(squares) - 1:
                        # Now check hits after/around this ship stern for the same reason
                        if is_vertical:
                            if has_hit_below(coords, grid) or has_hit_to_left(coords, grid) or has_hit_to_right(coords, grid):
                                return 0
                        else:
                            if has_hit_to_right(coords, grid) or has_hit_above(coords, grid) or has_hit_below(coords, grid):
                                return 0

                    else:
                        # Now check the middle of the ship for hits to its port/starboard
                        if is_vertical:
                            if has_hit_to_left(coords, grid) or has_hit_to_right(coords, grid):
                                return 0
                        else:
                            if has_hit_above(coords, grid) or has_hit_below(coords, grid):
                                return 0

                # Unexplored squares where a ship could possibly be have 1 by default
                return 1 + bonus_temp

            ### END: internal utility functions
            self.heatmap.clear()

            heatmap_sum = 0
            # NOTE: At first I wanted to consider only ships of unique length, but after a few tests,
            # it seems like Monika would perform just slightly worse. So we will iterate through every alive ship,
            # which is slower, but presumably gives better results. I'm not sure why this is the case,
            # mathematically it shouldn't matter, perhaps it's just a random occasion and I didn't run enough tests?
            for ship in opponent_grid.iter_ships():
                # Only count active ships
                if not ship.is_alive():
                    continue
                ship_length = ship.length

                for row in range(opponent_grid.HEIGHT):
                    for col in range(opponent_grid.WIDTH):
                        square = (col, row)
                        if square not in self.heatmap:
                            self.heatmap[square] = 0
                        if square in self.dead_ships_squares:
                            continue
                        if square in self._misses:
                            continue
                        if square in self._hits and not is_ship_alive_at(square, opponent_grid):
                            continue

                        # We only check right and down orientations since left and up would be just the same,
                        # no reason to do extra work
                        if col + ship_length - 1 < opponent_grid.WIDTH:
                            # Check how this ship could be placed horizontally from this square
                            squares = tuple(zip(range(col, col + ship_length), itertools.repeat(row, ship_length)))
                            amount = get_temp_increment(squares, opponent_grid, is_vertical=False)
                            if amount:
                                heatmap_sum += increment_temp(self.heatmap, squares, amount)

                        if row + ship_length - 1 < opponent_grid.HEIGHT:
                            # Check vertical placement of the ship
                            squares = tuple(zip(itertools.repeat(col, ship_length), range(row, row+ship_length)))
                            amount = get_temp_increment(squares, opponent_grid, is_vertical=True)
                            if amount:
                                heatmap_sum += increment_temp(self.heatmap, squares, amount)

            if not self.heatmap:
                # In case all ships are dead, use 0'd heatmap
                self.heatmap = {
                    (col, row): 0
                    for row in range(Grid.HEIGHT)
                    for col in range(Grid.WIDTH)
                }
            elif heatmap_sum and self.dataset is not None:
                # Otherwise enchance heatmap with the dataset we collected
                dataset_sum = sum(self.dataset.itervalues())
                if dataset_sum:
                    for coords, temp in self.heatmap.iteritems():
                        if not temp:
                            # 0 temp means we don't want to fire here at all
                            continue
                        # Normalise
                        temp = float(temp) / heatmap_sum
                        # Apply probabilities from the dataset
                        dataset_temp = float(self.dataset[coords]) / dataset_sum
                        self.heatmap[coords] = (temp*(1.0 - self.dataset_weight) + dataset_temp*self.dataset_weight) * 100

        def on_opponent_ship_destroyed(self, ship):
            super(AIPlayer, self).on_opponent_ship_destroyed(ship)

            for square in itertools.chain(*ship.get_squares()):
                self.dead_ships_squares.add(square)

        def on_game_loop_cycle(self, opponent):
            super(AIPlayer, self).on_game_loop_cycle(opponent)

            if renpy.config.developer:
                # This is slow and only used for debugging
                self._update_heatmap(opponent.grid)

        def _pick_best_square_from_list(self, squares):
            """
            Selects the best square from the given list

            IN:
                Sequence[tuple[int, int]] - list of grid squares

            OUT:
                tuple[int, int]
            """
            if len(squares) == 1:
                return squares[0]

            # square = random.choice(squares)
            should_focus_white = self._remaining_white_squares <= self._remaining_black_squares
            filtered_squares = [
                square
                for square in squares
                # If we're focusing white, filter out black, and vice versa
                if not (should_focus_white ^ self._is_white_square(square))
            ]
            if filtered_squares:
                # If we have any appropriate squares to shoot, we use them, otherwise shoot whatever we can
                squares = filtered_squares

            if len(squares) == 1:
                return squares[0]

            return random.choice(squares)

        def pick_square_for_attack(self, opponent):
            self._update_heatmap(opponent.grid)
            max_temp_coords = self._get_max_temp_squares()
            return self._pick_best_square_from_list(max_temp_coords)
