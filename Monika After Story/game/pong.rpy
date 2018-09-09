init:

    image bg pong field = "mod_assets/pong_field.png"

    python:
        import random
        import math

        class PongDisplayable(renpy.Displayable):

            def __init__(self):

                renpy.Displayable.__init__(self)

                # Some displayables we use.
                self.paddle = Image("mod_assets/pong.png")
                self.ball = Image("mod_assets/pong_ball.png")
                self.player = Text(_("[player]"), size=36)
                self.monika = Text(_("[m_name]"), size=36)
                self.ctb = Text(_("Click to Begin"), size=36)

                # The sizes of some of the images.
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.PADDLE_RADIUS = self.PADDLE_HEIGHT / 2
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 124
                self.COURT_BOTTOM = 654

                # The maximum possible reflection angle, achieved when the ball
                # hits the corners of the paddle.
                self.MAX_REFLECT_ANGLE = math.pi / 3

                # If the ball is stuck to the paddle.
                self.stuck = True

                # The positions of the two paddles.
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = self.playery

                # The computer should aim at somewhere along the paddle, but
                # not always at the centre. This is the offset, measured from
                # the centre.
                self.ctargetoffset = self.get_random_offset()

                # The speed of the computer.
                # I changed this to triple. Get ready for the dark souls of pong
                self.computerspeed = 1000.0

                # Get an initial angle for launching the ball.
                init_angle = random.uniform(-self.MAX_REFLECT_ANGLE, self.MAX_REFLECT_ANGLE)
                # The position, dental-position, and the speed of the
                # ball.
                self.bx = 110
                self.by = self.playery
                self.bdx = .5 * math.cos(init_angle)
                self.bdy = .5 * math.sin(init_angle)
                self.bspeed = 500.0

                # Where the computer wants to go.
                self.ctargety = self.by + self.ctargetoffset

                # The time of the past render-frame.
                self.oldst = None

                # The winner.
                self.winner = None

            def get_random_offset(self):
                return random.uniform(-self.PADDLE_RADIUS, self.PADDLE_RADIUS)

            def visit(self):
                return [ self.paddle, self.ball, self.player, self.monika, self.ctb ]

            # Recomputes the position of the ball, handles bounces, and
            # draws the screen.
            def render(self, width, height, st, at):

                # The Render object we'll be drawing into.
                r = renpy.Render(width, height)

                # Figure out the time elapsed since the previous frame.
                if self.oldst is None:
                    self.oldst = st

                dtime = st - self.oldst
                self.oldst = st

                # Figure out where we want to move the ball to.
                speed = dtime * self.bspeed
                oldbx = self.bx

                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed
                self.ctargety = self.by + self.ctargetoffset

                # Move the computer's paddle. It wants to go to self.by, but
                # may be limited by it's speed limit.
                cspeed = self.computerspeed * dtime
                if abs(self.ctargety - self.computery) <= cspeed:
                    self.computery = self.ctargety
                elif self.ctargety - self.computery >= 0:
                    self.computery += cspeed
                else:
                    self.computery -= cspeed

                # Handle bounces.

                # Bounce off of top.
                ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
                if self.by < ball_top:
                    self.by = ball_top + (ball_top - self.by)
                    self.bdy = -self.bdy
                    if not self.stuck:
                        renpy.sound.play("mod_assets/pong_beep.wav", channel=0)

                # Bounce off bottom.
                ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                if self.by > ball_bot:
                    self.by = ball_bot - (self.by - ball_bot)
                    self.bdy = -self.bdy
                    if not self.stuck:
                        renpy.sound.play("mod_assets/pong_beep.wav", channel=0)

                # This draws a paddle, and checks for bounces.
                def paddle(px, py, hotside, is_computer):

                    # Render the paddle image. We give it an 1280x720 area
                    # to render into, knowing that images will render smaller.
                    # (This isn't the case with all displayables. Solid, Frame,
                    # and Fixed will expand to fill the space allotted.)
                    # We also pass in st and at.
                    pi = renpy.render(self.paddle, 1280, 720, st, at)

                    # renpy.render returns a Render object, which we can
                    # blit to the Render we're making.
                    r.blit(pi, (int(px), int(py - self.PADDLE_RADIUS)))

                    if py - self.PADDLE_RADIUS <= self.by <= py + self.PADDLE_RADIUS:
                        hit = True
                        if oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                        elif oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                        else:
                            hit = False

                        if hit:
                            # The reflection angle scales linearly with the
                            # distance from the centre to the point of impact.
                            angle = (self.by - py) / self.PADDLE_RADIUS * self.MAX_REFLECT_ANGLE
                            self.bdy = .5 * math.sin(angle)
                            self.bdx = math.copysign(.5 * math.cos(angle), -self.bdx)

                            # Changes where the computer aims after a hit.
                            if is_computer:
                                self.ctargetoffset = self.get_random_offset()

                            renpy.sound.play("mod_assets/pong_boop.wav", channel=1)
                            self.bspeed *= 1.20

                # Draw the two paddles.
                paddle(100, self.playery, 100 + self.PADDLE_WIDTH, False)
                paddle(1175, self.computery, 1175, True)

                # Draw the ball.
                ball = renpy.render(self.ball, 1280, 720, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))

                # Show the player names.
                player = renpy.render(self.player, 1280, 720, st, at)
                r.blit(player, (100, 25))

                # Show Monika's name.
                monika = renpy.render(self.monika, 1280, 720, st, at)
                ew, eh = monika.get_size()
                r.blit(monika, (1150 - ew, 25))

                # Show the "Click to Begin" label.
                if self.stuck:
                    ctb = renpy.render(self.ctb, 1280, 720, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, (640 - cw / 2, 30))


                # Check for a winner.
                if self.bx < -200:
                    self.winner = "monika"

                    # Needed to ensure that event is called, noticing
                    # the winner.
                    renpy.timeout(0)

                elif self.bx > 1280:
                    self.winner = "player"
                    renpy.timeout(0)

                # Ask that we be re-rendered ASAP, so we can show the next
                # frame.
                renpy.redraw(self, 0)

                # Return the Render object.
                return r

            # Handles events.
            def event(self, ev, x, y, st):

                import pygame

                # Mousebutton down == start the game by setting stuck to
                # false.
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False

                # Set the position of the player's paddle.
                y = max(y, self.COURT_TOP)
                y = min(y, self.COURT_BOTTOM)
                self.playery = y

                # If we have a winner, return him or her. Otherwise, ignore
                # the current event.
                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()


label game_pong:
    hide screen keylistener
    m 1eua "You wanna play a game of Pong? Okay!"
#    m 1b "I'll beat you for sure this time!" # this line is useless #Why's the line here then blyat
    call demo_minigame_pong from _call_demo_minigame_pong
    return

label demo_minigame_pong:

    window hide None

    # Put up the pong background, in the usual fashion.
    scene bg pong field

    # natsuki scare setup if appropriate
    if persistent.playername.lower() == "natsuki":
        $ playing_okayev = store.songs.getPlayingMusicName() == "Okay, Everyone! (Monika)"

        # we'll take advantage of Okay everyone's sync with natsuki's version
        if playing_okayev:
            $ currentpos = get_pos(channel="music")
            $ adjusted_t5 = "<from " + str(currentpos) + " loop 4.444>bgm/5_natsuki.ogg"
            stop music fadeout 2.0
            $ renpy.music.play(adjusted_t5, fadein=2.0, tight=True)

    # Run the pong minigame, and determine the winner.
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)

    # natsuki scare if appropriate
    if persistent.playername.lower() == "natsuki":
        call natsuki_name_scare(playing_okayev=playing_okayev) from _call_natsuki_name_scare

    #Regenerate the spaceroom scene
    $scene_change=True #Force scene generation
    call spaceroom from _call_spaceroom_3

    if winner == "monika":
        $ inst_dialogue = store.mas_pong.DLG_WINNER

    else:
        #Give player XP if this is their first win
        if not persistent.ever_won['pong']:
            $persistent.ever_won['pong'] = True
            $grant_xp(xp.WIN_GAME)

        $ inst_dialogue = store.mas_pong.DLG_LOSER

    call expression inst_dialogue from _mas_pong_inst_dialogue

    $ mas_gainAffection(modifier=0.5)

    menu:
        m "Do you want to play again?"

        "Yes.":
            jump demo_minigame_pong
        "No.":

            if winner == "monika":
                if renpy.seen_label(store.mas_pong.DLG_WINNER_END):
                    $ end_dialogue = store.mas_pong.DLG_WINNER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_WINNER_END

            else:
                if renpy.seen_label(store.mas_pong.DLG_LOSER_END):
                    $ end_dialogue = store.mas_pong.DLG_LOSER_FAST
                else:
                    $ end_dialogue = store.mas_pong.DLG_LOSER_END

            call expression end_dialogue from _mas_pong_end_dialogue

    return

## pong text dialogue adjustments

# store to hold pong related constants
init -1 python in mas_pong:

    DLG_WINNER = "mas_pong_dlg_winner"
    DLG_WINNER_FAST = "mas_pong_dlg_winner_fast"
    DLG_LOSER = "mas_pong_dlg_loser"
    DLG_LOSER_FAST = "mas_pong_dlg_loser_fast"

    DLG_WINNER_END = "mas_pong_dlg_winner_end"
    DLG_LOSER_END = "mas_pong_dlg_loser_end"

    # tuple of all dialogue block labels
    DLG_BLOCKS = (
        DLG_WINNER,
        DLG_WINNER_FAST,
        DLG_WINNER_END,
        DLG_LOSER,
        DLG_LOSER_FAST,
        DLG_LOSER_END
    )

# dialogue shown right when monika wins
label mas_pong_dlg_winner:
    m 1hua "I win~!"
    return

# end dialogue shown when monika is the pong winner
label mas_pong_dlg_winner_end:
    m 4tku "I can't really get excited for a game this simple..."
    m 1eua "At least we can still hang out with each other."
    m 1hub "Ahaha!"
    m 1eua "Thanks for letting me win, [player]."
    m 1tku "Only elementary schoolers seriously lose at Pong, right?"
    m 1hua "Ehehe~"
    return

# quick dialogue shown when monika is the pong winner
label mas_pong_dlg_winner_fast:
    # there is nothing here on purpose
    return

# dialogtue shown right when monika loses
label mas_pong_dlg_loser:
    m 1hub "You won! Congratulations."
    return

# end dialogue shown when monka is the pong loser
label mas_pong_dlg_loser_end:
    m 1wuo "Wow, I was actually trying that time."
    m 1eua "You must have really practiced at Pong to get so good."
    m 1tku "Is that something for you to be proud of?"
    m 1hua "I guess you wanted to impress me, [player]~"
    return

# quick dialogue shown when monika is the pong loser
label mas_pong_dlg_loser_fast:
    m 1tfu "I'll beat you next time, [player]."
    return
