## overlay testing

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_overlay_testing",
            category=["dev"],
            prompt="TEST OVERLAYS",
            pool=True,
            unlocked=True
        )
    )

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_shields_testing",
            category=["dev"],
            prompt="TEST SHIELDS",
            pool=True,
            unlocked=True
        )
    )


label dev_overlay_testing:
    m "Hello there! I'm going to hide all the overlays~"
    $ mas_OVLHide()
    m "Now the overlays are gone!"
    m 1hua "I'll bring them back in three lines."
    m eua "1"
    m "2"
    m "3"
    $ mas_OVLShow()
    m "And here they are~"

    return

label dev_shields_testing:
    m "Hello there! I'm going to disable the overlays, or raise shields."
    $ mas_OVLRaiseShield()
    m "Now the overlays cannot be interacted with!"
    m hua "I'll drop the shields in three lines."
    m eua "1"
    m "2"
    m "3"
    $ mas_OVLDropShield()
    m "Now the overlays can be interacted with!"
    return
