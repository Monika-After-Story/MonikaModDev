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
    return


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


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_hold_still_monika",
            category=["dev"],
            prompt="HAVE MONIKA HOLD STILL",
            pool=True,
            unlocked=True
        )
    )

label dev_hold_still_monika:
    m 1eua "okay!"
    $ sel_pose = renpy.input("pose number (1-7)", allow="1234567", length=1)
    $ sel_pose = store.mas_utils.tryparseint(sel_pose, 1)
    if sel_pose < 1:
        $ sel_pose = 1
    elif sel_pose > 7:
        $ sel_pose = 7
    
    $ pose_to_make = str(sel_pose) + "eua"
    $ renpy.show("monika " + pose_to_make)
    m "HOLDING! (Click once to dismiss menu, once more to stop holding)"
    $ ui.add(PauseDisplayable())
    $ ui.interact()

    m 1eua "Done holding!"
    return

init python:
    class MASClickZoneTester(renpy.Displayable):

        import store.mas_interactions as mib

        def __init__(self):
            super(renpy.Displayable, self).__init__()
            self.chest = self.mib.ZONE_CHEST
            self.build_zones()

        def build_zones(self):
            zoom_level = store.mas_sprites.zoom_level

            self.boob_click = MASClickZone(
                self.mib.vertex_list_from_zoom(zoom_level, self.chest)
            )
            self.boob_click._debug_back = True
            self.boob_click._button_down = pygame.MOUSEBUTTONDOWN

            self.nose_click = MASClickZone(
                self.mib.vertex_list_from_zoom(zoom_level, self.mib.ZONE_NOSE)
            )
            self.nose_click._debug_back = True
            self.nose_click._button_down = pygame.MOUSEBUTTONDOWN

            self.head_click = MASClickZone(
                self.mib.vertex_list_from_zoom(zoom_level, self.mib.ZONE_HEAD)
            )
            self.head_click._debug_back = True
            self.head_click._button_down = pygame.MOUSEBUTTONDOWN


        def render(self, width, height, st, at):
            r = renpy.Render(width, height)
            boob_zone = renpy.render(self.boob_click, width, height, st, at)
            nose_zone = renpy.render(self.nose_click, width, height, st, at)
            head_zone = renpy.render(self.head_click, width, height, st, at)
            r.blit(boob_zone, (0, 0))
            r.blit(nose_zone, (0, 0))
            r.blit(head_zone, (0, 0))
            return r

        def event(self, ev, x, y, st):
            if ev.type == pygame.KEYUP: 

                if ev.key == pygame.K_q:
                    # quit when user hits q
                    return True

                if ev.key == pygame.K_DOWN:
                    if store.mas_sprites.zoom_level > 0:
                        store.mas_sprites.zoom_level -= 1
                        store.mas_sprites.adjust_zoom()
                        self.build_zones()
                        renpy.redraw(self, 0.0)
                        renpy.restart_interaction()

                elif ev.key == pygame.K_UP:
                    if store.mas_sprites.zoom_level < 20:
                        store.mas_sprites.zoom_level += 1
                        store.mas_sprites.adjust_zoom()
                        self.build_zones()
                        renpy.redraw(self, 0.0)
                        renpy.restart_interaction()

                elif ev.key == pygame.K_p:
                    # switch pose
                    if self.chest == self.mib.ZONE_CHEST:
                        self.chest = self.mib.ZONE_CHEST_1
                        self.build_zones()
                        renpy.redraw(self, 0.0)
                        renpy.show("monika 1eua")
                        renpy.restart_interaction()

                    else:
                        self.chest = self.mib.ZONE_CHEST
                        self.build_zones()
                        renpy.redraw(self, 0.0)
                        renpy.show("monika 6eua")
                        renpy.restart_interaction()

            else:
                boob_click = self.boob_click.event(ev, x, y, st)
                nose_click = self.nose_click.event(ev, x, y, st)
                head_click = self.head_click.event(ev, x, y, st)
                if (
                        boob_click is not None
                        or nose_click is not None
                        or head_click is not None
                ):
                    renpy.play(gui.activate_sound, channel="sound")



init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_clickzone_tests",
            category=["dev"],
            prompt="CLICKZONE TEST",
            pool=True,
            unlocked=True
        )
    )

label dev_clickzone_tests:

    m 1eua "I am reset zoom"
    $ store.mas_sprites.reset_zoom()
    m 6eua "ok, remember q is quit"
    window hide
    $ ui.add(MASClickZoneTester())
    $ ui.interact()
    window auto
    m 1eua "I am done"
    return
