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
                True,
                hover_dlg="You hover over test 1"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 2",
                "test1",
                "ring",
                True,
                hover_dlg="You hover over test 2"
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
        ctx_map = {}
        show_dlg = []

        test_items = [
            MASSelectableImageButtonDisplayable(
                tem,
                ctx_map,
                (1075, 5, 200, 625, 5),
                show_dlg
            )
            for tem in test_items
        ]


    m "first lets show the sidebar."

    show screen mas_selector_sidebar(test_items, "dev_selector_test_confirm", "dev_selector_test_cancel")

label dev_selector_test_loop:
    python:
        if len(show_dlg) == 0:
            tx_out = "Wait here!"

        else:
            tx_out = show_dlg.pop()

    m "[tx_out]"

    jump dev_selector_test_loop
    
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

label dev_selector_test_hover:
    m "you hovere in test1"
    return

label dev_selector_test_hover2:
    m " you hver in test2"
    return

