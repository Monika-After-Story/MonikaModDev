# makes sprites
# can also load sprites

import os
import menutils

import spritepuller as spull

from sprite import StaticSprite


class FilterSprite(StaticSprite):
    """
    A Filter sprite is a version of static sprite used for filtering
    other static sprites.

    The primary difference is that any of the initial properties can be
    None
    """
    POS = "position"
    EYE = "eyes"
    EYB = "eyebrows"
    NSE = "nose"
    BLH = "blush"
    TRS = "tears"
    SWD = "sweat"
    EMO = "emote"
    MTH = "mouth"

    def __init__(self, spcode):
        """
        Constructor
        """
        self._init_props()

    def filter(self, otherStaticSprite):
        """
        Checks if the given static sprite passes the filter for this one
        """
        pass

    def set_filter(self, category, code):
        """
        Sets a filter point
        :param category: the filter key to set
        :param code: the code to lookup
        """
        pass

    def __flt_set_pos(self, code):
        """
        Sets position filter
        :param code: the code to lookup
        """
        self.position = self._get_smap(self.POS, code, None)

        if self.position is None:
            self.is_lean = None
        else:
            self.is_lean = self._get_smap("is_lean", code, False)

    def __flt_set_eye(self, code):
        """
        Sets eye filter
        :param code: the code to lookup
        """
        self.eyes = self._get_smap(self.EYE, code, None)






def _load_sprites():
    """
    Loads sprite code data so this module can use it.
    NOTE: if None is returnd, treat as failure
    :returns: dictionary of the following format:
        [0] - sprite code (without static)
        [1] - StaticSprite object
    """
    sprite_list = []

    # load all static sprites
    for sprite_filepath in spull.STATIC_CHARTS:
        with open(os.path.normcase(sprite_filepath), "r") as sprite_file:
            sprite_list.extend(spull.pull_sprite_list_from_file(
                sprite_file,
                True
            ))

    # generate dict of static sprites
    sprite_db = {}
    for sprite_code in sprite_list:
        sprite_obj = StaticSprite(sprite_code)

        # immediately quit if invalid
        if sprite_obj.invalid:
            return None

        # otherwise add
        sprite_db[sprite_code] = sprite_obj

    return sprite_db



# TODO: pull sprites from the static charts and store them here
#   1 - allow user search
#   2 - allow user sprite make

### runners

def run():
    """
    Runs this module (menu related)
    """
    # first load all sprites
    print("Loading sprites...", end="")
    sprite_db = _load_sprites()

    # abort if failed
    if sprite_db is None:
        print("\nERROR in loading sprites. Aborting...")
        return

    # now sort keys
    sprite_db_keys = sorted(sprite_db.keys())

    # otherwise success
    print("DONE")

    choice = menutils.menu(menu_main)

    if choice is None:
        return

    choice(sprite_db, sprite_db_keys)


def run_lstc(sprite_db, sprite_db_keys):
    """
    List codes submenu
    """
    choice = menutils.menu(menu_lstc)

   
def run_srch(sprite_db, sprite_db_keys):
    """
    Interactively searches for a sprite code
    """
    pass



############### menus ############

menu_main = [
    ("Sprite Maker", "Option: "),
    ("Search Code", run_srch),
    ("List Codes", run_lstc),
    ("Make Sprite", run_mkspr),
]

menu_lstc = [
    ("Filter Options", "Option: "),
    ("Show List", run_lstc_show),
    ("Show Filters", run_lstc_showfilter),
    ("Set Filter", run_lstc_setfilter),
]
