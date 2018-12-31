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

init -20 python in mas_weather:
    import store

    WEATHER_MAP = {}

    
    def canChangeWeather():
        """
        Returns true if the user can change weather
        """


    ## weather programming points here

    def _weather_rain_entry():
        """
        Rain start programming point
        """
        # set global flag
        store.mas_is_raining = True

        # play rain sound
        renpy.music.play(
            store.audio.rain
            channel="background",
            loop=True,
            fadein=1.0
        )

        # lock rain start/rain/islands
        store.mas_lockEVL("monika_rain", "EVE")
        store.mas_lockEVL("mas_monika_islands", "EVE")


    def _weather_rain_exit():
        """
        RAIN stop programming point
        """
        # set gklobal flag
        store.mas_is_raining = False

        # stop rain sound
        renpy.music.stop(channel="background", fadeout=1.0)

        # unlock rain/islands
        store.mas_unlockEVL("monika_rain", "EVE")
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")


    def _weather_snow_entry():
        """
        Snow entry programming point
        """
        # set global flag
        store.mas_is_snowing = True

        # TODO


    def _weather_snow_exit():
        """
        Snow exit programming point
        """
        # set globla flag
        store.mas_is_snowing = False


    def _weather_thunder_entry():
        """
        Thunder entry programming point
        """
        # run rain programming points
        _weather_rain_entry()

        # set global flag
        store.mas_globals.show_lightning = True


    def _weather_thunder_exit():
        """
        Thunder exit programming point
        """
        # set global flag
        store.mas_globals.show_lightning = False

        # run rain progframming points
        _weather_rain_exit()


init -10 python:

    # weather class
    class MASWeather(object)
        """
        Weather class to determine some props for weather

        PROPERTIES:
            weather_id - Id that defines this weather object
            sp_left_day - image tag for spaceroom's left window in day time
            sp_right_day - image tag for spaceroom's right window in day time
            sp_left_night - image tag for spaceroom's left window in nighttime
            sp_right_night - image tag for spaceroom's right window in night

            entry_pp - programming point to execute when switching to this 
                weather
            exit_pp - programming point to execute when leaving this weather

        NOTE: for all image tags, `_fb` is appeneded for fallbacks
        """
        import store.mas_weather as mas_weather

        def __init__(
                self, 
                weather_id,
                sp_left_day,
                sp_right_day,
                sp_left_night=None,
                sp_right_night=None,
                entry_pp=None,
                exit_pp=None
            ):
            """
            Constructor for a MASWeather object

            IN:
                weather_id - id that defines this weather object
                    NOTE: must be unique
                sp_left_day - image tag for spaceroom's left window in daytime
                sp_right_day - image tag for spaceroom's right window in daytime
                sp_left_night - image tag for spaceroom's left window in night
                    If None, we use left_day for this
                    (Default: None)
                sp_right_night - image tag ofr spaceroom's right window in
                    night
                    If None, we use right_day for this
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
            self.sp_left_day = sp_left_day
            self.sp_right_day = sp_right_day
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp

            # clean day/night
            if sp_left_night is None:
                self.sp_left_night = sp_left_day
            else:
                self.sp_left_night = sp_left_night

            if sp_right_night is None:
                self.sp_right_night = sp_right_day
            else:
                self.sp_right_night = sp_right_night

            # add to weather map
            self.mas_weather.WEATHER_MAP[weather_id] = self


        def entry(self):
            """
            Runs entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp()


        def exit(self):
            """
            Runs exit programming point
            """
            if self.exit_pp is not None;
                self.exit_pp()


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


### define weather objects here

init -1 python:
   
    # default weather (day + night)
    mas_weather_def = MASWeather(
        "def",
        "room_mask3",
        "room_mask4",
        "room_mask",
        "room_mask2"
    )

    # rain weather
    mas_weather_rain = MASWeather(
        "rain",
        "rain_mask_left",
        "rain_mask_right",
        entry_pp=store.mas_weather._weather_rain_entry,
        exit_pp=store.mas_weather._weather_rain_exit
    )

    # snow weather
    mas_weather_snow = MASWeather(
        "snow",
        "snow_mask_day_left",
        "snow_mask_day_right",
        "snow_mask_night_left",
        "snow_mask_night_right",
        entry_pp=store.mas_weather._weather_snow_entry,
        exit_pp=store.mas_weather._weather_snow_exit
    )

    # thunder/lightning
    mas_weather_thunder = MASWeather(
        "thunder",
        "rain_mask_left",
        "rain_mask_right"
        # TODO: progarmming points
#        entry_pp=store.mas_weather._weather_rain_entry,
#        exit_pp=store.mas_weather._weather_rain_exit
    )

### end defining weather objects

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
        mas_current_weather = _weather
        mas_current_weather.entry()


    def mas_changeWeather(new_weather):
        """
        Changes weather without doing scene changes

        NOTE: this does NOT do scene change/spaceroom

        IN:
            new_weather - weather to change to
        """
        mas_current_weather.exit()
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
    $ mas_current_weather.exit()

    # set new weather and force change
    $ mas_current_weather = new_weather
    $ scene_change = True
    call spaceroom

    # call entry programming point
    $ mas_current_weather.entry()

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
            unlocked=False,
            rules={"no unlock": None},
            aff_range=(mas_aff.NORMAL, None)
        )
    )

