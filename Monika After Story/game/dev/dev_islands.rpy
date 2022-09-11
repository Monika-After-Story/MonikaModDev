init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_test_islands_progress",
            category=["dev"],
            prompt="SHOW ISLANDS PROGRESS",
            rules={"keep_idle_exp": None},
            pool=True,
            unlocked=True
        )
    )

label dev_test_islands_progress:
    if not config.developer:
        m 1rtsdlb "You're not supposed to use this, [player]..."
        return

    show monika 1eua

    $ data_lists = list()

    python hide:
        pm_var_backup = persistent._mas_pm_cares_island_progress

        try:
            start_lvl = store.mas_utils.tryparseint(
                renpy.input(
                    "Enter start level (default 0)",
                    allow=numbers_only,
                    length=3
                ).strip("\t\n\r"),
                0
            )

            data_def_rate = collections.defaultdict(list)
            data_fast_rate = collections.defaultdict(list)
            data_slow_rate = collections.defaultdict(list)

            for i in range(3):
                curr_lvl = start_lvl
                progress = store.mas_island_event.DEF_PROGRESS

                if i == 0:
                    first_text = "Default"
                    persistent._mas_pm_cares_island_progress = None
                    data = data_def_rate

                elif i == 1:
                    first_text = "Fast"
                    persistent._mas_pm_cares_island_progress = True
                    data = data_fast_rate

                else:
                    first_text = "Slow"
                    persistent._mas_pm_cares_island_progress = False
                    data = data_slow_rate

                while progress < store.mas_island_event.MAX_PROGRESS_LOVE:
                    progress = store.mas_island_event._calcProgress(curr_lvl, start_lvl)
                    data[progress].append(curr_lvl)
                    curr_lvl += 1

                data_lists.append([first_text])

                data_lists[-1].extend(
                    [
                        "Player lvls: {1}\nIslands lvl: {0}".format(
                            k,
                            ", ".join(map(str, v))
                        )
                        for k, v in data.iteritems()
                    ]
                )

        finally:
            persistent._mas_pm_cares_island_progress = pm_var_backup

    m "Press Esc when you're done.{w=1.0}{nw}"

    $ HKBHideButtons()
    call screen dev_test_islands_progress(data_lists)
    $ HKBShowButtons()

    $ del data_lists

    return

screen dev_test_islands_progress(data_lists):
    style_prefix "scrollable_menu"

    key "K_ESCAPE" action Return()

    frame:
        background "black"
        viewport:
            xcenter 0.5
            mousewheel True
            draggable True

            grid len(data_lists) len(data_lists[0]):
                spacing 75
                transpose True

                for data_list in data_lists:
                    for string in data_list:
                        text string:
                            xalign 0.5
                            text_align 0.5
