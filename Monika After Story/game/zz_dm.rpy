# data migration module

init -999 python in _mas_dm_dm:
    import store

    # sets current version of dta migration
    dm_data_version = 2
    # this should be updated whenever we do a data version migration

    # persistent var is set below

    #TODO: Add persistent._mas_windowreacts_database to this
    # persistent databases:
    per_dbs = [

        # ver 1, 2
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


    def __rm_idxs(_db, _key, _exp_len, idx_list):
        """INTERNAL ONLY
        removes indexes off the given key off the given db
        """
        # length check
        ignore_len = _exp_len <= 0

        _data = list(_db[_key])

        if ignore_len or len(_data) == _exp_len:
            for idx in idx_list:
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
        if len(idxs) < 1 or _db is None:
            return

        idxs_rev = sorted(idxs, reverse=True)

        for item in _db:
            __rm_idxs(_db, item, _exp_len, idxs_rev)


    ## migration functions

    def __dm_1_to_2_helper(curr_len):
        ### needed vars
        rules_index = 14

        ### perform logic

        # removes rules proprety at index 14
        for _db in per_dbs:
            rm_idxs_db(_db, curr_len, rules_index)

        # removes rules proerty in lock db at index 14
        rm_idxs_db(lock_db, curr_len, rules_index)


    def _dm_1_to_2():
        """
        Data migration from version 1 to 2

        GOALS:
            - remove rules property from events and shrink the tuples.
        """
        # ver 1 means we have 20 props
        __dm_1_to_2_helper(20)


    def _dm_0811_to_2():
        """
        Data migration from version 0811-0814 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        # versions 0811-0814 means we have 19 props
        __dm_1_to_2_helper(19)


    def _dm_089_to_2():
        """
        Data migration from version 089-0810 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        # versions 089-0810 means we have 18 props
        __dm_1_to_2_helper(18)


    def _dm_082_to_2():
        """
        Data migration from version 082-088 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        # versions 082-088 means we have 17 props
        __dm_1_to_2_helper(17)


    def _dm_080_to_2():
        """
        Data migration from version 080-081 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        # versions 080-081 means we have 16 props
        __dm_1_to_2_helper(16)


    def _dm_073_to_2():
        """
        Data migration from version 073-074 to 2

        GOALS:
            - remove rules property from events and shrink the tuples
        """
        # versions 073-074 means we have 15 props
        __dm_1_to_2_helper(15)


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
        add_idxs_db(lock_db, curr_len, (rules_index, False))


    # data migration map maps data migration functions and a version jump:
    #   key: tuple of the following format:
    #       [0]: version starting from
    #       [1]: version updating to
    #   value: function to run
    dm_map = {
        # special versions (aka migrating to 091)
        (-1, 2): _dm_0811_to_2,
        (-2, 2): _dm_089_to_2,
        (-3, 2): _dm_082_to_2,
        (-4, 2): _dm_080_to_2,
        (-5, 2): _dm_073_to_2,

        # regular data migrations
        (1, 2): _dm_1_to_2,
        (2, 1): _dm_2_to_1,
    }


    ## algorithm runners
    def _determine_version():
        """
        This returns an  appropriate dm version based on version
        NOTE: this should only be used if migrating from versions 0814 and
        below.
        """
        # if this value is None, but version number is not None, then the user
        # is coming from a post 0.5.0 install. They should have some data,
        # but we only want to modify it if contains RULES.
        version, sp, ignore = store.persistent.version_number.partition("-")
        maj_ver, mid_ver, min_ver = version.split(".")
        ## NOTE: crash if this fails.
        mid_ver = int(mid_ver)
        min_ver = int(min_ver)

        if mid_ver == 8:
            if 11 <= min_ver <= 14:
                return -1

            elif 9 <= min_ver <= 10:
                return -2

            elif 2 <= min_ver <= 8:
                return -3

            else:
                # 080 or 081
                return -4

        elif mid_ver == 7 and 3 <= min_ver <= 4:
            # 073 or 074
            return -5

        # otherwise, we do NOT do any ver migrations
        return dm_data_version


    def __lessthan(val_a, val_b):
        return val_a < val_b


    def __morethan(val_a, val_b):
        return val_a > val_b


    def _find_dm_fun(piv_ver, adj_ver, direction):
        """
        Iterates until we find a dm function and returns it.

        IN:
            piv_ver - the verion number we dont want to change when searching
            adj_ver - the verison number we change when searching
            direction - the direction to change adj_ver

        RETURNS tuple of the following format:
            [0]: data migration function found, Or none if not found
            [1]: value of adj_ver when data migration found
        """
        if direction < 0:
            # if we are decreasing the adj_ver, then we want to stop when
            #   adj_ver is less than or equal to piv_ver
            ver_not_passed = __lessthan
        else:
            # if we are increasing the adj_ver, then we want to stop when
            #   adj_ver is more than or equal to piv_ver
            ver_not_passed = __morethan

        # start
        dm_found = dm_map.get((piv_ver, adj_ver), None)
        while dm_found is None and ver_not_passed(piv_ver, adj_ver):
            adj_ver += direction
            dm_found = dm_map.get((piv_ver, adj_ver), None)

        return (dm_found, adj_ver)


    def run(start_ver, end_ver):
        """
        Runs the data migration algorithms.

        ASSUMES: start_ver != end_ver

        IN:
            start_ver - start version to start
            end_ver - ending version number
        """
        _dm_fun = dm_map.get((start_ver, end_ver), None)

        if _dm_fun == -1:
            # this is first run.
            return

        if _dm_fun is not None:
            # we have a direct migration
            _dm_fun()
            return

        # otherwise, we need to loop
        # but first, to find direction
        # NOTE: direction is what value we should add to END version.
        #   NOT what direction we are updating to.
        if start_ver < end_ver:
            direction = -1
        else:
            direction = 1

        curr_ver = start_ver
        while curr_ver != end_ver:
            _dm_fun, new_ver = _find_dm_fun(curr_ver, end_ver, direction)

            if _dm_fun is None:
                raise Exception(
                    "DATA MIGRATION FAILURE. {0} to {1}".format(
                        curr_ver, end_ver
                    )
                )

            # run the function and set the curr ver
            _dm_fun()
            curr_ver = new_ver


init -897 python:
    # if version number is None, we can assume this is a completely fresh game
    # as version number is not set until init level 10
    # This means that we should NOT run the data migration scripts
    # NOTE: this also may mean the user is from 0.3.0, but data is too old by
    #   that point.
    if persistent.version_number is None:
        persistent._mas_dm_data_version = store._mas_dm_dm.dm_data_version

    elif persistent._mas_dm_data_version is None:
        persistent._mas_dm_data_version = store._mas_dm_dm._determine_version()

    if persistent._mas_dm_data_version != store._mas_dm_dm.dm_data_version:
        store._mas_dm_dm.run(
            persistent._mas_dm_data_version,
            store._mas_dm_dm.dm_data_version
        )

        # NOTE: this should be the last thing we do
        persistent._mas_dm_data_version = store._mas_dm_dm.dm_data_version
