init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_pausedisplayable_test",
            category=["dev"],
            prompt="TEST PAUSEDISPLAYABLE",
            pool=True,
            unlocked=True
        )
    )

label dev_pausedisplayable_test:
    m 1eua "I'll start the pause and queue multiple events with different parameters.{w=0.5}.{w=0.5}.{nw}"

    python hide:
        events = (
            PauseDisplayableEvent(
                datetime.timedelta(seconds=5),
                renpy.partial(renpy.invoke_in_new_context, renpy.say, store.m, "5 SECONDS. REPEATABLE."),
                repeatable=True
            ),
            PauseDisplayableEvent(
                datetime.timedelta(seconds=10),
                renpy.partial(renpy.say, store.m, "10 SECONDS. INVOKED."),# This would crash w/o invoke_in_new_context
                invoke_in_new_context=True
            ),
            PauseDisplayableEvent(
                datetime.timedelta(seconds=3),
                renpy.partial(renpy.say, store.m, "3 SECONDS. INVOKED."),
                invoke_in_new_context=True
            ),
            PauseDisplayableEvent(
                datetime.timedelta(seconds=15),
                (
                    renpy.partial(renpy.invoke_in_new_context, renpy.say, store.m, "15 SECONDS. REPEATABLE. RESTARTS INTERACTION."),
                    renpy.partial(renpy.show, "monika 2eua")# The screen wouldn't update w/o restart_interaction
                ),
                repeatable=True,
                restart_interaction=True
            )
        )
        disp = PauseDisplayableWithEvents()
        disp.set_events(events)
        disp.start()

    m 1eua "We're done.{w=1}{nw}"

    return
