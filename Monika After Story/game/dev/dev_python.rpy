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
