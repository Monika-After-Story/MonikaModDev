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

    ## internal utility functions DO NOT USE

    def __add_idxs(_db, _key, _exp_len, idx_d_list):
        """INTERNAL ONLY
        adds indexes to the given key to the given db
        """
        # length check
        ignore_len = _exp_len < 0

        _data = list(_db[_key])

        if ignore_len or len(_data) == _exp_len:
            for idx, idx_data in idx_d_list:
                _data.insert(idx, idx_data)

            _db[_key] = tuple(_data)


    def __rm_idxs(_db, _key, _exp_len, idx_list)
        """INTERNAL ONLY
        removes indexes off the given key off the given db
        """
        # length check
        ignore_len = _exp_len <= 0

        _data = list(_db[_key])

        if ignore_len or len(_data) == _exp_len:
            for idx in idx_list
                _data.pop(idx)

            _db[_key] = tuple(_data)


    ## utility functions

    def add_idxs(_db, _key, _exp_len, *idxs_d):
        """
        Adds indexes to the given key 

        NOTE: indxs_d is added in reverse order. 

        IN:
            _db - database to add indexes to
            _key - key of the item to add indexes to
            _exp_len - the length the item should have prior to addition
                Pass in less than 0 to ignore length checks
            *idxs_d - tuples of the following format:
                [0]: index to add
                [1]: data to add at index
        """
        if len(idxs_d) < 1:
            return

        __add_idxs(_db, _key, _exp_len, sorted(idxs_d, reverse=True))


    def add_idxs_db(_db, _exp_len, *idxs_d):
        """
        Adds indexes to items in the given db

        IN:
            _db - database to add indexes to
            _exp_len - the length the item shoudl have prior to additoin
                Pass in 0 or less to ignore length checks
            *idxs_d - tuples of the following format:
                [0]: index to add
                [1]: data to add at index
        """
        # sanity check
        if len(idxs_d) < 1:
            return

        idxs_d_rev = sorted(idxs_d, reverse=True)

        for item in _db:
            __add_idxs(_db, item, _exp_len, idxs_d_rev)


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

        __rm_idxs(_db, _key, _exp_len, sorted(idxs, reverse=True))
        

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

        idxs_rev = sorted(idxs, reverse=True)

        for item in _db:
            __rm_idxs(_db, item, _exp_len, idxs_rev)


    ## migration functions

    def _dm_1_to_2():
        """
        Data migration from version 1 to 2

        GOALS:
            - remove rules property from events and shrink the tuples.
        """
        ### needed vars
        rules_index = 14
        curr_len = 20 # number of properties ver 1 events have. 

        ### perform logic

        # removes rules proprety at index 14
        for _db in per_dbs:
            rm_idxs_db(_db, curr_len, rules_index)

        # removes rules proerty in lock db at index 14
        rm_idxs_db(lock_db, curr_len, rules_index)


    def _dm_2_to_1():
        """
        Data migration from version 2 to 1

        GOALS:
            - add rules property to events, expand tuples
        """
        ### needed vars
        rules_index = 14
        rules_data = {}
        curr_len = 19 # number of properties ver 1 events have. 

        ### perform logic

        # adds rules property in index 14
        for _db in per_dbs:
            add_idxs_db(_db, curr_len, (rules_index, rules_data))

        # adds rules property to lock db index 14
        add_idxs_db(lock_db, curr_len, (rules_index, rules_data))


    # data migration map maps data migration functions and a version jump:
    #   key: tuple of the following format:
    #       [0]: version starting from
    #       [1]: version updating to
    #   value: function to run
    dm_map = {

        # if we dont have a current dm version, we can assume we are using
        #   the latest one
        (None, dm_data_version): None,
        (1, 2): _dm_1_to_2,
        (2, 1): _dm_2_to_1,
    }


init -897 python:
    pass
    
    



    # NOTE: this should be the last thing we do

    persistent._mas_dm_data_version = 1
    # this should be updated whenever we do a data version migration


