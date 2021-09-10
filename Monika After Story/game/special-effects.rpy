# This file is meant to store any special effects.
# These can be some images or transforms.
init -500 python in mas_parallax:
    import pygame
    import math

    import store

    class ParallaxDecal(object):
        """
        Represents a decal. Basically a struct, made for convenience
        This is not a desplayable.
        """
        def __init__(self, img, x=0, y=0, z=0):
            """
            Constructor for decals

            IN:
                img - the img/disp for this decal
                x - the x offset from the center of the main sprite
                    (Default: 0)
                y - the y offset from the center of the main sprite
                    (Default: 0)
                z - basically zorder
                    (Default: 0)
            """
            self.img = renpy.easy.displayable(img)
            self._x = x
            self._y = y
            self._z = z
            self.callback = None

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value
            if self.callback:
                self.callback()

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, value):
            self._y = value
            if self.callback:
                self.callback()

        @property
        def z(self):
            return self._z

        @z.setter
        def z(self, value):
            self._z = value
            if self.callback:
                self.callback()

        def __repr__(self):
            """
            Representation of this object
            """
            return "<{0}: (img: {1}, x: {2}, y: {3}, z: {4})>".format(type(self).__name__, repr(self.img), self._x, self._y, self._z)

    class _ParallaxDecalContainer(renpy.display.core.Displayable):
        """
        A container displayable. It takes a base (consider it main displayable) and any number of children.
        The container will be of just enough size to contain the base and the children, aligning everything to its center.
        Children can be given x, y, and zorder offsets relative to the center
        """
        def __init__(self, base, *children):
            """
            Constructor for containers

            IN:
                base - the base img (must be ParallaxDecal)
                children - children imgs (must be ParallaxDecal)
            """
            super(_ParallaxDecalContainer, self).__init__()

            self._base = base

            self._decals = list(children)
            self._decals.append(base)
            self.__sort_decals()
            for decal in self._decals:
                if not isinstance(decal, ParallaxDecal):
                    raise Exception("{0} can accept only ParallaxDecal, got: {1}".format(type(self).__name__, type(decal)))
                decal.callback = self.update

            self.size = (0, 0)

        def __sort_decals(self):
            """
            Sorts inner list of images, ensures the base is being the last
            """
            self._decals.sort(key=lambda decal: decal.z - float(decal is self._base)/2.0)

        @property
        def base(self):
            return self._base

        @base.setter
        def base(self, decal):
            if not isinstance(decal, ParallaxDecal):
                return

            base_id = self._decals.index(self._base)
            old_base = self._decals.pop(base_id)
            old_base.callback = None
            decal.callback = self.update
            self._base = decal
            self._decals.insert(base_id, decal)

            renpy.redraw(self, 0.0)

        @property
        def children(self):
            return [decal for decal in self._decals if decal is not self._base]

        def __repr__(self):
            """
            Representation of this object
            """
            return "<{0}: (base: {1}, children: {2})>".format(type(self).__name__, self._base, self.children)

        def add(self, *decals):
            """
            Adds a ParallaxDecal to this container
            """
            for decal in decals:
                if not isinstance(decal, ParallaxDecal):
                    continue

                decal.callback = self.update
                self._decals.append(decal)

            self.__sort_decals()
            renpy.redraw(self, 0.0)

        def remove(self, *decals):
            """
            Removes a ParallaxDecal instance from this container
            """
            for decal in decals:
                if decal in self._decals and decal is not self._base:
                    decal.callback = None
                    self._decals.remove(decal)

            renpy.redraw(self, 0.0)

        def remove_all(self):
            """
            Removes all decals from this container
            """
            for child in self.children:
                self._decals.remove(child)
                child.callback = None
            renpy.redraw(self, 0.0)

        def render(self, width, height, st, at):
            """
            The render method where we do the meth logic to align everything properly
            """
            # Predefine the size of the final render
            main_render_width = 0
            main_render_height = 0

            render_items = list()
            for decal in self._decals:
                decal_disp = decal.img
                decal_x_offset, decal_y_offset = decal.x, decal.y

                decal_render = renpy.render(decal_disp, width, height, st, at)
                decal_width = decal_render.width
                decal_height = decal_render.height

                main_render_width = max(main_render_width, decal_width)
                main_render_height = max(main_render_height, decal_height)

                width_diff = main_render_width - decal_width
                height_diff = main_render_height - decal_height
                abs_x_offset = abs(decal_x_offset)
                abs_y_offset = abs(decal_y_offset)

                if abs_x_offset > max(0, width_diff / 2.0):
                    main_render_width += (2*abs_x_offset - width_diff)

                if abs_y_offset > max(0, height_diff / 2.0):
                    main_render_height += (2*abs_y_offset - height_diff)

                render_items.append(
                    (
                        decal_disp,
                        decal_render,
                        decal_width/2.0 - decal_x_offset,
                        decal_height/2.0 - decal_y_offset
                    )
                )

            # Now that we finally have the appropriate width and height for the render, render our stuff
            main_render = renpy.Render(main_render_width, main_render_height)
            for _disp, _render, _x_offset, _y_offset in render_items:
                main_render.place(
                    _disp,
                    x=main_render_width/2.0 - _x_offset,
                    y=main_render_height/2.0 - _y_offset,
                    render=_render
                )

            # renpy.redraw(self, 1.0)
            self.size = (main_render_width, main_render_height)
            # main_render.fill("#ca00004d")

            return main_render

        def update(self):
            """
            Updates this disp
            """
            self.__sort_decals()
            renpy.redraw(self, 0)

        def visit(self):
            """
            Returns images of this disp for prediction
            """
            return [decal.img for decal in self._decals]


    class ParallaxSprite(renpy.display.core.Displayable):
        """
        Class to represent signle parallax sprite
        """
        NORMAL_ZOOM = 1.0
        DEF_ANCHOR = (0.5, 0.5)

        def __init__(self, img, x, y, z, function=None, decals=(), on_click=None, min_zoom=1.0, max_zoom=4.0):
            """
            Constructor for parallax sprites
            NOTE: the child image will be anchored to its center, bear that in mind when giving it transforms

            IN:
                img - path to the img/Displayable
                x - base x coord for the sprite
                y - base y coord for the sprite
                z - base z coord for the sprite
                    NOTE: treat this as zorder
                    NOTE: MUST BE > 0
                function - a function for the sprite's transform,
                    use it if you need additional effects
                    NOTE: your function SHOULD NOT affect the xoffset/yoffset/zoom (zoom only if you enabled it for the user) props
                    (Default: None)
                decals - list of decals for this sprite
                    (Default: empty tuple)
                on_click - a callable object that gets called on click (LMB) events
                    (Default: None)
                min_zoom - min zoom value
                    (Default: 1.0)
                max_zoom - max zoom value
                    (Default: 4.0)
                    NOTE: if min_zoom == max_zoom, the user won't be able to zoom in/out
            """

            super(ParallaxSprite, self).__init__()

            # For convenience, we assume the mouse is in the center
            self.mouse_x = 0
            self.mouse_y = 0
            self.reset_mouse_pos()

            self._x = x
            self._y = y
            if z < 1:
                raise Exception("The zorder property must be greater than 0.")
            self._z = z

            self._container = _ParallaxDecalContainer(
                ParallaxDecal(img, 0, 0, 0),
                *decals
            )

            self._transform = store.Transform(
                self._container,
                # TODO: enable functions
                # function=function,
                anchor=ParallaxSprite.DEF_ANCHOR,
                transform_anchor=True,
                subpixel=True
            )
            self._transform.zorder = z

            self.min_zoom = min_zoom
            self.max_zoom = max_zoom
            self._zoom = min_zoom

            # Set this again to run the methods
            self.zoom = min_zoom

            self._render = None

            if on_click is not None and not callable(on_click):
                raise Exception("The on_click property must be a callable.")
            self.on_click = on_click

            self._enable_events = True

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value
            self.update_offsets()

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, value):
            self._y = value
            self.update_offsets()

        @property
        def z(self):
            return self._z

        @z.setter
        def z(self, value):
            self._z = value
            self.update_offsets()

        @property
        def zoom(self):
            return self._zoom

        @zoom.setter
        def zoom(self, value):
            value = min(max(value, self.min_zoom), self.max_zoom)
            self._zoom = value
            self._transform.zoom = value
            self.update_offsets()

        def update_mouse_pos(self):
            """
            Updates mouse pos
            """
            self.mouse_x, self.mouse_y = renpy.get_mouse_pos()

        def reset_mouse_pos(self):
            """
            Resets mouse pos
            """
            self.mouse_x = int(renpy.config.screen_width / 2.0)
            self.mouse_y = int(renpy.config.screen_height / 2.0)

        def toggle_events(self, value):
            """
            Toggles events (and hence the parallax effect)
            """
            self._enable_events = value

        def __repr__(self):
            """
            Representation of this object
            """
            return "<{0}: (img: {1}, x: {2}, y: {3}, z: {4}, decals: {5})>".format(type(self).__name__, self._container.base, self._x, self._y, self._z, self._container.children)

        def update_offsets(self):
            """
            Updates the offsets of this parallax sprite
            NOTE: I have no idea how I made this meth work, don't change it
            """
            zoom_factor = abs(self._zoom - ParallaxSprite.NORMAL_ZOOM)

            # NOTE: Here we make an important assumption - the img we use (the container) will be of the screen width/height
            zoom_correction_x = renpy.config.screen_width * zoom_factor / 2.0
            zoom_correction_y = renpy.config.screen_height * zoom_factor / 2.0

            # We use screen_width and screen_height for our parallax
            available_x_shift = renpy.config.screen_width / float(self._z)
            available_y_shift = renpy.config.screen_height / float(self._z)

            half_screen_width = renpy.config.screen_width / 2.0
            half_screen_height = renpy.config.screen_height / 2.0

            mouse_x_factor = self.mouse_x / half_screen_width
            mouse_y_factor = self.mouse_y / half_screen_height

            # Our offsets consist of 3 parts:
            # - base coords give offsets to x and y (depend on zoom level)
            # - shift from the parallax effect (depends on mouse pos)
            # - correction to the zoom effect (depends on mouse pos)
            self._transform.xoffset = self._x*(1.0 + zoom_factor) + available_x_shift*(1.0 - mouse_x_factor) - zoom_correction_x*mouse_x_factor
            self._transform.yoffset = self._y*(1.0 + zoom_factor) + available_y_shift*(1.0 - mouse_y_factor) - zoom_correction_y*mouse_y_factor

            # Now update the screen
            self._transform.update()
            renpy.redraw(self, 0.0)

        def __getstate__(self):
            """
            This is used for pickling. Render objects cannot be pickled, so here we reset the value of _render to None.
            The docs say CDD shouldn't keep Render, but we have to, as it works much better than
            the built-in focus system which RenPy uses (for some reason it's more laggy and causes a few bugs).
            Instead we keep the latest Render and check whether or not the pixel at the given x and y is opaque (apparently it's faster).

            NOTE: The docs say CDD can be pickled, but it doesn't seem to be the case as Style objects inside them cannot be.
                Nevertheless, I decided to handle this case so we can be sure that isn't our fault.
            """
            rv = super(ParallaxSprite, self).__getstate__()
            rv["_render"] = None

            return rv

        def event(self, ev, x, y, st):
            """
            The event handler
            TODO: allow to move around and zoom in/out with keyboard
            """
            if self._enable_events:
                if ev.type == pygame.MOUSEMOTION:
                    self.update_mouse_pos()
                    self.update_offsets()

                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.min_zoom != self.max_zoom:
                        if ev.button == 4:
                            self.zoom += 0.1

                        elif ev.button == 5:
                            self.zoom -= 0.1

                elif ev.type == pygame.MOUSEBUTTONUP:
                    if ev.button == 1:
                        # if self.on_click is not None and self.is_focused():
                        if self.on_click is not None and self._render.is_pixel_opaque(x, y):
                            self.on_click()
                            # raise renpy.IgnoreEvent()

            return None

        def render(self, width, height, st, at):
            """
            The render method
            """
            img_render = renpy.render(self._transform, width, height, st, at)
            main_render = renpy.Render(width, height)
            main_render.place(self._transform, x=0, y=0, render=img_render)
            # main_render.add_focus(self, None, 0, 0, renpy.config.screen_width, renpy.config.screen_height, 0, 0, main_render)
            self._render = main_render

            return main_render

        def visit(self):
            """
            Returns the transform for prediction
            """
            return [self._transform]

        def predict_one(self):
            """
            Called to ask this displayable to call the callback with all
            the images it may want to load.
            """
            if self._enable_events:
                self.update_mouse_pos()
            self.update_offsets()


    @store.mas_utils.deprecated(use_instead="ParallaxSprite")
    class ParallaxBackground(renpy.display.core.Displayable):
        """
        DEPRECATED
        Class to represent a background with parallax effect
        """
        NORMAL_ZOOM = 1.0
        DEF_ANCHOR = (0.5, 0.5)

        def __init__(self, img, zoom=1.0, min_zoom=1.0, max_zoom=4.0):
            """
            Constructor for parallax background

            IN:
                img - the img for this background
                zoom - default zoom for this sprite
                    (Default: 1.0)
                min_zoom - min zoom value
                    (Default: 1.0)
                max_zoom - max zoom value
                    (Default: 4.0)
                NOTE: if min_zoom == max_zoom, the user won't be able to zoom in/out
            """
            super(ParallaxBackground, self).__init__()

            self.mouse_x = renpy.config.screen_width / 2.0
            self.mouse_y = renpy.config.screen_height / 2.0

            img = renpy.easy.displayable(img)
            self.size = img.load().get_size()

            self._transform = store.Transform(
                img,
                anchor=ParallaxBackground.DEF_ANCHOR,
                transform_anchor=True,
                subpixel=True
            )

            self.min_zoom = min_zoom
            self.max_zoom = max_zoom
            self._zoom = zoom

            self.zoom = zoom

        @property
        def zoom(self):
            return self._zoom

        @zoom.setter
        def zoom(self, value):
            value = min(max(value, self.min_zoom), self.max_zoom)
            self._zoom = value
            self._transform.zoom = value
            self.update_offsets()

        def __repr__(self):
            """
            Representation of this object
            """
            return "<{0}: (img: {1})>".format(type(self).__name__, self._transform.child)

        def update_offsets(self):
            """
            Updates the offsets of this background
            """
            #NOTE: Factor should always be > 0 here
            zoom_factor = self._zoom - ParallaxBackground.NORMAL_ZOOM
            available_x_shift = renpy.config.screen_width * zoom_factor / 2.0
            available_y_shift = renpy.config.screen_height * zoom_factor / 2.0

            half_screen_width = renpy.config.screen_width / 2.0
            half_screen_height = renpy.config.screen_height / 2.0

            self._transform.xoffset = self.size[0]/2 + available_x_shift*(2 - self.mouse_x/half_screen_width)
            self._transform.yoffset = self.size[1]/2 + available_y_shift*(3 - self.mouse_y/half_screen_height)

            self._transform.update()
            renpy.redraw(self, 0)

        def event(self, ev, x, y, st):
            """
            The event handler
            """
            if ev.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = renpy.get_mouse_pos()
                self.update_offsets()

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if self.min_zoom != self.max_zoom:
                    if ev.button == 4:
                        self.zoom += 0.1

                    elif ev.button == 5:
                        self.zoom -= 0.1

            return None

        def render(self, width, height, st, at):
            """
            The render method
            """
            img_render = renpy.render(self._transform, width, height, st, at)
            main_render = renpy.Render(width, height)
            main_render.place(self._transform, x=0, y=0, render=img_render)

            return main_render

        def visit(self):
            """
            Returns the background for prediction
            """
            return [self._transform]

        def predict_one(self):
            """
            Called to ask this displayable to call the callback with all
            the images it may want to load.
            """
            self.mouse_x, self.mouse_y = renpy.get_mouse_pos()
            self.update_offsets()


image yuri dragon2:
    parallel:
        "yuri/dragon1.png"
        0.01
        "yuri/dragon2.png"
        0.01
        repeat

image blood splatter1:
    size (1, 1)
    truecenter
    Blood("blood_particle",dripTime=0.5, burstSize=150, burstSpeedX=400.0, burstSpeedY=400.0, numSquirts=15, squirtPower=400, squirtTime=2.0).sm

image k_rects_eyes1:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (580, 270)
    size (20, 25)
    8.0

image k_rects_eyes2:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (652, 264)
    size (20, 25)
    8.0

image natsuki mas_ghost:
    "natsuki ghost2"
    parallel:
        easeout 0.25 zoom 4.5 yoffset 1200
    parallel:
        ease 0.025 xoffset -20
        ease 0.025 xoffset 20
        repeat
    0.25

image mujina:
    "mod_assets/other/mujina.png"
    zoom 1.25
    parallel:
        easeout 0.5 zoom 4.5 yoffset 1200
    0.5

image mas_lightning:
    "mod_assets/other/thunder.png"
    alpha 1.0

    choice:
        block:
            0.05
            alpha 0.0
            0.05
            alpha 1.0
            repeat 3

    choice:
        block:
            0.05
            alpha 0.0
            0.05
            alpha 1.0
            repeat 2

    choice:
        0.05

    parallel:
        easeout 2.8 alpha 0.0
    3.0
    Null()

image mas_lightning_s_bg = LiveComposite(
    (1280, 720),
    (0, 0), "mod_assets/other/thunder.png",
    (30, 200), "mod_assets/other/tree_sil.png"
)

image mas_lightning_s:
    "mas_lightning_s_bg"
    alpha 1.0

    block:
        0.05
        alpha 0.0
        0.05
        alpha 1.0
        repeat 2

    0.05
    alpha 0.0
    0.05
    "mod_assets/other/thunder.png"
    alpha 1.0

    parallel:
        easeout 2.8 alpha 0.0
    3.0
    Null()

image mas_lantern:
    "mod_assets/other/lantern.png"
    alpha 0.0
    block:
        0.05
        alpha 1.0
        0.05
        alpha 0.0
        repeat 4
    alpha 0.0

image mas_stab_wound:
    "mod_assets/other/stab-wound.png"
    zoom 0.9
    easein 1.0 zoom 1.0

image rects_bn1:
    RectCluster(Solid("#000"), 25, 20, 15).sm
    rotate 90
    pos (571, 217)
    size (20, 25)
    alpha 0.0
    easeout 1 alpha 1.0

image rects_bn2:
    RectCluster(Solid("#000"), 25, 20, 15).sm
    rotate 90
    pos (700, 217)
    size (20, 25)
    alpha 0.0
    easeout 1 alpha 1.0

image rects_bn3:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    rotate 180
    pos (636, 302)
    size (25, 15)
    alpha 0.0
    easeout 1 alpha 1.0

transform k_scare:
    tinstant(640)
    ease 1.0 zoom 2.0

transform otei_appear(a=0.70,time=1.0):
    i11
    alpha 0.0
    linear time alpha a

transform fade_in(time=1.0):
    alpha 0.0
    ease time alpha 1.0

# kissing animation transform
transform mas_kissing(_zoom, _y,time=2.0):
    i11
    xcenter 640 yoffset 700 yanchor 1.0
    linear time ypos _y zoom _zoom

transform mas_back_from_kissing(time, y):
    linear time xcenter 640 yoffset (y) zoom 0.80

# contains datetime of users's first kiss with monika
# NOTE: need to add this to calendar
default persistent._mas_first_kiss = None

# contains datetime of users's last kiss with monika
default persistent._mas_last_kiss = None

# mas_kissing_motion_base label
# Used to do the kiss motion, it takes care of setting persistent._mas_first_kiss
#
# IN:
#     transition - time in seconds used to transition to the actual kiss and then
#         used for going back to the inital state
#         (Default: 4.0)
#     duration -  time in seconds that the screen stays black
#         (Default: 3.0)
#     hide_ui - boolean indicating if we shoudl hide the ui
#         (Default: True)
#     initial_exp - string indicating the expression Monika will have at the beginning
#         of the animation
#         (Default: 6dubfd)
#     mid_exp - string indicating the expression Monika will have at the middle
#         of the animation, when moving back to the original postion
#         (Default: 6tkbfu)
#     final_exp - string indicating the expression Monika will have at the end
#         of the animation, when she's done getting back to the original position
#         (Default: 6tkbfu)
#     fade_duration - time in seconds spent fading the screen into black
#         (Default: 1.0)
label monika_kissing_motion(transition=4.0, duration=2.0, hide_ui=True,
        initial_exp="6dubfd", mid_exp="6tkbfu", final_exp="6ekbfa", fade_duration=1.0):
    # Note: the hardcoded constants work to give the focus on lips
    # effect these were calculated based on max/min values of the zoom

    if persistent._mas_first_kiss is None:
        $ persistent._mas_first_kiss = datetime.datetime.now()

    $ persistent._mas_last_kiss = datetime.datetime.now()

    window hide
    if hide_ui:
        # hide everything
        $ HKBHideButtons()
        $ mas_RaiseShield_core()
    # reset position to i11
    show monika at i11
    # do the appropriate calculations
    $ _mas_kiss_zoom = 4.9 / mas_sprites.value_zoom
    $ _mas_kiss_y = 2060 - ( 1700  * (mas_sprites.value_zoom - 1.1))
    $ _mas_kiss_y2 = -1320 + (1700 * (mas_sprites.value_zoom - 1.1))

    # start the kiss animation
    $ renpy.show("monika {}".format(initial_exp), [mas_kissing(_mas_kiss_zoom,int(_mas_kiss_y),transition)])
    # show monika 6dubfd at mas_kissing(_mas_kiss_zoom,int(_mas_kiss_y),transition)
    # wait until we're done with the animation
    $ renpy.pause(transition)
    # show black scene
    show black zorder 100 at fade_in(fade_duration)
    # wait half the time to play the sound effect
    $ renpy.pause(duration/2)
    play sound "mod_assets/sounds/effects/kissing.ogg"
    window auto
    "chu~{fast}{w=1}{nw}"
    window hide
    $ renpy.pause(duration/2)
    # hide the black scene
    hide black
    # trasition back which is the best time for non slow back off
    $ renpy.show("monika {}".format(mid_exp),[mas_back_from_kissing(transition,_mas_kiss_y2)])
    pause transition
    $ renpy.show("monika {}".format(final_exp),[i11()])
    show monika with dissolve_monika
    if hide_ui:
        if store.mas_globals.dlg_workflow:
            $ mas_MUINDropShield()
            $ enable_esc()
        else:
            $ mas_DropShield_core()
        $ HKBShowButtons()
    window auto
    return

# short kiss version
label monika_kissing_motion_short:
    call monika_kissing_motion(duration=0.5, initial_exp="6hua", fade_duration=0.5)
    return

# Zoom Transition label
# Used to transition from any valid zoom value to another valid
# zoom valid zoom value in a smooth way
# IN:
#     new_zoom - the new zoom value to move to
#     transition - the time in seconds used to transition to the new zoom level
#         (Default: 3.0)
label monika_zoom_value_transition(new_zoom,transition=3.0):
    if new_zoom == mas_sprites.value_zoom:
        return
    # Sanity checks
    if new_zoom > 2.1:
        $ new_zoom = 2.1
    elif new_zoom < 1.1:
        $ new_zoom = 1.1
    # store the time the transition will take
    $ _mas_transition_time = transition

    # store the old values
    $ _mas_old_zoom = mas_sprites.zoom_level
    $ _mas_old_zoom_value = mas_sprites.value_zoom
    $ _mas_old_y = mas_sprites.adjust_y

    # calculate and store the new values
    $ _mas_new_zoom = ((new_zoom - mas_sprites.default_value_zoom) / mas_sprites.zoom_step ) + mas_sprites.default_zoom_level
    if _mas_new_zoom > mas_sprites.default_value_zoom:
        $ _mas_new_y = mas_sprites.default_y + ((_mas_new_zoom-mas_sprites.default_zoom_level) * mas_sprites.y_step)
    else:
        $ _mas_new_y = mas_sprites.default_y
    $ _mas_new_zoom = ((new_zoom - mas_sprites.default_value_zoom) / mas_sprites.zoom_step ) + mas_sprites.default_zoom_level

    # calculate and store the differences between new and old values
    $ _mas_zoom_diff = _mas_new_zoom - _mas_old_zoom
    $ _mas_zoom_value_diff = new_zoom - _mas_old_zoom_value
    $ _mas_zoom_y_diff = _mas_new_y - _mas_old_y
    # do the transition and pause so it force waits for the transition to end
    show monika at mas_smooth_transition
    $ renpy.pause(transition, hard=True)
    return

# Zoom Transition label #2
# Used to transition from any valid zoom value to another valid
# zoom valid zoom value in a smooth way
# IN:
#     new_zoom - the new zoom level to move to
#     transition - the time in seconds used to transition to the new zoom level
#         (Default: 3.0)
label monika_zoom_fixed_duration_transition(new_zoom,transition=3.0):
    # Sanity checks
    if new_zoom == mas_sprites.zoom_level:
        return
    if new_zoom > 20:
        $ new_zoom = 20
    elif new_zoom < 0:
        $ new_zoom = 0
    # store the time the transition will take
    $ _mas_transition_time = transition

    # store the old values
    $ _mas_old_zoom = mas_sprites.zoom_level
    $ _mas_old_zoom_value = mas_sprites.value_zoom
    $ _mas_old_y = mas_sprites.adjust_y

    # calculate and store the new values
    if new_zoom > mas_sprites.default_zoom_level:
        $ _mas_new_y = mas_sprites.default_y + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.y_step
        )
        $ _mas_new_zoom_value = mas_sprites.default_value_zoom + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.zoom_step
        )
    else:
        $ _mas_new_y = mas_sprites.default_y
        if new_zoom == mas_sprites.default_zoom_level:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom
        else:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom - (
                (mas_sprites.default_zoom_level - new_zoom) * mas_sprites.zoom_step
            )
    # calculate and store the differences between new and old values
    $ _mas_zoom_diff = new_zoom - _mas_old_zoom
    $ _mas_zoom_value_diff = _mas_new_zoom_value - _mas_old_zoom_value
    $ _mas_zoom_y_diff = _mas_new_y - _mas_old_y
    # do the transition and pause so it force waits for the transition to end
    show monika at mas_smooth_transition
    $ renpy.pause(transition, hard=True)
    return

# Zoom Transition label #3
# Used to transition from any valid zoom value to another valid
# zoom valid zoom value in a smooth way
# IN:
#     new_zoom - the new zoom level to move to
#     transition - the time in seconds used to transition from the maximum to the
#         minimum zoom level, this works in a way that the time used in the
#         transition is lower the nearer the current zoom level is to the
#         new zoom level (Default: 3.0)
label monika_zoom_transition(new_zoom,transition=3.0):
    # Sanity checks
    if new_zoom == mas_sprites.zoom_level:
        return
    if new_zoom > 20:
        $ new_zoom = 20
    elif new_zoom < 0:
        $ new_zoom = 0

    # store the old values
    $ _mas_old_zoom = mas_sprites.zoom_level
    $ _mas_old_zoom_value = mas_sprites.value_zoom
    $ _mas_old_y = mas_sprites.adjust_y

    # calculate and store the new values
    if new_zoom > mas_sprites.default_zoom_level:
        $ _mas_new_y = mas_sprites.default_y + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.y_step
        )
        $ _mas_new_zoom_value = mas_sprites.default_value_zoom + (
            (new_zoom - mas_sprites.default_zoom_level) * mas_sprites.zoom_step
        )
    else:
        $ _mas_new_y = mas_sprites.default_y
        if new_zoom == mas_sprites.default_zoom_level:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom
        else:
            $ _mas_new_zoom_value = mas_sprites.default_value_zoom - (
                (mas_sprites.default_zoom_level - new_zoom) * mas_sprites.zoom_step
            )

    # calculate and store the differences between new and old values
    $ _mas_zoom_diff = new_zoom - _mas_old_zoom
    $ _mas_zoom_value_diff = _mas_new_zoom_value - _mas_old_zoom_value
    $ _mas_zoom_y_diff = _mas_new_y - _mas_old_y

    # store the time the transition will take
    $ _mas_transition_time = abs(_mas_zoom_value_diff) * transition

    # do the transition and pause so it force waits for the transition to end
    show monika at mas_smooth_transition
    $ renpy.pause(_mas_transition_time, hard=True)
    return

# Resets to the default zoom level, smoothly.
label monika_zoom_transition_reset(transition=3.0):
    call monika_zoom_transition(store.mas_sprites.default_zoom_level, transition)
    return

init python:
    def zoom_smoothly(trans, st, at):
        """
        Transition function used in mas_smooth_transition
        takes the standard parameters on functions used on transforms
        see https://www.renpy.org/doc/html/atl.html#function-statement
        ASSUMES:
            _mas_old_zoom - containing the old zoom
            _mas_old_zoom_value - containing the old zoom value
            _mas_old_y - containing the old y value
            _mas_zoom_diff - containing the difference between the old and new zoom levels
            _mas_zoom_value_diff - containing the difference between the old and new zoom values
            _mas_zoom_y_diff - containing the difference between the old and new y values
        """
        # check if the transition time is lower than the elapsed time
        if _mas_transition_time > st:
            # do some calcs
            step = st / _mas_transition_time
            mas_sprites.zoom_level = _mas_old_zoom + (step * _mas_zoom_diff)
            mas_sprites.value_zoom = _mas_old_zoom_value + (step * _mas_zoom_value_diff)
            mas_sprites.adjust_y = int(_mas_old_y + (step * _mas_zoom_y_diff))
            if mas_sprites.adjust_y < mas_sprites.default_y:
                mas_sprites.adjust_y = mas_sprites.default_y

            renpy.restart_interaction()
            # to be called as soon as possible we return 0
            return 0.1
        else:
            # get the zoom level and call adjust zoom to be sure it works
            mas_sprites.zoom_level = int(round(mas_sprites.zoom_level))
            mas_sprites.adjust_zoom()
            renpy.restart_interaction()
            # we return None to be able to move to the next statement
            return None

# zoom transition animation transform
transform mas_smooth_transition:
    i11 # this one may not be needed but I keep it just in case
    function zoom_smoothly

# labels to handle the prep and wrap up for timed text events
label mas_timed_text_events_prep:
    python:
        renpy.pause(0.5)

        # raise shield
        mas_RaiseShield_timedtext()

        # store/stop current music and background/sounds
        curr_song = songs.current_track
        play_song(None, 1.0)
        amb_vol = songs.getVolume("backsound")
        renpy.music.set_volume(0.0, 1.0, "background")
        renpy.music.set_volume(0.0, 1.0, "backsound")

        # store and disable auto-forward pref
        afm_pref = renpy.game.preferences.afm_enable
        renpy.game.preferences.afm_enable = False

    return

label mas_timed_text_events_wrapup:
    python:
        renpy.pause(0.5)

        # drop shield
        mas_DropShield_timedtext()

        # restart song/sounds that were playing before event
        if globals().get("curr_song", -1) is not -1 and curr_song != store.songs.FP_MONIKA_LULLABY:
            play_song(curr_song, 1.0)
        else:
            play_song(None, 1.0)

        renpy.music.set_volume(amb_vol, 1.0, "background")
        renpy.music.set_volume(amb_vol, 1.0, "backsound")

        # restor auto-forward pref
        renpy.game.preferences.afm_enable = afm_pref

    return
