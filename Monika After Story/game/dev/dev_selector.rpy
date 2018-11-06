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
        start_test_items = [
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 1",
                "test1",
                "ring",
                hover_dlg="You hover over test 1",
                first_select_dlg="You first select test 1",
                select_dlg="You select test 1"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 2",
                "test1",
                "ring",
                hover_dlg="You hover over test 2",
                select_dlg="You select test 2"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 3",
                "test1",
                "ring",
                hover_dlg="You hover over test 3",
                select_dlg="You select test 3"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 4",
                "test1",
                "ring",
                hover_dlg="You hover over test 4",
                select_dlg="You select test 4"
            ),
            MASSelectableAccessory(
                mas_acs_promisering,
                "Test 5",
                "test1",
                "ring",
                hover_dlg="You hover over test 5",
                select_dlg="You select test 5"
            )
        ]
        for acs in start_test_items:
            acs.unlocked = True

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("pick test:")
        sel_map = {}

        sb_params = {
            "items": start_test_items,
            "confirm_label": "dev_selector_test_confirm",
            "cancel_label": "dev_selector_test_cancel",
            "mailbox": mailbox,
            "select_map": sel_map
        }

    m "no screen rn, am testing"
    return

    # TODO: this needs to be called, so we need to redo the jump logic.,
#    jump mas_selector_sidebar_select(start_test_items, "dev_selector_test_confirm", "dev_selector_test_cancel", 

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

