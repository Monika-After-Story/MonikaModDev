## module with a function that pull sprites out of the sprite-chart
#
# VER: Python 2.7

import os
import gamedir as GDIR
import menutils

SPRITE_PATH = GDIR.REL_PATH_GAME + "sprite-chart.rpy"
SAVE_PATH = "zzzz_spritelist"
SAVE_PATH_D = "zzzz_spritedict"
SAVE_PATH_IO = GDIR.REL_PATH_GAME + "zzzz_sprite_opt.rpy"

IMG_START = "image monika"
IMG_OUT = '"monika {0}"'

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

    with open(os.path.normcase(SPRITE_PATH), "r") as sprite_file:
        for line in sprite_file:
            code = pull_sprite_code(line)
            
            if code:
                sprite_list.append(code)

    if as_dict:
        # do we want a dict instead?
        sprite_dict = dict()
        
        for sprite in sprite_list:
            sprite_dict[sprite] = 0

        return sprite_dict

    # otherwise we want the lsit
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

        # make a list of the "monika code" so we can join them later
        code_list = [
            IMG_OUT.format(code)
            for code in sprites
        ]

        outfile.write(",\n        ".join(code_list))
        
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
__ZZ_SP_OPT_HEADER = """
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
    image_list = [
        """

__ZZ_SP_OPT_FOOTER = """
    ]
    renpy.start_predict(*image_list)
"""

