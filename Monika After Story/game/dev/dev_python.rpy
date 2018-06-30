# module for ptod related stuff (dev only

init 10 python:

    if persistent._mas_dev_enable_ptods is None:
        persistent._mas_dev_enable_ptods = True


init 2018 python in dev_ptod:
    import store.mas_ptod as mas_ptod 

    # because its easier this way
    persistent = renpy.game.persistent

    
    def reset_ptods():
        """
        Removes all PTODS from the lockDB and per_eventDB
        this basically allows them to be refreshed on next load.
        """
        # max 1000 tips
        for tip_num in range(0,1000):
            tip_label = mas_ptod.M_PTOD.format(tip_num)

            # remove from persistent
            if tip_label in persistent.event_database:
                persistent.event_database.pop(tip_label)

            # also lock entruy
            if tip_label in Event.INIT_LOCKDB:
                Event.INIT_LOCKDB.pop(tip_label)

