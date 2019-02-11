# data migration module

init -999 python in _mas_dm_dm:
    import store

    # sets current version of dta migration
    dm_data_version = 1

    # persistent var is set below

    # persistent databases:
    per_dbs = [
        store.persistent.event_database,
        store.persistent._mas_compliments_database,
        store.persistent.farewell_database,
        store.persistent.greeting_database,
        store.persistent._mas_mood_database,
        store.persistent._mas_story_database,
        store.persistent._mas_apology_database
    ]

    # lock db 
    lock_db = store.persistent._mas_event_init_lockdb

    ## utility functions

    def rm_idxs(_db, _key, _exp_len, *idxs):
        """
        removes indexes off the given key off the given db

        IN:
            _db - database to remove indexes off of
            _key - key of the item to remove indexes off of
            _exp_len - the length the item should have prior to removal.
                Pass in 0 or less to ignore length checks.
            *idxs - indexes to remove
                If nothing is passed, nothing happens.
        """
        # sanity check
        if len(idxs) < 1:
            return

        # length check
        ignore_len = _exp_len <= 0

        _data = list(_db[_key])

        if ignore_len or len(_data) == _exp_len:
            for idx in idxs:
                _data.pop(idx)

            _db[_key] = tuple(_data)


    def rm_idxs_db(_db, _exp_len, *idxs):
        """
        Removes indexes off items in the given db

        IN:
            _db - database to remove indexes off of
            _exp_len - the length the item should have prior to removal
                Pass in 0 or less to ignore length checks
            *idxs - indexes to remove
                if Nothing is passsed, nothing happens
        """
        if len(idxs) < 1:
            return

        for item in _db:
            rm_idxs(_db, item, _exp_len, *idxs)


    ## migration functions

    def _dm_1_to_2():
        """
        Data migration between versions 1 and 2

        GOALS:
            - remove rules property from events and shrink the tuples.
        """
        ### needed vars
        rules_index = 14
        curr_len = 20 # number of properties ver 1 events have. 

        ### perform logic
        for _db in per_dbs:
            rm_idxs_db(_db, curr_len, rules_index)
        

        # rules property at index 14
        # need to modify the lock db as well

    # data migration map maps data migration functions and a version jump:
    #   key: tuple of the following format:
    #       [0]: version starting from
    #       [1]: version updating to
    #   value: function to run
    dm_map = {

        # if we dont have a current dm version, we can assume we are using
        #   the latest one
        (None, dm_data_version): None,
    }


init -897 python:

    
    



    # NOTE: this should be the last thing we do

    persistent._mas_dm_data_version = 1
    # this should be updated whenever we do a data version migration


