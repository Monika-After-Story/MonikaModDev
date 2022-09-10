init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_moni_disps_test",
            category=["dev"],
            prompt="MONIKA'S DISPLAYABLES TESTS",
            pool=True,
            unlocked=True
        )
    )

label dev_moni_disps_test:
    m 1eua "What do you want to test?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you want to test?{fast}"

        "Test idle disp.":
            $ test_idle_disp = MASMoniIdleDisp(
                (
                    MASMoniIdleExp("1eua", duration=3),
                    MASMoniIdleExp("1hua", duration=3),
                    MASMoniIdleExp("5eubsa", duration=3),
                    MASMoniIdleExp("5esu", duration=3),
                    MASMoniIdleExpGroup(
                        [
                            MASMoniIdleExp("1eua", duration=1),
                            MASMoniIdleExp("1kua", duration=1),
                            MASMoniIdleExp("1eua", duration=2),
                        ]
                    ),
                    MASMoniIdleExp("1eua_follow", duration=3),
                    MASMoniIdleExp("5esu_follow", duration=3)
                )
            )
            m 3eub "Remember, you can do `watch test_idle_disp` to keep track of the parameters."
            m 1eua "Click when you're done."
            show expression test_idle_disp as monika at i11 zorder MAS_MONIKA_Z
            $ PauseDisplayableWithEvents().start()

        "Test follow disps.":
            $ test_idle_disp = MASMoniIdleDisp(
                (
                    MASMoniIdleExp("1eua_follow", duration=10),
                    MASMoniIdleExp("5esu_follow", duration=10),
                    MASMoniIdleExp("5eubsa_follow", duration=19)
                )
            )
            m 1eua "Click when you're done."
            show expression test_idle_disp as monika at i11 zorder MAS_MONIKA_Z
            $ PauseDisplayableWithEvents().start()

        "Test wink disp.":
            m 3eub "I'll auto progress this one for you, don't click."
            show monika 1eua
            $ renpy.pause(0.5)

            m 1kua "Left wink via dlg line.{w=1.5}{nw}"
            m 1eua "Left wink via extend.{w=1.0}{nw}"
            extend 1kua "{w=1.0}{nw}"
            m 1eua "Left wink via show.{w=1.0}{nw}"
            window hide
            $ renpy.pause(0.2)
            show monika 1kua
            $ renpy.pause(1.0)

            show monika 1eua
            $ renpy.pause(0.5)

            m 1nua "Right wink via dlg line.{w=1.5}{nw}"
            m 1eua "Right wink via extend.{w=1.0}{nw}"
            extend 1nua "{w=1.0}{nw}"
            m 1eua "Right wink via show.{w=1.0}{nw}"
            window hide
            $ renpy.pause(0.2)
            show monika 1nua
            $ renpy.pause(1.0)

            show monika 1eua
            $ renpy.pause(0.5)

            m 1eua "Now idle winks.{w=1.0}{nw}"
            $ mas_moni_idle_disp.force(
                MASMoniIdleExpGroup(
                    [
                        MASMoniIdleExp("1eua", duration=1),
                        MASMoniIdleExp("1kua", duration=1),
                        MASMoniIdleExp("1eua", duration=1),
                        MASMoniIdleExp("1nua", duration=1),
                        MASMoniIdleExp("1eua", duration=2),
                    ]
                ),
                skip_dissolve=True
            )
            show monika idle at i11 zorder MAS_MONIKA_Z
            $ renpy.pause(6.0)

        "Test tears disp.":
            $ pd = PauseDisplayableWithEvents()
            m 1eua "Click to progress to the next image."
            show monika 1ektsc at i11 zorder MAS_MONIKA_Z
            $ pd.start()
            $ pd.reset()
            show monika 1lktsc at i11 zorder MAS_MONIKA_Z
            $ pd.start()
            $ pd.reset()
            show monika 1rktsc at i11 zorder MAS_MONIKA_Z
            $ pd.start()

    m 1eua "Do you want to test anything else?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you want to test anything else?{fast}"

        "Yes.":
            jump dev_moni_disps_test

        "No.":
            pass

    return
