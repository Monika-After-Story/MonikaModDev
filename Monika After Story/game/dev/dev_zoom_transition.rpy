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
    call monika_zoom_transition(new_zoom=2.1)
    # call expression "monika_zoom_transition" pass (new_zoom=2.1)
    #$ renpy.call_in_new_context("monika_zoom_transition", new_zoom=2.1)
    #pause 3.0
    # $ renpy.call("monika_zoom_transition",new_zoom=2.1)
    #jump dev_transition_test_max
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
    call monika_zoom_transition(new_zoom=1.1)
    # call expression "monika_zoom_transition" pass (new_zoom=1.1)
    #$ renpy.call_in_new_context("monika_zoom_transition", new_zoom=1.1)
    # $ renpy.restart_interaction()
    #pause 3.0
    # $ renpy.call("monika_zoom_transition",new_zoom=1.1)
    #jump dev_transition_test_min
    m 1esd "Finished transition"
    return

label dev_transition_test_min:
    call monika_zoom_transition(new_zoom=1.1)

label dev_transition_test_max:
    call monika_zoom_transition(new_zoom=2.1)
