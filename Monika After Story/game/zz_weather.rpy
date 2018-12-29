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

    WEATHER_MAP = {}

    ## weather programming points here

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
        "rain_mask_right"
        # TODO: programming points
    )

    # snow weather
    mas_weather_snow = MASWeather(
        "snow",
        "snow_mask_day_left",
        "snow_mask_day_right",
        "snow_mask_night_left",
        "snow_mask_night_right"
        # TODO: progarmming poin ts
    )


### end defining weather objects


## Changes weather if given a proper weather object
#
# IN:
#   new_weather - weather object to change to
label mas_change_weather(new_weather, sc_change=True):

    

    return
