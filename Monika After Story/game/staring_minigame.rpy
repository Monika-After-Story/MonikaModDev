"""
TODOs in no particular order:
    put this in the game menu
    unlock condition - the staring topic
    stalemate - when the screen is clicked short time (eg 0.2s) before moni loses
    glitch path - monika gets frustrated after losing a few times and tries to spook the player
    fix monika's position in staring_loop
    add dialogue
        how to lose
        randomized quips on win/loss
"""

screen staring_loop(sprcode,dur):
    """
    Shows Monika with a non-blinking expression for a given period.
    Interrupted by clicking.
    
    IN:
        sprcode - expression sprite code
        dur - duration for which the expression is shown

    OUT:
        string
            "keep_going" if time runs out
            "player_loss" if screen is clicked before timeout
    """
    timer dur action Return("keep_going")
    imagemap:
        # moni keeps getting shoved into the corner and idk how to fix that
        ground "monika "+ sprcode +"_static"
        hotspot (640,360,1280,720) action Return("player_loss") # should cover the whole screen - check this

label game_staring:

    m "You'd like to have a staring contest with me?"
    m "Alright, but you better be prepared to lose, ahaha~"

    # prevent interactions
    $ mas_RaiseShield_core()
    $ mas_OVLHide()
    $ disable_esc()

    $ staring_keep_going = True
    $ staring_step = 0          # monika's strain level
    $ exp_list = ["2tua","2eua","2esa","2euc","2efa","2efsdlc","2ffsdlc"]     # increasingly strained expressions
    hide monika with dissolve_monika

    while staring_keep_going:
        # main loop - goes through the 7 expressions in random length timesteps
        # total duration between 21 and 63 seconds
        call screen staring_loop(exp_list[staring_step],random.randint(3,9))

        if (_return == "keep_going"):
            if staring_step < 6:
                # go to next step
                $ staring_step += 1
            else:
                # monika's loss
                $ staring_keep_going = False
                $ monika_win = False

        else:
            # player's loss
            $ staring_keep_going = False
            $ monika_win = True

    # drop shields
    $ mas_DropShield_core()
    $ mas_OVLShow()
    $ enable_esc()

    if monika_win:
        show monika 2tub at i11 zorder MAS_MONIKA_Z
        m "Told you so.{w=0.3}{nw}"
        extend 2hua" Ahaha~"
    else:
        show monika 2hfsdld at i11 zorder MAS_MONIKA_Z
        m "Bleh."

return
