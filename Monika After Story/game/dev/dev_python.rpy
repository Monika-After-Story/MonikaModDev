# module for ptod related stuff (dev only

init 10 python:

    if persistent._mas_dev_enable_ptods is None:
        persistent._mas_dev_enable_ptods = True


init 2020 python:
    
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


### test eevent to show this screen
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ptod_console_testing",
            category=["dev"],
            prompt="TEST PTOD CONSOLE",
            pool=True,
            random=True,
            unlocked=True
        )
    )

label dev_ptod_console_testing:
    $ good_cmd = "a = 23"
    $ good_cmd_check = "a"
    $ bad_cmd = "please fail"
    $ local_context = dict()
    $ store.mas_ptod.restart_console()


    m "Hi, I'm going to show the console right now"
    m "edit 'good_cmd' and 'bad_cmd' to change the commands"
    m "edit 'good_cmd_check' to change the 'good_cmd' verification command"

    show monika at t22
    show screen mas_py_console_teaching

    m "I will write command to console"
    $ store.mas_ptod.write_command(good_cmd)
    m "This command should execute correctly"
    $ store.mas_ptod.exec_command(local_context)

    if len(good_cmd_check) > 0:
        m "let me check that the command worked!"
        $ store.mas_ptod.write_command(good_cmd_check)
        m "should get result!"
        $ store.mas_ptod.exec_command(local_context)

    m "now lets try something that will fail"
    $ store.mas_ptod.write_command(bad_cmd)
    m "this should fail with a reason"
    $ store.mas_ptod.exec_command(local_context)

    m "good?"
    m "okay time to hide screen"
    hide screen mas_py_console_teaching
    return

