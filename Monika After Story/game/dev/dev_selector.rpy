# selector testing

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_selector_test",
            category=["dev"],
            prompt="TEST SELECTOR (sidebar raw visual)",
            pool=True,
            unlocked=True
        )
    )


label dev_selector_test:
    m 1eua "Hi [player], I will test the sidebar selector system. (RAW)"

    python:
        test_items = [
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 1",
                "test1",
                "ring",
                True
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 2",
                "test1",
                "ring",
                True
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 3",
                "test1",
                "ring",
                True
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 4",
                "test1",
                "ring",
                True
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 5",
                "test1",
                "ring",
                True
            )
        ]

    m "first lets show the sidebar."
    $ ctx_map = {}

    show screen mas_selector_sidebar(test_items, ctx_map, "dev_selector_test_confirm", "dev_selector_test_cancel")

    m " okay! now we can test shit!"

    m "does it look okay visually?"
    
    m "now lets hide it"
    hide screen mas_selector_sidebar
    m "done!"
    return

label dev_selector_test_confirm:
    hide screen mas_selector_sidebar
    m "you hit the confirm button!"
    return

label dev_selector_test_cancel:
    hide screen mas_selector_sidebar
    m "You hit the cancel button!"
    return

