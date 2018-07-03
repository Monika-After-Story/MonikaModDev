# This is used for top-level game strucutre.
# Should not include any actual events or scripting; only logic and calling other labels.

label start:

    # Set the ID of this playthrough
    $ anticheat = persistent.anticheat

    # We'll keep track of the chapter we're on for poem response logic and other stuff
    $ chapter = 0

    #If they quit during a pause, we have to set _dismiss_pause to false again (I hate this hack)
    $ _dismiss_pause = config.developer

    # Each of the girls' names before the MC learns their name throughout ch0.
    $ s_name = "Sayori"
    $ m_name = "Monika"
    $ n_name = "Natsuki"
    $ y_name = "Yuri"

    $ quick_menu = True
    $ style.say_dialogue = style.normal
    #    $ in_sayori_kill = None
    $ allow_skipping = True
    $ config.allow_skipping = True
    
    if persistent.playthrough == 0:
        # Intro
        $ chapter = 0
        call ch0_main

        # Poem minigame 1
        call poem

        # Day 1
        $ chapter = 1
        call ch1_main
        call poemresponse_start
        call ch1_end

        # Poem minigame 2
        call poem

        # Day 2
        $ chapter = 2
        call ch2_main
        call poemresponse_start
        call ch2_end

        # Poem minigame 3
        call poem

        # Day 3
        $ chapter = 3
        call ch3_main
        call poemresponse_start
        call ch3_end

        $ chapter = 4
        call ch4_main

        python:
            try: renpy.file(config.basedir + "/hxppy thxughts.png")
            except: open(config.basedir + "/hxppy thxughts.png", "wb").write(renpy.file("hxppy thxughts.png").read())
        $ chapter = 5
        call ch5_main

        call endgame

        return

    elif persistent.playthrough == 1:
        $ chapter = 0
        call ch10_main
        jump playthrough2


    elif persistent.playthrough == 2:
        # Intro
        $ chapter = 0
        call ch20_main

        label playthrough2:

            # Poem minigame 1
            call poem
            python:
                try: renpy.file(config.basedir + "/CAN YOU HEAR ME.txt")
                except: open(config.basedir + "/CAN YOU HEAR ME.txt", "wb").write(renpy.file("CAN YOU HEAR ME.txt").read())

            # Day 1
            $ chapter = 1
            call ch21_main
            call poemresponse_start
            call ch21_end

            # Poem minigame 2
            call poem(False)
            python:
                try: renpy.file(config.basedir + "/iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt")
                except: open(config.basedir + "/iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt", "wb").write(renpy.file("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt").read())

            # Day 2
            $ chapter = 2
            call ch22_main
            call poemresponse_start
            call ch22_end

            # Poem minigame 3
            call poem(False)

            # Day 3
            $ chapter = 3
            call ch23_main
            if y_appeal >= 3:
                call poemresponse_start2
            else:
                call poemresponse_start

            if persistent.demo:
                stop music fadeout 2.0
                scene black with dissolve_cg
                "End of demo"
                return

            call ch23_end

            return

    elif persistent.playthrough == 3:
        jump ch30_main

    elif persistent.playthrough == 4:

        $ chapter = 0
        call ch40_main
        jump credits

label endgame(pause_length=4.0):
    $ quick_menu = False
    stop music fadeout 2.0
    scene black
    show end
    with dissolve_scene_full
    pause pause_length
    $ quick_menu = True
    return
