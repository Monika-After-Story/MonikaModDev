## module that contains a workable selection screen?
#
# NOTE: i have no idea how generic this can get.
#   Chances are, it will not be very generic.
#
# Selection MAPS:
#   new class: Selec


# databaess for selectable sprite data
# key: name of item
# value: tuple containing data
default persistent._mas_selspr_acs_db = {}
default persistent._mas_selspr_hair_db = {}
default persistent._mas_selspr_clothes_db = {}

init -100 python in mas_selspr:
    import store
    import store.mas_utils as mas_utils

    # prompt constants go here
    PROMPT_MAP = {
        "clothes": {
            "_ev": "monika_clothes_select",
            "change": "Can you change your clothes?",
        },
        "hair": {
            "_ev": "monika_hair_select",
            "change": "Can you change your hairstyle?",
        },
        "left-hair-clip": {
            "_ev": "monika_hairclip_select",
            "change": "Can you change your hairclip?",
            "wear": "Can you wear a hairclip?",
        },
        "left-hair-flower": {
            "_ev": "monika_hairflower_select",
            "change": "Can you change the flower in your hair?",
            "wear": "Can you wear a flower in your hair?",
        },
        "ribbon": {
            "_ev": "monika_ribbon_select",
            "change": "Can you change your ribbon?",
            "wear": "Can you wear a ribbon?",
        },
    }


    def get_prompt(key, prompt_key="change"):
        """
        Gets prompt with the given key and prompt key

        IN:
            key - select key
            prompt_key - key to get prompt

        RETURNS: prompt. "" if invalid
        """
        if prompt_key == "_ev":
            return ""

        return PROMPT_MAP.get(key, {}).get(prompt_key, "")


    def in_prompt_map(key):
        """
        Checks if a key is in the prompt select map

        IN:
            key - select key to check

        RETURNS: True if in the map, FAlse if not
        """
        return key in PROMPT_MAP


    def set_prompt(key, prompt_key="change"):
        """
        Sets prompt of ev with the given key with one associatd with given
        prompt key.

        IN:
            key - select key
            prompt_key - key to get propmt. if _ev, then no change
        """
        if prompt_key == "_ev":
            return

        prompt_data = PROMPT_MAP.get(key, {})

        ev = store.mas_getEV(prompt_data.get("_ev", None))
        prompt = prompt_data.get(prompt_key, None)

        if ev is not None and prompt is not None:
            ev.prompt = prompt


init -20 python:

    class MASSelectableSprite(object):
        """
        Wrapper around selectable sprite objects. We do this instead of
        extending because not everything would be selectble

        PROPERTIES:
            name - this is always the same thing as the MASSprite object we
                create thsi with.
            display_name - the name to use in the selectbale button screen
            thumb - thumbnail image to use for selection screen. Aim for a
                180x180
                (png is added in the constructor)
            group - string id to group related selectable sprites. this really
                applies only to acs, but in case other things need this.
            unlocked - True if this selectable sprite can be selected,
                False otherwise.
            visible_when_locked - True if this should be visible when locked
                False, otherwise.
                Locked items will generally be displayed with a placeholder
                thumb.
            hover_dlg - list of text to display when hovering over the object
            first_select_dlg - text to display the first time you
                select this sprite
            select_dlg - list text to display everytime you select this sprite
                (after the first time)
            selected - True if this item is selected, False if not
        """


        def __init__(self,
                _sprite_object,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            Selectable sprite objects constructor

            IN:
                _sprite_object - MASSpriteBase object to build this selectable
                    sprite object with.
                    NOTE: because of inheritance issues, this is NOT CHECKED.
                        The extending classes MUST check types.
                display_name - name to show on the selectable screen
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - list of text to display when hovering over the
                    object
                    (Default: None)
                first_select_dlg - text to display the first time you select
                    this sprite
                    (Default: None)
                select_dlg - list of text to display everytime you select this
                    sprite
                    (after the first time)
                    (Default: None)
            """
#            self._check_dlg(hover_dlg)
#            self._check_dlg(first_select_dlg)
#            self._check_dlg(select_dlg)

            self.name = _sprite_object.name
            self.display_name = display_name
            self.thumb = thumb + ".png"
            self.group = group
            self.unlocked = False
            self.visible_when_locked = visible_when_locked
            self.hover_dlg = hover_dlg
            self.first_select_dlg = first_select_dlg
            self.select_dlg = select_dlg
            self.selected = False

            # by default
            # NOTE: only ACS can override this
            self.remover = False


        def _check_dlg(self, dlg):
            if dlg is not None and not renpy.has_label(dlg):
                raise Exception("label '{0}' no exist".format(dlg))


        def _build_thumbstr(self):
            """
            Returns thumb string for this selectable
            """
            return MASSelectableImageButtonDisplayable.THUMB_DIR + self.thumb


        def fromTuple(self, read_tuple):
            """
            Loads data from the given tuple.

            IN:
                read_tuple - tuple of the following format:
                    [0]: unlocked property
                    [1]: visible_when_locked
            """
            self.unlocked, self.visible_when_locked = read_tuple


        def toTuple(self):
            """
            RETURNS: tuple version of this data:
                [0]: unlocked property
                [1]: visible_when_locked
            """
            return (self.unlocked, self.visible_when_locked)


    class MASSelectableAccessory(MASSelectableSprite):
        """
        Wrapper around MASAccessory sprite objects.

        PROPERTIES:
            remover - True if this item is a remover, aka a blank ACS,
                False if not


        SEE MASSelectableSprite for inherieted properties
        """

        def __init__(self,
                _sprite_object,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None,
                remover=False
            ):
            """
            MASSelectableAccessory

            IN:
                _sprite_object - MASAccessory object to build this selectable
                    sprite object with.
                display_name - name to show on the selectable screen
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - list of text to display when hovering over the
                    object
                    (Default: None)
                first_select_dlg - text to display the first time you select
                    this sprite
                    (Default: None)
                select_dlg - list of text to display everytime you select this
                    sprite
                    (after the first time)
                    (Default: None)
                remove - True if this ACS is a blank ACS (remover), False if
                    not
                    (Default: False)
            """
            if type(_sprite_object) != MASAccessory:
                raise Exception("not an acs: {0}".format(group))
            if remover and store.mas_selspr._has_remover(group):
                raise Exception(
                    "cannot have more than 1 remover per group: '{0}'".format(
                        group
                    )
                )

            super(MASSelectableAccessory, self).__init__(
                _sprite_object,
                display_name,
                "acs-" + thumb,
                group,
                visible_when_locked,
                hover_dlg,
                first_select_dlg,
                select_dlg
            )

            self.remover = remover


        def get_sprobj(self):
            """
            Gets the sprite object associated with this selectable.

            RETURNS: the sprite object for this selectbale, or None if not
                found
            """
            return store.mas_sprites.ACS_MAP.get(self.name, None)


    class MASSelectableHair(MASSelectableSprite):
        """
        Wrappare around MASHair sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """


        def __init__(self,
                _sprite_object,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableHair constructor

            IN:
                _sprite_object - MASHair object to build this selectable
                    sprite object with.
                display_name - name to show on the selectable screen
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - list of text to display when hovering over the
                    object
                    (Default: None)
                first_select_dlg - text to display the first time you select
                    this sprite
                    (Default: None)
                select_dlg - list of text to display everytime you select this
                    sprite
                    (after the first time)
                    (Default: None)
            """
            if type(_sprite_object) != MASHair:
                raise Exception("not a hair: {0}".format(group))

            super(MASSelectableHair, self).__init__(
                _sprite_object,
                display_name,
                "hair-" + thumb,
                group,
                visible_when_locked,
                hover_dlg,
                first_select_dlg,
                select_dlg
            )


        def get_sprobj(self):
            """
            Gets the sprite object associated with this selectable.

            RETURNS: the sprite object for this selectbale, or None if not
                found
            """
            return store.mas_sprites.HAIR_MAP.get(self.name, None)


    class MASSelectableClothes(MASSelectableSprite):
        """
        Wrappare around MASClothes sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """


        def __init__(self,
                _sprite_object,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableClothes constructor

            IN:
                _sprite_object - MASClothes object to build this selectable
                    sprite object with.
                display_name - name to show on the selectable screen
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - list of text to display when hovering over the
                    object
                    (Default: None)
                first_select_dlg - text to display the first time you select
                    this sprite
                    (Default: None)
                select_dlg - list of text to display everytime you select this
                    sprite
                    (after the first time)
                    (Default: None)
            """
            if type(_sprite_object) != MASClothes:
                raise Exception("not a clothes: {0}".format(group))

            super(MASSelectableClothes, self).__init__(
                _sprite_object,
                display_name,
                "clothes-" + thumb,
                group,
                visible_when_locked,
                hover_dlg,
                first_select_dlg,
                select_dlg
            )


        def get_sprobj(self):
            """
            Gets the sprite object associated with this selectable.

            RETURNS: the sprite object for this selectbale, or None if not
                found
            """
            return store.mas_sprites.CLOTH_MAP.get(self.name, None)


init -10 python in mas_selspr:
    import datetime
    import store

    # mailbox constants
    MB_DISP = "disp_text"
    MB_DISP_DEF = "def_disp_text"
    MB_CONF = "conf_enable"
    MB_DISP_FAST = "disp_fast"

    ## screen constants
    SB_VIEWPORT_BOUNDS = (1075, 5, 200, 625, 5)
    # keep this in sync with teh screen area

    ## string constants
    DEF_DISP = "..."

    ## selection types
    SELECT_ACS = store.mas_sprites_json.SP_ACS
    SELECT_HAIR = store.mas_sprites_json.SP_HAIR
    SELECT_CLOTH = store.mas_sprites_json.SP_CLOTHES

    SELECT_CONSTS = (
        SELECT_ACS,
        SELECT_HAIR,
        SELECT_CLOTH
    )

    # create the selectable lists
    # we also create a dict mapping similar to sprites.
    # maps
    ACS_SEL_MAP = {}
    HAIR_SEL_MAP = {}
    CLOTH_SEL_MAP = {}

    # lists, these should be sorted so do insertSort
    ACS_SEL_SL = []
    HAIR_SEL_SL = []
    CLOTH_SEL_SL = []

    # selector group - topic map
    # key: group
    # value: tuple of following format:
    #   [0] - topic label
    #   [2] - number of items before unlocking
    GRP_TOPIC_MAP = {
        "ribbon": ("monika_ribbon_select", 1),
        "left-hair-clip": ("monika_hairclip_select", 1),
        "left-hair-flower": ("monika_hairflower_select", 1),
    }


    def selectable_key(selectable):
        """
        Returns the display name of a selectable. meant for sorting.

        IN:
            selectable - the selectbale to get key for

        RETURNS the display name of the selectable
        """
        return selectable.display_name


    def _validate_group_topics():
        """
        Locks selector topics if there are no unlocked selectables with the
        appropriate group.
        Unlocks selector topics if they are unlocked selectables.
        """
        #ACS
        for group in GRP_TOPIC_MAP:
            topic_label, min_items = GRP_TOPIC_MAP[group]
            if len(filter_acs(True, group=group)) >= min_items:
                store.mas_unlockEVL(topic_label, "EVE")

            else:
                store.mas_lockEVL(topic_label, "EVE")


    def _has_remover(group):
        """
        Checks if acs of the given group have a remover

        IN:
            group - group to check

        RETURNS: True if this group already has a remover, False otherwise
        """
        acs_list = filter_acs(False, group=group)
        for acs in acs_list:
            if acs.remover:
                return True

        return False


    def _unlock_removers():
        """
        Unlocks remover ACS selectables
        """
        for acs in ACS_SEL_SL:
            if acs.remover:
                acs.unlocked = True


    def _rm_remover(item_list):
        """
        Gets the remover from a given list of items, takes it out of the list
        and reutrns it.

        IN:
            item_list - list of ACS

        RETURNS:
            remover selectable, or None if not found
        """
        for index in range(len(item_list)-1, -1, -1):
            if item_list[index].remover:
                return item_list.pop(index)

        return None


    def create_selectable_remover(acs_type, group):
        """
        Creates a selectable remover for acs

        IN:
            acs_type - acs type of the acs/remover to make
            group - group of selectables this ACS remover should be linked to

        RETURNS: remover ACS selectable
        """
        remover_acs = store.mas_sprites.create_remover(acs_type, group)
        init_selectable_acs(
            remover_acs,
            "Remove",
            "remove",
            group,
            remover=True
        )
        return ACS_SEL_MAP[remover_acs.name]


    def rm_selectable_remover(remover_sel):
        """
        Removes a selectable remover for acs.
        NOTE: also removes the ACS associated with this selectable.
        NOTE: only does this for remover type seelctables

        IN:
            remover_sel - remover selectable to remove
        """
        if not remover_sel.remover:
            return

        # otherwise is remover

        # remove the acs
        store.mas_sprites.rm_acs(remover_sel.get_sprobj())

        # and now the selectable
        for index in range(len(ACS_SEL_SL)-1, -1, -1):
            if ACS_SEL_SL[index].name == remover_sel.name:
                ACS_SEL_SL.pop(index)

        if remover_sel.name in ACS_SEL_MAP:
            ACS_SEL_MAP.pop(remover_sel.name)


    ## init functions for the sprites to use
    def init_selectable_acs(
            acs,
            display_name,
            thumb,
            group,
            visible_when_locked=True,
            hover_dlg=None,
            first_select_dlg=None,
            select_dlg=None,
            remover=False
        ):
        """
        Inits the selectable acs

        IN:
            acs - the acs to create a selectable from
            display_name - display name to use
            thumb - thumbnail image
            group - grouping id
            visible_when_locked - True if this should be visible even if locked
                (Default: True)
            hover_dlg - list of dialogue to say when the item is hovered over
                (Default: None)
            first_select_dlg - list of dialogue to say when the item is
                selected for the first time
                (Default: None)
            select_dlg - list of dialogue to say when the item is selected
                after the first time
                (Default: None)
            remover - True if this ACS is a blank one, False otherwise
                (Default: False)
        """
        # no duplicates
        if acs.name in ACS_SEL_MAP:
            raise Exception("ACS already is selectable: {0}".format(acs.name))

        new_sel_acs = store.MASSelectableAccessory(
            acs,
            display_name,
            thumb,
            group,
            visible_when_locked,
            hover_dlg,
            first_select_dlg,
            select_dlg,
            remover
        )
        ACS_SEL_MAP[acs.name] = new_sel_acs
        store.mas_insertSort(ACS_SEL_SL, new_sel_acs, selectable_key)


    def init_selectable_clothes(
            clothes,
            display_name,
            thumb,
            group,
            visible_when_locked=True,
            hover_dlg=None,
            first_select_dlg=None,
            select_dlg=None
        ):
        """
        Inits the selectable clothes

        IN:
            clothes - the clothes to create selectable from
            display_name - display name to use
            thumb - thumbnail image
            group - grouping id
            visible_when_locked - True if this should be visible even if locked
                (Default: True)
            hover_dlg - list of dialogue to say when the item is hovered over
                (Default: None)
            first_select_dlg - list of dialogue to say when the item is
                selected for the first time
                (Default: None)
            select_dlg - list of dialogue to say when the item is selected
                after the first time
                (Default: None)
        """
        # no duplicates
        if clothes.name in CLOTH_SEL_MAP:
            raise Exception(
                "Clothes already is selectable: {0}".format(clothes.name)
            )

        new_sel_clothes = store.MASSelectableClothes(
            clothes,
            display_name,
            thumb,
            group,
            visible_when_locked,
            hover_dlg,
            first_select_dlg,
            select_dlg
        )
        CLOTH_SEL_MAP[clothes.name] = new_sel_clothes
        store.mas_insertSort(CLOTH_SEL_SL, new_sel_clothes, selectable_key)


    def init_selectable_hair(
            hair,
            display_name,
            thumb,
            group,
            visible_when_locked=True,
            hover_dlg=None,
            first_select_dlg=None,
            select_dlg=None
        ):
        """
        Inits the selectable hair

        IN:
            hair - the hair to create a selectable from
            display_name - display name to use
            thumb - thumbnail image
            group - grouping id
            visible_when_locked - True if this should be visible even if locked
                (Default: True)
            hover_dlg - list of dialogue to say when the item is hovered over
                (Default: None)
            first_select_dlg - list of dialogue to say when the item is
                selected for the first time
                (Default: None)
            select_dlg - list of dialogue to say when the item is selected
                after the first time
                (Default: None)
        """
        # no duplicates
        if hair.name in HAIR_SEL_MAP:
            raise Exception("Hair already is selectable: {0}".format(hair.name))

        new_sel_hair = store.MASSelectableHair(
            hair,
            display_name,
            thumb,
            group,
            visible_when_locked,
            hover_dlg,
            first_select_dlg,
            select_dlg
        )
        HAIR_SEL_MAP[hair.name] = new_sel_hair
        store.mas_insertSort(HAIR_SEL_SL, new_sel_hair, selectable_key)


    ## adjust an aspect of monika.
    # NOTE: meant soley in use of preview and deselections.
    def _adjust_monika(
            moni_chr,
            old_map,
            new_map,
            select_type,
            use_old=False
        ):
        """
        Adjusts an aspect of monika based on the select type

        NOTE: this also logs exceptions if they occur. Also will undo
            a chnage that causes crash.

        IN:
            moni_chr - MASMonika object to adjust
            old_map - the old select map (what was previously selected)
            new_map - the new select map (what is currently selected)
            select_type - the select type, which determins what parts of
                monika to adjust
            use_old - True means we are reverting back to the old map,
                False meanse use the old map
                (Default: False)
        """
        if select_type == SELECT_ACS:
            old_map_view = old_map.viewkeys()
            new_map_view = new_map.viewkeys()

            # determine which map is the "old" and which is "new"
            # we want to remove what is excess from the desired map
            if use_old:
                remove_keys = new_map_view - old_map_view
                remove_map = new_map
                add_map = old_map

            else:
                remove_keys = old_map_view - new_map_view
                remove_map = old_map
                add_map = new_map

            # remove what is excess
            for item_name in remove_keys:
                moni_chr.remove_acs(
                    remove_map[item_name].selectable.get_sprobj()
                )

            # then readd everything that was previous
            for item in add_map.itervalues():
                moni_chr.wear_acs(item.selectable.get_sprobj())

        elif select_type == SELECT_HAIR:

            # determine which map to change to
            if use_old:
                select_map = old_map

            else:
                select_map = new_map

            # change to that map
            for item in select_map.itervalues():
                if use_old or item.selected:
                    prev_hair = moni_chr.hair
                    new_hair = item.selectable.get_sprobj()

                    if prev_hair == new_hair:
                        # hair is the same? no point in changing
                        return

                    try:
                        moni_chr.change_hair(new_hair)

                    except Exception as e:
                        mas_utils.writelog("BAD HAIR: " + repr(e))
                        moni_chr.change_hair(prev_hair)

                    return # always quit early since you can only have 1 hair

        elif select_type == SELECT_CLOTH:

            # determine which map to change to
            if use_old:
                select_map = old_map

            else:
                select_map = new_map

            # change to that map
            for item in select_map.itervalues():
                if use_old or item.selected:
                    prev_cloth = moni_chr.clothes
                    new_cloth = item.selectable.get_sprobj()

                    if prev_cloth == new_cloth:
                        # we are changing to the what we are wearing? no point
                        return

                    try:
                        moni_chr.change_clothes(new_cloth)

                    except Exception as e:
                        mas_utils.writelog("BAD CLOTHES: " + repr(e))
                        moni_chr.change_clothes(prev_cloth)

                    return # quit early since you can only have 1 clothes

        # else, we do not do anything.


    def _fill_select_map(moni_chr, select_type, items, select_map):
        """
        Fills the select map with what monika is currently wearing, based on
        the given select type

        IN:
            moni_chr - MASMonika object to read from
            select_type - the select type, which determins what part of monika
                to read
            items - list of displayables we should check if monika is wearing

        OUT:
            select_map - select map filled with appropriate selectbales.

        RETURNS: true if Monika was found wearing something in the list,
            False if not.
        """
        found_item = False
        if select_type == SELECT_ACS:
            for item in items:
                if moni_chr.is_wearing_acs(item.selectable.get_sprobj()):
                    select_map[item.selectable.name] = item
                    item.selected = True
                    found_item = True

                    # NOTE: cannot quit early because multiple accessories

        elif select_type == SELECT_HAIR:
            for item in items:
                if item.selectable.name == moni_chr.hair.name:
                    select_map[moni_chr.hair.name] = item
                    item.selected = True
                    # we can quit early since you can only have 1 hair
                    return True

        elif select_type == SELECT_CLOTH:
            for item in items:
                if item.selectable.name == moni_chr.clothes.name:
                    select_map[moni_chr.clothes.name] = item
                    item.selected = True
                    # we can quit early since you only have 1 clothes
                    return True

        # else we do not do anything
        return found_item


    def _clean_select_map(select_map, select_type, remove_items, moni_chr):
        """
        Cleans the select map of non-selected items.

        IN:
            select_map - select map to clean
            select_type - select type, only used if remove_items is True
            remove_items - True means we also remove items from monika chr
            moni_chr - MASMonika object to modify.

        OUT:
            select_map - select map cleaned of non-selectd items
        """
        for item_name in select_map.keys():
            if not select_map[item_name].selected:
                item = select_map.pop(item_name)

                if remove_items and (select_type == SELECT_ACS):
                    moni_chr.remove_acs(item.selectable.get_sprobj())


    ## selection group check
    def valid_select_type(sel_con):
        """
        Returns True if valid selection constant, False otherwise

        IN:
            sel_con - selection constnat to check

        RETURNS: True if vali dselection constant
        """
        sel_types = (SELECT_ACS, SELECT_HAIR, SELECT_CLOTH)
        return sel_con in sel_types


    ## acs/hair/clothes selection helper functions
    def is_same(old_map_view, new_map_view):
        """
        Compares the given select map views for differences.

        NOTE: we only check key existence. Use this after you clean the
        map.

        IN:
            old_map_view - viewkeys view of the old map
            new_map_view - viewkeys view of the new map

        RETURNS:
            True if the maps are the same, false if different.
        """
        old_len = len(old_map_view)

        # lengths dont match? clearly these views do not match then.
        if old_len != len(new_map_view):
            return False

        # otherwise, now we get intersection and verify length
        return old_len == len(old_map_view & new_map_view)


    def _save_selectable(source, dest):
        """
        Saves selectable data from the given source into the destination.

        IN:
            source - source data to read
            dest - data place to save
        """
        for item_name, item in source.iteritems():
            dest[item_name] = item.toTuple()


    def save_selectables():
        """
        Goes through the selectables and saves their unlocked property.

        NOTE: we do this by adding the name into the appropriate persistent.
        also the data we want to save
        """
        _save_selectable(ACS_SEL_MAP, store.persistent._mas_selspr_acs_db)
        _save_selectable(HAIR_SEL_MAP, store.persistent._mas_selspr_hair_db)
        _save_selectable(
            CLOTH_SEL_MAP,
            store.persistent._mas_selspr_clothes_db
        )


    def _load_selectable(source, dest):
        """
        Loads selectable data from the given source into the destination.

        IN:
            source - source data to load from
            dest - data to save the loaded data into
        """
        for item_name, item_tuple in source.iteritems():
            if item_name in dest:
                dest[item_name].fromTuple(item_tuple)


    def load_selectables():
        """
        Loads the persistent data into selectables.
        """
        _load_selectable(store.persistent._mas_selspr_acs_db, ACS_SEL_MAP)
        _load_selectable(store.persistent._mas_selspr_hair_db, HAIR_SEL_MAP)
        _load_selectable(
            store.persistent._mas_selspr_clothes_db,
            CLOTH_SEL_MAP
        )


    def _filter_sel_single(item, unlocked, group):
        """
        Checks if the given item matches the given criteria

        IN:
            item - selectable to check
            unlocked - True means item matches if its unlocked
            group - if not None, then item matches if the group matches

        RETURNS:
            True if the item matches the criteria, False otherwise
        """
        if unlocked and not item.unlocked:
            return False

        if group is not None and item.group != group:
            return False

        return True


    def _filter_sel(select_list, unlocked, group=None):
        """
        Filters the selectable list based on criteria

        IN:
            select_list - list of Selectables to filter
            unlocked - True means we only match unlocked selectables
            group - non-None means we match selectables that match this
                group. If None, we dont check group at all.
                (Default: None)

        RETURNS: list of selectables that match criteria
        """
        return [
            item
            for item in select_list
            if _filter_sel_single(item, unlocked, group)
        ]


    def filter_acs(unlocked, group=None):
        """
        Filters the selectable acs based on criteria

        IN:
            unlocked - True means we only match unlocked selectables
            group - non-None means we match selectables that match this group
                if None, we don't check group at all.
                (Default: None)

        RETURNS: list of selectable acs that match criteria
        """
        return _filter_sel(ACS_SEL_SL, unlocked, group)


    def filter_clothes(unlocked, group=None):
        """
        Filters the selectable clothes based on critera

        IN:
            unlocked - True means we only match unlocked selectables
            group - non-None means we match selectables that match this group
                if None, we don't check group at all
                (Default: None)

        RETURNS: list of selectable clothes that match criteria
        """
        return _filter_sel(CLOTH_SEL_SL, unlocked, group)


    def filter_hair(unlocked, group=None):
        """
        Filters the selectable hair based on critera

        IN:
            unlocked - True means we only match unlocked selectables
            group - non-None means we match selectables that match this group
                if None, we don't check group at all
                (Default: None)

        RETURNS: list of selectable hair that match criteria
        """
        return _filter_sel(HAIR_SEL_SL, unlocked, group)


    def _get_sel(item, select_type):
        """
        Retreives the selectable for the given item.

        IN:
            item - item to find Selectable for
            select_type - the type of selectable we are trying to find

        RETURNS the selectable for the item, or None if not found
        """
        if select_type == SELECT_ACS:
            return get_sel_acs(item)

        elif select_type == SELECT_HAIR:
            return get_sel_hair(item)

        elif select_type == SELECT_CLOTH:
            return get_sel_clothes(item)

        return None


    def get_sel(item):
        """
        Retrieves the selectable for the given item
        This uses sprite object type from jsons.

        IN:
            item - sprite objct to find the Selectable for

        RETURNS: selectable for the given item
        """
        if item.gettype() == store.mas_sprites_json.SP_ACS:
            return get_sel_acs(item)

        elif item.gettype() == store.mas_sprites_json.SP_HAIR:
            return get_sel_hair(item)

        elif item.gettype() == store.mas_sprites_json.SP_CLOTHES:
            return get_sel_clothes(item)

        return None


    def get_sel_acs(acs):
        """
        Retrieves the selectable for the given accessory.

        IN:
            acs - MASAccessory object to find selectable for

        RETURNS the selectable for this acs, or None if not found.
        """
        return ACS_SEL_MAP.get(acs.name, None)


    def get_sel_clothes(clothes):
        """
        Retrieves the selectable for the given clothes

        IN:
            clothes - MASClothes object to find selectable for

        RETURNS the selectable for these clothes, or None if not found
        """
        return CLOTH_SEL_MAP.get(clothes.name, None)


    def get_sel_hair(hair):
        """
        Retrieves the selectable for the given hair

        IN:
            hair - MASHair object to find selectbale for

        RETURNS the selectable for this hair, or none if not found
        """
        return HAIR_SEL_MAP.get(hair.name, None)


    def _lock_item(item, select_type):
        """
        Locks the given item's selectable.

        IN:
            item - item to find selectable for
            select_type - the type of selectable we are trying to find
        """
        sel_item = _get_sel(item, select_type)
        if sel_item:
            sel_item.unlocked = False


    def lock_acs(acs):
        """
        Locks the given accessory's selectable

        IN:
            acs - MASAccessory object to lock
        """
        _lock_item(acs, SELECT_ACS)


    def lock_clothes(clothes):
        """
        Locks the given clothes' selectable

        IN:
            clothes - MASClothes object to lock
        """
        _lock_item(clothes, SELECT_CLOTH)


    def lock_hair(hair):
        """
        locks the given hair's selectable

        IN:
            hair - MASHair object to lock
        """
        _lock_item(hair, SELECT_HAIR)


    def _unlock_item(item, select_type):
        """
        Unlocks the given item's selectable

        IN:
            item - item to find selectable for
            select_type - the type of selectable we are trying to find
        """
        sel_item = _get_sel(item, select_type)
        if sel_item:
            sel_item.unlocked = True


    def unlock_acs(acs):
        """
        Unlocks the given accessory's selectable

        IN:
            acs - MASAccessory object to unlock
        """
        _unlock_item(acs, SELECT_ACS)


    def unlock_clothes(clothes, add_to_holiday_map=False):
        """
        Unlocks the given clothes' selectable

        IN:
            clothes - MASClothes object to unlock
            add_to_holiday_map - add to the holiday map if we want this for happy+ for the day
        """
        _unlock_item(clothes, SELECT_CLOTH)

        if add_to_holiday_map:
            store.persistent._mas_event_clothes_map[datetime.date.today()] = clothes.name


    def unlock_hair(hair):
        """
        Unlocks the given hair's selectable

        IN:
            hair - MASHair object to unlock
        """
        _unlock_item(hair, SELECT_HAIR)


    def unlock_selector(group):
        """RUNTIME ONLY
        Unlocks the selector of the given group.

        IN:
            group - group to unlock selector topic.
        """
        selector_label = GRP_TOPIC_MAP.get(group, None)
        if selector_label is None:
            return

        store.mas_unlockEVL(selector_label[0], "EVE")


    def json_sprite_unlock(sp_obj, unlock_label=True):
        """RUNTIME ONLY
        Unlocks selectable for the given sprite, as ewll as the selector
        topic for that sprite.

        IN:
            sp_obj - sprite object to unlock selectbale+
            unlock_label - True will unlock the selector lable, False will not
                (Default: True)
        """
        sp_type = sp_obj.gettype()

        # unlocks the selectable
        _unlock_item(sp_obj, sp_type)

        # retrieve selectable and unlock the group's selector
        if unlock_label:
            sel_obj = _get_sel(sp_obj, sp_type)
            unlock_selector(sel_obj.group)


    # extension of mailbox
    class MASSelectableSpriteMailbox(store.MASMailbox):
        """
        SelectableSprite extension of the mailbox

        PROPERTIES:
            (no additional)

        See MASMailbox for properties.
        """

        def __init__(self, def_disp_text=DEF_DISP):
            """
            Constructor for the selectable sprite mailbox
            """
            super(MASSelectableSpriteMailbox, self).__init__()
            self.send_def_disp_text(def_disp_text)
            self.send_conf_enable(False)


        def _get(self, headline):
            """
            Class the super class's get

            This is just for ease of use
            """
            return super(MASSelectableSpriteMailbox, self).get(headline)


        def _read(self, headline):
            """
            Calls the super class read

            THis is just for ease of us
            """
            return super(MASSelectableSpriteMailbox, self).read(headline)


        def _send(self, headline, msg):
            """
            Calls the super classs's send

            This is just for ease of use.
            """
            super(MASSelectableSpriteMailbox, self).send(headline, msg)


        def read_conf_enable(self):
            """
            Returns the value of the conf enable message

            RETURNS:
                True if the confirmation button should be enabled, False
                otherwise
            """
            return self._read(MB_CONF)


        def read_def_disp_text(self):
            """
            Returns the default display text message

            NOTE: does NOT remove.

            RETURNS: display text, default
            """
            return self._read(MB_DISP_DEF)


        def get_disp_fast(self):
            """
            Removes and returns the fast flag

            RETURNS: True if we want to append fast, False/None if not
            """
            return self._get(MB_DISP_FAST)


        def get_disp_text(self):
            """
            Removes and returns the display text message

            RETURNS: display text
            """
            return self._get(MB_DISP)


        def send_conf_enable(self, enable):
            """
            Sends enable message

            IN:
                enable - True means to enable, False means to disable
            """
            self._send(MB_CONF, enable)


        def send_def_disp_text(self, txt):
            """
            Sends default display message

            IN:
                txt - txt to display
            """
            self._send(MB_DISP_DEF, txt)


        def send_disp_fast(self):
            """
            Sends default fast flag
            """
            self._send(MB_DISP_FAST, True)


        def send_disp_text(self, txt):
            """
            Sends display text message

            IN:
                txt - txt to display
            """
            self._send(MB_DISP, txt)


init -1 python:
    import random

    # better more user-friendly sel functions
    def mas_SELisUnlocked(_sprite_item):
        """
        Checks if the given sprite item is unlocked

        IN:
            _sprite_item - sprite object to check

        RETURNS: True if the given sprite item is unlocked, false otherwise
        """
        _sel_item = store.mas_selspr._get_sel(
            _sprite_item,
            _sprite_item.gettype()
        )
        if _sel_item is not None:
            return _sel_item.unlocked

        return False


    def mas_filterUnlockGroup(sp_type, group, unlock_min=None):
        """
        Unlock selector topic for the given group if appropriate number of
        selector objects are unlocked.

        IN:
            sp_type - sprite type to filter on
            group - group to use for filtering selectors
            unlock_min - minimum number that has to be unlocked for us to
                unock the selector topic.
                IF None, then we use the amount provided by the GRP_TOPIC_MAP
                (Default: None)
        """
        # type sanity check
        if sp_type not in store.mas_selspr.SELECT_CONSTS:
            return

        # check if we even have a label to unlock
        grp_topic = store.mas_selspr.GRP_TOPIC_MAP.get(group, None)
        if grp_topic is None:
            return

        if unlock_min is None:
            unlock_min = grp_topic[1]

        grp_topic = grp_topic[0]

        if sp_type == store.mas_selspr.SELECT_ACS:
            sel_list = store.mas_selspr.filter_acs(True, group=group)

        elif sp_type == store.mas_selspr.SELECT_HAIR:
            sel_list = store.mas_selspr.filter_hair(True, group=group)

        else:
            sel_list = store.mas_selspr.filter_clothes(True, group=group)

        if len(sel_list) >= unlock_min:
            mas_unlockEVL(grp_topic, "EVE")


    ## custom displayable
    class MASSelectableImageButtonDisplayable(renpy.Displayable):
        """
        Custom button for the selectable items.
        """
        import pygame
        from store.mas_selspr import MB_DISP

        # constnats
        THUMB_DIR = "mod_assets/thumbs/"

        WIDTH = 180 # default width
        TX_WIDTH = 170 # width of the text object

        # technically this should change.
        TOTAL_HEIGHT = 218
        SELECTOR_HEIGHT = 180

        # this is the default, but the real may change using the expanding
        # frame properties.
        TOP_FRAME_HEIGHT = 38 # default
        TOP_FRAME_TEXT_HEIGHT = 35 # part of the top frame where text should be
        TOP_FRAME_CHUNK = 35 # each text chunk should consist of 35px
        TOP_FRAME_SPACER = 5 # pixels between each text chunk line

        # mouse stuff
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP
        )
        MOUSE_WHEEL = (4, 5)


        def __init__(self,
                _selectable,
                select_map,
                viewport_bounds,
                mailbox={},
                multi_select=False
            ):
            """
            Constructor for this displayable

            IN:
                selectable - the selectable object we want to encapsulate
                select_map - dict containing group keys of previously selected
                    objects.
                viewport_bounds - tuple of the following format:
                    [0]: xpos of the viewport upper left
                    [1]: ypos of the viewport upper left
                    [2]: width of the viewport
                    [3]: height of the viewport
                    [4]: border size
                mailbox - dict to send messages to outside from this
                    displayable.
                    (Default: {})
                multi_select - True means we can select more than one item.
                    False otherwise
                    (Default: False)
            """
            super(MASSelectableImageButtonDisplayable, self).__init__()

            self.selectable = _selectable
            self.select_map = select_map
            self.mailbox = mailbox
            self.multi_select = multi_select
            self.been_selected = False

            # if this is a remover, we don't use the thumb
            if self.selectable.remover:
                thumb_path = self.THUMB_DIR + "remove.png"

            else:
                # as a precaution, if a thumb doesn't exist, we use a
                # placeholder.
                thumb_path = self.THUMB_DIR + _selectable.thumb
                if not renpy.loadable(thumb_path):
                    thumb_path = self.THUMB_DIR + "unknown.png"

            self.thumb = Image(thumb_path)

            # image setups
            self.thumb_overlay = Image(
                mas_getTimeFile("mod_assets/frames/selector_overlay.png")
            )
            self.thumb_overlay_locked = Image(
                mas_getTimeFile("mod_assets/frames/selector_overlay_disabled.png")
            )
            self.top_frame = Frame(
                mas_getTimeFile("mod_assets/frames/selector_top_frame.png"),
                left=4,
                top=4,
                tile=True
            )
            self.top_frame_selected = Frame(
                mas_getTimeFile("mod_assets/frames/selector_top_frame_selected.png"),
                left=4,
                top=4,
                tile=True
            )
            self.top_frame_locked = Frame(
                mas_getTimeFile("mod_assets/frames/selector_top_frame_disabled.png"),
                left=4,
                top=4,
                tile=True
            )

            # renpy solids and stuff
            self.hover_overlay = Solid("#ffaa99aa")

            # text objects
            # NOTE: we build these on first render
            self.item_name = None
            self.item_name_hover = None
#            self.item_name = self._display_name(False, self.selectable.display_name)
#            self.item_name_hover = self._display_name(True, self.selectable.display_name)

            # setup viewport bound values
            vpx, vpy, vpw, vph, vpb = viewport_bounds
            self.xlim_lo = vpx + vpb
            self.xlim_up = (vpx + vpw) - vpb
            self.ylim_lo = vpy + vpb
            self.ylim_up = (vpy + vph) - vpb

            # flags
            self.hovered = False
            self.hover_jumped = False # True means we just jumped to label

            # these get changed
            self.hover_width = self.WIDTH
            self.hover_height = self.TOTAL_HEIGHT

            self.selected = False
            self.select_jump = False

            self.first_render = True

            # when True, we make a call to end the interaction after reaching
            # the end of event.
            self.end_interaction = False

            # top frame sizes
            self.top_frame_height = self.TOP_FRAME_HEIGHT

            # cached renders
            self.render_cache = {}

            # locked mode
            self.locked = not self.selectable.unlocked
            self.locked_thumb = Image("mod_assets/thumbs/locked.png")


        def _blit_bottom_frame(self, r, _renders):
            """
            bliting the bottom frames

            IN:
                r - render to blit to
                _renders - list of bottom renders to blit
            """
            for _render in _renders:
                r.blit(_render, (0, self.top_frame_height))


        def _blit_top_frame(self, r, _renders, _disp_name):
            """
            bliting the top frames

            IN:
                r - render to blit to
                _renders - list of top renders to blit
                _disp_name - list of display name renders to blit
            """
            for _render in _renders:
                r.blit(_render, (0, 0))

            # text
            line_index = 1
            for line in _disp_name:
                r.blit(
                    line,
                    (
                        5,
                        (line_index * self.TOP_FRAME_CHUNK)
                        - line.get_size()[1]
                    )
                )
                line_index += 1


        def _check_display_name(self, _display_name_text, st, at):
            """
            Checks the given display name to see if it fits within the frame
            bounds. We will have to adjust if not

            IN:
                _display_name_text - display name as text

            RETURNS:
                the rendered display name rendre if it fits, None if not.
            """
            # render the text object we want to test
            _disp_text = self._display_name(False, _display_name_text)
            _render = renpy.render(
                _disp_text,
                1000,
                self.TOP_FRAME_CHUNK,
                st,
                at
            )
            dtw, dth = _render.get_size()

            # check width
            if dtw > self.TX_WIDTH:
                return None

            return _render


        def _check_render_split(self, line, lines_list, st, at):
            """
            Checks the given line to see if it fits within a line render.

            NOTE: adds hypen and multiple lines if the line is too long

            IN:
                line - the line we want to check for render
                lines_list - list to add lines to
                st - st for renpy render
                at - at for renpy render

            OUT:
                lines_list - list with lines added
            """
            _render = self._check_display_name(line, st, at)
            if not _render:
                self._hypen_render_split(line, lines_list, st, at)

            else:
                self.item_name.append(_render)
                lines_list.append(line)


        def _display_name(self, selected, _text):
            """
            Returns the text object for the display name.

            IN:
                selected - True if selected, False if not
                _text - actual text to convert into display name obj

            RETURNS:
                the text object for the display name
            """
            if selected:
                color = mas_ui.light_button_text_hover_color
            else:
                color = mas_ui.light_button_text_idle_color

            return Text(
                _text,
                font=gui.default_font,
                size=gui.text_size,
                color=color,
                outlines=[]
            )


        def _hover(self):
            """
            Does hover actions, which include playing hover sound and sending
            hover msg if appropriate
            """
            if not self.hovered:
                self.hover_jumped = False

            elif not self.hover_jumped:
                # first time hovering
                self.hover_jumped = True

                # play hover sound
                renpy.play(gui.hover_sound, channel="sound")

                # send out hover dlg
                if self.selectable.hover_dlg is not None:
                    self._send_hover_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

                # always reset on a hover
                self.end_interaction = True


        def _hypen_render_split(self, line, lines_list, st, at, tokens=None):
            """
            Splits a line via hypen.

            We do a reverse through the string to find appropriate render
            sizes.

            NOTE: we add renders to self.item_name

            IN:
                line - line to split
                lines_list - list to add lines to
                st - st for renpy render
                at - at for renpy render
                tokens - current list of tokens, if we are in the token mode.
                    Insert the leftover token word at position 1.
                    (Default: None)

            OUT:
                lines_list - list with lines added
            """
            # NOTE: we do reverse because it is more likely that text is
            #   just barely too large, than dealing with one huge string.
            index = len(line)-2
            while index >= 0:
                # split and add hypen
                line1 = line[:index] + "-"

                # check the render
                _l1_render = self._check_display_name(line1, st, at)
                if _l1_render:
                    # add line 1
                    self.item_name.append(_l1_render)
                    lines_list.append(line1)

                    # recurse 2nd line
                    line2 = line[index:]
                    if tokens is not None:
                        tokens.insert(1, line2)
                    else:
                        self._check_render_split(line2, lines_list, st, at)
                    return

                # doesnt fit, decreaes index and continue
                index -= 1


        def _is_over_me(self, x, y):
            """
            Returns True if the given x, y is over us.
            This also handles if the mouse is past the viewport bounds.

            IN:
                x - x coord relative to upper left of this displayable
                y - y coord relative to upper left of this displayable
            """
            mouse_x, mouse_y = renpy.get_mouse_pos()
            return (
                self.xlim_lo <= mouse_x <= self.xlim_up
                and self.ylim_lo <= mouse_y <= self.ylim_up
                and 0 <= x <= self.hover_width
                and 0 <= y <= self.hover_height
            )


        def _rand_select_dlg(self, dlg_list):
            """
            Randomly selects dialogue from the given list

            IN:
                dlg_list - list to select from

            ASSUMES the list is not empty
            """
            return dlg_list[random.randint(0, len(dlg_list)-1)]


        def _render_bottom_frame(self, hover, st, at):
            """
            Renders the bottom frames, returns a list of the renders in order
            of bliting.

            IN:
                hover - True means we are hovering (or are selected), false
                    otherwise

            RETURNS:
                list of renders, in correct blit order
            """
            _renders = [
                self._render_bottom_frame_piece(self.thumb, st, at),
                self._render_bottom_frame_piece(self.thumb_overlay, st, at)
            ]

            if hover:
                _renders.append(
                    self._render_bottom_frame_piece(self.hover_overlay, st, at)
                )

            return _renders


        def _render_bottom_frame_piece(self, piece, st, at):
            """
            Renders a single bottom frame piece and returns it
            """
            return renpy.render(
                piece,
                self.WIDTH,
                self.SELECTOR_HEIGHT,
                st,
                at
            )


        def _render_display_name(self, hover, _text, st, at):
            """
            Renders display name

            IN:
                hover - True if selected, False if not
                _text - actual text to render
                st - st for renpy render
                at - at for renpy render

            """
            return renpy.render(
                self._display_name(hover, _text),
                self.WIDTH,
                self.TOP_FRAME_CHUNK,
                st,
                at
            )


        def _render_top_frame(self, hover, st, at):
            """
            Renders the top renders, returns a list of the renders in order of
            bliting.

            IN:
                hover - True means we are hovering (or are selected

            RETURNS:
                list of renders, in correct blit order
            """
            if hover:
                _main_piece = self._render_top_frame_piece(
                    self.top_frame_selected,
                    st,
                    at
                )

            else:
                _main_piece = self._render_top_frame_piece(
                    self.top_frame,
                    st,
                    at
                )

            return [_main_piece]


        def _render_top_frame_piece(self, piece, st, at):
            """
            Renders a top frame piece. No Text, please
            """
            return renpy.render(
                piece,
                self.WIDTH,
                self.top_frame_height,
                st,
                at
            )


        def _select(self):
            """
            Makes this item a selected item. Also handles other logic realted
            to selecting this.
            """
            # if already selected, then we need to deselect.
            if self.selected:
                # TODO: this actually can break things if we dselect
                #   probably should handle this a smarter way like if
                #   something was selected originally, dont make it possible
                #   to deselect.
                #   or make it select what was originally selected.
                # deselect self
#                self.selected = False
#                renpy.redraw(self, 0)

                # end interaction so display text is rest
#                self.end_interaction = True
                return

            # TODO: should be moved to the top when deselect can happen
            # play the select sound
            renpy.play(gui.activate_sound, channel="sound")

            # otherwise select self
            self.selected = True

            if not self.multi_select:
                # must clean select map
                for item in self.select_map.itervalues():
                    # setting to False will queue for removal of item
                    # NOTE: the caller must handle teh removal
                    item.selected = False
                    renpy.redraw(item, 0)

            # add this item to the select map
            self.select_map[self.selectable.name] = self

            # the appropriate dialogue
            if self.been_selected:
                if self.selectable.select_dlg is not None:
                    self._send_select_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

            else:
                # not been selected before
                self.been_selected = True
                if self.selectable.first_select_dlg is not None:
                    self._send_first_select_text()

                elif self.selectable.select_dlg is not None:
                    self._send_select_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

            # always reset interaction if something has been selected
            self.end_interaction = True


        def _send_first_select_text(self):
            """
            Sends first select text to mailbox

            ASSUMES first select text exists
            """
            self._send_msg_disp_text(
                self._rand_select_dlg(
                    self.selectable.first_select_dlg
                )
            )


        def _send_hover_text(self):
            """
            Sends hover text to mailbox

            ASSUMES hover text exists
            """
            self._send_msg_disp_text(
                self._rand_select_dlg(
                    self.selectable.hover_dlg
                )
            )


        def _send_msg_disp_text(self, msg):
            """
            Sends text message to mailbox.

            IN:
                msg - text message to send
            """
            self.mailbox.send_disp_text(msg)


        def _send_select_text(self):
            """
            Sends the select text to mailbox

            ASSUMES select text exists
            """
            self._send_msg_disp_text(
                self._rand_select_dlg(
                    self.selectable.select_dlg
                )
            )


        def _setup_display_name(self, st, at):
            """
            Sets up item_name and item_name_hover with list of renders, ready
            for bliting.

            IN:
                st - st for renpy render
                at - at for renpy render
            """
            # lets initially check if the pure text renders nicely
            _render = self._check_display_name(
                self.selectable.display_name,
                st,
                at
            )

            if _render:
                self.item_name = [_render]
                self.item_name_hover = [
                    self._render_display_name(
                        True,
                        self.selectable.display_name,
                        st,
                        at
                    )
                ]
                return

            # if we got a None, the text is too long.
            # prepare item_name for renders
            self.item_name = []
            _lines = self._split_render(self.selectable.display_name, st, at)

            # render the hover variants
            # and calculate total height
#            top_height = 0
            self.item_name_hover = [
                self._render_display_name(True, line, st, at)
                for line in _lines
            ]
#            top_height += (_render.get_size()[1] + self.TOP_FRAME_SPACER)

            # now setup the new frame size
            self.top_frame_height = (
                (self.TOP_FRAME_CHUNK * len(self.item_name_hover))
            )


        def _split_render(self, disp_name, st, at):
            """
            Attempts to split the displayname, then checks renders for it
            to see if it fits within the bounds.

            NOTE: this will add renders to self.item_name

            IN:
                disp_name - display name to split
                st - st for renpy render
                at - at for renpy render

            RETURNS:
                list of string lines that fit when rendered.
            """
            _tokens = disp_name.split()
            _lines = []

            self._split_render_tokens(_tokens, _lines, st, at)

            return _lines


        def _split_render_tokens(self, tokens, lines_list, st, at, loop=False):
            """
            Token version of _split_render

            IN:
                tokens - tokens to handle with
                lines_list - list of string lines that we rendered
                st - st for renpy render
                at - at for renpy render
                loop - True if we are recursively calling this.
                    (Default: False)
            """
            # sanity check
            if len(tokens) == 0:
                return

            if len(tokens) > 2 or loop:
                self._token_render_split(tokens, lines_list, st, at)

            elif len(tokens) <= 1:
                self._hypen_render_split(tokens[0], lines_list, st, at)

            else:
                # otherwise, we can just use the 2 splits
                self._check_render_split(tokens[0], lines_list, st, at)
                self._check_render_split(tokens[1], lines_list, st, at)


        def _token_render_split(self, tokens, lines_list, st, at):
            """
            Uses the given tokens to determine best fit render options for
            those tokens.

            NOTE: we also do self.item_name

            IN:
                tokens - list of string tokens to apply best fit
                lines_list - list to add lines to
                st - st for renpy render
                at - at for renpy render

            OUT:
                lines_list - list with lines added
            """
            # reverse order siunce we want to maximize render line size
            index = len(tokens)
            while index > 0:

                # build a string with a number of tokens
                line1 = " ".join(tokens[:index])

                # check the render
                _l1_render = self._check_display_name(line1, st, at)
                if _l1_render:
                    # add line 1
                    self.item_name.append(_l1_render)
                    lines_list.append(line1)

                    # recurse the remaining tokens
                    self._split_render_tokens(
                        tokens[index:],
                        lines_list,
                        st,
                        at,
                        True
                    )
                    return

                # otherwise, lower index
                index -= 1

            # if we got here, then we are dealing with a single token that is
            # too long.
            self._hypen_render_split(tokens[0], lines_list, st, at, tokens)
            self._split_render_tokens(tokens[1:], lines_list, st, at, True)


        def event(self, ev, x, y, st):
            """
            EVENT. We only want to handle 2 cases:
                MOUSEMOTION + hover is over us
                MOUSEDOWN + mouse is over us
            """
            # window event means we need to re-render everything
            if ev.type == pygame.WINDOWEVENT:
                self.first_render = True
                renpy.redraw(self, 0)
                return

            if ev.type in self.MOUSE_EVENTS:

                if ev.type == pygame.MOUSEMOTION:
                    if not self.locked:
                        self.hovered = self._is_over_me(x, y)
                        renpy.redraw(self, 0)

                elif ev.type == pygame.MOUSEBUTTONDOWN:

                    if ev.button in self.MOUSE_WHEEL:
                        # TODO: scrolling in mouse wheel is not perfect,
                        #   the previously hovered item gest hovered instead
                        #   of what we actually want.
                        if not self.locked:
                            self.hovered = self._is_over_me(x, y)
                            renpy.redraw(self, 0)

                    elif ev.button == 1:
                        # left click
                        if not self.locked and self._is_over_me(x, y):
                            self._select()
                            renpy.redraw(self, 0)

#                        elif self.selected and not self.multi_select:
#                            self.selected = False
#                            renpy.redraw(self, 0)

            # apply hover dialogue logic if not selected
            if not self.selected and not self.locked:
                self._hover()

            if self.end_interaction:
                self.end_interaction = False
                renpy.end_interaction(True)


        def render(self, width, height, st, at):
            """
            Render. we want the button here.
            """
            if self.first_render:
                # on first render, we do the rendering.
                # this is so we can just blit later instead of rendering each
                # time.

                # setup the display name
                self._setup_display_name(st, at)

                # now save the render cache
                if self.locked:
                    _locked_bot_renders = [
                        self._render_bottom_frame_piece(
                            self.locked_thumb,
                            st,
                            at
                        ),
                        self._render_bottom_frame_piece(
                            self.thumb_overlay_locked,
                            st,
                            at
                        )
                    ]
                    _locked_top_renders = [
                        self._render_top_frame_piece(
                            self.top_frame_locked,
                            st,
                            at
                        )
                    ]

                    self.render_cache = {
                        "bottom": _locked_bot_renders,
                        "bottom_hover": _locked_bot_renders,
                        "top": _locked_top_renders,
                        "top_hover": _locked_top_renders,
                        "disp_name": self.item_name,
                        "disp_name_hover": self.item_name
                    }

                else:
                    self.render_cache = {
                        "bottom": self._render_bottom_frame(False, st, at),
                        "bottom_hover": self._render_bottom_frame(True, st, at),
                        "top": self._render_top_frame(False, st, at),
                        "top_hover": self._render_top_frame(True, st, at),
                        "disp_name": self.item_name,
                        "disp_name_hover": self.item_name_hover
                    }

                # setup the hiehg tof this displyaable
                self.real_height = self.top_frame_height + self.SELECTOR_HEIGHT
                self.hover_height = self.real_height

                # now that we have cached renders, no need to render again
                self.first_render = False

            # now which renders are we going to select
            if self.locked:
                _suffix = ""
            elif self.hovered or self.selected:
                _suffix = "_hover"
            else:
                _suffix = ""

            _bottom_renders = self.render_cache["bottom" + _suffix]
            _top_renders = self.render_cache["top" + _suffix]
            _disp_name = self.render_cache["disp_name" + _suffix]

            # now blit
            r = renpy.Render(self.WIDTH, self.real_height)
            self._blit_top_frame(r, _top_renders, _disp_name)
            self._blit_bottom_frame(r, _bottom_renders)
            return r


init 200 python in mas_selspr:
    load_selectables()


# now these tranforms are for the selector sidebar screen
transform mas_selector_sidebar_tr_show:
    xpos 1280 xanchor 0 ypos 10 yanchor 0
    easein 0.7 xpos 1070

transform mas_selector_sidebar_tr_hide:
    xpos 1080 xanchor 0 ypos 10 yanchor 0
    easeout 0.7 xpos 1280

style mas_selector_sidebar_vbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
#    thumb "gui/slider/horizontal_hover_thumb.png"
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    bar_vertical True
    bar_invert True

# the selector screen sidebar version should be shown, not called.
# note that we do tons of calls here, so just be ready to do tons of loop overs
# every couple of seconds.
#
# IN:
#   items - list of MASSelectableImagebuttonDisplayables to display
#   mailbox - MASSelectableSpriteMailbox for messages
#   confirm - label to jump to when confirming
#   cancel - label to jump to when canceling
#   remover - remover display item, if appropriate. Can be None
screen mas_selector_sidebar(items, mailbox, confirm, cancel, remover=None):
    zorder 50
#    modal True

    frame:
        area (1075, 5, 200, 625)
        background Frame(mas_getTimeFile("mod_assets/frames/black70_pinkborder100_5px.png"), left=6, top=6, tile=True)

        vbox:
            xsize 200
            xalign 0.5
            viewport id "sidebar_scroll":
                mousewheel True
                arrowkeys True

                vbox:
                    xsize 200
                    spacing 10
                    null height 1

                    # add the remover
                    if remover is not None:
                        add remover:
                            xalign 0.5

                    for selectable in items:
                        add selectable:
#                            xoffset 5
                            xalign 0.5

                    null height 1

            null height 10

            if mailbox.read_conf_enable():
                textbutton _("Confirm"):
                    style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
                    xalign 0.5
                    action Jump(confirm)
            else:
                frame:
                    ypadding 5
                    xsize 120
                    xalign 0.5

                    background Image(mas_getTimeFile("mod_assets/hkb_disabled_background.png"))
                    text "Confirm" style ("hkb_text" if not mas_globals.dark_mode else "hkb_dark_text")

            textbutton _("Cancel"):
                style ("hkb_button" if not mas_globals.dark_mode else "hkb_dark_button")
                xalign 0.5
                action Jump(cancel)
#                action Function(mailbox.mas_send_return, -1)

        vbar value YScrollValue("sidebar_scroll"):
            style "mas_selector_sidebar_vbar"
            xoffset -25

# GENERAL sidebar selector label
# NOTE: you should NOT call this label. You should call the helper labels
# instead.
# NOTE: this shows the `mas_selector_sidebar` screen. It is the caller's
#   responsibility to hide the screen when done.
#
# IN:
#   items - list of MASSelectable objects to select from.
#   select_type - SELECT_* constant for the current mode. We throw
#       exceptions if this is not passed in and is a valid type.
#   preview_selections - True means the selections are previewed, False means
#       they are not.
#       (Default: True)
#   only_unlocked - True means we only show unlocked items, False means
#       show everything.
#       (Default: True)
#   save_on_confirm - True means we should save selections on a confirm
#       (which means we dont undo selections), while False means we will
#       undo selections on a confirm, and let the caller handle the actual
#       selection saving.
#       (Default: True)
#   mailbox - MASSelectableSpriteMailbox object to use
#       Call send_def_disp_text to set the default display text.
#       Call send_disp_text to set the inital display text.
#       IF None, we create a MASSelectableSpriteMaibox for use.
#   add_remover - True if we want to include a remover in the selector menu,
#       False if not
#       (Default: False)
#
# OUT:
#   select_map - map of selections. Organized like:
#       name: MASSelectableImageButtonDisplayable object
#
# RETURNS True if we are confirming the changes, False if not.
label mas_selector_sidebar_select(items, select_type, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False):

    python:
        if not store.mas_selspr.valid_select_type(select_type):
            raise Exception(
                "invalid selection constant: {0}".format(select_type)
            )

        # otherwise, quickly setup the flags for what mode we are in.
#        selecting_acs = select_type == store.mas_selspr.SELECT_ACS
#        selecting_hair = select_type == store.mas_selspr.SELECT_HAIR
#        selecting_clothes = select_type == store.mas_selspr.SELECT_CLOTH

        # save state
        prev_moni_state = monika_chr.save_state(True, True, True)

        # setup the mailbox
        if mailbox is None:
            mailbox = store.mas_selspr.MASSelectableSpriteMailbox()

        # pull out the remover selectable for special use, if found
        remover_item = store.mas_selspr._rm_remover(items)
        remover_disp_item = None

    # sanity check to avoid crashes
    if len(items) < 1:
        return False

    python:

        # however, we only want to actually create a remover if we were
        # asked to do so
        if add_remover:
            if remover_item is None:
                sample_sel = items[0]
                sample_obj = sample_sel.get_sprobj()

                # create generic remover item
                remover_item = store.mas_selspr.create_selectable_remover(
                    sample_obj.acs_type,
                    sample_sel.group
                )

            # unlock the remover
            remover_item.unlocked = True

            # create the displayable
            remover_disp_item = MASSelectableImageButtonDisplayable(
                remover_item,
                select_map,
                store.mas_selspr.SB_VIEWPORT_BOUNDS,
                mailbox
            )

        # only show unlock
        if only_unlocked:
            disp_items = [
                MASSelectableImageButtonDisplayable(
                    item,
                    select_map,
                    store.mas_selspr.SB_VIEWPORT_BOUNDS,
                    mailbox
                )
                for item in items
                if item.unlocked
            ]

        else:
            disp_items = [
                MASSelectableImageButtonDisplayable(
                    item,
                    select_map,
                    store.mas_selspr.SB_VIEWPORT_BOUNDS,
                    mailbox
                )
                for item in items
            ]


        # fill select map
        item_found = store.mas_selspr._fill_select_map(
            monika_chr,
            select_type,
            disp_items,
            select_map
        )

        # select remover if no item found
        if not item_found and remover_disp_item is not None:
            select_map[remover_item.name] = remover_disp_item
            remover_disp_item.selected = True

        # make copy of old select map
        old_select_map = dict(select_map)

        # also create views that we use for comparisons
        old_view = old_select_map.viewkeys()
        new_view = select_map.viewkeys()

        # disable menu interactions to prevent bugs
        disable_esc()

        # store current auto forward mode state
        afm_state = _preferences.afm_enable

        # and disable it
        _preferences.afm_enable = False

        # setup prev line
        prev_line = ""

    show screen mas_selector_sidebar(disp_items, mailbox, "mas_selector_sidebar_select_confirm", "mas_selector_sidebar_select_cancel", remover=remover_disp_item)

label mas_selector_sidebar_select_loop:
    python:
        # display text parsing
        disp_text = mailbox.get_disp_text()
        disp_fast = mailbox.get_disp_fast()

        if disp_text is None:
            disp_text = mailbox.read_def_disp_text()

        if disp_fast:
            disp_text += "{fast}"

        # select map parsing
        store.mas_selspr._clean_select_map(
            select_map,
            select_type,
            preview_selections,
            monika_chr
        )

        # once select map is cleaned, determine the confirm button enable
        mailbox.send_conf_enable(
            not store.mas_selspr.is_same(old_view, new_view)
        )

        if preview_selections:
            store.mas_selspr._adjust_monika(
                monika_chr,
                old_select_map,
                select_map,
                select_type
            )

        # force this to execute in this python block (no prediction)
        renpy.say(m, disp_text)

        #Clear repeated lines
        if prev_line != disp_text:
            _history_list.pop()
            #Using this to clear relevant entries from history
            prev_line = disp_text

    jump mas_selector_sidebar_select_loop

label mas_selector_sidebar_select_confirm:
    hide screen mas_selector_sidebar

    # re-enable the menu and restore afm
    $ _preferences.afm_enable = afm_state
    $ enable_esc()

    python:
        if not save_on_confirm:
            store.mas_selspr._clean_select_map(
                select_map,
                select_type,
                preview_selections,
                monika_chr
            )

#            store.mas_selspr._adjust_monika(
#                monika_chr,
#                old_select_map,
#                select_map,
#                select_type,
#                True
#            )

            # reload state
            monika_chr.reset_outfit()
            monika_chr.remove_all_acs()
            monika_chr.load_state(prev_moni_state)

        # If monika is wearing a remover ACS, remove it.
        for item_name in select_map.keys():
            sel_obj = select_map[item_name].selectable
            if sel_obj.remover:
                spr_obj = sel_obj.get_sprobj()
                monika_chr.remove_acs(spr_obj)
                select_map.pop(item_name)

        # delete the remover if we used one
        if add_remover:
            store.mas_selspr.rm_selectable_remover(remover_item)

        # always save confirming
        monika_chr.save()
        renpy.save_persistent()

    return True

label mas_selector_sidebar_select_cancel:
    hide screen mas_selector_sidebar

    # re-enable the menu and restore afm
    $ _preferences.afm_enable = afm_state
    $ enable_esc()

    python:
        store.mas_selspr._clean_select_map(
            select_map,
            select_type,
            preview_selections,
            monika_chr
        )

#        store.mas_selspr._adjust_monika(
#            monika_chr,
#            old_select_map,
#            select_map,
#            select_type,
#            True
#        )

        # delete the remover if we used one
        if add_remover:
            store.mas_selspr.rm_selectable_remover(remover_item)

        # reload state
        monika_chr.reset_outfit()
        monika_chr.remove_all_acs()
        monika_chr.load_state(prev_moni_state)

    return False

# ACS sidebar selector label
#
# SEE mas_selector_sidebar_select for info on input params.
# NOTE: select_type is not a param here.
#
# RETURNS: True if we are confirming the changes, False if not
label mas_selector_sidebar_select_acs(items, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False):

    call mas_selector_sidebar_select(items, store.mas_selspr.SELECT_ACS, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map, add_remover)

    return _return


# HAIR sidebar selector label
#
# SEE mas_selector_sidebar_select for info on input params.
# NOTE: select_type is not a param here.
#
# RETURNS: True if we are confirming the changes, False if not
label mas_selector_sidebar_select_hair(items, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False):

    call mas_selector_sidebar_select(items, store.mas_selspr.SELECT_HAIR, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map, add_remover)

    if _return:
        # user hit confirm
        $ persistent._mas_force_hair = True

    return _return

# CLOTH sidebar selector label
#
# SEE mas_selector_sidebar_select for info on input params.
# NOTE: select_type is not a param here.
#
# RETURNS: True if we are confirming the changes, False if not
label mas_selector_sidebar_select_clothes(items, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False):

    call mas_selector_sidebar_select(items, store.mas_selspr.SELECT_CLOTH, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map, add_remover)

    if _return:
        # user hit confirm
        $ persistent._mas_force_clothes = True

    return _return


########################## SELECTOR TOPICS ####################################
# [MONSEL]

#### Begin monika clothes topics
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_clothes_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("clothes", "change"),
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_clothes_select:
    # setup
    python:
        mailbox = store.mas_selspr.MASSelectableSpriteMailbox(
            "Which clothes would you like me to wear?"
        )
        sel_map = {}

    # initial dialogue
    m 1hua "Sure!"

    # setup the monika expression during the selection screen
    show monika 1eua

    # start the selection screen
    if mas_isMoniLove():
        # for Love, all unlocked clothes are available
        call mas_selector_sidebar_select_clothes(store.mas_selspr.CLOTH_SEL_SL, mailbox=mailbox, select_map=sel_map)

    else:
        python:
            # need to get a list of clothes that have been gifted
            # so we will get a list of all clothes and then remove the event_clothes
            gifted_clothes = mas_selspr.filter_clothes(True)

            for index in range(len(gifted_clothes)-1, -1, -1):
                spr_obj = gifted_clothes[index].get_sprobj()
                if (
                        not spr_obj.is_custom
                        and spr_obj != mas_clothes_def
                        and spr_obj != mas_clothes_blazerless
                ):
                    gifted_clothes.pop(index)

            #Now we handle holiday clothes
            clothes_to_add = persistent._mas_event_clothes_map.get(datetime.date.today())

            #If there's something for today, then we'll add it to be unlocked
            if clothes_to_add:
                #Get the outfit selector and add it
                gifted_clothes.append(mas_selspr.get_sel_clothes(
                    mas_sprites.get_sprite(
                        mas_sprites.SP_CLOTHES,
                        clothes_to_add
                    )
                ))
                gifted_clothes.sort(key=mas_selspr.selectable_key)


        # below Love, only gifted clothes (and def) are available
        call mas_selector_sidebar_select_clothes(gifted_clothes, mailbox=mailbox, select_map=sel_map)

    # results
    if not _return:
        # user hit cancel
        m 1eka "Oh, alright."

    # closing
    m 1eub "If you want me to wear different clothes, just ask, okay?"

    return


#### ends Monika clothes topic

##### monika hair topics [MONHAIR]
# TODO: as we introduce addiotinal hair types, we need to change the dialogue
# for these.

#init 5 python:
    # NOTE: this event is DEPRECATED
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_hair_ponytail",
#            category=["monika"],
#            prompt="Can you tie your hair into a ponytail?",
#            pool=True,
#            unlocked=False,
#            rules={"no unlock": None}
#        )
#    )

label monika_hair_ponytail:
    m 1eua "Sure thing!"
    m "Just give me a second."
    show monika 1dsc
    pause 1.0

    # this should auto lock/unlock stuff
    $ monika_chr.reset_hair()

    m 3hub "All done!"
    m 1eua "If you want me to let my hair down, just ask, okay?"

    return

#init 5 python:
    # NOTE: this is DEPRECATED
    # TODO: remove this event after version 0.8.10
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_hair_down",
#            category=["monika"],
#            prompt="Can you let your hair down?",
#            pool=True,
#            unlocked=False,
#            rules={"no unlock": None}
#        )
#    )

label monika_hair_down:
    m 1eua "Sure thing, [player]."
    m "Just give me a moment."
    show monika 1dsc
    pause 1.0

    $ monika_chr.change_hair(mas_hair_down)

    m 3hub "And it's down!"
    m 1eua "If you want my hair in a ponytail again, just ask away, [player]~"

    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hair_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("hair", "change"),
            pool=True,
            unlocked=False,
            rules={"no unlock": None}
        )
    )

label monika_hair_select:
    # setup
    python:
        sorted_hair = store.mas_selspr.HAIR_SEL_SL
        mailbox = store.mas_selspr.MASSelectableSpriteMailbox(
            "Which hairstyle would you like me to wear?"
        )
        sel_map = {}

    # initial dialogue
    m 1hua "Sure!"

    # setup the monika expression during the selection screen
    show monika 1eua

    # start the selection screen
    call mas_selector_sidebar_select_hair(sorted_hair, mailbox=mailbox, select_map=sel_map)

    # results
    if not _return:
        # user hit cancel
        m 1eka "Oh, alright."

    # closing
    m 1eub "If you want my hair in a different style, just ask, okay?"

    return

##### End monika hair topics

#### Monika ribbons topic
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_ribbon_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("ribbon", "change"),
            pool=True,
            unlocked=False,
            rules={"no unlock": None}
        )
    )

label monika_ribbon_select:
    python:
        # if we are not using a force ribbon hair, add a remover.
#        use_remover = not monika_chr.is_wearing_hair_with_exprop("force-ribbon")

        use_acs = store.mas_selspr.filter_acs(True, group="ribbon")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Which ribbon would you like me to wear?")
        sel_map = {}

    m 1eua "Sure [player]!"

#    if monika_chr.hair.name != mas_hair_def.name:
#        m "But im going to change my clothes and hair back to normal."
#        $ monika_chr.reset_outfit(False)


    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map, add_remover=True)

    if not _return:
        m 1eka "Oh, alright."

    # set appropriate prompt and dialogue
    if monika_chr.get_acs_of_type("ribbon"):
#        $ ribbon_prompt_key = "change"
        $ ribbon_dlg = "If you want me to change my ribbon, just ask, okay?"

    else:
#        $ ribbon_prompt_key = "wear"
        $ ribbon_dlg = "If you want me to wear a ribbon again, just ask, okay?"

#    $ store.mas_selspr.set_prompt("ribbon", ribbon_prompt_key)

    m 1eka "[ribbon_dlg]"

    return
#### End Ribbon change topic

#### Monika hairclips
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hairclip_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("left-hair-clip", "change"),
            pool=True,
            unlocked=False,
            rules={"no unlock": None},
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_hairclip_select:
    python:
        use_acs = store.mas_selspr.filter_acs(True, group="left-hair-clip")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox(
            "Which hairclip would you like me to wear?"
        )
        sel_map = {}

    m 1eua "Sure [player]!"

    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map, add_remover=True)

    if not _return:
        m 1eka "Oh, alright."

    # set the appropriate prompt and dialogue
    if monika_chr.get_acs_of_type('left-hair-clip'):
        $ store.mas_selspr.set_prompt("left-hair-clip", "change")
        m 1eka "If you want me to change my hairclip, just ask, okay?"
    else:
        $ store.mas_selspr.set_prompt("left-hair-clip", "wear")
        m 1eka "If you want me to wear a hairclip again, just ask, okay?"

    return


#### End Monika hairclips/strand topics

#### Monika left hair flower
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_hairflower_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("left-hair-flower", "change"),
            pool=True,
            unlocked=False,
            rules={"no unlock": None},
            aff_range=(mas_aff.HAPPY, None)
        )
    )

label monika_hairflower_select:
    python:
        use_acs = store.mas_selspr.filter_acs(True, group="left-hair-flower")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox(
            "Which flower would you like me to put in my hair?"
        )
        sel_map = {}

    m 1eua "Sure [player]!"

    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map, add_remover=True)

    if not _return:
        m 1eka "Oh, alright."

    # set the appropriate prompt and dialogue
    if monika_chr.get_acs_of_type("left-hair-flower"):
        $ store.mas_selspr.set_prompt("left-hair-flower", "change")
        m 1eka "If you want me to change the flower, just ask, okay?"
    else:
        $ store.mas_selspr.set_prompt("left-hair-flower", "wear")
        m 1eka "If you want me to wear a flower, just ask, okay?"

    return

#### End Monika hairflower


############### END SELECTOR TOPICS ###########################################
