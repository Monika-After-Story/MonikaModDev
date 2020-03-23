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

# t10 and t12 are slight movements from t11 intended for piano use
transform t10:
    tcommon(637)

transform t12:
    tcommon(643)


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



