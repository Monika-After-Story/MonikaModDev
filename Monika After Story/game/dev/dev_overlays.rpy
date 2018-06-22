## overlay testing

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_show_overlay_testing",
            category=["dev"],
            prompt="SHOW OVERLAYS",
            pool=True,
            random=True,
            unlocked=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_hide_overlay_testing",
            category=["dev"],
            prompt="HIDE OVERLAYS",
            pool=True,
            random=True,
            unlocked=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_raise_shields_testing",
            category=["dev"],
            prompt="RAISE SHIELDS",
            pool=True,
            random=True,
            unlocked=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_drop_shields_testing",
            category=["dev"],
            prompt="DROP SHIELDS",
            pool=True,
            random=True,
            unlocked=True
        )
    )


label dev_show_overlay_testing:
    m "Hi there, I am going show all the overlays."
    $ mas_showOverlays()
    m "Now you can see the overlays"
    return

label dev_hide_overlay_testing:
    m "Hi there, I am going to hide all the overlays."
    $ mas_hideOverlays()
    m "Now the overlays are gone!"
    return

label dev_raise_shields_testing:
    m "Hi there, I am going to disable the overlays (raise shields)"
    $ mas_raiseShields()
    m "Now the overlays cannot be interacted with!"
    return

label dev_drop_shields_testing:
    m "Hithere, I am going to enable the overlays (drop shields)"
    $ mas_dropShields()
    m "Now the overlays can be interacted with!"
    return
