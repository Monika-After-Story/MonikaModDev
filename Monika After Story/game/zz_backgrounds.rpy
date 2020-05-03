#Here's where we store our background data
default persistent._mas_background_MBGdata = {}

#START: Class definition
init -10 python:

    class MASBackgroundFilter(object):
        """
        Represntation of a filter for a MASBackground.
        this is related to the sprite filters, but gives each filter extra
        oomph. 

        BG filters are designed to be flexible to work with BGs.
        See the MASBackgroundFilterManager for more info on how this works.

        PROPERTIES:
            name - the name of this filter. This should be a filter ENUM.
                NOTE: this not checked until init level 0
            minlength - the amount of time in seconds that this filter must
                be able to be used for it to be shown. If the filter cannot be
                shown for this amount of time, it will not be shown at all.
            priority - the priority of this filter object. Lower number means
                higher priority. Lower priority means filter will be removed
                first.
            flt - the filter (imagematrix) objects to use. OPTIONAL.
                if this is None, it is assumed the filter data is handled
                elsewhere.
        """

        def __init__(self, name, minlength, priority=10, flt=None):
            """
            Constructor

            IN:
                name - name of the filter. This is NOT checked against filter
                    ENUMS until init level 0.
                minlength - amount of time in seconds that this filter must
                    be at least shown for.
                priority - priority of this filter object. Lower number means
                    higher priority.
                    (Default: 10)
                flt - imagemanip/matrix compatible filter to use. 
                    only pass in if you wish to use the `add_to_filters` 
                    function
                    (Default: None)
            """
            self.name = name
            self.minlength = minlength
            self.priority = priority
            self.flt = flt

        def add_to_filters(self):
            """
            Adds this filter to the filters dict. Wil fail and log if used
            after init level -1.
            Only works if self.flt is not None.
            """
            if self.flt is not None:
                store.mas_sprites.add_filter(self.name, self.flt)

        def can_fit(self, seconds):
            """
            Checks if this filter can fit in the time allotted

            IN:
                seconds - number of seconds to check

            RETURNS: True if this filter can fit in the given number of seconds
                FAlse if not
            """
            return self.minlength <= seconds

        def can_fit_td(self, td):
            """
            Checks if the filter can fit in the time allotted

            IN:
                td - timedelta object to check

            RETURNS: True if this filter can fit in the given timedelta,
                False if not
            """
            return self.minlength <= int(td.total_seconds())

        def verify(self):
            """
            Verifies if this filter's name is a valid filter. Call this
            after init level -1.

            RETURNS: True if filter is valid, False if not
            """
            return store.mas_sprites.is_filter(self.name)


    class MASBackgroundFilterManager(object):
        """
        Filter Management class for backgrounds

        The BG filter system slices a day into a set of ranges for a filter
        to be used on. The ranges done in a way where slices are intelligently
        picked depending on the suntimes. This allows for handling of cases
        where there isn't enough time for each slice to exist.

        Each slice is a MASBackgroundFilter object that has a minlength. That
        minimum length is used to determine if an object can fit in its 
        allocated time slice. Priorities of each object is used to determine
        which slices to keep. By default we try to keep every slice we can.

        Slices are defined by a datetime.time to change to the that filter.
        Slices start at midnight, which is the base slice. This slice by
        default will always take priority over any other slice.

        Code can be ran during a filter change by passing in function to 
        appropriate param. Any exceptions are caught and loggged.

        PROPERTIES:
            None
        """

        def __init__(self, mn_flt, *slices, pp=None):
            """
            Constructor

            IN:
                mn_flt - the base (midnight) filter. priority here is ignored,
                    defaulting to the highest priority.
                *slices - slice arguments. There should be an even number of
                    these. Each slice is a set of two args:
                        - 1st arg should be a datetime.time
                            (any duplicate times will override existing data
                            and will be logged)
                        - 2nd arg should be a MASBackgroundFilter
                pp - progpoint to run on a filter change (or slice change)
                    the following args are passed to the progpoint:
                        flt_old - the outgoing filter 
                        flt_new - the incoming filter 
                        curr_time - the current time
                    (Default: None)
            """
            if not isinstance(mn_flt, MASBackgroundFilter):
                raise Exception("Expected MASBackgroundFilter object")

            self._mn_flt = mn_flt
            # base filter

            self._times = {}
            # times associatd to filter objects
            # key: datetime.time object
            # value: filter associated with the object

            self._slices = []
            # times in proper sorted order

            self._eff_slices = []
            # times that we actually are using in proper sorted order

            self._pp = pp
            # progpoint

            self._index = 0
            # the index in eff_slices of the last filter change

            self._parse_slices(slices)

        def build(self, sunrise, sunset):
            """
            Builds the effective slices array using the given suntimes as 
            guidance.

            slices are built in a greedy fashion starting from midnight.

            IN:
                sunrise - time for sunrise as number of minutes from midnight
                sunset - time for sunset as number of minutes from midnight
            """
            # TODO: i need to know if a filter should be day or night!


        def filters(self):
            """
            RETURNS: list of all the filters associatd with this filter manager
                (list of strings)
            """
            # use a dict so we only return each filter once
            filters = {}
            for bg_flt in self_times.itervalues():
                filters[bg_flt.name] = None
            filters[self._mn_flt.name] = None

            return filters.keys()

        def _parse_slices(self, slices):
            """
            Parses the slices data
            """
            # verify slices
            if len(slices) % 2 != 0:
                raise Exception("slice count should be even")

            for change_time, bg_flt in zip(slices[0::2], slices[1::2]):
                if not isinstance(change_time, datetime.time):
                    raise Exception("Expected datetime.time object")
                if not isinstance(bg_flt, MASBackgroundFilter):
                    raise Exception("Expected MASBackgroundFilter object")

                # add to times and slices
                self._times[change_time] = bg_flt
                store.mas_utils.insert_sort_keyless(self._slices, change_time)


    # TODO: the background class needs to decide the filters to use.
    #   *AS WELL AS THE PROGRESSION*
    # TODO: move the current DAY/NIGHT filters from mas_sprites to here.
    # NOTE: I will do this when adding sunset progression
    class MASBackground(object):
        """
        Background class to get display props for bgs

        PROPERTIES:
            background_id - the id which defines this bg
            prompt - button label for the bg
            image_map - Dict mapping all images for the bgs, keys are precip types (See MASWeather)
            hide_calendar - whether or not we display the calendar with this
            hide_masks - whether or not we display the window masks
            disable_progressive - weather or not we disable progesssive weather
            unlocked - whether or not this background is unlocked
            entry_pp - entry programming points for bgs
            exit_pp - exit programming points
            filters - mapping of filters associated with this BG
        """
        import store.mas_background as mas_background
        import store.mas_weather as mas_weather

        def __init__(
            self,
            background_id,
            prompt,
            image_day,
            image_night,
            image_rain_day=None,
            image_rain_night=None,
            image_overcast_day=None,
            image_overcast_night=None,
            image_snow_day=None,
            image_snow_night=None,
            hide_calendar=False,
            hide_masks=False,
            disable_progressive=None,
            unlocked=False,
            entry_pp=None,
            exit_pp=None,
        ):
            """
            Constructor for background objects

            IN:
                background_id:
                    id that defines the background object
                    NOTE: Must be unique

                prompt:
                    button label for this bg

                image_day:
                    the renpy.image object we use for this bg during the day
                    NOTE: Mandatory

                image_night:
                    the renpy.image object we use for this bg during the night
                    NOTE: Mandatory

                image_rain_day:
                    the image tag we use for the background while it's raining (day)
                    (Default: None, not required)

                image_rain_night:
                    the image tag we use for the background while it's raining (night)
                    (Default: None, not required)

                image_overcast_day:
                    the image tag we use for the background while it's overcast (day)
                    (Default: None, not required)

                image_overcast_night:
                    the image tag we use for the background while it's overcast (night)
                    (Default: None, not required)

                image_snow_day:
                    the image tag we use for the background while it's snowing (day)
                    (Default: None, not required)

                image_snow_night:
                    the image tag we use for the background while it's snowing (night)
                    (Default: None, not required)

                hide_calendar:
                    whether or not we want to display the calendar
                    (Default: False)

                hide_masks:
                    weather or not we want to show the windows
                    (Default: False)

                disable_progressive:
                    weather or not we want to disable progressive weather
                    (Default: None, if hide masks is true and this is not provided, we assume True, otherwise False)

                unlocked:
                    whether or not this background starts unlocked
                    (Default: False)

                entry_pp:
                    Entry programming point for the background
                    (Default: None)

                exit_pp:
                    Exit programming point for this background
                    (Default: None)
            """

            if background_id in self.mas_background.BACKGROUND_MAP:
                raise Exception("duplicate background ID")

            self.background_id = background_id
            self.prompt = prompt
            self.image_day = image_day
            self.image_night = image_night


            self.image_map = {
                #Def
                mas_weather.PRECIP_TYPE_DEF: (image_day, image_night),
                #Rain
                mas_weather.PRECIP_TYPE_RAIN: (image_rain_day if image_rain_day else image_day, image_rain_night if image_rain_night else image_night),
                #Overcast
                mas_weather.PRECIP_TYPE_OVERCAST: (image_overcast_day if image_overcast_day else image_day, image_overcast_night if image_overcast_night else image_night),
                #Snow
                mas_weather.PRECIP_TYPE_SNOW: (image_snow_day if image_snow_day else image_day, image_snow_night if image_snow_night else image_night)
            }

            #Then the other props
            self.hide_calendar = hide_calendar
            self.hide_masks = hide_masks

            #Progressive handling
            if disable_progressive is None:
                self.disable_progressive = hide_masks
            else:
                self.disable_progressive = disable_progressive

            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp

            # add to background map
            self.mas_background.BACKGROUND_MAP[background_id] = self


        def __eq__(self, other):
            if isinstance(other, MASBackground):
                return self.background_id == other.background_id
            return NotImplemented


        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result


        def entry(self, old_background):
            """
            Run the entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_background)


        def exit(self, new_background):
            """
            Run the exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_background)


        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]


        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)

        def getDayRoom(self, weather=None):
            """
            Returns the day masks to use given the conditions/availablity of present assets
            """
            if weather is None:
                weather = store.mas_current_weather

            return self.image_map[weather.precip_type][0]

        def getNightRoom(self, weather=None):
            """
            Returns the night masks to use given the conditions/availablity of present assets
            """
            if weather is None:
                weather = store.mas_current_weather

            return self.image_map[weather.precip_type][1]

        def getRoomForTime(self, weather=None):
            """
            Gets the room for the current time

            IN:
                weather - get the room bg for the time and weather
                (Default: current weather)
            """
            if weather is None:
                weather = store.mas_current_weather
            if store.mas_isMorning():
                return self.getDayRoom(weather)
            return self.getNightRoom(weather)

        def isChangingRoom(self, old_weather, new_weather):
            """
            If the room has a different look for the new weather we're going into, the room is "changing" and we need to flag this to
            scene change and dissolve the spaceroom in the spaceroom label
            """
            return self.getRoomForTime(old_weather) != self.getRoomForTime(new_weather)

        def isFltDay(self, flt=None):
            """
            Checks if the given filter is considered a "day" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "day" filter according to this bg
            """
            # TODO: a BG will be in charge of which filters are "day" and
            #   which are "night". This will be implemented in the future.
            #   for now we just assume "day" is day and "night" is night
            if flt is None:
                flt = store.mas_sprites.get_filter()

            return flt == store.mas_sprites.FLT_DAY

        def isFltNight(self, flt=None):
            """
            Checks if the given filter is considered a "night" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "night" filter according to this BG
            """
            # TODO: see isFltDay
            return not self.isFltDay(flt)


#Helper methods and such
init -20 python in mas_background:
    import store
    BACKGROUND_MAP = {}
    BACKGROUND_RETURN = "Nevermind"

    def loadMBGData():
        """
        Loads persistent MASBackground data into the weather map

        ASSUMES: background map is already filled
        """
        if store.persistent._mas_background_MBGdata is None:
            return

        for mbg_id, mbg_data in store.persistent._mas_background_MBGdata.iteritems():
            mbg_obj = BACKGROUND_MAP.get(mbg_id, None)
            if mbg_obj is not None:
                mbg_obj.fromTuple(mbg_data)

    def saveMBGData():
        """
        Saves MASBackground data from weather map into persistent
        """
        for mbg_id, mbg_obj in BACKGROUND_MAP.iteritems():
            store.persistent._mas_background_MBGdata[mbg_id] = mbg_obj.toTuple()

    def getUnlockedBGCount():
        """
        Gets the number of unlocked backgrounds
        """
        unlocked_count = 0
        for mbg_obj in BACKGROUND_MAP.itervalues():
            unlocked_count += int(mbg_obj.unlocked)

        return unlocked_count

#START: BG change functions
init 800 python:

    def mas_setBackground(_background):
        """
        Sets the initial bg

        NOTE: We don't handle exit pp's here

        IN:
            _background:
                The background we're changing to
        """
        global mas_current_background
        old_background = mas_current_background
        mas_current_background = _background
        mas_current_background.entry(old_background)

    def mas_changeBackground(new_background, by_user=None):
        """
        changes the background w/o any scene changes

        IN:
            new_background:
                The background we're changing to

            by_user:
                If the user switched the background themselves
        """
        if by_user is not None:
            mas_background.force_background = bool(by_user)

        mas_current_background.exit(new_background)
        mas_setBackground(new_background)

    #Just set us to the normal room here
    mas_current_background = None
    mas_setBackground(mas_background_def)

    #Make sure the bg selector is only available with at least 2 bgs unlocked
    if mas_background.getUnlockedBGCount() < 2:
        mas_lockEVL("monika_change_background","EVE")

#START: Programming points
init -2 python in mas_background:
    import store

    def _def_background_entry(_old):
        """
        Entry programming point for befault background
        """
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

    def _def_background_exit(_new):
        """
        Exit programming point for befault background
        """
        store.mas_lockEVL("mas_monika_islands", "EVE")


#START: bg defs
init -1 python:
    #Default spaceroom
    mas_background_def = MASBackground(
        #Identification
        "spaceroom",
        "Spaceroom",

        #Day/Night
        "monika_day_room",
        "monika_room",

        #Rain Day/Night
        image_rain_day="monika_rain_room",

        image_overcast_day="monika_rain_room",

        image_snow_day="monika_snow_room_day",
        image_snow_night="monika_snow_room_night",

        #Def room should always be unlocked
        unlocked=True,

        #Programming points for the spaceroom
        entry_pp=store.mas_background._def_background_entry,
        exit_pp=store.mas_background._def_background_exit
    )


#START: Image definitions
#Spaceroom
image monika_day_room = "mod_assets/location/spaceroom/spaceroom.png"
image monika_room = "mod_assets/location/spaceroom/spaceroom-n.png"
#Thanks Orca
image monika_rain_room = "mod_assets/location/spaceroom/spaceroom_rain.png"
#Thanks Velius/Orca
image monika_snow_room_day = "mod_assets/location/spaceroom/spaceroom_snow.png"
image monika_snow_room_night = "mod_assets/location/spaceroom/spaceroom_snow-n.png"

#TODO: locking/unlocking of this based on other backgrounds
#START: Location Selector
#init 5 python:
#    # available only if moni affection is affectionate+
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_change_background",
#            category=["location"],
#            prompt="Can we go somewhere else?",
#            pool=True,
#            unlocked=False,
#            rules={"no unlock": None},
#            aff_range=(mas_aff.AFFECTIONATE, None)
#        )
#    )

label monika_change_background:

    m 1hua "Sure!"

label monika_change_background_loop:

    show monika 1eua at t21

    $ renpy.say(m, "Where would you like to go?", interact=False)

    python:
        # build menu list
        import store.mas_background as mas_background
        import store.mas_moods as mas_moods

        # we assume that we will always have more than 1
        # default should always be at the top
        backgrounds = [(mas_background_def.prompt, mas_background_def, False, False)]

        # build other backgrounds list
        other_backgrounds = [
            (mbg_obj.prompt, mbg_obj, False, False)
            for mbg_id, mbg_obj in mas_background.BACKGROUND_MAP.iteritems()
            if mbg_id != "spaceroom" and mbg_obj.unlocked
        ]

        # sort other backgrounds list
        other_backgrounds.sort()

        # build full list
        backgrounds.extend(other_backgrounds)

        # now add final quit item
        final_item = (mas_background.BACKGROUND_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(backgrounds, mas_ui.SCROLLABLE_MENU_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    $ sel_background = _return

    show monika at t11

    # return value False? then return
    if sel_background is False:
        m 1eka "Oh, alright."
        m "If you want to go somewhere, just ask, okay?"
        return

    if sel_background == mas_current_background:
        m 1hua "We're here right now, silly."
        m "Try again~"
        jump monika_change_background_loop

    call mas_background_change(sel_background)
    return

#Generic background changing label, can be used if we wanted a sort of story related change
label mas_background_change(new_bg, skip_leadin=False, skip_outro=False):
    # otherwise, we can change the background now
    if not skip_leadin:
        m 1eua "Alright!"
        m 1hua "Let's go, [player]!"

    #Little transition
    hide monika
    scene black
    with dissolve
    pause 2.0

    # finally change the background
    $ mas_changeBackground(new_bg)

    #If we've disabled progressive and hidden masks, then we shouldn't allow weather change
    if new_bg.disable_progressive and new_bg.hide_masks:
        $ mas_weather.temp_weather_storage = mas_current_weather
        $ mas_changeWeather(mas_weather_def)
        $ mas_lockEVL("monika_change_weather", "EVE")

    else:
        if mas_weather.temp_weather_storage is not None:
            $ mas_changeWeather(mas_weather.temp_weather_storage)

        else:
            #If we don't have tempstor, run the startup weather
            $ set_to_weather = mas_shouldRain()
            if set_to_weather is not None:
                $ mas_changeWeather(set_to_weather)
            else:
                $ mas_changeWeather(mas_weather_def)

        #Then we unlock the weather sel here
        $ mas_unlockEVL("monika_change_weather", "EVE")

    call spaceroom(scene_change=True, dissolve_all=True)

    if not skip_outro:
        m 1eua "Here we are!"
        m "Let me know if you want to go somewhere else, okay?"
    return
