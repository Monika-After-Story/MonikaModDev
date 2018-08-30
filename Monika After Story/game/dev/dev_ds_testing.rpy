init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ds_invoke_testing",
            category=["dev"],
            prompt="TEST INVOKE IN THREAD",
            pool=True,
            unlocked=True
        )
    )

label dev_ds_invoke_testing:
    python:
        mas_test = None
        def mas_invokeME():
            """
            This wants you to be invoked
            """
            global mas_test
            mas_test = store.mas_dockstat.generateMonika(mas_docking_station)

    m "Hi there. I am going to test invoke in new thread by running the generate function in a new thread"
    m "Okay, after this message, I will run the thread"
    $ renpy.invoke_in_thread(mas_invokeME)
    if mas_test is None:
        m "this happened"
    else:
        m "but it was not None"

    m "Was that a good test?"
    return
