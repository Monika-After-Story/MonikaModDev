# This file is meant to store any special effects.
# These can be some images or transforms.
init -500 python in mas_parallax:
    import math
    import collections
    import pygame

    import store

    class ParallaxDecal(renpy.display.core.Displayable):
        """
        Represents a decal, intended to be used with ParallaxSprite,
        may work not as expected in other cases.
        """
        def __init__(self, img, x=0, y=0, z=0, on_click=None):
            """
            Constructor for decals

            IN:
                img - the img/disp for this decal
                x - the x offset in the container
                    (Default: 0)
                y - the y offset in the container
                    (Default: 0)
                z - basically zorder
                    (Default: 0)
                on_click - a callable to call on click events, or just a non-None value to return
                    (Default: None)
            """
            super(ParallaxDecal, self).__init__()

            self.img = renpy.easy.displayable(img)
            self._x = x
            self._y = y
            self._z = z
            self.on_click = on_click
            self.callback = None

            # width, height, at offset
            self._last_render_params = (0, 0, 0.0)

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
            return "<{0}: (img: {1}, x: {2}, y: {3}, z: {4})>".format(
                type(self).__name__,
                repr(self.img),
                self._x,
                self._y,
                self._z
            )

        def event(self, ev, x, y, st):
            """
            The event handler
            """
            # Check for left mouse button click
            if ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                # if self.is_focused():
                # NOTE: In the latest renpy keeping references to renders causes leaks.
                # The focus system is slow and doesn't allow to use button displayables along with parallax sprites.
                # So we'll just get the last render with `renpy.render`, that should be reliable since
                # `render` is called before `event`. Also renpy does something similar internally, too.
                w, h, at_offset = self._last_render_params
                last_render = renpy.render(
                    self,
                    w,
                    h,
                    st,
                    st + at_offset
                )
                if last_render.is_pixel_opaque(x, y):
                    if callable(self.on_click):
                        return self.on_click()

                    return self.on_click

            return None

        def render(self, width, height, st, at):
            """
            The render method
            """
            img_surf = renpy.render(self.img, width, height, st, at)
            render = renpy.Render(img_surf.width, img_surf.height)
            render.blit(img_surf, (0, 0))
            # render.add_focus(self, None, 0, 0, img_surf.width, img_surf.height, 0, 0, render)

            self._last_render_params = (render.width, render.height, at-st)

            return render

        def visit(self):
            """
            Returns the img for prediction
            """
            return [self.img]


    class _ParallaxDecalContainer(renpy.display.core.Displayable):
        """
        A container displayable. It takes a base (consider it main displayable) and any number of children.
        The container will be of just enough size to contain the base and the children.
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
                    raise ValueError("{0} can accept only ParallaxDecal, got: {1}".format(type(self).__name__, type(decal).__name__))
                decal.callback = self.update

            self.offsets = (0, 0)
            self.size = (0, 0)
            self._debug = False

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
            # Is not here because instance checks are mandatory
            return [decal for decal in self._decals if decal is not self._base]

        @property
        def debug(self):
            return self._debug

        @debug.setter
        def debug(self, value):
            self._debug = value
            renpy.redraw(self, 0.0)

        def __repr__(self):
            """
            Representation of this object
            """
            return "<{0}: (base: {1}, children: {2})>".format(
                type(self).__name__,
                repr(self._base),
                self.children
            )

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
                    self._decals.remove(decal)
                    decal.callback = None

            renpy.redraw(self, 0.0)

        def remove_all(self):
            """
            Removes all decals from this container
            """
            for child in self.children:
                self._decals.remove(child)
                child.callback = None

            renpy.redraw(self, 0.0)

        def event(self, ev, x, y, st):
            """
            The event handler for this container,
            propagates events to its children
            """
            for i in range(len(self._decals)-1, -1, -1):
                decal = self._decals[i]
                rv = decal.event(ev, x + self.offsets[0] - decal.x, y + self.offsets[1] - decal.y, st)
                if rv is not None:
                    return rv

            return None

        def render(self, width, height, st, at):
            """
            The render method where we do the meth logic to align everything properly
            """
            min_blit_x = 0
            min_blit_y = 0
            render_width = 0
            render_height = 0
            render_items = list()

            for decal in self._decals:
                decal_surf = renpy.render(decal, width, height, st, at)

                min_blit_x = min(min_blit_x, decal.x)
                min_blit_y = min(min_blit_y, decal.y)

                render_width = max(render_width, decal_surf.width + decal.x)
                render_height = max(render_height, decal_surf.height + decal.y)

                render_items.append((decal_surf, decal.x, decal.y))

            base_blit_x = abs(min_blit_x)
            base_blit_y = abs(min_blit_y)

            render_width += base_blit_x
            render_height += base_blit_y

            render = renpy.Render(render_width, render_height)
            for surf, blit_x, blit_y in render_items:
                render.blit(surf, (base_blit_x + blit_x, base_blit_y + blit_y))

            self.size = (render_width, render_height)
            self.offsets = (min_blit_x, min_blit_y)
            if self._debug:
                canvas = render.canvas()
                canvas.rect("#cd0202", (0, 0, render_width-1, render_height-1), width=1)

            return render

        def _update_offsets(self):
            """
            HACK: Runs the render method and updates offsets,
            this is terrible, but has to be done. Blame RenPy.
            """
            self.render(renpy.config.screen_width, renpy.config.screen_height, 0, 0)

        def update(self):
            """
            Updates this disp
            """
            self.__sort_decals()
            renpy.redraw(self, 0.0)

        def visit(self):
            """
            Returns images of this disp for prediction
            """
            return [decal for decal in self._decals]


    class ParallaxSprite(renpy.display.core.Displayable):
        """
        Represents a sprite with parallax effect
        """
        NORMAL_ZOOM = 1.0

        __RED_DOT = store.Solid("#cd0202", xsize=1, ysize=1)
        __GREEN_DOT = store.Solid("#66ff21", xsize=1, ysize=1)

        def __init__(self, img, x, y, z, function=None, decals=(), on_click=None, min_zoom=1.0, max_zoom=4.0):
            """
            Constructor for parallax sprites

            IN:
                img - path to the img/Displayable
                x - the sprite x pos on the screen
                y - the sprite y pos on the screen
                z - the sprite z pos
                    NOTE: treat this as zorder, it also determines the maximum amount of parallax effect
                    NOTE: MUST BE > 0
                function - a function for the sprite's transform,
                    use it if you need additional effects
                    (Default: None)
                decals - list of decals for this sprite
                    (Default: empty tuple)
                on_click - if it's a callable object, it'll be called on click (LMB) events,
                    otherwise it'll be returned on those events
                    (Default: None)
                min_zoom - min zoom value
                    (Default: 1.0)
                max_zoom - max zoom value
                    (Default: 4.0)
                    NOTE: if min_zoom == max_zoom, the user won't be able to zoom in/out
            """
            super(ParallaxSprite, self).__init__()

            # Current parallax effect offsets
            self._xoffset = 0.0
            self._yoffset = 0.0

            # This is used for debugging, displays last pos
            self._debug = False
            self._prev_parallax_offsets = None
            self._prev_transform_offsets = None

            # For convenience, we assume the mouse is in the center
            self._mouse_x = 0
            self._mouse_y = 0
            self.reset_mouse_pos()

            # Sprite pos
            self._x = x
            self._y = y
            if z < 1:
                raise ValueError(
                    "{} zorder property must be greater than 0.".format(
                        type(self).__name__
                    )
                )
            self._z = z

            self._container = _ParallaxDecalContainer(
                ParallaxDecal(img, 0, 0, 0, on_click=on_click),
                *decals
            )

            self._transform = store.Transform(
                self._container,
                function=function,
                rotate_pad=True,
                transform_anchor=True,
                subpixel=True
            )
            # Might be useful to have a reference to the sprite from the transform function
            self._transform.__parallax_sprite__ = self
            # Renpy doesn't define this attr in __init__ for some reason...
            self._transform.render_size = (0, 0)
            # renpy.display.render.Matrix2D
            # Used to convert screen coords into disp coords
            self._forward_matrix = None

            # Set up zoom
            self.min_zoom = min_zoom
            self.max_zoom = max_zoom
            self._zoom = min_zoom
            # Set this again to run the callback
            self.zoom = min_zoom

            # Are we listening for events?
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
            self.update_offsets()

        @property
        def decals(self):
            return self._container.children

        @property
        def debug(self):
            return self._debug

        @debug.setter
        def debug(self, value):
            if self._debug == value:
                return

            # If we enable debug mode, create new queues
            if value:
                self._prev_parallax_offsets = collections.deque(maxlen=50)
                self._prev_transform_offsets = collections.deque(maxlen=50)

            # Otherwise clear the queues and set to None
            else:
                self._prev_parallax_offsets.clear()
                self._prev_parallax_offsets = None
                self._prev_transform_offsets.clear()
                self._prev_transform_offsets = None

            self._debug = value

        def __repr__(self):
            """
            Representation of this object
            """
            return "<{0}: (img: {1}, x: {2}, y: {3}, z: {4}, decals: {5})>".format(
                type(self).__name__,
                repr(self._container.base.img),
                self._x,
                self._y,
                self._z,
                self.decals
            )

        def update_mouse_pos(self):
            """
            Updates mouse pos
            """
            self._mouse_x, self._mouse_y = renpy.get_mouse_pos()

        def reset_mouse_pos(self):
            """
            Resets mouse pos
            """
            self._mouse_x = int(renpy.config.screen_width / 2.0)
            self._mouse_y = int(renpy.config.screen_height / 2.0)

        def toggle_events(self, value):
            """
            Toggles events (and hence the parallax effect)

            IN:
                value - the value to set
            """
            self._enable_events = value

        def add_decals(self, *decals):
            """
            Adds decals to this sprite

            IN:
                decals - ParallaxDecal objects
            """
            self._container.add(*decals)

        def remove_decals(self, *decals):
            """
            Removes decals from this sprite

            IN:
                decals - ParallaxDecal objects
            """
            self._container.remove(*decals)

        def clear_decals(self):
            """
            Removes all decals from this sprite
            """
            self._container.remove_all()

        def __get_transform_placement(self):
            """
            Returns placement of the transform according
            to renpy placement algo

            OUT:
                tuple of 2 items
            """
            return renpy.display.core.place(
                renpy.config.screen_width,
                renpy.config.screen_height,
                *self._transform.render_size,
                placement=self._transform.get_placement()
            )

        def update_offsets(self):
            """
            Updates the offsets of this parallax sprite
            """
            screen_width = renpy.config.screen_width
            screen_height = renpy.config.screen_height

            # Basically how much zoom is currently going on
            zoom_factor = abs(self._zoom - ParallaxSprite.NORMAL_ZOOM)

            # We use screen_width and screen_height for our parallax
            # determines how far away from center can the parallax shift be
            available_x_shift = screen_width / float(self._z)
            available_y_shift = screen_height / float(self._z)

            half_screen_width = screen_width / 2.0
            half_screen_height = screen_height / 2.0

            # Normalize the mouse position with the center of the screen
            # 1.0 - left / top
            # 0.0 - center
            # -1.0 - right / bottom
            mouse_x_factor = 1.0 - self._mouse_x / half_screen_width
            mouse_y_factor = 1.0 - self._mouse_y / half_screen_height

            # Offsets from the container
            container_offset_x = abs(self._container.offsets[0])
            container_offset_y = abs(self._container.offsets[1])

            # Offsets from the transform. That's so if the sprite has a custom func
            # for its transform which modifies these params, we don't have to
            # account for zoom level in the func, instead we do it here for convenience.
            transform_offset_x, transform_offset_y = self.__get_transform_placement()

            # Our offsets consist of 5 parts:
            # - base coords give offsets to x and y (depend on zoom level)
            # - shift from the parallax effect (depends on mouse pos)
            # - correction to the zoom effect (depends on mouse pos)
            # - offsets from the container (depend on zoom level)
            # - offsets from the transfrom xpos, ypos, xanchor, yanchor (depend on zoom level)
            new_xoffset = (
                self._x*(1.0 + zoom_factor)
                + available_x_shift*mouse_x_factor
                - zoom_factor*self._mouse_x
                - container_offset_x*(1.0 + zoom_factor)
                + transform_offset_x*zoom_factor
            )
            new_yoffset = (
                self._y*(1.0 + zoom_factor)
                + available_y_shift*mouse_y_factor
                - zoom_factor*self._mouse_y
                - container_offset_y*(1.0 + zoom_factor)
                + transform_offset_y*zoom_factor
            )

            if new_xoffset != self._xoffset or new_yoffset != self._yoffset:
                self._xoffset = new_xoffset
                self._yoffset = new_yoffset
                # Now update the displayable
                renpy.redraw(self, 0.0)

        def event(self, ev, x, y, st):
            """
            The event handler
            TODO: allow to move around and zoom in/out with keyboard
            """
            if self._enable_events:
                if ev.type == pygame.MOUSEMOTION:
                    self.update_mouse_pos()
                    self.update_offsets()
                    return None

                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if self.min_zoom != self.max_zoom:
                        # Check for mouse wheel scrolling up
                        if ev.button == 4:
                            self.zoom += 0.1
                        # Check for mouse wheel scrolling down
                        elif ev.button == 5:
                            self.zoom -= 0.1

                    return None

                elif ev.type == pygame.MOUSEBUTTONUP:
                    # Check for left mouse button click
                    if ev.button == 1:
                        # Transform ev coords
                        transform_offset_x, transform_offset_y = self.__get_transform_placement()
                        real_x, real_y = self._forward_matrix.transform(x - self._xoffset - transform_offset_x, y - self._yoffset - transform_offset_y)
                        # Optimisazation: only propagate the event if it's withing the image
                        x_size, y_size = self._transform.render_size
                        if 0 <= real_x <= x_size and 0 <= real_y <= y_size:
                            return self._transform.event(ev, real_x, real_y, st)

                    return None

            if store._mas_root.is_dm_enabled():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_v:
                    self.debug = not self.debug
                    self._container.debug = not self._container.debug

            return None

        def __debug_info_render(self, width, height, st, at, render):
            """
            Renders debug info on a render. This is slow,
            but it's only for debugging (obviously)

            IN:
                width - render width
                height - render height
                st - current st
                at - current at
                render - the render to render onto

            ASSUMES:
                Debug mode is on
            """
            threshold = 1.0

            # Only add the new offset, if it's changed since last time
            if self._prev_parallax_offsets:
                last_x_offset, last_y_offset = self._prev_parallax_offsets[-1]
                if (
                    abs(last_x_offset - self._xoffset) >= threshold
                    or abs(last_y_offset - self._yoffset) >= threshold
                ):
                    self._prev_parallax_offsets.append((self._xoffset, self._yoffset))

            else:
                self._prev_parallax_offsets.append((self._xoffset, self._yoffset))

            red_point_surf = renpy.render(self.__RED_DOT, width, height, st, at)
            for x_offset, y_offset in self._prev_parallax_offsets:
                blit_coords = (x_offset, y_offset)
                render.subpixel_blit(
                    red_point_surf,
                    blit_coords
                )

            # Same logic here
            transform_x_offset, transform_y_offset = self.__get_transform_placement()
            if self._prev_transform_offsets:
                last_transform_x_offset, last_transform_y_offset = self._prev_transform_offsets[-1]
                if (
                    abs(last_transform_x_offset - transform_x_offset) >= threshold
                    or abs(last_transform_y_offset - transform_y_offset) >= threshold
                ):
                    self._prev_transform_offsets.append((transform_x_offset, transform_y_offset))

            else:
                self._prev_transform_offsets.append((transform_x_offset, transform_y_offset))

            green_point_surf = renpy.render(self.__GREEN_DOT, width, height, st, at)
            for transform_x_offset, transform_y_offset in self._prev_transform_offsets:
                blit_coords = (self._xoffset + transform_x_offset, self._yoffset + transform_y_offset)
                render.subpixel_blit(
                    green_point_surf,
                    blit_coords
                )

            # We want redraw asap in this case
            renpy.redraw(self, 0.1)

        def render(self, width, height, st, at):
            """
            The render method
            """
            img_surf = renpy.render(self._transform, width, height, st, at)
            # NOTE: This has to do full size screen render + use place
            render = renpy.Render(width, height)
            render.place(self._transform, x=self._xoffset, y=self._yoffset, render=img_surf)

            # Add debug info if needed
            if self._debug:
                self.__debug_info_render(width, height, st, at, render)

            # Set zoom
            render.zoom(self._zoom, self._zoom)
            # Same the matrix for events
            self._forward_matrix = render.forward
            # self._reverse_matrix = render.reverse

            return render

        def visit(self):
            """
            Returns the transform for prediction

            OUT:
                list with the disp to predict
            """
            return [self._transform]

        def predict_one(self):
            """
            Called to ask this displayable to call the callback with all
            the images it may want to load.
            """
            if self._enable_events:
                self.update_mouse_pos()
            self._container._update_offsets()
            self.update_offsets()


    class ParallaxBackground(renpy.display.core.Displayable):
        """
        A more optimised version of RenPy's Composite.
        Intended to be used when you need multiple ParallaxSprite on the screen.
        """
        def __init__(self, *children):
            """
            Constructor for parallax background

            IN:
                children - ParallaxSprite objects for this background to compose together,
                    but technically can be any displayables (for example if you need something static)
            """
            super(ParallaxBackground, self).__init__()

            self.children = list(children)

        def add(self, sprite):
            """
            Adds a sprite to this background

            IN:
                sprite - perhaps a ParallaxSprite or other kind of displayable
            """
            self.children.append(sprite)

        def insert(self, index, sprite):
            """
            Inserts a sprite in this background

            IN:
                index - the index to insert at
                sprite - the sprite to insert

            ASSUMES:
                the index exists
            """
            self.children.insert(index, sprite)

        def remove(self, sprite):
            """
            Removes a sprite from this background

            IN:
                sprite - the sprite to remove

            ASSUMES:
                the sprite IS in the background
            """
            self.children.remove(sprite)

        def event(self, ev, x, y, st):
            """
            The event handler
            """
            for i in range(len(self.children)-1, -1, -1):
                child = self.children[i]
                rv = child.event(ev, x, y, st)

                if rv is not None:
                    return rv

            return None

        def render(self, width, height, st, at):
            """
            The render method
            """
            render = renpy.Render(width, height)

            for child in self.children:
                render.blit(
                    renpy.render(child, width, height, st, at),
                    (0, 0)
                )

            return render

        def visit(self):
            """
            Returns the children for prediction

            OUT:
                list of ParallaxSprite
            """
            return [child for child in self.children]


init -500 python:
    import random
    import math

    # Backported from DDLC, used in splash screen
    class ParticleBurst(object):
        def __init__(self, theDisplayable, explodeTime=0, numParticles=20, particleTime = 0.500, particleXSpeed = 3, particleYSpeed = 5):
            self.sm = SpriteManager(update=self.update)

            self.stars = [ ]
            self.displayable = theDisplayable
            self.explodeTime = explodeTime
            self.numParticles = numParticles
            self.particleTime = particleTime
            self.particleXSpeed = particleXSpeed
            self.particleYSpeed = particleYSpeed
            self.gravity = 240
            self.timePassed = 0

            for i in range(self.numParticles):
                self.add(self.displayable, 1)

        def add(self, d, speed):
            s = self.sm.create(d)
            speed = random.random()
            angle = random.random() * 3.14159 * 2
            xSpeed = speed * math.cos(angle) * self.particleXSpeed
            ySpeed = speed * math.sin(angle) * self.particleYSpeed - 1
            s.x = xSpeed * 24
            s.y = ySpeed * 24
            pTime = self.particleTime
            self.stars.append((s, ySpeed, xSpeed, pTime))

        def update(self, st):
            sindex=0
            for s, ySpeed, xSpeed, particleTime in self.stars:
                if (st < particleTime):
                    s.x = xSpeed * 120 * (st + .20)
                    s.y = (ySpeed * 120 * (st + .20) + (self.gravity * st * st))
                else:
                    s.destroy()
                    self.stars.pop(sindex)
                sindex += 1
            return 0



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
# Requires enam+ affection
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
label monika_kissing_motion(
    transition=4.0,
    duration=2.0,
    hide_ui=True,
    initial_exp="6dubfd",
    mid_exp="6tkbfu",
    final_exp="6ekbfa",
    fade_duration=1.0
):
    if not mas_isMoniEnamored(higher=True):
        return
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
# Default duration 0.5
# Default init exp 6hua
label monika_kissing_motion_short(**kwargs):
    python:
        kwargs.setdefault("duration", 0.5)
        kwargs.setdefault("fade_duration", 0.5)
        kwargs.setdefault("initial_exp", "6hua")
    call monika_kissing_motion(**kwargs)
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
        mas_play_song(None, 1.0)
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
        if globals().get("curr_song", -1) != -1 and curr_song != store.songs.FP_MONIKA_LULLABY:
            mas_play_song(curr_song, 1.0)
        else:
            mas_play_song(None, 1.0)

        renpy.music.set_volume(amb_vol, 1.0, "background")
        renpy.music.set_volume(amb_vol, 1.0, "backsound")

        # restor auto-forward pref
        renpy.game.preferences.afm_enable = afm_pref

    return
