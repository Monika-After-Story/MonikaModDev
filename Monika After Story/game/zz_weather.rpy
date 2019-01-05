## new weather module to handle weather changing
#

### spaceroom weather art

image room_mask = Movie(
    channel="window_1",
    play="mod_assets/window/spaceroom/window_1.webm",
    mask=None
)
image room_mask_fb = "mod_assets/window/spaceroom/window_1_fallback.png"

image room_mask2 = Movie(
    channel="window_2",
    play="mod_assets/window/spaceroom/window_2.webm",
    mask=None
)
image room_mask2_fb = "mod_assets/window/spaceroom/window_2_fallback.png"

image room_mask3 = Movie(
    channel="window_3",
    play="mod_assets/window/spaceroom/window_3.webm",
    mask=None
)
image room_mask3_fb = "mod_assets/window/spaceroom/window_3_fallback.png"

image room_mask4 = Movie(
    channel="window_4",
    play="mod_assets/window/spaceroom/window_4.webm",
    mask=None
)
image room_mask4_fb = "mod_assets/window/spaceroom/window_4_fallback.png"

# big thanks to sebastianN01 for the rain art!
image rain_mask_left = Movie(
    channel="window_5",
    play="mod_assets/window/spaceroom/window_5.webm",
    mask=None
)
image rain_mask_left_fb = "mod_assets/window/spaceroom/window_5_fallback.png"

image rain_mask_right = Movie(
    channel="window_6",
    play="mod_assets/window/spaceroom/window_6.webm",
    mask=None
)
image rain_mask_right_fb = "mod_assets/window/spaceroom/window_6_fallback.png"

# big thanks to Zer0mniac for fixing the snow
image snow_mask_night_left = Movie(
    channel="window_7",
    play="mod_assets/window/spaceroom/window_7.webm",
    mask=None
)
image snow_mask_night_left_fb = "mod_assets/window/spaceroom/window_7_fallback.png"

image snow_mask_night_right = Movie(
    channel="window_8",
    play="mod_assets/window/spaceroom/window_8.webm",
    mask=None
)
image snow_mask_night_right_fb = "mod_assets/window/spaceroom/window_8_fallback.png"

image snow_mask_day_left = Movie(
    channel="window_9",
    play="mod_assets/window/spaceroom/window_9.webm",
    mask=None
)
image snow_mask_day_left_fb = "mod_assets/window/spaceroom/window_9_fallback.png"

image snow_mask_day_right = Movie(
    channel="window_10",
    play="mod_assets/window/spaceroom/window_10.webm",
    mask=None
)
image snow_mask_day_right_fb = "mod_assets/window/spaceroom/window_10_fallback.png"

## end spaceroom weather art

## living room weather art

## end living room weather art

## start island bg weather art

image mas_island_frame_day = "mod_assets/location/special/with_frame.png"
image mas_island_day = "mod_assets/location/special/without_frame.png"
image mas_island_frame_night = "mod_assets/location/special/night_with_frame.png"
image mas_island_night = "mod_assets/location/special/night_without_frame.png"
#image mas_island_frame_rain = "mod_assets/location/special/rain_with_frame.png"
#image mas_island_rain = "mod_assets/location/special/rain_without_frame.png"

## end island bg weather art

# NOTE: might not use these
#default persistent._mas_weather_snow_happened = False
#default persistent._mas_weather_rain_happened = False

default persistent._mas_weather_MWdata = {}
# stores locked/unlocked status for weather

init -20 python in mas_weather:
    import store

    WEATHER_MAP = {}

    # weather constants
    # NOTE: just reference MOOD's numbers
    WEAT_RETURN = "Nevermind"

    
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
                fadein=1.0
            )

            # lock rain start/rain/islands
            store.mas_lockEVL("mas_monika_islands", "EVE") # TODO: island rain art


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

        # unlock rain/islands
#        store.mas_unlockEVL("monika_rain", "EVE")

            # TODO: island rain art
            islands_ev = store.mas_getEV("mas_monika_islands")
            if (
                    islands_ev is not None
                    and islands_ev.shown_count > 0
                    and islands_ev.checkAffection(store.mas_curr_affection)
                ):
                store.mas_unlockEVL("mas_monika_islands", "EVE")

#        else:
#            store.mas_unlockEVL("greeting_ourreality", "GRE")

        # TODO: unlock islands greeting as well


    def _weather_snow_entry(_old):
        """
        Snow entry programming point
        """
        # set global flag
        store.mas_is_snowing = True

        # lock islands
        store.mas_lockEVL("mas_monika_islands", "EVE")

        # TODO: lock islands greeting as well


    def _weather_snow_exit(_new):
        """
        Snow exit programming point
        """
        # set globla flag
        store.mas_is_snowing = False

        # unlock islands
        islands_ev = store.mas_getEV("mas_monika_islands")
        if (
                islands_ev is not None
                and islands_ev.shown_count > 0
                and islands_ev.checkAffection(store.mas_curr_affection)
            ):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

        # TODO: unlock islands greeting as well


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


init -10 python:

    # weather class
    class MASWeather(object):
        """
        Weather class to determine some props for weather

        PROPERTIES:
            weather_id - Id that defines this weather object
            prompt - button label for this weater
            unlocked - determines if this weather is unlocked/selectable
            sp_left_day - image tag for spaceroom's left window in day time
            sp_right_day - image tag for spaceroom's right window in day time
            sp_left_night - image tag for spaceroom's left window in nighttime
            sp_right_night - image tag for spaceroom's right window in night
            isbg_wf_day - image PATH for islands bg daytime with frame
            isbg_wof_day = image PATH for islands bg daytime without frame
            isbg_wf_night - image PATH for island bg nighttime with frame
            isbg_wof_night - image PATH for island bg nighttime without framme

            entry_pp - programming point to execute when switching to this 
                weather
            exit_pp - programming point to execute when leaving this weather

        NOTE: for all image tags, `_fb` is appeneded for fallbacks
        """
        import store.mas_weather as mas_weather

        def __init__(
                self, 
                weather_id,
                prompt,
                sp_left_day,
                sp_right_day,
                sp_left_night=None,
                sp_right_night=None,
                isbg_wf_day=None,
                isbg_wof_day=None,
                isbg_wf_night=None,
                isbg_wof_night=None,
                entry_pp=None,
                exit_pp=None,
                unlocked=False
            ):
            """
            Constructor for a MASWeather object

            IN:
                weather_id - id that defines this weather object
                    NOTE: must be unique
                prompt - button label for this weathe robject
                sp_left_day - image tag for spaceroom's left window in daytime
                sp_right_day - image tag for spaceroom's right window in daytime
                unlocked - True if this weather object starts unlocked,
                    False otherwise
                    (Default: False)
                sp_left_night - image tag for spaceroom's left window in night
                    If None, we use left_day for this
                    (Default: None)
                sp_right_night - image tag ofr spaceroom's right window in
                    night
                    If None, we use right_day for this
                    (Default: None)
                isbg_wf_day - image PATH for islands bg daytime with frame
                    (Default: None)
                isbg_wof_day = image PATH for islands bg daytime without frame
                    (Default: None)
                isbg_wf_night - image PATH for island bg nighttime with frame
                    If None, we use isbg_wf_day
                    (Default: None)
                isbg_wof_night - image PATH for island bg nighttime without 
                    framme
                    If None, we use isbg_wof_day
                    (Default: None)
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
            self.sp_left_day = sp_left_day
            self.sp_right_day = sp_right_day
            self.sp_left_night = sp_left_night
            self.sp_right_night = sp_right_night
            self.isbg_wf_day = isbg_wf_day
            self.isbg_wof_day = isbg_wof_day
            self.isbg_wf_night = isbg_wf_night
            self.isbg_wof_night = isbg_wof_night
            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp

            # clean day/night
            if sp_left_night is None:
                self.sp_left_night = sp_left_day

            if sp_right_night is None:
                self.sp_right_night = sp_right_day

            # clean islands
            if isbg_wf_night is None:
                self.isbg_wf_night = isbg_wf_day

            if isbg_wof_night is None:
                self.isbg_wof_night = isbg_wof_day

            # add to weather map
            self.mas_weather.WEATHER_MAP[weather_id] = self


        def __eq__(self, other):
            if isinstance(other, MASWeather):
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


        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]


        def sp_window(self, day):
            """
            Returns spaceroom masks for window

            IN:
                day - True if we want day time masks

            RETURNS tuple of following format:
                [0]: left window mask
                [1]: right window mask
            """
            if day:
                return (self.sp_left_day, self.sp_right_day)

            return (self.sp_left_night, self.sp_right_night)


        def isbg_window(self, day, no_frame):
            """
            Returns islands bg PATH for window

            IN:
                day - True if we want daytime bg
                no_frame - True if we want no frame
            """
            if day:
                if no_frame:
                    return self.isbg_wof_day

                return self.isbg_wf_day

            # else night
            if no_frame:
                return self.isbg_wof_night

            return self.isbg_wf_night


        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)


### define weather objects here

init -1 python:
   
    # default weather (day + night)
    mas_weather_def = MASWeather(
        "def",
        "Default",

        # sp day
        "room_mask3",
        "room_mask4",

        # sp night
        "room_mask",
        "room_mask2",

        # islands bg day
        "mod_assets/location/special/with_frame.png",
        "mod_assets/location/special/without_frame.png",

        # islands bg night
        "mod_assets/location/special/night_with_frame.png",
        "mod_assets/location/special/night_without_frame.png",

        unlocked=True
    )

    # rain weather
    mas_weather_rain = MASWeather(
        "rain",
        "Rain",

        # sp day and night
        "rain_mask_left",
        "rain_mask_right",

        # islands bg day and night
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        entry_pp=store.mas_weather._weather_rain_entry,
        exit_pp=store.mas_weather._weather_rain_exit,
        unlocked=True,
    )

    # snow weather
    mas_weather_snow = MASWeather(
        "snow",
        "Snow",

        # sp day
        "snow_mask_day_left",
        "snow_mask_day_right",

        # sp night
        "snow_mask_night_left",
        "snow_mask_night_right",

        entry_pp=store.mas_weather._weather_snow_entry,
        exit_pp=store.mas_weather._weather_snow_exit
    )

    # thunder/lightning
    mas_weather_thunder = MASWeather(
        "thunder",
        "Thunder/Lightning",

        # sp day and night
        "rain_mask_left",
        "rain_mask_right",

        # islands bg day and night
        isbg_wf_day="mod_assets/location/special/rain_with_frame.png",
        isbg_wof_day="mod_assets/location/special/rain_without_frame.png",

        entry_pp=store.mas_weather._weather_thunder_entry,
        exit_pp=store.mas_weather._weather_thunder_exit
    )

### end defining weather objects

    # loads weather objects
    store.mas_weather.loadMWData()

# sets up weather
init 800 python:

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


    def mas_changeWeather(new_weather):
        """
        Changes weather without doing scene changes

        NOTE: this does NOT do scene change/spaceroom

        IN:
            new_weather - weather to change to
        """
        mas_current_weather.exit(new_weather)
        mas_setWeather(new_weather)


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
label mas_change_weather(new_weather):

    # call exit programming points
    $ mas_current_weather.exit(new_weather)

    # set new weather and force change
    $ old_weather = mas_current_weather
    $ mas_current_weather = new_weather
    $ scene_change = True
    call spaceroom

    # call entry programming point
    $ mas_current_weather.entry(old_weather)

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
            rules={"no unlock": None},
            aff_range=(mas_aff.NORMAL, None)
        )
    )

label monika_change_weather:

    m 1hua "Sure!"

label monika_change_weather_loop:

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

        # now add final quit item
        final_item = (mas_weather.WEAT_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(weathers, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item=final_item)

    $ sel_weather = _return

    show monika at t11

    # return value False? then return
    if sel_weather is False:
        m 1eka "Oh, alright."
        m "If you want to change the weather, just ask, okay?"
        return

    if sel_weather == mas_current_weather:
        m 1hua "That's the current weather, silly."
        m "Try again~" 
        jump monika_change_weather_loop

    $ skip_outro = False
    $ skip_leadin = False

    # otherwise, we can change the weather now
    # NOTE: here is where youc an react to a weather change
    if sel_weather == mas_weather_rain or sel_weather == mas_weather_thunder:
        if not renpy.seen_label("monika_rain"):
            $ pushEvent("monika_rain")
            $ skip_outro = True

        elif persistent._mas_likes_rain is False:
            m 1eka "I thought you didn't like rain."
            m 2etc "Maybe you changed your mind?"
            m 1dsc "..."
            $ skip_leadin = True
            
    # TODO: maybe react to snow?

    if not skip_leadin:
        m 1eua "Alright!"
        m 1dsc "Just give me a second..."

    pause 1.0

    # finally change the weather
    call mas_change_weather(sel_weather)

    if not skip_outro:
        m 1eua "There we go!"
        m "If you want to change the weather again, just ask me, okay?"

    return
