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
                (png is added in the constructor)
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
            selected - True if this item is selected, False if not
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
#            self._check_dlg(hover_dlg)
#            self._check_dlg(first_select_dlg)
#            self._check_dlg(select_dlg)

            self.name = _sprite_object.name
            self.display_name = display_name
            self.thumb = thumb + ".png"
            self.group = group
            self.unlocked = unlocked
            self.visible_when_locked = visible_when_locked
            self.hover_dlg = hover_dlg
            self.first_select_dlg = first_select_dlg
            self.select_dlg = select_dlg
            self.selected = False


        def _check_dlg(self, dlg):
            if dlg is not None and not renpy.has_label(dlg):
                raise Exception("label '{0}' no exist".format(dlg))


    class MASSelectableAccessory(MASSelectableSprite):
        """
        Wrapper around MASAccessory sprite objects.

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherieted properties
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
                raise Exception("not an acs: {0}".format(group))

            super(MASSelectableAccessory, self).__init__(
                _sprite_object,
                display_name,
                "acs-" + thumb,
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
                raise Exception("not a hair: {0}".format(group))

            super(MASSelectableHair, self).__init__(
                _sprite_object,
                display_name,
                "hair-" + thumb,
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
                raise Exception("not a clothes: {0}".format(group))

            super(MASSelectableClothes, self).__init__(
                _sprite_object,
                display_name,
                "clothes-" + thumb,
                group,
                unlocked,
                visible_when_locked,
                hover_dlg,
                first_select_dlg,
                select_dlg
            )


init -1 python:

    
    ## custom displayable
    class MASSelectableImageButtonDisplayable(renpy.Displayable):
        """
        Custom button for the selectable items.
        """
        import pygame

        # constnats
        THUMB_DIR = "mod_assets/thumb/"

        WIDTH = 180 # default width
        
        # technically this should change.
        TOTAL_HEIGHT = 218 
        SELECTOR_HEIGHT = 180 

        # this is the default, but the real may change using the expanding
        # frame properties.
        TOP_FRAME_HEIGHT = 38 # default


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
                show_dlg=[],
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
                show_dlg - list to add dialogue lines to show to the user.
                    NOTE: its up to the caller to apply subs or not
                multi_select - True means we can select more than one item.
                    False otherwise
                    (Default: False)
            """
            super(MASSelectableImageButtonDisplayable, self).__init__()

            self.selectable = _selectable
            self.select_map = select_map
            self.show_dlg = show_dlg
            self.multi_select = multi_select

            # image setups
            self.thumb = Image(self.THUMB_DIR + _selectable.thumb)
            self.thumb_overlay = Image(
                "mod_assets/frames/selector_overlay.png"
            )
            self.top_frame = Frame(
                "mod_assets/frames/selector_top_frame.png",
                left=3,
                top=3,
                tile=True
            )
            self.top_frame_selected = Frame(
                "mod_assets/frames/selector_top_frame_selected.png",
                left=3,
                top=3,
                tile=True
            )

            # renpy solids and stuff
            self.hover_overlay = Solid("#ffaa99aa")

            # text objects
            self.item_name = self._display_name(False)
            self.item_name_hover = self._display_name(True)

            # setup viewport bound values
            vpx, vpy, vpw, vph, vpb = viewport_bounds
            self.xlim_lo = vpx + vpb
            self.xlim_up = (vpx + vpw) - vpb
            self.ylim_lo = vpy + vpb
            self.ylim_up = (vpy + vph) - vpb

            # flags
            self.hovered = False
            self.hover_jumped = False # True means we just jumped to label
            self.hover_width = self.WIDTH
            self.hover_height = self.TOTAL_HEIGHT # TODO

            self.selected = False
            self.select_jump = False


        def _check_display_name(self, _display_name_text):
            """
            Checks the given display name to see if it fits within the frame
            bounds. We will have to adjust if not

            IN:
                _display_name_text - Text object of the display name

            RETURNS:
                True if it fits, False if not
            """
            return True


        def _display_name(self, selected):
            """
            Returns the text object for the display name.

            IN:
                selected - True if selected, False if not

            RETURNS:
                the text object for the display name
            """
            # TODO: auto split
            if selected:
                color = "#fa9"
            else:
                color = "#000"

            return Text(
                self.selectable.display_name,
                font=gui.default_font,
                size=gui.text_size,
                color=color,
                outlines=[]
            )


        def _hover_jump(self):
            """
            Jumps to hover if applicable.
            Also does some hover data resetting.
            """
            if self.selectable.hover_dlg is not None:
                if not self.hovered:
                    self.hover_jumped = False

                elif not self.hover_jumped:
                    self.hover_jumped = True
#                    renpy.say(m, "I AM HOVER", interact=False)
                    self.show_dlg.append(self.selectable.hover_dlg)
                    renpy.end_interaction(True)
#                    renpy.call_in_new_context(self.selectable.hover_dlg)


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
            # TODO smart frmae size
            return renpy.render(
                piece,
                self.WIDTH,
                self.TOP_FRAME_HEIGHT,
                st,
                at
            )


        def _render_display_name(self, hover, st, at):
            """
            Smart renders the display name. This is currently a place holder.
            """
            if hover:
                return renpy.render(
                    self.item_name_hover,
                    self.WIDTH,
                    self.TOP_FRAME_HEIGHT,
                    st,
                    at
                )

            return renpy.render(
                self.item_name,
                self.WIDTH,
                self.TOP_FRAME_HEIGHT,
                st,
                at
            )


        def _blit_bottom_frame(self, r, _renders):
            """
            bliting the bottom frames

            # TODO documentation
            """
            # TODO: modify for adjustable top frames
            for _render in _renders:
                r.blit(_render, (0, 38))


        def _blit_top_frame(self, r, _renders, _disp_name):
            """
            bliting the top frames

            # TODO documentaiton
            """
            for _render in _renders:
                r.blit(_render, (0, 0))

            # text
            # NOTE: this is top left. to do align on bottom, you must get 
            #   size
            # TODO: modify for adjustable top frames
            dnw, dnh = _disp_name.get_size()
            r.blit(_disp_name, (5, 35 - dnh))


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


        def event(self, ev, x, y, st):
            """
            EVENT. We only want to handle 2 cases:
                MOUSEMOTION + hover is over us
                MOUSEDOWN + mouse is over us
            """
            if ev.type in self.MOUSE_EVENTS:
                
                if ev.type == pygame.MOUSEMOTION:
                    self.hovered = self._is_over_me(x, y)
                    renpy.redraw(self, 0)

                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    
                    if ev.button in self.MOUSE_WHEEL:
                        # TODO: scrolling in mouse wheel is not perfect, 
                        #   the previously hovered item gest hovered instead
                        #   of what we actually want.
                        self.hovered = self._is_over_me(x, y)
                        renpy.redraw(self, 0)           

                    elif ev.button == 1:
                        # left click
                        # select something
                        pass


            self._hover_jump()



        def render(self, width, height, st, at):
            """
            Render. we want the button here.
            """
            # first, render all items.
            _bottom_renders = self._render_bottom_frame(self.hovered, st, at)
            _top_renders = self._render_top_frame(self.hovered, st, at)
            _disp_name = self._render_display_name(self.hovered, st, at)

            # now blit
            r = renpy.Render(self.WIDTH, self.TOTAL_HEIGHT)
            self._blit_top_frame(r, _top_renders, _disp_name)
            self._blit_bottom_frame(r, _bottom_renders)
            return r


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
#   only_unlocked - True means we only show the unlocked ones.
#   confirm - label to jump to when confirming
#   cancel - label to jump to when canceling
screen mas_selector_sidebar(items, confirm, cancel, only_unlocked=True):
    zorder 50

    frame:
        area (1075, 5, 200, 625)
        background Frame("mod_assets/frames/black70_pinkborder100_5px.png", left=6, top=6, tile=True)

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

                    for selectable in items:
                        add selectable:
#                            xoffset 5
                            xalign 0.5

                    null height 1

            null height 10
            textbutton _("Confirm"):
                style "hkb_button"
                xalign 0.5
                action Jump(confirm)
            textbutton _("Cancel"):
                style "hkb_button"
                xalign 0.5
                action Jump(cancel)

        vbar value YScrollValue("sidebar_scroll"):
            style "mas_selector_sidebar_vbar"
            xoffset -25

