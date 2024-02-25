# This is used for top-level game strucutre.
# Should not include any actual events or scripting; only logic and calling other labels.
#
# NOTE: this is ran when user starts a new game.

# For simplicity, I'm taking the MAS lines from the script.rpy that was made. It's basically the same.
label start:

    # Set the ID of this playthrough
    $ anticheat = persistent.anticheat

    # We'll keep track of the chapter we're on for poem response logic and other stuff
    $ chapter = 0

    #If they quit during a pause, we have to set _dismiss_pause to false again (I hate this hack)
    $ _dismiss_pause = store._mas_root.is_dm_enabled()

    # Each of the girls' names before the MC learns their name throughout ch0.
    $ s_name = "Sayori"
    $ m_name = "Monika"
    $ n_name = "Natsuki"
    $ y_name = "Yuri"

    $ style.say_dialogue = style.normal
    $ quick_menu = True
    #    $ in_sayori_kill = None
    $ allow_skipping = True
    $ config.allow_skipping = True

    #Jump to the space room.
    if persistent.autoload:
        #Stop the title screen music
        stop music
        jump ch30_preloop
    jump ch30_main

label endgame(pause_length=4.0):
    $ quick_menu = False
    stop music fadeout 2.0
    scene black
    show end
    with dissolve_scene_full
    pause pause_length
    $ quick_menu = True
    return
