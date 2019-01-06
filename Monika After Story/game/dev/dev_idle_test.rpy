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


init -1 python in mas_greetings:

    TYPE_IDLE_RET_TEST = "idle_test"


label dev_idle_test:
    m 1eua "Hi there! I will test idle mode now."
    
    # set crash/quit greeting
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_IDLE_RET_TEST

    # set return label when done with idle
    $ mas_idle_mailbox.send_idle_cb("dev_idle_test_cb")

    # return idle to notify event system to switch to idle
    return "idle"


label dev_idle_test_cb:
    m 1hua "done with idle!"
    return


init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_dev_idle_test",
            unlocked=True,
            category=[
                store.mas_greetings.TYPE_IDLE_RET_TEST,
            ],
        ),
        code="GRE"
    )

label greeting_dev_idle_test:

    if persistent._mas_idle_mode_was_crashed:

        # NOTE: when first crashed, you might want to launch a slightly custom
        #   version of the existing first crash dialogue.
        #   See the mas_crashed_start label in script-story-events for labels
        #   you can call to trigger certain bits of the starting crash setup

        if persistent._mas_crashed_before:
            # crashed

            # this restores visuals and other things
            call mas_crashed_preshort

            m 1hua "i THINK you CRASHSED"

            call mas_crashed_post

        else:
            # first time crash

            # this just sets some vars
            call mas_crashed_prelong

            $ scene_change = True
            call spaceroom
            
            m 1hua "i THINK you CRASHED for the first time"

            call mas_crashed_post

    else:
        # quit
        m 2efc "I think YOU closed THE game ON me"

    m "okay we good now."
    return
