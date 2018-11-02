# Module containing custom transform functions.
# Last just because

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
transform leftin_slow(x=640, z=0.80):
    xcenter -300 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein 1.00 xcenter x

# transform positional shortcuts
# NOTE: only the ones that we need are defined. Add them as you need em
transform ls32:
    leftin_slow(640)

