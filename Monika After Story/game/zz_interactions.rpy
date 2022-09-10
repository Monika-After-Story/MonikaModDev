# all complicated interactions go here
# mainly:
#   boop
#   pat
#   etc...


#### BOOP


init -10 python in mas_interactions:

    import ccmath.ccmath as cmath

    import store

    import store.mas_sprites as mas_sprites
    import store.mas_utils as mas_utils


    class MASClickZoneManager(object):
        """
        Manages clickzones, with varying zoom levels.
        Use to automate caching and stuff with clickzones.

        ACCESSING ZONES:
            use backet notation to access a clickzone:
            zonemanager[zone_key]

            This takes current zoom into account, and auto zooms something
            if no clickzone exists.

            NOTE: use get to get for a specific zoom level

        CONTAINS:
            'in' is allowed for checking zone_keys.

        ITERABLE:
            this will iterate over zone_keys and clickzones at the current
            zoom level.
        """

        def __init__(self):
            self._zoom_cz = {}
            # key: zoom level
            # value: dict:
            #   key: zonekey
            #   value: clickzone

            self._zones = {}
            # contains all zone_keys managed by this manager
            # key: zone_key
            # value: ignored

        def __contains__(self, item):
            return item in self._zones

        def __getitem__(self, key):
            """
            Key should be the zone_key.
            This will get the clickzone for the current zoom level, generating
            it if not found.
            """
            return self.get(key, mas_sprites.zoom_level)

        def __iter__(self):
            for zone_key in self._zones:
                yield zone_key, self[zone_key]

        def add(self, zone_key, cz):
            """
            Adds a clickzone to this manager.
            NOTE: will NOt override an existing zone_key
            NOTE: you must add the clickzone at the default zoom level for
                zoom algs to work.

            IN:
                zone_key - key to use to represnt this zone
                cz - MASClickZone to add.
                    Assumed to work for default zoom level
            """
            if zone_key in self._zones:
                return

            # add to zones
            self._zones[zone_key] = cz

            # add to zoom level/zone
            cz_d = self._zoom_cz.get(mas_sprites.default_zoom_level, {})
            cz_d[zone_key] = cz
            self._zoom_cz[mas_sprites.default_zoom_level] = cz_d

        def _cz_iter(self):
            """
            Iterates over all clickzones in this clickzone manager, for
            all zoom levels.

            Output is a tuple of:
                [0] zone_key
                [1] zoom level
                [2] clickzone
            """
            for zl, zl_d in self._zoom_cz.iteritems():
                for zone_key, cz in zl_d.iteritems():
                    yield zone_key, zl, cz

        def _debug(self, value):
            """
            Sets the debug_back value for all clickzones

            IN:
                value - value to set to _debug_back
            """
            for zk, zl, cz in self._cz_iter():
                cz._debug_back = value

        def get(self, zone_key, zl):
            """
            Gets a clickzone from this manager, from a zoom level.

            Generates the clickzone if not exist for this zoom level.
            NOTE: this will generate ALL clickzones for a zoom level for
            consistency and speed.

            IN:
                zone_key - key of zone to get
                zl - zoom level of zone to get

            RETURNS: MASClickZone object, or None if failed to get
            """
            if zl not in self._zoom_cz:
                self.zoom_to(zl)

            return self._zoom_cz.get(zl, {}).get(zone_key, None)

        def remove(self, zone_key):
            """
            Removes a clickzone from this manager.

            IN:
                zone_key - key of the zone to remove
            """
            if zone_key not in self._zones:
                return

            # remove from zones
            self._zones.pop(zone_key)

            # remove from zoom levels
            for zone_d in self._zoom_cz.itervalues():
                if zone_key in zone_d:
                    zone_d.pop(zone_key)

        def set_disabled(self, zone_key, value):
            """
            Sets all clickzones with the given zonekey's disabled prop.

            IN:
                zone_key - key of the clickzone to change
                value - value to set disabled to
            """
            for zl_d in self._zoom_cz.itervalues():
                cz = zl_d.get(zone_key, None)
                if cz is not None:
                    cz.disabled = value

        def zoom_to(self, zoom_level):
            """
            Fills zoom cache with Clickzones for a zoom level

            IN:
                zoom_level - zoom level to generate clickzones for
            """
            # get zoom level dict containing clickzones
            zl_set = self._zoom_cz.get(zoom_level, {})

            for zone_key, cz in self._zones.iteritems():

                # only add clickzones that dont already exist
                if zone_key not in zl_set:
                    new_cz = store.MASClickZone.copyfrom(
                        cz,
                        vx_list_zoom(zoom_level, cz.corners)
                    )
                    zl_set[zone_key] = new_cz

            self._zoom_cz[zoom_level] = zl_set


    # important enums
    ZONE_CHEST = "chest"
    ZONE_CHEST_1_L = "chest-1-l"
    ZONE_CHEST_1_M = "chest-1-m"
    ZONE_CHEST_1_R = "chest-1-r"
    ZONE_HEAD = "head"
    ZONE_NOSE = "nose"
    ZONE_EYE_E_L = "eye-e-l"
    ZONE_EYE_E_R = "eye-e-r"
    ZONE_MOUTH_A = "mouth-a"

    # default zoom clickzone map
    cz_map = {
        ZONE_CHEST: [
            (514, 453), # (her) right top
            (491, 509),
            (489, 533),
            (493, 551),
            (506, 573),
            (525, 588),
            (541, 592),
            (650, 586), # middle below apex
            (709, 592),
            (761, 592),
            #(787, 580),
            (790, 585),
            #(806, 559),
            (810, 560),
            (813, 536),
            (813, 517),
            (789, 453),
        ],
        ZONE_CHEST_1_R: [
            (514, 453), # (her) right top
            (491, 509), 
            (489, 533),
            (493, 551),
            (498, 555), # (her) right to arm 
            (508, 498),
            (515, 453),
        ],
        ZONE_CHEST_1_M: [
            (568, 453), # (her) right top
            (568, 590), # (her) right bottom
            (650, 586), # middle below apex
            (728, 592), # (her) left bottom
            (735, 453), # (her) left top
        ],
        ZONE_CHEST_1_L: [
            (782, 453), # (her) left top
            (784, 474),
            (790, 516),
            (801, 570), # (her) left to arm
            (810, 560),
            (813, 536),
            (813, 517),
            (789, 453),
        ],
        ZONE_HEAD: [
            (634, 68-100),
            (597, 73-100),
            (552, 91-100),
            (540, 94-100),
            (531, 4),
            (517, 42),
            (498, 80),
            (486, 144),
            (708, 144),
            (778, 178),
            (792, 129),
            (792, 80),
            (777, 30),
            (751, 99-100),
            (690, 71-100),
        ],
        ZONE_NOSE: [
            (629, 240),
            (623, 252),
            (629, 258),
            (633, 252),
        ],
    }

    # speciality constants
    FOCAL_POINT = (640, 750)
    FOCAL_POINT_UP = (640, 740)

    ZOOM_INC_PER = 0.04


    def get_vx(zone_enum):
        """
        Get vx list of a zone enum

        IN:
            zone_enum - zone enum to get vertex list for

        RETURNS: vertex list, or empty if not found
        """
        return cz_map.get(zone_enum, [])


    def z_vx_list_zoom(zoom_level, zone_enum):
        """
        Generates a vertex list from the given zoom and zone enum

        IN:
            zoom_level - zoom level to generate vertex list for
            zone_enum - zone enum to generate vertex list for

        RETURNS:
            list of vertexes. May be empty if not valid zone enum
        """
        vx_list = cz_map.get(zone_enum, None)
        if vx_list is None:
            return []

        return vx_list_zoom(zoom_level, vx_list)


    def vx_list_zoom(zoom_level, vx_list):
        """
        Generates a vertex list from the given zoom

        IN:
            zoom_level - zoom level to generate vertex list
            vx_list - list of vertexes to geneate new list for

        RETURNS: list of vertexes
        """
        if zoom_level == mas_sprites.default_zoom_level:
            return list(vx_list)

        # otherwise, modify the vertex list
        return _vx_list_zoom(
            zoom_level,
            vx_list,
            zoom_level < mas_sprites.default_zoom_level
        )


    # internal


    def _vx_list_zoom(zoom_level, vx_list, zoom_out):
        """
        Generates vertex list for zooming.

        IN:
            zoom_level zoom level to generate vertex list for
            vx_list - list of vetex points to adjust for zoom.
                NOTE: we generate a new list, so dont worry about this changing
            zoom_out - True if we are zooming out, False if zooming in

        RETURNS: adjustd list of vertexes
        """
        # NOTE: methodology:
        #   Basically, zoom increases/decreases by 0.05 per level. Using that,
        #   the amount the image increases or decreases compared to the default
        #   zoom level can be deteremined. This was figured to be the
        #   distance between the zoom level and the default zoom multiplied by
        #   4%. I.e: zoom level 0 is 12% smaller than zoom level 3 (3-0 * 4%).
        #   Zoom level 10 is 28% larger than zoom level 3 (10-3 * 4%).
        #
        #   Zooming also generally resovles around a focal point.
        #   Once that focal point is determined the distance between that
        #   point and other points will always increase by the same factor as
        #   the total image. ie: the distance from the focal to point A at
        #   zoom level 10 is 28% larger than at zoom level 3. Same goes for
        #   the distance at zoom level 0 being 12% smaller than at
        #   zoom level 3.
        #
        #   Distances to points can be modified easily by converting regular
        #   coordinates to polar coordinates, which keeps direction separate
        #   from distance. After modifying the distance, the polar coords are
        #   reconverted back into regular coords, which now have been properly
        #   zoomed.
        #
        #   Since the focal point is NOT the origin, the points are normalized
        #   to the origin using the focal point before distance modification.
        #   Then they are unnormalized back into regular coords appropraite
        #   to the actual image.
        #
        #   NOTE: Zooming in also modifies the focal point by a factor *
        #       a y_step, which is a number of pixels to move the image down
        #       the screen per zoom level. The focal point in this case must
        #       be modified before normalizing other points with it, but the
        #       modification should NOT be reversed when unnormalizing.
        #       This is because of the nature that the image is moved down
        #       a certain number of pixels, and such the points must be moved
        #       down with this offset as well.

        # setup diff between zooming in and out
        if zoom_out:
            zoom_diff = mas_sprites.default_zoom_level - zoom_level
            per_mod = -1 * (zoom_diff * ZOOM_INC_PER)
            xfc, yfc = FOCAL_POINT
            yfc_offset = 0

        else:
            zoom_diff = zoom_level - mas_sprites.default_zoom_level
            per_mod = zoom_diff * ZOOM_INC_PER
            xfc, yfc = FOCAL_POINT_UP
            yfc_offset = -1 * zoom_diff * mas_sprites.y_step

        # now process all pts
        new_vx_list = []
        for xcoord, ycoord in vx_list:
            # first, normalize the pt to origin
            xcoord -= xfc
            ycoord -= (yfc + yfc_offset)

            # now convert the pt into polar coords
            radius, angle = cmath.polar(xcoord, ycoord)

            # modify the radius by the appropraite percent val
            radius += (radius * per_mod)

            # convert the new polar coord back into regular coords
            new_x, new_y = cmath.rect(radius, angle)

            # unnormalize to get the real x, y and save
            new_vx_list.append((
                int(new_x + xfc),
                int(new_y + yfc)
            ))

        return new_vx_list


init -9 python:


    class MASZoomableInteractable(renpy.Displayable):
        """
        Interactable designed for use with MASClickZones and zooming.

        This is the primary way that zoomable MASClickZones should be used.

        Supports both being Call'd or Showned.
        pass in zone_actions to determine what happens when a zone_key is
        clicked. Default (or unset) action is to return zone_key.
        """
        ZONE_ACTION_NONE = 0
        ZONE_ACTION_RET = 1
        ZONE_ACTION_JUMP = 2
        ZONE_ACTION_END = 3
        ZONE_ACTION_RST = 4

        def __init__(
                self,
                cz_manager,
                zone_actions=None,
                zone_order=None,
                start_zoom=None,
                debug=False
        ):
            """
            Constructor for an interactable.

            IN:
                cz_manager - MASClickZoneManager containing the clickzones
                    to use in this MASZoomableInteractable
                zone_actions - dict of the following format:
                    key: zone key
                    value: variety of values:
                        - if None, or not set, then we return zone_key
                        - if a string, then we jump to that label if
                            it exists. If it doesn't exist, we return it.
                        - if 0 - then nothing None is returned, which is
                            basically like ignoring it.
                        - if 1 - then renpy.end_interaction will be called
                            with True param
                        - if 2 - then renpy.restart_interaction will be called
                zone_order - order to evaluate zones. if None, then no order
                    is followed. Should be list of zone keys
                    (Default: None)
                start_zoom - pass this in if the clickzones are startnig at
                    a zoom level that is not the current.
                    (Default: None)
            """ 
            if zone_actions is None:
                zone_actions = {}
            if zone_order is None:
                zone_order = []
            if start_zoom is None:
                start_zoom = store.mas_sprites.zoom_level

            self._cz_man = cz_manager
            self.zones_stat = {}
            self._zones_action = zone_actions
            self._zones_order = zone_order
            self._zones_unorder = {}

            self._last_zoom_level = start_zoom
            
            self._end_int = None
            self._rst_int = False
            self._jump_to = None
            self._zk_click = None
            self._ret_val = None

            self._debug = debug
            if debug:
                self._cz_man._debug(True)

            self._build_zones()

            super(MASZoomableInteractable, self).__init__()

        def add_zone(self, zone_key, cz):
            """
            Adds a zone. This should rarely be used.
            NOTE: this will NOT replace an existing zone.

            IN:
                zone_key - key of the zone to add
                cz - MASClickZone to add
            """
            if zone_key in self._cz_man:
                return

            self._cz_man.add(zone_key, cz)
            if zone_key not in self._zones_order:
                self._zones_unorder[zone_key] = None
            if zone_key not in self.zones_stat:
                self.zones_stat[zone_key] = 0

        def adjust_for_zoom(self):
            """
            Adjusts clickzones for current zoom level.
            """
            if self._last_zoom_level == store.mas_sprites.zoom_level:
                return

            # otherwise change occured
            self._zone_zoom(store.mas_sprites.zoom_level)
            self._last_zoom_level = store.mas_sprites.zoom_level

        def _build_zones(self):
            """
            Sets internal zone components based on the cz_man
            """
            for zone_key, cz in self._cz_man:
                self.zones_stat[zone_key] = 0
                if zone_key not in self._zones_order:
                    self._zones_unorder[zone_key] = None

        def check_click(self, ev, x, y, st):
            """
            Checks if an ev was a click over a zone.

            RETURNS: zone key if clicked, None if not clicked
            """
            for zone_key, cz in self.zone_iter():
                if cz.event(ev, x, y, st) is not None:
                    return zone_key

            return None

        def check_over(self, x, y):
            """
            Checks if the given x y is over a zone, and returns the zone key
            if appropripate

            IN:
                x - x
                y - y

            RETURNS: zone_key, or None if no click over zones
            """
            for zone_key, cz in self.zone_iter():
                if cz._isOverMe(x, y):
                    return zone_key

            return None

        def clicks(self, zone_key):
            """
            Returns number of times a zone_key was clicked

            RETURNS: number of times a zone_key was clicked
            """
            return self.zones_stat.get(zone_key, 0)

        def disable_zone(self, zone_key):
            """
            Disables a clickzone

            IN:
                zone_key - clickzone to disable
            """
            self._cz_man.set_disabled(zone_key, True)

        def enable_zone(self, zone_key):
            """
            Enables a clickzone

            IN:
                zone_key - clickzone to enable
            """
            self._cz_man.set_disabled(zone_key, False)

        def event(self, ev, x, y, st):
            """
            By default, we process events in order and return/jump as 
            appropriate.
            """
            self.event_begin(ev, x, y, st)
            return self.event_end(ev, x, y, st)

        def event_begin(self, ev, x, y, st):
            """
            Call this when starting event actions. This handles the click
            for all clickzones.

            RETURNS: zone_key that was clicked.
            """
            self.adjust_for_zoom()

            self._rst_int = False
            self._end_int = None
            self._jump_to = None
            self._ret_val = None

            self._zk_click = self.check_click(ev, x, y, st)
            if self._zk_click is not None:
                self.zones_stat[self._zk_click] += 1
                self._ret_val = self.zone_action(self._zk_click)

            return self._zk_click

        def event_end(self, ev, x, y, st):
            """
            Call this when wrapping up event actions.
            NOTE: this will do actions determined when event_begin was called.
            To not do these actions, either override this or do not call this.

            RETURNS: value to return in event
            """
            if self._jump_to is not None:
                renpy.jump(self._jump_to)

            if self._rst_int:
                renpy.restart_interaction()

            else:
                renpy.end_interaction(self._end_int)

            return self._ret_val

        def remove_zone(self, zone_key):
            """
            Removes a clickzone if we have it

            IN:
                zone_key - key of the zone to remove
            """
            self._cz_man.remove(zone_key)
            if zone_key in self._zones_unorder:
                self._zones_unorder.pop(zone_key)

        def render(self, width, height, st, at):
            """
            By default, we will not render unless debug mode is on
            """
            r = renpy.Render(width, height)

            if not self._debug:
                return r

            renders = []
            
            # render in reverse zone order for visual clarity
            for zone_key, cz in self.zone_iter_r():
                if not cz.disabled:
                    renders.append(renpy.render(cz, width, height, st, at))

            for render in renders:
                r.blit(render, (0, 0))

            return r

        def zone_action(self, zone_key):
            """
            Determines zone action for zone key
            Actions are setup to be done when this is called.

            RETURNS: return value to return in event
            """
            action = self._zones_action.get(zone_key, None)
            if action is None:
                # return zone key
                return zone_key

            if isinstance(action, str):
                if renpy.has_label(action):
                    # label to jump to
                    self._jump_to = action

                # otherwise return like zone key
                return action

            if action == 1:
                # end interaction
                self._end_int = True

            elif action == 2:
                # restart interaction
                self._rst_int = True

            # othewise, do nothing
            return None

        def zone_iter(self):
            """
            Generates zone_key with clickzone

            YIELDS: tuple of zone_key, clickzone
            """
            for zone_key in self._zones_order:
                cz = self._cz_man[zone_key]
                if cz is not None:
                    yield zone_key, cz

            for zone_key in self._zones_unorder:
                yield zone_key, self._cz_man[zone_key]

        def zone_iter_r(self):
            """
            Generates zone_key with clickzone, in reverse

            YIELDS: tuple of zone_key, clickzone
            """
            for zone_key in self._zones_unorder:
                yield zone_key, self._cz_man[zone_key]

            for zone_key in self._zones_order:
                cz = self._cz_man[zone_key]
                if cz is not None:
                    yield zone_key, cz

        def _zone_zoom(self, zoom_level):
            """
            adjusts all clickzones for a zoom level, using the zoom adjustment
            algorithm.

            NOTE: no checks are done here before zoom is changed. Use
            adjust_for_zoom if you only care that it matches current zoom
            level

            IN:
                zoom_level - zoom level to adjust clickzones to
            """
            self._cz_man.zoom_to(zoom_level)


label mas_nose_boop_launch:

    # because monika idle causes issues, monika will jump to 6eua
    # there literally is nothing that can be done about this.
    show monika 6eua


    # drop shields
    $ mas_DropShield_core()

    show monika idle

    # when done with monika game, we return to ch30 loop
    jump ch30_loop
