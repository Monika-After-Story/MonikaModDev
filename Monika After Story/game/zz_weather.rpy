#Stores the last weather the player had chosen
#Default: "auto"
default persistent._mas_current_weather = "auto"

### spaceroom weather art
#Big thanks to Legendkiller21/Orca/Velius for helping out with these
image def_weather = MASFallbackFilterDisplayable(
    day=Movie(
        channel="window_1",
        play="mod_assets/window/def_day_mask.mp4",
        mask=None
    ),
    sunset=Movie(
        play="mod_assets/window/def_sunset_mask.mp4",
        mask=None
    ),
    night=Movie(
        channel="window_2",
        play="mod_assets/window/def_night_mask.mp4",
        mask=None
    )
)
image def_weather_fb = MASFallbackFilterDisplayable(
    day="mod_assets/window/def_day_mask_fb.png",
    sunset="mod_assets/window/def_sunset_mask_fb.png",
    night="mod_assets/window/def_night_mask_fb.png",
)

image rain_weather = MASFallbackFilterDisplayable(
    day=Movie(
        channel="window_3",
        play="mod_assets/window/rain_day_mask.mpg",
        mask=None
    ),
    night=Movie(
        channel="window_4",
        play="mod_assets/window/rain_night_mask.mpg",
        mask=None
    )
)
image rain_weather_fb = MASFallbackFilterDisplayable(
    day="mod_assets/window/rain_day_mask_fb.png",
    night="mod_assets/window/rain_night_mask_fb.png",
)

image overcast_weather = MASFallbackFilterDisplayable(
    day=Movie(
        channel="window_5",
        play="mod_assets/window/overcast_day_mask.mpg",
        mask=None
    ),
    night=Movie(
        channel="window_6",
        play="mod_assets/window/overcast_night_mask.mpg",
        mask=None
    ),
)
image overcast_weather_fb = MASFallbackFilterDisplayable(
    day="mod_assets/window/overcast_day_mask_fb.png",
    night="mod_assets/window/overcast_night_mask_fb.png",
)

image snow_weather = MASFallbackFilterDisplayable(
    day=Movie(
        channel="window_7",
        play="mod_assets/window/snow_day_mask.mp4",
        mask=None
    ),
    sunset=Movie(
        play="mod_assets/window/snow_sunset_mask.mp4",
        mask=None
    ),
    night=Movie(
        channel="window_8",
        play="mod_assets/window/snow_night_mask.mp4",
        mask=None
    ),
)
image snow_weather_fb = MASFallbackFilterDisplayable(
    day="mod_assets/window/snow_day_mask_fb.png",
    sunset="mod_assets/window/snow_sunset_mask_fb.png",
    night="mod_assets/window/snow_night_mask_fb.png",
)

## end spaceroom weather art

## living room weather art

## end living room weather art

## start island bg weather art

image mas_island_frame_day = "mod_assets/location/special/with_frame.png"
image mas_island_day = "mod_assets/location/special/without_frame.png"
image mas_island_frame_night = "mod_assets/location/special/night_with_frame.png"
image mas_island_night = "mod_assets/location/special/night_without_frame.png"
image mas_island_frame_rain = "mod_assets/location/special/rain_with_frame.png"
image mas_island_rain = "mod_assets/location/special/rain_without_frame.png"
image mas_island_frame_rain_night = "mod_assets/location/special/night_rain_with_frame.png"
image mas_island_rain_night = "mod_assets/location/special/night_rain_without_frame.png"
image mas_island_frame_overcast = "mod_assets/location/special/overcast_with_frame.png"
image mas_island_overcast = "mod_assets/location/special/overcast_without_frame.png"
image mas_island_frame_overcast_night = "mod_assets/location/special/night_overcast_with_frame.png"
image mas_island_overcast_night = "mod_assets/location/special/night_overcast_without_frame.png"
image mas_island_frame_snow = "mod_assets/location/special/snow_with_frame.png"
image mas_island_snow = "mod_assets/location/special/snow_without_frame.png"
image mas_island_frame_snow_night = "mod_assets/location/special/night_snow_with_frame.png"
image mas_island_snow_night = "mod_assets/location/special/night_snow_without_frame.png"

## end island bg weather art

# NOTE: might not use these
#default persistent._mas_weather_snow_happened = False
#default persistent._mas_weather_rain_happened = False

default persistent._mas_weather_MWdata = {}
# stores locked/unlocked status for weather

#When did we last check if it could rain
default persistent._mas_date_last_checked_rain = None

#Should it rain today?
default persistent._mas_should_rain_today = None

#Loading at init 0 because of season functions
init python in mas_weather:

    def shouldRainToday():

        #Is it a new day? If so, we should see if it should rain today
        if store.mas_pastOneDay(store.persistent._mas_date_last_checked_rain):
            store.persistent._mas_date_last_checked_rain = datetime.date.today()

            #Now we roll
            chance = random.randint(1,100)

            #ODDS:
            #   Spring:
            #       - 30% chance for it to not rain on a particular day
            #   Summer:
            #       - 85% chance for it to not rain on a particular day
            #   Fall:
            #       - 40% chance for it to not rain on a particular day
            #   Winter:
            #       - 0%. Just snow
            if store.mas_isSpring():
                store.persistent._mas_should_rain_today = chance >= 30
            elif store.mas_isSummer():
                store.persistent._mas_should_rain_today = chance >= 85
            elif store.mas_isFall():
                store.persistent._mas_should_rain_today = chance >= 40
            else:
                store.persistent._mas_should_rain_today = False

        return store.persistent._mas_should_rain_today


    def _determineCloudyWeather(
            rain_chance,
            thunder_chance,
            overcast_chance,
            rolled_chance=None
        ):
        """
        Determines if weather should be rainiy/thunder/overcase, or none of
        those.

        IN:
            rain_chance - chance of rain out of 100
            thunder_chance - chance of thunder out of 100
                NOTE: this should be percentage based on rain chance, i.e.:
                thunder_chance * (rain_chance as %)
            overcast_chance - chance of overcast out of 100
            rolled_chance - if passed, then we use that chance instead of
                generating a random chance. None means we generate our
                own chance.
                (Default: None)

        RETURNS:
            appropriate weather type, or None if neither of these weathers.
        """
        if rolled_chance is None:
            rolled_chance = random.randint(1,100)

        if shouldRainToday():
            # try raining if we can

            if rolled_chance <= rain_chance:

                # double check thunder
                if rolled_chance <= thunder_chance:
                    return store.mas_weather_thunder

                # otherwise rain
                return store.mas_weather_rain

            # if we failed to rain here, then modify the rolled chance to be
            # appropriate to for the next chance
            rolled_chance -= rain_chance

        if rolled_chance <= overcast_chance:
            return store.mas_weather_overcast

        # otherwise, no cloudy weather
        return None


init -99 python in mas_weather:
    import random
    import datetime
    import store

    #NOTE: Not persistent since weather changes on startup
    force_weather = False

    WEATHER_MAP = {}

    # weather constants
    # NOTE: just reference MOOD's numbers
    WEAT_RETURN = "Nevermind"

    #Stores the time at which weather should change
    weather_change_time = None

    #Precipitation type constants
    PRECIP_TYPE_DEF = "def"
    PRECIP_TYPE_RAIN = "rain"
    PRECIP_TYPE_OVERCAST = "overcast"
    PRECIP_TYPE_SNOW = "snow"

    # all precip types
    PRECIP_TYPES = (
        PRECIP_TYPE_DEF,
        PRECIP_TYPE_RAIN,
        PRECIP_TYPE_OVERCAST,
        PRECIP_TYPE_SNOW
    )

    #Keep a temp store of weather here for if we're changing backgrounds
    temp_weather_storage = None

    old_weather_tag = "mas_old_style_weather_{0}"
    old_weather_id = 1

    OLD_WEATHER_OBJ = {}
    # key: generated ID
    # value: assocaited displayable

    def _generate_old_image(disp):
        """
        Generates an image for the old-style weather.

        IN:
            disp - displayable to pass to renpy.image

        RETURNS: the created image tag
        """
        global old_weather_id
        tag = old_weather_tag.format(old_weather_id)
        store.renpy.image(tag, disp)
        OLD_WEATHER_OBJ[old_weather_id] = tag
        old_weather_id += 1

        return tag


init -20 python in mas_weather:

#    def canChangeWeather():
#        """
#        Returns true if the user can change weather
#
#        NOTE: this does not check affection.
#        """
#        return (
#            store.persistent._mas_weather_rain_happened
#            or store.persistent._mas_weather_snow_happened
#        )

    def weatherProgress():
        """
        Runs a roll on mas_shouldRain() to pick a new weather to change to after a time between half an hour - one and a half hour

        RETURNS:
            - True or false on whether or not to call spaceroom
        """

        #If the player forced weather or we're not in a background that supports weather, we do nothing
        if force_weather or store.mas_current_background.disable_progressive:
            return False

        #Otherwise we do stuff
        global weather_change_time
        #Set a time for startup
        if not weather_change_time:
            # TODO: make this a function so init can set the weather_change _time and prevent double weather setting
            weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))

        elif weather_change_time < datetime.datetime.now():
            #Need to set a new check time
            weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))

            #Change weather
            new_weather = store.mas_shouldRain()
            if new_weather is not None and new_weather != store.mas_current_weather:
                #Let's see if we need to scene change
                if store.mas_current_background.isChangingRoom(
                        store.mas_current_weather,
                        new_weather
                ):
                    store.mas_idle_mailbox.send_scene_change()

                #Now we change weather
                store.mas_changeWeather(new_weather)

                #Play the rumble in the back to indicate thunder
                if new_weather == store.mas_weather_thunder:
                    renpy.play("mod_assets/sounds/amb/thunder_1.wav",channel="backsound")
                return True

            elif store.mas_current_weather != store.mas_weather_def:
                #Let's see if we need to scene change
                if store.mas_current_background.isChangingRoom(
                        store.mas_current_weather,
                        store.mas_weather_def
                ):
                    store.mas_idle_mailbox.send_scene_change()

                store.mas_changeWeather(store.mas_weather_def)
                return True

        return False


    def loadMWData():
        """
        Loads persistent MASWeather data into the weather map

        ASSUMES: weather map is already filled
        """
        if store.persistent._mas_weather_MWdata is None:
            return

        for mw_id, mw_data in store.persistent._mas_weather_MWdata.iteritems():
            mw_obj = WEATHER_MAP.get(mw_id, None)
            if mw_obj is not None:
                mw_obj.fromTuple(mw_data)


    def saveMWData():
        """
        Saves MASWeather data from weather map into persistent
        """
        for mw_id, mw_obj in WEATHER_MAP.iteritems():
            store.persistent._mas_weather_MWdata[mw_id] = mw_obj.toTuple()


    def unlockedWeathers():
        """
        Returns number of unlocked weather items
        """
        count = 0
        for mw_id, mw_obj in WEATHER_MAP.iteritems():
            if mw_obj.unlocked:
                count += 1

        return count


    ## weather programming points here
    # NOTE: all points should expect the weather object they are either
    #   replacing or being replaced by

    def _weather_rain_entry(_old):
        """
        Rain start programming point
        """

        # dont need to change anything if we are switching from thunder
        if _old != store.mas_weather_thunder:
            # set global flag
            store.mas_is_raining = True

            # play rain sound
            renpy.music.play(
                store.audio.rain,
                channel="background",
                loop=True,
                fadein=1.0,
                if_changed=True
            )

        if store.persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = True

    def _weather_rain_exit(_new):
        """
        RAIN stop programming point
        """

        # dont change any flags if we are switching to thunder
        if _new != store.mas_weather_thunder:
            # set gklobal flag
            store.mas_is_raining = False

            # stop rain sound
            renpy.music.stop(channel="background", fadeout=1.0)

        if store.persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = False

    def _weather_snow_entry(_old):
        """
        Snow entry programming point
        """
        # set global flag
        store.mas_is_snowing = True

        #We want this topic seen for the first time with aurora visible outside her window
        #But we also don't want it to machine gun other topics too
        if (
            store.mas_current_background.isFltNight()
            and not store.persistent.event_list
            and not store.mas_getEVL_shown_count("monika_auroras")
        ):
            store.queueEvent("monika_auroras", notify=True)


    def _weather_snow_exit(_new):
        """
        Snow exit programming point
        """
        # set globla flag
        store.mas_is_snowing = False


    def _weather_thunder_entry(_old):
        """
        Thunder entry programming point
        """
        # dont run rain if swtiching from it
        # run rain programming points
        if _old != store.mas_weather_rain:
            _weather_rain_entry(_old)

        # set global flag
        store.mas_globals.show_lightning = True


    def _weather_thunder_exit(_new):
        """
        Thunder exit programming point
        """
        # set global flag
        store.mas_globals.show_lightning = False

        # run rain progframming points
        # NOTE: dont change anything if swithing to rain
        if _new != store.mas_weather_rain:
            _weather_rain_exit(_new)


    def _weather_overcast_entry(_old):
        """
        Overcast entry programming point
        """
        if store.persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = True

    def _weather_overcast_exit(_new):
        """
        Overcast exit programming point
        """
        if store.persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = False


init -10 python:

    def MASWeather(
            weather_id,
            prompt,
            sp_day,
            sp_night=None,
            precip_type=store.mas_weather.PRECIP_TYPE_DEF,
            isbg_wf_day=None,
            isbg_wof_day=None,
            isbg_wf_night=None,
            isbg_wof_night=None,
            entry_pp=None,
            exit_pp=None,
            unlocked=False
    ):
        """DEPRECATED
        Old-style MASWeather objects.
        This is mapped to a MASFilterableWeather with day/night filter settings
        NOTE: for all image tags, `_fb` is appeneded for fallbacks

        IN:
            weather_id - id that defines this weather object
                NOTE: must be unique
            prompt - button label for this weathe robject
            sp_day - image tag for spaceroom's left window in daytime
            sp_night - image tag for spaceroom's left window in night
                (Default: None)
            precip_type - type of precipitation, def, rain, overcast, or snow
                (Default: def)
            isbg_wf_day - ignored
            isbg_wof_day - ignored
            isbg_wf_night - ignored
            isbg_wof_night - ignored
            entry_pp - programming point to execute after switching to
                this weather
                (Default: None)
            exit_pp - programming point to execute before leaving this
                weather
                (Default: None)
            unlocked - True if this weather object starts unlocked,
                False otherwise
                (Default: False)

        RETURNS: MASFitlerableWeather object
        """
        if sp_night is None:
            sp_night = sp_day

        sp_day_fb = sp_day + "_fb"
        sp_night_fb = sp_night + "_fb"

        # create weather images
        dyn_tag = store.mas_weather._generate_old_image(
            MASFallbackFilterDisplayable(day=sp_day, night=sp_night)
        )
        stt_tag = store.mas_weather._generate_old_image(
            MASFallbackFilterDisplayable(day=sp_day_fb, night=sp_night_fb)
        )

        return MASFilterableWeather(
            weather_id,
            prompt,
            stt_tag,
            ani_img_tag=dyn_tag,
            precip_type=precip_type,
            unlocked=unlocked,
            entry_pp=entry_pp,
            exit_pp=exit_pp
        )


    class MASFilterableWeather(object):
        """
        Weather class to determine some props for weather

        PROPERTIES:
            weather_id - Id that defines this weather object
            prompt - button label for this weater
            unlocked - determines if this weather is unlocked/selectable
            precip_type - type of precipitation (to use for the room type)
            img_tag - image tag to use for the static version of weather
            ani_img_tag - image tag to use for the animated version of weather
            entry_pp - programming point to execute when switching to this
                weather
            exit_pp - programming point to execute when leaving this weather
        """
        import store.mas_weather as mas_weather

        def __init__(self,
                weather_id,
                prompt,
                img_tag,
                ani_img_tag=None,
                precip_type=store.mas_weather.PRECIP_TYPE_DEF,
                unlocked=False,
                entry_pp=None,
                exit_pp=None
        ):
            """
            Constructor for a MASFilterableWeather object

            IN:
                weather_id - id that defines this weather object
                    NOTE: must be unique
                prompt - button label for this weathe robject
                img_tag - image tag to use for the static version of weather
                ani_img_tag - image tag to use for the animated version of
                    weather. If None, we always use the static version.
                    (Default: None)
                precip_type - type of precipitation, def, rain, overcast, or snow
                    (Default: def)
                unlocked - True if this weather object starts unlocked,
                    False otherwise
                    (Default: False)
                entry_pp - programming point to execute after switching to
                    this weather
                    (Default: None)
                exit_pp - programming point to execute before leaving this
                    weather
                    (Default: None)
            """
            if weather_id in self.mas_weather.WEATHER_MAP:
                raise Exception("duplicate weather ID")

            self.weather_id = weather_id
            self.prompt = prompt
            self.img_tag = img_tag
            self.ani_img_tag = ani_img_tag
            self.precip_type = precip_type
            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp

            # add to weather map
            self.mas_weather.WEATHER_MAP[weather_id] = self

        def __eq__(self, other):
            if isinstance(other, MASFilterableWeather):
                return self.weather_id == other.weather_id
            return NotImplemented

        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result

        def entry(self, old_weather):
            """
            Runs entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_weather)

        def exit(self, new_weather):
            """
            Runs exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_weather)

        def get_mask(self):
            """
            Returns the appropriate weathermask based on animation settings

            RETURNS: image tag to use
            """
            if persistent._mas_disable_animations or self.ani_img_tag is None:
                return self.img_tag

            return self.ani_img_tag

        @staticmethod
        def getPrecipTypeFrom(weather=None):
            """
            Gets precip type of the given weather object.

            IN:
                weather - weather object to get precip type for.
                    if None, we use the current weather
                    (Default: None)

            RETURNS: precip_type
            """
            if weather is None:
                return mas_current_weather.precip_type
            return weather.precip_type

        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]

        def sp_window(self, day):
            """DEPRECATED
            Use get_mask instead.
            This returns whatever get_mask returns.
            """
            return self.get_mask()

        def isbg_window(self, day, no_frame):
            """DEPRECATED
            Islands are now separate images. See script-islands-event.
            """
            return ""

        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)


    class MASWeatherMap(object):
        """
        A weather map is an extension of MASHighlightMap except using precip
        types as keys.

        NOTE: actual implementation is by wrapping around MASHighlightMap.
        This is to avoid calling functions that would crash.

        PROPERTIES:
            None
        """

        def __init__(self, precip_map=None):
            """
            Constructor

            IN:
                precip_map - mapping of precip types and values to map to
                    key: precip type
                    value: value to map to precip type
                    NOTE: not required, you can also use add functions instead
                    NOTE: PRECIP_TYPE_DEF is used as a default if given.
            """
            self.__mhm = MASHighlightMap.create_from_mapping(
                store.mas_weather.PRECIP_TYPES,
                None,
                precip_map
            )

        def __iter__(self):
            """
            Returns MHM iterator
            """
            return iter(self.__mhm)

        def add(self, key, value):
            """
            Adds value to map.
            See MASHighlightMap.add
            """
            self.__mhm.add(key, value)

        def apply(self, mapping):
            """
            Applies a dict mapping to this map.
            See MASHlightMap.apply
            """
            self.__mhm.apply(mapping)

        def get(self, key):
            """
            Gets value with the given key

            Uses PRECIP_TYPE_DEF as a default if key not found

            See MASHighlightMap.get
            """
            value = self._raw_get(key)
            if value is None:
                return self._raw_get(store.mas_weather.PRECIP_TYPE_DEF)

            return value

        def _mhm(self):
            """
            Returns the internal MASHighlightMap. Only use if you know what
            you are doing.

            RETURNS: MASHighlightMap object
            """
            return self.__mhm

        def _raw_get(self, precip_type):
            """
            Gets value with given precip_type. this does Not do defaulting.

            IN:
                precip_type - precip type to get value for

            RETURNS: value
            """
            return self.__mhm.get(precip_type)


    class MASFilterWeatherMap(MASFilterMapSimple):
        """
        Extension of MASFilterMap.

        Use this to map weather maps to filters.

        NOTE: this does NOT verify filters.

        PROPERTIES:
            use_fb - if True, this will default to using fallback-based
                getting when using fw_get.
                Defaults to False and must be set after creation.
        """

        def __init__(self, **filter_pairs):
            """
            Constructor

            Will throw exceptions if not given MASWeatherMap objects

            IN:
                **filter_pairs - filter=val args to use. Invalid filters are
                    ignored. Values should be MASWeatherMap objects.
            """
            # validate MASWeatherMap objects
            for wmap in filter_pairs.itervalues():
                if not isinstance(wmap, MASWeatherMap):
                    raise TypeError(
                        "Expected MASWeatherMap object, not {0}".format(
                            type(wmap)
                        )
                    )

            super(MASFilterWeatherMap, self).__init__(**filter_pairs)
            self.use_fb = False

        def fw_get(self, flt, weather=None):
            """
            Gets value from map based on filter and current weather.
            May do fallback-based getting if configured to do so.

            fallback-baesd getting uses the FLT_FB dict to find the NEXT
            available value for a given precip_type. This overrides the
            MASWeatherMap's handling of using PRECIP_TYPE_DEF as a fallback
            until the final MASWeatherMap in the chain.
            For more, see MASFilterWeatherDisplayable in sprite-chart-matrix.

            IN:
                flt - filter to lookup
                weather - weather to lookup. If None, we use the current
                    weather.
                    (Default: None)

            RETURNS: value for the given filter and weather
            """
            return self._raw_fw_get(
                flt,
                MASFilterableWeather.getPrecipTypeFrom(weather)
            )

        def get(self, flt):
            """
            Gets value from map based on filter.

            IN:
                flt - filter to lookup

            RETURNS: value for the given filter
            """
            return self._raw_get(flt)

        def has_def(self, flt):
            """
            Checks if the given flt has a MASWeatherMap that contains a
            non-None value for the default precip type.

            IN:
                flt - filter to check

            RETURNS: True if the filter has a non-None default precip type,
                False otherwise.
            """
            wmap = self._raw_get(flt)
            if wmap is not None:
                return (
                    wmap._raw_get(store.mas_weather.PRECIP_TYPE_DEF)
                    is not None
                )

            return False

        def _raw_fw_get(self, flt, precip_type):
            """
            Gets the actual value from a filter and precip type. This may
            do fallback-based getting if configured to do so.

            NOTE: if the given filter doesn't have an associated MASWeatherMap,
            we ALWAYS use the fallback-based system, but find the next
            available default. See MASFilterWeatherDisplayable in
            sprite-chart-matrix.

            IN:
                flt - filter to lookup
                precip_type - precip type to lookup

            RETURNS: value for a given filter and precip type
            """
            wmap = self._raw_get(flt)
            if not self.use_fb and wmap is not None:
                # if not use fallback get, then use the MASWeatherMap's
                # default handling.
                return wmap.get(precip_type)

            # otherwise, use our special handling

            # wmap could be None because of a not-defined filter. In that case
            # set value to None so we can traverse filters until we find a
            # valid wmap.
            if wmap is not None:
                value = wmap._raw_get(precip_type)
            else:
                value = None

            curr_flt = flt
            while value is None:
                nxt_flt = store.mas_sprites._rslv_flt(curr_flt)

                # if the filters match, we foudn the last one.
                if nxt_flt == curr_flt:
                    # in this case, use standard MASWeatherMap handling.
                    if wmap is None:
                        # without a wmap, we cant do anything except fail.
                        return None

                    return wmap.get(precip_type)

                # otherwise, get the wmap if possible and check value
                wmap = self._raw_get(nxt_flt)
                if wmap is not None:
                    if self.use_fb:
                        value = wmap._raw_get(precip_type)
                    else:
                        # if not in fallback mode, use regular gets
                        value = wmap.get(precip_type)

                curr_flt = nxt_flt

            # non-None value means we use this
            return value

        def _raw_get(self, flt):
            """
            Gets value from map based on filter.

            IN:
                flt - filter to lookup

            RETURNS: value for the given filter
            """
            return super(MASFilterWeatherMap, self).get(flt)


### define weather objects here

init -1 python:

    # default weather (day + night)
    mas_weather_def = MASFilterableWeather(
        "def",
        "Clear",
        "def_weather_fb",
        "def_weather",
        precip_type=store.mas_weather.PRECIP_TYPE_DEF,
        unlocked=True
    )

    # rain weather
    mas_weather_rain = MASFilterableWeather(
        "rain",
        "Rain",
        "rain_weather_fb",
        "rain_weather",
        precip_type=store.mas_weather.PRECIP_TYPE_RAIN,
        unlocked=True,
        entry_pp=store.mas_weather._weather_rain_entry,
        exit_pp=store.mas_weather._weather_rain_exit,
    )

    # snow weather
    mas_weather_snow = MASFilterableWeather(
        "snow",
        "Snow",
        "snow_weather_fb",
        "snow_weather",
        precip_type=store.mas_weather.PRECIP_TYPE_SNOW,
        unlocked=True,
        entry_pp=store.mas_weather._weather_snow_entry,
        exit_pp=store.mas_weather._weather_snow_exit,
    )

    # thunder/lightning
    mas_weather_thunder = MASFilterableWeather(
        "thunder",
        "Thunder/Lightning",
        "rain_weather_fb",
        "rain_weather",
        precip_type=store.mas_weather.PRECIP_TYPE_RAIN,
        unlocked=True,
        entry_pp=store.mas_weather._weather_thunder_entry,
        exit_pp=store.mas_weather._weather_thunder_exit,
    )

    #overcast
    mas_weather_overcast = MASFilterableWeather(
        "overcast",
        "Overcast",
        "overcast_weather_fb",
        "overcast_weather",
        precip_type=store.mas_weather.PRECIP_TYPE_OVERCAST,
        unlocked=True,
        entry_pp=store.mas_weather._weather_overcast_entry,
        exit_pp=store.mas_weather._weather_overcast_exit,
    )

### end defining weather objects

    # loads weather objects
    store.mas_weather.loadMWData()

# sets up weather
#NOTE: MUST be before BGs
init 799 python:
    def mas_setWeather(_weather):
        """
        Sets the initial weather.
        This is meant for startup/ch30_reset

        NOTE: this does NOt call exit programming points

        IN:
            _weather - weather to set to.
        """
        global mas_current_weather
        old_weather = mas_current_weather
        mas_current_weather = _weather
        mas_current_weather.entry(old_weather)


    def mas_changeWeather(new_weather, by_user=None, set_persistent=False, new_bg=None):
        """
        Changes weather without doing scene changes

        NOTE: this does NOT do scene change/spaceroom

        IN:
            new_weather - weather to change to
            by_user - flag for if user changes weather or not
            set_persistent - whether or not we want to make this weather persistent
            new_bg - MASFilterableBackground which will be switched to along with weather change.
                If none, mas_current_background is used.
                (Default: None)
        """
        if new_bg is None:
            new_bg = store.mas_current_background

        #If the current background doesn't support weather, we set to def weather instead
        #Since it has no sfx or anything
        if new_bg.disable_progressive and new_bg.hide_masks:
            new_weather = store.mas_weather_def

        if by_user is not None:
            mas_weather.force_weather = bool(by_user)

        if set_persistent:
            persistent._mas_current_weather = new_weather.weather_id

        mas_current_weather.exit(new_weather)
        mas_setWeather(new_weather)

    def mas_startupWeather():
        """
        Runs a weather startup alg, checking whether or not persistent weather should be used
        Sets weather accordingly
        """
        #If the current bg doesn't support weather, we don't do anything
        #Same if we forced weather or we're to skip setting weather
        if (
            not store.mas_current_background.disable_progressive
            and not store.mas_weather.force_weather
            and not store.skip_setting_weather
        ):
            #Let's check for persistent weather. If persistent is auto or no longer a thing, we revert to standard progressive
            if (
                persistent._mas_current_weather == "auto"
                or persistent._mas_current_weather not in mas_weather.WEATHER_MAP
                or store.mas_isMoniHappy(lower=True)
            ):
                set_to_weather = mas_shouldRain()
                #In the case that the weather object no longer exists, we'll set current weather to auto
                persistent._mas_current_weather = "auto"

            #Otherwise, we'll set to the persistent weather
            else:
                set_to_weather = mas_weather.WEATHER_MAP.get(persistent._mas_current_weather)
                #And since we have persistent weather, we know weather is forced
                store.mas_weather.force_weather = True

            #Now set weather accordingly
            if set_to_weather is not None:
                mas_changeWeather(set_to_weather)

    # set weather to default
    mas_current_weather = None
    mas_setWeather(mas_weather_def)


## Changes weather if given a proper weather object
# NOTE: we always scene change here
# NOTE: if you need to change weather without chanign scene, use the
#   set
#
# IN:
#   new_weather - weather object to change to
#   by_user - whether or not user forced weather
#   set_persistent - whether or not we should load with this weather
label mas_change_weather(new_weather, by_user=None, set_persistent=False):
    python:
        if by_user is not None:
            mas_weather.force_weather = bool(by_user)

        if set_persistent:
            persistent._mas_current_weather = new_weather.weather_id

        #Call exit programming points
        mas_current_weather.exit(new_weather)

        #Set new weather and force change
        old_weather = mas_current_weather
        mas_current_weather = new_weather

        #NOTE: We do this before the spaceroom call because of vars which need to be set
        #Prior to the drawing of the spaceroom (so we can pick the right room to use)

        #Call entry programming point
        mas_current_weather.entry(old_weather)

    call spaceroom(scene_change=True, dissolve_all=True, force_exp="monika 1dsc_static")
    return

init 5 python:
    # available only if moni affection is normal+
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_weather",
            category=["weather"],
            prompt="Can you change the weather?",
            pool=True,
            unlocked=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_change_weather:
    show monika 1eua at t21

    $ renpy.say(m, "What kind of weather would you like?", interact=False)

    python:
        # build menu list
        import store.mas_weather as mas_weather
        import store.mas_moods as mas_moods

        # we assume that we will always have more than 1
        # default should always be at the top
        weathers = [(mas_weather_def.prompt, mas_weather_def, False, False)]

        # build other weather list
        other_weathers = [
            (mw_obj.prompt, mw_obj, False, False)
            for mw_id, mw_obj in mas_weather.WEATHER_MAP.iteritems()
            if mw_id != "def" and mw_obj.unlocked
        ]

        # sort other weather list
        other_weathers.sort()

        # build full list
        weathers.extend(other_weathers)

        #Add the auto option
        weathers.append(("Progressive", "auto", False, False))

        # now add final quit item
        final_item = (mas_weather.WEAT_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(weathers, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    $ sel_weather = _return

    # return value False? then return
    if sel_weather is False:
        return "prompt"

    elif sel_weather == "auto":
        show monika at t11
        if mas_weather.force_weather:
            m 1hub "Sure!"
            m 1dsc "Just give me a second.{w=0.5}.{w=0.5}.{nw}"

            #Set to false and return since nothing more needs to be done
            $ mas_weather.force_weather = False
            $ persistent._mas_current_weather = "auto"
            m 1eua "There we go!"
        else:
            m 1hua "That's the current weather, silly."
            m "Try again~"
            jump monika_change_weather
        return

    if sel_weather == mas_current_weather and mas_weather.force_weather:
        m 1hua "That's the current weather, silly."
        m "Try again~"
        jump monika_change_weather

    $ skip_outro = False
    $ skip_leadin = False

    # otherwise, we can change the weather now
    # NOTE: here is where youc an react to a weather change
    if sel_weather == mas_weather_rain or sel_weather == mas_weather_thunder:
        if not renpy.seen_label("monika_rain"):
            $ pushEvent("monika_rain")
            $ skip_outro = True

        elif persistent._mas_pm_likes_rain is False:
            m 1eka "I thought you didn't like rain."
            m 2etc "Maybe you changed your mind?"
            m 1dsc "..."
            $ skip_leadin = True

    # TODO: maybe react to snow?

    if not skip_leadin:
        show monika at t11
        m 1eua "Alright!"
        m 1dsc "Just give me a second.{w=0.5}.{w=0.5}.{nw}"

    # finally change the weather
    call mas_change_weather(sel_weather, by_user=True, set_persistent=True)

    if not skip_outro:
        m 1eua "There we go!"

    return
