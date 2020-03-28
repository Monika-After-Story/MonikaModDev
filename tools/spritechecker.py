# module that checks dialogue lines for proper expression code usage
# 
# this will NOT catch issues with non-standard code usage
# TODO: add special functions for non-standard usages
#
# VER: py27

import os
import spritepuller as spp
import gamedir as GDIR

import menutils

from collections import namedtuple

# every line of applicable dialogue starts with m and a space
DLG_START = "m "

# every show line starts with show monika
SHW_START = "show monika"

#Every extend line starts with extend
EXT_START = "extend "

# special key words that are unique to show lines
SHW_KEY = [
    "at",
    "zorder",
    "as",
    "with"
]

EXT_RPY = ".rpy"

# bad code file name
BAD_CODE_FN = "zzzz_badcodes.txt"
BAD_CODE_LN = "{1} - FILE:{2} [{0}]"

## namedtuple used to represent sprite codes not found
SpriteMismatch = namedtuple(
    "SpriteMismatch",
    "code line filename"
)

def check_sprites(inc_dev=False):
    """
    Goes through every rpy file and checks dialogue and show lines.

    If a sprite code is used in a non-standard way, this will miss those cases

    IN:
        inc_dev - if True, we will check dev files as well
            (Defualt: False)

    RETURNS:
        list of SpriteMismatch's
    """
    # sprite dict so we can compare to this
    # we want a dict for O(1) lookups
    sp_dict = spp.pull_sprite_list(as_dict=True)

    # get all the rpys we want to adjust
    rpys = get_rpy_paths(inc_dev=inc_dev)

    # go through each rpy and get sprite mms
    bad_codes = list()
    for rpy in rpys:
        bad_codes.extend(check_file(rpy, sp_dict))

    return bad_codes


def check_file(fpath, sp_dict):
    """
    Checks the given file for sprite code correctness

    IN:
        fpath - filepath of the fie to check
        sp_dict - dict of currently available sprite codes

    RETURNS:
        list of SpriteMismatches, one for every sprite code that was bad
    """
    sp_mismatches = list()
    ln_count = 1

    with open(fpath, "r") as rpy_file:
        for line in rpy_file:

            # clean the line first
            cl_line = line.strip()

            # check what kind of line this is
            # first, lets try dialogue
            _code = extract_code_if_dlg(cl_line)

            if _code is None:
                # okay, then try show line
                _code = extract_code_if_shw(cl_line)

            #Otherwise it may be an extend line. Let's try that
            if _code is None:
                _code = extract_code_if_ext(cl_line)

            if _code and _code not in sp_dict:
                # we have a code but its not in the dict?!
                sp_mismatches.append(SpriteMismatch(_code, ln_count, fpath))

            ln_count += 1

    return sp_mismatches


def extract_dlg_code(line):
    """
    Extracts the sprite code from the given line
    Assumes the line is a dlg line or extend line

    IN:
        line - line to get sprite code

    RETURNS:
        sprite code extracted
    """
    return line.split(" ")[1]


def extract_code_if_dlg(line):
    """
    Does both checking and extraction of a code from a potential dialogue
    line

    IN:
        line - line to check and get sprite code

    RETURNS:
        the extracted sprite code, or None if no sprite code found
    """
    if line.startswith(DLG_START):
        # line is dlg line

        code = extract_dlg_code(line)
        if code.startswith('"') or code.startswith("'"):
            return None

        # otherwise we have a dlg code
        return code

    return None


def extract_shw_code(line):
    """
    Extracts the sprite code from the given line
    Assumes the line is a show line

    IN:
        line - line to get sprite code

    RETURNS:
        sprite code extracted
    """
    return line.split(" ")[2]


def extract_code_if_shw(line):
    """
    Does both checking and extractiong of a code from a potential show line

    IN:
        line - line to check and get srpite code

    RETURNS:
        the extracted sprite code, or None if no sprite found
    """
    if line.startswith(SHW_START):
        # line is a show line

        code = extract_shw_code(line)
        if code in SHW_KEY:
            # its a valid keyword for show line, not a sprite code
            return None

        # otherwise we have a code
        return code

    return None

def extract_code_if_ext(line):
    """
    Does both checking and extractiong of a code from a potential extend line

    IN:
        line - line to check and get srpite code

    RETURNS:
        the extracted sprite code, or None if no sprite found
    """
    if line.startswith(EXT_START):
        # line is an extend line

        code = extract_dlg_code(line)
        if code.startswith('"') or code.startswith("'"):
            return None

        # otherwise we have a dlg code
        return code

    return None

def get_rpy_paths(inc_dev=False):
    """
    Gets a list of all filepaths in teh game dir that are rpy files.
    Non-recursive

    IN:
        inc_dev - if True, we will include dev rpys as well
            (Default: False)

    RETURNS:
        list of filepaths in the game dir that are rpy files.
    """
    fp_list = os.listdir(GDIR.REL_PATH_GAME)

    # we only want rpys
    fp_list = [
        os.path.normcase(GDIR.REL_PATH_GAME + fp)
        for fp in fp_list
        if fp.endswith(EXT_RPY)
    ]

    # include dev items?
    if inc_dev:
        dev_list = os.listdir(GDIR.REL_PATH_DEV)
        dev_list = [
            os.path.normcase(GDIR.REL_PATH_DEV + fp)
            for fp in dev_list
            if fp.endswith(EXT_RPY)
        ]

        fp_list.extend(dev_list)

    return fp_list


def write_bad_codes(bad_list):
    """
    Writes out the bad codes to file

    IN:
        bad_list - list of SpriteMismatches found
    """
    with open(BAD_CODE_FN, "w") as outfile:
        for bad_code in bad_list:
            outfile.write(
                BAD_CODE_LN.format(
                    bad_code.line,
                    bad_code.code,
                    bad_code.filename
                ) + "\n"
            )


############## special run methods ##################################

def run():
    """
    Runs this module (menu-related)
    """
    # for now, we only have 1 workflow
    run_chk(False)


def run_chk(quiet=False, inc_dev=False):
    """
    Main sprite checker workflow

    IN:
        quiet - True will suppress output
        inc_dev - True will include dev files in check, False will not
    """
    if not quiet:
        inc_dev = menutils.menu(menu_inc_dev)

        if inc_dev is None:
            return

    bad_codes = check_sprites(inc_dev=inc_dev)

    if len(bad_codes) == 0:
        # no bad codes
        if not quiet:
            print("All sprite codes accounted for!")
            menutils.e_pause()
        return

    # otherwise, bad codes found, we should write them out
    if not quiet:
        print("We found some invalid sprites. Writing results to " + BAD_CODE_FN)

    write_bad_codes(bad_codes)

    if not quiet:
        print("\nDone")
        menutils.e_pause()   


############## menus ############
menu_inc_dev = [
    ("Include Dev?","Option: "),
    ("Yes", True),
    ("No", False)
]
