# deco testing

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_deco_tag_test",
            category=["dev"],
            prompt="DECO TAG TEST",
            pool=True,
            unlocked=True
        )
    )

label dev_deco_tag_test:
    # TODO:
    #   1. show image - not Now
    #   2. change bg
    #   3. hide image - not Now
    #   4. change bg
    #   5. show image now
    #   6. change bg
    #   7. hide image now
    #   8. change bg
    return

# TODO: create the following:
#   2 fake backgrounds
#   2 fake decorations
