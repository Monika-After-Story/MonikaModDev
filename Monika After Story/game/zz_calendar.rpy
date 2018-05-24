# Calendar

init python:

    import math

    class MASCalendar(renpy.Displayable):
        """
        """
        import pygame

        # CONSTANTS
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720


        MOUSE_EVENTS = (
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )


        def __init__(self, child, opaque_distance, transparent_distance, **kwargs):

            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(renpy.Displayable, self).__init__(**kwargs)

            # The child.
            self.calendar_background = renpy.displayable("mod_assets/calendar_bg.png")

            # background tile
            self.background = Solid(
                "#000000B2",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )

            # The distance at which the child will become fully opaque, and
            # where it will become fully transparent. The former must be less
            # than the latter.
            self.opaque_distance = opaque_distance
            self.transparent_distance = transparent_distance

            # The alpha channel of the child.
            self.alpha = 0.0

            # The width and height of us, and our child.
            self.width = 0
            self.height = 0

        def render(self, width, height, st, at):

            back = renpy.render(self.background, width, height, st, at)
            # Create a transform, that can adjust the alpha channel of the
            # child.
            #t = Transform(child=self.child, alpha=self.alpha)

            # Create a render from the child.
            calendar_bg = renpy.render(self.calendar_background, width, height, st, at)

            # Get the size of the child.
            self.width, self.height = calendar_bg.get_size()

            # Create the render we will return.
            render = renpy.Render(width, height)
            render.blit(back,(0,0))
            # Blit (draw) the child's render to our render.
            render.blit(calendar_bg, (192, 103))

            # Return the render.
            return render

        def event(self, ev, x, y, st):

            # Compute the distance between the center of this displayable and
            # the mouse pointer. The mouse pointer is supplied in x and y,
            # relative to the upper-left corner of the displayable.
            distance = math.hypot(x - (self.width / 2), y - (self.height / 2))

            # Base on the distance, figure out an alpha.
            if distance <= self.opaque_distance:
                alpha = 1.0
            elif distance >= self.transparent_distance:
                alpha = 0.0
            else:
                alpha = 1.0 - 1.0 * (distance - self.opaque_distance) / (self.transparent_distance - self.opaque_distance)

            # If the alpha has changed, trigger a redraw event.
            if alpha != self.alpha:
                self.alpha = alpha
                renpy.redraw(self, 0)

            # Pass the event to our child.
            if ev.type in self.MOUSE_EVENTS:
                return "reeee"

            #return self.child.event(ev, x, y, st)

            # otherwise continue
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()

#        def visit(self):
#            return [ self.child ]

screen mas_alpha_magic:

    zorder 51

    add MASCalendar("mod_assets/calendar_bg.png", 100, 200)
        #xalign 0.5
        #yalign 0.5

label mas_start_calendar:

    call screen mas_alpha_magic

    # return value?
    if _return:

        m "got a return value "



    m "Can you find the logo?"

    return
