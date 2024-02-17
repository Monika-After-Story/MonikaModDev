# Monika's ???? Event
# deserves it's own file because of how much dialogue these have
# it basically shows a new screen over everything, and has an image map
# Monika reacts to he place the player clicks


# Start lvl to start calculations from
# NOTE: being set to an int when the user unlocks the islands
default persistent._mas_islands_start_lvl = None
# Current progress, -1 means not unlocked yet
default persistent._mas_islands_progress = store.mas_island_event.DEF_PROGRESS
# Most of the progression is linear, but some things are unlocked at random
# that's so every player gets a bit different progression.
# Bear in mind, if you decide to add a new item, you'll need an update script
default persistent._mas_islands_unlocks = store.mas_island_event.IslandsDataDefinition.getDefaultUnlocks()

# Will be loaded later
init python in audio:
    # can't use define with mutable data
    # default just doesn't work /shrug
    isld_isly_clear = None
    isld_isly_rain = None
    isld_isly_snow = None


### initialize the island images
init 1:
    #   if for some reason we fail to convert the files into images
    #   then we must backout of showing the event.
    #
    #   NOTE: other things to note:
    #       on o31, we cannot have islands event
    define mas_decoded_islands = store.mas_island_event.decode_data()
    define mas_cannot_decode_islands = not mas_decoded_islands

    python:
        def mas_canShowIslands(flt=None):
            """
            Global check for whether or not we can show the islands event
            This only checks the technical side, NOT event unlocks

            IN:
                flt - the filter to use in check
                    If None, we fetch the current filter
                    If False, we don't check the fitler at all
                    (Default: None)

            OUT:
                boolean
            """
            # If None, get the current flt
            if flt is None:
                flt = mas_sprites.get_filter()

            # IF False, we don't need to check the flt
            elif flt is False:
                return mas_decoded_islands

            return mas_decoded_islands and mas_island_event.isFilterSupported(flt)


# A bunch of transforms we use for the final islands event
transform mas_islands_final_reveal_trans_1(delay, move_time):
    zoom 3.2
    align (0.45, 0.0)

    pause delay
    linear move_time align (0.9, 0.0)

transform mas_islands_final_reveal_trans_2(delay, move_time):
    zoom 2.5
    align (0.15, 0.5)

    pause delay
    linear move_time align (0.0, 0.2) zoom 1.9

transform mas_islands_final_reveal_trans_3(delay, move_time, zoom_time):
    zoom 3.0
    align (1.0, 0.2)

    pause delay
    linear move_time align (0.7, 0.6)
    linear zoom_time zoom 1.0

transform mas_islands_final_reveal_trans_4(delay, zoom_time):
    align (0.62, 0.55)
    pause delay
    linear zoom_time zoom 10.0


# Transform for weather overlays
transform mas_islands_weather_overlay_transform(speed=1.0, img_width=1500, img_height=2000):
    animation

    subpixel True
    anchor (0.0, 0.0)

    block:
        crop (img_width-config.screen_width, img_height-config.screen_height, 1280, 720)
        linear speed crop (0, 0, config.screen_width, config.screen_height)
        repeat

# Overlay image for the lightning effect
image mas_islands_lightning_overlay:
    animation

    alpha 0.75

    block:
        # Set the def child
        mas_island_event.NULL_DISP

        # Select wait time
        block:
            choice 0.3:
                pause 5.0
            choice 0.4:
                pause 10.0
            choice 0.3:
                pause 15.0

        # Choice showing lightning or skip
        block:
            choice (1.0 / mas_globals.lightning_chance):
                "mas_lightning"
                pause 0.1
                function mas_island_event._play_thunder
                pause 3.0
            choice (1.0 - 1.0/mas_globals.lightning_chance):
                pass

        repeat


# ## Base room
# # Day images
# image living_room_day = mas_island_event._get_room_sprite("d", False)
# image living_room_day_rain = mas_island_event._get_room_sprite("d_r", False)
# image living_room_day_overcast = "living_room_day_rain"
# image living_room_day_snow = mas_island_event._get_room_sprite("d_s", False)
# # Night images
# image living_room_night = mas_island_event._get_room_sprite("n", False)
# image living_room_night_rain = mas_island_event._get_room_sprite("n_r", False)
# image living_room_night_overcast = "living_room_night_rain"
# image living_room_night_snow = mas_island_event._get_room_sprite("n_s", False)
# # Sunset images
# image living_room_ss = mas_island_event._apply_flt_on_room_sprite("living_room_day", mas_sprites.FLT_SUNSET)
# image living_room_ss_rain = mas_island_event._apply_flt_on_room_sprite("living_room_day_rain", mas_sprites.FLT_SUNSET)
# image living_room_ss_overcast = mas_island_event._apply_flt_on_room_sprite("living_room_day_overcast", mas_sprites.FLT_SUNSET)
# image living_room_ss_snow = mas_island_event._apply_flt_on_room_sprite("living_room_day_snow", mas_sprites.FLT_SUNSET)


# ## Lit room
# # Day images
# image living_room_lit_day = "living_room_day"
# image living_room_lit_day_rain = "living_room_day_rain"
# image living_room_lit_day_overcast = "living_room_day_overcast"
# image living_room_lit_day_snow = "living_room_day_snow"
# # Night images
# image living_room_lit_night = mas_island_event._get_room_sprite("n", True)
# image living_room_lit_night_rain = mas_island_event._get_room_sprite("n_r", True)
# image living_room_lit_night_overcast = "living_room_lit_night_rain"
# image living_room_lit_night_snow = mas_island_event._get_room_sprite("n_s", True)
# # Sunset images
# image living_room_lit_ss = "living_room_ss"
# image living_room_lit_ss_rain = "living_room_ss_rain"
# image living_room_lit_ss_overcast = "living_room_ss_overcast"
# image living_room_lit_ss_snow = "living_room_ss_snow"


# # # Image defination
init -20 python in mas_island_event:
    class IslandsDataDefinition(object):
        """
        A generalised abstraction around raw data for the islands sprites
        """
        TYPE_ISLAND = "island"
        TYPE_DECAL = "decal"
        TYPE_BG = "bg"
        TYPE_OVERLAY = "overlay"
        TYPE_INTERIOR = "interior"
        TYPE_OTHER = "other"# This is basically for everything else
        TYPES = frozenset(
            (
                TYPE_ISLAND,
                TYPE_DECAL,
                TYPE_BG,
                TYPE_OVERLAY,
                TYPE_INTERIOR,
                TYPE_OTHER
            )
        )

        FILENAMES_MAP = {
            TYPE_OVERLAY: ("d", "n"),
        }
        DEF_FILENAMES = ("d", "d_r", "d_s", "n", "n_r", "n_s", "s", "s_r", "s_s")

        DELIM = "_"

        _data_map = dict()

        def __init__(
            self,
            id_,
            type_=None,
            default_unlocked=False,
            filenames=None,
            fp_map=None,
            partial_disp=None
        ):
            """
            Constructor

            IN:
                id_ - unique id for this sprite
                    NOTE: SUPPORTED FORMATS:
                        - 'island_###'
                        - 'decal_###'
                        - 'bg_###'
                        - 'overlay_###'
                        - 'other_###'
                        where ### is something unique
                type_ - type of this sprite, if None, we automatically get it from the id
                    (Default: None)
                default_unlocked - whether or not this sprite is unlocked from the get go
                    (Default: False)
                filenames - the used filenames for this data, those are the keys for fp_map, if None, will be used default
                    paths in the FILENAMES_MAP or DEF_FILENAMES
                    (Default: None)
                fp_map - the map of the images for this sprite, if None, we automatically generate it
                    NOTE: after decoding this will point to a loaded ImageData object instead of a failepath
                    (Default: None)
                partial_disp - functools.partial of the displayable for this sprite
                    (Default: None)
            """
            if self.__split_id(id_)[0] not in self.TYPES:
                raise ValueError(
                    "Bad id format. Supported formats for id: {}, got: '{}'.".format(
                        ", ".join("'{}_###'".format(t) for t in self.TYPES),
                        id_
                    )
                )
            if id_ in self._data_map:
                raise Exception("Id '{}' has already been used.".format(id_))

            self.id = id_

            if type_ is not None:
                if type_ not in self.TYPES:
                    raise ValueError("Bad type. Allowed types: {}, got: '{}'.".format(self.TYPES, type_))

            else:
                type_ = self._getType()

            self.type = type_

            self.default_unlocked = bool(default_unlocked)
            self.filenames = filenames
            self.fp_map = fp_map if fp_map is not None else self._buildFPMap()
            self.partial_disp = partial_disp

            self._data_map[id_] = self

        def _getType(self):
            """
            Private method to get type of this sprite if it hasn't been passed in

            OUT:
                str
            """
            return self._split_id()[0]

        def _buildFPMap(self):
            """
            Private method to build filepath map if one hasn't been passed in

            OUT:
                dict
            """
            filepath_fmt = "{type_}/{name}/{filename}"
            type_, name = self._split_id()
            if self.filenames is None:
                filenames = self.FILENAMES_MAP.get(self.type, self.DEF_FILENAMES)
            else:
                filenames = self.filenames

            # FIXME: Use f-strings with py3 pls
            return {
                filename: filepath_fmt.format(
                    type_=type_,
                    name=name,
                    filename=filename
                )
                for filename in filenames
            }

        def _split_id(self):
            """
            Splits an id into type and name strings
            """
            return self.__split_id(self.id)

        @classmethod
        def __split_id(cls, id_):
            """
            Splits an id into type and name strings
            """
            return id_.split(cls.DELIM, 1)

        @classmethod
        def getDataFor(cls, id_):
            """
            Returns data for an id

            OUT:
                IslandsDataDefinition
                or None
            """
            return cls._data_map.get(id_, None)

        @classmethod
        def getDefaultUnlocks(cls):
            """
            Returns default unlocks for sprites

            OUT:
                dict
            """
            # FIXME: py3 update
            return {
                id_: data.default_unlocked
                for id_, data in cls._data_map.iteritems()
            }

        @classmethod
        def getFilepathsForType(cls, type_):
            """
            Returns filepaths for images of sprites of the given type

            OUT:
                dict
            """
            # FIXME: py3 update
            return {
                id_: data.fp_map
                for id_, data in cls._data_map.iteritems()
                if data.type == type_ and data.fp_map
            }

    # # # Transform funcs for island disps
    # These transforms perform cyclic motion. See dev/transforms for graphical
    # representations of the motions.
    # 'transform' is the transform object we're modifying
    # 'st' and 'at' are not documented, timestamps, we're using 'at' since we're doing animations,
    #     it controls the current position of the object
    # 'amplitude' variables control the maximum extent of the function (basically how far the object can move)
    # 'frequency' variables control the frequency (period) of the function (basically speed of the object)
    # Using different combinations of the functinos and parameters allow to give each object a unique pattern,
    # which will be repeated after some time, creating a seamless loop.
    def __isld_1_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        amplitude = 0.02
        frequency_1 = 1.0 / 9.0
        frequency_2 = 1.0 / 3.0

        transform.ypos = math.cos(at*frequency_1) * math.sin(at*frequency_2) * amplitude
        # We updated the transform, so we must update the sprite, too
        # But only once the transform is active (otherwise you get a recursive loop)
        if transform.active:
            transform.__parallax_sprite__.update_offsets()

        return 0.0

    def __isld_2_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        y_amplitude = -0.01
        y_frequency_1 = 0.5
        y_frequency_2 = 0.25

        x_amplitude = -0.0035
        x_frequency = 0.2

        transform.ypos = math.sin(math.sin(at*y_frequency_1) + math.sin(at*y_frequency_2)) * y_amplitude
        transform.xpos = math.cos(at*x_frequency) * x_amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()

        return 0.0

    def __isld_3_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        amplitude = 0.005
        frequency_1 = 0.25
        frequency_2 = 0.05

        transform.ypos = (math.sin(at*frequency_1) + abs(math.cos(at*frequency_2))) * amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()

        return 0.0

    def __isld_5_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        y_amplitude = -0.01
        y_frequency_1 = 1.0 / 10.0
        y_frequency_2 = 7.0

        x_amplitude = 0.005
        x_frequency = 0.25

        transform.ypos = math.sin(math.sin(at*y_frequency_1) * y_frequency_2) * y_amplitude
        transform.xpos = math.cos(at*x_frequency) * x_amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()

        return 0.0

    def __chibi_transform_func(transform, st, at):
        """
        A function which we use as a transform, updates the child
        """
        roto_speed = -10
        amplitude = 0.065
        frequency = 0.5

        transform.rotate = at % 360 * roto_speed
        transform.ypos = math.sin(at * frequency) * amplitude
        if transform.active:
            transform.__parallax_sprite__.update_offsets()

        return 0.0

    def _play_thunder(transform, st, at):
        """
        This is used in a transform to play the THUNDER sound effect
        """
        renpy.play("mod_assets/sounds/amb/thunder.wav", channel="backsound")
        return None

    # # # Img definations

    # NOTE: As you can see ParallaxDecal aren't being passed in partials, they are dynamically added later
    # during composite image building
    # NOTE: Use functools.partial instead of renpy.partial because the latter has an argument conflict. Smh Tom
    # Islands
    IslandsDataDefinition(
        "island_0",
        default_unlocked=True,
        partial_disp=functools.partial(
            ParallaxSprite,
            x=-85,
            y=660,
            z=15,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_1",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=483,
            y=373,
            z=35,
            function=__isld_1_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_2",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=275,
            y=299,
            z=70,
            function=__isld_2_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_3",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=292,
            y=155,
            z=95,
            function=__isld_3_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_4",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=-15,
            y=-15,
            z=125,
            on_click="mas_island_upsidedownisland"
        )
    )
    IslandsDataDefinition(
        "island_5",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=991,
            y=184,
            z=55,
            function=__isld_5_transform_func,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_6",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=912,
            y=46,
            z=200,
            function=None,
            on_click="mas_island_distant_islands"
        )
    )
    IslandsDataDefinition(
        "island_7",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=439,
            y=84,
            z=250,
            function=None,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "island_8",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=484,
            y=54,
            z=220,
            on_click="mas_island_distant_islands"
        )
    )

    # Decals
    IslandsDataDefinition(
        "decal_bookshelf",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=358,
            y=62,
            z=6,
            on_click="mas_island_bookshelf"
        )
    )
    IslandsDataDefinition(
        "decal_bushes",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=305,
            y=70,
            z=8,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_house",# FIXME: clear and snow sprites appear to be of different sizes
        partial_disp=functools.partial(
            ParallaxDecal,
            x=215,
            y=-37,
            z=1
        )
    )
    IslandsDataDefinition(
        "decal_tree",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click="mas_island_cherry_blossom_tree"
        )
    )
    GLITCH_FPS = (
        "other/glitch/frame_0",
        "other/glitch/frame_1",
        "other/glitch/frame_2",
        "other/glitch/frame_3",
        "other/glitch/frame_4",
        "other/glitch/frame_5",
        "other/glitch/frame_6"
    )
    IslandsDataDefinition(
        "decal_glitch",
        fp_map={},# TODO: move GLITCH_FPS to fp_map
        partial_disp=functools.partial(
            ParallaxDecal,
            x=216,
            y=-54,
            z=2,
            on_click="mas_island_glitchedmess"
        )
    )
    # O31 specific decals
    IslandsDataDefinition(
        "decal_bloodfall",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=213,
            y=0,
            z=1,
            on_click="mas_island_bloodfall"
        )
    )
    IslandsDataDefinition(
        "decal_ghost_0",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=366,
            y=-48,
            z=5,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_ghost_1",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=366,
            y=-48,
            z=5,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_ghost_2",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=366,
            y=-48,
            z=5,
            on_click=True
        )
    )
    # NOTE: these trees have same params as decal_tree
    IslandsDataDefinition(
        "decal_haunted_tree_0",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_haunted_tree_1",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_haunted_tree_2",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-194,
            z=4,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_gravestones",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=123,
            y=17,
            z=1,
            on_click="mas_island_gravestones"
        )
    )
    IslandsDataDefinition(
        "decal_jack",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=253,
            y=63,
            z=2,
            on_click="mas_island_pumpkins"
        )
    )
    IslandsDataDefinition(
        "decal_pumpkins",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=178,
            y=59,
            z=15,
            on_click="mas_island_pumpkins"
        )
    )
    IslandsDataDefinition(
        "decal_skull",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=120,
            y=-10,
            z=1,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_webs",
        filenames=("d", "n"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=187,
            y=-99,
            z=5,
            # on_click=True
        )
    )
    # D25 specific deco
    IslandsDataDefinition(
        "decal_bookshelf_lantern",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=387,
            y=47,
            z=7,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_circle_garland",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=234,
            y=22,
            z=2,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_hanging_lantern",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=210,
            y=23,
            z=2,
            on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_rectangle_garland",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=320,
            y=28,
            z=2,
            on_click=True
        )
    )
    TREE_LIGHTS_FPS = (
        "other/tree_lights/d",
        "other/tree_lights/n_0",
        "other/tree_lights/n_1",
        "other/tree_lights/n_2",
        "other/tree_lights/s"
    )
    IslandsDataDefinition(
        "decal_tree_lights",
        fp_map={},# TODO: move TREE_LIGHTS_FPS to fp_map
        partial_disp=functools.partial(
            ParallaxDecal,
            x=140,
            y=-168,
            z=5,
            # on_click=True
        )
    )
    IslandsDataDefinition(
        "decal_wreath",
        filenames=("d", "n", "s"),
        partial_disp=functools.partial(
            ParallaxDecal,
            x=294,
            y=33,
            z=2,
            on_click=True
        )
    )

    # Objects
    IslandsDataDefinition(
        "other_shimeji",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxSprite,
            Transform(renpy.easy.displayable("chibika smile"), zoom=0.3),
            x=930,
            y=335,
            z=36,
            function=__chibi_transform_func,
            on_click="mas_island_shimeji"
        )
    )
    # IslandsDataDefinition(
    #     "other_isly",
    #     filenames=("clear", "rain", "snow")
    # )

    # # Interior
    # IslandsDataDefinition(
    #     "interior_room",
    #     filenames=("d", "d_r", "d_s", "n", "n_r", "n_s")
    # )
    # IslandsDataDefinition(
    #     "interior_room_lit",
    #     filenames=("d", "d_r", "d_s", "n", "n_r", "n_s")
    # )
    # IslandsDataDefinition(
    #     "interior_tablechair",
    #     filenames=("chair", "shadow", "table")
    # )

    # BGs
    IslandsDataDefinition(
        "bg_def",
        default_unlocked=True,
        partial_disp=functools.partial(
            ParallaxSprite,
            x=0,
            y=0,
            z=15000,
            min_zoom=1.02,
            max_zoom=4.02,
            on_click="mas_island_sky"
        )
    )

    # Overlays
    IslandsDataDefinition(
        "overlay_rain",
        default_unlocked=True,
        partial_disp=functools.partial(
            _build_weather_overlay_transform,
            speed=0.8
        )
    )
    IslandsDataDefinition(
        "overlay_snow",
        default_unlocked=True,
        partial_disp=functools.partial(
            _build_weather_overlay_transform,
            speed=3.5
        )
    )
    IslandsDataDefinition(
        "overlay_thunder",
        default_unlocked=True,
        fp_map={},
        partial_disp=functools.partial(
            renpy.easy.displayable,
            "mas_islands_lightning_overlay"
        )
    )
    IslandsDataDefinition(
        "overlay_vignette",
        default_unlocked=True
    )


# # # Main framework
init -25 python in mas_island_event:
    import random
    import functools
    import math
    import io
    from zipfile import ZipFile
    import datetime

    import store
    from store import (
        persistent,
        mas_utils,
        mas_weather,
        mas_sprites,
        mas_ics,
        Transform,
        LiveComposite,
        MASWeatherMap,
        MASFilterWeatherDisplayableCustom,
        MASFilterWeatherDisplayable
    )
    from store.mas_parallax import (
        ParallaxBackground,
        ParallaxSprite,
        ParallaxDecal
    )

    DEF_PROGRESS = -1
    MAX_PROGRESS_ENAM = 4
    MAX_PROGRESS_LOVE = 8
    PROGRESS_FACTOR = 4

    SHIMEJI_CHANCE = 0.01
    DEF_SCREEN_ZORDER = 55

    SUPPORTED_FILTERS = frozenset(
        {
            mas_sprites.FLT_DAY,
            mas_sprites.FLT_NIGHT,
            mas_sprites.FLT_SUNSET
        }
    )

    DATA_ITS_JUST_MONIKA = b"JUSTMONIKA"*1024
    DATA_JM_SIZE = len(DATA_ITS_JUST_MONIKA)
    DATA_READ_CHUNK_SIZE = 2 * 1024**2
    DATA_SPACING = 8 * 1024**2

    REVEAL_FADEIN_TIME = 0.5
    REVEAL_WAIT_TIME = 0.1
    REVEAL_FADEOUT_TIME = REVEAL_FADEIN_TIME

    REVEAL_TRANSITION_TIME = REVEAL_FADEIN_TIME + REVEAL_WAIT_TIME + REVEAL_FADEOUT_TIME
    REVEAL_ANIM_DELAY = REVEAL_FADEIN_TIME + REVEAL_WAIT_TIME

    REVEAL_ANIM_1_DURATION = 12.85
    REVEAL_ANIM_2_DURATION = 13.1
    REVEAL_ANIM_3_1_DURATION = 13.6
    REVEAL_ANIM_3_2_DURATION = 12.7
    REVEAL_ANIM_4_DURATION = 0.5

    REVEAL_OVERVIEW_DURATION = 10.0

    REVEAL_FADE_TRANSITION = store.Fade(REVEAL_FADEIN_TIME, REVEAL_WAIT_TIME, REVEAL_FADEOUT_TIME)
    REVEAL_DISSOLVE_TRANSITION = store.Dissolve(REVEAL_FADEIN_TIME)

    SFX_LIT = "_lit"
    SFX_NIGHT = "_night"

    LIVING_ROOM_ID = "living_room"
    LIVING_ROOM_LIT_ID = LIVING_ROOM_ID + SFX_LIT

    FLT_LR_NIGHT = LIVING_ROOM_ID + SFX_NIGHT
    mas_sprites.add_filter(
        FLT_LR_NIGHT,
        store.im.matrix.tint(0.421, 0.520, 0.965),
        mas_sprites.FLT_NIGHT
    )
    FLT_LR_LIT_NIGHT = LIVING_ROOM_LIT_ID + SFX_NIGHT
    mas_sprites.add_filter(
        FLT_LR_LIT_NIGHT,
        store.im.matrix.tint(0.972, 0.916, 0.796),
        mas_sprites.FLT_NIGHT
    )

    # These're being populated later once we decode the imgs
    island_disp_map = dict()
    decal_disp_map = dict()
    other_disp_map = dict()
    bg_disp_map = dict()
    overlay_disp_map = dict()
    interior_disp_map = dict()

    NULL_DISP = store.Null()

    # setup the docking station we are going to use here
    islands_station = store.MASDockingStation(mas_ics.ISLANDS_FOLDER)

    def isFilterSupported(flt):
        """
        Checks if the event supports a filter

        IN:
            flt - the filter to check (perhaps one of the constants in mas_sprites)

        OUT:
            boolean
        """
        return flt in SUPPORTED_FILTERS

    def _select_img(st, at, mfwm):
        """
        Selection function to use in Island-based images

        IN:
            st - renpy related
            at - renpy related
            mfwm - MASFilterWeatherMap for this island

        RETURNS:
            displayable data
        """
        # During winter we always return images with snow
        # Nonideal, but we have to do this because of the tree
        # FIXME: ideal solution would be split the images by seasons too
        if store.mas_isWinter():
            return mfwm.fw_get(mas_sprites.get_filter(), store.mas_weather_snow), None

        return store.mas_fwm_select(st, at, mfwm)

    def IslandFilterWeatherDisplayable(**filter_pairs):
        """
        DynamicDisplayable for Island images.

        IN:
            **filter_pairs - filter pairs to MASFilterWeatherMap.

        OUT:
            DynamicDisplayable for Island images that respect filters and
                weather.
        """
        return MASFilterWeatherDisplayableCustom(
            _select_img,
            True,
            **filter_pairs
        )

    def _handle_raw_pkg_data(pkg_data, base_err_msg):
        """
        Handles raw data and returns clean, parsed data
        Logs errors

        IN:
            pkg_data - memory buffer

        OUT:
            memory buffer or None
        """
        buf = io.BytesIO()
        buf.seek(0)
        pkg_data.seek(0)

        try:
            while True:
                this_slice_read = 0
                pkg_data.seek(DATA_JM_SIZE, io.SEEK_CUR)

                while this_slice_read < DATA_SPACING:
                    chunk = pkg_data.read(DATA_READ_CHUNK_SIZE)
                    chunk_size = len(chunk)

                    if not chunk_size:
                        buf.seek(0)
                        return buf

                    this_slice_read += chunk_size
                    buf.write(chunk)

        except Exception as e:
            mas_utils.mas_log.error(
                base_err_msg.format(
                    "Unexpected exception while parsing raw package data: {}".format(e)
                )
            )
            return None

        buf.seek(0)
        return buf

    def decode_data():
        """
        Attempts to decode the images

        OUT:
            True upon success, False otherwise
        """
        err_msg = "Failed to decode isld data: {}."

        pkg = islands_station.getPackage("our_reality")

        if not pkg:
            mas_utils.mas_log.error(err_msg.format("Missing package"))
            return False

        pkg_data = islands_station.unpackPackage(pkg, pkg_slip=mas_ics.ISLAND_PKG_CHKSUM)

        if not pkg_data:
            mas_utils.mas_log.error(err_msg.format("Bad package"))
            return False

        zip_data = _handle_raw_pkg_data(pkg_data, err_msg)
        if not zip_data:
            return False

        glitch_frames = None

        def _read_zip(zip_file, map_):
            """
            Inner helper function to read zip and override maps

            IN:
                zip_file - the zip file opened for reading
                map_ - the map to get filenames from, and which will be overriden
            """
            # FIXME: py3 update
            for name, path_map in map_.iteritems():
                for sprite_type, path in path_map.iteritems():
                    raw_data = zip_file.read(path)
                    img = store.MASImageData(raw_data, "{}_{}.png".format(name, sprite_type))
                    path_map[sprite_type] = img

        try:
            with ZipFile(zip_data, "r") as zip_file:
                island_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_ISLAND)
                decal_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_DECAL)
                bg_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_BG)
                overlay_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_OVERLAY)
                interior_map = IslandsDataDefinition.getFilepathsForType(IslandsDataDefinition.TYPE_INTERIOR)
                # Now override maps to contain imgs instead of img paths
                for map_ in (island_map, decal_map, bg_map, overlay_map, interior_map):
                    _read_zip(zip_file, map_)

                # Anim frames are handled a bit differently
                glitch_frames = tuple(
                    (store.MASImageData(zip_file.read(fn), fn + ".png") for fn in GLITCH_FPS)
                )

                tree_lights_imgs = {}
                for fn in TREE_LIGHTS_FPS:
                    k = fn.rpartition("/")[-1]
                    raw_disp = store.MASImageData(zip_file.read(fn), fn + ".png")
                    tree_lights_imgs[k] = raw_disp

                # Audio is being loaded right away
                isly_data = IslandsDataDefinition.getDataFor("other_isly")
                if isly_data:
                    for fn, fp in isly_data.fp_map.iteritems():
                        audio_data = store.MASAudioData(zip_file.read(fp), fp + ".ogg")
                        setattr(store.audio, "isld_isly_" + fn, audio_data)

        except Exception as e:
            mas_utils.mas_log.error(err_msg.format(e), exc_info=True)
            return False

        else:
            # We loaded the images, now create dynamic displayables
            _build_displayables(
                island_map,
                decal_map,
                bg_map,
                overlay_map,
                interior_map,
                glitch_frames,
                tree_lights_imgs
            )

        return True

    def _build_filter_pairs(img_map):
        """
        Builds filter pairs for IslandFilterWeatherDisplayable
        or MASFilterWeatherDisplayable
        """
        precip_to_suffix_map = {
            mas_weather.PRECIP_TYPE_DEF: "",
            mas_weather.PRECIP_TYPE_RAIN: "_r",
            mas_weather.PRECIP_TYPE_SNOW: "_s",
            mas_weather.PRECIP_TYPE_OVERCAST: "_r"# reuse rain
        }

        def _create_weather_map(main_key):
            if main_key not in img_map:
                return None

            precip_map = {}

            for p_type, suffix in precip_to_suffix_map.iteritems():
                k = main_key + suffix
                if k in img_map:
                    precip_map[p_type] = img_map[k]

            if not precip_map:
                raise Exception("Failed to make precip map for: {}".format(img_map))

            return MASWeatherMap(precip_map)

        filter_keys = ("day", "night", "sunset")
        filter_pairs = {}

        for k in filter_keys:
            wm = _create_weather_map(k[0])
            if wm is not None:
                filter_pairs[k] = wm

        return filter_pairs

    def _build_ifwd(img_map):
        """
        Builds a single IslandFilterWeatherDisplayable
        using the given image map
        """
        filter_pairs = _build_filter_pairs(img_map)
        return IslandFilterWeatherDisplayable(**filter_pairs)

    def _build_fwd(img_map):
        """
        Builds a single MASFilterWeatherDisplayable
        using the given image map
        """
        filter_pairs = _build_filter_pairs(img_map)
        return MASFilterWeatherDisplayable(use_fb=True, **filter_pairs)

    def _build_weather_overlay_transform(child, speed):
        """
        A wrapper around mas_islands_weather_overlay_transform
        It exists so we can properly pass the child argument
        to the transform
        """
        return store.mas_islands_weather_overlay_transform(
            child=child,
            speed=speed
        )

    def _build_displayables(
        island_imgs_maps,
        decal_imgs_maps,
        bg_imgs_maps,
        overlay_imgs_maps,
        interior_imgs_map,
        glitch_frames,
        tree_lights_imgs
    ):
        """
        Takes multiple maps with images and builds displayables from them, sets global vars
        NOTE: no sanity checks
        FIXME: py3 update

        IN:
            island_imgs_maps - the map from island names to raw images map
            decal_imgs_maps - the map from decal names to raw images map
            bg_imgs_maps - the map from bg ids to raw images map
            overlay_imgs_maps - the map from overlay ids to raw images map
            interior_imgs_map - the map from the interior stuff to the raw images map
            glitch_frames - tuple of glitch raw anim frames
            tree_lights_imgs - map of images for the tree lights, format:
                img_name: disp
        """
        global island_disp_map, decal_disp_map, other_disp_map
        global bg_disp_map, overlay_disp_map, interior_disp_map

        # Build the islands
        for island_name, img_map in island_imgs_maps.iteritems():
            disp = _build_ifwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(island_name).partial_disp
            island_disp_map[island_name] = partial_disp(disp)

        # Build the decals
        for decal_name, img_map in decal_imgs_maps.iteritems():
            disp = _build_ifwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(decal_name).partial_disp
            decal_disp_map[decal_name] = partial_disp(disp)

        # Build the bg
        for bg_name, img_map in bg_imgs_maps.iteritems():
            disp = _build_ifwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(bg_name).partial_disp
            bg_disp_map[bg_name] = partial_disp(disp)

        # Build the overlays
        for overlay_name, img_map in overlay_imgs_maps.iteritems():
            disp = _build_fwd(img_map)
            partial_disp = IslandsDataDefinition.getDataFor(overlay_name).partial_disp
            if partial_disp is not None:
                disp = partial_disp(disp)
            overlay_disp_map[overlay_name] = disp

        # Build the interior
        for name, img_map in interior_imgs_map.iteritems():
            interior_disp_map[name] = img_map

        if interior_disp_map:
            # HACK: add custom tablechair into the cache right here
            # That's because our images are not on the disk, we can't just use a sprite tag
            # because the paths are hardcoded and we can't use a displayable directly
            for flt_id in (FLT_LR_NIGHT, FLT_LR_LIT_NIGHT):
                tablechair_disp_cache = mas_sprites.CACHE_TABLE[mas_sprites.CID_TC]
                table_im = mas_sprites._gen_im(
                    flt_id,
                    interior_disp_map["interior_tablechair"]["table"]
                )
                tablechair_disp_cache[(flt_id, 0, LIVING_ROOM_ID, 0)] = table_im
                tablechair_disp_cache[(flt_id, 0, LIVING_ROOM_ID, 1)] = table_im# shadow variant can reuse the same img
                tablechair_disp_cache[(flt_id, 1, LIVING_ROOM_ID)] = mas_sprites._gen_im(
                    flt_id,
                    interior_disp_map["interior_tablechair"]["chair"]
                )
                # Shadow is being stored in the highlight cache
                table_shadow_hl_disp_cache = mas_sprites.CACHE_TABLE[mas_sprites.CID_HL]
                table_shadow_hl_disp_cache[(mas_sprites.CID_TC, flt_id, 0, LIVING_ROOM_ID, 1)] = interior_disp_map["interior_tablechair"]["shadow"]

        # Build glitch disp
        def _glitch_transform_func(transform, st, at):
            """
            A function which we use as a transform, updates the child
            """
            redraw = random.uniform(0.3, 1.3)
            next_child = random.choice(glitch_frames)

            transform.child = next_child

            return redraw

        glitch_disp = Transform(child=glitch_frames[0], function=_glitch_transform_func)
        partial_disp = IslandsDataDefinition.getDataFor("decal_glitch").partial_disp
        decal_disp_map["decal_glitch"] = partial_disp(glitch_disp)

        # Build tree lights disp
        tree_lights_frames = tuple(
            tree_lights_imgs.pop("n_" + i)# don't need these in the map anymore
            for i in "012"
        )
        def _tree_lights_transform_func(transform, st, at):
            next_child = random.choice(tree_lights_frames)
            transform.child = next_child
            return 0.4

        tree_lights_night_disp = Transform(child=tree_lights_frames[0], function=_tree_lights_transform_func)
        tree_lights_imgs["n"] = tree_lights_night_disp

        tree_lights_disp = _build_ifwd(tree_lights_imgs)
        partial_disp = IslandsDataDefinition.getDataFor("decal_tree_lights").partial_disp
        decal_disp_map["decal_tree_lights"] = partial_disp(tree_lights_disp)

        # Build chibi disp
        partial_disp = IslandsDataDefinition.getDataFor("other_shimeji").partial_disp
        other_disp_map["other_shimeji"] = partial_disp()

        # Build thunder overlay
        partial_disp = IslandsDataDefinition.getDataFor("overlay_thunder").partial_disp
        overlay_disp_map["overlay_thunder"] = partial_disp()

        return

    def _get_room_sprite(key, is_lit):
        """
        Returns the appropriate displayable for the room sprite based on the criteria

        IN:
            key - str - the sprite key
            is_lit - bool - sprite for the lit or unlit version?

        OUT:
            MASImageData
            or Null displayable if we failed to get the image
        """
        main_key = "interior_room" if not is_lit else "interior_room_lit"
        try:
            return interior_disp_map[main_key][key]

        except KeyError:
            return NULL_DISP

    def _apply_flt_on_room_sprite(room_img_tag, flt):
        """
        Returns the room image with the filter applied on it

        IN:
            room_img_tag - str - the image tag
            flt - str - the filter id to use

        OUT:
            image manipulator
            or Null displayable if we failed to decode the images
        """
        if not store.mas_decoded_islands:
            return NULL_DISP

        return store.MASFilteredSprite(
            flt,
            renpy.displayable(room_img_tag)
        )

    def _is_unlocked(id_):
        """
        Checks if a sprite is unlocked

        IN:
            id_ - the unique id of the sprite

        OUT:
            boolean
        """
        return persistent._mas_islands_unlocks.get(id_, False)

    def _unlock(id_):
        """
        Unlocks a sprite

        IN:
            id_ - the unique id of the sprite

        OUT:
            boolean whether or not the sprite was unlocked
        """
        if id_ in persistent._mas_islands_unlocks:
            persistent._mas_islands_unlocks[id_] = True
            return True

        return False

    def _lock(id_):
        """
        Locks a sprite

        IN:
            id_ - the unique id of the sprite

        OUT:
            boolean whether or not the sprite was locked
        """
        if id_ in persistent._mas_islands_unlocks:
            persistent._mas_islands_unlocks[id_] = False
            return True

        return False

    def _unlock_one(*items):
        """
        Unlocks one of the sprites at random.
        Runs only once

        IN:
            *items - the ids of the sprites

        OUT:
            boolean whether or not a sprite was unlocked
        """
        for i in items:
            if _is_unlocked(i):
                return False

        return _unlock(random.choice(items))


    # # # START functions for lvl unlocks
    def __unlocks_for_lvl_0():
        _unlock("island_1")
        _unlock("island_8")

    def __unlocks_for_lvl_1():
        _unlock("other_shimeji")
        if not renpy.seen_label("mas_monika_islands_final_reveal"):
            _unlock("decal_glitch")

        _unlock("decal_pumpkins")
        _unlock("decal_skull")

    def __unlocks_for_lvl_2():
        _unlock("island_2")

    def __unlocks_for_lvl_3():
        # Unlock only one, the rest at lvl 6
        _unlock_one("island_4", "island_5")

    def __unlocks_for_lvl_4():
        # Unlock only one, the rest at lvl 7
        _unlock_one("island_6", "island_7")

    def __unlocks_for_lvl_5():
        # This requires the 4th isld
        if _is_unlocked("island_4"):
            _unlock("decal_bloodfall")

        # This requires the 5th isld
        if _is_unlocked("island_5"):
            _unlock("decal_gravestones")

    def __unlocks_for_lvl_6():
        _unlock("decal_bushes")

        # Unlock everything from lvl 3
        _unlock("island_4")
        _unlock("island_5")

    def __unlocks_for_lvl_7():
        _unlock("island_3")

        # Unlock only one, the rest at lvl 7
        _unlock_one("decal_bookshelf", "decal_tree")

        # These require the tree
        if _is_unlocked("decal_tree"):
            _unlock_one(*("decal_ghost_" + i for i in "012"))
            _unlock("decal_tree_lights")

        # This requires the bookshelf
        if _is_unlocked("decal_bookshelf"):
            _unlock("decal_bookshelf_lantern")

        # Unlock everything from lvl 4
        _unlock("island_7")
        _unlock("island_6")

    def __unlocks_for_lvl_8():
        # Unlock everything from lvl 7
        _unlock("decal_bookshelf")
        _unlock("decal_tree")

        # These require the tree
        for i in "012":
            _unlock("decal_haunted_tree_" + i)
        _unlock("decal_tree_lights")

        # This requires the bookshelf
        _unlock("decal_bookshelf_lantern")

    def _final_unlocks():
        # TODO: update monika_why_spaceroom
        # NOTE: NO SANITY CHECKS, use carefully
        _unlock("other_isly")
        _unlock("decal_house")

        # These requires the house
        _unlock("decal_jack")
        _unlock("decal_webs")
        _unlock("decal_circle_garland")
        _unlock("decal_hanging_lantern")
        _unlock("decal_rectangle_garland")
        _unlock("decal_wreath")

        # This should be removed once we have the house
        _lock("decal_glitch")

    def __unlocks_for_lvl_9():
        if persistent._mas_pm_cares_island_progress is not False:
            if renpy.seen_label("mas_monika_islands_final_reveal"):
                _final_unlocks()

            else:
                pass

    def __unlocks_for_lvl_10():
        if persistent._mas_pm_cares_island_progress is False:
            if renpy.seen_label("mas_monika_islands_final_reveal"):
                _final_unlocks()

            else:
                pass

    # # # END


    def __handle_unlocks():
        """
        Method to unlock various islands features when the player progresses.
        For example: new decals, new islands, new extra events, set persistent vars, etc.
        """
        g = globals()
        for i in range(persistent._mas_islands_progress + 1):
            fn_name = renpy.munge("__unlocks_for_lvl_{}".format(i))
            callback = g.get(fn_name, None)
            if callback is not None:
                callback()

    def _calc_progress(curr_lvl, start_lvl):
        """
        Returns islands progress for the given current and start levels
        NOTE: this has no sanity checks, don't use this directly

        IN:
            curr_lvl - int, current level
            start_lvl - int, start level

        OUT:
            int, progress
        """
        lvl_difference = curr_lvl - start_lvl

        if lvl_difference < 0:
            return DEF_PROGRESS

        if store.mas_isMoniEnamored(higher=True):
            if store.mas_isMoniLove(higher=True):
                max_progress = MAX_PROGRESS_LOVE

            else:
                max_progress = MAX_PROGRESS_ENAM

            modifier = 1.0

            if persistent._mas_pm_cares_island_progress is True:
                modifier -= 0.2

            elif persistent._mas_pm_cares_island_progress is False:
                modifier += 0.3

            progress_factor = PROGRESS_FACTOR * modifier

            progress = min(int(lvl_difference / progress_factor), max_progress)

        else:
            progress = DEF_PROGRESS

        return progress

    def advance_progression():
        """
        Increments the lvl of progression of the islands event,
        it will do nothing if the player hasn't unlocked the islands yet or if
        the current lvl is invalid
        """
        # If this var is None, then the user hasn't unlocked the event yet
        if persistent._mas_islands_start_lvl is None:
            return

        new_progress = _calc_progress(store.mas_xp.level(), persistent._mas_islands_start_lvl)

        if new_progress == DEF_PROGRESS:
            return

        curr_progress = persistent._mas_islands_progress
        # I hate this, but we have to push the ev from here
        if (
            # Has progress means has new unlocks
            new_progress > curr_progress
            # Not the first lvls, not the last lvl
            and DEF_PROGRESS + 1 < new_progress < MAX_PROGRESS_LOVE - 1
            # Hasn't seen the event yet
            and persistent._mas_pm_cares_island_progress is None
            and not store.seen_event("mas_monika_islands_progress")
            # Hasn't visited the islands for a few days
            and store.mas_timePastSince(store.mas_getEVL_last_seen("mas_monika_islands"), datetime.timedelta(days=1))
        ):
            store.MASEventList.push("mas_monika_islands_progress")

        # Now set new level
        persistent._mas_islands_progress = min(max(new_progress, curr_progress), MAX_PROGRESS_LOVE)
        # Run unlock callbacks
        __handle_unlocks()

        return

    def _get_progression():
        """
        Returns current islands progress lvl
        """
        return persistent._mas_islands_progress

    def start_progression():
        """
        Starts islands progression
        """
        if store.mas_isMoniEnamored(higher=True) and persistent._mas_islands_start_lvl is None:
            persistent._mas_islands_start_lvl = store.mas_xp.level()
            advance_progression()

    def _reset_progression():
        """
        Resets island progress
        """
        persistent._mas_islands_start_lvl = None
        persistent._mas_islands_progress = DEF_PROGRESS
        persistent._mas_islands_unlocks = IslandsDataDefinition.getDefaultUnlocks()

    def play_music():
        """
        Plays appropriate music based on the current weather
        """
        if not _is_unlocked("other_isly"):
            return

        if store.mas_is_raining:
            track = store.audio.isld_isly_rain

        elif store.mas_is_snowing:
            track = store.audio.isld_isly_snow

        else:
            track = store.audio.isld_isly_clear

        if track:
            store.mas_play_song(track, loop=True, set_per=False, fadein=2.5, fadeout=2.5)

    def stop_music():
        """
        Stops islands music
        """
        if store.songs.current_track in (
            store.audio.isld_isly_rain,
            store.audio.isld_isly_snow,
            store.audio.isld_isly_clear
        ):
            store.mas_play_song(None, fadeout=2.5)

    def get_islands_displayable(enable_interaction=True, check_progression=False):
        """
        Builds an image for islands and returns it
        NOTE: This is temporary until we split islands into foreground/background
        FIXME: py3 update

        IN:
            enable_interaction - whether to enable events or not (including parallax effect)
                (Default: True)
            check_progression - whether to check for new unlocks or not,
                this might be a little slow
                (Default: False)

        OUT:
            ParallaxBackground
        """
        global SHIMEJI_CHANCE

        enable_o31_deco = persistent._mas_o31_in_o31_mode and not is_winter_weather()
        enable_d25_deco = persistent._mas_d25_in_d25_mode and is_winter_weather()

        def _reset_parallax_disp(disp):
            # Just in case we always remove all decals and readd them as needed
            disp.clear_decals()
            # Toggle events as desired
            disp.toggle_events(enable_interaction)
            # Reset offsets and zoom
            disp.reset_mouse_pos()
            disp.zoom = disp.min_zoom
            # Return it for convenience
            return disp

        # Progress lvl
        if check_progression:
            advance_progression()

        # Add all unlocked islands
        sub_displayables = [
            _reset_parallax_disp(disp)
            for key, disp in island_disp_map.iteritems()
            if _is_unlocked(key)
        ]

        # Add all unlocked decals for islands 1
        isld_1_decals = ["decal_bookshelf", "decal_bushes", "decal_house", "decal_glitch"]
        if not enable_o31_deco:# O31 has a different tree
            isld_1_decals.append("decal_tree")

        island_disp_map["island_1"].add_decals(
            *(
                decal_disp_map[key]
                for key in isld_1_decals
                if _is_unlocked(key)
            )
        )

        # Add all unlocked O31 decals
        if enable_o31_deco:
            # Basic decals
            isld_to_decals_map = {
                "island_0": ("decal_skull",),
                "island_1": (
                    "decal_ghost_0",
                    "decal_ghost_1",
                    "decal_ghost_2",
                    "decal_jack",
                    "decal_pumpkins",
                    "decal_webs"
                ),
                "island_5": ("decal_gravestones",)
            }
            for isld, decals in isld_to_decals_map.iteritems():
                island_disp_map[isld].add_decals(
                    *(decal_disp_map[key] for key in decals if _is_unlocked(key))
                )

            # The tree has extra logic
            if store.mas_current_background.isFltDay() or not is_cloudy_weather():
                if random.random() < 0.5:
                    haunted_tree = "decal_haunted_tree_0"
                else:
                    haunted_tree = "decal_haunted_tree_1"
            else:
                haunted_tree = "decal_haunted_tree_2"

            if _is_unlocked(haunted_tree):
                island_disp_map["island_1"].add_decals(decal_disp_map[haunted_tree])

            # The bloodfall has extra condition
            if store.mas_current_background.isFltNight() and _is_unlocked("decal_bloodfall"):
                island_disp_map["island_4"].add_decals(decal_disp_map["decal_bloodfall"])

        # Add all unlocked D25 decals
        if enable_d25_deco:
            isld_1_d25_decals = (
                "decal_bookshelf_lantern",
                "decal_circle_garland",
                "decal_hanging_lantern",
                "decal_rectangle_garland",
                "decal_tree_lights",
                "decal_wreath"
            )
            island_disp_map["island_1"].add_decals(
                *(decal_disp_map[key] for key in isld_1_d25_decals if _is_unlocked(key))
            )

        # Add chibi
        if _is_unlocked("other_shimeji") and random.random() <= SHIMEJI_CHANCE:
            shimeji_disp = other_disp_map["other_shimeji"]
            _reset_parallax_disp(shimeji_disp)
            SHIMEJI_CHANCE /= 2.0
            sub_displayables.append(shimeji_disp)

        # Add the bg (we only have one as of now)
        bg_disp = bg_disp_map["bg_def"]
        _reset_parallax_disp(bg_disp)
        sub_displayables.append(bg_disp)

        # Sort in order from back to front
        sub_displayables.sort(key=lambda sprite: sprite.z, reverse=True)

        # Now add overlays (they are always last)
        if store.mas_is_raining:
            sub_displayables.append(overlay_disp_map["overlay_rain"])
            if store.mas_globals.show_lightning:
                sub_displayables.insert(1, overlay_disp_map["overlay_thunder"])

        elif store.mas_is_snowing:
            sub_displayables.append(overlay_disp_map["overlay_snow"])

        # NOTE: Vignette is above EVERYTHING else and works even during the snow
        if persistent._mas_o31_in_o31_mode:
            sub_displayables.append(overlay_disp_map["overlay_vignette"])

        return ParallaxBackground(*sub_displayables)

    def is_winter_weather():
        """
        Checks if the weather on the islands is wintery

        OUT:
            boolean:
                - True if we're using snow islands
                - False otherwise
        """
        return store.mas_is_snowing or store.mas_isWinter()

    def is_cloudy_weather():
        """
        Checks if the weather on the islands is cloudy

        OUT:
            boolean:
                - True if we're using overcast/rain islands
                - False otherwise
        """
        return store.mas_is_raining or store.mas_current_weather == store.mas_weather_overcast


init -1 python in mas_island_event:
    from store import (
        MASFilterableBackground,
        MASFilterWeatherMap,
        MASBackgroundFilterManager,
        MASBackgroundFilterChunk,
        MASBackgroundFilterSlice
    )

    def _living_room_entry(_old, **kwargs):
        """
        Entry pp for lr background
        """
        store.monika_chr.tablechair.table = "living_room"
        store.monika_chr.tablechair.chair = "living_room"


    def _living_room_exit(_new, **kwargs):
        """
        Exit pp for lr background
        """
        store.monika_chr.tablechair.table = "def"
        store.monika_chr.tablechair.chair = "def"

    def register_room(id_):
        """
        Registers lr as a background object

        IN:
            id_ - the id to register under

        OUT:
            MASFilterableBackground
        """
        flt_name_night = id_ + SFX_NIGHT
        mfwm_params = {
            "day": MASWeatherMap(
                {
                    mas_weather.PRECIP_TYPE_DEF: id_ + "_day",
                    mas_weather.PRECIP_TYPE_RAIN: id_ + "_day_rain",
                    mas_weather.PRECIP_TYPE_OVERCAST: id_ + "_day_overcast",
                    mas_weather.PRECIP_TYPE_SNOW: id_ + "_day_snow"
                }
            ),
            "sunset": MASWeatherMap(
                {
                    mas_weather.PRECIP_TYPE_DEF: id_ + "_ss",
                    mas_weather.PRECIP_TYPE_RAIN: id_ + "_ss_rain",
                    mas_weather.PRECIP_TYPE_OVERCAST: id_ + "_ss_overcast",
                    mas_weather.PRECIP_TYPE_SNOW: id_ + "_ss_snow"
                }
            )
        }
        mfwm_params[flt_name_night] = MASWeatherMap(
            {
                mas_weather.PRECIP_TYPE_DEF: id_ + "_night",
                mas_weather.PRECIP_TYPE_RAIN: id_ + "_night_rain",
                mas_weather.PRECIP_TYPE_OVERCAST: id_ + "_night_overcast",
                mas_weather.PRECIP_TYPE_SNOW: id_ + "_night_snow"
            }
        )

        return MASFilterableBackground(
            id_,
            "Living room",
            MASFilterWeatherMap(**mfwm_params),
            MASBackgroundFilterManager(
                MASBackgroundFilterChunk(
                    False,
                    None,
                    MASBackgroundFilterSlice.cachecreate(
                        id_ + SFX_NIGHT,
                        60,
                        None,
                        10
                    )
                ),
                MASBackgroundFilterChunk(
                    True,
                    None,
                    MASBackgroundFilterSlice.cachecreate(
                        mas_sprites.FLT_SUNSET,
                        60,
                        30*60,
                        10
                    ),
                    MASBackgroundFilterSlice.cachecreate(
                        mas_sprites.FLT_DAY,
                        60,
                        None,
                        10
                    ),
                    MASBackgroundFilterSlice.cachecreate(
                        mas_sprites.FLT_SUNSET,
                        60,
                        30*60,
                        10
                    )
                ),
                MASBackgroundFilterChunk(
                    False,
                    None,
                    MASBackgroundFilterSlice.cachecreate(
                        id_ + SFX_NIGHT,
                        60,
                        None,
                        10
                    )
                )
            ),
            hide_calendar=True,
            unlocked=False,
            entry_pp=_living_room_entry,
            exit_pp=_living_room_exit
        )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_islands",
            category=['monika','misc'],
            prompt="Can you show me the floating islands?",
            pool=True,
            unlocked=False,
            rules={"no_unlock": None, "bookmark_rule": store.mas_bookmarks_derand.WHITELIST},
            aff_range=(mas_aff.ENAMORED, None),
            flags=EV_FLAG_DEF if mas_canShowIslands(False) else EV_FLAG_HFM
        ),
        restartBlacklist=True
    )

label mas_monika_islands:
    m 1eub "Of course! You can admire the scenery for now."

    call mas_islands(force_exp="monika 1eua", scene_change=True)

    m 1eua "I hope you liked it, [mas_get_player_nickname()]~"
    return

default persistent._mas_pm_cares_island_progress = None
# pm var re: player caring about Moni's island progress

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_monika_islands_progress"
        ),
        restartBlacklist=True
    )

label mas_monika_islands_progress:
    m 1eub "[player], I've got some exciting news for you!"
    m 3hub "I made some new additions on the islands, {w=0.2}{nw}"
    extend 1rua "and I thought maybe you'd like to take a look."
    m 1hublb "They are {i}our{/i} islands after all~"

    m 3eua "What do you say?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you say?{fast}"

        "Sure, [m_name].":
            $ persistent._mas_pm_cares_island_progress = True
            $ mas_gainAffection(5, bypass=True)
            m 2hub "Yay!"

            call mas_islands(force_exp="monika 1hua")

            m "Hope you liked it~"
            m 1lusdlb "I know it's far from being done, {w=0.2}{nw}"
            extend 1eka "but I really wanted to showcase my progress to you."
            m 2lsp "I'm still learning how to code and this engine being inconsistent doesn't help me..."
            m 7hub "But I think I made quite a bit of progress so far!"
            $ mas_setEventPause(10)
            $ mas_moni_idle_disp.force_by_code("1hua", duration=10, skip_dissolve=True)

        "I'm not interested.":
            $ persistent._mas_pm_cares_island_progress = False
            $ mas_loseAffectionFraction(min_amount=50, modifier=1.0)
            m 2ekc "Oh..."
            m 6rktpc "I..."
            m 6fktpd "I worked really hard on this..."
            m 2rktdc "You...{w=0.5} You must just be busy..."
            $ mas_setEventPause(60*10)
            $ mas_moni_idle_disp.force_by_code("2ekc", duration=60*10, skip_dissolve=True)

        "Maybe later.":
            m 2ekc "Oh...{w=0.5}{nw}"
            extend 2eka "alright."
            m 7eka "Just don't keep me waiting too long~"
            $ mas_setEventPause(20)
            $ mas_moni_idle_disp.force_by_code("1euc", duration=20, skip_dissolve=True)

    return

# default persistent._mas_pm_likes_islands = None

# init 5 python:
#     addEvent(
#         Event(
#             persistent.event_database,
#             eventlabel="mas_monika_islands_final_reveal"
#         ),
#         restartBlacklist=True
#     )

# label mas_monika_islands_final_reveal:
#     python:
#         renpy.dynamic("islands_disp")
#         mas_island_event._final_unlocks()
#         islands_disp = mas_island_event.get_islands_displayable(False, False)

#     m 4sub "I'm so excited to finally show you my work!"

#     if mas_getCurrentBackgroundId() != "spaceroom":
#         m 7eua "Let's return to the classroom for the best view."
#         call mas_background_change(mas_background_def, skip_leadin=True, skip_outro=True)

#     m 1eua "Now let me turn off the light.{w=0.3}.{w=0.3}.{w=0.3}{nw}"

#     window hide
#     call .islands_scene
#     window auto

#     m "..."
#     m "I'm surprised it actually worked, ahaha!~"
#     m "You know, after spending so much time working on this..."
#     m "It feels so satisfying not only being able to see the result myself..."
#     m "But also being able to show it to you, [mas_get_player_nickname()]."
#     m "I'm sure you had been wondering what was behind that bug on the central island~"
#     m "It's a small house for us to spend time in, we can go there any time now, just ask."

#     if mas_background.getUnlockedBGCount() == 1:
#         m "I know staying in this empty classroom can feel tiresome sometimes."
#         m "So it's nice to get more places to visit."

#     else:
#         m "Even with all the other places we have, it's always nice to get new surroundings."

#     m "Now, why don't we go inside, [player]?"

#     window hide
#     call .zoom_in
#     window auto

#     python hide:
#         bg = mas_getBackground(mas_island_event.LIVING_ROOM_ID)
#         if bg:
#             mas_changeBackground(bg)
#         mas_island_event.stop_music()

#     call spaceroom(scene_change=True, dissolve_all=True, force_exp="monika 4hub")

#     m "Tada!~"
#     m 2eua "So, [player]..."
#     m 3eka "Your opinion is {i}really{/i} important to me."

#     call .ask_opinion

#     return

# label mas_monika_islands_final_reveal.islands_scene:
#     $ mas_RaiseShield_core()
#     $ mas_OVLHide()
#     $ mas_hotkeys.no_window_hiding = True
#     $ mas_play_song(None)
#     scene black with dissolve

#     $ mas_island_event.play_music()

#     # I'd love to split the lines properly, but renpy doesn't allow that, so have this cursed thing instead
#     show expression islands_disp as islands_disp at mas_islands_final_reveal_trans_1(
#         delay=mas_island_event.REVEAL_ANIM_DELAY,
#         move_time=mas_island_event.REVEAL_ANIM_1_DURATION - mas_island_event.REVEAL_ANIM_DELAY
#     ) zorder mas_island_event.DEF_SCREEN_ZORDER with mas_island_event.REVEAL_FADE_TRANSITION
#     $ renpy.pause(mas_island_event.REVEAL_ANIM_1_DURATION - mas_island_event.REVEAL_TRANSITION_TIME - mas_island_event.REVEAL_FADEIN_TIME, hard=True)

#     show expression islands_disp as islands_disp at mas_islands_final_reveal_trans_2(
#         delay=mas_island_event.REVEAL_ANIM_DELAY,
#         move_time=mas_island_event.REVEAL_ANIM_2_DURATION - mas_island_event.REVEAL_ANIM_DELAY
#     ) zorder mas_island_event.DEF_SCREEN_ZORDER with mas_island_event.REVEAL_FADE_TRANSITION
#     $ renpy.pause(mas_island_event.REVEAL_ANIM_2_DURATION - mas_island_event.REVEAL_TRANSITION_TIME - mas_island_event.REVEAL_FADEIN_TIME, hard=True)

#     show expression islands_disp as islands_disp at mas_islands_final_reveal_trans_3(
#         delay=mas_island_event.REVEAL_ANIM_DELAY,
#         move_time=mas_island_event.REVEAL_ANIM_3_1_DURATION - mas_island_event.REVEAL_ANIM_DELAY,
#         zoom_time=mas_island_event.REVEAL_ANIM_3_2_DURATION
#     ) zorder mas_island_event.DEF_SCREEN_ZORDER with mas_island_event.REVEAL_FADE_TRANSITION
#     $ renpy.pause(mas_island_event.REVEAL_ANIM_3_1_DURATION + mas_island_event.REVEAL_ANIM_3_2_DURATION - mas_island_event.REVEAL_TRANSITION_TIME, hard=True)

#     $ renpy.pause(mas_island_event.REVEAL_OVERVIEW_DURATION, hard=True)
#     $ mas_hotkeys.no_window_hiding = False
#     $ mas_OVLShow()
#     $ mas_DropShield_core()
#     $ mas_RaiseShield_dlg()

#     return

# label mas_monika_islands_final_reveal.zoom_in:
#     show expression islands_disp as islands_disp at mas_islands_final_reveal_trans_4(
#         delay=0.0,
#         zoom_time=mas_island_event.REVEAL_ANIM_4_DURATION
#     ) zorder mas_island_event.DEF_SCREEN_ZORDER
#     $ renpy.pause(mas_island_event.REVEAL_ANIM_4_DURATION - mas_island_event.REVEAL_FADEOUT_TIME, hard=True)
#     scene black with mas_island_event.REVEAL_DISSOLVE_TRANSITION

#     return

# label mas_monika_islands_final_reveal.ask_opinion:
#     m 1eksdla "What do you think?~{nw}"
#     $ _history_list.pop()
#     menu:
#         m "What do you think?~{fast}"

#         "It's not too bad.":
#             $ persistent._mas_pm_likes_islands = False
#             $ mas_loseAffectionFraction(min_amount=50, modifier=1.0)
#             $ mas_lockEVL("mas_monika_islands", "EVE")
#             m 2ekd "Oh...{w=0.3}{nw}"
#             extend 2lkc "I guess it's not perfect..."
#             m 2dktpc "But after all that time I've spent working for a place for us, {w=0.1}{nw}"
#             extend 2fktud "you could at least pretend to care."

#             if persistent._mas_pm_cares_island_progress is False:
#                 $ mas_loseAffectionFraction(min_amount=50, modifier=0.5)
#                 m 2dktsc "..."
#                 m 2gftpc "Although, what did I expect...{w=0.3}{nw}"
#                 extend 2eftud "you have said you don't care before."
#                 m 2dstdc "Forget, {w=0.3}{nw}"
#                 extend 2mstdc "this was a waste of time. {w=0.3}{nw}"
#                 extend 2tsc "For both of us."

#             else:
#                 m 2dktsc "It hurts, [player]... {w=0.3}It really, {w=0.1}{i}really{/i} hurts."
#                 m 2fftdd "You know what? {w=0.1}Forget. {w=0.3}{nw}"
#                 extend 2mftdc "It was a mistake from the start."

#             # TODO: reference monika_sweatercurse?

#         "You did an amazing job!":
#             $ persistent._mas_pm_likes_islands = True
#             $ mas_gainAffection(10, bypass=True)
#             m 1wuo "Really? {w=0.3}{nw}"
#             extend 2suo "You can't imagine how much that means to me, [player]!"
#             m 2fktpa "I'm so, {w=0.1}{i}so{/i} glad you liked it."

#             if persistent._mas_pm_cares_island_progress is False:
#                 $ mas_gainAffection(5, bypass=True)
#                 m 3rktdc "You've got me a bit worried before when you said you don't care about our islands..."
#                 m 1eka "It makes me incredibly happy you've changed your mind."

#             elif persistent._mas_pm_cares_island_progress:
#                 $ mas_gainAffection(5, bypass=True)
#                 m 3fktda "It's only because of your everlasting love and support I was able to finish this."

#             m 3hublb "Thanks for being my inspiration, [mas_get_player_nickname()]~"

#     return


label mas_islands(
    fade_in=True,
    fade_out=True,
    raise_shields=True,
    drop_shields=True,
    enable_interaction=True,
    check_progression=False,
    **spaceroom_kwargs
):
    # Sanity check
    if persistent._mas_islands_start_lvl is None or not mas_canShowIslands(False):
        return

    python:
        # NOTE: We can't progress filter here, it looks bad
        spaceroom_kwargs.setdefault("progress_filter", False)
        # Always scene change unless asked not to
        spaceroom_kwargs.setdefault("scene_change", True)
        is_done = False
        islands_displayable = mas_island_event.get_islands_displayable(
            enable_interaction=enable_interaction,
            check_progression=check_progression
        )
        renpy.start_predict(islands_displayable)

    if fade_in:
        # HACK: Show the disp so we can fade in
        # fix it in r7 where you can show/call screens with transitions
        scene
        show expression islands_displayable as islands_background onlayer screens zorder mas_island_event.DEF_SCREEN_ZORDER
        with Fade(0.5, 0, 0.5)
        hide islands_background onlayer screens with None

    if raise_shields:
        python:
            mas_OVLHide()
            mas_RaiseShield_core()
            disable_esc()
            mas_hotkeys.no_window_hiding = True

    if enable_interaction:
        # If this is an interaction, we call the screen so
        # the user can see the parallax effect + events
        while not is_done:
            hide screen mas_islands
            call screen mas_islands(islands_displayable)
            show screen mas_islands(islands_displayable, show_return_button=False)

            if _return is False:
                $ is_done = True

            elif _return is not True and renpy.has_label(_return):
                call expression _return

    else:
        # Otherwise just show it as a static image
        show screen mas_islands(islands_displayable, show_return_button=False)

    if drop_shields:
        python:
            mas_hotkeys.no_window_hiding = False
            enable_esc()
            mas_MUINDropShield()
            mas_OVLShow()

    if fade_out:
        hide screen mas_islands
        # HACK: Show the disp so we can fade out of it into spaceroom,
        # fix it in r7 where you can hide screens with transitions
        show expression islands_displayable as islands_background onlayer screens zorder mas_island_event.DEF_SCREEN_ZORDER with None
        call spaceroom(**spaceroom_kwargs)
        hide islands_background onlayer screens
        with Fade(0.5, 0, 0.5)

    python:
        renpy.stop_predict(islands_displayable)
        del islands_displayable, is_done
    return


label mas_island_upsidedownisland:
    if persistent._mas_o31_in_o31_mode and random.random() < 0.3:
        jump mas_island_spooky_ambience

    m "Oh, that."
    m "I guess you're wondering why that island is upside down, right?"
    m "Well...I was about to fix it until I took another good look at it."
    m "It looks surreal, doesn't it?"
    m "I just feel like there's something special about it."
    m "It's just...mesmerizing."
    return

label mas_island_glitchedmess:
    m "Oh, that."
    m "It's something I'm currently working on."
    m "It's still a huge mess, though. I'm still trying to figure it all out."
    m "In due time, I'm sure I'll get better at coding!"
    m "Practice makes perfect after all, right?"
    return

label mas_island_cherry_blossom_tree:
    python:

        if not renpy.store.seen_event("mas_island_cherry_blossom1"):

            renpy.call("mas_island_cherry_blossom1")

        else:
            _mas_cherry_blossom_events = [
                "mas_island_cherry_blossom1",
                "mas_island_cherry_blossom3",
                "mas_island_cherry_blossom4"
            ]

            if not mas_island_event.is_winter_weather():
                _mas_cherry_blossom_events.append("mas_island_cherry_blossom2")

            renpy.call(renpy.random.choice(_mas_cherry_blossom_events))

    return

label mas_island_cherry_blossom1:
    if mas_island_event.is_winter_weather():
        m "This tree may look dead right now...but when it blooms, it's gorgeous."

    else:
        m "It's a beautiful tree, isn't it?"

    m "It's called a Cherry Blossom tree; they're native to Japan."
    m "Traditionally, when the flowers are in bloom, people would go flower viewing and have a picnic underneath the trees."
    m "Well, I didn't choose this tree because of tradition."
    m "I chose it because it's lovely and pleasing to look at."
    m "Just staring at the falling petals is awe-inspiring."

    if mas_island_event.is_winter_weather():
        m "When it's blooming, that is."
        m "I can't wait until we get the chance to experience that, [player]."

    return

label mas_island_cherry_blossom2:
    m "Did you know you can eat the flower petals of a Cherry Blossom tree?"
    m "I don't know the taste myself, but I'm sure it can't be as sweet as you."
    m "Ehehe~"
    return

label mas_island_cherry_blossom3:
    m "You know, the tree is symbolic like life itself."
    m "Beautiful, but short-lived."
    m "But with you here, it's always blooming beautifully."

    if mas_island_event.is_winter_weather():
        m "Even if it's bare now, it'll blossom again soon."

    m "Know that I'll always be grateful to you for being in my life."
    m "I love you, [player]~"
    # manually handle the "love" return key
    $ mas_ILY()
    return

label mas_island_cherry_blossom4:
    m "You know what'd be nice to drink under the Cherry Blossom tree?"
    m "A little sake~"
    m "Ahaha! I'm just kidding."
    m "I'd rather have tea or coffee."

    if mas_island_event.is_winter_weather():
        m "Or hot chocolate, even. It'd certainly help with the cold."
        m "Of course, even if that failed, we could always cuddle together...{w=0.5} That'd be really romantic~"

    else:
        m "But, it'd be nice to watch the falling petals with you."
        m "That'd be really romantic~"

    return

label mas_island_sky:
    python:

        if mas_current_background.isFltDay():
            _mas_sky_events = [
                "mas_island_day1",
                "mas_island_day2",
                "mas_island_day3"
            ]

        else:
            _mas_sky_events = [
                "mas_island_night1",
                "mas_island_night2",
                "mas_island_night3"
            ]

        _mas_sky_events.append("mas_island_daynight1")
        _mas_sky_events.append("mas_island_daynight2")

        renpy.call(renpy.random.choice(_mas_sky_events))

    return

label mas_island_day1:
    #NOTE: this ordering is key, during winter we only use snow covered islands with clear sky
    # so Winter path needs to be first
    if mas_island_event.is_winter_weather():
        m "What a beautiful day today."
        m "Perfect for taking a walk to admire the scenery."
        m "...Huddled together, so as to stave off the cold."
        m "...With some nice hot drinks to help keep us warm."

    elif mas_is_raining:
        m "Aww, I would've liked to do some reading outdoors."
        m "But I'd rather avoid getting my books wet..."
        m "Soggy pages are a pain to deal with."
        m "Another time, maybe."

    elif mas_current_weather == mas_weather_overcast:
        m "Reading outside with this weather wouldn't be too bad, but it could rain at any moment."
        m "I'd rather not risk it."
        m "Don't worry, [player]. We'll do it some other time."

    else:
        m "It's a nice day today."

        if mas_island_event._is_unlocked("decal_tree"):
            m "This weather would be good for a little book reading under the Cherry Blossom tree right, [player]?"

        else:
            m "This weather would be good for a little book reading outside right, [player]?"

        m "Lying under the shade while reading my favorite book."
        m "...Along with a snack and your favorite drink on the side."
        m "Ahh, that'd be really nice to do~"

    return

label mas_island_day2:
    #NOTE: this ordering is key, during winter we only use snow covered islands with clear sky
    # so Winter path needs to be first
    if mas_island_event.is_winter_weather():
        m "Have you ever made a snow angel, [player]?"
        m "I've tried in the past, but never had much success..."
        m "It's a lot harder than it looks like."
        m "I bet we'd have a lot of fun, even if whatever we make doesn't end up looking like an angel."
        m "It's just a matter of being a bit silly, you know?"

    elif mas_island_event.is_cloudy_weather():
        m "Going outdoors with this kind of weather doesn't look very appealing..."
        m "Maybe if I had an umbrella I'd feel more comfortable."
        m "Imagine both of us, shielded from the rain, inches apart."
        m "Staring into each other's eyes."
        m "Then we start leaning closer and closer until we're almost-"
        m "I think you can finish that thought yourself, [player]~"

    else:
        m "The weather looks nice."
        m "This would definitely be the best time to have a picnic."
        m "We even have a great view to accompany it with!"
        m "Wouldn't it be nice?"

        if mas_island_event._is_unlocked("decal_tree"):
            m "Eating under the Cherry Blossom tree."

        m "Adoring the scenery around us."
        m "Enjoying ourselves with each other's company."
        m "Ahh, that'd be fantastic~"

    return

label mas_island_day3:
    if mas_is_raining and not mas_isWinter():
        m "It's raining pretty heavily..."
        m "I wouldn't want to be outside now."
        m "Though being indoors at a time like this feels pretty cozy, don't you think?"

    else:
        m "It's pretty peaceful outside."

        if mas_island_event.is_winter_weather():
            m "We could have a snowball fight, you know."
            m "Ahaha, that'd be so much fun!"
            m "I bet I could land a shot on you a few islands away."
            m "Some healthy competition never hurt anyone, right?"

        else:
            m "I wouldn't mind lazing around in the grass right now..."
            m "With your head resting on my lap..."
            m "Ehehe~"

    return

label mas_island_night1:
    m "While it's nice to be productive during the day, there's something so peaceful about the night."
    m "The sounds of crickets chirping mixed with a gentle breeze is so relaxing."
    m "You'd hold me on a night like that, right~"
    return

label mas_island_night2:
    if not mas_isWinter() and mas_island_event.is_cloudy_weather():
        m "Too bad we can't see the stars tonight..."
        m "I would've loved to gaze at the cosmos with you."
        m "That's alright though, we'll get to see it some other time, then."

    else:
        if seen_event('monika_stargazing'):
            m "Aren't the stars so beautiful, [player]?"
            m "Although, this isn't {i}quite{/i} what I had in mind when I mentioned stargazing before..."
            m "As nice as they are to look at, the part that I want to experience most is being with you, holding each other tight while we lay there."
            m "Someday, [player].{w=0.3} Someday."

        else:
            m "Have you ever gone stargazing, [mas_get_player_nickname()]?"
            m "Taking some time out of your evening to look at the night sky and to just stare at the beauty of the sky above..."
            m "It's surprisingly relaxing, you know?"
            m "I've found that it can really relieve stress and clear your head..."
            m "And seeing all kinds of constellations in the sky just fills your mind with wonder."
            m "Of course, it really makes you realize just how small we are in the universe."
            m "Ahaha..."

    return

label mas_island_night3:
    if not mas_isWinter() and mas_island_event.is_cloudy_weather():
        m "Cloudy weather is kind of depressing, don't you think?"
        m "Especially at nighttime, when it hides the stars away from our view."
        m "It's such a shame, really..."

    else:
        m "What a beautiful night!"

        if mas_island_event.is_winter_weather():
            m "There's just something about a cold, crisp night that I love."
            m "The contrast of the dark sky and the land covered in snow is really breathtaking, don't you think?"
        else:
            m "If I could, I'd add fireflies."
            m "Their lights complement the night sky, it's a pretty sight."
            m "Improve the ambience a little, you know?"

    return

label mas_island_daynight1:
    m "Maybe I should add more shrubs and trees."
    m "Make the islands prettier you know?"
    m "I just have to find the right flowers and foliage to go with it."
    m "Or maybe each island should have its own set of plants so that everything will be different and have variety."
    m "I'm getting excited thinking about it~"
    return

label mas_island_daynight2:
    # aurora borealis
    m "{i}~Windmill, windmill for the land~{/i}"

    # a-aurora borealis
    m "{i}~Turn forever hand in hand~{/i}"

    # aurora borealis
    m "{i}~Take it all in on your stride~{/i}"

    # at this time of day?
    m "{i}~It is ticking, falling down~{/i}"

    # aurora borealis
    m "{i}~Love forever, love is free~{/i}"

    # a-aurora borealis
    m "{i}~Let's turn forever, you and me~{/i}"

    # in this part of the country? Yes
    m "{i}~Windmill, windmill for the land~{/i}"

    m "Ehehe, don't mind me, I just wanted to sing out of the blue~"
    return

label mas_island_shimeji:
    m "Ah!"
    m "How'd she get there?"
    m "Give me a second, [player].{w=0.2}.{w=0.2}.{w=0.2}{nw}"
    $ islands_displayable.remove(mas_island_event.other_disp_map["other_shimeji"])
    m "All done!"
    m "Don't worry, I just moved her to a different place."
    return

label mas_island_bookshelf:
    python:

        _mas_bookshelf_events = [
            "mas_island_bookshelf1",
            "mas_island_bookshelf2"
        ]

        renpy.call(renpy.random.choice(_mas_bookshelf_events))

    return

label mas_island_bookshelf1:
    #NOTE: this ordering is key, during winter we only use snow covered islands with clear sky
    # so Winter path needs to be first
    if mas_island_event.is_winter_weather():
        m "That bookshelf might not look terribly sturdy, but I'm sure it can weather a little snow."
        m "It's the books that worry me a bit."
        m "I just hope they don't get too damaged..."

    elif mas_island_event.is_cloudy_weather():
        m "At times like this, I wish I would've kept my books indoors..."
        m "Looks like we'll just have to wait for better weather to read them."
        m "In the meantime..."
        m "How about cuddling a bit, [player]?"
        m "Ehehe~"

    else:
        m "Some of my favorite books are in there."
        m "{i}Fahrenheit 451{/i}, {i}Hard-Boiled Wonderland{/i}, {i}Nineteen Eighty-Four{/i}, and a few others."
        m "Maybe we can read them together sometime~"

    return

label mas_island_bookshelf2:
    #NOTE: this ordering is key, during winter we only use snow covered islands with clear sky
    # so Winter path needs to be first
    if mas_island_event.is_winter_weather():
        m "You know, I wouldn't mind doing some reading outside even if there is a bit of snow."
        m "Though I wouldn't venture out without a warm coat, a thick scarf, and a snug pair of gloves."
        m "I guess turning the pages might be a bit hard that way, ahaha..."
        m "But I'm sure we'll manage somehow."
        m "Isn't that right, [player]?"

    elif mas_island_event.is_cloudy_weather():
        m "Reading indoors with rain just outside the window is pretty relaxing."
        m "If only I hadn't left the books outside..."
        m "I should probably bring some in here when I get the chance."
        m "I'm certain we can find other things to do meanwhile, right [player]?"

    else:
        m "Reading outdoors is a nice change of pace, you know?"
        m "I'd take a cool breeze over a stuffy library any day."
        m "Maybe I should add a table underneath the Cherry Blossom tree."
        m "It'd be nice to enjoy a cup of coffee with some snacks to go alongside my book reading."
        m "That'd be wonderful~"

    return

label mas_island_distant_islands:
    if persistent._mas_o31_in_o31_mode:
        jump mas_island_spooky_ambience

    return

label mas_island_spooky_ambience:
    m "{i}It was a dark and stormy night...{/i}"
    m "Ehehe~ This is the perfect time of year for spooky stories, isn't it?"
    m "If you're in the mood, we should read some together."
    m "Although, I don't mind just enjoying the ambience with you for now."

    return

label mas_island_bloodfall:
    m "I'm pretty proud of that waterfall there. It was already looking pretty surreal being upside-down."
    m "All I really had to do was change the value of the water to #641F21, and--{nw}"
    $ _history_list.pop()
    m "Wait, I don't want to ruin the magic for you!{w=0.2} Forget I said that, please!"

    return

label mas_island_pumpkins:
    m "There's nothing that reminds me of Halloween quite as much as pumpkins."
    m "I thought it would be so cozy to have a bunch of them around my reading nook."
    m "It's a bit chilly in the rain, but don't you think it would be nice to put on some sweaters and snuggle up together?"
    m "Maybe I could make some flavored coffee to enhance the mood even more."

    return

label mas_island_gravestones:
    if mas_safeToRefDokis():
        m "What?"
        m "...{w=0.2}What tombstones? {w=0.2}I'm not sure what you're talking about."
        m "Are you...{w=0.2}pfft--"
        m "Ahaha!"
        m "Sorry, I couldn't resist."
        m "It would be pretty spooky if those three were still haunting our happy ending, wouldn't it?"

    else:
        m "Ehehe...I'm not sure if those decorations are entirely tasteful."
        m "I was thinking, though...{w=0.2}Halloween is a time when some cultures honor the dead."
        m "Sure, there are a lot of spooky stories about the dead rising, or ghosts haunting people..."
        m "But there's a side of this holiday about remembering, isn't there?"
        m "I guess I just thought I shouldn't leave them out."

    return


# TODO: Allow to hide ui with H and mouse 2 clicks w/o globals
screen mas_islands(islands_displayable, show_return_button=True):
    style_prefix "island"
    layer "screens"
    zorder mas_island_event.DEF_SCREEN_ZORDER

    if show_return_button:
        key "K_ESCAPE" action Return(False)

    add islands_displayable

    if show_return_button:
        # Unsure why, but w/o a hbox renpy won't apply the style prefix
        hbox:
            align (0.5, 0.98)
            textbutton _("Go Back"):
                action Return(False)

# screen mas_islands_background:

#     add mas_island_event.getBackground()

#     if _mas_island_shimeji:
#         add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
#             xpos 935
#             ypos 395
#             zoom 0.5

# screen mas_show_islands():
#     style_prefix "island"
#     imagemap:

#         ground mas_island_event.getBackground()

#         hotspot (11, 13, 314, 270) action Return("mas_island_upsidedownisland") # island upside down
#         hotspot (403, 7, 868, 158) action Return("mas_island_sky") # sky
#         hotspot (699, 347, 170, 163) action Return("mas_island_glitchedmess") # glitched house
#         hotspot (622, 269, 360, 78) action Return("mas_island_cherry_blossom_tree") # cherry blossom tree
#         hotspot (716, 164, 205, 105) action Return("mas_island_cherry_blossom_tree") # cherry blossom tree
#         hotspot (872, 444, 50, 30) action Return("mas_island_bookshelf") # bookshelf

#         if _mas_island_shimeji:
#             hotspot (935, 395, 30, 80) action Return("mas_island_shimeji") # Mini Moni

#     if _mas_island_shimeji:
#         add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
#             xpos 935
#             ypos 395
#             zoom 0.5

#     hbox:
#         yalign 0.98
#         xalign 0.96
#         textbutton _mas_toggle_frame_text action [ToggleVariable("_mas_island_window_open"),ToggleVariable("_mas_toggle_frame_text","Open Window", "Close Window") ]
#         textbutton "Go Back" action Return(False)


# Defining a new style for buttons, because other styles look ugly

# properties for these island view buttons
style island_button is generic_button_light:
    xysize (205, None)
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_dark is generic_button_dark:
    xysize (205, None)
    ypadding 5
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style island_button_text is generic_button_text_light:
    font gui.default_font
    size gui.text_size
    xalign 0.5
    kerning 0.2
    outlines []

style island_button_text_dark is generic_button_text_dark:
    font gui.default_font
    size gui.text_size
    xalign 0.5
    kerning 0.2
    outlines []

# mini moni ATL
# transform moni_sticker_mid:
#     block:
#         function randomPauseMonika
#         parallel:
#             sticker_move_n
#         repeat
