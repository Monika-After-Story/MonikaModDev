# test zoom transitions
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_mas_max_zoom",
            category=["dev"],
            prompt="TEST TRANSITION MAX ZOOM",
            pool=True,
            unlocked=True
        )
    )

label dev_mas_max_zoom:
    m 1esa "Testing transition"
    call monika_zoom_transition(new_zoom=20)
    m 1esd "Finished transition"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_mas_min_zoom",
            category=["dev"],
            prompt="TEST TRANSITION MIN ZOOM",
            pool=True,
            unlocked=True
        )
    )

label dev_mas_min_zoom:
    m 1esa "Testing transition"
    call monika_zoom_transition(new_zoom=0)
    m 1esd "Finished transition"
    return
