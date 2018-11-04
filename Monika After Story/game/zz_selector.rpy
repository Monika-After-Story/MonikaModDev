## module that contains a workable selection screen?
#
# NOTE: i have no idea how generic this can get.
#   Chances are, it will not be very generic.
#
# Selection MAPS:
#   new class: Selec

# TODO:
# NEW CLASS
#   - thumb (thumbnail image name)
#   - group (basically a string id that can be used to group related acs)
#   - unlocked (True if unlocked, False if not)

# databaess for selectable sprite data
# currently we only store UNLOCKED
default persistent._mas_selspr_acs_db = {}
default persistent._mas_selspr_hair_db = {}
default persistent._mas_selspr_clothes_db = {}

init 200 python:

    class MASSelectableSprite(object):
        """
        Wrapper around selectable sprite objects. We do this instead of
        extending because not everything would be selectble

        PROPERTIES:
            name - this is always the same thing as the MASSprite object we
                create thsi with.
            thumb - thumbnail image to use for selection screen. Aim for a
                200x200 size.
            group - string id to group related selectable sprites. this really
                applies only to acs, but in case other things need this.
            unlocked - True if this selectable sprite can be selected, 
                False otherwise.
            visible_when_locked - True if this should be visible when locked
                False, otherwise.
                Locked items will generally be displayed with a placeholder
                thumb.
            first_select_dlg - label to call the first time you select
                this sprite
            select_dlg - label to call everytime you select this sprite
                (after the first time)
        """


        def __init__(self, 
                _sprite_object,
                thumb, 
                group,
                unlocked=False,
                visible_when_locked=True,
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
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                first_select_dlg - label to call the first time you select this
                    sprite. 
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.
                    (Default: None)
                select_dlg - label to call subsequent times you select this 
                    sprite.
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.
            """
            self.name = _sprite_object.name
            self.thumb = thumb
            self.group = group
            self.unlocked = unlocked
            self.visible_when_locked = visible_when_locked
            self.first_select_dlg = first_select_dlg
            self.select_dlg = select_dlg


    class MASSelectableAccessory(MASSelectableSprite):
        """
        Wrapper around MASAccessory sprite objects.

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherieted properties
        """

        def __init__(self,
                _sprite_object,
                thumb,
                group,
                unlocked=False,
                visible_when_locked=True,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableAccessory

            IN:
                _sprite_object - MASAccessory object to build this selectable
                    sprite object with.
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                first_select_dlg - label to call the first time you select this
                    sprite. 
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.
                    (Default: None)
                select_dlg - label to call subsequent times you select this 
                    sprite.
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.        
            """
            if type(_sprite_object) != MASAccessory:
                raise new Exception("not an acs: {0}".format(group))

            super(MASSelectableAccessory, self).__init__(
                _sprite_object,
                thumb,
                group,
                unlocked,
                visible_when_locked,
                first_select_dlg,
                select_dlg
            )


    class MASSelectableHair(MASSelectableSprite):
        """
        Wrappare around MASHair sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """


        def __init__(self,
                _sprite_object,
                thumb,
                group,
                unlocked=False,
                visible_when_locked=True,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableHair constructor

            IN:
                _sprite_object - MASHair object to build this selectable
                    sprite object with.
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                first_select_dlg - label to call the first time you select this
                    sprite. 
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.
                    (Default: None)
                select_dlg - label to call subsequent times you select this 
                    sprite.
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.        
            """
            if type(_sprite_object) != MASHair:
                raise new Exception("not a hair: {0}".format(group))

            super(MASSelectableHair, self).__init__(
                _sprite_object,
                thumb,
                group,
                unlocked,
                visible_when_locked,
                first_select_dlg,
                select_dlg
            )


    class MASSelectableClothes(MASSelectableSprite):
        """
        Wrappare around MASClothes sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """


        def __init__(self,
                _sprite_object,
                thumb,
                group,
                unlocked=False,
                visible_when_locked=True,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableClothes constructor

            IN:
                _sprite_object - MASClothes object to build this selectable
                    sprite object with.
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                first_select_dlg - label to call the first time you select this
                    sprite. 
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.
                    (Default: None)
                select_dlg - label to call subsequent times you select this 
                    sprite.
                    NOTE: the caller is responsible for actually calling this
                    set of dialogue.        
            """
            if type(_sprite_object) != MASClothes:
                raise new Exception("not a clothes: {0}".format(group))

            super(MASSelectableClothes, self).__init__(
                _sprite_object,
                thumb,
                group,
                unlocked,
                visible_when_locked,
                first_select_dlg,
                select_dlg
            )
