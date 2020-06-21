## module with a function that pull sprites out of the sprite-chart
#
# VER: Python 2.7

import os
import gamedir as GDIR
import menutils

STATIC_PREFIX = "sprite-chart-0"
ALIAS_PREFIX = "sprite-chart-1"
ATL_PREFIX = "sprite-chart-2"

STATIC_TEMPLATE = STATIC_PREFIX + "{0}.rpy"
ALIAS_TEMPLATE = ALIAS_PREFIX + "{0}.rpy"
ATL_TEMPLATE = ATL_PREFIX + "{0}.rpy"

STATIC_CHARTS = []
ALIAS_CHARTS = []
ATL_CHARTS = []

SPRITE_PATH = [
    GDIR.REL_PATH_GAME + "sprite-chart.rpy",
]

SAVE_PATH = "zzzz_spritelist"
SAVE_PATH_D = "zzzz_spritedict"
SAVE_PATH_IO = GDIR.REL_PATH_GAME + "zzzz_sprite_opt.rpy"

IMG_START = "image monika"
IMG_OUT = '"monika {0}"'
IMG_OUT_L = '\n        "monika {0}",'

DYN_DIS = "DynamicDisplayable"

MAX_FILE_LIMIT = 10


def clean_sprite(code):
    """
    Cleans the given sprite (removes excess whitespace, colons)

    IN:
        code - sprite code to clean

    RETURNS:
        cleaned sprite code
    """
    code = code.strip()
    return code.replace(":","")


def is_dyn_line(line):
    """
    Checks if the given line is a sprite line with dynamic displayable
    :param line: line to check
    :returns: True if the given line is a sprite line, False otherwise.
    """
    return is_sprite_line(line) and DYN_DIS in line


def is_sprite_line(line):
    """
    Checks if the given line is a sprite line

    NOTE: a sprite line is a line that starts with "image monika"
    
    NOTE: does not strip the given line.

    IN:
        line - line to check

    RETURNS:
        True if the given line is a sprite line, False otherwise.
    """
    return line.startswith(IMG_START)


def pull_dyn_sprite_code(line):
    """
    Pulls sprite code from teh given line.
    Only ones that are monika + dynamic displayable are allowed
    NOTE: this also removes the _static lines
    :param line: line topull sprite code
    :returns: the sprite code we got, or None if not found
    """
    if is_dyn_line(line):
        spcode = clean_sprite(line.split(" ")[2])
        return spcode.partition("_")[0]

    return None


def pull_sprite_code(line):
    """
    Pulls the sprite code from the given line.
    This checks if the given line is a sprite line before pulling the code.

    IN:
        line - line to pull sprite code

    RETURNS: the sprite code we got, if not a sprite code, we return None
    """
    if is_sprite_line(line):
        return clean_sprite(line.split(" ")[2])

    return None


def pull_sprite_list(as_dict=False):
    """
    Goes through the sprite chart and generates a list of all the known sprite
    codes.

    NOTE:
        This does not really do any filtering, so if sprite-chart has excess
        images, they will be reflected here.

    IN:
        as_dict - if True, this will return a dict with the known sprite codes
            as keys. The values will be 0.

    RETURNS:
        list of known sprite codes, or dict if as_dict is True
    """
    sprite_list = list()

    for sprfile in SPRITE_PATH:
        with open(os.path.normcase(sprfile), "r") as sprite_file:
            sprite_list.extend(pull_sprite_list_from_file(sprite_file))

    if as_dict:
        # do we want a dict instead?
        sprite_dict = dict()
        
        for sprite in sprite_list:
            sprite_dict[sprite] = 0

        return sprite_dict

    # otherwise we want the lsit
    return sprite_list


def pull_sprite_list_from_file(sprite_file, dyn_only=False):
    """
    Pulls a list of sprite from the given file
    :param sprite_file: file object to read sprites from
    :param dyn_only: True will only get the dynamic displayable sprites, False
        will get all
    :returns: list of sprite codes
    """
    if dyn_only:
        puller = pull_dyn_sprite_code
    else:
        puller = pull_sprite_code

    sprite_list = []

    for line in sprite_file:
        code = puller(line)

        if code:
            sprite_list.append(code)

    return sprite_list


def write_spritecodes(sprites):
    """
    Writes out a sprite file that just contains each sprite code out,
    one sprite code per line

    IN:
        sprites - list of sprite codes to write out.
    """
    with open(os.path.normcase(SAVE_PATH), "w") as outfile:
        for line in sprites:
            outfile.write(line + "\n")


def write_spritestats(sprites):
    """
    Writes out a sprite file that just contains each sprite code with its 
    value, one sprite code per line

    IN:
        sprites - dict of sprite codes to write out
    """
    with open(os.path.normcase(SAVE_PATH_D), "w") as outfile:
        for code in sprites:
            outfile.write("{0}: {1}\n".format(code, sprites[code]))


def write_zz_sprite_opt(sprites):
    """
    Writes out a sprite file that can be used in renpy to optimize sprites
    using image prediction.

    IN:
        sprites - list of sprite codes to write out.
    """
    with open(os.path.normcase(SAVE_PATH_IO), "w") as outfile:
        outfile.write(__ZZ_SP_OPT_HEADER)

        open_list = False

        # we must write in pieces beause a giant list is too long
        for index in range(len(sprites)):
            # write header every 100
            if index % 100 == 0:
                open_list = True
                outfile.write(__ZZ_SP_OPT_LINE_START)

            # now actual line
            outfile.write(IMG_OUT_L.format(sprites[index]))

            # on the 100th item, write footer
            if index % 100 == 99:
                open_list = False
                outfile.write(__ZZ_SP_OPT_LINE_END)

        # 1 last footer needed
        if open_list:
            outfile.write(__ZZ_SP_OPT_LINE_END)
        
        outfile.write(__ZZ_SP_OPT_FOOTER)


####################### special run methods ##################################


def run():
    """
    Runs this module (menu-related)
    """
    choice = menutils.menu(menu_main)

    if choice is None:
        return

    # otherwise we have a choice
    choice()


def run_spl(quiet=False):
    """
    Generates the sprite code list and writes it to file

    IN:
        quiet - True will suppress output
    """
    if not quiet:
        print("Generating sprite list....")

    sp_list = pull_sprite_list()

    if not quiet:
        print("Writing sprite list to " + SAVE_PATH)

    write_spritecodes(sp_list)

    if not quiet:
        print("\nDone")
        menutils.e_pause()


def run_rpy_all(quiet=False):
    """
    Generates optimized image rpy for ALL images

    IN:
        quiet - True will suppress output
    """
    if not quiet:
        print("Generating sprite list....")

    sp_list = pull_sprite_list()

    if not quiet:
        print("Writing optimized rpy to " + SAVE_PATH_IO)

    write_zz_sprite_opt(sp_list)

    if not quiet:
        print("\nDone")
        menutils.e_pause()


################### menus #################

menu_main = [
    ("Sprite Puller", "Option: "),
    ("Generate Sprite Code List", run_spl),
    ("Generate Optimized RPY", run_rpy_all)
]


#### strings for formatting:
__ZZ_SP_OPT_HEADER = """\
############################ AUTO-GENERATED ###################################
## DO NOT EDIT THIS FILE                                                     ##
##                                                                           ##
## This was auto-generated by the spritepuller tool                          ##
###############################################################################
#
# This is a module designed for optimizing sprites by predicting them.
# NOTE: memory usage increases massively when this is used.
#   USE AT YOUR OWN RISK
#

init 2020 python:
    image_list = []
"""

__ZZ_SP_OPT_LINE_START = """\
    image_list.extend(["""

__ZZ_SP_OPT_LINE_END = """
    ])
"""

__ZZ_SP_OPT_FOOTER = """
    renpy.start_predict(*image_list)
"""

# startup stuff

def _find_files(prefix):
    """
    Generates list of all the files with a given prefix
    This also adds the appropriate path
    """
    spr_files = os.listdir(os.path.normcase(GDIR.REL_PATH_GAME))

    return [
        GDIR.REL_PATH_GAME + filename
        for filename in spr_files
        if filename.startswith(prefix)
    ]


def _init():
    """
    Startup
    """
    # get files
    static_files = _find_files(STATIC_PREFIX)
    alias_files = _find_files(ALIAS_PREFIX)
    atl_files = _find_files(ATL_PREFIX)

    # add to individual lists
    STATIC_CHARTS.extend(static_files)
    ALIAS_CHARTS.extend(alias_files)
    ATL_CHARTS.extend(atl_files)

    # add to sprite path
    SPRITE_PATH.extend(static_files)
    SPRITE_PATH.extend(alias_files)
    SPRITE_PATH.extend(atl_files)


_init()
