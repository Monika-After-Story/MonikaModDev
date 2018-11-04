## module that contains a workable selection screen?
#
# NOTE: i have no idea how generic this can get.
#   Chances are, it will not be very generic.
#
# Selection MAPS:
#   new class: Selec


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
            display_name - the name to use in the selectbale button screen
            thumb - thumbnail image to use for selection screen. Aim for a
                180x180
            group - string id to group related selectable sprites. this really
                applies only to acs, but in case other things need this.
            unlocked - True if this selectable sprite can be selected, 
                False otherwise.
            visible_when_locked - True if this should be visible when locked
                False, otherwise.
                Locked items will generally be displayed with a placeholder
                thumb.
            hover_dlg - label to call when hovering over this object
            first_select_dlg - label to call the first time you select
                this sprite
            select_dlg - label to call everytime you select this sprite
                (after the first time)
        """


        def __init__(self, 
                _sprite_object,
                display_name,
                thumb, 
                group,
                unlocked=False,
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
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - label to call when hovering over this object
                    (Default: None)
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
            self.display_name = display_name
            self.thumb = thumb
            self.group = group
            self.unlocked = unlocked
            self.visible_when_locked = visible_when_locked
            self.hover_dlg = hover_dlg
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
                display_name
                thumb,
                group,
                unlocked=False,
                visible_when_locked=True,
                hover_dlg,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableAccessory

            IN:
                _sprite_object - MASAccessory object to build this selectable
                    sprite object with.
                display_name - name to show on the selectable screen
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - label to call when hovering over this object
                    (Default: None)
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
                display_name,
                thumb,
                group,
                unlocked,
                visible_when_locked,
                hover_dlg,
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
                display_name,
                thumb,
                group,
                unlocked=False,
                visible_when_locked=True,
                hover_dlg,
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
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - label to call when hovering over this object
                    (Default: None)
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
                display_name,
                thumb,
                group,
                unlocked,
                visible_when_locked,
                hover_dlg,
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
                display_name,
                thumb,
                group,
                unlocked=False,
                visible_when_locked=True,
                hover_dlg,
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
                unlocked - True if this item is unlocked, false otherwise
                    (Default: False)
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - label to call when hovering over this object
                    (Default: None)
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
                display_name,
                thumb,
                group,
                unlocked,
                visible_when_locked,
                hover_dlg,
                first_select_dlg,
                select_dlg
            )


# now these tranforms are for the selector sidebar screen
transform mas_selector_sidebar_tr_show
    xpos 1280 xanchor 0 ypos 10 yanchor 0
    easein 0.7 xpos 1070

transform mas_selector_sidebar_tr_hide
    xpos 1080 xanchor 0 ypos 10 yanchor 0
    easeout 0.7 xpos 1280

style mas_selector_sidebar_vbar:
    xsize 18
    base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
#    thumb "gui/slider/horizontal_hover_thumb.png"
    thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    bar_vertical True

# the selector screen sidebar version should be shown, not called.
# note that we do tons of calls here, so just be ready to do tons of loop overs
# every couple of seconds.
screen mas_selector_sidebar(items, only_unlocked=True):
    zorder 50


    frame:
        area (1070, 10, 200, 700)

        viewport id "sidebar_scroll"
            mousewheel True
            arrowkeys True

            # TODO: custom displayabe button
                


        vbar value YScrollValue("sidebar_scroll"):
            style "mas_selector_sidebar_vbar"
            xoffset -20

