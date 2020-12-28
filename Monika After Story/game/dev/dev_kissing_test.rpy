rpy python 3
# test kiss transition

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_mas_kiss",
            category=["dev"],
            prompt="TEST KISS",
            pool=True,
            unlocked=True
        )
    )

label dev_mas_kiss:
    m 1wubfb "Eh? D-Did you say... k-kiss?"
    m "This suddenly... it’s a little embarrassing..."
    m 6esbfa "But if it’s with you... I-I am okay with it ..."
    $ prev_kiss = persistent._mas_first_kiss
    call monika_kissing_motion
    $ persistent._mas_first_kiss = prev_kiss
    m 6esbfa "I love you [player]~"
    return
