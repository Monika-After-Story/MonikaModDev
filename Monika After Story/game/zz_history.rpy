# Historical data module
#
# How this works:
#   Historical data is persistent data over time. 
#
# ORGANIZED:
#   dicts of dicts:
#   <year> : <subdict>
#       year - just the 4/5 digit year (2018, 2017, and so on)
#       subdict - as follows:
#           <data key> : <data value>
#               data key - key to identify this data. See below for layout
#               data value - value to save
#
# DATA KEY LAYOUT:
#   data keys need to follow a structure so we can ensure uniqueness:
#   <topic category>.<sub category>.<sub sub category>.<name>
#   EX: o31.activity.tricktreat.went_outside
#   topic category - main topic category
#       o31 - halloween
#       d25 - chms
#       922 - monika bday
#       player_bday - player bday
#       pm - player model 
#       and so on
#   sub category - fine tuned category if needed
#       Use BASE if not needed
#   sub sub category - even more fine tuned category if needed
#       Use BASE if not needed
#   name - variable name. this should be pretty descriptive
#       
# MAPPING
#   Data saving is done by mapping a persistent variable name (as string) to
#   the data key (as string).
#   NOTE: we do NOT just use the persistent variable name as data key in the
#       event that we wnat to save a non-persistent variable.
#
# MAPPING STORAGE
#   New class called MASHistorySaver, contains a datetime and a mapping, 
#   as well as the callbacks/programming points for a mapping.
#   Also contains an ID for uniqueness. We use that ID in saving data.
#
#   The datetime determines the next time the mapping is saved. This will be
#   auto adjusted to the next year. We also scan through datetimes and fix
#   times that are beyond 1 year ahead (in the case of time traveling)
#
#   MASHistorySaver data is saved into a dict of tuples. We use the ID for key.
#
# CALLBACKS:
#   When data mapping is done, there is option to run entry/exit programming
#   points. Not sure if this is really helpful but we'll see.
#
# RUN:
#   All MASHistorySaver objects are checked at init -800. This is designed to 
#   be run after persistent backup system is run, but before lots of other
#   things.
#   The datetimes of each object are checked and if the current date is
#   past this datetime we run the data save. This uses the mapping to save
#   appropriate data into the historical dict.
#
#   All persistent variables that were saved are then set to None. This preps
#   them for default values later in the pipeline
#
# STORAGE:
#   all historical data is saved in `persistent._mas_history_archives`
#   access is given via public functions. DO NOT ACCESS DIRECTLY
#
#   MASHistorySaver object data is stored in `persistent._mas_history_mhs_data`
#   NEVER ACCESS THIS IN RUNTIME
#   
#   MASHistorySaver objects are created on start and stored in `mhs_db`
#   Access is given via public functions. DO NOT ACCESS DIRECTLY

init -860 python in mas_history:
    import store
    import datetime

    ### initialize the archives
    if store.persistent._mas_history_archives is None:
        store.persistent._mas_history_archives = dict()

    # add all years up to today in the archives
    for year in range(2017, datetime.date.today().year + 1):
        if year not in store.persistent._mas_history_archives:
            store.persistent._mas_history_archives[year] = dict()
    ### END init

    ### MASHistorySaver data init
    if store.persistent._mas_history_mhs_data is None:
        store.persistent._mas_history_mhs_data = dict()
    ### END init

    mhs_db = dict()
    # MASHistorySaver objects database

    ### CONSTANTS

    ## lookup constants
    L_FOUND = 0
    # we FOUND data for the year + key in the archives

    L_NO_YEAR = 1
    # we did not find the year in the archives

    L_NO_KEY = 2
    # we did not find the key in the archives (for the given year)

    ### archive functions:
    def lookup(key, year)
        """
        Looks up data in the historical archives.

        IN:
            key - data key to lookup
            year - year to look up data

        RETURNS: a tuple of the following format:
            [0]: Lookup constant 
            [1]: retrieved data (which may be None). This is always None if
                we could not find year or key
        """
        archives = store.persistent._mas_history_archives

        # get data from the year
        data_file = archives.get(year, None)
        if data_file is None:
            return (L_NO_YEAR, None)

        # otherwise year found! Check for key
        if key not in data_file:
            return (L_NO_KEY, None)

        # key is here, return data
        return (L_FOUND, data_file[key])


    def lookup_ot(key, *years)
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to lookup
            years - years to look up data

        RETURNS: SEE lookup_ot_l
        """
        return lookup_ot_l(key, years)


    def lookup_otl(key, years_list):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years_list - list of years to lookup data

        RETURNS: dict of the following format:
            year: tuple (SEE lookup)
        """
        found_data = dict()

        for year in years_list:
            found_data[year] = lookup(key, year)

        return found_data


    ### archive saving functions: (NOT PUBLIC)
    def _store(value, key, year):
        """
        Stores data in the historical archives.

        NOTE: will OVERWRITE data that already exists.

        IN:
            value - value to store
            key - data key to store value
            year - year to store value
        """
        store.persistent._mas_history_archives[year][key] = value


init -850 python:

    ## public archive functions
    def mas_HistLookup(key, year):
        """
        Looks up data in the historical archives.

        IN:
            key - data key to look up
            year - year to look up data

        RETURNS: a tuple of the following format:
            [0]: mas_history lookup constant
            [1]: retrieved data (which may be None). This is always None if
                we could not find year or key
        """
        return store.mas_history.lookup(key, year)


    def mas_HistLookup_ot(key, *years):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years - years to look updata

        RETURNS: dict of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(key, years)


    def mas_HistLookup_otl(key, years_list):
        """
        Looks up data overtime in the historical archives.

        IN:
            key - data key to look up
            years_list - list of years to lookup data

        RETURNS: dict of the following format:
            year: data tuple from mas_HistLookup
        """
        return store.mas_history.lookup_otl(key, years_list)


    ## MASHistorySaver stuff
    
    class MASHistorySaver(object):
        """
        Class designed to represent mapping of historial data that we need to
        save over certain intervals.

        PROPERTIES:
            mhs_id - identifier of this MASHistorySaver object
                NOTE: Must be unique
            trigger - datetime to trigger the saving
                NOTE: this is changed automatically when saving is done
                NOTE: the trigger's year is what we use to determine where to
                    save the historical data
            mapping - mapping of persistent variable names to historical data
                keys
            use_year_before - True means that when saving data, we should use
                trigger.year - 1 as the year to determine where to save
                historical data. This is mainly for year-end events like 
                d31 and new years
            entry_pp - programming point called before saving data
                self is passed to this
            exitpp - programming point called after saving data
                self is passed to this
        """
        import store.mas_history as mas_history

        def __init__(self, 
                mhs_id,
                trigger,
                mapping,
                use_year_before=False,
                entry_pp=None,
                exit_pp=None
            ):
            """
            Constructor

            Throws exception if mhs_id is NOT unique

            IN:
                mhs_id - identifier of this MASHistorySaver object
                    NOTE: Must be unique
                trigger - datetime of when to trigger data saving for this
                    NOTE: if the year of this datetime is 2 years ahead of the
                        current year, we reset this to 1 year ahead of the
                        current year.
                    NOTE: this is changed every time we execute the saveing
                        routine
                    NOTE: trigger.year is used when saving historical data
                mapping - mapping of the persistent variable names to 
                    historical data keys
                use_year_before - True will use trigger.year-1 when saving
                    historical data instead of trigger.year. 
                    (Default: False)
                entry_pp - programming point called before saving data
                    self is passed to this
                    (Default: None)
                exit_pp - programming point called after saving data
                    self is passed to this
                    (Default: None)
            """
            # sanity checks
            if mhs_id in self.mas_history.mhs_db:
                raise Exception(
                    "History object '{0}' already exists".format(mhs_id)
                )

            self.mhs_id = mhs_id
            self.setTrigger(trigger)  # use the set function for cleansing
            self.use_year_before = use_year_before
            self.mapping = mapping
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp

       
        @staticmethod
        def correctTriggerYear(_trigger):
            """
            Determines the correct year to set trigger to.

            A triggers with a correct year are basically triggers that have not
            passed yet. It's not as simple as increasing year since we have to
            account for triggers that have yet to execute this year.

            IN:
                _trigger - trigger we are trying to change

            RETURNS: _trigger with the correct year
            """
            current_date = datetime.date.today()
            _temp_trigger = _trigger.replace(year=current_date.year)

            if current_date > _temp_trigger:
                # trigger has already past, set the trigger for next year
                return _trigger.replace(year=current_date.year + 1)

            # trigger has NOT passed yet, set the trigger for this year
            return _temp_trigger


        def fromTuple(self, data_tuple):
            """
            Loads data from the data tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: datetime to set the trigger property
            """
            self.setTrigger(data_tuple[0])


        def setTrigger(self, _trigger):
            """
            Sets the trigger of this object. This function does cleansing of
            bad trigger dates.

            IN:
                _trigger - trigger to change to
            """
            current_date = datetime.date.today()
            if _trigger.year > (current_date.year + 1):
                # if the trigger year is at least 2 years beyond current, its
                # definitely a time travel issue.

                # but we need to determine if the trigger has already happend
                # in teh current year or will happen this year so we can 
                # both prevent overwrites and save data when we need to.
                self.trigger = MASHistorySaver.correctTriggerYear(_trigger)

            else:
                # otherwise, no issues with the new trigger
                self.trigger = _trigger


        def save(self):
            """
            Runs the saving routine

            NOTE: does NOT check trigger.

            NOTE: will CHANGE trigger
            """
            if self.entry_pp is not None:
                self.entry_pp(self)

            # now to actually save
            source = persistent.__dict__
            dest = self.mas_history
            save_year = self.trigger.year

            # go through mapping and save data
            for p_key in self.mapping:
                p_data = source.get(p_key, None)
                dest._store(p_data, self.mapping[p_key], save_year)

            # change trigger year
            self.trigger = MASHistorySaver.correctTriggerYear(self.trigger)

            if self.exit_pp is not None:
                self.exit_pp(self)


        def toTuple(self):
            """
            Converts this MASHistorySaver object into a tuple

            RETURNS tuple of the following format:
                [0]: trigger - the trigger property of this object
            """
            return (self.trigger,)
