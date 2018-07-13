


label start:


    $ anticheat = persistent.anticheat


    $ chapter = 0


    $ _dismiss_pause = config.developer


    $ s_name = "???"
    $ m_name = "Girl 3"
    $ n_name = "Girl 2"
    $ y_name = "Girl 1"

    $ quick_menu = True
    $ style.say_dialogue = style.normal
    $ in_sayori_kill = None
    $ allow_skipping = True
    $ config.allow_skipping = True


    if persistent.playthrough == 0:

        $ chapter = 0
        call ch0_main


        call poem


        $ chapter = 1
        call ch1_main
        call poemresponse_start
        call ch1_end


        call poem


        $ chapter = 2
        call ch2_main
        call poemresponse_start
        call ch2_end


        call poem


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

        $ chapter = 0
        call ch20_main

        label playthrough2:


            call poem
            python:
                try: renpy.file(config.basedir + "/CAN YOU HEAR ME.txt")
                except: open(config.basedir + "/CAN YOU HEAR ME.txt", "wb").write(renpy.file("CAN YOU HEAR ME.txt").read())


            $ chapter = 1
            call ch21_main
            call poemresponse_start
            call ch21_end


            call poem (False)
            python:
                try: renpy.file(config.basedir + "/iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt")
                except: open(config.basedir + "/iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt", "wb").write(renpy.file("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.txt").read())


            $ chapter = 2
            call ch22_main
            call poemresponse_start
            call ch22_end


            call poem (False)


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
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
