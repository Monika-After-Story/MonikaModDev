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
    m "Hi there, I am going to hide all the overlays."
    $ mas_OVLHide()
    m "Now the overlays are gone!"
    m "now in 3 lines of text i will show the overlays"
    m "1"
    m "2"
    m "3"
    $ mas_OVLShow()
    m "Now you can see the overlays"

    return

label dev_shields_testing:
    m "Hi there, I am going to disable the overlays (raise shields)"
    $ mas_OVLRaiseShield()
    m "Now the overlays cannot be interacted with!"
    m "now in 3 lines of text i will drop the shields"
    m "1"
    m "2"
    m "3"
    $ mas_OVLDropShield()
    m "Now the overlays can be interacted with!"
    return
