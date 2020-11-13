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
    m 1eua "Okay!"
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

    m 3eua "Would you like to test another pose?{nw}"
    $ _history_list.pop()
    menu:
        m "Would you like to test another pose?{fast}"

        "Yes.":
            jump dev_hold_still_monika

        "No.":
            return



init python:
    class MASClickZoneTester(MASZoomableInteractable):

        import store.mas_interactions as mib

        def __init__(self):
            self.cz_man = self.mib.MASClickZoneManager()
            self.build_zones()
            self.pose_one = False
            self.debug_back = True
            super(MASClickZoneTester, self).__init__(
                self.cz_man,
                zone_actions=self.build_zone_actions(),
                debug=True
            )

        def quick_add(self, zone_enum):
            self.cz_man.add(
                zone_enum,
                MASClickZone(self.mib.get_vx(zone_enum))
            )

        def build_zones(self):
            self.quick_add(self.mib.ZONE_CHEST)

            self.quick_add(self.mib.ZONE_CHEST_1_R)
            self.cz_man.set_disabled(self.mib.ZONE_CHEST_1_R, True)
            self.quick_add(self.mib.ZONE_CHEST_1_M)
            self.cz_man.set_disabled(self.mib.ZONE_CHEST_1_M, True)
            self.quick_add(self.mib.ZONE_CHEST_1_L)
            self.cz_man.set_disabled(self.mib.ZONE_CHEST_1_L, True)

            self.quick_add(self.mib.ZONE_HEAD)
            
            self.quick_add(self.mib.ZONE_NOSE)

        def build_zone_actions(self):
            return {
                self.mib.ZONE_CHEST: MASZoomableInteractable.ZONE_ACTION_NONE,
                self.mib.ZONE_CHEST_1_R: 
                    MASZoomableInteractable.ZONE_ACTION_NONE,
                self.mib.ZONE_CHEST_1_M: 
                    MASZoomableInteractable.ZONE_ACTION_NONE,
                self.mib.ZONE_CHEST_1_L: 
                    MASZoomableInteractable.ZONE_ACTION_NONE,
                self.mib.ZONE_HEAD: MASZoomableInteractable.ZONE_ACTION_NONE,
                self.mib.ZONE_NOSE: MASZoomableInteractable.ZONE_ACTION_NONE,
            }

        def render(self, width, height, st, at):
            return super(MASClickZoneTester, self).render(width, height, st, at)

        def event(self, ev, x, y, st):
            if ev.type == pygame.KEYUP:

                if ev.key == pygame.K_q:
                    # quit when user hits q
                    return True

                if ev.key == pygame.K_DOWN:
                    if store.mas_sprites.zoom_level > 0:
                        store.mas_sprites.zoom_level -= 1
                        store.mas_sprites.adjust_zoom()
                        self.adjust_for_zoom()
                        renpy.redraw(self, 0.0)
                        renpy.restart_interaction()

                elif ev.key == pygame.K_UP:
                    if store.mas_sprites.zoom_level < 20:
                        store.mas_sprites.zoom_level += 1
                        store.mas_sprites.adjust_zoom()
                        self.adjust_for_zoom()
                        renpy.redraw(self, 0.0)
                        renpy.restart_interaction()

                elif ev.key == pygame.K_p:
                    # switch pose
                    if self.pose_one:
                        self.pose_one = False
                        self.enable_zone(self.mib.ZONE_CHEST)
                        self.disable_zone(self.mib.ZONE_CHEST_1_R)
                        self.disable_zone(self.mib.ZONE_CHEST_1_M)
                        self.disable_zone(self.mib.ZONE_CHEST_1_L)
                        renpy.redraw(self, 0.0)
                        renpy.show("monika 6eua")
                        renpy.restart_interaction()

                    else:
                        self.pose_one = True
                        self.disable_zone(self.mib.ZONE_CHEST)
                        self.enable_zone(self.mib.ZONE_CHEST_1_R)
                        self.enable_zone(self.mib.ZONE_CHEST_1_M)
                        self.enable_zone(self.mib.ZONE_CHEST_1_L)

                        renpy.redraw(self, 0.0)
                        renpy.show("monika 1eua")
                        renpy.restart_interaction()

                elif ev.key == pygame.K_d:
                    # toggle debug backs
                    self.debug_back = not self.debug_back
                    self._cz_man._debug(self.debug_back)
                    renpy.redraw(self, 0.0)

            else:
                if self.event_begin(ev, x, y, st):
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
    $ dbg_out = MASClickZoneTester()
    $ ui.add(dbg_out)
    $ ui.interact()
    window auto
    m 1eua "I am done"
    return
