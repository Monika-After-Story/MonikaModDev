# Module containing custom transform functions.
# Last just because

# user defined trasnforms
transform leftin_slow(x=640, z=0.80):
    xcenter -300 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein 1.00 xcenter x

# transform positional shortcuts
# NOTE: only the ones that we need are defined. Add them as you need em
transform ls32:
    leftin_slow(640)

