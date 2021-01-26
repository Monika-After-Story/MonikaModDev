# testing module ofr idle

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel='dev_idle_test',
            prompt="TEST IDLE MODE",
            category=['dev'],
            pool=True,
            unlocked=True,
        )
    )



label dev_idle_test:
    m 1eua "Hi there! I will test idle mode now."

    # set idle data
    $ persistent._mas_idle_data["dev_idle_test"] = True

    # set return label when done with idle
    $ mas_idle_mailbox.send_idle_cb("dev_idle_test_cb")

    # return idle to notify event system to switch to idle
    return {"idle": None}


label dev_idle_test_cb:
    m 1hua "done with idle!"
    return



