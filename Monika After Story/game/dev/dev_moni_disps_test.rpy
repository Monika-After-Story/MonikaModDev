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

        "Test idle disp dissolves.":
            $ test_idle_disp = MASMoniIdleDisp(
                (
                    MASMoniIdleExp("1eua", duration=5),
                    MASMoniIdleExp("1hua", duration=5),
                    MASMoniIdleExp("5eubsa", duration=5),
                    MASMoniIdleExp("5esu", duration=5)
                )
            )
            show expression test_idle_disp as monika at i11 zorder MAS_MONIKA_Z
            $ PauseDisplayableWithEvents().start()

        "Test winks disp.":
            $ renpy.pause(0.5)
            m 1kua "Left wink."
            m 1nua "Right wink."
            m 1eua "Now idle winks.{w=0.2}.{w=0.2}.{w=0.2}{nw}"
            $ mas_moni_idle_disp.force(
                MASMoniIdleExpGroup(
                    [
                        MASMoniIdleExp("1eua", duration=1),
                        MASMoniIdleExp("1kua", duration=1),
                        MASMoniIdleExp("1eua", duration=1),
                        MASMoniIdleExp("1nua", duration=1),
                        MASMoniIdleExp("1eua", duration=3),
                    ]
                ),
                skip_dissolve=True
            )
            show monika idle at i11 zorder MAS_MONIKA_Z
            $ renpy.pause(7.0)

        "Streaming tears disp.":
            $ pd = PauseDisplayableWithEvents()
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
