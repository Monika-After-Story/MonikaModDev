# module that adds a tiny mouse tracker overlay

init -1 python:
    
    # quick functions to enable disable the mouse tracker
    def mas_enableMouseTracking():
        if not mas_isMouseTrackingVisible():
            config.overlay_screens.append("dev_mouseoverlay")


    def mas_disableMouseTracking():
        if mas_isMouseTrackingVisible():
            config.overlay_screens.remove("dev_mouseoverlay")
            renpy.hide_screen("dev_mouseoverlay")


    def mas_isMouseTrackingVisible():
        return "dev_mouseoverlay" in config.overlay_screens


    class MASMouseTracker(renpy.Displayable):
        """
        Custom mouse tracker displayable
        """
        import pygame

        def __init__(self):
            super(MASMouseTracker, self).__init__()
            self.mouse_x, self.mouse_y = renpy.get_mouse_pos()


        def event(self, ev, x, y, st):
            if ev.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = renpy.get_mouse_pos()
                renpy.redraw(self, 0)


        def render(self, width, height, st, at):

            # render the mouse text
            mouse_text = renpy.render(
                Text(
                    "({0}, {1})".format(self.mouse_x, self.mouse_y),
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#FFF"
                ),
                width, height, st, at
            )
            mtw, mth = mouse_text.get_size()

            # blit the mouse text
            r = renpy.Render(mtw, mth)
            r.blit(mouse_text, (0, 0))
            return r


    class MASRenderInfo(renpy.Displayable):
        """
        custom screen that shows render information
        """
        import pygame

        def __init__(self):
            super(MASRenderInfo, self).__init__()
            self._last_event = "None"
            self._last_event_name = "None"


        def event(self, ev, x, y, st):
            self._last_event = str(ev.type)
            self._last_event_name = pygame.event.event_name(ev.type)
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_q:
                # quit when user hits q
                return True


        def render(self, width, height, st, at):

            # render information
            info_text = renpy.render(
                Text(
                    "w: {0} | h: {1} | s: {2} | a: {3} | e: {4} / {5}".format(
                        width, height, st, at, self._last_event, self._last_event_name
                    ),
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#FFF"
                ),
                width, height, st, at
            )

            # blit this text top left
            r = renpy.Render(width, height)
            r.blit(info_text, (0, 0))

            # constant render
            renpy.redraw(self, 0)
            return r


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_mouse_tracker",
            category=["dev"],
            prompt="TOGGLE MOUSE TRACKING",
            pool=True,
            unlocked=True
        )
    )


label dev_mouse_tracker:
    if mas_isMouseTrackingVisible():
        m "I disable mouse tracker now."
        $ mas_disableMouseTracking()

    else:
        m "I enable mouse tracker now."
        $ mas_enableMouseTracking()


screen dev_mouseoverlay():
    zorder 100
    fixed:
        area (440, 0, 400, 35)
        add MASMouseTracker():
            xalign 0.5

#    python:
#        mouse_xpos, mouse_ypos = renpy.get_mouse_pos()
#
#    zorder 100
#    fixed:
#        area (440, 0, 400, 35)
#        text "([mouse_xpos], [mouse_ypos])":
#            size 14
#            font gui.default_font
#            color "#FFF"
#            xalign 0.5
#





init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_render_screen_info",
            category=["dev"],
            prompt="SHOW CUSTOM SCREEN RENDER INFO",
            pool=True,
            unlocked=True
        )
    )

label dev_render_screen_info:
    m 1eua "I will show a custom screen now."
    $ ui.add(MASRenderInfo())
    $ nothing = ui.interact()
    m "okay done!"
    return

