# all complicated interactions go here
# mainly:
#   boop
#   pat
#   etc...


#### BOOP


init -10 python in mas_interactions_boop:

    import cmath

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
            (556, 0),
            (519, 40),
            (498, 80),
            (486, 144),
            (708, 144),
            (778, 178),
            (792, 129),
            (792, 80),
            (777, 30),
            (748, 0),
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
#    FOCAL_POINT_UP = (640, 850)
#    FOCAL_POINT_UP = (640, 690)
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

        if zoom_level > mas_sprites.default_zoom_level:
            #pass
            # TODO: do function for zoom up
            # NOTE: temporary debug here
            return _vx_list_zoom_in(zoom_level, zone_enum)

        elif zoom_level < mas_sprites.default_zoom_level:
            return _vx_list_zoom_out(zoom_level, zone_enum)

        # otherwise, we want the defaults
        return cz_map[zone_enum]


    # internal


    def _vx_list_zoom_in(zoom_level, zone_enum):
        """
        Generates vertex list for zooming in (zone leve less than default)

        IN:
            zoom_level
        """
        zoom_diff = zoom_level - mas_sprites.default_zoom_level
        # zooming in increaes distance to focal point by 4%
        percent_inc = zoom_diff * ZOOM_INC_PER

        # now process all pts
        pts = cz_map[zone_enum]
        vx_list = []
        for xcoord, ycoord in pts:
            # first, normalize the pt to origin
            xcoord -= FOCAL_POINT[0]
            ycoord -= (FOCAL_POINT_UP[1] - (zoom_diff * mas_sprites.y_step))

            # now convert the pt into polar coords
            radius, angle = cmath.polar(complex(xcoord, ycoord))

            # modify the radius by the appropraite percent val
            radius += (radius * percent_inc)

            # convert the new polar coord back into regular coords
            coords = cmath.rect(radius, angle)

            # unnormalize to get the real x, y and save
            vx_list.append((
                int(coords.real + FOCAL_POINT[0]),
                int(coords.imag + FOCAL_POINT_UP[1])
            ))

        # return the modified vertexes
        return vx_list


    
    def _vx_list_zoom_out(zoom_level, zone_enum):
        """
        Generates vertex list for zooming out (zoom level less than default)

        IN:
            zoom_level - zoom level to generate vertex list
            zone_enum - zone enum to get vertex list for

        RETURNS: list of vertexes
        """
        # zooming out decreases distance to focal point by 4%
        percent_dec = -1 * (
            (mas_sprites.default_zoom_level - zoom_level) * ZOOM_INC_PER
        )

        # now process all pts
        pts = cz_map[zone_enum]
        vx_list = []
        for xcoord, ycoord in pts:
            # first, normalize the pt to origin
            xcoord -= FOCAL_POINT[0]
            ycoord -= FOCAL_POINT[1]

            # now convert the pt into polar coords
            radius, angle = cmath.polar(complex(xcoord, ycoord))

            # modify the radius by the appropraite percent val
            radius += (radius * percent_dec)

            # convert the new polar coord back into regular coords
            coords = cmath.rect(radius, angle)

            # unnormalize to get the real x, y and save
            vx_list.append((
                int(coords.real + FOCAL_POINT[0]),
                int(coords.imag + FOCAL_POINT[1])
            ))

        # return the modified vertexes
        return vx_list


init python:


    class MASInteractableDisplayable(renpy.Displayable):
        # TODO

        
        testing = 10
