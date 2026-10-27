init -8 python in mas_battleship:
    class TestAgentPlayer(AIPlayer):
        """
        AI player for test games vs Monika
        """
        def __init__(self):
            super(TestAgentPlayer, self).__init__(None)


    class BattleshipAITest(Battleship):
        """
        Subclass for AI tests
        """
        def __init__(self):
            super(BattleshipAITest, self).__init__()
            self._player = TestAgentPlayer()

        def handle_player_turn(self):
            if not self.is_in_action():
                log_err("called BattleshipAITest.handle_player_turn while in {} phase, the game hasn't started yet".format(self._phase))
                return

            if self.is_monika_turn():
                return

            square = self._player.pick_square_for_attack(self._monika)
            if square is None:
                log_err("AIPlayer.pick_square_for_attack returned None")
                self._switch_turn()
                return

            if self._player.has_shot_at(square):
                log_err("AIPlayer.pick_square_for_attack returned a square that test agent already shot at")
                self._switch_turn()
                return

            if not self._debug_no_pause:
                renpy.pause(self.MONIKA_TURN_DURATION)

            self.register_player_shot(square)
            self._switch_turn()

        def render(self, width, height, st, at):
            main_render = super(BattleshipAITest, self).render(width, height, st, at)

            if self._debug_heatmap:
                for coords, color in self._player.get_heatmap_colors().iteritems():
                    color = color.replace_opacity(0.8)
                    heat_overlay = store.Solid(color, xsize=32, ysize=32)
                    x, y = self._grid_coords_to_screen_coords(coords, self.TRACKING_GRID_ORIGIN)
                    color_render = renpy.render(heat_overlay, width, height, st, at)
                    main_render.subpixel_blit(color_render, (x, y))

                    temp = str(round(self._player.heatmap[coords], 3))
                    txt = store.Text(temp, color=(0, 0, 0, 255), size=12, outlines=())
                    txt_render = renpy.render(txt, width, height, st, at)
                    main_render.subpixel_blit(txt_render, (x, y))

            return main_render


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_battleship_generate_heatmap_using_monte_carlo",
            category=["dev"],
            prompt="GENERATE BATTLESHIP HEATMAP USING MONTE CARLO",
            rules={"keep_idle_exp": None},
            pool=True,
            unlocked=True,
        )
    )

label mas_battleship_generate_heatmap_using_monte_carlo:
    $ iterations = store.mas_utils.tryparseint(
        renpy.input(
            "How many iterations would you like to run? Default 10000.",
            allow=numbers_only,
            length=5,
        ).strip("\t\n\r"),
        10000,
    )
    if iterations < 1:
        return

    $ use_player_data = False
    m 3eua "Should I use player dataset to influence the placement?{nw}"
    $ _history_list.pop()
    menu:
        m "Should I use player dataset to influence the placement?{fast}"

        "Yes.":
            $ use_player_data = True

        "No, just random.":
            pass

    m 1dsa "The game may hang, bear with me...{nw}"

    python:
        tmp_game = mas_battleship.Battleship()
        counter = {
            (x, y): 0
            for y in range(mas_battleship.Grid.HEIGHT)
            for x in range(mas_battleship.Grid.WIDTH)
        }

        for _unused in range(iterations):
            tmp_game.build_and_place_player_ships(use_player_data)

            for coords in tmp_game._player.grid.iter_squares_with_ships():
                counter[coords] += 1

        total = sum(counter.itervalues())
        tmp_game._monika.heatmap = {
            k: round(float(v) / total * 100, 2)
            for k, v in counter.iteritems()
        }
        tmp_game._debug_heatmap = True
        tmp_game._player.grid.clear()

    show monika 1eua at t31
    show screen mas_battleship_ui(tmp_game)
    m ""
    hide screen mas_battleship_ui
    show monika at t11

    m 3eua "Repeat?{nw}"
    $ _history_list.pop()
    menu:
        m "Repeat?{fast}"

        "Yes.":
            jump mas_battleship_generate_heatmap_using_monte_carlo

        "No.":
            pass

    $ del iterations, use_player_data, tmp_game, counter, total
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_battleship_show_player_dataset",
            category=["dev"],
            prompt="SHOW BATTLESHIP PLAYER DATASET",
            rules={"keep_idle_exp": None},
            pool=True,
            unlocked=True,
        )
    )

label mas_battleship_show_player_dataset:
    $ show_raw = False
    m 3eua "Raw or probabilities?{nw}"
    $ _history_list.pop()
    menu:
        m "Raw or probabilities?{fast}"

        "Raw.":
            $ show_raw = True

        "Probabilities":
            pass

    python:
        tmp_game = mas_battleship.Battleship()
        total = sum(persistent._mas_game_battleship_player_ship_dataset.itervalues())
        if show_raw:
            tmp_game._monika.heatmap = dict(persistent._mas_game_battleship_player_ship_dataset)
        else:
            tmp_game._monika.heatmap = {
                k: round(float(v) / total * 100, 2)
                for k, v in persistent._mas_game_battleship_player_ship_dataset.iteritems()
            }
        tmp_game._debug_heatmap = True

    show monika 1eua at t31
    show screen mas_battleship_ui(tmp_game)
    m ""
    hide screen mas_battleship_ui
    show monika at t11
    $ del show_raw, tmp_game, total
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_battleship_simulate_game",
            category=["dev"],
            prompt="SIMULATE BATTLESHIP GAME",
            rules={"keep_idle_exp": None},
            pool=True,
            unlocked=True,
        )
    )

label mas_battleship_simulate_game:
    show monika 1eua
    $ iterations = store.mas_utils.tryparseint(
        renpy.input(
            "How many iterations would you like to run? Default 10.",
            allow=numbers_only,
            length=5,
        ).strip("\t\n\r"),
        10,
    )
    if iterations < 1:
        return

    $ buttons = [
        ("Show boards (slower)?", "show_boards", False, True, False),
        ("Fast turns?", "fast_turns", True, True, False),
        ("Show Monika's ship (slower)?", "show_monika_ships", False, True, False),
        ("Show heatmap (slower)?", "show_heatmap", False, True, False),
        ("Should test agent position ships using dataset?", "agent_uses_dataset", False, True, False),
        ("Should Monika use dataset for shots?", "monika_uses_dataset", False, True, False),
    ]
    call screen mas_check_scrollable_menu(buttons, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, selected_button_prompt="Run", return_all=True)
    python:
        del buttons
        settings = _return

        test_agent_wins = 0
        monika_wins = 0

    if not settings["show_boards"]:
        m 1dsa "The game may hang, bear with me...{nw}"

label mas_battleship_simulate_game.loop:
    python:
        iterations -= 1
        tmp_game = mas_battleship.BattleshipAITest()
        if not settings["monika_uses_dataset"]:
            tmp_game._monika.dataset = None
        tmp_game._debug_heatmap = settings["show_heatmap"]
        tmp_game._debug_no_quips = True
        tmp_game._debug_no_pause = settings["fast_turns"]
        tmp_game._debug_monika_ships = settings["show_monika_ships"]
        tmp_game.build_and_place_monika_ships()
        tmp_game.build_and_place_player_ships(settings["agent_uses_dataset"])
        tmp_game.pick_first_player()
        tmp_game.set_phase_action()

    if settings["show_boards"]:
        show screen mas_battleship_ui(tmp_game)
        if not test_agent_wins and not monika_wins:
            show monika 1eua at t31
            pause 0.5

    python:
        while not tmp_game.is_done():
            tmp_game.game_loop()

    if tmp_game.is_player_winner():
        $ test_agent_wins += 1

    elif tmp_game.is_monika_winner():
        $ monika_wins += 1

    else:
        m 1esc "We're in an invalid state, it says player gave up. Aborting test."
        $ iterations = 0

    if iterations > 0:
        if settings["show_boards"]:
            pause 0.05
        jump mas_battleship_simulate_game.loop

    if settings["show_boards"]:
        hide screen mas_battleship_ui
        show monika at t11

    m 1esa "We're done, statistics: test agent wins [test_agent_wins], my wins [monika_wins]."

    m 3eua "Repeat?{nw}"
    $ _history_list.pop()
    menu:
        m "Repeat?{fast}"

        "Yes.":
            jump mas_battleship_simulate_game

        "No.":
            pass

    $ del iterations, settings, test_agent_wins, monika_wins, tmp_game
    return
