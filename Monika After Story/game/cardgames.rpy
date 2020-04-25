
# # # NOU CARDGAME

# NOU PERSISTENT VARS
default persistent._mas_game_nou_points = {"Monika": 0, "Player": 0}
default persistent._mas_game_nou_wins = {"Monika": 0, "Player": 0}
default persistent._mas_game_nou_abandoned = 0
default persistent._mas_game_nou_house_rules = {
    "win_points": 200,
    "start_cards": 7,
    "stack_d2": False,
    "play_wd4_anytime": False
}

# NOU CLASS DEF
init 5 python in mas_nou:

    from store import m, persistent, Solid
    from store.mas_cardgames import *

    ASSETS = "mod_assets/games/nou/"

    # Response constants
    NO_REACTION = 0
    MONIKA_REFLECTED_ACT = 1
    PLAYER_REFLECTED_ACT = 2
    MONIKA_REFLECTED_WDF = 3
    PLAYER_REFLECTED_WDF = 4
    MONIKA_REFLECTED_ACT_AFTER_WDF = 5
    PLAYER_REFLECTED_ACT_AFTER_WDF = 6
    MONIKA_REFLECTED_WCC = 7
    PLAYER_REFLECTED_WCC = 8

    # stats for curr sesh
    player_wins_this_sesh = 0
    monika_wins_this_sesh = 0

    player_win_streak = 0
    monika_win_streak = 0

    # are we playing a round or not
    in_progress = False

    # Last winner
    # NOTE: if this's not None, then we played in this sesh
    winner = None

    class NoU(object):
        """
        A class to represent a shedding card game - NoU
        Total cards in the deck: 108
        The one who first gets rid of cards wins the round
        The one who first reaches the points cap (default 200) wins the game
        One game takes about 5-10 minutes, you keep your points through sessions
            so you can start the game in one sesh and finish it later if you wish
        """
        # These constants represent parameters for nou cards
        TYPES = ("number", "action", "wild")
        NUMBER_LABELS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        ACTION_LABELS = ("Skip", "Draw Two", "Reverse")
        WILD_LABELS = ("Wild", "Wild Draw Four")
        COLOURS = ("red", "blue", "green", "yellow")

        # Coordinates
        DRAWPILE_X = 465
        DRAWPILE_Y = 352
        DISCARDPILE_X = 830
        DISCARDPILE_Y = 352
        PLAYERHAND_X = 640
        PLAYERHAND_Y = 595
        MONIKAHAND_X = PLAYERHAND_X
        MONIKAHAND_Y = 110
        PLAYER_CARDS_OFFSET = 0
        MONIKA_CARDS_OFFSET = -6

        # Quips for when we get a wdf as the first card for the discardpile
        QUIPS_MONIKA_RESHUFFLE_DECK = (
            _("Oh, let me shuffle it again.{w=1.5}{nw}"),
            _("Oops, let's try again.{w=1.5}{nw}")
        )

        # Quips that Monika can say at the start of each round
        QUIPS_MONIKA_PLAYS_TURN = (
            _("Oh, it's my turn."),
            _("My turn~"),
            _("I play first~")
        )
        QUIPS_MONIKA_SKIPS_TURN = (
            _("Oh, I have to skip my turn."),
            _("Lucky you, I skip this turn.")
        )
        QUIPS_MONIKA_DRAWS_CARDS = (
            _("Oh, I must draw some more."),
            _("Lucky you, I'll give you a handicap with these cards.")
        )
        QUIPS_MONIKA_WILL_REFLECT = (
            _("You better be ready~"),
            _("No, no, no~ I'm not going to skip this turn!"),
            _("Nope! This time you'll skip turn~")
        )

        QUIPS_PLAYER_PLAYS_TURN = (
            _("It's your turn, honey~"),
            _("You play first."),
            _("Your turn, [player].")
        )
        QUIPS_PLAYER_SKIPS_TURN = (
            _("Whoops! You have to skip your turn."),
            _("Unlucky!")
        )
        QUIPS_PLAYER_DRAWS_CARDS = (
            _("Go ahead and draw your cards, ehehe~"),
            _("Oops, you must draw more cards.")
        )

        # Quips if you pervert are trying to touch her hand
        QUIPS_PLAYER_CLICKS_MONIKA_CARDS = [
            _("[player], these're my cards!"),
            _("I see what you're doing, [player]~"),
            _("This's a little embarrassing~"),
            _("Ah?{w=0.2} What are you trying to do?~")
        ]
        # NOTE: would be nice to have a pm var for cheaters, but this should work too
        if persistent._mas_chess_skip_file_checks:
            QUIPS_PLAYER_CLICKS_MONIKA_CARDS.append(_("Are you trying to cheat again?"))

        # Maximum cards in hand
        HAND_CARDS_LIMIT = 30

        def __init__(self):
            """
            Constructor
            """
            self.table = Table(
                back=ASSETS + "cards/back.png",
                base=Solid(
                    "#00000000",
                    xsize=150,
                    ysize=214
                ),
                springback=0.3, rotate=0.15,
                can_drag=self.__can_drag
            )

            self.drawpile = self.table.stack(
                self.DRAWPILE_X, self.DRAWPILE_Y,
                xoff=-0.03, yoff=-0.08,
                click=True, drag=DRAG_TOP
            )

            self.discardpile = self.table.stack(
                self.DISCARDPILE_X, self.DISCARDPILE_Y,
                xoff=0.03, yoff=-0.08,
                drag=DRAG_TOP, drop=True
            )

            # I can leave it like this until the devs actually add it
            self.player = self.__Player(leftie=persistent._mas_pm_is_righty is False)
            self.monika = self.__AI(self, leftie=True)

            self.player.hand = self.table.stack(
                self.PLAYERHAND_X, self.PLAYERHAND_Y,
                xoff=self.__calculate_xoffset(self.player), yoff=0,
                click=True, drag=DRAG_CARD, drop=True, hover=True
            )

            self.monika.hand = self.table.stack(
                self.MONIKAHAND_X, self.MONIKAHAND_Y,
                xoff=self.__calculate_xoffset(self.monika, self.MONIKA_CARDS_OFFSET), yoff=0,
                click=True
            )

            self.set_sensitive(False)
            # list of dicts with various info about players state during their turns
            self.game_log = []
            # used for Moni's reaction labels (so we don't end up in an inf loop)
            self.has_jumped = False
            # NOTE: Start count from 1 because it's easier to use
            self.total_turns = 1

            self.__fill_drawpile()

        def __can_drag(self, table, stack, card):
            """
            Checks if you can drag card from stack

            OUT:
                True if you can, False otherwise
            """
            # Makes no sense to drag card if it's the only card in the discardpile
            if (
                stack is self.discardpile
                and len(self.discardpile) < 2
            ):
                return False
            return True

        def __springback_cards(self, hand):
            """
            Makes all cards in the given hand to spring back

            IN:
                hand - hand to spring back cards in
            """
            for card in hand:
                self.table.get_card(card).springback()

        def __say_quip(self, what):
            """
            Wrapper around renpy.say
            NOTE: always with interact = True

            IN:
                what - a list/tuple of quips or a single quip to say
            """
            if isinstance(quips, list, tuple):
                quip = renpy.random.choice(what)

            else:
                quip = what

            quip = renpy.substitute(quip)
            renpy.say(m, quip, True)

        def __calculate_xoffset(self, player, shift=0):
            """
            Determines the x offset depending on quantity of cards in player's hand

            IN:
                player - the player in whose hand we change the offset
                shift - extra offset
                    (Default: 0)

            OUT:
                integer as the offset

            ASSUMES:
                Monika is a leftie
            """
            # If the hand is None or there are less than 7 cards, we use 32
            offset = 32

            if player.hand is not None:
                amount = len(player.hand)

                if amount > 10:
                    offset = 28

                elif amount > 7:
                    offset = 30

            if player.isAI:
                if player.leftie:
                    xoffset = offset + shift
                else:
                    xoffset = -(offset + shift)

            else:
                if player.leftie:
                    xoffset = -(offset + shift)
                else:
                    xoffset = offset + shift

            return xoffset

        def __set_xoffset(self, player, shift=0):
            """
            Changes cards offset depending on quantity of cards in hand

            IN:
                player - the player in whose hand we change the offset
                shift - extra offset
                    (Default: 0)
            """
            player.hand.xoff = self.__calculate_xoffset(player, shift)
            self.__springback_cards(player.hand)

        def __calculate_xpos(self, player):
            """
            Determines position of the first card
            depending on quantity of cards in player's hand

            IN:
                player - the player in whose hand we change
                    the x attribute of the card

            OUT:
                integer as the x coordinate for the hand

            ASSUMES:
                we updated (if needed) the x offset for the hand before calling this
            """
            if player.isAI:
                xpos = self.MONIKAHAND_X

            else:
                xpos = self.PLAYERHAND_X

            if player.hand is not None:
                amount = len(player.hand) - 1
                offset = player.hand.xoff

            else:
                amount = 6
                offset = 32

            for i in range(amount):
                xpos -= (offset / 2)

            return xpos

        def __set_xpos(self, player):
            """
            Changes the placement of the first card
            depending on quantity of cards in player's hand

            IN:
                player - the player in whose hand we set
                    the x attribute of the card

            ASSUMES:
                we updated (if needed) the x offset for the hand before calling this
            """

            player.hand.x = self.__calculate_xpos(player)
            self.__springback_cards(player.hand)

        def __update_cards_positions(self, player, shift=0):
            """
            Updates cards positions in player's hand

            IN:
                player - the player for whose hand we update cards positions
                shift - extra offset (see __calculate_xoffset)
                    (Default: 0)
            """
            self.__set_xoffset(player, shift)
            self.__set_xpos(player)

        def __get_card_filename(self, card):
            """
            Generates filename for card based on its colour and type

            IN:
                card - card object

            OUT:
                string with filename w/o extension
            """
            # For non-Wild cards
            if card.colour:
                part1 = card.colour[0]

                if card.type == "number":
                    part2 = card.label
                else:
                    if card.label == "Skip":
                        part2 = 's'
                    elif card.label == "Draw Two":
                        part2 = "d2"
                    # "Reverse"
                    else:
                        part2 = 'r'

            # For Wild cards
            else:
                part1 = ""

                if card.label == "Wild":
                    part2 = "wcc"
                # "Wild Draw Four"
                else:
                    part2 = "wd4"

            return part1 + part2

        def __load_card_asset(self, card):
            """
            Associates a card object with its asset, adds it to the deck and sets it face down
            # NOTE: Thanks to Velius aka big pout booplicate for this cool card deck

            IN:
                card - card object
            """
            card_png = self.__get_card_filename(card)
            self.table.card(card, "{0}cards/{1}.png".format(ASSETS, card_png))
            self.table.set_faceup(card, False)

        def __fill_drawpile(self):
            """
            Fills the drawpile with cards

            NOTE: does not shuffles the drawpile
            """
            for type in self.TYPES:
                if type != "wild":
                    for colour in self.COLOURS:
                        # number cards
                        if type == "number":
                            for dupe in range(2):
                                for label in self.NUMBER_LABELS:
                                    # NOTE: we don't duplicate "0" cards
                                    if dupe == 1 and label == "0":
                                        continue
                                    else:
                                        card = self.__Card(type, label, colour)
                                        self.__load_card_asset(card)
                                        self.drawpile.append(card)
                        # action cards
                        else:
                            for dupe in range(2):
                                for label in self.ACTION_LABELS:
                                    card = self.__Card(type, label, colour)
                                    self.__load_card_asset(card)
                                    self.drawpile.append(card)
                # wild cards
                else:
                    for dupe in range(4):
                        for label in self.WILD_LABELS:
                            card = self.__Card(type, label)
                            self.__load_card_asset(card)
                            self.drawpile.append(card)

        def __update_drawpile(self):
            """
            Moves all - except the top one - cards from the discardpile
            onto the drawpile, then shuffles them
            """
            renpy.pause(0.5, True)

            while len(self.discardpile) > 1:
                card = self.discardpile[1]

                self.table.set_faceup(card, False)
                self.table.set_rotate(card, 0)
                self.table.get_card(card).pos_offsets = (0, 0)

                self.drawpile.append(card)

            renpy.pause(0.2, True)

            # align the last card
            last_card = self.table.get_card(self.discardpile[0])
            self.table.set_rotate(last_card.value, 90)
            last_card.pos_offsets = (0, 0)

            self.shuffle_deck()

        def __write_game_log(self, current_player, next_player):
            """
            Writes/updates the log with actions/attributes of the current and next players
            It does it at the end of every turn, we can back in any turn
                and check what happened there

            NOTE: have to do it in 2 steps:
                write first bits when the previous player ends their turn
                and add more data after the current player ends their turn
                and so on

            NOTE: for the reason above we update the log in prepare_game()
                for the 1st time

            IN:
                current_player - the player who ends their turn
                next_player - next played
            """
            next_player_data = {
                "turn": self.total_turns + 1,
                "player": next_player,
                "had_skip_turn": next_player.should_skip_turn,
                "had_draw_cards": next_player.should_draw_cards,
                "drew_card": None,
                "played_card": None
            }

            current_player_data = {
                "drew_card": current_player.drew_card,
                "played_card": current_player.played_cards[-1] if current_player.played_card else None
            }

            self.game_log[-1].update(current_player_data)
            self.game_log.append(next_player_data)

        def end_turn(self, current_player, next_player):
            """
            Updates players' attributes at the end of turn
            Also switches sensitivity and makes sure that the drawpile has cards

            IN:
                current_player - the player who ends their turn
                next_player - next player
            """
            if not self.drawpile:
                # BUG: we can still have an active interaction during this call
                # which will lead to a crash. Dirty fix: invoke this method
                # Look for renpy.end_interaction(value)
                renpy.invoke_in_new_context(self.__update_drawpile)

            self.__write_game_log(current_player, next_player)

            current_player.should_skip_turn = False
            current_player.plays_turn = False

            # now that we wrote 'should_skip_turn' in the log, we can set it to 0 if player reached the cap
            if len(next_player.hand) >= self.HAND_CARDS_LIMIT:
                # turn this off so you don't skip the dlg
                self.set_sensitive(False)

                if next_player.isAI:
                    renpy.say(m, "There's no way you could hold more cards, ahaha!", True)
                    renpy.say(m, "You don't have to draw more this turn, [player].", True)

                else:
                    renpy.say(m, "[player]...{w=0.2}look I can't hold all these cards!", True)
                    renpy.say(m, "And I can't draw more either, ehehe~", True)

                next_player.should_draw_cards = 0

            next_player.drew_card = False
            next_player.played_card = False
            next_player.plays_turn = True

            self.set_sensitive(not next_player.isAI)

            self.total_turns += 1

        def __win_check(self, player):
            """
            Checks if player can win the game (has no cards left)
            If we have a winner, we update wins and jump to the end game label
            The rest will be handled in the label

            IN:
                player - the player we check
            """
            if player.hand:
                return

            self.set_sensitive(False)

            global winner

            if player.isAI:
                winner = "Monika"
                persistent._mas_game_nou_wins[winner] += 1

            else:
                winner = "Player"
                persistent._mas_game_nou_wins[winner] += 1

            renpy.pause(2, True)
            renpy.jump("mas_nou_game_end")

        def __is_matching_card(self, player, card):
            """
            Checks if the given card matches the top card in the discardpile

            IN:
                player - the player who tries to play the card
                card - the card the player wants to play

            OUT:
                True if the player can play the card, False otherwise

            ASSUMES:
                len(discardpile) > 0
            """
            # sanity check
            if card not in player.hand:
                return False

            def has_colour(hand, colour):
                """
                Checks if there's a card with the given colour in the given hand
                NOTE: to avoid unwanted incidents, we don't check cards w/o colour

                IN:
                    hand - the hand we check
                    colour - the colour we're looking for

                OUT:
                    True if there is a card with that colour, False otherwise
                """
                return colour in [card.colour for card in hand if card.colour is not None]

            # "Attack rules"
            if not player.should_skip_turn:
                if (
                    card.label == "Wild"
                    or (
                        card.label == "Wild Draw Four"
                        and (
                                persistent._mas_game_nou_house_rules["play_wd4_anytime"]
                                or not has_colour(player.hand, self.discardpile[-1].colour)
                            )
                    )
                    or card.colour == self.discardpile[-1].colour
                    or card.label == self.discardpile[-1].label
                ):
                    return True
                else:
                    return False

            # "Defence rules"
            else:
                if (
                    (
                        self.discardpile[-1].label == "Wild Draw Four"
                        and card.label == "Draw Two"
                        and self.discardpile[-1].colour == card.colour
                    )
                    or (
                        self.discardpile[-1].label == "Draw Two"
                        and card.label == "Draw Two"
                    )
                    or (
                        self.discardpile[-1].label == "Skip"
                        and card.label == "Skip"
                        and self.discardpile[-1].colour == card.colour
                    )
                    or (
                        self.discardpile[-1].label == "Reverse"
                        and card.label == "Reverse"
                    )
                ):
                    return True
                else:
                    return False

        def play_card(self, current_player, next_player, card):
            """
            A method to play cards and change players' attributes
            NOTE: this doesn't check if the card matches

            IN:
                current_player - the player who plays card
                next_player - the player who will be affected by card if any
                card - card to play
            """
            # First get new rotation and offset for the card
            if current_player.isAI:
                cards_offset = self.MONIKA_CARDS_OFFSET
                card_rotation = renpy.random.randint(-193, -167)

            else:
                cards_offset = self.PLAYER_CARDS_OFFSET
                card_rotation = renpy.random.randint(-13, 13)

            card_position = (renpy.random.randint(-14, 14), renpy.random.randint(-10, 10))

            # now move the card and apply changes
            self.discardpile.append(card)
            self.table.set_rotate(self.discardpile[-1], card_rotation)
            self.table.get_card(self.discardpile[-1]).pos_offsets = card_position
            self.table.set_faceup(self.discardpile[-1], True)

            self.__update_cards_positions(current_player, cards_offset)

            # and update players' attributes
            current_player.played_card = True
            current_player.played_cards.append(card)

            if self.discardpile[-1].type == "action" or self.discardpile[-1].label == "Wild Draw Four":
                next_player.should_skip_turn = True
                current_player.should_skip_turn = False

                if self.discardpile[-1].label == "Draw Two":
                    next_player.should_draw_cards = 2

                    if persistent._mas_game_nou_house_rules["stack_d2"]:
                        next_player.should_draw_cards += current_player.should_draw_cards

                    current_player.should_draw_cards = 0

                elif self.discardpile[-1].label == "Wild Draw Four":
                    next_player.should_draw_cards = 4
                    current_player.should_draw_cards = 0

        def __actually_deal_cards(self, player, amount, smooth):
            """
            Moves cards from the drawpile into player's hand,
            updates offsets, rotation and sets cards faceup if needed

            NOTE: Unsafe to use this directly, we use deal_cards

            IN:
                player - the player who will get the cards
                amount - amount of cards to deal
                smooth - whether or not we use a little pause between dealing cards
            """
            for i in range(amount):
                if len(player.hand) >= self.HAND_CARDS_LIMIT:
                    return

                player.hand.append(self.drawpile[-1])

                if player.isAI:
                    self.table.set_rotate(player.hand[-1], -180)
                    offset = self.MONIKA_CARDS_OFFSET

                else:
                    self.table.set_faceup(player.hand[-1], True)
                    offset = self.PLAYER_CARDS_OFFSET

                self.__update_cards_positions(player, offset)

                if smooth:
                    renpy.pause(0.4)

        def deal_cards(self, player, amount=1, smooth=True):
            """
            Deals cards to players
            Also refreshing the drawpile if there're not enough cards

            IN:
                player - the player whose hand we deal cards in
                amount - amount of cards to deal
                    (Default: 1)
                smooth - whether or not we use a little pause between dealing cards
                    (Default: True)
            """
            drawpile_cards = len(self.drawpile)

            # there're enough cards for you
            if drawpile_cards >= amount:
                self.__actually_deal_cards(player, amount, smooth)

                if player.should_draw_cards:
                    player.should_draw_cards -= amount

            # there're not enough cards
            else:
                # deal as much as we can
                cards_to_deal = amount - drawpile_cards
                self.__actually_deal_cards(player, drawpile_cards, smooth)

                if player.should_draw_cards:
                    player.should_draw_cards -= drawpile_cards

                self.__update_drawpile()
                drawpile_cards = len(self.drawpile)

                # we should never get here, but just in case
                if drawpile_cards < cards_to_deal:
                    self.__actually_deal_cards(player, drawpile_cards, smooth)
                    player.should_draw_cards = 0

                # deal remaining cards
                else:
                    self.__actually_deal_cards(player, cards_to_deal, smooth)
                    player.should_draw_cards = 0

            player.drew_card = True

        def prepare_game(self):
            """
            This method sets up everything we need to start a game of NoU:
                1. Chooses who plays first
                2. Shuffles the deck
                3. Deals cards
                4. Places first card onto the discardpile
                    and handles if it's an action/wild card
                5. Writes first bits in the log
                6. Makes our table sensetive to the user's imput
                    if needed
            """
            # Decide who will play the first turn
            global player_win_streak
            global monika_win_streak

            if player_win_streak:
                current_player = self.player
                next_player = self.monika

            elif monika_win_streak:
                current_player = self.monika
                next_player = self.player

            else:
                if renpy.random.randint(0, 1):
                    current_player = self.player
                    next_player = self.monika

                else:
                    current_player = self.monika
                    next_player = self.player

            self.shuffle_deck()

            # Deal 14 cards or whatever you asked her for
            total_cards = persistent._mas_game_nou_house_rules["start_cards"] * 2 + 1
            for i in range(1, total_cards):
                if not i % 2:
                    temp_player = next_player
                else:
                    temp_player = current_player

                self.deal_cards(temp_player)
                temp_player.drew_card = False

            # We need to shuffle the deck if the top card is WDF
            ready = False
            pulled_wdf = False

            while not ready:
                card = self.drawpile[-1]

                self.discardpile.append(card)
                self.table.set_rotate(card, 90)
                self.table.set_faceup(card, True)

                if card.label == "Wild Draw Four":
                    if not pulled_wdf:
                        pulled_wdf = True
                        quip = renpy.substitute(renpy.random.choice(self.QUIPS_MONIKA_RESHUFFLE_DECK))
                        renpy.say(m, quip, True)
                        renpy.pause(0.5, True)

                    else:
                        renpy.pause(1, True)

                    self.drawpile.insert(47, card)
                    self.table.set_rotate(card, 0)
                    self.table.set_faceup(card, False)

                    renpy.pause(0.1, True)
                    self.shuffle_deck()

                else:
                    ready = True

            # The 1st player will choose a colour if it's WCC
            if self.discardpile[-1].label == "Wild":
                if current_player.isAI:
                    renpy.pause(0.5, True)
                    # BUG: Moni will announce the new colour and then say that it's her turn
                    # probably will fix it with the new changes I have in mind for choose_colour
                    self.discardpile[-1].colour = self.monika.choose_colour()

            # Unlucky! The 1st player should skip the turn
            elif self.discardpile[-1].type == "action":
                current_player.should_skip_turn = True

                # Even more, you should draw 2 cards!
                if self.discardpile[-1].label == "Draw Two":
                    current_player.should_draw_cards = 2

            # Need to write some info in the game log
            current_player_data = {
                "turn": self.total_turns,
                "player": current_player,
                "had_skip_turn": current_player.should_skip_turn,
                "had_draw_cards": current_player.should_draw_cards,
                "drew_card": None,
                "played_card": None
            }
            self.game_log.append(current_player_data)

            # FIXME: big oooof, how to improve these spaghetti?
            if current_player.isAI:
                if current_player.should_skip_turn:
                    can_reflect = current_player.choose_card()
                    current_player.forced_card = can_reflect

                    if can_reflect:
                        quips_to_use = self.QUIPS_MONIKA_WILL_REFLECT

                    elif current_player.should_draw_cards:
                        quips_to_use = self.QUIPS_MONIKA_DRAWS_CARDS

                    else:
                        quips_to_use = self.QUIPS_MONIKA_SKIPS_TURN

                else:
                    quips_to_use = self.QUIPS_MONIKA_PLAYS_TURN

            else:
                if current_player.should_skip_turn:
                    if current_player.should_draw_cards:
                        quips_to_use = self.QUIPS_PLAYER_DRAWS_CARDS

                    else:
                        quips_to_use = self.QUIPS_PLAYER_SKIPS_TURN

                else:
                    quips_to_use = self.QUIPS_PLAYER_PLAYS_TURN

            quip = renpy.substitute(renpy.random.choice(quips_to_use))

            renpy.say(m, quip, True)

            # Finally allow to interact with cards
            current_player.plays_turn = True
            self.set_sensitive(not current_player.isAI)

        def reset_game(self):
            """
            Reinitialize the game so you can start another round
            """
            del[self.monika]
            del[self.player]
            del[self.drawpile]
            del[self.discardpile]
            del[self.table]

            self.__init__()

        def player_turn_loop(self):
            """
            Tracks the player's actions and responds to their interactions
            """
            while self.player.plays_turn:
                actions = ui.interact()
                
                for evt in actions:
                    if evt.type == "hover":
                        if evt.card in self.player.hand:
                            # get this card from the table
                            card = self.table.get_card(evt.card)
                            # now move it
                            card.pos_offsets = (0, -35)
                            card.springback()

                            # this moves the card stack on top of rendering order
                            stack = card.stack
                            self.table.stacks.remove(stack)
                            self.table.stacks.append(stack)

                    elif evt.type == "unhover":
                        if evt.card in self.player.hand:
                            card = self.table.get_card(evt.card)

                            card.pos_offsets = (0, 0)
                            card.springback()

                    elif evt.type == "doubleclick":
                        # Player takes cards
                        if (
                            evt.stack is self.drawpile
                            and self.discardpile[-1].colour is not None
                            # check if you drew max cards already or just have to skip your turn
                            and not (
                                (
                                    self.player.drew_card
                                    or self.player.should_skip_turn
                                )
                                and not self.player.should_draw_cards
                            )
                        ):
                            self.set_sensitive(False)

                            if self.player.should_draw_cards:
                                self.deal_cards(self.player, self.player.should_draw_cards)
                            else:
                                self.deal_cards(self.player)

                            self.set_sensitive(True)

                    elif evt.type == "drag":
                        # if we're dragging, it means we've hovered before
                        # and we need to reset the offsets
                        card = self.table.get_card(evt.card)
                        card.pos_offsets = (0, 0)

                        # Player draws a card
                        if (
                            evt.stack is self.drawpile 
                            and evt.drop_stack is self.player.hand 
                            and self.discardpile[-1].colour is not None
                            and not (
                                (
                                    self.player.drew_card
                                    or self.player.should_skip_turn
                                )
                                and not self.player.should_draw_cards
                            )
                        ):
                            self.set_sensitive(False)
                            self.deal_cards(self.player)
                            self.set_sensitive(True)

                        # Player plays a card
                        elif (
                            evt.stack is self.player.hand 
                            and evt.drop_stack is self.discardpile 
                            and self.discardpile[-1].colour is not None
                            and not self.player.played_card
                            # Ensure that if you draw a card, then you can't play a defensive card anymore this turn
                            and not (self.player.should_skip_turn and self.player.drew_card)
                        ):
                            if self.__is_matching_card(self.player, evt.card):
                                self.play_card(self.player, self.monika, evt.card)

                                self.__win_check(self.player)

                                # NOTE: We don't leave if the player has to choose a colour
                                if self.discardpile[-1].colour is not None:
                                    self.end_turn(self.player, self.monika)

                    elif evt.type == "click":
                        if (
                            evt.stack is self.monika.hand
                            and not renpy.random.randint(0, 19)
                        ):
                            quip = renpy.substitute(renpy.random.choice(
                                self.QUIPS_PLAYER_CLICKS_MONIKA_CARDS
                                )
                            )
                            renpy.say(m, quip, True)

        def monika_turn_loop(self):
            """
            Monika's actions during her turn
            Yes, I know that this's not a loop
            """
            if not self.monika.plays_turn:
                return

            if not self.has_jumped:
                self.has_jumped = True
                time = 1 + renpy.random.random()
                renpy.pause(time, True)

                self.monika.shuffle_hand()
                self.monika.guess_player_cards()
                self.monika.play_card(self.monika.choose_card())

                reaction = self.monika.choose_reaction()

                if reaction["type"] != NO_REACTION:
                    renpy.call(reaction["label"], reaction["seen_count"])

            self.has_jumped = False
            self.end_turn(self.monika, self.player)

        def set_visible(self, value):
            """
            Shows/Hides cards on the table

            IN:
                value - True/False
            """
            if value:
                self.table.show()
            else:
                self.table.hide()

        def set_sensitive(self, value):
            """
            Make cards (in-)sensitive to the player's input

            IN:
                value - True/False
            """
            self.table.set_sensitive(value)

        def is_sensitive(self):
            """
            Checks if the table is sensitive to the input

            OUT:
                True if sensitive, False otherwise
            """
            return self.table.sensitive

        def shuffle_deck(self):
            """
            Shuffles the drawpile and animates cards shuffling

            ASSUMES:
                len(drawpile) > 15
            """
            total_cards = len(self.drawpile)

            # NOTE: Just in case, in theory the drawpile will have about 47 cards in the worst scenario
            if total_cards > 15:
                # 7/10
                k = renpy.random.randint(0, 9)
                renpy.pause(0.5, True)

                for i in range(7):
                    card_id = renpy.random.randint(0, total_cards - 2)
                    if k == i:
                        insert_id = total_cards - 1
                    else:
                        insert_id = renpy.random.randint(0, total_cards - 2)

                    card = self.table.get_card(self.drawpile[card_id])

                    x_offset = renpy.random.randint(160, 190)
                    y_offset = renpy.random.randint(-15, 15)

                    card.pos_offsets = (x_offset, y_offset)
                    card.springback()
                    renpy.pause(0.2, True)

                    self.drawpile.insert(insert_id, card.value)

                    card.pos_offsets = (0, 0)
                    card.springback()
                    renpy.pause(0.2, True)

            self.drawpile.shuffle()
            renpy.pause(0.5, True)

        # TODO: delete this
        def pass_func(self):
            pass

        class __Card(object):
            """
            A class to represent a card

            PROPERTIES:
                type - (str) number, action or wild
                label - (str) number/action on card '0'-'9', "Draw Two", etc
                colour - (str/None) red, blue, green, yellow or None
                    (Default: None (colourless))
                value - (int) how much points the card gives
            """
            def __init__(self, t, l, c=None):
                """
                Constructor

                IN:
                    t - type of the card
                    l - the card's label
                    c - the card's colour
                        (Default: None)
                """
                self.type = t
                self.label = l
                self.colour = c

                if self.type == "number":
                    self.value = int(self.label)

                elif self.type == "action":
                    self.value = 20

                else:
                    self.value = 50

            def __repr__(self):
                if self.colour is not None:
                    return self.colour + " " + self.label
                else:
                    return self.label

        class __Player(object):
            """
            A class to represent players

            PROPERTIES:
                leftie - (bool) is player leftie or rightie
                isAI - (bool) is it the Player or Monika
                hand - (stack) represents player's hand (a Stack object)
                drew_card - (bool) has player drew a card in this turn
                plays_turn - (bool) is it player's turn
                should_draw_cards - (int) should player draw cards and how much
                played_card - (bool) has player played a card in this turn
                played_cards - (list) list of all played card in this game by this player
                should_skip_turn - (bool) should player skip their turn
                yelled_nou - (bool) has player yelled "No U" before playing their last card
            """
            def __init__(self, leftie=False):
                """
                Constructor

                IN:
                    leftie - is player leftie or rightie
                """
                self.leftie = leftie
                self.isAI = False
                self.hand = None
                self.drew_card = False
                self.should_draw_cards = 0
                self.played_card = False
                self.played_cards = []
                self.plays_turn = False
                self.should_skip_turn = False
                self.yelled_nou = False
                # self.name = ""
                # self.points = 0

            def __repr__(self):
                return "<__Player {0}>".format(persistent.playername)

        class __AI(__Player):
            """
            AI variation of player
            TODO: after I make nou yelling system
                it should affect the way Moni plays. Like you didn't yell >
                she makes some minor mistakes assuming you're far from victory
                (basically everywhere I check for len() of the player's cards
                I will check for yelling nou too)

            PROPERTIES:
                everything from __Player
                game - (NoU) pointer for internal use
                cards_data - (dict) data about our cards (amount, values, ids)
                forced_card - (__Card) the card we want to play in the next turn
                player_cards_data - (dict) potentially the most common colour (or None)
                    and most rare colours (or an empty list) in the Player's hand
                    'reset_in' shows how much turns left until we reset 'has_colour'
                reactions - (list) all reactions that monika had during this game
                    (even if they didn't trigger)
            """
            def __init__(self, game, leftie=False):
                """
                Constructor

                IN:
                    leftie - is this player leftie or rightie
                    game - pointer to our NoU object
                """
                super(game.__AI, self).__init__(leftie)

                self.isAI = True
                self.game = game
                self.cards_data = {}
                self.forced_card = None
                self.player_cards_data = {
                    # we reset 'has_colour' to None in 'reset_in' turns
                    "reset_in": 0,
                    # we keep track only on 1 colour here
                    "has_colour": None,
                    # but keep track on multiple colours here
                    "lacks_colours": []
                }
                # all previous reactions
                # format: {"type": type, "label": reaction_label, "turn": id, "monika_card": card, "player_card": card, "seen_count": int}
                self.reactions = []

            def __repr__(self):
                return "<__AI Monika>"

            def __randomise_colour(self):
                """
                Chooses one of the colours at random
                Excludes the potential colour that the player may have
                If we know what the colours the player doesn't have,
                we will return one of them at random

                OUT:
                    string with one of 4 colours
                """
                if self.player_cards_data["lacks_colours"]:
                    return renpy.random.choice(self.player_cards_data["lacks_colours"])

                colours = list(self.game.COLOURS)

                if self.player_cards_data["has_colour"] is not None:
                    colours.remove(self.player_cards_data["has_colour"])

                return renpy.random.choice(colours)

            def guess_player_cards(self):
                """
                Guesses cards' colours in the player's hand
                NOTE: must run this before anything else
                NOTE: this and player_cards_data look terrible to me, but idk
                    how to make it better
                """
                # sanity check
                if len(self.game.game_log) < 2:
                    return

                # decrement if the pleyer played a card
                if (
                    self.player_cards_data["reset_in"] > 0
                    and self.game.game_log[-2]["played_card"] is not None
                ):
                    self.player_cards_data["reset_in"] -= 1

                # First let's guess what colour the player may have
                # when you set a new colour, you probably have cards with that colour
                if (
                    (
                        self.game.game_log[-2]["played_card"] is not None
                        and self.game.game_log[-2]["played_card"].type == "wild"
                    )
                    or (
                        self.game.total_turns == 2
                        and len(self.game.discardpile) > 1
                        and self.game.discardpile[-2].type == "wild"
                    )
                ):
                    colour = self.game.game_log[-2]["played_card"].colour

                    self.player_cards_data["has_colour"] = colour
                    self.player_cards_data["reset_in"] = 4

                    # remove it from the other dict
                    if colour in self.player_cards_data["lacks_colours"]:
                        self.player_cards_data["lacks_colours"].remove(colour)

                # Now guess what colour the player lacks
                # If you have to play wild cards, then you don't have the previous colour
                if (
                    # NOTE: the player can trick Monika here, but they won't
                    # get much from this so I'll leave it
                    self.game.game_log[-2]["played_card"] is not None
                    and self.game.game_log[-2]["played_card"].type == "wild"
                    and (
                        not persistent._mas_game_nou_house_rules["play_wd4_anytime"]
                        # 1/4
                        or not renpy.random.randint(0, 3)
                    )
                    and len(self.game.discardpile) > 1
                ):
                    if self.game.discardpile[-2].colour not in self.player_cards_data["lacks_colours"]:
                        self.player_cards_data["lacks_colours"].append(self.game.discardpile[-2].colour)

                    if self.player_cards_data["has_colour"] in self.player_cards_data["lacks_colours"]:
                        self.player_cards_data["has_colour"] = None

                # the player drew a card in their turn by their own will,
                # that means they might not have the current colour
                elif (
                    self.game.game_log[-2]["drew_card"]
                    and not self.game.game_log[-2]["had_skip_turn"]
                ):
                    # if not self.game.player.played_card:
                    # None means the player haven't played a card
                    if not self.game.game_log[-2]["played_card"]:
                        # NOTE: since the player drew a card and didn't play it, we can't be sure about
                        # other colours in the list
                        self.player_cards_data["lacks_colours"] = [self.game.discardpile[-1].colour]

                    elif self.game.discardpile[-2].colour not in self.player_cards_data["lacks_colours"]:
                        # append only if it's not in the list
                        self.player_cards_data["lacks_colours"].append(self.game.discardpile[-2].colour)

                    if self.player_cards_data["has_colour"] in self.player_cards_data["lacks_colours"]:
                        self.player_cards_data["has_colour"] = None

                # if the player lacks 3 colours, we can assume which colour they have
                if len(self.player_cards_data["lacks_colours"]) == 3:
                    missing_colours = self.player_cards_data["lacks_colours"]
                    all_colours = frozenset(self.game.COLOURS)

                    # now compare the set and the list, then iterate to get the only element from it
                    self.player_cards_data["has_colour"] = next(iter(all_colours.difference(missing_colours)))
                    self.player_cards_data["reset_in"] = 4

                # Now we check if we should reset some of our data
                # reset the data if the player drew 2+ cards in their turn
                if (
                    self.game.game_log[-2]["drew_card"]
                    and self.game.game_log[-2]["had_draw_cards"]
                ):
                    self.player_cards_data["lacks_colours"] = []

                # reset this data as outdated
                if self.player_cards_data["reset_in"] == 0:
                    self.player_cards_data["has_colour"] = None

            def __get_sorted_cards_data(self, keys_order=["num", "act"], values_order=["value", "amount"]):
                """
                Sorts (by keys and then values) the cards data dict
                and returns it as a list of tuples

                Example:
                    [
                        ('num_red', {'amount': 5, 'ids': [6, 1, 3, 12], 'value': 26}),
                        ('num_yellow', {'amount': 4, 'ids': [5, 10, 8, 11], 'value': 9}),
                        ...
                        ('act_yellow', {'amount': 2, 'ids': [2, 9], 'value': -1}),
                        ('wcc', {'amount': 0, 'ids': [], 'value': -1}),
                        ('wd4', {'amount': 1, 'ids': [4], 'value': -1})
                    ]

                IN:
                    NOTE: check sortKey for these
                    keys_order - the dict's key we're sortign by
                    values_order - the dict's values we're sorting by

                OUT:
                    sorted list of tuples

                ASSUMES:
                    cards_data
                """
                def sortKey(items, keys_order=["num", "act"], values_order=["value", "amount"]):
                    """
                    Function which we use as a sort key for cards data
                    NOTE: keys have priority over values,
                        and first elements have priority over last ones

                    IN:
                        items - tuples from the list from the cards data dict
                        keys_order - list of strings to sort the list by the dict's keys
                            (Default: ['num', 'act'])
                            For example: ['num'] will put number cards first
                            or ['red', 'act'] will put red coloured cards first, then action ones, and then the rest
                        values_order - list of strings to sort the list by the dict's values
                            (Default: ['value', 'amount'])
                            For exaple: the default list will sort by cards values first,
                            and then by their amount

                    OUT:
                        list which we'll use in sorting
                    """
                    # rv = []

                    # for key in keys_order:
                    #     rv.append(key in items[0])

                    # for value in values_order:
                    #     rv.append(items[1][value])

                    # return rv
                    return [(key in items[0]) for key in keys_order] + [(items[1][value]) for value in values_order]

                sorted_list = sorted(
                    self.cards_data.iteritems(),
                    key=lambda items: sortKey(
                        items,
                        keys_order,
                        values_order
                    ),
                    reverse=True
                )
                # renpy.invoke_in_new_context(
                #     renpy.say,
                #     who=m,
                #     what=str(sorted_list).replace("[", "[[").replace("{", "{{"),
                #     interact=True
                # )
                return sorted_list

            def __update_cards_data(self):
                """
                A method that represents cards in a Monika-friendly way (c)
                    NOTE: ids of number and action cards are sorted by cards value
                    NOTE: This should be called after any changes in Monika's hand,
                    and before she'll do anything with cards so Monika has an actual info about her cards
                """
                new_cards_data = {
                    "num_red": {
                        "amount": 0,
                        "value": 0,
                        "ids": []
                    },
                    "num_blue": {
                        "amount": 0,
                        "value": 0,
                        "ids": []
                    },
                    "num_green": {
                        "amount": 0,
                        "value": 0,
                        "ids": []
                    },
                    "num_yellow": {
                        "amount": 0,
                        "value": 0,
                        "ids": []
                    },
                    "act_red": {
                        "amount": 0,
                        "value": -1,
                        "ids": []   
                    },
                    "act_blue": {
                        "amount": 0,
                        "value": -1,
                        "ids": []   
                    },
                    "act_green": {
                        "amount": 0,
                        "value": -1,
                        "ids": []   
                    },
                    "act_yellow": {
                        "amount": 0,
                        "value": -1,
                        "ids": []   
                    },
                    "wd4": {
                        "amount": 0,
                        "value": -1,
                        "ids": []   
                    },
                    "wcc": {
                        "amount": 0,
                        "value": -1,
                        "ids": []   
                    }
                }

                # First make a sorted list of cards
                # don't reverse for one-round games
                # TODO: make sure it works good, otherwise just always use True
                should_reverse = bool(persistent._mas_game_nou_house_rules["win_points"])

                sorted_hand = [
                    card_obj.value for card_obj in sorted(
                        self.hand.cards,
                        key=lambda card_obj: card_obj.value.value,
                        reverse=should_reverse
                    )
                ]
                # renpy.invoke_in_new_context(
                #     renpy.say,
                #     who=m,
                #     what=str(sorted_hand).replace("[", "[["),
                #     interact=True
                # )
                # Now fill the dict with the sorted data
                for card in sorted_hand:
                    if card.type == "number":
                        new_cards_data["num_" + card.colour]["amount"] += 1
                        new_cards_data["num_" + card.colour]["value"] += card.value
                        # we sorted it, but have to use ids from the hand
                        new_cards_data["num_" + card.colour]["ids"].append(self.hand.index(card))

                    elif card.type == "action":
                        new_cards_data["act_" + card.colour]["amount"] += 1
                        # NOTE: We don't sum up values for action and wild cards
                        # new_cards_data["act_" + card.colour]["value"] += card.value
                        new_cards_data["act_" + card.colour]["ids"].append(self.hand.index(card))

                    elif card.label == "Wild Draw Four":
                        new_cards_data["wd4"]["amount"] += 1
                        # new_cards_data["wd4"]["value"] += card.value
                        new_cards_data["wd4"]["ids"].append(self.hand.index(card))

                    # Just Wild cards
                    else:
                        new_cards_data["wcc"]["amount"] += 1
                        # new_cards_data["wcc"]["value"] += card.value
                        new_cards_data["wcc"]["ids"].append(self.hand.index(card))

                self.cards_data = new_cards_data

            def shuffle_hand(self, chance=30):
                """
                Moves some cards in Monika's hand
                This's just for visuals
                NOTE: Since this changes cards' ids,
                    either do this at the start of the turn (optimal),
                    or update cards data again after shuffling (slow).

                IN:
                    chance - the chance for Monika to shuffle cards
                """
                if self.game.total_turns < 4:
                    # no point in doing anything
                    return

                total_cards = len(self.hand)
                if total_cards < 4:
                    # no point in doing anything
                    return

                rng = renpy.random.randint(1, 100)
                if rng > chance:
                    # we failed, return
                    return

                # how we want to shuffle
                shuffle_type = renpy.random.randint(0, 2)

                # just one
                if shuffle_type == 0:
                    # choose the card
                    card_id = renpy.random.randint(0, total_cards - 1)
                    # all ids we can insert to
                    free_ids = [id for id in range(total_cards - 1) if id != card_id]
                    # choose the id
                    insert_id = renpy.random.choice(free_ids)

                    card = self.hand[card_id]
                    self.hand.insert(insert_id, card)

                # shuffle some
                elif shuffle_type == 1:
                    all_ids = [id for id in range(total_cards - 1)]
                    ids_to_shuffle = []

                    # decide how much cards we'll shuffle
                    if total_cards > 12:
                        total_to_shuffle = 7
                    else:
                        total_to_shuffle = total_cards / 2

                    # make a list of ids we'll shuffle
                    for i in range(total_to_shuffle):
                        id = renpy.random.choice(all_ids)
                        all_ids.remove(id)
                        ids_to_shuffle.append(id)

                    for card_id in ids_to_shuffle:
                        # oof
                        free_ids = [id for id in range(total_cards - 1) if id != card_id]
                        insert_id = renpy.random.choice(free_ids)
                        card = self.hand[card_id]
                        self.hand.insert(insert_id, card)

                # shuffle (read sort) all
                else:
                    self.hand.cards.sort(key=lambda card: card.value.value, reverse=True)

                renpy.pause(0.5, True)

            def choose_colour(self):
                """
                Moni chooses colour to set for Wild cards

                OUT:
                    string with colour
                """
                def sortKey(id):
                    """
                    For action cards
                    Sorts by both cards colours and labels
                    """
                    labels = (
                        "Skip",
                        "Draw Two",
                        "Reverse"
                    )
                    colours = [sorted_cards_data[i][0].replace("num_", "") for i in range(4)]

                    rv = [self.hand[id].label == label for label in labels] + [self.hand[id].colour == colour for colour in colours]
                    return rv

                def announce_colour(colour):
                    """
                    TODO: move announcing to reactions
                    Wrapper around renpy.say

                    IN: colour - colour to announce
                    """
                    lines = (
                        _("I think I'll set...{{w=0.5}}{0} colour!"),
                        _("I want {0} colour."),
                        _("I choose {0} colour."),
                        _("Hmm.{{w=0.1}}.{{w=0.1}}.{{w=0.1}} I choose {0}!")
                    )
                    line = renpy.random.choice(lines)
                    renpy.say(m, line.format(colour), True)

                self.__update_cards_data()

                # just 1 card left, set either its colour or use rng
                if len(self.hand) == 1:
                    if self.hand[0].type == "wild":
                        colour = self.__randomise_colour()

                    else:
                        colour = self.hand[0].colour

                    announce_colour(colour)
                    return colour

                else:
                    if persistent._mas_game_nou_house_rules["win_points"]:
                        sorted_cards_data = self.__get_sorted_cards_data()
                    else:
                        # NOTE: use like this because value doesn't matter in games w/o points
                        sorted_cards_data = self.__get_sorted_cards_data(values_order=["amount"])

                    # more agressive
                    if len(self.game.player.hand) < 3:
                        action_ids = []

                        for colour in self.game.COLOURS:
                            # BUG: this doesn't respect colours since we sort later (might be fixed)
                            action_ids += self.cards_data["act_" + colour]["ids"]

                        if action_ids:
                            action_ids.sort(
                                key=sortKey,
                                reverse=True
                            )

                            self.forced_card = self.hand[action_ids[0]]

                            colour = self.forced_card.colour
                            announce_colour(colour)
                            return colour

                    # default
                    else:
                        sortByLabel = lambda card: (
                            card.label == "Skip",
                            card.label == "Draw Two",
                            card.label == "Reverse"
                        )

                        # we use amount in games where value doesn't make sense
                        if persistent._mas_game_nou_house_rules["win_points"]:
                            srt_data_key = "value"

                        else:
                            srt_data_key = "amount"

                        highest_value = sorted_cards_data[0][1][srt_data_key]

                        # no reason to enter the loop if we have no number cards
                        if highest_value:
                            for j in range(4):
                                # if the difference between the highest valued colour
                                # and the one we're checking is more than 60%,
                                # then it isn't worth it, leave to set colour by values of number cards
                                # can make it a var tbh
                                if (highest_value - sorted_cards_data[j][1][srt_data_key]) / highest_value >= 0.6:
                                    break

                                # try to find an action card with the colour of most valuebale number cards
                                if sorted_cards_data[j][1]["amount"]:
                                    # keep the colour part of the key but replace the card's type
                                    data_key = sorted_cards_data[j][0].replace("num_", "act_")

                                    if self.cards_data[data_key]["amount"]:
                                        # we play Skips in priority, then d2's and then reverses
                                        self.forced_card = sorted(
                                            [self.hand[id] for id in self.cards_data[data_key]["ids"]],
                                            key=sortByLabel,
                                            reverse=True
                                        )[0]

                                        colour = self.forced_card.colour
                                        announce_colour(colour)
                                        return colour

                    # fallback
                    if sorted_cards_data[0][1]["amount"]:
                        colour = sorted_cards_data[0][0].replace("num_", "")

                    elif sorted_cards_data[4][1]["amount"]:
                        colour = sorted_cards_data[4][0].replace("act_", "")

                    else:
                        colour = self.__randomise_colour()

                    announce_colour(colour)
                    return colour

            def choose_card(self):
                """
                Monika chooses a card to play
                There are different variants depending on the game state
                If Monika can't play a card, she'll draw one
                TODO: now that we have 'player_cards_data':
                    Moni could try not to play the colour the player has
                    if that will lead to their victory (<2 card?)
                    That especially will help in a situation where she
                    knows for sure that the palyer has only 1 colour

                OUT:
                    card if we found or drew one
                    or None if we don't want to (or can't) play a card this turn
                """
                # nested functions to analyse cards
                def analyse_numbers():
                    """
                    Goes through the cards data in the order we sorted it
                    and tries to find a number card that we can play

                    OUT:
                        card object if found a card, None otherwise

                    ASSUMES:
                        sorted_cards_data
                        player_cards_data
                    """
                    for colour_id in range(4):
                        # let's see if we want to play a 0
                        if sorted_cards_data[colour_id][1]["amount"]:
                            # get the last card as a possible 0
                            last_card = self.hand[
                                sorted_cards_data[colour_id][1]["ids"][-1]
                            ]

                            if (
                                last_card.label == "0"
                                and sorted_cards_data[colour_id][1]["amount"] > 2
                                and (
                                    last_card.colour in self.player_cards_data["lacks_colours"]
                                    or (
                                        # we can't be sure here, so just a guess play
                                        last_card.colour != self.player_cards_data["has_colour"]
                                        and len(self.game.player.hand) > 2
                                        and renpy.random.randint(0, 2) == 0
                                    )
                                )
                            ):
                                # if we've passed all checks, let's see if we actually can play the card
                                if self.game.__is_matching_card(self, card):
                                    return card

                        # try to play something
                        for id in sorted_cards_data[colour_id][1]["ids"]:
                            card = self.hand[id]

                            if self.game.__is_matching_card(self, card):
                                return card

                    return None

                def analyse_actions():
                    """
                    Goes through all action cards we have and tries to find
                    one that we can play this turn

                    OUT:
                        card object if we found one, None otherwise

                    ASSUMES:
                        sorted_cards_data
                        cards_data
                    """
                    # sortByLabel = lambda id: (
                    #     self.hand[id].label == "Skip",
                    #     self.hand[id].label == "Draw Two",
                    #     self.hand[id].label == "Reverse"
                    # )
                    action_cards_ids = []

                    def sortKey(id):
                        """
                        TODO: with this sort key it should respect both colours and labels
                        but I need more tests with this
                        """
                        labels = (
                            "Skip",
                            "Draw Two",
                            "Reverse"
                        )
                        colours = [sorted_cards_data[i][0].replace("num_", "") for i in range(4)]

                        rv = [self.hand[id].label == label for label in labels] + [self.hand[id].colour == colour for colour in colours]
                        return rv

                    for colour in self.game.COLOURS:
                        # BUG: this doesn't respect colours since we sort it later (might be fixed)
                        action_cards_ids += self.cards_data["act_" + colour]["ids"]

                    action_cards_ids.sort(key=sortKey, reverse=True)

                    for id in action_cards_ids:
                        card = self.hand[id]

                        if self.game.__is_matching_card(self, card):
                            return card

                    return None

                def analyse_wilds(label=None):
                    """
                    Return one of wilds we have

                    IN:
                        label - card label either 'wd4' or 'wcc'
                            (Default: None - any of wild cards)

                    OUT:
                        card object if we found one, None otherwise

                    ASSUMES:
                        cards_data
                    """
                    if not label:
                        wild_cards_ids = self.cards_data["wd4"]["ids"] + self.cards_data["wcc"]["ids"]

                    else:
                        wild_cards_ids = self.cards_data[label]["ids"]

                    # we don't have any wild cards
                    if not wild_cards_ids:
                        return None

                    card = self.hand[renpy.random.choice(wild_cards_ids)]

                    if self.game.__is_matching_card(self, card):
                        return card

                    # we should never get to this, but just in case
                    return None

                def analyse_cards(func_list):
                    """
                    Analyse all cards we have with funcs in func_list and return first
                    appropriate card we want and can play in this turn

                    IN:
                        func_list - a list/tuple of tuples with func, args and kwargs,
                            we call those to find the card

                    OUT:
                        card if we found one,
                        or None if no card was found
                    """
                    for func, args, kwargs in func_list:
                        card = func(*args, **kwargs)

                        if card is not None:
                            return card

                    return None

                self.__update_cards_data()

                total_cards = len(self.hand)

                # Monika has to skip turn
                if self.should_skip_turn:
                    # Let's try to play a defensive card
                    if persistent._mas_game_nou_house_rules["win_points"]:
                        # keys_order=["num"]
                        sorted_cards_data = self.__get_sorted_cards_data()
                    else:
                        sorted_cards_data = self.__get_sorted_cards_data(values_order=["amount"])

                    action_cards_ids = []

                    # make a list with action cards ordered by colours values
                    for i in reversed(range(4)):
                        # NOTE: 0-3 items are number cards, we start from less common ones
                        # to get rid of them
                        colour = sorted_cards_data[i][0].replace("num_", "")
                        action_cards_ids += self.cards_data["act_" + colour]["ids"]

                    # now try to play actions from our sorted list
                    for id in action_cards_ids:
                        card = self.hand[id]

                        if self.game.__is_matching_card(self, card):
                            return card

                    # Monika doesn't have the right card, and should draw some more
                    if self.should_draw_cards:
                        self.game.deal_cards(self, self.should_draw_cards)
                        # fall through

                # Just Monika's turn
                else:
                    # We have a card we wanted to play
                    if (
                        self.forced_card is not None
                        and self.game.__is_matching_card(self, self.forced_card)
                    ):
                        # TODO: might want to set it to None if we faield to play it
                        return self.forced_card

                    # We don't have forsed card or we can't play it
                    else:
                        # try to play the last card
                        if total_cards == 1:
                            card = self.hand[0]

                            if self.game.__is_matching_card(self, card):
                                return card

                        else:
                            if persistent._mas_game_nou_house_rules["win_points"]:
                                sorted_cards_data = self.__get_sorted_cards_data()
                            else:
                                sorted_cards_data = self.__get_sorted_cards_data(values_order=["amount"])

                            # the player is close to victory, need to play more aggressive
                            if (
                                total_cards > 5
                                and len(self.game.player.hand) < 4
                            ):
                                analysis = (
                                    (
                                        analyse_wilds,
                                        (),
                                        {"label": "wd4"}
                                    ),
                                    (
                                        analyse_actions,
                                        (),
                                        {}
                                    ),
                                    (
                                        analyse_numbers,
                                        (),
                                        {}
                                    ),
                                    (
                                        analyse_wilds,
                                        (),
                                        {"label": "wcc"}
                                    )
                                )

                            # standart logic
                            else:
                                analysis = (
                                    (
                                        analyse_numbers,
                                        (),
                                        {}
                                    ),
                                    (
                                        analyse_actions,
                                        (),
                                        {}
                                    ),
                                    (
                                        analyse_wilds,
                                        (),
                                        {}
                                    )
                                )

                            card = analyse_cards(analysis)

                            if card is not None:
                                return card

                        # Come here when Monika has nothing to play (or doesn't want to), must draw a card, then
                        self.game.deal_cards(self)
                        card = self.hand[-1]

                        if (
                            self.game.__is_matching_card(self, card)
                            # don't play it if it will make the player draw a card next turn
                            and (
                                # but always play if we have just 2 cards left
                                len(self.hand) < 3
                                # play if the player may have that colour
                                or self.game.discardpile[-1].colour not in self.player_cards_data["lacks_colours"]
                                # 1/5 to play anyway
                                or not renpy.random.randint(0, 4)
                            )
                        ):
                            return card

                # Come here when we don't want to/can't play a card
                return None

            def play_card(self, card):
                """
                Inner wrapper around play_card
                NOTE: no checks done here

                IN:
                    card - card to play
                """
                if not card:
                    return

                if card is self.forced_card:
                    self.forced_card = None

                self.game.play_card(self, self.game.player, card)

                self.game.__win_check(self)

                if (
                    self.game.discardpile[-1].type == "wild"
                ):
                    self.game.discardpile[-1].colour = self.choose_colour()

            def choose_reaction(self):
                """
                Helps Monika choose a dialogue based on state of the game
                TODO: reaction if Monika wasn't able to reflect card
                TODO: add odds so you won't trigger responses every time
                TODO: add at the end a reaction if you draw like 5 cards in a row (player 'lets' Moni win)
                TODO: quite hard, but would be cool if Moni could react on you both drawing cards
                    bc you can't play a card with the current colour
                TODO: won't work with the current choose_colour (since we announce colour there)
                    might need to return a card with choose_card and save itы attributes,
                    then use it here in response, and only after that actually play the card
                    quite complicated, but should worth it
                """
                def getLabelForReaction(reaction):
                    """
                    Gets the label corresponding to the given reaction

                    IN:
                        reaction - the reaction id

                    OUT:
                        string with the label for that reaction
                        or None if no reaction was found

                    ASSUMES:
                        reaction in reactions_map
                    """
                    reactions_map = {
                        NO_REACTION: None,
                        MONIKA_REFLECTED_ACT: "mas_nou_reaction_monika_reflected_act",
                        PLAYER_REFLECTED_ACT: "mas_nou_reaction_player_reflected_act",
                        MONIKA_REFLECTED_WDF: "mas_nou_reaction_monika_reflected_wdf",
                        PLAYER_REFLECTED_WDF: "mas_nou_reaction_player_reflected_wdf",
                        MONIKA_REFLECTED_ACT_AFTER_WDF: "mas_nou_reaction_monika_reflected_act_after_wdf",
                        PLAYER_REFLECTED_ACT_AFTER_WDF: "mas_nou_reaction_player_reflected_act_after_wdf",
                        MONIKA_REFLECTED_WCC: "mas_nou_reaction_monika_reflected_wcc",
                        PLAYER_REFLECTED_WCC: "mas_nou_reaction_player_reflected_wcc"
                    }

                    return reactions_map[reaction]

                # Someone reflected an action card
                if (
                    self.game.player.played_card
                    and self.game.player.played_cards
                    and self.game.player.played_cards[-1].type == "action"
                    and self.played_cards
                    and self.played_cards[-1].label == self.game.player.played_cards[-1].label
                ):
                    # it's Monika
                    if (
                        self.played_card
                        and self.game.player.should_skip_turn
                    ):
                        # Do we reflect a card that reflected a wild card before?
                        # Monika played a wd4 > the player reflected > Monika reflected
                        if (
                            len(self.game.game_log) > 2
                            and self.game.game_log[self.game.total_turns - 3]["player"] is self
                            and self.game.game_log[self.game.total_turns - 3]["played_card"] is not None
                            and self.game.game_log[self.game.total_turns - 3]["played_card"].label == "Wild Draw Four"
                        ):
                            reaction = {
                                "type": MONIKA_REFLECTED_ACT_AFTER_WDF,
                                "seen_count": 0
                            }

                        # the player played a wd4 > Monika reflected > the player reflected > Monika reflected
                        elif (
                            # len(self.game.game_log) > 3
                            # self.game.game_log[self.game.total_turns - 4]["player"] is self.game.player
                            # and self.game.game_log[self.game.total_turns - 4]["played_card"] is not None
                            # and self.game.game_log[self.game.total_turns - 4]["played_card"].label == "Wild Draw Four"
                            # NOTE: probably we don't need all these checks, just 2 are enough
                            self.reactions
                            and self.reactions[-1]["type"] == MONIKA_REFLECTED_WDF
                        ):
                            reaction = {
                                "type": MONIKA_REFLECTED_ACT_AFTER_WDF,
                                "seen_count": 0
                            }

                        # the player played a wd4 > Monika reflected > the player reflected > Monika reflected > the player reflected > Monika reflected and so on
                        elif (
                            self.reactions
                            and self.reactions[-1]["type"] == MONIKA_REFLECTED_ACT_AFTER_WDF
                        ):
                            reaction = {"type": MONIKA_REFLECTED_ACT_AFTER_WDF}

                            if (
                                len(self.reactions) > 1
                                and self.reactions[-2]["type"] == MONIKA_REFLECTED_ACT_AFTER_WDF
                                and self.reactions[-1]["type"] == MONIKA_REFLECTED_ACT_AFTER_WDF
                            ):
                                reaction["seen_count"] = 2

                            else:
                                reaction["seen_count"] = 1

                        # We don't, it's just the player played an act > Monika reflected
                        else:
                            reaction = {"type": MONIKA_REFLECTED_ACT}

                            # Monika keeps track on series of reactions
                            if (
                                len(self.reactions) > 1
                                and self.reactions[-2]["type"] == MONIKA_REFLECTED_ACT
                                and self.reactions[-1]["type"] == MONIKA_REFLECTED_ACT
                            ):
                                reaction["seen_count"] = 2

                            elif (
                                self.reactions
                                and self.reactions[-1]["type"] == MONIKA_REFLECTED_ACT
                            ):
                                reaction["seen_count"] = 1

                            else:
                                reaction["seen_count"] = 0

                        reaction["turn"] = self.game.total_turns
                        reaction["monika_card"] = self.played_cards[-1]
                        reaction["player_card"] = self.game.player.played_cards[-1]
                        reaction["label"] = getLabelForReaction(reaction["type"])

                        self.reactions.append(reaction)

                        return reaction

                    # it's the Player
                    elif (
                        not self.played_card
                        # and self.game.game_log[self.game.total_turns - 3]["played_card"]
                        and self.should_skip_turn
                    ):
                        # Monika played wd4 > the player reflected > Monika reflected > the player reflected
                        # NOTE: What did I mean by this??? > (also possible to get here from the case below when both player player 4 d2 which is quite hard to get)
                        if (
                            self.reactions
                            and self.reactions[-1]["type"] == MONIKA_REFLECTED_ACT_AFTER_WDF
                        ):
                            reaction = {
                                "type": PLAYER_REFLECTED_ACT_AFTER_WDF,
                                "turn": self.game.total_turns,
                                "monika_card": self.played_cards[-1],
                                "player_card": self.game.player.played_cards[-1],
                                "seen_count": 0
                            }

                            # TODO: could use seen_count a bit different: track for how long both players tried to reflect the card
                            # if (
                            #     len(self.reactions) > 1
                            #     and self.reactions[-2]["type"] == MONIKA_REFLECTED_ACT_AFTER_WDF
                            # ):
                            #     reaction["seen_count"] = 1

                            # else:
                            #     reaction["seen_count"] = 0

                            reaction["label"] = getLabelForReaction(reaction["type"])

                            self.reactions.append(reaction)

                            return reaction

                        # the player played wd4 > Monika reflected > the player reflected
                        elif (
                            self.reactions
                            and self.reactions[-1]["type"] == MONIKA_REFLECTED_WDF
                        ):
                            reaction = {
                                "type": PLAYER_REFLECTED_ACT_AFTER_WDF,
                                "turn": self.game.total_turns,
                                "monika_card": self.played_cards[-1],
                                "player_card": self.game.player.played_cards[-1],
                                "seen_count": 0
                            }

                            reaction["label"] = getLabelForReaction(reaction["type"])

                            self.reactions.append(reaction)

                            return reaction

                        # someone played act > ... > Monika mirrored > the player mirrored
                        elif (
                            self.game.game_log[self.game.total_turns - 3]["player"] is self
                            and self.game.game_log[self.game.total_turns - 3]["played_card"] is not None
                            and self.game.game_log[self.game.total_turns - 3]["played_card"].label == self.game.player.played_cards[-1].label
                        ):
                            reaction = {
                                "type": PLAYER_REFLECTED_ACT,
                                "turn": self.game.total_turns,
                                "monika_card": self.played_cards[-1],
                                "player_card": self.game.player.played_cards[-1],
                                "seen_count": 0
                            }

                            # TODO: could use seen_count a bit different: track for how long both players tried to reflect the card
                            # if (
                            #     self.reactions
                            #     and self.reactions[-1]["type"] == MONIKA_REFLECTED_ACT
                            # ):
                            #     reaction["seen_count"] = 1

                            # else:
                            #     reaction["seen_count"] = 0

                            reaction["label"] = getLabelForReaction(reaction["type"])

                            self.reactions.append(reaction)

                            return reaction

                        # NOTE: There's a possibility that we didn't return yet,
                        # so we have to fall through remaining checks

                # Monika mirrored a WDF card
                if (
                    self.game.player.played_cards
                    and self.game.player.played_cards[-1].label == "Wild Draw Four"
                    and self.game.player.should_skip_turn
                    and self.played_cards
                    and self.played_cards[-1].label == "Draw Two"
                ):
                    reaction = {
                        "type": MONIKA_REFLECTED_WDF,
                        "turn": self.game.total_turns,
                        "monika_card": self.played_cards[-1],
                        "player_card": self.game.player.played_cards[-1]
                    }

                    turns = 8
                    if sum(reaction["type"] == MONIKA_REFLECTED_WDF and reaction["turn"] >= self.game.total_turns - 2 * turns for reaction in self.reactions[-turns:]):
                        reaction["seen_count"] = 1
                    else:
                        reaction["seen_count"] = 0

                    reaction["label"] = getLabelForReaction(reaction["type"])

                    self.reactions.append(reaction)

                    return reaction

                # The Player mirrored a WDF card
                elif (
                    self.game.player.played_cards
                    and self.game.player.played_cards[-1].label == "Draw Two"
                    and not self.played_card
                    and self.played_cards
                    and self.played_cards[-1].label == "Wild Draw Four"
                    and self.should_skip_turn
                ):
                    reaction = {
                        "type": PLAYER_REFLECTED_WDF,
                        "turn": self.game.total_turns,
                        "monika_card": self.played_cards[-1],
                        "player_card": self.game.player.played_cards[-1]
                    }

                    turns = 8
                    if sum(reaction["type"] == PLAYER_REFLECTED_WDF and reaction["turn"] >= self.game.total_turns - 2 * turns for reaction in self.reactions[-turns:]):
                        reaction["seen_count"] = 1
                    else:
                        reaction["seen_count"] = 0

                    reaction["label"] = getLabelForReaction(reaction["type"])

                    self.reactions.append(reaction)

                    return reaction

                # Monika reflected a WCC card
                elif (
                    self.game.player.played_card
                    and self.game.player.played_cards[-1].label == "Wild"
                    and self.played_card
                    and self.played_cards[-1].label == "Wild"
                ):
                    reaction = {
                        "type": MONIKA_REFLECTED_WCC,
                        "turn": self.game.total_turns,
                        "monika_card": self.played_cards[-1],
                        "player_card": self.game.player.played_cards[-1]
                    }

                    turns = 8
                    if sum(reaction["type"] == MONIKA_REFLECTED_WCC and reaction["turn"] >= self.game.total_turns - 2 * turns for reaction in self.reactions[-turns:]):
                        reaction["seen_count"] = 1
                    else:
                        reaction["seen_count"] = 0

                    reaction["label"] = getLabelForReaction(reaction["type"])

                    self.reactions.append(reaction)

                    return reaction

                # The Player reflected a WCC card
                elif (
                    self.game.player.played_card
                    and self.game.player.played_cards[-1].label == "Wild"
                    and (
                        (
                            self.played_card
                            and len(self.played_cards) > 1
                            and self.played_cards[-2].label == "Wild"
                        )
                        or (
                            not self.played_card
                            and self.played_cards
                            and self.played_cards[-1].label == "Wild"
                        )
                    )
                ):
                    reaction = {
                        "type": PLAYER_REFLECTED_WCC,
                        "turn": self.game.total_turns,
                        "monika_card": self.played_cards[-1],
                        "player_card": self.game.player.played_cards[-1]
                    }

                    turns = 8
                    if sum(reaction["type"] == PLAYER_REFLECTED_WCC and reaction["turn"] >= self.game.total_turns - 2 * turns for reaction in self.reactions[-turns:]):
                        reaction["seen_count"] = 1
                    else:
                        reaction["seen_count"] = 0

                    reaction["label"] = getLabelForReaction(reaction["type"])

                    self.reactions.append(reaction)

                    return reaction

                # Monika has nothing to say
                reaction = {
                    "type": NO_REACTION,
                    "turn": self.game.total_turns,
                    "seen_count": 0
                }

                if self.played_cards:
                    reaction["monika_card"] = self.played_cards[-1]

                if self.game.player.played_cards:
                    reaction["player_card"] = self.game.player.played_cards[-1]

                reaction["label"] = getLabelForReaction(reaction["type"])

                self.reactions.append(reaction)

                return reaction

# END CLASS DEF

# UTIL FUNCTIONS
init 5 python in mas_nou:
        def give_points():
            """
            Gives points to the winner

            ASSUMES:
                mas_nou.game
                mas_nou.winner
            """
            global game
            global winner

            if (
                winner == "Monika"
                or winner == "Surrendered"
            ):
                _key = "Monika"
                loser = game.player

            elif winner == "Player":
                _key = "Player"
                loser = game.monika

            else:
                # just in case
                return

            # we don't forget to add points if you win the game with a d2 or wd4
            if loser.should_draw_cards:
                # NOTE: may need to call in new context just in case
                game.deal_cards(
                    player=loser,
                    amount=loser.should_draw_cards,
                    smooth=False
                )

            for card in loser.hand:
                persistent._mas_game_nou_points[_key] += card.value

        def reset_points():
            """
            Resets the persistent var to 0 for both Moni and the player
            """
            persistent._mas_game_nou_points["Monika"] = 0
            persistent._mas_game_nou_points["Player"] = 0

# Our events
# House rules unlocked after you finish your first game
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nou_change_house_rules",
            prompt="Let's change our house rules for NoU",
            category=["games"],
            pool=True,
            unlocked=False,
            conditional="persistent._mas_game_nou_wins['Monika'] or persistent._mas_game_nou_wins['Player']",
            action=EV_ACT_UNLOCK,
            rules={"no unlock": None},
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_nou_change_house_rules:
    if (
        persistent._mas_game_nou_house_rules["win_points"]
        and (
            persistent._mas_game_nou_points["Monika"]
            or persistent._mas_game_nou_points["Player"]
        )
    ):
        m 3eud "[player], we still haven't finished our game."
        m 1euc "If you want to play with new rules, then we'll have to start a new game next time."

    else:
        m 1eub "Of course."

    label .selection_loop:
        python:
            menu_items = [
                (
                    _("I'd like to change the amount of points required to win."),
                    "win_points",
                    False,
                    False
                ),
                (
                    _("I'd like to change the number of cards we start each round with."),
                    "start_cards",
                    False,
                    False
                ),
                (
                    _("I'd like to play with stackable Draw 2's.") if not persistent._mas_game_nou_house_rules["stack_d2"] else _("I'd like to play with non-stackable Draw 2's."),
                    "stack_d2",
                    False,
                    False
                ),
                (
                    _("I'd like to play with free Wild Draw 4's.") if not persistent._mas_game_nou_house_rules["play_wd4_anytime"] else _("I'd like to play with default Wild Draw 4's."),
                    "play_wd4_anytime",
                    False,
                    False
                )
            ]

            if not (
                persistent._mas_game_nou_house_rules["win_points"] == 200
                and persistent._mas_game_nou_house_rules["start_cards"] == 7
                and persistent._mas_game_nou_house_rules["stack_d2"] == False
                and persistent._mas_game_nou_house_rules["play_wd4_anytime"] == False
            ):
                menu_items.append((_("I'd like to go back to the classic rules."), "restore", False, False))

            final_item = (_("Nevermind"), False, False, False, 20)

        show monika 1eua at t21

        $ renpy.say(m, _("What kind of rule would you like to change?"), interact=False)

        call screen mas_gen_scrollable_menu(menu_items, mas_ui.SCROLLABLE_MENU_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

        show monika 1eua at t11

        if not _return:
            m 1eua "Oh, alright."
            python:
                del[menu_items]
                del[final_item]
            return

        elif _return == "win_points":
            m 1eub "Alright!"
            call monika_nou_change_house_rules.change_win_points_loop

        elif _return == "start_cards":
            m 1eub "Alright!"
            call monika_nou_change_house_rules.change_starting_cards_loop

        elif _return == "stack_d2":
            if not persistent._mas_game_nou_house_rules["stack_d2"]:
                m 1tub "Okay, but I must warn you that that might go against you~"

            else:
                m 1ttu "Did I go too hard at this game for you?"
                m 1hub "Ahaha~ I'm just kidding!"

            $ persistent._mas_game_nou_house_rules["stack_d2"] = not persistent._mas_game_nou_house_rules["stack_d2"]

        elif _return == "play_wd4_anytime":
            if not persistent._mas_game_nou_house_rules["play_wd4_anytime"]:
                # m "Oh, you better be ready for this one, [player]~"
                m 1eua "That sounds fun."

            else:
                m 1eua "Back to the classic rules, I see."

            $ persistent._mas_game_nou_house_rules["play_wd4_anytime"] = not persistent._mas_game_nou_house_rules["play_wd4_anytime"]

        else:
            m 3eub "Okay! Then settled!"

            python:
                persistent._mas_game_nou_house_rules["win_points"] = 200
                persistent._mas_game_nou_house_rules["start_cards"] = 7
                persistent._mas_game_nou_house_rules["stack_d2"] = False
                persistent._mas_game_nou_house_rules["play_wd4_anytime"] = False

                persistent._mas_game_nou_points["Monika"] = 0
                persistent._mas_game_nou_points["Player"] = 0

                del[menu_items]
                del[final_item]

            return

    $ persistent._mas_game_nou_points["Monika"] = 0
    $ persistent._mas_game_nou_points["Player"] = 0

    m 3eua "Is there anything else you would like to change?{nw}"
    $ _history_list.pop()
    menu:
        m "Is there anything else you would like to change?{fast}"

        "Yes.":
            jump monika_nou_change_house_rules.selection_loop

        "No.":
            m 2eub "Then let's play together soon~"

    python:
        del[menu_items]
        del[final_item]

    return

label .change_win_points_loop:
    $ ready = False
    while not ready:
        show monika 1eua at t11

        $ points_cap = store.mas_utils.tryparseint(
            renpy.input(
                "How many points would you like it to be?",
                allow=numbers_only,
                length=4
            ).strip("\t\n\r"),
            200
        )

        if points_cap < 0:
            m 2rksdla "[player], the game will never end, if the goal is negative."
            m 3ekb "Try again, silly!"

        elif points_cap == 0:
            m 3eua "Oh, you just want to have quick games?"
            m 2tuu "Alright! But don't expect me to go easy on you~"
            $ persistent._mas_game_nou_house_rules["win_points"] = points_cap
            $ ready = True

        elif points_cap < 50:
            m 3rksdlb "Hmm, It doesn't make sense to play with a point total {i}that{/i} small."
            m 1eka "We can play without points if you wish.{nw}"
            $ _history_list.pop()
            menu:
                m "We can play without points if you wish.{fast}"

                "I'd like that.":
                    m 1eub "Oh, alright!"
                    $ persistent._mas_game_nou_house_rules["win_points"] = 0
                    $ ready = True

                "No":
                    m 3eua "Then choose again."

        elif points_cap > 3000:
            m 2eka "Oh it's too much I think..."
            m 3eka "Let's leave it at 3000?{nw}"
            $ _history_list.pop()
            menu:
                m "Let's leave it at 3000?{fast}"

                "Alright.":
                    m 1eua "Settled."
                    $ persistent._mas_game_nou_house_rules["win_points"] = 3000
                    $ ready = True

                "No":
                    m 3eua "Then choose again."

        else:
            m 3eub "Okay, from now on, whoever reaches [points_cap] points, wins!"
            $ persistent._mas_game_nou_house_rules["win_points"] = points_cap
            $ ready = True

    $ del[ready]
    $ del[points_cap]

    return

label .change_starting_cards_loop:
    $ ready = False
    while not ready:
        show monika 1eua at t11

        $ starting_cards = store.mas_utils.tryparseint(
            renpy.input(
                "With how many cards would you like to start the game?",
                allow=numbers_only,
                length=2
            ).strip("\t\n\r"),
            7
        )

        if starting_cards < 1:
            m 2rksdlb "We can't play cards without cards, [player]!"
            m 3ekb "Try again, silly~"

        elif starting_cards < 4:
            m 2eka "I don't think this will makes sense, [player]..."
            m 3eka "Let's start with at least 4 cards?{nw}"
            $ _history_list.pop()
            menu:
                m "Let's start with at least 4 cards?{fast}"

                "Alright.":
                    $ persistent._mas_game_nou_house_rules["start_cards"] = 4
                    $ ready = True

                "No.":
                    m 3eua "Then try again."

        elif starting_cards > 20:
            m 2hub "Ahaha, [player]! How do you think I'll hold all these cards?"
            m 3eua "Let's leave it at 20 cards?{nw}"
            $ _history_list.pop()
            menu:
                m "Let's leave it at 20 cards?{fast}"

                "Alright.":
                    $ persistent._mas_game_nou_house_rules["start_cards"] = 20
                    $ ready = True

                "No.":
                    m 3eua "Then try again."

        else:
            $ _round = _("round") if persistent._mas_game_nou_house_rules["win_points"] else _("game")
            m 3eub "Okay, from now we will start each [_round!t] with [starting_cards] cards!"
            $ persistent._mas_game_nou_house_rules["start_cards"] = starting_cards
            $ ready = True

    $ del[ready]
    $ del[starting_cards]

    return

# Explaining rules unlocked after you give Monika the deck
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_nou_explain_rules",
            prompt="Can you explain NoU rules to me?",
            category=["games"],
            pool=True,
            unlocked=False,
            conditional="renpy.seen_label('mas_reaction_gift_carddeck')",
            action=EV_ACT_UNLOCK,
            rules={"no unlock": None},
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_nou_explain_rules:
    m 4eub "Even if the game looks complicated at first, it's rather quite simple."
    m 1eua "I'm sure if we play some more games, you'll get into it."
    m "We start the game with [persistent._mas_game_nou_house_rules[start_cards]] cards."
    m "Your goal is to play all your cards before I play mine."
    m 3eua "To play a card you need to match it by the color or the text on the card with the top card on the discard pile."
    m "If you can't play a card in your turn, you must draw one from the draw pile."
    m 1eua "You don't have to play it, though."
    m "After you played a card or skipped your turn, my turn begins. And so on until someone wins."
    m 4eub "Besides the Number cards, there're also special cards known as Action and Wild cards."
    m 4eua "You can distinguish an Action card by its symbol and a Wild card by its black color."
    m 1eua "Those cards can make your opponent skip their turn or even draw some cards."
    m 1tsu "And by some I mean 12 cards in a row."
    m 1eua "The Wild cards don't have a color which means they can be placed on any card."
    m 3eua "Although, there's one rule for Wild Draw Four. To play it you must have no other cards with the color of the discard pile."
    m 1eua "When you play any Wild card, you should choose what color you want to set for it."
    m "As powerful Wild and Action cards may look, you can still save yourself from them."
    m 3eub "For example you can mirror a Wild Draw Four by playing a Draw Two with the same color."
    m 3eua "Or you can play any Draw Two to mirror a Draw Two. The color won't matter in that case."
    m 1eua "I hope all that will give you a better understanding of the game."
    m 1eka "But I think the point of it is not winning anyway, right?"
    show monika 5ekbsa at t11 zorder MAS_MONIKA_Z with dissolve
    m 5ekbsa "It's all about spending time with the one you love~"
    m 5hubfa "Ehehe~"
    return

# The game handling label
label mas_nou_game_start:

    if (
        persistent._mas_game_nou_house_rules["win_points"]
        and (
                persistent._mas_game_nou_points["Monika"] > 0
                or persistent._mas_game_nou_points["Player"] > 0
        )
    ):
        if store.mas_nou.winner is not None:
            m "Let's continue~"

        else:
            m "Want to finish our game?"
            m 3eua "Let me grab that note with our score.{w=0.2}.{w=0.2}.{w=0.2}{nw}"

    else:
        m 1eub "Let's start!~"

    $ store.mas_nou.game = store.mas_nou.NoU()

    call mas_nou_game_loop
    return

label mas_nou_game_loop:

    window hide None
    if not store.mas_nou.in_progress:
        $ HKBHideButtons()
        $ disable_esc()
        scene bg cardgames desk with Fade(0.2, 0, 0.2)
        show screen nou_gui
        show screen nou_stats

        $ store.mas_nou.game.set_visible(True)
        pause 0.2
        $ store.mas_nou.game.prepare_game()
        $ store.mas_nou.in_progress = True

    python:
        while store.mas_nou.in_progress:
            store.mas_nou.game.player_turn_loop()
            store.mas_nou.game.monika_turn_loop()

    return

label mas_nou_game_end:

    $ store.mas_nou.in_progress = False
    $ store.mas_nou.game.set_visible(False)
    hide screen nou_stats
    hide screen nou_gui
    call spaceroom(scene_change=True, force_exp="monika 1eua")
    $ enable_esc()
    $ HKBShowButtons()

    if persistent._mas_game_nou_house_rules["win_points"]:
        $ _round = _("round")

    else:
        $ _round = _("game")

    $ choice = None

    if store.mas_nou.winner == "Player":
        call mas_nou_reaction_player_wins_round

        python:
            store.mas_nou.give_points()
            persistent._mas_game_nou_abandoned = 0
            store.mas_nou.player_wins_this_sesh += 1
            store.mas_nou.player_win_streak += 1
            store.mas_nou.monika_win_streak = 0
            persistent.ever_won["nou"] = True

        if (
            persistent._mas_game_nou_house_rules["win_points"]
            and persistent._mas_game_nou_points["Player"] >= persistent._mas_game_nou_house_rules["win_points"]
        ):
            call mas_nou_reaction_player_wins_game

            $ store.mas_nou.reset_points()

            m 1eua "Would you like to play more?{nw}"
            $ _history_list.pop()
            menu:
                m "Would you like to play more?{fast}"

                "Yes.":
                    m "Yay!"
                    python:
                        store.mas_nou.game.reset_game()
                        nou_ev = mas_getEV("mas_nou")
                        if nou_ev:
                            nou_ev.shown_count += 1

                    jump mas_nou_game_loop

                "No.":
                    m "Okay, just let me know when you want to play again~"

            $ del[choice]
            $ del[_round]
            $ del[store.mas_nou.game]
            return

    elif store.mas_nou.winner == "Monika":
        call mas_nou_reaction_monika_wins_round

        python:
            store.mas_nou.give_points()
            persistent._mas_game_nou_abandoned = 0
            store.mas_nou.monika_wins_this_sesh += 1
            store.mas_nou.monika_win_streak += 1
            store.mas_nou.player_win_streak = 0

        if (
            persistent._mas_game_nou_house_rules["win_points"]
            and persistent._mas_game_nou_points["Monika"] >= persistent._mas_game_nou_house_rules["win_points"]
        ):
            call mas_nou_reaction_monika_wins_game

            $ store.mas_nou.reset_points()

            m 1eua "Would you like to play more?{nw}"
            $ _history_list.pop()
            menu:
                m "Would you like to play more?{fast}"

                "Yes.":
                    m "Yay!"
                    python:
                        store.mas_nou.game.reset_game()
                        nou_ev = mas_getEV("mas_nou")
                        if nou_ev:
                            nou_ev.shown_count += 1

                    jump mas_nou_game_loop

                "No.":
                    m "Okay, just let me know when you want to play again~"

            $ del[choice]
            $ del[_round]
            $ del[store.mas_nou.game]
            return

    else:
        jump mas_nou_reaction_player_surrenders

        # we don't suggest to play again if the palyer don't want to play
        $ del[choice]
        $ del[_round]
        $ del[store.mas_nou.game]
        return

    m 1eua "Would you like to play another [_round!t]?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to play another [_round!t]?{fast}"

        "Yes.":
            python:
                store.mas_nou.game.reset_game()
                nou_ev = mas_getEV("mas_nou")
                if nou_ev:
                    nou_ev.shown_count += 1

            jump mas_nou_game_loop

        "No.":
            m "Alright, let's play again soon."

    $ del[choice]
    $ del[_round]
    $ del[store.mas_nou.game]
    return

# All reactions labels go here
label mas_nou_reaction_player_wins_round:
    if persistent._mas_game_nou_abandoned > 2:
        m "I'm glad you won this time!"
        m "Good job, [player]!"

    elif store.mas_nou.player_win_streak > 5:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "[player]...{w=0.5}you keep winning..."

            if len(store.mas_nou.game.monika.hand) > 2:
                m "I have no chance against you!"

            else:
                m "Give me at least a chance~"

        elif choice == 1:
            m "And another [_round!t]!"
            m "Incredible, [player]!"

        else:
            m "Wow! You won again!"
            m "Will you tell me your secret, [player]?"
            m "I want to win too~"

    elif store.mas_nou.player_win_streak > 2:
        $ choice = renpy.random.randint(0, 3)

        if not choice:
            m "And you won another [_round!t]!"
            m "You're really good!"

        elif choice == 1:
            m "Amazing, you won again!"
            m "But I'm sure I'll win next [_round!t]."

        elif choice == 2:
            m "Incredible! Another win for you!"
            m "Don't relax, though. {w=0.5}{nw}"
            extend "I'm sure I'll win next time!"

        else:
            m "You're lucky today."
            m "Ahaha~ Good job, [player]!"

    elif store.mas_nou.monika_win_streak > 5:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "I'm really glad you won this time~"

        elif choice == 1:
            m "I had a feeling you will win~"
            m "Ehehe~ Good, job!"

        else:
            if len(store.mas_nou.game.monika.hand) > 2:
                m "Your luck is back?~"
                m "Well played! {w=0.2}{nw}"
                extend "Ehehe~"

            else:
                m "Yay, you won!~"

    elif store.mas_nou.monika_win_streak > 2:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "Oh, you started playing seriously?"
            m "Ahaha~"

        elif choice == 1:
            if len(store.mas_nou.game.monika.hand) < 3:
                m "Ah... I almost won this one too!"
                m "Well played, [player]."

            else:
                m "You won, [player]!"
                if len(store.mas_nou.game.monika.hand) > 3:
                    m "That was amazing!"

        else:
            if store.mas_nou.game.total_turns > 50:
                m "You were really trying this time!"
                m "Great job, [player]!"

            else:
                m "And you won! Nice~"

    elif store.mas_nou.game.total_turns < 25:
        if store.mas_nou.player_win_streak > 0:
            $ choice = renpy.random.randint(0, 2)

            if not choice:
                m "Another quick win for you!"

                if renpy.random.randint(0, 4) > 3:
                    m "But you better not to relax, [player]~"

            elif choice == 1:
                m "Wow, [player]!"
                # TODO: this doesn't make sense imo
                m "I can't keep up with you!"

            else:
                if len(store.mas_nou.game.monika.hand) > 3:
                    m "Maybe I should try a bit harder?~"
                    m "Ehehe, you keep finishing [_round!t]s before I can do anything."

                else:
                    m "Ah...{w=0.1}I was so close!"
                    m "Good job, [player]!"

        elif (
            len(store.mas_nou.game.monika.hand) > 4
            or not store.mas_nou.game.player.yelled_nou
        ):
            m "Wow!{w=0.2} Played all your cards already?"
            m "That was quick!"

        else:
            $ choice = renpy.random.randint(0, 2)

            if not choice:
                m "Well played!"

            elif choice == 1:
                m "Impressive, [player]!"

            else:
                m "That was a quick [_round!t] for you!"

    elif store.mas_nou.game.total_turns > 75:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "A quite long [_round!t], [player]."

            if len(store.mas_nou.game.monika.hand) < 4:
                if store.mas_nou.player_win_streak > 0:
                    m "And I almost won this time!"

                else:
                    m "And I almost won!"

                m "Ahaha~ Well played!"

            else:
                m "Well played!"

        elif choice == 1:
            m "That was intense!"

        else:
            m "Ehehe~ You're really good!"

    else:
        $ choice = renpy.random.randint(0, 3)

        if not choice:
            if store.mas_nou.player_win_streak > 0:
                m "You won again!"

            else:
                m "You won!~"

        elif choice == 1:
            m "This [_round!t] is yours!"

        elif choice == 2:
            m "And you won! Good job!"
            if renpy.random.randint(0, 8) > 7:
                m "But don't expect to win everytime~"

        else:
            if store.mas_nou.monika_win_streak > 1:
                m "I'm glad you won this time~"

            m "Good job, [player]!"
    return

label mas_nou_reaction_player_wins_game:
    $ choice = renpy.random.randint(0, 3)

    if not choice:
        m "Oh!{w=0.2} Actually you won this game!"
        # TODO: check here for saying NoU and total turns
        m "I didn't notice you were so close to victory."
        m "Good job, ehehe~"

    elif choice == 1:
        m "Oh, and you won this game too!"
        m "Congratulations! Ehehe~"

    elif choice == 2:
        m "Let's see.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
        m "Oh, [player]! You won this game!"
        if mas_isMoniEnamored(higher=True) and not renpy.random.randint(0, 4):
            # m "I'd give you a big boop!"
            m "I would give you a big hug if I were near you~"
            m "Ehehe~"
        else:
            m "That was fun!"

    else:
        m "...And you're the first who reached [persistent._mas_game_nou_house_rules[win_points]] points!"
        m "Congrats, [player]~"
    return

label mas_nou_reaction_monika_wins_round:
    if persistent._mas_game_nou_abandoned > 2:
        m "I win!~"
        m "Thanks for playing with me, [player], {w=0.2}{nw}"
        extend "I'm sure you'll win next time!"

    elif store.mas_nou.player_win_streak > 5:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            if len(store.mas_nou.game.player.hand) > 4:
                m "I won!"
                m "..."
                m "Not without your help, I guess. Ehehe~"

            else:
                m "Told you I'll win!"
                m "Now it's time for you to draw cards."

        elif choice == 1:
            m "Ahaha! My luck is back~"

        else:
            m "There we go!"
            m "I finally won~"

    elif store.mas_nou.player_win_streak > 2:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "Don't relax, [player]~"

        elif choice == 1:
            m "I won!"

        else:
            m "Yay I won this time!~"

    elif store.mas_nou.monika_win_streak > 5:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "And another win for me!~"

        elif choice == 1:
            if len(store.mas_nou.game.player.hand) < 3:
                m "That was tough, [player]!"
                extend "You almost won this time."

            else:
                m "I have a feeling that you'll win next [_round!t]."

        else:
            if len(store.mas_nou.game.player.hand) < 3:
                m "Well played, [player]. But the win is mine again~"

            else:
                m "That was fun!"
                m "I hope you're enjoying playing with me, [player]~"
                m "Maybe next time you'll win."

    elif store.mas_nou.monika_win_streak > 2:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "Ehehe~ Another win for me~"

        elif choice == 1:
            if len(store.mas_nou.game.player.hand) < 3:
                m "You were quite close this time, [player]."

            else:
                m "Should I go easy on you?"
                m "Ahaha, just kidding, [player]~"

        else:
            m "I won again!"

    elif store.mas_nou.game.total_turns < 25:
        if store.mas_nou.monika_win_streak > 0:
            $ choice = renpy.random.randint(0, 2)

            if not choice:
                m "Another quick win for me!"

            elif choice == 1:
                m "Can't keep up with me, huh?~"

            else:
                m "Yay, I won again!"

        else:
            $ choice = renpy.random.randint(0, 1)

            if not choice:
                m "Yay, I won~"

            else:
                m "That was quick."

    elif store.mas_nou.game.total_turns > 75:
        $ choice = renpy.random.randint(0, 2)

        if not choice:
            m "That was a long [_round!t]!"

            if len(store.mas_nou.game.player.hand) < 4:
                if store.mas_nou.monika_win_streak > 0:
                    m "You almost won this time."

                else:
                    m "You almost won."

                m "Ehehe~ Well played!"

            else:
                m "Well played!"

        elif choice == 1:
            m "That was intense!"

        else:
            if len(store.mas_nou.game.player.hand) > 4:
                m "Not bad, [player]."
                m "I think you could even have won this time, if not for all those cards you drew"

            else:
                # sparkle pls
                m "Oh, I won!"

    else:
        if store.mas_nou.monika_win_streak > 0:
            m "I won again~"

        elif store.mas_nou.player_win_streak > 1:
            m "Finally I won too~"

        else:
            m "I won~"

    return

label mas_nou_reaction_monika_wins_game:
    $ choice = renpy.random.randint(0, 3)

    if not choice:
        m "And this time I won the game!"
        if (persistent._mas_game_nou_house_rules["win_points"] - persistent._mas_game_nou_points["Player"]) / persistent._mas_game_nou_house_rules["win_points"] < 0.2:
            m "You were quite close, though!"
            if renpy.random.randint(0, 14):
                m "I'm sure you'll win next time."

            # 1/15
            else:
                m "Did you let me win on purpose?"
                m "Ehehe~"

        else:
            # m "It's really interesting to play against you, [player]."
            m "I had a lot of fun!"
            m "I'm sure you'll win next time."

    elif choice == 1:
        m "Oh!{w=0.1} I won this game!"
        m "That was really fun!"
        if (persistent._mas_game_nou_house_rules["win_points"] - persistent._mas_game_nou_points["Player"]) / persistent._mas_game_nou_house_rules["win_points"] > 0.4:
            m "I hope you had fun too."
            # TODO: move it out of the RNG selection to 100% get it
            if (
                persistent._mas_game_nou_wins["Monika"] + persistent._mas_game_nou_wins["Player"] < 15
                and persistent._mas_game_nou_wins["Monika"] > persistent._mas_game_nou_wins["Player"]
            ):
                m "I'm sure if we play more games you'll win too."

            else:
                "Maybe next time you'll win~"

    elif choice == 2:
        m "I won this game too!"
        m "Ehehe~"
        m "Thanks for playing with me, [player]."

    else:
        m "And I'm the first who reached [persistent._mas_game_nou_house_rules[win_points]] points!"
        m "I won this time~"
    return

label mas_nou_reaction_player_surrenders:
    $ persistent._mas_game_nou_abandoned += 1
    $ store.mas_nou.player_win_streak = 0
    # TODO: consider silently add points to Monika here
    # so you can't abuse it when you're losing

    if persistent._mas_game_nou_abandoned > 4:
        m "That's alright, [player]..."
        m "But promise you'll finish the game next time?{w=0.4} For me?~"

    elif persistent._mas_game_nou_abandoned > 2:
        m "[player]...{w=0.3}{nw}"
        extend "you keep giving up on our games..."
        m "I hope you're enjoying playing with me."
        m "I do enjoy every moment I'm with you~"

    elif store.mas_nou.game.total_turns == 1:
        m "But we just started."
        m "Let me know when you'll have time."

    elif store.mas_nou.game.total_turns < 6:
        m "Giving up already, [player]?"
        if (
            len(store.mas_nou.game.monika.hand) < 5
            and len(store.mas_nou.game.player.hand) > 8
        ):
            m "I love to play with you no matter what the outcome is!"
            m "I hope you're feeling the same way."

        else:
            m "You could at least try..."

    else:
        # This part isn't really correct, but she just tries to support you
        if len(store.mas_nou.game.monika.hand) >= len(store.mas_nou.game.player.hand):
            m "I'm pretty sure you could win this [_round!t], [player]!"

        else:
            if len(store.mas_nou.game.monika.hand) > 1:
                m "Actually I had quite bad cards, [player]."
            else:
                m "Actually I had a quite bad card, [player]."

            m "I think you could win this [_round!t]."

        m "Don't give up so easily next time."
    return

label mas_nou_reaction_monika_reflected_act(seen_count=0):
    if seen_count == 0:
        m "I read you as an open book~"

    elif seen_count == 1:
        m "Nope!"

    else:
        m "Still nope~"
    jump mas_nou_game_loop

label mas_nou_reaction_player_reflected_act(seen_count=0):
    m "Just this time..."
    jump mas_nou_game_loop

label mas_nou_reaction_monika_reflected_wdf(seen_count=0):
    m "Ahaha! I knew you will do that!"
    jump mas_nou_game_loop

label mas_nou_reaction_player_reflected_wdf(seen_count=0):
    m "TODO: ME"
    jump mas_nou_game_loop

label mas_nou_reaction_monika_reflected_act_after_wdf(seen_count=0):
    if seen_count == 0:
        pass

    elif seen_count == 1:
        m "I don't think so, [player]!"

    else:
        pass
    jump mas_nou_game_loop

label mas_nou_reaction_player_reflected_act_after_wdf(seen_count=0):
    if seen_count == 0:
        m "Hmm, I wasn't prepared for this."

    else:
        m "Ehehe, I thought it was a simple game between lovers, not a tournament."
    jump mas_nou_game_loop

label mas_nou_reaction_monika_reflected_wcc(seen_count=0):
    jump mas_nou_game_loop

label mas_nou_reaction_player_reflected_wcc(seen_count=0):
    jump mas_nou_game_loop

# SL and stuff
# NOTE: Can be used in other games in the future
image bg cardgames desk = MASFilterSwitch(
    "mod_assets/games/nou/desk.png"
)
# Points screen
screen nou_stats():
    layer "master"
    zorder 0

    # TODO: this's temp, should use the generic func for changing styles
    if mas_isDayNow():
        style_prefix "nou"
    else:
        style_prefix "nou_dark"

    add MASFilterSwitch(
        "mod_assets/games/nou/note.png"
    ) pos (7, 120) anchor (0, 0) at nou_note_rotate_left

    # NOTE: Thanks to Briar aka @kkrosie123 for Monika's pen
    add MASFilterSwitch(
        "mod_assets/games/nou/pen.png"
    ) pos (225, 370) anchor (0.5, 0.5) at nou_pen_rotate_right

    text _("Our score!") pos (89, 110) anchor (0, 0.5) at nou_note_rotate_left

    # For one-round games we show wins
    if store.persistent._mas_game_nou_house_rules["win_points"] == 0:
        $ monika_score = store.mas_nou.monika_wins_this_sesh
        $ player_score = store.mas_nou.player_wins_this_sesh

    else:
        $ monika_score = store.persistent._mas_game_nou_points["Monika"]
        $ player_score = store.persistent._mas_game_nou_points["Player"]

    text _("Monika: [monika_score]") pos (62, 204) anchor (0, 0.5) at nou_note_rotate_left
    text _("[player]: [player_score]") pos (98, 298) anchor (0, 0.5) at nou_note_rotate_left

# Buttons screen
screen nou_gui():

    zorder 50
    
    if mas_isDayNow():
        style_prefix "nou"
    else:
        style_prefix "nou_dark"

    # $ turns = store.mas_nou.game.total_turns
    $ played_card = store.mas_nou.game.player.played_card
    $ end_turn = store.mas_nou.game.end_turn
    $ player = store.mas_nou.game.player
    $ monika = store.mas_nou.game.monika

    # Game menu
    vbox:
        xpos 1050
        ypos 360
        yanchor 0.5

        if (
            store.mas_nou.game.player.plays_turn 
            and (
                store.mas_nou.game.player.drew_card
                or store.mas_nou.game.player.should_skip_turn
            )
            and (
                not store.mas_nou.game.player.should_draw_cards
                or len(store.mas_nou.game.player.hand) >= store.mas_nou.game.HAND_CARDS_LIMIT
            )
            and (
                store.mas_nou.game.discardpile
                and store.mas_nou.game.discardpile[-1].colour is not None
            )
        ):
            textbutton _("Skip turn"):
                action [
                        Function(end_turn, player, monika),
                        Return([])
                    ]

        else:
            textbutton _("Skip turn")

        if store.mas_nou.game.player.plays_turn and not store.mas_nou.game.player.played_card:
            # TODO: need a func for this
            textbutton _("Yell 'No U!'"):
                action Function(store.mas_nou.game.pass_func)

        else:
            textbutton _("Yell 'No U!'")

        if not store.mas_nou.game.player.played_card:
            # TODO: need a func for this
            textbutton _("Remind Monika to yell 'No U!'"):
                action Function(store.mas_nou.game.pass_func)

        else:
            textbutton _("Remind Monika to yell 'No U!'")

        null height 30

        if store.mas_nou.game.player.hand and store.mas_nou.game.monika.hand:
            textbutton _("Give up"):
                action [
                        SetField(mas_nou, "winner", "Surrendered"),
                        SetField(mas_nou, "in_progress", False),
                        Jump("mas_nou_game_end")
                    ]

        else:
            textbutton _("Give up")

    # Choose colour menu
    vbox:
        xpos 640
        ypos 360
        anchor (0.5, 0.5)

        if (
            store.mas_nou.game.player.plays_turn
            # and store.mas_nou.game.is_sensitive()
            and (
                store.mas_nou.game.discardpile
                and store.mas_nou.game.discardpile[-1].colour is None
            )
            and store.mas_nou.game.player.hand
        ):
            $ top_card = store.mas_nou.game.discardpile[-1]

            textbutton _("Red"):
                xminimum 230
                action If(played_card,
                        true = [
                                SetField(top_card, "colour", "red"),
                                Function(end_turn, player, monika),
                                Return([])
                            ],
                        false = [
                                SetField(top_card, "colour", "red"),
                                Return([])
                            ]
                        )
            textbutton _("Blue"):
                xminimum 230
                action If(played_card,
                        true = [
                                SetField(top_card, "colour", "blue"),
                                Function(end_turn, player, monika),
                                Return([])
                            ],
                        false = [
                                SetField(top_card, "colour", "blue"),
                                Return([])
                            ]
                        )
            textbutton _("Green"):
                xminimum 230
                action If(played_card,
                        true = [
                                SetField(top_card, "colour", "green"),
                                Function(end_turn, player, monika),
                                Return([])
                            ],
                        false = [
                                SetField(top_card, "colour", "green"),
                                Return([])
                            ]
                        )
            textbutton _("Yellow"):
                xminimum 230
                action If(played_card,
                        true = [
                                SetField(top_card, "colour", "yellow"),
                                Function(end_turn, player, monika),
                                Return([])
                            ],
                        false = [
                                SetField(top_card, "colour", "yellow"),
                                Return([])
                            ]
                        )

# Styles for NoU GUI
style nou_vbox is vbox:
    spacing 5

style nou_dark_vbox is nou_vbox

style nou_button is generic_button_light:
    xsize 200
    ysize None
    ypadding 5

style nou_dark_button is generic_button_dark:
    xsize 200
    ysize None
    ypadding 5

style nou_button_text is generic_button_text_light:
    # xalign 0.5
    # yalign 0.5
    kerning 0.2
    layout "subtitle"
    text_align 0.5
    # line_leading 2

style nou_dark_button_text is generic_button_text_dark:
    # xalign 0.5
    # yalign 0.5
    kerning 0.2
    layout "subtitle"
    text_align 0.5

style nou_text:
    size 30
    color "#000"
    outlines []
    font "gui/font/m1.ttf"

style nou_dark_text is nou_text

transform nou_note_rotate_left:
    rotate -23
    rotate_pad True
    transform_anchor True

transform nou_pen_rotate_right:
    rotate 40
    rotate_pad True
    transform_anchor True

# # # FRAMEWORK FOR CARDGAMES

# Copyright 2008-2020 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

init -10 python in mas_cardgames:

    import pygame
    from store import RotoZoom, MASFilterSwitch

    # Drag type constants
    DRAG_NONE = 0
    DRAG_CARD = 1
    DRAG_ABOVE = 2
    DRAG_STACK = 3
    DRAG_TOP = 4

    def __rect_overlap_area(r1, r2):
        """
        Checks if 2 given rectangles overlap

        IN:
            r1, r2 - tuples of the following format: (x, y, w, h) 

        OUT:
            overlap between the 2 rectangles (False if they don't overlap)
        """
        if r1 is None or r2 is None:
            return 0

        x1, y1, w1, h1 = r1
        x2, y2, w2, h2 = r2

        maxleft = max(x1, x2)
        minright = min(x1 + w1, x2 + w2)
        maxtop = max(y1, y2)
        minbottom = min(y1 + h1, y2 + h2)

        if minright < maxleft:
            return 0

        if minbottom < maxtop:
            return 0

        return (minright - maxleft) * (minbottom - maxtop)

    def __default_can_drag(table, stack, card):
        """
        Function to check if the player can drag card
        NOTE: You can use yours in the constructor,
            but it must always take 3 arguments
            and return True or False

        IN:
            table - the table the card belongs to
            stack - the stack the card belongs to
            card - the card the player tries to drag

        OUT:
            True if the card is set faceup, False otherwise
        """
        return table.get_faceup(card)

    class Table(renpy.Displayable):
        """
        Table class to represent a "table" for card games

        PROPERTIES:
            back - the back of cards that don't have a more specific back defined
            base - the base of stacks that don't have a more specific base defined
            springback - the amount of time it takes for cards to springback into their rightful place
            rotate - the amount of time it takes for cards to rotate into their proper orientation
            can_drag - a function that is called to tell if we can drag a particular card
            doubleclick - the time between clicks for the click to be considered a double-click
            cards - a map from card value to the card object corresponding to that value
            stacks - a list of the stacks that have been defined
            sensitive - weather or not we're sensetive to the user's input
            last_event - last click event (CardEvent() obj)
            click_card - the card that has been clicked
            click_stack - the stack that has been clicked
            drag_cards - the list of cards that are being dragged
            dragging - weather or not we're dragging some cards
            click_x - the x position where we clicked
            click_y - the y position where we clicked
            st - the amount of time we've been shown for
        """

        def __init__(
            self,
            back=None,
            base=None,
            springback=0.1,
            rotate=0.1,
            can_drag=__default_can_drag,
            doubleclick=0.33,
            **kwargs
        ):
            """
            Constructor for Table objects

            IN:
                back - the back of cards that don't have a more specific back defined
                    (Default: None)
                base - the base of stacks that don't have a more specific base defined
                    (Default: None)
                springback - the amount of time it takes for cards to springback into their rightful place
                    (Default: 0.1)
                rotate - the amount of time it takes for cards to rotate into their proper orientation
                    (Default: 0.1)
                can_drag - a function that is called to tell if we can drag a particular card
                    (Default: __default_can_drag)
                doubleclick - the time between clicks for the click to be considered a double-click
                    (Default: 0.33)
            """
            super(renpy.Displayable, self).__init__(**kwargs)

            # We supports only these types
            if isinstance(back, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.back = MASFilterSwitch(back)

            # This's some kind of displayable or just None, but not an image
            else:
                self.back = renpy.easy.displayable_or_none(back)

            if isinstance(base, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.base = MASFilterSwitch(base)

            else:
                self.base = renpy.easy.displayable_or_none(base)

            self.springback = springback

            self.rotate = rotate

            self.can_drag = can_drag

            self.doubleclick = doubleclick

            # A map from card value to the card object corresponding to that value
            self.cards = {}

            # A list of the stacks that have been defined
            self.stacks = []

            self.sensitive = True

            self.last_event = CardEvent()

            self.click_card = None

            self.click_stack = None

            self.drag_cards = []

            self.dragging = False

            self.click_x = 0
            self.click_y = 0

            self.st = 0

        def show(self, layer="master"):
            """
            Shows the table on the given layer

            IN:
                layer - the layer we'll render our table om
                    (Default: "master")
            """
            for v in self.cards.itervalues():
                v.offset = __Fixed(0, 0)

            ui.layer(layer)
            ui.add(self)
            ui.close()

        def hide(self, layer="master"):
            """
            Hides the table on the given layer

            IN:
                layer - the layer we render our table om
                    (Default: "master")
            """
            ui.layer(layer)
            ui.remove(self)
            ui.close()

        def set_sensitive(self, value):
            """
            Changes the table's sensetivity

            IN:
                value - True if we set to sensetive, False otherwise
            """
            self.sensitive = value

        def get_card(self, value):
            """
            Gets the table's card object corresponding to the given value

            IN:
                value - your custom card object

            OUT:
                table's card object
            """
            if value not in self.cards:
                # raising an exception might be better
                # that gives an idea to coder that he's a dumbass
                raise Exception("No card has the value {0!r}.".format(value))

            return self.cards[value]

        def set_faceup(self, card, faceup=True):
            """
            Sets the given card faceup/down and makes renpy redraw the table

            in:
                card - card
                faceup - True if we set it faceup, False otherwise
                    (Default: True)
            """
            self.get_card(card).faceup = faceup
            renpy.redraw(self, 0)

        def get_faceup(self, card):
            """
            Checks if the given card is faceup

            IN:
                card - card

            OUT:
                True if the card is set faceup, False otherwise
            """
            return self.get_card(card).faceup

        def set_rotate(self, card, rotation):
            """
            Sets the rotation of the given card and makes renpy redraw the table

            IN:
                card - card
                rotation - rotation for the card
            """
            __Rotate(self.get_card(card), rotation)
            renpy.redraw(self, 0)

        def get_rotate(self, card):
            """
            Returns card rotation

            IN:
                card - card

            OUT:
                card's rotation
            """
            return self.get_card(card).rotate.rotate_limit()

        def add_marker(self, card, marker):
            """
            Adds marker on card and redraws the table

            IN:
                card - card
                marker - marker
            """
            self.get_card(card).markers.append(marker)
            renpy.redraw(self, 0)

        def remove_marker(self, card, marker):
            """
            Removes marker from card and redraws the table

            IN:
                card - card
                marker - marker
            """
            table_card = self.get_card(card)
            if marker in table_card.markers:
                table_card.markers.remove(marker)
                renpy.redraw(self, 0)

        def card(self, value, face, back=None):
            """
            Creates a card and adds it to the table's cards map

            IN:
                value - your custom card object
                face - is the card face up or face down
                back - the card's back
                    (Default: None)
            """
            self.cards[value] = __Card(self, value, face, back)

        def stack(
            self,
            x,
            y,
            xoff=0,
            yoff=0,
            show=1024,
            base=None,
            click=False,
            drag=DRAG_NONE,
            drop=False,
            hover=False,
            hidden=False
        ):
            """
            Creates a stack and adds it to the table's stacks list

            IN:
                x - the x position for the stack
                y - the y position for the stack
                xoff - the offset x for the stack
                    (Default: 0)
                yoff - the offset y for the stack
                    (Default: 0)
                show - maximum cards to render
                    (Default: 1024)
                base - img for the stack's base
                    (Default: None)
                click - whether or not the user can click on the stack
                    (Default: False)
                drag - the drag mode for the stack
                    (Default: DRAG_NONE)
                drop - whether or not the user can drop cards on the stack
                    (Default: False)
                hover - whether or not we respond to user hovering mouse over the stack
                    (Default: False)
                hidden - whether or not we hide the stack
                    (Default: False)

            OUT:
                new stack object
            """
            rv = __Stack(self, x, y, xoff, yoff, show, base, click, drag, drop, hover, hidden)

            self.stacks.append(rv)
            return rv

        def per_interact(self):
            """
            Forces redraw on each interaction
            """
            renpy.redraw(self, 0)

        def render(self, width, height, st, at):
            """
            Renders the table's stacks and cards that should be rendered
            """
            self.st = st

            rv = renpy.Render(width, height)

            for s in self.stacks:

                if s.hidden:
                    s.rect = None
                    for c in s.cards:
                        c.rect = None
                    continue

                s.render_to(rv, width, height, st, at)

                for c in s.cards:
                    c.render_to(rv, width, height, st, at)

            return rv

        def visit(self):
            """
            Returns a list of all displayable objects we use
            """
            stacks_bases = [stack.base for stack in self.stacks]
            cards_faces = [card.face for card in self.cards.itervalues()]
            cards_backs = [card.back for card in self.cards.itervalues()]

            return stacks_bases + cards_faces + cards_backs

        def event(self, ev, x, y, st):
            """
            Event handler
            This framework allows you to work with 5 event types
                each event has its own attributes (they share some of them):
                    'drag' - the user dragged 1 or more cards:
                        table
                        stack
                        card
                        drag_cards
                        drop_stack (can be None)
                        drop_card (can be None)
                        time
                    'click' and 'doubleclick' - the user
                        clicked somewhere:
                        table
                        stack
                        card (can be None)
                        time
                    'hover' and 'unhover' - the user started/ended
                        hovering mouse over card:
                        table
                        stack
                        card
                        time
                if the event doesn't have an attribute, it means the attribute is None

            OUT:
                list of events happened during this interaction
            """
            evt_list = []

            self.st = st

            if not self.sensitive:
                raise renpy.IgnoreEvent()

            grabbed = renpy.display.focus.get_grab()

            if (grabbed is not None) and (grabbed is not self):
                return

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.click_stack:
                    return

                stack = None
                card = None

                for s in self.stacks:

                    sx, sy, sw, sh = s.rect
                    if sx <= x and sy <= y and sx + sw > x and sy + sh > y:
                        stack = s


                    for c in s.cards[-s.show:]:
                        if c.rect is None:
                            continue

                        cx, cy, cw, ch = c.rect
                        if cx <= x and cy <= y and cx + cw > x and cy + ch > y:
                            card = c
                            stack = c.stack

                if stack is None:
                    return

                # Grab the display.
                renpy.display.focus.set_grab(self)

                # Don't let the user grab a moving card.
                if card is not None:
                    xoffset, yoffset = card.offset.offset()
                    if (xoffset or yoffset) and not card.hovered:
                        raise renpy.IgnoreEvent()

                # Move the stack containing the card to the front.
                self.stacks.remove(stack)
                self.stacks.append(stack)

                if stack.click or stack.drag:
                    self.click_card = card
                    self.click_stack = stack

                if (
                    card is None
                    or not self.can_drag(self, card.stack, card.value)
                ):
                    self.drag_cards = []

                elif card.stack.drag == DRAG_CARD:
                    self.drag_cards = [card]

                elif card.stack.drag == DRAG_ABOVE:
                    self.drag_cards = []
                    for c in card.stack.cards:
                        if c is card or self.drag_cards:
                            self.drag_cards.append(c)

                elif card.stack.drag == DRAG_STACK:
                    self.drag_cards = list(card.stack.cards)

                elif card.stack.drag == DRAG_TOP:
                    if card.stack.cards[-1] is card:
                        self.drag_cards = [card]
                    else:
                        self.drag_cards = []

                for c in self.drag_cards:
                    c.offset = __Fixed(0, 0)

                self.click_x = x
                self.click_y = y
                self.dragging = False

                renpy.redraw(self, 0)

                # raise renpy.IgnoreEvent()

            if ev.type == pygame.MOUSEMOTION or (ev.type == pygame.MOUSEBUTTONUP and ev.button == 1):
                if abs(x - self.click_x) > 7 or abs(y - self.click_y) > 7:
                    self.dragging = True

                dx = x - self.click_x
                dy = y - self.click_y

                for c in self.drag_cards:
                    xoffset, yoffset = c.offset.offset()

                    cdx = dx - xoffset
                    cdy = dy - yoffset

                    c.offset = __Fixed(dx, dy)

                    if c.rect:
                        cx, cy, cw, ch = c.rect
                        cx += cdx
                        cy += cdy
                        c.rect = (cx, cy, cw, ch)

                area = 0
                dststack = None
                dstcard = None

                for s in self.stacks:
                    if not s.drop:
                        continue

                    for c in self.drag_cards:

                        if c.stack == s:
                            continue
                        a = __rect_overlap_area(c.rect, s.rect)
                        if a >= area:
                            dststack = s
                            dstcard = None
                            area = a

                        for c1 in s.cards:
                            a = __rect_overlap_area(c.rect, c1.rect)
                            if a >= area:
                                dststack = s
                                dstcard = c1
                                area = a

                if area == 0:
                    dststack = None
                    dstcard = None
                
                renpy.redraw(self, 0)

                # if ev.type == pygame.MOUSEMOTION:
                #     raise renpy.IgnoreEvent()

            if (
                ev.type == pygame.MOUSEMOTION
                or (
                    (
                        ev.type == pygame.MOUSEBUTTONDOWN
                        or ev.type == pygame.MOUSEBUTTONUP
                    )
                    and ev.button == 1
                )
            ):
                if not self.drag_cards:
                    for s in self.stacks:
                        if not s.hover:
                            continue

                        for i, c in enumerate(s.cards):
                            if not c.rect:
                                continue

                            c_x_min, c_y_min, c_w, c_h = c.rect
                            c_x_max = 0
                            c_y_max = 0
                            # For the last card in the stack
                            if i == len(s.cards) - 1:
                                c_x_max = c_x_min + c_w
                                c_y_max = c_y_min + c_h
                            # For any card except the last one
                            # Also only if we have any x/y offsets
                            elif not s.xoff == 0 or not s.yoff == 0:
                                if abs(s.xoff) >= c_w:
                                    c_x_max = c_x_min + c_w

                                else:
                                    if s.xoff > 0:
                                        c_x_max = c_x_min + s.xoff

                                    elif s.xoff < 0:
                                        c_x_max = c_x_min + c_w
                                        c_x_min = c_x_min + c_w + s.xoff

                                    else:
                                        c_x_max = c_x_min + c_w

                                if abs(s.yoff) >= c_h:
                                    c_y_max = c_y_min + c_h

                                else:
                                    if s.yoff > 0:
                                        c_y_max = c_y_min + s.yoff

                                    elif s.yoff < 0:
                                        c_y_max = c_y_min + c_h + s.yoff
                                        c_y_min = c_y_min + s.yoff

                                    else:
                                        c_y_max = c_y_min + c_h

                            # if (
                            #     (s.xoff != 0 or c.pos_offsets[0]) and (s.yoff != 0 or c.pos_offsets[1])
                            # ):

                            # if s.xoff != 0 and (s.yoff != 0 or c.pos_offsets[1]):
                            #     extra_x_range = (c_x_max, c_x_min + c_w)
                            #     extra_y_range = 

                            # if c.pos_offsets[0] and (s.yoff != 0 or c.pos_offsets[1])

                            # Make an evt if we hover over this card
                            if c_x_min <= x < c_x_max and c_y_min <= y < c_y_max and c.hovered == False:
                                evt = CardEvent()
                                evt.type = "hover"
                                evt.table = self
                                evt.stack = s
                                evt.card = c.value
                                evt.time = st
                                c.hovered = True
                                evt_list.insert(0, evt)
                            # We don't hover over this card anymore
                            elif (not c_x_min <= x < c_x_max or not c_y_min <= y < c_y_max) and c.hovered == True:
                                evt = CardEvent()
                                evt.type = "unhover"
                                evt.table = self
                                evt.stack = s
                                evt.card = c.value
                                evt.time = st
                                c.hovered = False
                                evt_list.insert(0, evt)

            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                # Ungrab the display.
                renpy.display.focus.set_grab(None)

                evt = None

                if self.dragging:
                    if dststack is not None and self.drag_cards:

                        evt = CardEvent()
                        evt.type = "drag"
                        evt.table = self
                        evt.stack = self.click_stack
                        evt.card = self.click_card.value
                        evt.drag_cards = [c.value for c in self.drag_cards]
                        evt.drop_stack = dststack
                        if dstcard:
                            evt.drop_card = dstcard.value
                        evt.time = st

                else:

                    if self.click_stack is not None:
                        if self.click_stack.click:

                            evt = CardEvent()
                            evt.table = self
                            evt.stack = self.click_stack
                            if self.click_card:
                                evt.card = self.click_card.value
                            else:
                                evt.card = None
                            evt.time = st

                            if (
                                self.last_event.type == "click"
                                and self.last_event.stack == evt.stack
                                and self.last_event.card == evt.card
                                and self.last_event.time + self.doubleclick > evt.time
                            ):
                                evt.type = "doubleclick"
                            else:
                                evt.type = "click"

                if evt is not None:
                    self.last_event = evt
                    evt_list.append(evt)

                for c in self.drag_cards:
                    c.springback()

                self.click_card = None
                self.click_stack = None
                self.drag_cards = []

            if evt_list:
                return evt_list
            else:
                raise renpy.IgnoreEvent()

    class CardEvent(object):
        """
        Represents cards events
        PROPERTIES:
            type - the type of the event
            stack - the stack where the event started
            card - the card that triggered the event
            drag_cards - the cards we're dragging
            drop_stack - the stack we're dropping our cards on
            drop_card - the bottom card we're dropping
            time - the event time
        """

        def __init__(self):
            self.type = None
            self.stack = None
            self.card = None
            self.drag_cards = None
            self.drop_stack = None
            self.drop_card = None
            self.time = 0

    class __Stack(object):
        """
        Represents a stack of one or more cards, which can be placed on the table.

        PROPERTIES:
            table - the table the stack belongs to
            x/y - coordinates of the center of the top card of the stack
            xoff/yoff - the offset in the x and y directions of each successive card
            show - the number of cards to render
            base - the image that is shown behind the stack
            click - whether or not we report click events on the stack
            drag - the drag mode for the stack
            drop - whether or not the user can drop cards on the stack
            hover - whether or not we report hover/unhover events for the stack
            hidden - whether or not we render the stack
            cards - the list of cards in the stack
            rect - the rectangle for the background
        """
        def __init__(
            self,
            table,
            x,
            y,
            xoff,
            yoff,
            show,
            base,
            click,
            drag,
            drop,
            hover,
            hidden
        ):
            """
            Constructor for a stack
            NOTE: since we define stacks via the table method,
                they don't have default parameters in the init method

            IN:
                table - the table of this stack
                x - x of the center of the top card
                y - y of the center of the top card
                xoff - x offset of each successive card
                yoff - y offset of each successive card
                show - maximum cards to render
                base - the image for the base of this stack
                click - whether or not we report the user's clicks
                drag - the drag mode for this stack
                drop - whether or not the user's can drop cards on this stack
                hover -  whether or not we report hover events for the stack
                hidden - whether or not we render the stack
            """
            self.table = table

            self.x = x
            self.y = y

            self.xoff = xoff
            self.yoff = yoff

            self.show = show

            # If None, the background is taken from the table.
            if isinstance(base, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.base = MASFilterSwitch(base)

            elif base is not None:
                self.base = base

            elif self.table.base is not None:
                self.base = self.table.base

            else:
                raise Exception(
                    "Neither Stack {0} nor Table {1} has defined image for stack base.".format(self, self.table)
                )

            self.click = click
            self.drag = drag
            self.drop = drop
            self.hover = hover

            self.hidden = hidden

            self.cards = []

            self.rect = None

        def insert(self, index, card):
            """
            Inserts card in the stack at index

            IN:
                index - the index to insert the card at
                card - card to move
            """
            card = self.table.get_card(card)

            if card.stack:
                card.stack.cards.remove(card)

            card.stack = self
            self.cards.insert(index, card)

            self.table.stacks.remove(self)
            self.table.stacks.append(self)

            card.springback()

        def append(self, card):
            """
            Places card on the top of the stack

            IN:
                card - card to move
            """
            if card in self.cards:
                self.insert(len(self.cards) - 1, card)
            else:
                self.insert(len(self.cards), card)

        def remove(self, card):
            """
            Removes card from the stack
            NOTE: cards that don't have a stack won't be rendered!

            IN:
                card - card to remove
            """
            card = self.table.get_card(card)

            self.cards.remove(card)

            card.stack = None
            card.rect = None

        def index(self, card):
            """
            Returns card index in the stack

            IN:
                card - the card which index we're trying to find

            OUT:
                int as card index
                or None if no such card in the stack
            """
            card = self.table.get_card(card)

            try:
                id = self.cards.index(card)
            except ValueError:
                id = None

            return id

        def deal(self):
            """
            Removes the card at the top of the stack from the stack

            OUT:
                the card that was removed
                or None if the stack si empty
            """
            if not self.cards:
                return None

            card = self.cards[-1]
            self.remove(card.value)
            return card.value

        def shuffle(self):
            """
            Shuffles the cards in the stack
            """
            renpy.random.shuffle(self.cards)
            renpy.redraw(self.table, 0)

        def __repr__(self):
            return "<__Stack " + "{0!r}".format(self.cards).strip("[]") + ">"

        def __len__(self):
            return len(self.cards)

        def __getitem__(self, idx):
            if isinstance(idx, slice):
                return [card.value for card in self.cards[idx]]

            else:
                return self.cards[idx].value

        def __iter__(self):
            for i in self.cards:
                yield i.value

        def __contains__(self, card):
            return self.table.get_card(card) in self.cards

        def render_to(self, rv, width, height, st, at):
            """
            Blits the stack to the table's render
            """
            render = renpy.render(self.base, width, height, st, at)
            cw, ch = render.get_size()

            cx = self.x - cw / 2
            cy = self.y - ch / 2

            self.rect = (cx, cy, cw, ch)
            rv.blit(render, (cx, cy))

    class __Card(object):
        """
        Represent a card for our table
        NOTE: THIS IS NOT THE CLASS FOR YOUR CARDS
        This is only for internal use only

        PROPERTIES:
            table - the table the card belongs to
            value - value of the card (your card object)
            face - the face for the card
            back - the back for the card
            faceup - whether or not this card is set face up
            rotate - an object for cards rotation
            markers - a list of marker that will be rendered over the card
            stack - the stack the card belongs to
            offset - an object that gives the offset of this card relative to
                where it would normally be placed
            rect - the rectangle where this card was last drawn to the screen at
            hovered - whether or not the user hovered over this card
            pos_offsets - the offsets which you can use to change the card positions
        """
        def __init__(self, table, value, face, back):
            """
            The constructor for a card
            NOTE: no default values since we use the table method for defining cards

            table - the table of this card
            value - your card object corresponding to this card
            face - the face of this card
            back - the back of this card
            """
            self.table = table

            self.value = value

            self.face = MASFilterSwitch(face)

            if isinstance(back, (basestring, tuple, renpy.display.im.ImageBase, renpy.display.image.ImageReference)):
                self.back = MASFilterSwitch(back)

            elif back is not None:
                self.back = back

            elif self.table.back is not None:
                self.back = self.table.back

            else:
                raise Exception(
                    "Neither Card {0} nor Table {1} has defined image for card back.".format(self, self.table)
                )

            self.faceup = True

            self.rotate = None

            self.markers = []

            self.stack = None

            self.offset = __Fixed(0, 0)

            self.rect = None

            self.hovered = False

            # TODO: method to set these?
            self.pos_offsets = (0, 0)

            __Rotate(self, 0)

        def place(self):
            """
            Returns the base x and y placement of this card

            OUT:
                tuple with x and y coordinates of this card
            """
            s = self.stack
            offset = max(len(s.cards) - s.show, 0)
            index = max(s.cards.index(self) - offset, 0)

            x_pos_off, y_pos_off = self.pos_offsets

            return (x_pos_off + s.x + s.xoff * index, y_pos_off + s.y + s.yoff * index)

        def springback(self):
            """
            Makes this card to springback
            """
            if self.rect is None:
                self.offset = __Fixed(0, 0)
            else:
                self.offset = __Springback(self)

        def render_to(self, rv, width, height, st, at):
            """
            Blits the card to the table's render
            """

            x, y = self.place()
            xoffset, yoffset = self.offset.offset()
            x += xoffset
            y += yoffset

            if self.faceup:
                d = self.face
            else:
                d = self.back

            # TODO: Figure out if we can reuse some of this.

            if self.markers:
                d = Fixed(* ([d] + [renpy.easy.displayable(i) for i in self.markers]))

            r = self.rotate.rotate()
            if r:
                d = RotoZoom(r, r, 0, 1, 1, 0)(d)

            render = renpy.render(d, width, height, st, at)
            w, h = render.get_size()

            x -= w / 2
            y -= h / 2

            self.rect = (x, y, w, h)

            rv.blit(render, (x, y))

        def __repr__(self):
            return "<__Card {0!r}>".format(self.value)

    class __Springback(object):

        def __init__(self, card):
            self.card = card
            self.table = table = card.table

            self.start = table.st

            cx, cy, cw, ch = self.card.rect
            x = cx + cw / 2
            y = cy + ch / 2

            self.startx = x
            self.starty = y

        def offset(self):

            t = (self.table.st - self.start) / self.table.springback
            t = min(t, 1.0)

            if t < 1.0:
                renpy.redraw(self.table, 0)

            px, py = self.card.place()

            return int((self.startx - px) * (1.0 - t)), int((self.starty - py) * (1.0 - t))

    class __Fixed(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def offset(self):
            return self.x, self.y

    class __Rotate(object):
        def __init__(self, card, amount):

            self.table = table = card.table
            self.start = table.st

            if card.rotate is None:
                self.start_rotate = amount
            else:
                self.start_rotate = card.rotate.rotate()

            self.end_rotate = amount

            card.rotate = self

        def rotate(self):

            if self.start_rotate == self.end_rotate:
                return self.start_rotate

            t = (self.table.st - self.start) / self.table.springback
            t = min(t, 1.0)

            if t < 1.0:
                renpy.redraw(self.table, 0)

            return self.start_rotate + (self.end_rotate - self.start_rotate) * t

        def rotate_limit(self):
            return self.end_rotate
