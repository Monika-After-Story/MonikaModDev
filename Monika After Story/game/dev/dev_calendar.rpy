## calendar testing

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_calendar_testing",
            category=["dev"],
            prompt="TEST CALENDAR",
            pool=True,
            random=True,
            unlocked=True
        )
    )

label dev_calendar_testing:
    $ import store.mas_calendar as mas_cal
    menu:
        m "Which do you want to do?"
        "View Calenar":
            call mas_start_calendar_read_only

        "Select Date":
            call mas_start_calendar_select_date

            $ sel_date = _return

            if not sel_date:
                m "You did not select a date!"

            else:
                $ sel_date_formal = sel_date.strftime("%B %d, %Y")
                m "You selected [sel_date_formal]."

    return
                    



