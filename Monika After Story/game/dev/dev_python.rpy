# module for ptod related stuff (dev only

init 10 python:

    if persistent._mas_dev_enable_ptods is None:
        # force this to False by default
        persistent._mas_dev_enable_ptods = False


init 998 python:
    
    def mas_reset_ptods():
        """
        Removes all PTODS from the lockDB and per_eventDB
        this basically allows them to be refreshed on next load.

        NOTE: this quits the game
        """
        # max 1000 tips
        tip_list = [
            mas_ptod.M_PTOD.format(tip_num)
            for tip_num in range(0,1000)
        ]

        mas_remove_event_list(tip_list)


    def mas_ptod_warptime():
        """
        Emulates moving forward 1 day by changing all currently unlocked
        python tips to have an unlock date of yesterday
        """
        # max 1000 tips
        tip_list = [
            mas_ptod.M_PTOD.format(tip_num)
            for tip_num in range(0,1000)
        ]
        yesterday = datetime.date.today() - datetime.timedelta(1)

        for tip in tip_list:
            tip_ev = mas_getEV(tip)

            if tip.unlock_date is not None:
                tip.unlock_date = yesterday


### test eevent to show this screen
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ptod_console_testing",
            category=["dev"],
            prompt="TEST PTOD CONSOLE",
            pool=True,
            unlocked=True
        )
    )

label dev_ptod_console_testing:
    $ good_cmd = "a = 23"
    $ good_cmd_check = "a"
    $ bad_cmd = "please fail"
    $ local_context = dict()
    $ store.mas_ptod.restart_console()

    m "Hello! I'm going to show the console."
    m "Edit 'good_cmd' and 'bad_cmd' to change the commands."
    m "Edit 'good_cmd_check' to change the 'good_cmd' verification command."

    show monika at t22
    show screen mas_py_console_teaching

    m "I'll write something to the console."
    $ store.mas_ptod.write_command(good_cmd)
    m "This command should execute correctly."
    $ store.mas_ptod.exec_command(local_context)

    if len(good_cmd_check) > 0:
        m "Let me check to see if that command worked..."
        $ store.mas_ptod.write_command(good_cmd_check)
        m 1hua "And no issues."
        $ store.mas_ptod.exec_command(local_context)

    m 1eua "Now, let's try something that will fail..."
    $ store.mas_ptod.write_command(bad_cmd)
    m "This should fail, and give a reason."
    $ store.mas_ptod.exec_command(local_context)

    m "Alright, I hope everything's working~"
    m "I'll hide the screen now."
    hide screen mas_py_console_teaching
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ptod_console_testing_lines",
            category=["dev"],
            prompt="TEST PTOD CONSOLE MAX",
            pool=True,
            unlocked=True
        )
    )

label dev_ptod_console_testing_lines:
    python:
        char_lim = list()
        for i in range(1, store.mas_ptod.LINE_MAX-4+1):
            char_lim.append(str(i % 10))

        char_lim = "".join(char_lim)

        local_context = dict()
        store.mas_ptod.restart_console()
        max_history = store.mas_ptod.H_SIZE + 1

    m "I'll show the screen!"
    show monika at t22
    show screen mas_py_console_teaching

    m "I'm going to test for the maximum lines and characters."

    m "First, the max number of characters is [store.mas_ptod.LINE_MAX]."
    $ store.mas_ptod.write_command(char_lim)
    $ store.mas_ptod.exec_command(local_context)

    m "And the max number of lines in history is [max_history]."
    python:
        for ln in range(0, store.mas_ptod.H_SIZE):
            store.mas_ptod.write_command(char_lim)
            store.mas_ptod.exec_command(local_context)

    m "And there you have it! The console dimensions."
    m "I'll hide the screen now~"
    hide screen mas_py_console_teaching
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ptod_console_testing_line_break",
            category=["dev"],
            prompt="TEST PTOD CONSOLE LINE BREAK",
            pool=True,
            unlocked=True
        )
    )

label dev_ptod_console_testing_line_break:
    python:
        char_lim = list()
        for i in range(1, store.mas_ptod.LINE_MAX+1):
            char_lim.append(str(i % 10))

        char_lim = "".join(char_lim)

        local_context = dict()
        store.mas_ptod.restart_console()

    m "Here, I'll bring the screen up."
    show monika at t22
    show screen mas_py_console_teaching

    m "I'm going to test for line breaks."

    m "First, the max number of characters is [store.mas_ptod.LINE_MAX]."
    $ store.mas_ptod.write_command(char_lim)
    m "This command should be split on 2 lines."
    $ store.mas_ptod.exec_command(local_context)
    m "But the result should fit on one line."

    m "I hope everything's working!"
    m "Alright, I'll hide the screen now~"
    hide screen mas_py_console_teaching
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ptod_console_testing_block",
            category=["dev"],
            prompt="TEST PTOD CONSOLE BLOCK",
            pool=True,
            unlocked=True
        )
    )

label dev_ptod_console_testing_block:
    python:
        char_lim = list()
        for i in range(1, store.mas_ptod.LINE_MAX+1):
            char_lim.append(str(i % 10))

        char_lim = "".join(char_lim)

        local_context = dict()
        store.mas_ptod.restart_console()

    m "Here, I'll pull the screen up~"
    show monika at t22
    show screen mas_py_console_teaching

    m 1hua "I'm going to test block statements."

    m eua "First, let's define two test values."
    $ store.mas_ptod.write_command("test = 12")
    pause 0.7
    $ store.mas_ptod.exec_command(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("result = 0")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)

    m "Now to run if statement tests..."
    $ store.mas_ptod.w_cmd("if test % 2 == 1:")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("    result = 1")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("elif test % 3 == 0:")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("    result = 2")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("else:")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("    result = 3")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)
    pause 0.7
    $ store.mas_ptod.w_cmd("")
    m "Hopefully, there's no errors here."
    $ store.mas_ptod.x_cmd(local_context)
    m "The result should be 2!"
    $ store.mas_ptod.w_cmd("result")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)

    m "Let's try a syntax error."
    $ store.mas_ptod.w_cmd(":")
    pause 0.7
    $ store.mas_ptod.x_cmd(local_context)

    m "And now, a block error..."
    call mas_w_cmd("if True:")
    call mas_x_cmd(local_context)
    call mas_w_cmd(" result = 100")
    call mas_x_cmd(local_context)
    call mas_w_cmd("  result = 200")
    call mas_x_cmd(local_context)
    call mas_w_cmd("")
    m "We should get an error now."
    call mas_x_cmd(local_context)

    m "But the result should still be 2."
    call mas_w_cmd("result")
    call mas_x_cmd(local_context)

    m "Okay, now for a loop!"
    call mas_wx_cmd("size = 11", local_context)
    call mas_wx_cmd("a_list = list()", local_context)
    call mas_wx_cmd("for i in range(0, size):", local_context)
    call mas_wx_cmd("  a_list.append(i)", local_context)
    call mas_w_cmd("")
    m "Here we go!"
    call mas_x_cmd(local_context)

    m "And let's print out the list..."
    call mas_wx_cmd("a_list", local_context)

    m "Alright, time to disable the console."
    $ store.mas_ptod.ex_cn()

    m 1hua "I think that's enough testing for today."
    m 1eua "I hope everything's working."
    m "Alright, I'll hide the screen now~"
    hide screen mas_py_console_teaching
    return
