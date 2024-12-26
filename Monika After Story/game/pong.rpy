# pong difficulty changes on win / loss. Determines monika's paddle-movement-cap, the ball's start-speed, max-speed and acceleration.
default persistent._mas_pong_difficulty = 10
# increases the pong difficulty for the next game by the value this is set to. Resets after a finished match.
default persistent._mas_pong_difficulty_change_next_game = 0
# whether the player answered monika he lets her win on purpose
default persistent._mas_pm_ever_let_monika_win_on_purpose = False
# the day at which the difficulty change was initiated
default persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()

define PONG_DIFFICULTY_CHANGE_ON_WIN            = +1
define PONG_DIFFICULTY_CHANGE_ON_LOSS           = -1
define PONG_DIFFICULTY_POWERUP                  = +5
define PONG_DIFFICULTY_POWERDOWN                = -5
define PONG_PONG_DIFFICULTY_POWERDOWNBIG        = -10

#Triggering the same response twice in a row leads to a different response, not all responses reset this (on purpose)
define PONG_MONIKA_RESPONSE_NONE                                                = 0
define PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES                = 1
define PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES         = 2
define PONG_MONIKA_RESPONSE_WIN_LONG_GAME                                       = 3
define PONG_MONIKA_RESPONSE_WIN_SHORT_GAME                                      = 4
define PONG_MONIKA_RESPONSE_WIN_TRICKSHOT                                       = 5
define PONG_MONIKA_RESPONSE_WIN_EASY_GAME                                       = 6
define PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME                                     = 7
define PONG_MONIKA_RESPONSE_WIN_HARD_GAME                                       = 8
define PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME                                     = 9
define PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME                                    = 10
define PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL                           = 11
define PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT                                      = 12
define PONG_MONIKA_RESPONSE_LOSE_LONG_GAME                                      = 13
define PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME                                     = 14
define PONG_MONIKA_RESPONSE_LOSE_EASY_GAME                                      = 15
define PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME                                    = 16
define PONG_MONIKA_RESPONSE_LOSE_HARD_GAME                                      = 17
define PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME                                    = 18
define PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME                                   = 19

define pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

define played_pong_this_session = False
define mas_pong_taking_break = False
define player_lets_monika_win_on_purpose = False
define instant_loss_streak_counter = 0
define loss_streak_counter = 0
define win_streak_counter = 0
define lose_on_purpose = False
define monika_asks_to_go_easy = False

# Need to be set before every game and be accessible outside the class
define ball_paddle_bounces = 0
define powerup_value_this_game = 0
define instant_loss_streak_counter_before = 0
define loss_streak_counter_before = 0
define win_streak_counter_before = 0
define pong_difficulty_before = 0
define pong_angle_last_shot = 0.0

init:

    image bg pong field = "mod_assets/games/pong/pong_field.png"

    python:
        import random
        import math

        class PongDisplayable(renpy.Displayable):

            def __init__(self):

                renpy.Displayable.__init__(self)

                # Some displayables we use.
                self.paddle = Image("mod_assets/games/pong/pong.png")
                self.ball = Image("mod_assets/games/pong/pong_ball.png")
                self.player = Text(_("[player]"), size=36)
                self.monika = Text(_("Моника"), size=36)
                self.ctb = Text(_("Кликни чтобы начать!"), size=36)

                # Sounds used.
                self.playsounds = True
                self.soundboop = "mod_assets/sounds/pong_sounds/pong_boop.wav"
                self.soundbeep = "mod_assets/sounds/pong_sounds/pong_beep.wav"

                # The sizes of some of the images.
                self.PADDLE_WIDTH = 8
                self.PADDLE_HEIGHT = 79
                self.PADDLE_RADIUS = self.PADDLE_HEIGHT / 2
                self.BALL_WIDTH = 15
                self.BALL_HEIGHT = 15
                self.COURT_TOP = 124
                self.COURT_BOTTOM = 654

                # Other variables
                self.CURRENT_DIFFICULTY = max(persistent._mas_pong_difficulty + persistent._mas_pong_difficulty_change_next_game, 0)

                self.COURT_WIDTH = 1280
                self.COURT_HEIGHT = 720

                self.BALL_LEFT = 80 - self.BALL_WIDTH / 2
                self.BALL_RIGHT = 1199 + self.BALL_WIDTH / 2
                self.BALL_TOP = self.COURT_TOP + self.BALL_HEIGHT / 2
                self.BALL_BOTTOM = self.COURT_BOTTOM - self.BALL_HEIGHT / 2

                self.PADDLE_X_PLAYER = 128                                      #self.COURT_WIDTH * 0.1
                self.PADDLE_X_MONIKA = 1152 - self.PADDLE_WIDTH                 #self.COURT_WIDTH * 0.9 - self.PADDLE_WIDTH

                self.BALL_MAX_SPEED = 2000.0 + self.CURRENT_DIFFICULTY * 100.0

                # The maximum possible reflection angle, achieved when the ball
                # hits the corners of the paddle.
                self.MAX_REFLECT_ANGLE = math.pi / 3
                # A bit redundand, but math.pi / 3 is greater than 1, which is a problem.
                self.MAX_ANGLE = 0.9

                # If the ball is stuck to the paddle.
                self.stuck = True

                # The positions of the two paddles.
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = (self.COURT_BOTTOM - self.COURT_TOP) / 2

                # The computer should aim at somewhere along the paddle, but
                # not always at the centre. This is the offset, measured from
                # the centre.
                self.ctargetoffset = self.get_random_offset()

                # The speed of Monika's paddle.
                self.computerspeed = 150.0 + self.CURRENT_DIFFICULTY * 30.0

                # Get an initial angle for launching the ball.
                init_angle = random.uniform(-self.MAX_REFLECT_ANGLE, self.MAX_REFLECT_ANGLE)

                # The position, dental-position, and the speed of the ball.
                self.bx = self.PADDLE_X_PLAYER + self.PADDLE_WIDTH + 0.1
                self.by = self.playery
                self.bdx = .5 * math.cos(init_angle)
                self.bdy = .5 * math.sin(init_angle)
                self.bspeed = 500.0 + self.CURRENT_DIFFICULTY * 25

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

            def check_bounce_off_top(self):
                # The ball wants to leave the screen upwards.
                if self.by < self.BALL_TOP and self.oldby - self.by != 0:

                    # The x value at which the ball hits the upper wall.
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_TOP) / (self.oldby - self.by))

                    # Ignores the walls outside the field.
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return

                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_TOP

                    # Bounce off by teleporting ball (mirror position on wall).
                    self.by = -self.by + 2 * self.BALL_TOP

                    if not self.stuck:
                        self.bdy = -self.bdy

                    # Ball is so fast it still wants to leave the screen after mirroring, now downwards.
                    # Bounces the ball again (to the other wall) and leaves it there.
                    if self.by > self.BALL_BOTTOM:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_BOTTOM) / (self.bounceby - self.by))
                        self.by = self.BALL_BOTTOM
                        self.bdy = -self.bdy

                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)

                    return True
                return False

            def check_bounce_off_bottom(self):
                # The ball wants to leave the screen downwards.
                if self.by > self.BALL_BOTTOM and self.oldby - self.by != 0:

                    # The x value at which the ball hits the lower wall.
                    collisionbx = self.oldbx + (self.bx - self.oldbx) * ((self.oldby - self.BALL_BOTTOM) / (self.oldby - self.by))

                    # Ignores the walls outside the field.
                    if collisionbx < self.BALL_LEFT or collisionbx > self.BALL_RIGHT:
                        return

                    self.bouncebx = collisionbx
                    self.bounceby = self.BALL_BOTTOM

                    # Bounce off by teleporting ball (mirror position on wall).
                    self.by = -self.by + 2 * self.BALL_BOTTOM

                    if not self.stuck:
                        self.bdy = -self.bdy

                    # Ball is so fast it still wants to leave the screen after mirroring, now downwards.
                    # Bounces the ball again (to the other wall) and leaves it there.
                    if self.by < self.BALL_TOP:
                        self.bx = self.bouncebx + (self.bx - self.bouncebx) * ((self.bounceby - self.BALL_TOP) / (self.bounceby - self.by))
                        self.by = self.BALL_TOP
                        self.bdy = -self.bdy

                    if not self.stuck:
                        if self.playsounds:
                            renpy.sound.play(self.soundbeep, channel=1)

                    return True
                return False

            def getCollisionY(self, hotside, is_computer):
                # Checks whether the ball went through the player's paddle on the x-axis while moving left or monika's paddle while moving right.
                # Returns the y collision-position and sets self.collidedonx

                self.collidedonx = is_computer and self.oldbx <= hotside <= self.bx or not is_computer and self.oldbx >= hotside >= self.bx;

                if self.collidedonx:

                    # Checks whether a bounce happened before potentially colliding with the paddle.
                    if self.oldbx <= self.bouncebx <= hotside <= self.bx or self.oldbx >= self.bouncebx >= hotside >= self.bx:
                        startbx = self.bouncebx
                        startby = self.bounceby
                    else:
                        startbx = self.oldbx
                        startby = self.oldby

                    # The y value at which the ball hits the paddle.
                    if startbx - self.bx != 0:
                        return startby + (self.by - startby) * ((startbx - hotside) / (startbx - self.bx))
                    else:
                        return startby

                # The ball did not go through the paddle on the x-axis.
                else:
                    return self.oldby

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

                # Stores the starting position of the ball.
                self.oldbx = self.bx
                self.oldby = self.by
                self.bouncebx = self.bx
                self.bounceby = self.by

                # Handles the ball-speed.
                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed

                # Bounces the ball up to one time, either up or down
                if not self.check_bounce_off_top():
                   self.check_bounce_off_bottom()

                # Handles Monika's targeting and speed.

                # If the ball goes through Monika's paddle, aim for the collision-y, not ball-y.
                # Avoids Monika overshooting her aim on lags.
                collisionby = self.getCollisionY(self.PADDLE_X_MONIKA, True)
                if self.collidedonx:
                    self.ctargety = collisionby + self.ctargetoffset
                else:
                    self.ctargety = self.by + self.ctargetoffset

                cspeed = self.computerspeed * dtime

                # Moves Monika's paddle. It wants to go to self.by, but
                # may be limited by it's speed limit.
                global lose_on_purpose
                if lose_on_purpose and self.bx >= self.COURT_WIDTH * 0.75:
                    if self.bx <= self.PADDLE_X_MONIKA:
                        if self.ctargety > self.computery:
                            self.computery -= cspeed
                        else:
                            self.computery += cspeed

                else:
                    cspeed = self.computerspeed * dtime

                    if abs(self.ctargety - self.computery) <= cspeed:
                        self.computery = self.ctargety
                    elif self.ctargety >= self.computery:
                        self.computery += cspeed
                    else:
                        self.computery -= cspeed

                # Limits the position of Monika's paddle.
                if self.computery > self.COURT_BOTTOM:
                    self.computery = self.COURT_BOTTOM
                elif self.computery < self.COURT_TOP:
                    self.computery = self.COURT_TOP;

                # This draws a paddle, and checks for bounces.
                def paddle(px, py, hotside, is_computer):

                    # Render the paddle image. We give it an 1280x720 area
                    # to render into, knowing that images will render smaller.
                    # (This isn't the case with all displayables. Solid, Frame,
                    # and Fixed will expand to fill the space allotted.)
                    # We also pass in st and at.
                    pi = renpy.render(self.paddle, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)

                    # renpy.render returns a Render object, which we can
                    # blit to the Render we're making.
                    r.blit(pi, (int(px), int(py - self.PADDLE_RADIUS)))

                    # Checks whether the ball went through the paddle on the x-axis and gets the y-collision-posisiton.
                    collisionby = self.getCollisionY(hotside, is_computer)

                    # Checks whether the ball went through the paddle on the y-axis.
                    collidedony = py - self.PADDLE_RADIUS - self.BALL_HEIGHT / 2 <= collisionby <= py + self.PADDLE_RADIUS + self.BALL_HEIGHT / 2

                    # Checks whether the ball collided with the paddle
                    if not self.stuck and self.collidedonx and collidedony:
                        hit = True
                        if self.oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                        elif self.oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                        else:
                            hit = False

                        if hit:
                            # The reflection angle scales linearly with the
                            # distance from the centre to the point of impact.
                            angle = (self.by - py) / (self.PADDLE_RADIUS + self.BALL_HEIGHT / 2) * self.MAX_REFLECT_ANGLE

                            if angle >    self.MAX_ANGLE:
                                angle =   self.MAX_ANGLE
                            elif angle < -self.MAX_ANGLE:
                                angle =  -self.MAX_ANGLE;

                            global pong_angle_last_shot
                            pong_angle_last_shot = angle;

                            self.bdy = .5 * math.sin(angle)
                            self.bdx = math.copysign(.5 * math.cos(angle), -self.bdx)

                            global ball_paddle_bounces
                            ball_paddle_bounces += 1

                            # Changes where the computer aims after a hit.
                            if is_computer:
                                self.ctargetoffset = self.get_random_offset()

                            if self.playsounds:
                                renpy.sound.play(self.soundboop, channel=1)

                            self.bspeed += 125.0 + self.CURRENT_DIFFICULTY * 12.5
                            if self.bspeed > self.BALL_MAX_SPEED:
                                self.bspeed = self.BALL_MAX_SPEED

                # Draw the two paddles.
                paddle(self.PADDLE_X_PLAYER, self.playery, self.PADDLE_X_PLAYER + self.PADDLE_WIDTH, False)
                paddle(self.PADDLE_X_MONIKA, self.computery, self.PADDLE_X_MONIKA, True)

                # Draw the ball.
                ball = renpy.render(self.ball, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                              int(self.by - self.BALL_HEIGHT / 2)))

                # Show the player names.
                player = renpy.render(self.player, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                r.blit(player, (self.PADDLE_X_PLAYER, 25))

                # Show Monika's name.
                monika = renpy.render(self.monika, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                ew, eh = monika.get_size()
                r.blit(monika, (self.PADDLE_X_MONIKA - ew, 25))

                # Show the "Click to Begin" label.
                if self.stuck:
                    ctb = renpy.render(self.ctb, self.COURT_WIDTH, self.COURT_HEIGHT, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, ((self.COURT_WIDTH - cw) / 2, 30))


                # Check for a winner.
                if self.bx < -200:

                    if self.winner == None:
                        global loss_streak_counter
                        loss_streak_counter += 1

                        if ball_paddle_bounces <= 1:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter += 1
                        else:
                            global instant_loss_streak_counter
                            instant_loss_streak_counter = 0

                    global win_streak_counter
                    win_streak_counter = 0;

                    self.winner = "monika"

                    # Needed to ensure that event is called, noticing
                    # the winner.
                    renpy.timeout(0)

                elif self.bx > self.COURT_WIDTH + 200:

                    if self.winner == None:
                        global win_streak_counter
                        win_streak_counter += 1;

                    global loss_streak_counter
                    loss_streak_counter = 0

                    #won't reset if Monika misses the first hit
                    if ball_paddle_bounces > 1:
                        global instant_loss_streak_counter
                        instant_loss_streak_counter = 0

                    self.winner = "player"

                    renpy.timeout(0)

                # Ask that we be re-rendered ASAP, so we can show the next
                # frame.
                renpy.redraw(self, 0.0)

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

    if played_pong_this_session:
        if mas_pong_taking_break:
            m 1eua "Готов сыграть снова?"
            m 2tfb "Покажи на что способен, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"

            #Reset this flag
            $ mas_pong_taking_break = False
        else:
            m 1hua "Ты хочешь сыграть снова?"
            m 3eub "Я готова когда ты готов~"
    else:
        $ played_pong_this_session = True

    $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_NONE

    call demo_minigame_pong from _call_demo_minigame_pong
    return

label demo_minigame_pong:

    window hide None

    # Put up the pong background, in the usual fashion.
    scene bg pong field

    # natsuki scare setup if appropriate
    if store.mas_egg_manager.natsuki_enabled():
        $ playing_okayev = store.songs.getPlayingMusicName() == "Okay, Everyone! (Monika)"

        # we'll take advantage of Okay everyone's sync with natsuki's version
        if playing_okayev:
            $ currentpos = get_pos(channel="music")
            $ adjusted_t5 = "<from " + str(currentpos) + " loop 4.444>bgm/5_natsuki.ogg"
            stop music fadeout 2.0
            $ renpy.music.play(adjusted_t5, fadein=2.0, tight=True)

    $ ball_paddle_bounces = 0
    $ pong_difficulty_before = persistent._mas_pong_difficulty
    $ powerup_value_this_game = persistent._mas_pong_difficulty_change_next_game
    $ loss_streak_counter_before = loss_streak_counter
    $ win_streak_counter_before = win_streak_counter
    $ instant_loss_streak_counter_before = instant_loss_streak_counter

    # Run the pong minigame, and determine the winner.
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)

    # natsuki scare if appropriate
    if store.mas_egg_manager.natsuki_enabled():
        call natsuki_name_scare(playing_okayev=playing_okayev) from _call_natsuki_name_scare

    #Regenerate the spaceroom scene
    call spaceroom(scene_change=True, force_exp='monika 3eua')

    # resets the temporary difficulty bonus
    $ persistent._mas_pong_difficulty_change_next_game = 0;

    if winner == "monika":
        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_LOSS

        $ inst_dialogue = store.mas_pong.DLG_WINNER

    else:
        $ new_difficulty = persistent._mas_pong_difficulty + PONG_DIFFICULTY_CHANGE_ON_WIN

        $ inst_dialogue = store.mas_pong.DLG_LOSER

        #Give player XP if this is their first win
        if not persistent._mas_ever_won['pong']:
            $persistent._mas_ever_won['pong'] = True

    if new_difficulty < 0:
        $ persistent._mas_pong_difficulty = 0
    else:
        $ persistent._mas_pong_difficulty = new_difficulty;

    call expression inst_dialogue from _mas_pong_inst_dialogue

    $ mas_gainAffection(modifier=0.5)

    m 3eua "Хочешь сыграть снова?{nw}"
    $ _history_list.pop()
    menu:
        m "Хочешь сыграть снова?{fast}"

        "Да.":
            $ pong_ev = mas_getEV("mas_pong")
            if pong_ev:
                # each game counts as a game played
                $ pong_ev.shown_count += 1

            jump demo_minigame_pong

        "Нет.":
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

#START: Dialogue shown when Monika wins
label mas_pong_dlg_winner:
    #Dlg based on difficulty
    #NOTE: Order is very important here.
    #TODO: Dlg based on affection


    #Player lets Monika win after being asked to go easy on her without hitting the ball
    if monika_asks_to_go_easy and ball_paddle_bounces == 1:
        m 1rksdlb "А-ха-ха..."
        m 1hksdla "Я знаю что я просила тебя быть полегче со мной, но это не то что я имела ввиду..."
        m 3eka "Но я признательна этому жесту~"
        $ monika_asks_to_go_easy = False

    #Player lets Monika win after being asked to go easy on her without hitting the ball too much
    elif monika_asks_to_go_easy and ball_paddle_bounces <= 9:
        m 1hub "Ура, я победила!"
        show monika 5ekbfa at t11 zorder MAS_MONIKA_Z with dissolve_monika
        m 5ekbfa "Спасибо, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]. Это было весело~"
        $ monika_asks_to_go_easy = False


    #The player fails to hit the first ball
    elif ball_paddle_bounces == 1:

        #Once
        if instant_loss_streak_counter == 1:
            m 2rksdlb "А-ха-ха, не повезло..."

        #Twice
        elif instant_loss_streak_counter == 2:
            m 2rksdlc "[player],{w=0.1} ты снова пропустил мяч..."

        #Thrice
        elif instant_loss_streak_counter == 3:
            m 2tfd "[player]!"

            if persistent._mas_pm_ever_let_monika_win_on_purpose:
                $ menu_response = _("Ты снова специально позволяешь выиграть мне?")
            else:
                $ menu_response = _("Ты мпециально позволяешь выиграть мне?")

            m 2rkc "[menu_response]"
            $ _history_list.pop()
            menu:
                m "[menu_response]{fast}"

                "...Возможно.":
                    m 1hua "Е-хе-хе!~"
                    m 1eka "Спасибо тебе, [player]~"
                    show monika 5eka at t11 zorder MAS_MONIKA_Z with dissolve_monika
                    m 5eka "Но знаешь,{w=0.1} я не против иногда проигрывать тебе."

                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        m 5eua "Я хочу видеть то как ты выигрываешь так же как и ты хочешь видеть как выигрываю я~"

                    $ player_lets_monika_win_on_purpose = True
                    $ persistent._mas_pm_ever_let_monika_win_on_purpose = True

                "Нет.":
                    if persistent._mas_pm_ever_let_monika_win_on_purpose:
                        show monika 1ttu
                        m "Ты {i}уверен?{/i}{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Ты {i}уверен?{/i}{fast}"

                            "Да":
                                call mas_pong_dlg_sorry_assuming

                            "Нет":
                                m 1rfu "[player]!"
                                m 2hksdlb "Не шути так!"
                                $ player_lets_monika_win_on_purpose = True
                                $ lose_on_purpose = True

                    else:
                        call mas_pong_dlg_sorry_assuming

        #Any more times
        else:
            if player_lets_monika_win_on_purpose:
                m 2tku "Ты ещё не устал позволять мне выиграть, [player]?"
            else:
                m 1rsc "..."

                #Just so we don't get this every time, feels a little more genuine
                if random.randint(1,3) == 1:
                    m 1eka "Да ладно, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"
                    m 1hub "Ты можешь сделать это, я верю в тебя!"

    #Monika wins a game after the player let her win on purpose at least three times
    elif instant_loss_streak_counter_before >= 3 and player_lets_monika_win_on_purpose:
        m 3hub "Отличная попытка [player],{w=0.1} {nw}"
        extend 3tsu "Но я и сама могу победить!"
        m 3hub "А-ха-ха!"

    #Monika wins after telling the player she would win the next game
    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 1hua "Е-хе-хе~"

        if persistent._mas_pong_difficulty_change_next_game_date == datetime.date.today():
            m 2tsb "Разве я тебе не говорила, что я выиграю в этот раз?"
        else:
            $ p_nickname = mas_get_player_nickname(regex_replace_with_nullstr='my ')
            m 2ttu "Запомни, [p_nickname]?{w=0.1} {nw}"
            extend 2tfb "Я пообещала выиграть в следующий раз."

    #Monika wins after going easy on the player
    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1rksdla "Ах..."
        m 3hksdlb "Поробуй снова, [player]!"

        $ persistent._mas_pong_difficulty_change_next_game = PONG_PONG_DIFFICULTY_POWERDOWNBIG

    #Monika wins after going even easier on the player
    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 2rksdlb "А-ха-ха..."
        m 2eksdla "Я правда надеялась что ты выиграешь в этот раз."
        m 2hksdlb "Прости, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"

    #The player has lost 3, 8, 13, ... matches in a row.
    elif loss_streak_counter >= 3 and loss_streak_counter % 5 == 3:
        m 2eka "Да ладно, [player], я знаю что ты можешь обыграть меня..."
        m 3hub "Продолжай стараться!"

    #The player has lost 5, 10, 15, ... matches in a row.
    elif loss_streak_counter >= 5 and loss_streak_counter % 5 == 0:
        m 1eua "Я надеюсь ты веселишься, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]."
        m 1eka "Я бы не хотела чтобы ты злился из-за игры."
        m 1hua "Мы всегда можнм взять перерыв и сыграть позже, если ты хочешь."

    #Monika wins after the player got a 3+ winstreak
    elif win_streak_counter_before >= 3:
        $ p_nickname = mas_get_player_nickname(regex_replace_with_nullstr='my ')
        m 1hub "А-ха-ха!"
        m 2tfu "Прости [p_nickname],{w=0.1} {nw}"
        extend 2tub "но похоже твоя удача иссякла."
        m 2hub "Теперь это моё время блестать~"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES

    #Monika wins a second time after the player got a 3+ winstreak
    elif pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES:
        m 1hua "Е-хе-хе!"
        m 1tub "Продолжай, [player]!{w=0.3} {nw}"
        extend 2tfu "Похоже что твоя очеред побед окончена!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_SECOND_WIN_AFTER_PLAYER_WON_MIN_THREE_TIMES

    #Monika wins a long game
    elif ball_paddle_bounces > 9 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_LONG_GAME:
            m 3eub "Играть против тебя очень сложно, [player]."
            m 1hub "Продолжай в том же духе и ты победишь, я уверена!"
        else:
            m 3hub "Хорошо сыграно, [player], ты очень хорош!"
            m 1tfu "Но я тоже не промах,{w=0.1} {nw}"
            extend 1hub "а-ха-ха!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_LONG_GAME

    #Monika wins a short game
    elif ball_paddle_bounces <= 3:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_SHORT_GAME:
            m 3hub "Ещё одна быстрый раунд в мою пользу~"
        else:
            m 4huu "Е-хе-хе,{w=0.1} {nw}"
            extend 4hub "я обыграла тебя в этот раз!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_SHORT_GAME

    #Monika wins by a trickshot
    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_TRICKSHOT:
            m 2eksdld "Ах...{w=0.3}{nw}"
            extend 2rksdlc "это снова случилось."
            m 1hksdlb "Извини, [player]!"
        else:
            m 2rksdlb "Прости, [player]!"
            m 3hksdlb "Я не хотела чтобы он отскакивал так много..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_TRICKSHOT

    #Monika wins a game
    else:
        #Easy
        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EASY_GAME:
                m 1eub "Ты можешь сделать это, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"
                m 3hub "Я верю в тебя~"
            else:
                m 2duu "Соберись, [player]."
                m 3hub "Продолжай стараться, я уверена ты скоро победишь!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EASY_GAME

        #Medium
        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME:
                m 1hub "Я выиграла очередной раунд~"
            else:
                if loss_streak_counter > 1:
                    m 3hub "Похоже я выиграла~"
                else:
                    m 3hua "Позоже я снова выиграла~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_MEDIUM_GAME

        #Hard
        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_HARD_GAME:
                m 1hub "А-ха-ха!"
                m 2tsb "Я играю слишком хорошо для тебя?"
                m 1tsu "Я шучу, [player]."
                m 3hub "Ты очень даже неплох!"
            else:
                if loss_streak_counter > 1:
                    m 1hub "Я снова выиграла~"
                else:
                    m 1huu "Я выиграла~"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_HARD_GAME

        #Expert
        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME:
                m 2tub "Выигрывать так приятно!"
                m 2hub "Не волнуйся, я уверены ты скоро тоже одолеешь меня~"
            else:
                if loss_streak_counter > 1:
                    m 2eub "Я победила в очередном раунде!"
                else:
                    m 2eub "Я победила в этом раунде!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXPERT_GAME

        #Extreme
        else:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME:
                m 2duu "Не плохо, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]."
                m 4eua "Я выложилась по полной, так что не терзай себя за то что ты проиграл мне."
            else:
                m 2hub "В этот раз победа моя!"
                m 2efu "Продолжай в том же духе, [player]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_WIN_EXTREME_GAME

    return

#dlg for Monika saying she's sorry for assuming
#Duplicated, hence label
label mas_pong_dlg_sorry_assuming:
    m 3eka "Хорошо."
    m 2ekc "Извини за предположение..."

    #This is only used in bits where the player lets Monika win on purpose
    $ player_lets_monika_win_on_purpose = False

    m 3eka "Может отдохнём немного, [player]?{nw}"
    $ _history_list.pop()
    menu:
        m "Может отдохнём немного, [player]?{fast}"

        "Хорошо.":
            m 1eka "Хорошо, [player].{w=0.3} {nw}"
            extend 1hua "Я хорошо провела время, спасибо что сыграл в Понг со мной!"
            m 1eua "Скажи когда ты будешь готов сыграть снова."

            #Set this var so Monika knows you're ready to play again
            $ mas_pong_taking_break = True

            #Dissolve into idle poses
            show monika idle with dissolve_monika
            jump ch30_loop

        "Нет.":
            m 1eka "Хорошо, [player]. Если ты так уверен."
            m 1hub "Продолжай, ведь ты скоро сможешь победить меня!"
    return

#START: Dialogue shown right when monika loses
label mas_pong_dlg_loser:
    # adapts the dialog, depending on the difficulty, game length (bounces), games losses, wins and dialog response.
    # the order of the dialog is crucial, the first matching condition is chosen, other possible dialog is cancelled in the process.
    # todo: adapt dialog to affection
    # todo: add randomized dialog

    $ monika_asks_to_go_easy = False

    #Monika loses on purpose
    if lose_on_purpose:
        m 1hub "А-ха-ха!"
        m 1kua "Теперь мы квиты, [player]!"
        $ lose_on_purpose = False

    #Monika loses without hitting the ball
    elif ball_paddle_bounces == 0:
        m 1rksdlb "А-ха-ха..."

        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL:
            m "Может мне стоит постараться чуть сильнее..."
        else:
            m "Кажется мне не хватает немного скорости..."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_WITHOUT_HITTING_BALL

    #Player starts playing seriously and wins after losing at least 3 times on purpose
    elif instant_loss_streak_counter_before >= 3 and persistent._mas_pm_ever_let_monika_win_on_purpose:
        m 2tsu "Теперь играем серьёзно, ведь так?~"
        m 2tfu "Давай проверим, насколько ты хорош, [player]!"

    #Player wins after losing at least three times in a row
    elif loss_streak_counter_before >= 3:
        m 4eub "Поздравляю, [player]!{w=0.3} {nw}"
        extend 2hub "Я знала что ты выиграешь после достаточной практики!"
        m 4eua "Помни, если долго тренируешься, то достич можно чего угодно!"

    #Monika loses after saying she would win this time
    elif powerup_value_this_game == PONG_DIFFICULTY_POWERUP:
        m 2wuo "Вау...{w=0.3}{nw}"
        extend 7wuo "Я правда старалась в этот раз!"
        m 3hub "Так держать, [player]!"

    #Monika loses after going easy on the player
    elif powerup_value_this_game == PONG_DIFFICULTY_POWERDOWN:
        m 1hua "Е-хе-хе!"
        m 2hub "Хорошая работа, [player]!"

    #Monika loses after going even easier on the player
    elif powerup_value_this_game == PONG_PONG_DIFFICULTY_POWERDOWNBIG:
        m 1hua "Я рада что ты выиграл в этот раз, [player]."

    #Monika loses by a trickshot
    elif pong_angle_last_shot >= 0.9 or pong_angle_last_shot <= -0.9:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT:
            m 2wuo "[player]!"
            m 2hksdlb "У меня не было шансов отбить этот удар!"
        else:
            m 2wuo "Вау, это был крутой удар!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_TRICKSHOT

    #Monika loses three times in a row
    elif win_streak_counter == 3:
        m 2wuo "Вау, [player]..."
        m 2wud "Ты уже выиграл три раза продряд..."

        #Easy
        if pong_difficulty_before <= 5:
            m 2tsu "Может в этот раз я должна постаряться получше~"

        #Medium
        elif pong_difficulty_before <= 10:
            m 4hua "Ты очень хорош!"

        #Hard
        elif pong_difficulty_before <= 15:
            m 3hub "Хорошо сыграно!"

        #Expert
        elif pong_difficulty_before <= 20:
            m 4wuo "Это было круто!"

        #Extreme
        else:
            m 2hub "Это было легендарно!"  # translator note: i have no idea how to translate "legendary" in this context

    #Monika loses five times in a row
    elif win_streak_counter == 5:
        m 2wud "[mas_get_player_nickname(capitalize=True, regex_replace_with_nullstr='my ')]..."
        m 2tsu "Неужели ты практиковался?"
        m 3hksdlb "Не знаю что прозошло, но у меня нет шансов против тебя!"
        m 1eka "Можешь пожалуйста немножечко поддаваться?{w=0.3} {nw}"
        extend 3hub "Я буду очень благодарна~"
        $ monika_asks_to_go_easy = True

    #Monika loses a long game
    elif ball_paddle_bounces > 10 and ball_paddle_bounces > pong_difficulty_before * 0.5:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_LONG_GAME:
            m 2wuo "Вау,{w=0.1} я не могу обыграть тебя!"
        else:
            m 2hub "Потрясающе, [player]!"
            m 4eub "Ты очень хорош!"

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_LONG_GAME

    #Monika loses a short game
    elif ball_paddle_bounces <= 2:
        if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME:
            m 2hksdlb "А-ха-ха..."
            m 3eksdla "Я думаю мне стоит попытаться чуть усерднее..."
        else:
            m 1rusdlb "Я не ожидала проиграть так быстро."

        $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_SHORT_GAME

    #Monika loses a game
    else:
        #Easy difficulty
        if pong_difficulty_before <= 5:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EASY_GAME:
                m 4eub "Ты выиграл этот раунд."
            else:
                if win_streak_counter > 1:
                    m 1hub "Ты снова выиграл!"
                else:
                    m 1hua "Ты выиграл!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EASY_GAME

        #Medium
        elif pong_difficulty_before <= 10:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME:
                m 1eua "Это приятно видеть как ты выигрываешь, [player]."
                m 1hub "Продолжай в том же духе~"
            else:
                if win_streak_counter > 1:
                    m 1hub "Ты снова выиграл! {w=0.2}Хорошая работа~"
                else:
                    m 1eua "Ты выиграл! {w=0.2}Неплохо."

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_MEDIUM_GAME

        #Hard
        elif pong_difficulty_before <= 15:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_HARD_GAME:
                m 4hub "Очередная победа за тобой!"
                m 4eua "Хорошая работа, [player]."
            else:
                if win_streak_counter > 1:
                    m 2hub "Ты снова выиграл! {w=0.2}Поздравляю!"
                else:
                    m 2hua "Ты выиграл! {w=0.2}Поздравляю!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_HARD_GAME

        #Expert
        elif pong_difficulty_before <= 20:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME:
                m 2wuo "Вау,{w=0.1} я правда пытаюсь...{w=0.3} ты неостановим!"
                m 2tfu "Но я увреена что рано или поздно выиграю, [player]."
                m 3hub "А-ха-ха!"
            else:
                if win_streak_counter > 1:
                    m 4hub "Ты снова выиграл! {w=0.2}Отличная работа!"
                else:
                    m 4hub "Ты выиграл! {w=0.2}Поразительно!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXPERT_GAME

        #Extreme
        else:
            if pong_monika_last_response_id == PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME:
                m 3eua "Ты очень хорош, [player]."
                m 1hub "Я люблю играть Понг с тобой!"
            else:
                m 1tsu "Это было сложно!"
                m 1hub "Продолжай в том же духе, [mas_get_player_nickname(regex_replace_with_nullstr='my ')]!"

            $ pong_monika_last_response_id = PONG_MONIKA_RESPONSE_LOSE_EXTREME_GAME
    return


#Quick Moni lose dlg
label mas_pong_dlg_loser_fast:
    m 1eka "Хорошо, [player]."
    m 3tfu "Но я выиграю в следующий раз."

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERUP;
    $ persistent._mas_pong_difficulty_change_next_game_date = datetime.date.today()
    return

#Quick Moni win dlg
label mas_pong_dlg_winner_fast:
    m 1eka "Хорошо, [player]. Спасибо что сыграл в понг со мной."
    m 1hua "Мне было очень весело! Давай сыграем потом ещё, хорошо?"

    $ persistent._mas_pong_difficulty_change_next_game = PONG_DIFFICULTY_POWERDOWN;
    return

#Post dlg Moni lose
label mas_pong_dlg_loser_end:
    m 1wuo "Вау, я очень старалась в этот раз."
    m 1eua "Ты видимо много практиковался чтобы играть настолько хорошо."
    m 2tuu "Мне кажется ты пытался впечатлить меня, [player]."
    m 1hua "Ты такой милый~"
    return

#Post dlg Moni win
label mas_pong_dlg_winner_end:
    m 4tku "Я не могу радоваться игре, которая была настолько проста..."
    m 1eua "Но мне всё ещё было весело играть."
    m 1ekbsa "Особенно с тобой, [player]."
    m 1hubfa "Е-хе-хе~"
    return
