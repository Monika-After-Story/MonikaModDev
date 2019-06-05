# makes sprites
# can also load sprites

from __future__ import print_function

import os
import menutils

import spritepuller as spull

from sprite import StaticSprite


class SortedKeySpriteDBIter(object):
    """
    Iterator over a sprite db. This iterates so that the StaticSprites are
    in key order (aka from the given list of keys)
    """

    def __init__(self, sprite_db, sprite_db_keys):
        """
        Constructor for this iterator
        """
        self.index = -1
        self.sprite_db = sprite_db
        self.sprite_db_keys = sprite_db_keys

        # create an empty filter sprite so we dont have crashes during
        # iteration
        self.__default_fs = FilterSprite()
        self.__default_fs.invalid = True

    def __iter__(self):
        return self

    def next(self):
        """
        returns next iteration item
        """
        if self.index < len(self.sprite_db_keys)-1:
            self.index += 1
            return self.sprite_db.get(
                self.sprite_db_keys[self.index],
                self.__default_fs
            )

        # otherwise dnoe iterationg
        raise StopIteration


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

    CLEAR = "CLEAR"

    def __init__(self):
        """
        Constructor
        """
        self._init_props()

        # setup filter map
        self.__filter_set_map = {
            self.POS: self.__flt_set_pos,
            self.EYE: self.__flt_set_eye,
            self.EYB: self.__flt_set_eyb,
            self.NSE: self.__flt_set_nse,
            self.BLH: self.__flt_set_blh,
            self.TRS: self.__flt_set_trs,
            self.SWD: self.__flt_set_swd,
            self.EMO: self.__flt_set_emo,
            self.MTH: self.__flt_set_mth,
        }

        # setup eq map
        self.__filter_eq_map = {
            self.POS: self.__flt_eq_pos,
            self.EYE: self.__flt_eq_eye,
            self.EYB: self.__flt_eq_eyb,
            self.NSE: self.__flt_eq_nse,
            self.BLH: self.__flt_eq_blh,
            self.TRS: self.__flt_eq_trs,
            self.SWD: self.__flt_eq_swd,
            self.EMO: self.__flt_eq_emo,
            self.MTH: self.__flt_eq_mth,
        }

        self._dbl_tab = self._tab + self._tab
        self._flt_fmt = "{: <12}"

        self.menu_flt_set = [
            ("Set Filters", "Filter: "),
            (self.POS.title(), self.POS),
            (self.EYE.title(), self.EYE),
            (self.EYB.title(), self.EYB),
            (self.NSE.title(), self.NSE),
            (self.BLH.title(), self.BLH),
            (self.TRS.title(), self.TRS),
            (self.SWD.title(), self.SWD),
            (self.EMO.title(), self.EMO),
            (self.MTH.title(), self.MTH),
        ]

    def __str__(self):
        """
        The string representation of this is a neat thing showing the status
        of each filter
        """
        # initial setup strings + position
        msg = [menutils.header("Filter Settings")]

        # lean and position check
        if self.position is None:
            position = None
            is_lean = None
        elif self.is_lean:
            position = StaticSprite.lean_tostring(self.position)
            is_lean = True
        else:
            position = self.position 
            is_lean = self.is_lean

        # now add each filter piece
        self.__fmt_flt(msg, "Position:", position)
        self.__fmt_flt(msg, "Is Lean:", is_lean)
        self.__fmt_flt(msg, "Eyes:", self.eyes)
        self.__fmt_flt(msg, "Eyebrows:", self.eyebrows)
        self.__fmt_flt(msg, "Nose:", self.nose)
        self.__fmt_flt(msg, "Blush:", self.blush)
        self.__fmt_flt(msg, "Tears:", self.tears)
        self.__fmt_flt(msg, "Sweatdrop:", self.sweatdrop)
        self.__fmt_flt(msg, "Emote:", self.emote)
        self.__fmt_flt(msg, "Mouth:", self.mouth)

        return "".join(msg)

    def filter(self, otherStaticSprite):
        """
        Checks if the given static sprite passes the filter for this one
        :param otherStaticSprite: the Static sprite object to compare to
        :returns: True if this sprite passes the filter, False if not
        """
        if otherStaticSprite.invalid:
            return False

        for flt in self.__filter_eq_map.itervalues():
            if not flt(otherStaticSprite):
                return False

        return True

    def set_filter(self, category, code):
        """
        Sets a filter point
        :param category: the filter key to set
        :param code: the code to lookup
        """
        flt_setter = self.__filter_set_map.get(category, None)
        if flt_setter is not None:
            flt_setter(code)

    @staticmethod
    def build_menu(category):
        """
        Builds a menu based on the given category
        :param category: one of the class constants 
        :returns: menu list usable by menutils. May return None if could not
            build list
        """
        is_positions = category == FilterSprite.POS

        selections = FilterSprite._sprite_map.get(category, None)
        if selections is None:
            return None

        sorted_keys = sorted(selections.keys())

        # build the menu
        # title goes first
        menu = [ (category.title() + " Codes", "Code: ") ]

        # now the items
        for code in sorted_keys:
            name = selections[code]
            if is_positions and type(name) is not str:
                menu.append((StaticSprite.lean_tostring(name), code))

            else:
                menu.append((name, code))

        # append an option to clear the filter
        menu.append(("Clear Filter", FilterSprite.CLEAR))

        return menu

    def __flt_eq_pos(self, other):
        """
        Checks if this position is same as other
        :param other: the other static sprite
        :returns: False if not None and does not match, True otherwise
        """
        if self.position is None:
            return True

        return (
            self.position == other.position
            and self.is_lean == other.is_lean
        )

    def __flt_eq_eye(self, other):
        """
        Checks if this eqyes is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.eyes is None:
            return True

        return self.eyes == other.eyes

    def __flt_eq_eyb(self, other):
        """
        Checks if this eyebrows is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.eyebrows is None:
            return True

        return self.eyebrows == other.eyebrows

    def __flt_eq_nse(self, other):
        """
        Checks if this nose is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.nose is None:
            return True

        return self.nose == other.nose

    def __flt_eq_blh(self, other):
        """
        Checks if this blush is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.blush is None:
            return True

        return self.blush == other.blush

    def __flt_eq_trs(self, other):
        """
        Checks if this tears is same as other
        :param other: the StaticSprite to compare to
        "returns: False if not None and does not match, True otherwise
        """
        if self.tears is None:
            return True

        return self.tears == other.tears

    def __flt_eq_swd(self, other):
        """
        Checks if this sweatdrop is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.sweatdrop is None:
            return True

        return self.sweatdrop == other.sweatdrop

    def __flt_eq_emo(self, other):
        """
        Checks if this emote is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.emote is None:
            return True

        return self.emote == other.emote

    def __flt_eq_mth(self, other):
        """
        Checks if this mouth is same as other
        :param other: the StaticSprite to compare to
        :returns: False if not None and does not match, True otherwise
        """
        if self.mouth is None:
            return True

        return self.mouth == other.mouth

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

    def __flt_set_eyb(self, code):
        """
        Sets eyebrow filter
        :param code: the code to lookup
        """
        self.eyebrows = self._get_smap(self.EYB, code, None)

    def __flt_set_nse(self, code):
        """
        Sets nose filter
        :param code: the code to lookup
        """
        self.nose = self._get_smap(self.NSE, code, None)

    def __flt_set_blh(self, code):
        """
        Sets blush filter
        :param code: the code to lookup
        """
        self.blush = self._get_smap(self.BLH, code, None)

    def __flt_set_trs(self, code):
        """
        Sets tears filter
        :param code: the code to lookup
        """
        self.tears = self._get_smap(self.TRS, code, None)

    def __flt_set_swd(self, code):
        """
        Sets sweatdrop filter
        :param code: the code to lookup
        """
        self.sweatdrop = self._get_smap(self.SWD, code, None)

    def __flt_set_emo(self, code):
        """
        Sets emote filter
        :param code: the code to lookup
        """
        self.emote = self._get_smap(self.EMO, code, None)

    def __flt_set_mth(self, code):
        """
        Sets mouth filter
        :param code: the code to lookup
        """
        self.mouth = self._get_smap(self.MTH, code, None)

    def __fmt_flt(self, msg_arr, string, value):
        """
        adds appropraitely formatted filter string to msg arr
        """
        if value is None:
            value_str = ""
        else:
            value_str = str(value)

        msg_arr.extend([
            "\n",
            self._tab,
            self._flt_fmt.format(string),
            value_str
        ])


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

    choice = True
    while choice is not None:
        choice = menutils.menu(menu_main)

        if choice is not None:
            choice(sprite_db, sprite_db_keys)


def run_mkspr(sprite_db, sprite_db_keys):
    """
    """
    pass


def run_lstc(sprite_db, sprite_db_keys):
    """
    List codes submenu
    """
    choice = True
    ss_filter = FilterSprite()

    while choice is not None:
        choice = menutils.menu(menu_lstc)

        if choice is not None:
            choice(sprite_db, sprite_db_keys, ss_filter)


def run_lstc_show(sprite_db, sprite_db_keys, ss_filter):
    """
    Show sprites, based on filter
    """
    # filter valid sprites
    filtered = filter(
        ss_filter.filter,
        SortedKeySpriteDBIter(sprite_db, sprite_db_keys)
    )

    # show codes
    menutils.paginate(
        "Sprite Codes",
        filtered,
        str_func=StaticSprite.as_scstr_code
    )


def run_lstc_showfilter(sprite_db, sprite_db_keys, ss_filter):
    """
    Show filter settings
    """
    menutils.clear_screen()
    print(str(ss_filter))
    menutils.e_pause()


def run_lstc_setfilter(sprite_db, sprite_db_keys, ss_filter):
    """
    Set filter settings
    """
    choice = True

    while choice is not None:
        choice = menutils.menu(ss_filter.menu_flt_set)

        if choice is not None:
            # get a menu baesd on the category
            category_menu = FilterSprite.build_menu(choice)
            if category_menu is not None:
                code = menutils.menu(category_menu)
                
                # set if not none
                if code is not None:
                    ss_filter.set_filter(choice, code)


def run_srch(sprite_db, sprite_db_keys):
    """
    Interactively searches for a sprite code
    """
    pass



############### menus ############

menu_main = [
    ("Sprite Maker", "Option: "),
#    ("Search Code", run_srch),
    ("List Codes", run_lstc),
#    ("Make Sprite", run_mkspr),
]

menu_lstc = [
    ("Filter Options", "Option: "),
    ("Show List", run_lstc_show),
    ("Show Filters", run_lstc_showfilter),
    ("Set Filter", run_lstc_setfilter),
]
