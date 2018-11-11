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
#   <topic category>.<sub category>.<sub sub category>...<name>
#   EX: o31.activity.tricktreat.went_outside
#   topic category - main topic category
#       o31 - halloween
#       d25 - chms
#       922 - monika bday
#       player_bday - player bday
#       pm - player model 
#       and so on
#   sub category - fine tuned category if needed
#   sub sub category - even more fine tuned category if needed
#   ...
#   name - variable name. this should be pretty descriptive
#   
#   You don't need to use the sub categories if you dont need them.
#   However, topic category is REQUIRED
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
#
# CREATION:
#   All MASHistorySaver objects should be created before init level -800.
#   Tuple persistent data is loaded at -800, then the algorithms are ran.

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
    def lookup(key, year):
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


    def lookup_ot(key, *years):
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


    ### history saver data save/load
    def loadMHSData():
        """
        Loads persistent MASHistorySaver data into the mhs_db

        ASSUMES: the mhs database is already filled
        """
        for mhs_id, mhs_data in store.persistent._mas_history_mhs_data.iteritems():
            mhs = mhs_db.get(mhs_id, None)
            if mhs is not None:
                mhs.fromTuple(mhs_data)


    def saveMHSData():
        """
        Saves MASHistorySaver data from mhs_db into persistent
        """
        for mhs_id, mhs in mhs_db.iteritems():
            store.persistent._mas_history_mhs_data[mhs_id] = mhs.toTuple()


    ### mhs_db functions
    def addMHS(mhs):
        """
        Adds the given mhs to the database.

        IN:
            mhs - MASHistorySaver object to add
        
        ASSUMES that the given mhs does not conflict with existing
        """
        mhs_db[mhs.id] = mhs


    def getMHS(mhs_id):
        """
        Gets the MASHistorySaver object with the given id

        IN:
            mhs_id - id of the MASHistorySaver object to get

        RETURNS: MASHistorySaver object, or None if not found
        """
        return mhs_db.get(mhs_id, None)


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


    def mas_HistVerify(key, _verify, *years):
        """
        Verifies if data at the given key matches the verification value.

        IN:
            key - data key to lookup
            _verify - the data we want to match to
            years - years to look up data (as args)
                Dont pass in anything if you want to lookup all years since
                2017

        RETURNS: tuple of the following format:
            [0]: true/False if we found data that matched the verification
            [1]: list of years that matched the verification
        """
        if len(years) == 0:
            years = range(2017, datetime.date.today().year+1)

        found_data = mas_HistLookup_otl(key, years)
        years_found = []

        for year, data_tuple in found_data.iteritems():
            status, _data = data_tuple
            
            if status == store.mas_history.L_FOUND and _data == _verify:
                years_found.append(year)

        return (len(years_found) > 0, years_found)


    ## MASHistorySaver stuff
    
    class MASHistorySaver(object):
        """
        Class designed to represent mapping of historial data that we need to
        save over certain intervals.

        PROPERTIES:
            id - identifier of this MASHistorySaver object
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
            dont_reset - True means we do NOT reset the persistent var
                when doing the save.
            entry_pp - programming point called before saving data
                self is passed to this
            exitpp - programming point called after saving data
                self is passed to this
            trigger_pp - programming point called to update trigger with
                instead of the default year+1
        """
        import store.mas_history as mas_history

        # also setup first session as a static variable
        first_sesh = -1

        def __init__(self, 
                mhs_id,
                trigger,
                mapping,
                use_year_before=False,
                dont_reset=False,
                entry_pp=None,
                exit_pp=None,
                trigger_pp=None
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
                dont_reset - True will NOT reset the persistent var after
                    saving.
                    (Default: False)
                entry_pp - programming point called before saving data
                    self is passed to this
                    (Default: None)
                exit_pp - programming point called after saving data
                    self is passed to this
                    (Default: None)
                trigger_pp - if not None, this pp is called with the current
                    trigger when updating trigger, and the returned datetime 
                    is used as the new trigger.
                    (Default: None)
            """
            # sanity checks
            if mhs_id in self.mas_history.mhs_db:
                raise Exception(
                    "History object '{0}' already exists".format(mhs_id)
                )
            # init first sesh
            if MASHistorySaver.first_sesh == -1:
                if persistent.sessions is not None:
                    MASHistorySaver.first_sesh = persistent.sessions.get(
                        "first_session",
                        None
                    )

                else:
                    MASHistorySaver.first_sesh = None

            self.id = mhs_id
            self.setTrigger(trigger)  # use the set function for cleansing
            self.use_year_before = use_year_before
            self.mapping = mapping
            self.dont_reset = dont_reset
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            self.trigger_pp = trigger_pp

       
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
            _now = datetime.datetime.now()
            _temp_trigger = _trigger.replace(year=_now.year)

            if _now > _temp_trigger:
                # trigger has already past, set the trigger for next year
                return _trigger.replace(year=_now.year + 1)

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
            _now = datetime.datetime.now()

            # grab first sesh
            # if we do not have a first sesh, then assume today is first
            # sessions
            first_sesh = MASHistorySaver.first_sesh
            if first_sesh is None:
                first_sesh = _now

            if (
                    _trigger.year > (_now.year + 1)
                    or _trigger <= first_sesh
                ):
                # if the trigger year is at least 2 years beyond current, its
                # definitely a time travel issue.
                #
                # or if the trigger is before or same date as the first session
                # then we should move it into the future

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

            if self.use_year_before:
                save_year -= 1

            # go through mapping and save data
            for p_key, data_key in self.mapping.iteritems():

                # retrieve and save
                dest._store(source.get(p_key, None), data_key, save_year)

                # reset
                if not self.dont_reset:
                    source[p_key] = None

            # update trigger
            if self.trigger_pp is not None:
                self.trigger = self.trigger_pp(self.trigger)

            else:
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


init -800 python in mas_history:
    # and now we run the MASHistorySaver algorithms

    def _runMHSAlg():
        """
        Runs the historical data saving algorithm

        ASSUMES:
            - mhs_db is filled with MASHistorySaver objects 
        """
        # now we go through the mhs_db and run their save algs if their trigger
        # is past today.
        _now = datetime.datetime.now()
        
        for mhs in mhs_db.itervalues():
            # trigger rules:
            #   current date must be past trigger
            if mhs.trigger <= _now:
                mhs.save()

    # first, we need to load existing MHS data
    loadMHSData()

    # now run the algorithm
    _runMHSAlg()

    # save trigger data
    saveMHSData()


init -816 python in mas_delact:
    ## need a place to define DelayedAction callbacks? do it here I guess.
    nothing = "temp"


init -815 python in mas_history:
    ## Need a place define callbacks/programming points? Do it here I guess.
    from store.mas_delact import _MDA_safeadd

    # BDAY
    def _bday_exit_pp(mhs):
        # this PP will just add the appropriate delayed action IDs to the 
        # persistent delayed action list.
        _MDA_safeadd(3, 4, 5, 6, 7)


init -810 python:
    ## Add MASHistorySaver objects here. 
    ## NOTE: If you've declared all the persistent variables you want to use
    ##  in one file, its better to create your MASHistorySaver object there.
    ##
    ## Use this python block in case you made persistent variables in various
    ## locations

    # PLAYER MODEL
    # NOTE: because player model variables are used basically everywhere, 
    #   rather than make a ton of player model MHS objects, lets just make a 
    #   generic one that runs on jan 1 of every year.
    #
    # Sub cats:
    #   lifestyle - what you do
    #   emotions - emotional/mental states
    #   family - family related stuff
    #   actions - what you have done
    #   location - location-based stuff
    #   likes - likes/wants
    #   know - knowledge
    store.mas_history.addMHS(MASHistorySaver(
        "pm",
        datetime.datetime(2019, 1, 1),
        {
            # lifestyles (of the rich and famous)
            "_mas_pm_religious": "pm.lifestyle.religious",
            "_mas_pm_like_playing_sports": "pm.lifestyle.plays_sports",
            "_mas_pm_meditates": "pm.lifestyle.meditates",
            "_mas_pm_see_therapist": "pm.lifestyle.sees_therapist",

            # lifestyle / ring
            "_mas_pm_wearsRing": "pm.lifestyle.ring.wears_one",

            # lifestyle / music
            "_mas_pm_play_jazz": "pm.lifestyle.music.play_jazz",

            # lifestyle / smoking
            "_mas_pm_do_smoke": "pm.lifestyle.smoking.smokes",
            "_mas_pm_do_smoke_quit": "pm.lifestyle.smoking.trying_to_quit",

            # lifestyle / food
            "_mas_pm_eat_fast_food": "pm.lifestyle.food.eats_fast_food",

            # emotions
            "_mas_pm_love_yourself": "pm.emotions.love_self",

            # family
            "_mas_pm_have_fam": "pm.family.have_family",
            "_mas_pm_have_fam_sibs": "pm.family.have_siblings",
            "_mas_pm_no_fam_bother": "pm.family.bothers_you",
            "_mas_pm_have_fam_mess": "pm.family.is_mess",
            "_mas_pm_have_fam_mess_better": "pm.family.will_get_better",
            "_mas_pm_no_talk_fam": "pm.family.no_talk_about",
            "_mas_pm_fam_like_monika": "pm.family.likes_monika",

            # actions
            "_mas_pm_drawn_art": "pm.actions.drawn_art",

            # actions / prom
            "_mas_pm_gone_to_prom": "pm.actions.prom.went",
            "_mas_pm_prom_good": "pm.actions.prom.good",
            "_mas_pm_had_prom_date": "pm.actions.prom.had_date",
            "_mas_pm_prom_monika": "pm.actions.prom.wanted_monika",
            "_mas_pm_prom_not_interested": "pm.actions.prom.no_interest",
            "_mas_pm_prom_shy": "pm.actions.prom.too_shy",
            "_mas_pm_no_prom": "pm.actions.prom.no_prom",

            # actions / books
            "_mas_pm_read_yellow_wp": "pm.actions.books.read_yellow_wp",

            # actions / mas / music
            "_mas_pm_added_custom_bgm": "pm.actions.mas.music.added_custom_bgm",

            # actions / mas / zoom
            "_mas_pm_zoomed_out": "pm.actions.mas.zoom.out",
            "_mas_pm_zoomed_in": "pm.actions.mas.zoom.in",
            "_mas_pm_zoomed_in_max": "pm.actions.mas.zoom.in_max",

            # location
            "_mas_pm_live_in_city": "pm.location.live_in_city",
            "_mas_pm_live_near_beach": "pm.location.live_near_beach",

            # likes
            "_mas_pm_likes_horror": "pm.likes.horror",
            "_mas_pm_likes_spoops": "pm.likes.spooks",
            "_mas_pm_watch_mangime": "pm.likes.manga_and_anime",

            # likes / monika
            "_mas_pm_a_hater": "pm.likes.monika.not",

            # likes / music
            "_mas_pm_like_rap": "pm.likes.music.rap",
            "_mas_pm_like_vocaloids": "pm.likes.music.vocaloids",
            "_mas_pm_like_rock_n_roll": "pm.likes.music.rock_n_roll",
            "_mas_pm_like_orchestral_music": "pm.likes.music.orchestral",
            "_mas_pm_like_jazz": "pm.likes.music.jazz",
            "_mas_pm_like_other_music": "pm.likes.music.other",

            # likes / food
            "_mas_pm_like_mint_ice_cream": "pm.likes.food.mint_ice_cream",

            # likes / clothes
            "_mas_pm_likes_panties": "pm.likes.clothes.panties",
            "_mas_pm_no_talk_panties": "pm.likes.clothes.panties.no_talk",

            # knowledge
            # knowledge / lang
            "_mas_pm_lang_other": "pm.know.lang.other",
            "_mas_pm_lang_jpn": "pm.know.lang.jpn"
        },
        use_year_before=True,
        dont_reset=True
    ))

    # BDAY
    # NOTE: kind of wish I put all the bday variables together. Since they are
    #   not together, they will be here.
    store.mas_history.addMHS(MASHistorySaver(
        "922",
        datetime.datetime(2018, 9, 30),
        {
            "_mas_bday_opened_game": "922.actions.opened_game",
            "_mas_bday_no_time_spent": "922.actions.no_time_spent",
            "_mas_bday_no_recognize": "922.actions.no_recognize",
            "_mas_bday_said_happybday": "922.actions.said_happybday",
            "_mas_bday_date_count": "922.actions.date.count",
            "_mas_bday_date_affection_lost": "922.actions.date.aff_lost",
            "_mas_bday_date_affection_gained": "922.actions.date.aff_gained",
            "_mas_bday_sbp_aff_given": "922.actions.surprise.aff_given",
            "_mas_bday_sbp_reacted": "922.actions.surprise.reacted",
            "_mas_bday_sbp_found_cake": "922.actions.surprise.found_cake",
            "_mas_bday_sbp_found_banners": "922.actions.surprise.found_banners",
            "_mas_bday_sbp_found_balloons": "922.actions.surprise.found_balloons"
        },
        exit_pp=store.mas_history._bday_exit_pp
    ))

