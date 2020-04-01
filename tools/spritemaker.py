# makes sprites
# can also load sprites

from __future__ import print_function

import os
import gamedir as GDIR
import menutils

import spritepuller as spull

import sprite as spr_module

from sprite import StaticSprite

# state vars

_need_to_gen_sprites = False

# classes

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
    OPTIONAL = "OPTIONAL"

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
        return self._status(True, "Filter Settings", True, True)

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
        menu = FilterSprite._build_menu(category)
        if menu is None:
            return None

        # add title
        menu.insert(0, (category.title() + " Codes", "Code: "))

        # append an option to clear the filter
        menu.append(("Clear Filter", FilterSprite.CLEAR))

        return menu

    @staticmethod
    def build_selection_menu(category, optional=False, headeradd=""):
        """
        Builds a seleciton menu based on the given cateogory
        :param category: one of the class constants
        :param optional: True will add an optional option, basically skips
        setting this.
        :param headeradd: add text here to be appended to the header
        :returns: menu list usable by menutils. May return None if could not
        build list
        """
        menu = FilterSprite._build_menu(category)
        if menu is None:
            return None

        # add title part
        menu.insert(
            0,
            ("Select " + category.title() + headeradd, "Option: ")
        )

        # add optional
        if optional:
            menu.append(("No " + category.title(), FilterSprite.OPTIONAL))

        return menu

    @staticmethod
    def from_ss(static_spr):
        """
        Generates a FilterSprite object from a StaticSprite

        May return None if invalid static sprite
        """
        if static_spr.invalid:
            return None

        filter_spr = FilterSprite()
        filter_spr.position = static_spr.position
        filter_spr.eyes = static_spr.eyes
        filter_spr.eyebrows = static_spr.eyebrows
        filter_spr.nose = static_spr.nose
        filter_spr.blush = static_spr.blush
        filter_spr.tears = static_spr.tears
        filter_spr.sweatdrop = static_spr.sweatdrop
        filter_spr.emote = static_spr.emote
        filter_spr.mouth = static_spr.mouth
        filter_spr.is_lean = static_spr.is_lean
        filter_spr.sides = static_spr.sides
        filter_spr.single = static_spr.single
        filter_spr.head = static_spr.head
        filter_spr.spcode = static_spr.spcode

        return filter_spr

    @staticmethod
    def _build_menu(category):
        """
        Builds menu options for a category

        May return None if errors occured
        """
        is_positions = category == FilterSprite.POS

        selections = FilterSprite._sprite_map.get(category, None)
        if selections is None:
            return None

        sorted_keys = sorted(selections.keys())

        menu = []

        # now the items
        for code in sorted_keys:
            name = selections[code]
            if is_positions and type(name) is not str:
                menu.append((StaticSprite.lean_tostring(name), code))

            else:
                menu.append((name, code))

        return menu

    def _status(self,
            useheader,
            headerstring, 
            shownose,
            showemote
    ):
        """
        Builds string representation of this Filter according to given
        status props
        :param useheader: True will use the block header from menutils,
            False will not
        :param headerstring: the string to use in the header
        :param shownose: True will show the nose part of the filter, False
            will not
        :param showemote: True will show the emote part of the filter, False
            will not
        """
        # setup initial strings
        if useheader:
            msg = [menutils.header(headerstring)]
        else:
            msg = [self._tab + headerstring]

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
        if shownose:
            self.__fmt_flt(msg, "Nose:", self.nose)
        self.__fmt_flt(msg, "Blush:", self.blush)
        self.__fmt_flt(msg, "Tears:", self.tears)
        self.__fmt_flt(msg, "Sweatdrop:", self.sweatdrop)
        if showemote:
            self.__fmt_flt(msg, "Emote:", self.emote)
        self.__fmt_flt(msg, "Mouth:", self.mouth)

        return "".join(msg)

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


def gen_sprite_files(
        sprites,
        file_prefix,
        file_template,
        file_header,
        spacing="\n\n",
        tostring=str,
        quiet=False,
        sp_per_file=500,
        skip_pause=True,
        skip_continue=True
):
    """
    Generates sprite files. 

    IN:
        sprites - the list of sprite objects to generate stuff for
        file_prefix - the prefix for each filename
        file_template - the template for each filename
        file_header - the header to write at the top of each file
        spacing - spacing between items
            (Default: \n\n)
        tostring - to string function to use (must take a sprite object)
            (Default: str)
        quiet - True will supress menus and stdout
            (Default: False)
        sp_per_file - max number of sprites allowed per file
            (Default: 500)
        skip_pause - True will skip pause at end. False will not
            (Default: True)
        skip_continue - True will skip the continue. False will not

    RETURNS: True if successful, False if abort
    """
    # first, check if we will go over the max file limit
    if ( int(len(sprites) / sp_per_file) + 1) > spull.MAX_FILE_LIMIT:
        # always show error messages
        print(MSG_OVER_FILE_LIMIT.format(
            len(sprites),
            spull.MAX_FILE_LIMIT
        ))
        return False

    # ask user to continue
    if not (quiet or skip_continue):
        print(MSG_OVERWRITE.format(file_prefix))
        if not menutils.ask_continue():
            return False

    # setup file counts
    file_num = 0
    sp_count = 0

    # and file data
    filename = file_template.format(file_num)
    filepath = GDIR.REL_PATH_GAME + filename

    # create thef irst file
    if not quiet:
        print(MSG_GEN_FILE.format(filename), end="")
    output_file = open(os.path.normcase(filepath), "w")
    output_file.write(file_header)

    # begin loop over sprites
    for sprite_obj in sprites:

        if sp_count >= sp_per_file:
            # over the sprites per file limit. we should make new file.

            # increment counts
            sp_count = 0
            file_num += 1

            # close file and say done
            output_file.close()
            if not quiet:
                print("done")

            # setup next file stuff
            filename = file_template.format(file_num)
            filepath = GDIR.REL_PATH_GAME + filename

            # open file
            if not quiet:
                print(MSG_GEN_FILE.format(filename), end="")
            output_file = open(os.path.normcase(filepath), "w")
            output_file.write(file_header)

        # add sprite object to file
        output_file.write(tostring(sprite_obj))
        output_file.write(spacing)
        sp_count += 1

    # finally, close the last file and say done
    output_file.close()
    if not quiet:
        print("done")

        if not skip_pause:
            menutils.e_pause()

    return True


def make_sprite(sprite_db, sprite_db_keys):
    """
    Makes a sprite and adds it to the sprite database.
    NOTE: keys should be regenerated after this by the caller

    RETURNS: True if sprite creation successful, False if not
    """
    sprite_obj = FilterSprite()
    sprite_code = []

    # this is the order we ask for sprites as it is the order of the
    # sprite code
    sprite_parts = (
        (FilterSprite.POS, False),
        (FilterSprite.EYE, False),
        (FilterSprite.EYB, False),
        # NOTE: we skip nose because there is only 1
#        FilterSprite.NSE,
        (FilterSprite.BLH, True),
        (FilterSprite.TRS, True),
        (FilterSprite.SWD, True),
        # NOTE: emote skipped 
#        FilterSprite.EMO,
        (FilterSprite.MTH, False),
    )

    for sp_cat, is_optional in sprite_parts:
        sel_not_chosen = True

        # loop until user selection
        while sel_not_chosen:

            # generate menu
            sel_menu = FilterSprite.build_selection_menu(
                sp_cat,
                optional=is_optional,
                headeradd=" - " + "".join(sprite_code)
            )

            # if optional, we set the default to optional, which is always
            # the last item
            if is_optional:
                defindex = len(sel_menu) - 1
            else:
                defindex = None

            # now run teh menu
            sel_code = menutils.menu(sel_menu, defindex)

            if sel_code is not None:
                # a selection was chosen, check if optinal

                if sel_code != FilterSprite.OPTIONAL:
                    # actual code selected, update the filter sprite and
                    # the sprite code list
                    sprite_code.append(sel_code)
                    sprite_obj.set_filter(sp_cat, sel_code)

                # mark as selected
                sel_not_chosen = False

            else:
                # Exit was reached, verify if we actually want to exit
                print("\nExiting will abort the creation of this sprite!\n")
                if menutils.ask("Discard this sprite"):
                    return False

    # if we reached here, we should have a sprite now
    menutils.clear_screen()

    # lets double check if this is a duplicate
    sprite_code = "".join(sprite_code)
    if sprite_code in sprite_db:
        print("\n\nSprite code {0} already exists! Aborting...".format(
            sprite_code
        ))
        menutils.e_pause()
        return False

    # otherwise, no duplicate
    # lets show the user and then confirm
    print(sprite_obj._status(
        True,
        "Selected Sprite Settings - " + sprite_code,
        False,
        False
    ))

    # TODO: ask user if they would want to see a preview. Get libpng and
    #   generate a composite image with the appropraite paths. This is
    #   really a stretch since exp_previewer covers this already.

    # spacing
    print("\n\n")

    # ask to create the sprite
    if not menutils.ask("Create sprite"):
        print("\nSprite discarded.")
        menutils.e_pause()
        return False

    # user said yes!
    # create the sprite
    real_sprite = StaticSprite(sprite_code)

    # now determine if we need an atl variant
    atl_sprite = real_sprite.make_atl()

    # print and abort if errors occured
    if real_sprite.invalid or (atl_sprite is not None and atl_sprite.invalid):
        menutils.clear_screen()
        print("\n\nError making this sprite. Notify devs to fix.")
        menutils.e_pause()
        return False

    # otherwise we ok
    sprite_db[real_sprite.spcode] = real_sprite

    if atl_sprite is not None:
        sprite_db[atl_sprite.spcode] = atl_sprite

    return True


def make_sprite_bc(sprite_db, sprite_db_keys):
    """
    Makes sprite using just a code and adds it to sprite database.
    NOTE: keys should be regenerated after this by the caller

    RETURNS: True if sprite creation successful, False if not
    """
    not_valid_code = True
    sprite_created = False
    while not_valid_code:
        menutils.clear_screen()
        print("\n\n")
        trycode = raw_input("Enter a sprite code: ")

        # build a static sprite with the code
        new_sprite = StaticSprite(trycode)

        # and atl version
        atl_sprite = new_sprite.make_atl()

        if new_sprite.invalid or (atl_sprite is not None and atl_sprite.invalid):
            # if invalid, ask user if they want to continue
            print("\nSprite code {0} is invalid.\n".format(trycode))
            if not menutils.ask("Try again", def_no=False):
                return sprite_created

        elif new_sprite.spcode in sprite_db:
            # check if already exists
            print("\nSprite code {0} already exists!\n".format(
                new_sprite.spcode
            ))
            if not menutils.ask("Try again", def_no=False):
                return sprite_created

        else:
            # valid sprite, means we should show it and ask for confirm
            filter_spr = FilterSprite.from_ss(new_sprite)
            print(filter_spr._status(
                True,
                "Selected Sprite Settings - " + new_sprite.spcode,
                True,
                True
            ))

            # spacing
            print("\n\n")

            # ask to create the sprite
            if not menutils.ask("Create sprite"):
                print("\nSprite discarded.\n")

            else:
                # user said yes!
                # add sprite to db and prompt for more
                sprite_db[new_sprite.spcode] = new_sprite

                if atl_sprite is not None:
                    sprite_db[atl_sprite.spcode] = atl_sprite

                sprite_created = True
                print("\nSprite created.\n")

            if not menutils.ask("Create another sprite", def_no=False):
                return sprite_created


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

        # set apropriate title text
        if _need_to_gen_sprites:
            title_entry = ("Sprite Maker" + MSG_UNSAVED, "Option: ")
        else:
            title_entry = ("Sprite Maker", "Option: ")

        menu_main[0] = title_entry

        choice = menutils.menu(menu_main)

        if choice is not None:
            result = choice(sprite_db, sprite_db_keys)

            # only make sprite returns a value, which is the updated keys
            # list
            if result is not None:
                sprite_db_keys = result

        elif _need_to_gen_sprites:
            # user hit None, but we should make sure that they wanted to leave
            # without saving changes
            menutils.clear_screen()
            print("\n\n" + MSG_WARN_GEN)
            if not menutils.ask("Leave this menu"):
                choice = True


def run_gss(sprite_db, sprite_db_keys, quiet=False, sp_per_file=500):
    """
    Generates static sprites, and alises

    IN:
        quiet - supresses menus and stdout
        sp_per_file - max number of sprites allowed per file
    """
    # ask for draw function to use
    if not quiet:
        df_choice = True
        while df_choice is not None:
            df_choice = menutils.menu(menu_sdf, defindex=1)

            # if no choice was made here (or we aborted), then quit
            if df_choice is None:
                return

            # otherwise set and quit loop
            spr_module.draw_function = df_choice
            df_choice = None

    # ask if okay to overwrite files
    if not quiet:
        print("\n" + MSG_OVERWRITE.format(
            ", ".join([
                spull.STATIC_PREFIX,
                spull.ALIAS_PREFIX,
                spull.ATL_PREFIX
            ])
        ))
        if not menutils.ask_continue():
            return

    # generate static sprites
    if not gen_sprite_files(
            list(SortedKeySpriteDBIter(sprite_db, sprite_db_keys)),
            spull.STATIC_PREFIX,
            spull.STATIC_TEMPLATE,
            __SP_STATIC_HEADER,
            quiet=quiet,
            sp_per_file=sp_per_file
    ):
        return

    # now for filter sprites
    if not gen_sprite_files(
            filter(
                StaticSprite.as_is_closed_eyes,
                SortedKeySpriteDBIter(sprite_db, sprite_db_keys)
            ),
            spull.ALIAS_PREFIX,
            spull.ALIAS_TEMPLATE,
            __SP_STATIC_HEADER,
            spacing="\n",
            tostring=StaticSprite.as_alias_static,
            quiet=quiet,
            sp_per_file=5000
    ):
        return

    # and finally atl sprites
    if not gen_sprite_files(
            filter(
                StaticSprite.as_is_not_closed_eyes,
                SortedKeySpriteDBIter(sprite_db, sprite_db_keys)
            ),
            spull.ATL_PREFIX,
            spull.ATL_TEMPLATE,
            __SP_STATIC_HEADER,
            tostring=StaticSprite.as_atlify,
            quiet=quiet,
            sp_per_file=sp_per_file
    ):
        return

    # done, print done
    if not quiet:
        menutils.e_pause()

    global _need_to_gen_sprites
    _need_to_gen_sprites = False


def run_mkspr(sprite_db, sprite_db_keys):
    """
    Makes a sprite. 

    Returns an updated sprite_db_keys, or None if no changes
    """
    if make_sprite(sprite_db, sprite_db_keys):
        # success we made a sprite

        # mark that we are dirty and need to regen
        global _need_to_gen_sprites
        _need_to_gen_sprites = True

        # return updated keys
        return sorted(sprite_db.keys())

    return None


def run_mkspr_bc(sprite_db, sprite_db_keys):
    """
    Makes a sprite.

    Returns an updated sprite_db_keys, or None if no changes
    """
    if make_sprite_bc(sprite_db, sprite_db_keys):
        # we made some sprites

        # mark that we are dirty and need to regin
        global _need_to_gen_sprites
        _need_to_gen_sprites = True

        # return updated keys
        return sorted(sprite_db.keys())

    return None


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


############### menus ############

menu_main = [
    ("Sprite Maker", "Option: "),
    ("List Codes", run_lstc),
    ("Make Sprite (Interactive)", run_mkspr),
    ("Make Sprite (By Code)", run_mkspr_bc),
    ("Generate Sprites", run_gss),
]

menu_lstc = [
    ("Filter Options", "Option: "),
    ("Show List", run_lstc_show),
    ("Show Filters", run_lstc_showfilter),
    ("Set Filter", run_lstc_setfilter),
]

menu_sdf = [
    ("Set Draw Function", "Option: "),
    (
        "Image Manipulators (" + spr_module.DRAW_MONIKA_IM + ")",
        spr_module.DRAW_MONIKA_IM
    ),
    (
        "Sprite Strings (" + spr_module.DRAW_MONIKA + ")",
        spr_module.DRAW_MONIKA
    ),
]

# strings

MSG_OVERWRITE = (
    "This will overwrite all sprite chart files that start with:\n    {0}\n"
)

MSG_OVER_FILE_LIMIT = "\nCannot fit {0} sprites into {1} files. Aborting..."
MSG_GEN_FILE = "Generating file '{0}'..."
MSG_WARN_GEN = (
    "WARNING! You have created a sprite but have not regenerated the sprite "
    "charts.\nLeaving this menu will abort your changes.\n"
)
MSG_UNSAVED = " - **Run Generate Sprites to save changes**"

__SP_STATIC_HEADER = """\
############################ AUTO-GENERATED ###################################
## DO NOT EDIT THIS FILE                                                     ##
##                                                                           ##
## This was auto-generated by the the spritemaker tool                       ##
###############################################################################

"""

# internal functions


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

