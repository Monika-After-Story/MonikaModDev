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
# (e.g. either bookshelf or bushes at lvl X, but both at lvl X+Y)
# that's so every player gets a bit different progression.
# Bear in mind, if you decide to add a new item, you'll need an update script
default persistent._mas_islands_unlocks = store.mas_island_event._IslandsImgDataHolder.getDefaultUnlocks()


### initialize the island images
init 1 python:
    ## NOTE: we assume 2 things:
    #   - we have write access to teh mod_assets folder
    #   - the existing pngs dont exist yet
    #
    #   if for some reason we fail to convert the files into images
    #   then we must backout of showing the event.
    #
    #   NOTE: other things to note:
    #       on o31, we cannot have islands event
    mas_decoded_islands = store.mas_island_event.decodeImages()
    mas_cannot_decode_islands = not mas_decoded_islands


init -25 python in mas_island_event:
    import random
    import itertools
    import functools
    import weakref
    from zipfile import ZipFile

    import store
    import store.mas_dockstat as mds
    import store.mas_ics as mis
    from store import (
        persistent,
        mas_utils,
        mas_weather,
        Transform,
        LiveComposite,
        MASWeatherMap,
        MASFilterWeatherDisplayableCustom,
        MASFilterWeatherDisplayable
    )
    from store.mas_parallax import (
        ParallaxSprite,
        ParallaxDecal
    )

    DEF_PROGRESS = -1
    MAX_PROGRESS_ENAM = 4
    MAX_PROGRESS_LOVE = 9
    PROGRESS_FACTOR_ENAM = 4
    PROGRESS_FACTOR_LOVE = 5

    # These're being populated later once we decode the imgs
    island_disp_map = dict()
    decal_disp_map = dict()
    bg_disp_map = dict()
    overlay_disp_map = dict()

    # setup the docking station we are going to use here
    islands_station = store.MASDockingStation(mis.ISLANDS_FOLDER)

    class _IslandsImgDataHolder(object):
        """
        A generalised abstraction around raw data for the islands sprites
        """
        TYPE_ISLAND = "isld"
        TYPE_DECAL = "decal"
        TYPE_BG = "bg"
        TYPE_OVERLAY = "overlay"
        TYPES = frozenset(
            (
                TYPE_ISLAND,
                TYPE_DECAL,
                TYPE_BG,
                TYPE_OVERLAY
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
                        - 'isld_###'
                        - 'decal_###'
                        - 'bg_###'
                        - 'overlay_###'
                        where ### is something unique
                type_ - type of this sprite, if None, we automatically get it from the id
                    (Default: None)
                default_unlocked - whether or not this sprite is unlocked from the get go
                    (Default: False)
                fp_map - the map of the images for this sprite, if None, we automatically generate it
                    (Default: None)
                partial_disp - functools.partial of the displayable for this sprite
                    (Default: None)
            """
            if id_.split(self.DELIM)[0] not in self.TYPES:
                raise Exception(
                    "Bad id format. Supported formats for id: {}, got: {}".format(
                        ", ".join("'{}_###'".format(t) for t in self.TYPES),
                        id_
                    )
                )
            self.id = id_
            if type_ is not None:
                if type_ not in self.TYPES:
                    raise Exception("Bad type. Allowed types: {}, got: {}.".format(self.TYPES, type_))

            else:
                type_ = self._getType()
            self.type = type_
            self.default_unlocked = default_unlocked
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
            # FIXME: Use f-strings with py3 pls
            fp_parts = self.id.split(self.DELIM)
            # TODO: this should be proper fp updates, not this temp fix
            suffix = "s" if fp_parts[0] != "bg" else ""
            return {
                "d": "{}{}/{}/d.obj".format(fp_parts[0], suffix, fp_parts[1]),
                "d_r": "{}{}/{}/d_r.obj".format(fp_parts[0], suffix, fp_parts[1]),
                "d_s": "{}{}/{}/d_s.obj".format(fp_parts[0], suffix, fp_parts[1]),
                "n": "{}{}/{}/n.obj".format(fp_parts[0], suffix, fp_parts[1]),
                "n_r": "{}{}/{}/n_r.obj".format(fp_parts[0], suffix, fp_parts[1]),
                "n_s": "{}{}/{}/n_s.obj".format(fp_parts[0], suffix, fp_parts[1])
            }

        @classmethod
        def getDataFor(cls, id_):
            """
            Returns data for an id

            OUT:
                _IslandsImgDataHolder
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
        def getFPsForType(cls, type_):
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


    # NOTE: As you can see ParallaxDecal aren't being passed in partials, they are dynamically added later
    # during composite image building
    # NOTE: Use functools.partial instead of renpy.partial because the latter has an argument conflict. Smh Tom
    # Islands
    _IslandsImgDataHolder(
        "isld_0",
        default_unlocked=True,
        partial_disp=functools.partial(
            ParallaxSprite,
            x=0,
            y=624,
            z=10,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_1",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=463,
            y=373,
            z=40,
            function=None,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_2",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=255,
            y=289,
            z=90,
            function=None,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_3",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=262,
            y=145,
            z=130,
            function=None,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_4",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=0,
            y=0,
            z=150,
            on_click="mas_island_upsidedownisland"
        )
    )
    _IslandsImgDataHolder(
        "isld_5",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=996,
            y=184,
            z=50,
            function=None,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_6",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=912,
            y=46,
            z=200,
            function=None,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_7",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=439,
            y=84,
            z=250,
            function=None,
            on_click=True
        )
    )
    _IslandsImgDataHolder(
        "isld_8",
        partial_disp=functools.partial(
            ParallaxSprite,
            x=484,
            y=54,
            z=220,
            on_click=True
        )
    )
    # Decals
    _IslandsImgDataHolder(
        "decal_bookshelf",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=407,
            y=64,
            z=4,
            on_click="mas_island_bookshelf"
        )
    )
    _IslandsImgDataHolder(
        "decal_bushes",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=348,
            y=73,
            z=5
        )
    )
    _IslandsImgDataHolder(
        "decal_house",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=245,
            y=-48,
            z=1
        )
    )
    _IslandsImgDataHolder(
        "decal_tree",
        partial_disp=functools.partial(
            ParallaxDecal,
            x=149,
            y=-228,
            z=3,
            on_click="mas_island_cherry_blossom_tree"
        )
    )
    _IslandsImgDataHolder(
        "decal_glitch",
        fp_map={},
        partial_disp=functools.partial(
            ParallaxDecal,
            x=25,
            y=100,
            z=2,
            on_click="mas_island_glitchedmess"
        )
    )
    GLITCH_FPS = (
        "glitch/g_0.obj",
        "glitch/g_1.obj",
        "glitch/g_2.obj",
        "glitch/g_3.obj",
        "glitch/g_4.obj",
        "glitch/g_5.obj",
        "glitch/g_6.obj"
    )
    # BGs
    _IslandsImgDataHolder(
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
    _IslandsImgDataHolder(
        "overlay_rain",
        default_unlocked=True,
        fp_map={
            "d": "overlays/rain/d.obj",
            "n": "overlays/rain/n.obj"
        },
        partial_disp=functools.partial(
            MASFilterWeatherDisplayable,
            use_fb=True
        )
    )
    _IslandsImgDataHolder(
        "overlay_snow",
        default_unlocked=True,
        fp_map={
            "d": "overlays/snow/d.obj",
            "n": "overlays/snow/n.obj"
        },
        partial_disp=functools.partial(
            MASFilterWeatherDisplayable,
            use_fb=True
        )
    )


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
            return mfwm.fw_get(store.mas_sprites.get_filter(), store.mas_weather_snow)

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

        pkg = islands_station.getPackage("project_or")

        if not pkg:
            mas_utils.writelog(err_msg.format("Missing package"))
            return False

        pkg_data = islands_station.unpackPackage(pkg, pkg_slip=mis.ISLAND_PKG_CHKSUM)

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
                    img = store.MASImageData(raw_data, name + ".png")
                    path_map[sprite_type] = img

        try:
            with ZipFile(pkg_data, "r") as zip_file:
                isld_map = _IslandsImgDataHolder.getFPsForType(_IslandsImgDataHolder.TYPE_ISLAND)
                decal_map = _IslandsImgDataHolder.getFPsForType(_IslandsImgDataHolder.TYPE_DECAL)
                bg_map = _IslandsImgDataHolder.getFPsForType(_IslandsImgDataHolder.TYPE_BG)
                overlay_map = _IslandsImgDataHolder.getFPsForType(_IslandsImgDataHolder.TYPE_OVERLAY)
                # Now override maps to contain imgs instead of img paths
                for map_ in (isld_map, decal_map, bg_map, overlay_map):
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
            _buildDisplayables(isld_map, decal_map, bg_map, overlay_map, glitch_frames)

        return True

    def _buildDisplayables(isld_imgs_maps, decal_imgs_maps, bg_imgs_maps, overlay_imgs_maps, glitch_frames):
        """
        Takes multiple maps with images and builds displayables from them, sets global vars
        NOTE: no sanity checks
        FIXME: py3 update

        IN:
            isld_imgs_maps - the map from island names to raw images map
            decal_imgs_maps - the map from decal names to raw images map
            bg_imgs_maps - the map from bg ids to raw images map
            overlay_imgs_maps - the map from overlay ids to raw images map
            glitch_frames - tuple of glitch raw anim frames
        """
        global island_disp_map, decal_disp_map, bg_disp_map, overlay_disp_map

        # Build the islands
        for isld_name, img_map in isld_imgs_maps.iteritems():
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
                )
            )
            partial_disp = _IslandsImgDataHolder.getDataFor(isld_name).partial_disp
            island_disp_map[isld_name] = partial_disp(disp)

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
                )
            )
            partial_disp = _IslandsImgDataHolder.getDataFor(decal_name).partial_disp
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
                )
            )
            partial_disp = _IslandsImgDataHolder.getDataFor(bg_name).partial_disp
            bg_disp_map[bg_name] = partial_disp(disp)

        # Build the overlays
        for overlay_name, img_map in overlay_imgs_maps.iteritems():
            # Overlays are just dynamic displayables
            partial_disp = _IslandsImgDataHolder.getDataFor(overlay_name).partial_disp
            overlay_disp_map[overlay_name] = partial_disp(
                day=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["d"]
                    }
                ),
                night=MASWeatherMap(
                    {
                        mas_weather.PRECIP_TYPE_DEF: img_map["n"]
                    }
                )
            )

        # Build glitch disp
        def _select_glitch_frame(transform, st, at):
            """
            A function which we use as a transform, updates the child
            """
            redraw = random.uniform(0.3, 1.3)
            next_child = random.choice(glitch_frames)

            transform.child = next_child

            return redraw

        glitch_disp = Transform(child=glitch_frames[0], function=_select_glitch_frame)
        partial_disp = _IslandsImgDataHolder.getDataFor("decal_glitch").partial_disp
        decal_disp_map["decal_glitch"] = partial_disp(glitch_disp)

        return


    # # # START functions for lvl unlocks, head to _handleUnlocks to understand how this works
    def _unlocks_for_lvl_0():
        persistent._mas_islands_unlocks["isld_1"] = True
        persistent._mas_islands_unlocks["isld_8"] = True

    def _unlocks_for_lvl_1():
        persistent._mas_islands_unlocks["isld_2"] = True

    def _unlocks_for_lvl_2():
        persistent._mas_islands_unlocks["decal_tree"] = True

    def _unlocks_for_lvl_3():
        # Unlock only 1, the rest at lvl 5
        if not (
            persistent._mas_islands_unlocks["isld_4"]
            and persistent._mas_islands_unlocks["isld_5"]
        ):
            if bool(random.randint(0, 1)):
                persistent._mas_islands_unlocks["isld_4"] = True

            else:
                persistent._mas_islands_unlocks["isld_5"] = True

    def _unlocks_for_lvl_4():
        persistent._mas_islands_unlocks["decal_glitch"] = True

        # Unlock only 1, the rest at lvl 7
        if not (
            persistent._mas_islands_unlocks["decal_bookshelf"]
            and persistent._mas_islands_unlocks["decal_bushes"]
        ):
            if bool(random.randint(0, 1)):
                persistent._mas_islands_unlocks["decal_bookshelf"] = True

            else:
                persistent._mas_islands_unlocks["decal_bushes"] = True

    def _unlocks_for_lvl_5():
        persistent._mas_islands_unlocks["isld_7"] = True

        # Unlock everything from lvl 3
        persistent._mas_islands_unlocks["isld_4"] = True
        persistent._mas_islands_unlocks["isld_5"] = True

    def _unlocks_for_lvl_6():
        persistent._mas_islands_unlocks["isld_3"] = True
        persistent._mas_islands_unlocks["isld_6"] = True

    def _unlocks_for_lvl_7():
        # Unlock everything from lvl 4
        persistent._mas_islands_unlocks["decal_bookshelf"] = True
        persistent._mas_islands_unlocks["decal_bushes"] = True

    def _unlocks_for_lvl_8():
        # TODO: me
        return

    def _unlocks_for_lvl_9():
        # TODO: me
        return

    # # # END


    def _handleUnlocks():
        """
        Method to unlock various islands features when the player progresses.
        For example: new decals, new islands, new extra events, set persistent vars, etc.
        """
        g = globals()
        for i in range(persistent._mas_islands_progress + 1):
            callback = g.get("_unlocks_for_lvl_{}".format(i), None)
            if callback is not None:
                callback()

    def _advanceProgression():
        """
        Increments the lvl of progression of the islands event,
        it will do nothing if the player hasn't unlocked the islands yet or if
        the current lvl is invalid

        OUT:
            int - current progress lvl
        """
        # If this var is None, then the user hasn't unlocked the event yet
        if persistent._mas_islands_start_lvl is None:
            return persistent._mas_islands_progress

        lvl_difference = store.mas_xp.level() - persistent._mas_islands_start_lvl
        # This should never happen
        # TODO: potentially throw an error here?
        if lvl_difference < 0:
            return persistent._mas_islands_progress

        if store.mas_isMoniEnamored(higher=True):
            if store.mas_isMoniLove(higher=True):
                max_progress = MAX_PROGRESS_LOVE
                progress_factor = PROGRESS_FACTOR_LOVE

            else:
                max_progress = MAX_PROGRESS_ENAM
                progress_factor = PROGRESS_FACTOR_ENAM

            new_progress = min(int(lvl_difference // progress_factor), max_progress)

        else:
            new_progress = DEF_PROGRESS

        # Now set new level
        persistent._mas_islands_progress = min(max(new_progress, persistent._mas_islands_progress), MAX_PROGRESS_LOVE)
        _handleUnlocks()

        return persistent._mas_islands_progress

    def _setupProgression():
        """
        Sets the starting level for islands progression
        """
        if persistent._mas_islands_start_lvl is None:
            persistent._mas_islands_start_lvl = store.mas_xp.level()

    def startProgression():
        """
        Starts islands progression
        """
        if store.mas_isMoniEnamored(higher=True):
            _setupProgression()
            _advanceProgression()

    def _resetProgression():
        """
        Resets island progress
        """
        persistent._mas_islands_start_lvl = None
        persistent._mas_islands_progress = DEF_PROGRESS
        persistent._mas_islands_unlocks = _IslandsImgDataHolder.getDefaultUnlocks()

    def getIslandsDisp(check_progression=True, enable_interaction=True):
        """
        Builds an image for islands and returns it
        NOTE: This is temporary until we split islands into foreground/background
        FIXME: py3 update

        IN:
            check_progression - whether to check for new unlocks or not,
                this might be a little slow
                (Default: True)
            enable_interaction - whether to enable events or not (including parallax effect)
                (Default: True)

        OUT:
            LiveComposite
        """
        # Progress lvl
        if check_progression:
            _advanceProgression()

        sub_displayables = list()

        # Add all unlocked islands
        for key, disp in island_disp_map.iteritems():
            # Just in case we always remove all decals and readd them as needed
            disp._container.remove_all()
            # Toggle events as desired
            disp.toggle_events(enable_interaction)
            # Reset offsets and zoom
            disp.reset_mouse_pos()
            # Reset offsets and zoom
            disp.zoom = disp.min_zoom
            # Add if unlocked
            if persistent._mas_islands_unlocks[key]:
                sub_displayables.append(disp)

        # Add all unlocked decals for islands 1 (other islands don't have any as of now)
        for key in ("decal_bookshelf", "decal_bushes", "decal_house", "decal_tree", "decal_glitch"):
            if persistent._mas_islands_unlocks[key]:
                island_disp_map["isld_1"]._container.add(decal_disp_map[key])

        # Add the bg (we only have one as of now)
        bg_disp = bg_disp_map["bg_def"]
        bg_disp.toggle_events(enable_interaction)
        bg_disp.reset_mouse_pos()
        bg_disp.zoom = bg_disp.min_zoom
        sub_displayables.append(bg_disp)

        # Sort in order from back to front
        sub_displayables.sort(key=lambda sprite: sprite.z, reverse=True)

        # Now add overlays (they are always last)
        if store.mas_is_raining:
            sub_displayables.append(overlay_disp_map["overlay_rain"])

        elif store.mas_is_snowing:
            sub_displayables.append(overlay_disp_map["overlay_snow"])

        def_coords = itertools.repeat((0, 0), len(sub_displayables))
        lc_args = itertools.chain.from_iterable(itertools.izip(def_coords, sub_displayables))

        # Try to make a LiveComposite
        return LiveComposite(
            (renpy.config.screen_width, renpy.config.screen_height),
            *lc_args
        )

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
            flags=EV_FLAG_DEF if mas_decoded_islands else EV_FLAG_HFM
        )
    )

label mas_monika_islands:
    # Sanity check in case of restart and failing to decode
    if not mas_decoded_islands:
        return

    m 1eub "I'll let you admire the scenery for now."
    m 1hub "Hope you like it!"

    # Raise shields
    python:
        mas_OVLHide()
        mas_RaiseShield_core()
        disable_esc()
        renpy.store.mas_hotkeys.no_window_hiding = True

    call mas_islands(force_exp="monika 1eua")

    # 155, 545
    # random chance to get mini moni appear
    # if renpy.random.randint(1,100) == 1:
    #     $ _mas_island_shimeji = True

    # Drop shields
    python:
        store.mas_hotkeys.no_window_hiding = False
        enable_esc()
        mas_MUINDropShield()
        mas_OVLShow()

    m 1eua "I hope you liked it, [mas_get_player_nickname()]~"
    return

label mas_islands(fade_in=True, fade_out=True, check_progression=True, enable_interaction=True, **spaceroom_kwargs):
    # Sanity check
    if persistent._mas_islands_start_lvl is None:
        return

    python:
        # NOTE: We can't progress filter here, it looks bad
        spaceroom_kwargs.setdefault("progress_filter", False)
        is_done = False
        islands_disp = store.mas_island_event.getIslandsDisp(
            check_progression=check_progression,
            enable_interaction=enable_interaction
        )

    # HACK: We show the disp with a tranition first and then show the screen.
    # With r7 we will be able to call screens with transitions,
    # So we better to update this code later
    if fade_in:
        scene
        show expression islands_disp as islands_bg
        with Fade(0.5, 0, 0.5)
        hide islands_bg with None

    if enable_interaction:
        # If this is an interaction, we call the screen so
        # the user can see the parallax effect + events
        while not is_done:
            hide screen mas_islands
            call screen mas_islands(islands_disp)
            show screen mas_islands(islands_disp, show_return_button=False)

            if _return is False:
                $ is_done = True

            elif renpy.has_label(_return):
                call expression _return

    else:
        # Otherwise just show it as a static image
        show screen mas_islands(islands_disp, show_return_button=False)

    if fade_out:
        hide screen mas_islands
        show expression islands_disp as islands_bg zorder MAS_MONIKA_Z*10 with None
        call spaceroom(**spaceroom_kwargs)
        hide islands_bg
        with Fade(0.5, 0, 0.5)

    $ del islands_disp, is_done
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
        m "This weather would be good for a little book reading under the Cherry Blossom tree right, [player]?"
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
    m "Give me a second, [player]..."
    $ _mas_island_shimeji = False
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
    layer "master"
    zorder MAS_MONIKA_Z*10

    add islands_displayable

    if show_return_button:
        # Unsure why, but w/o hbox renpy won't apply the prefix style
        hbox:
            align (0.5, 0.98)
            textbutton _("Go Back"):
                action Return(False)

screen mas_islands_background:

    add mas_island_event.getBackground()

    if _mas_island_shimeji:
        add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
            xpos 935
            ypos 395
            zoom 0.5

screen mas_show_islands():
    style_prefix "island"
    imagemap:

        ground mas_island_event.getBackground()

        hotspot (11, 13, 314, 270) action Return("mas_island_upsidedownisland") # island upside down
        hotspot (403, 7, 868, 158) action Return("mas_island_sky") # sky
        hotspot (699, 347, 170, 163) action Return("mas_island_glitchedmess") # glitched house
        hotspot (622, 269, 360, 78) action Return("mas_island_cherry_blossom_tree") # cherry blossom tree
        hotspot (716, 164, 205, 105) action Return("mas_island_cherry_blossom_tree") # cherry blossom tree
        hotspot (872, 444, 50, 30) action Return("mas_island_bookshelf") # bookshelf

        if _mas_island_shimeji:
            hotspot (935, 395, 30, 80) action Return("mas_island_shimeji") # Mini Moni

    if _mas_island_shimeji:
        add "gui/poemgame/m_sticker_1.png" at moni_sticker_mid:
            xpos 935
            ypos 395
            zoom 0.5

    hbox:
        yalign 0.98
        xalign 0.96
        textbutton _mas_toggle_frame_text action [ToggleVariable("_mas_island_window_open"),ToggleVariable("_mas_toggle_frame_text","Open Window", "Close Window") ]
        textbutton "Go Back" action Return(False)


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
transform moni_sticker_mid:
    block:
        function randomPauseMonika
        parallel:
            sticker_move_n
        repeat
