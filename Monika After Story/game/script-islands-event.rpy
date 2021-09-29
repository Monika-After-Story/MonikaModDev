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
default persistent._mas_islands_unlocks = store.mas_island_event.IslandsImageDefinition.getDefaultUnlocks()


### initialize the island images
init 1:
    #   if for some reason we fail to convert the files into images
    #   then we must backout of showing the event.
    #
    #   NOTE: other things to note:
    #       on o31, we cannot have islands event
    define mas_decoded_islands = store.mas_island_event.decodeImages()
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

# # # Image defination
init -20 python in mas_island_event:
    class IslandsImageDefinition(object):
        """
        A generalised abstraction around raw data for the islands sprites
        """
        TYPE_ISLAND = "island"
        TYPE_DECAL = "decal"
        TYPE_BG = "bg"
        TYPE_OVERLAY = "overlay"
        TYPE_OBJECT = "obj"# This is basically for everything else
        TYPES = frozenset(
            (
                TYPE_ISLAND,
                TYPE_DECAL,
                TYPE_BG,
                TYPE_OVERLAY,
                TYPE_OBJECT
            )
        )

        DELIM = "_"

        _data_map = dict()

        def __init__(
            self,
            id_,
            type_=None,
            default_unlocked=False,
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
                        - 'obj_###'
                        where ### is something unique
                type_ - type of this sprite, if None, we automatically get it from the id
                    (Default: None)
                default_unlocked - whether or not this sprite is unlocked from the get go
                    (Default: False)
                fp_map - the map of the images for this sprite, if None, we automatically generate it
                    NOTE: after decoding this will point to a loaded ImageData object instead of a failepath
                    (Default: None)
                partial_disp - functools.partial of the displayable for this sprite
                    (Default: None)
            """
            if id_.split(self.DELIM)[0] not in self.TYPES:
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
            self.fp_map = fp_map if fp_map is not None else self._buildFPMap()
            self.partial_disp = partial_disp

            self._data_map[id_] = self

        def _getType(self):
            """
            Private method to get type of this sprite if it hasn't been passed in

            OUT:
                str
            """
            return self.id.split(self.DELIM)[0]

        def _buildFPMap(self):
            """
            Private method to build filepath map if one hasn't been passed in

            OUT:
                dict
            """
            filepath_fmt = "{prefix}s/{name}/{suffix}"
            prefix, name = self.id.split(self.DELIM)
            # Otherlays are a bit different
            if self.type == self.TYPE_OVERLAY:
                suffixes = ("d", "n")

            else:
                suffixes = ("d", "d_r", "d_s", "n", "n_r", "n_s", "s", "s_r", "s_s")

            # FIXME: Use f-strings with py3 pls
            return {
                suffix: filepath_fmt.format(
                    prefix=prefix,
                    name=name,
                    suffix=suffix
                )
                for suffix in suffixes
            }

        @classmethod
        def getDataFor(cls, id_):
            """
            Returns data for an id

            OUT:
                IslandsImageDefinition
            """
            return cls._data_map[id_]

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
    IslandsImageDefinition(
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
    IslandsImageDefinition(
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
    IslandsImageDefinition(
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
    IslandsImageDefinition(
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
    IslandsImageDefinition(
        "island_4",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=-15,
            y=-15,
            z=125,
            on_click="mas_island_upsidedownisland"
        )
    )
    IslandsImageDefinition(
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
    IslandsImageDefinition(
        "island_6",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=912,
            y=46,
            z=200,
            function=None,
            on_click=True
        )
    )
    IslandsImageDefinition(
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
    IslandsImageDefinition(
        "island_8",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=484,
            y=54,
            z=220,
            on_click=True
        )
    )
    # Decals
    IslandsImageDefinition(
        "decal_bookshelf",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=358,
            y=55,
            z=4,
            on_click="mas_island_bookshelf"
        )
    )
    IslandsImageDefinition(
        "decal_bushes",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=305,
            y=63,
            z=5,
            on_click=True
        )
    )
    IslandsImageDefinition(
        "decal_house",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=215,
            y=-44,
            z=1
        )
    )
    IslandsImageDefinition(
        "decal_tree",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=130,
            y=-200,
            z=3,
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
    IslandsImageDefinition(
        "decal_glitch",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxDecal,
            x=216,
            y=-54,
            z=2,
            on_click="mas_island_glitchedmess"
        )
    )
    IslandsImageDefinition(
        "obj_shimeji",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxSprite,
            Transform(renpy.easy.displayable("chibika smile"), zoom=0.4),
            x=930,
            y=335,
            z=36,
            function=__chibi_transform_func,
            on_click="mas_island_shimeji"
        )
    )
    # BGs
    IslandsImageDefinition(
        "bg_def",
        default_unlocked=True,
        partial_disp=functools.partial(
            ParallaxSprite,
            x=0,
            y=0,
            z=15000,
            min_zoom=1.1,
            max_zoom=4.1,
            on_click="mas_island_sky"
        )
    )
    # Overlays
    IslandsImageDefinition(
        "overlay_rain",
        default_unlocked=True,
        partial_disp=functools.partial(
            MASFilterWeatherDisplayable,
            use_fb=True
        )
    )
    IslandsImageDefinition(
        "overlay_snow",
        default_unlocked=True,
        partial_disp=functools.partial(
            MASFilterWeatherDisplayable,
            use_fb=True
        )
    )
    IslandsImageDefinition(
        "overlay_thunder",
        default_unlocked=True,
        fp_map={},
        partial_disp=functools.partial(
            renpy.easy.displayable,
            "mas_islands_lightning_overlay"
        )
    )


# # # Main framework
init -25 python in mas_island_event:
    import random
    import functools
    import math
    from zipfile import ZipFile

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
    # TODO: add a few more lvl
    MAX_PROGRESS_LOVE = 7
    PROGRESS_FACTOR = 4

    SHIMEJI_CHANCE = 100
    DEF_SCREEN_ZORDER = 55

    SUPPORTED_FILTERS = frozenset(
        {
            mas_sprites.FLT_DAY,
            mas_sprites.FLT_NIGHT,
            mas_sprites.FLT_SUNSET
        }
    )

    # These're being populated later once we decode the imgs
    island_disp_map = dict()
    decal_disp_map = dict()
    obj_disp_map = dict()
    bg_disp_map = dict()
    overlay_disp_map = dict()

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

    def shouldDecodeImages():
        """
        A united check whether or not we should decode images in this sesh
        """
        # TODO: add more checks here as needed
        return (
            not store.mas_isO31()
            # and (X or not Y)
        )

    def decodeImages():
        """
        Attempts to decode the images

        OUT:
            True upon success, False otherwise
        """
        if not shouldDecodeImages():
            return False

        err_msg = "[ERROR] Failed to decode images: {}.\n"

        pkg = islands_station.getPackage("our_reality")

        if not pkg:
            mas_utils.writelog(err_msg.format("Missing package"))
            return False

        pkg_data = islands_station.unpackPackage(pkg, pkg_slip=mas_ics.ISLAND_PKG_CHKSUM)

        if not pkg_data:
            mas_utils.writelog(err_msg.format("Bad package."))
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
            with ZipFile(pkg_data, "r") as zip_file:
                island_map = IslandsImageDefinition.getFilepathsForType(IslandsImageDefinition.TYPE_ISLAND)
                decal_map = IslandsImageDefinition.getFilepathsForType(IslandsImageDefinition.TYPE_DECAL)
                bg_map = IslandsImageDefinition.getFilepathsForType(IslandsImageDefinition.TYPE_BG)
                overlay_map = IslandsImageDefinition.getFilepathsForType(IslandsImageDefinition.TYPE_OVERLAY)
                # Now override maps to contain imgs instead of img paths
                for map_ in (island_map, decal_map, bg_map, overlay_map):
                    _read_zip(zip_file, map_)

                # Anim frames are handled a bit differently
                glitch_frames = tuple(
                    (store.MASImageData(zip_file.read(fn), fn + ".png") for fn in GLITCH_FPS)
                )

        except Exception as e:
            mas_utils.writelog(err_msg.format(e))
            return False

        else:
            # We loaded the images, now create dynamic displayables
            _buildDisplayables(island_map, decal_map, bg_map, overlay_map, glitch_frames)

        return True

    def _buildDisplayables(island_imgs_maps, decal_imgs_maps, bg_imgs_maps, overlay_imgs_maps, glitch_frames):
        """
        Takes multiple maps with images and builds displayables from them, sets global vars
        NOTE: no sanity checks
        FIXME: py3 update

        IN:
            island_imgs_maps - the map from island names to raw images map
            decal_imgs_maps - the map from decal names to raw images map
            bg_imgs_maps - the map from bg ids to raw images map
            overlay_imgs_maps - the map from overlay ids to raw images map
            glitch_frames - tuple of glitch raw anim frames
        """
        global island_disp_map, decal_disp_map, obj_disp_map, bg_disp_map, overlay_disp_map

        # Build the islands
        for island_name, img_map in island_imgs_maps.iteritems():
            disp = IslandFilterWeatherDisplayable(
                day=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["d"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["d_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["d_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["d_r"]
                    }
                ),
                night=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["n"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["n_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["n_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["n_r"]
                    }
                ),
                sunset=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["s"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["s_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["s_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["s_r"]
                    }
                )
            )
            partial_disp = IslandsImageDefinition.getDataFor(island_name).partial_disp
            island_disp_map[island_name] = partial_disp(disp)

        # Build the decals
        for decal_name, img_map in decal_imgs_maps.iteritems():
            disp = IslandFilterWeatherDisplayable(
                day=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["d"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["d_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["d_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["d_r"]
                    }
                ),
                night=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["n"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["n_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["n_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["n_r"]
                    }
                ),
                sunset=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["s"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["s_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["s_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["s_r"]
                    }
                )
            )
            partial_disp = IslandsImageDefinition.getDataFor(decal_name).partial_disp
            decal_disp_map[decal_name] = partial_disp(disp)

        # Build the bg
        for bg_name, img_map in bg_imgs_maps.iteritems():
            disp = IslandFilterWeatherDisplayable(
                day=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["d"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["d_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["d_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["d_r"]
                    }
                ),
                night=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["n"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["n_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["n_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["n_r"]
                    }
                ),
                sunset=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["s"],
                        mas_weather.PRECIP_TYPE_RAIN: img_map["s_r"],
                        mas_weather.PRECIP_TYPE_SNOW: img_map["s_s"],
                        mas_weather.PRECIP_TYPE_OVERCAST: img_map["s_r"]
                    }
                )
            )
            partial_disp = IslandsImageDefinition.getDataFor(bg_name).partial_disp
            bg_disp_map[bg_name] = partial_disp(disp)

        # Build the overlays
        overlay_speed_map = {
            "overlay_rain": 0.8,
            "overlay_snow": 3.5
        }
        for overlay_name, img_map in overlay_imgs_maps.iteritems():
            # Overlays are just dynamic displayables
            partial_disp = IslandsImageDefinition.getDataFor(overlay_name).partial_disp
            overlay_disp_map[overlay_name] = store.mas_islands_weather_overlay_transform(
                child=partial_disp(
                    day=MASWeatherMap(
                        {
                            mas_weather.PRECIP_TYPE_DEF: img_map["d"]
                        }
                    ),
                    night=MASWeatherMap(
                        {
                            mas_weather.PRECIP_TYPE_DEF: img_map["n"]
                        }
                    ),
                    # sunset=MASWeatherMap(
                    #     {
                    #         mas_weather.PRECIP_TYPE_DEF: img_map["s"]
                    #     }
                    # )
                ),
                speed=overlay_speed_map.get(overlay_name, 1.0)
            )

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
        partial_disp = IslandsImageDefinition.getDataFor("decal_glitch").partial_disp
        decal_disp_map["decal_glitch"] = partial_disp(glitch_disp)

        # Build chibi disp
        partial_disp = IslandsImageDefinition.getDataFor("obj_shimeji").partial_disp
        obj_disp_map["obj_shimeji"] = partial_disp()

        # Build thunder overlay
        partial_disp = IslandsImageDefinition.getDataFor("overlay_thunder").partial_disp
        overlay_disp_map["overlay_thunder"] = partial_disp()

        return

    def _isUnlocked(id_):
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


    # # # START functions for lvl unlocks, head to __handleUnlocks to understand how this works
    # NOTE: Please, keep these private
    def __unlocks_for_lvl_0():
        _unlock("island_1")
        _unlock("island_8")

    def __unlocks_for_lvl_1():
        _unlock("obj_shimeji")
        _unlock("decal_glitch")

    def __unlocks_for_lvl_2():
        _unlock("island_2")

    def __unlocks_for_lvl_3():
        # Unlock only one, the rest at lvl 5
        if (
            not _isUnlocked("island_4")
            and not _isUnlocked("island_5")
        ):
            if bool(random.randint(0, 1)):
                _unlock("island_4")

            else:
                _unlock("island_5")

    def __unlocks_for_lvl_4():
        # Unlock only one, the rest at lvl 6
        if (
            not _isUnlocked("island_6")
            and not _isUnlocked("island_7")
        ):
            if bool(random.randint(0, 1)):
                _unlock("island_6")

            else:
                _unlock("island_7")

    def __unlocks_for_lvl_5():
        _unlock("decal_bushes")
        # Unlock everything from lvl 3
        _unlock("island_4")
        _unlock("island_5")

    def __unlocks_for_lvl_6():
        _unlock("island_3")
        # Unlock only one, the rest at lvl 7
        if (
            not _isUnlocked("decal_bookshelf")
            and not _isUnlocked("decal_tree")
        ):
            if bool(random.randint(0, 1)):
                _unlock("decal_bookshelf")

            else:
                _unlock("decal_tree")
        # Unlock everything from lvl 4
        _unlock("island_7")
        _unlock("island_6")

    def __unlocks_for_lvl_7():
        # Unlock everything from lvl 6
        _unlock("decal_bookshelf")
        _unlock("decal_tree")

    def __unlocks_for_lvl_8():
        # TODO: me
        # _lock("decal_glitch")
        # _unlock("decal_house")
        # Update monika_why_spaceroom when the islands are finished
        return

    # # # END


    def __handleUnlocks():
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

    def advanceProgression():
        """
        Increments the lvl of progression of the islands event,
        it will do nothing if the player hasn't unlocked the islands yet or if
        the current lvl is invalid
        """
        # If this var is None, then the user hasn't unlocked the event yet
        if persistent._mas_islands_start_lvl is None:
            return

        lvl_difference = store.mas_xp.level() - persistent._mas_islands_start_lvl
        # This should never happen
        if lvl_difference < 0:
            return

        if store.mas_isMoniEnamored(higher=True):
            if store.mas_isMoniLove(higher=True):
                max_progress = MAX_PROGRESS_LOVE

            else:
                max_progress = MAX_PROGRESS_ENAM

            new_progress = min(int(lvl_difference // PROGRESS_FACTOR), max_progress)

        else:
            new_progress = DEF_PROGRESS

        # Now set new level
        persistent._mas_islands_progress = min(max(new_progress, persistent._mas_islands_progress), MAX_PROGRESS_LOVE)
        __handleUnlocks()

        return

    def getProgression():
        """
        Returns current islands progress lvl
        """
        return persistent._mas_islands_progress

    def startProgression():
        """
        Starts islands progression
        """
        if store.mas_isMoniEnamored(higher=True) and persistent._mas_islands_start_lvl is None:
            persistent._mas_islands_start_lvl = store.mas_xp.level()
            advanceProgression()

    def _resetProgression():
        """
        Resets island progress
        """
        persistent._mas_islands_start_lvl = None
        persistent._mas_islands_progress = DEF_PROGRESS
        persistent._mas_islands_unlocks = IslandsImageDefinition.getDefaultUnlocks()

    def getIslandsDisplayable(enable_interaction=True, check_progression=False):
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

        def _reset_parallax_disp(disp):
            # Just in case we always remove all decals and readd them as needed
            disp.clear_decals()
            # Toggle events as desired
            disp.toggle_events(enable_interaction)
            # Reset offsets and zoom
            disp.reset_mouse_pos()
            disp.zoom = disp.min_zoom

        # Progress lvl
        if check_progression:
            advanceProgression()

        sub_displayables = list()

        # Add all unlocked islands
        for key, disp in island_disp_map.iteritems():
            if _isUnlocked(key):
                _reset_parallax_disp(disp)
                sub_displayables.append(disp)

        # Add all unlocked decals for islands 1 (other islands don't have any as of now)
        island_disp_map["island_1"].add_decals(
            *[
                decal_disp_map[key]
                for key in (
                    "decal_bookshelf",
                    "decal_bushes",
                    "decal_house",
                    "decal_tree",
                    "decal_glitch"
                )
                if _isUnlocked(key)
            ]
        )

        if _isUnlocked("obj_shimeji") and renpy.random.randint(1, SHIMEJI_CHANCE) == 1:
            shimeji_disp = obj_disp_map["obj_shimeji"]
            _reset_parallax_disp(shimeji_disp)
            SHIMEJI_CHANCE *= 2
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

        return ParallaxBackground(*sub_displayables)

    def isWinterWeather():
        """
        Checks if the weather on the islands is wintery

        OUT:
            boolean:
                - True if we're using snow islands
                - False otherwise
        """
        return store.mas_is_snowing or store.mas_isWinter()

    def isCloudyWeather():
        """
        Checks if the weather on the islands is cloudy

        OUT:
            boolean:
                - True if we're using overcast/rain islands
                - False otherwise
        """
        return store.mas_is_raining or store.mas_current_weather == store.mas_weather_overcast


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
    m 1eub "I'll let you admire the scenery for now."
    m 1hub "Hope you like it!"

    call mas_islands(force_exp="monika 1eua")

    m 1eua "I hope you liked it, [mas_get_player_nickname()]~"
    return


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
        is_done = False
        islands_displayable = mas_island_event.getIslandsDisplayable(
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

            if not mas_island_event.isWinterWeather():
                _mas_cherry_blossom_events.append("mas_island_cherry_blossom2")

            renpy.call(renpy.random.choice(_mas_cherry_blossom_events))

    return

label mas_island_cherry_blossom1:
    if mas_island_event.isWinterWeather():
        m "This tree may look dead right now...but when it blooms, it's gorgeous."

    else:
        m "It's a beautiful tree, isn't it?"

    m "It's called a Cherry Blossom tree; they're native to Japan."
    m "Traditionally, when the flowers are in bloom, people would go flower viewing and have a picnic underneath the trees."
    m "Well, I didn't choose this tree because of tradition."
    m "I chose it because it's lovely and pleasing to look at."
    m "Just staring at the falling petals is awe-inspiring."

    if mas_island_event.isWinterWeather():
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

    if mas_island_event.isWinterWeather():
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

    if mas_island_event.isWinterWeather():
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
    if mas_island_event.isWinterWeather():
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

        if mas_island_event._isUnlocked("decal_tree"):
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
    if mas_island_event.isWinterWeather():
        m "Have you ever made a snow angel, [player]?"
        m "I've tried in the past, but never had much success..."
        m "It's a lot harder than it looks like."
        m "I bet we'd have a lot of fun, even if whatever we make doesn't end up looking like an angel."
        m "It's just a matter of being a bit silly, you know?"

    elif mas_island_event.isCloudyWeather():
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

        if mas_island_event._isUnlocked("decal_tree"):
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

        if mas_island_event.isWinterWeather():
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
    if not mas_isWinter() and mas_island_event.isCloudyWeather():
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
    if not mas_isWinter() and mas_island_event.isCloudyWeather():
        m "Cloudy weather is kind of depressing, don't you think?"
        m "Especially at nighttime, when it hides the stars away from our view."
        m "It's such a shame, really..."

    else:
        m "What a beautiful night!"

        if mas_island_event.isWinterWeather():
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
    $ islands_displayable.remove(mas_island_event.obj_disp_map["obj_shimeji"])
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
    if mas_island_event.isWinterWeather():
        m "That bookshelf might not look terribly sturdy, but I'm sure it can weather a little snow."
        m "It's the books that worry me a bit."
        m "I just hope they don't get too damaged..."

    elif mas_island_event.isCloudyWeather():
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
    if mas_island_event.isWinterWeather():
        m "You know, I wouldn't mind doing some reading outside even if there is a bit of snow."
        m "Though I wouldn't venture out without a warm coat, a thick scarf, and a snug pair of gloves."
        m "I guess turning the pages might be a bit hard that way, ahaha..."
        m "But I'm sure we'll manage somehow."
        m "Isn't that right, [player]?"

    elif mas_island_event.isCloudyWeather():
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
