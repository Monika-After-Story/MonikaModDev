# Module containing custom transform functions.
# Last just because
# NOTE: Depends on script-poemgame

# special early access image accessors
init -10 python:

    def getCharacterImage(char, expression="1a"):
        #
        # Retrieves the image of the given character + expression combo
        # This is the raw object that represents an image
        #
        # IN:
        #   char - string name of the character to find:
        #       "monika", "sayori", "natsuki", "yuri"
        #   expression - string expression to find
        #       (Default: 1a)
        #
        # RETURNS:
        #   the image object that is held internally, or None if not found
        return renpy.display.image.images.get((char, expression), None)


    def mas_getPropFromStyle(style_name, prop_name):
        """
        Retrieves a property from a style
        Recursively checks parent styles until the property is found.

        IN:
            style_name - name of style as string
            prop_name - property to find as string

        RETURNS: value of the propery if we can find it, None if not found
        """
        style_name = (style_name,)
        prop_not_found = True
        while prop_not_found:
            # pull from styles dict
            # NOTE: directly accessing to avoid exceptions
            style_obj = renpy.style.styles.get(style_name, None)
            if style_obj is None:
                return None

            # sanity check to ensure properties exists
            if len(style_obj.properties) > 0:

                # check for the prop we want
                if prop_name in style_obj.properties[0]:
                    return style_obj.properties[0][prop_name]

            # otherwise check parent
            if style_obj.parent is None:
                return None

            # recurse
            style_name = style_obj.parent

        # should never be reached
        return None


    def mas_prefixFrame(frm, prefix):
        """
        Generates a frame object with the given prefix substitued into the
        image. This effectively makes a copy of the given Frame object.

        NOTE: cannot use _duplicate as it does shallow copy for some reason.

        IN:
            frm - Frame object
            prefix - prefix to replace `prefix_`. "_" will be added if not
                found

        RETURNS: Frame object, or None if failed to make it
        """
        if not prefix.endswith("_"):
            prefix += "_"

        try:
            # sve borders
            frm_borders = {
                "left": frm.left,
                "top": frm.top,
                "right": frm.right,
                "bottom": frm.bottom,
            }

            # set image path
            img_path = renpy.substitute(
                frm.image.name,
                scope={"prefix_": prefix}
            )

            # build frame
            return Frame(img_path, **frm_borders)
        except:
            return None

# A transition of the new type
# which only works with mas_with_statement or Ren'Py 7.0+
init -5 python:
    dissolve_monika = {"master": Dissolve(0.25, alpha=True)}
    dissolve_textbox = {"screens": Dissolve(0.2, alpha=True)}

# user defined trasnforms
transform leftin_slow(x=640, z=0.80, t=1.00):
    xcenter -300 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein t xcenter x

# transform positional shortcuts
# NOTE: only the ones that we need are defined. Add them as you need em
transform ls32:
    leftin_slow(x=640)

# piano slides in
transform lps32:
    leftin_slow(x=640,t=4.00)

# used so things that slide in will also slide back out
transform lslide(t=1.00, x=-600):
    subpixel True
    on hide:
        easeout t xcenter x

# used so Monika can slide back out
transform rs32:
    lslide()

# used so piano can slide back out
transform rps32:
    lslide(t=4.00,x=-700)

### transforms for chibi monika
transform mas_chdropin(x=640, y=405, travel_time=3.00):
    ypos -300 xcenter x
    easein travel_time ypos y

transform mas_chflip(dir):
    # -1 to face right.
    # 1 to face left
    xzoom dir

transform mas_chflip_s(dir, travel_time=0.36):
    ease travel_time xzoom dir

transform mas_chhopflip(dir, ydist=-15, travel_time=0.36):
    # -1 to face right
    # 1 to face left
    easein_quad travel_time/2.0 yoffset ydist xzoom 0
    easeout_quad travel_time/2.0 yoffset 0 xzoom dir

transform mas_chmove(x, y, travel_time=1.0):
    # x and y should be coordinates
    # use this to directly move to a location
    ease travel_time xpos x ypos y

# NOTE: use sticker_hop for straight hopping

transform mas_chriseup(x=300, y=405, travel_time=1.00):
    ypos 800 xcenter x
    easein travel_time ypos y

# parabola jump
transform mas_chlongjump(x, y, ymax, travel_time=1.0):
    parallel:
        linear travel_time xpos x
    parallel:
        easeout travel_time*0.6 ypos ymax
        easein travel_time*0.4 ypos y

transform tcommon(x=640, z=0.80):
    yanchor 1.0 subpixel True
    on show:
        ypos 1.03
        zoom z*0.95 alpha 0.00
        xcenter x yoffset -20
        easein .25 yoffset 0 zoom z*1.00 alpha 1.00
    on replace:

        alpha 1.00
        parallel:
            easein .25 xcenter x zoom z*1.00
        parallel:
            easein .15 yoffset 0 ypos 1.03

transform tinstant(x=640, z=0.80):
    xcenter x yoffset 0 zoom z*1.00 alpha 1.00 yanchor 1.0 ypos 1.03

transform t41:
    tcommon(200)
transform t42:
    tcommon(493)
transform t43:
    tcommon(786)
transform t44:
    tcommon(1080)
transform t31:
    tcommon(240)
transform t32:
    tcommon(640)
transform t33:
    tcommon(1040)
transform t21:
    tcommon(400)
transform t22:
    tcommon(880)
transform t11:
    tcommon(640)

transform i41:
    tinstant(200)
transform i42:
    tinstant(493)
transform i43:
    tinstant(786)
transform i44:
    tinstant(1080)
transform i31:
    tinstant(240)
transform i32:
    tinstant(640)
transform i33:
    tinstant(1040)
transform i21:
    tinstant(400)
transform i22:
    tinstant(880)
transform i11:
    tinstant(640)

transform sticker_hop:
    easein_quad .18 yoffset -80
    easeout_quad .18 yoffset 0
    easein_quad .18 yoffset -80
    easeout_quad .18 yoffset 0

transform sticker_move_n:
    easein_quad .08 yoffset -15
    easeout_quad .08 yoffset 0
