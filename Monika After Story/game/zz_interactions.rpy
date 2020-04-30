# all complicated interactions go here
# mainly:
#   boop
#   pat
#   etc...


#### BOOP


init -10 python in mas_interactions:

    import ccmath.ccmath as cmath

    import store.mas_sprites as mas_sprites
    import store.mas_utils as mas_utils

    # important enums
    ZONE_CHEST = "chest"
    ZONE_CHEST_1 = "chest-1"
    ZONE_HEAD = "head"
    ZONE_NOSE = "nose"

    ZONE_ENUMS = (
        ZONE_CHEST,
        ZONE_CHEST_1,
        ZONE_HEAD,
        ZONE_NOSE,
    )

    # default zoom clickzone map
    cz_map = {
        ZONE_CHEST: [
            (514, 453),
            (491, 509),
            (489, 533),
            (493, 551),
            (506, 573),
            (525, 588),
            (541, 592),
            (652, 586),
            (709, 592),
            (761, 592),
            (787, 580),
            (806, 559),
            (813, 536),
            (813, 517),
            (789, 453),
        ],
        ZONE_CHEST_1: [
            (602, 487),
            (590, 531),
            (587, 597),
            (652, 586),
            (714, 592),
            (708, 530),
            (697, 487),
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


    def vertex_list_from_zoom(zoom_level, zone_enum):
        """
        Generates a vertex list from the given zoom

        IN:
            zoom_level - zoom level to generate vertex list
            zone_enum - zone enum to get vertex list for

        RETURNS: list of vertexes. might be empty list if invalid data passed
            in
        """
        if zone_enum not in ZONE_ENUMS:
            return []

        if zoom_level == mas_sprites.default_zoom_level:
            return cz_map[zone_enum]

        # otherwise, modify the vertex list
        return _vx_list_zoom(
            zoom_level,
            zone_enum,
            zoom_level < mas_sprites.default_zoom_level
        )


    # internal


    def _vx_list_zoom(zoom_level, zone_enum, zoom_out):
        """
        Generates vertex list for zooming.

        IN:
            zoom_level zoom level to generate vertex list for
            zone_enum - zone enum to get vertex list for
            zoom_out - True if we are zooming out, False if zooming in

        RETURNS: list of vertexes
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
        pts = cz_map[zone_enum]
        vx_list = []
        for xcoord, ycoord in pts:
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
            vx_list.append((
                int(new_x + xfc),
                int(new_y + yfc)
            ))

        return vx_list


init -9 python:

    class MASBoopInteractable(MASInteractable):
        """
        Interactable for nose booping
        """
        import store.mas_interactions as smi

        def __init__(self, chest_open):
            """
            contstructor

            IN:
                chest_open - true if the chest is fully open at start
            """
            # the current zoom level effects what zones we get



label mas_nose_boop_launch:

    # because monika idle causes issues, monika will jump to 6eua
    # there literally is nothing that can be done about this.
    show monika 6eua


    # drop shields
    $ mas_DropShield_core()

    show monika idle

    # when done with monika game, we return to ch30 loop
    jump ch30_loop
