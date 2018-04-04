# enabling unstable mode
default persistent._mas_unstable_mode = False
define mas_updater.regular = "http://updates.monikaafterstory.com/updates.json"
define mas_updater.unstable = "http://unstable.monikaafterstory.com/updates.json"
define mas_updater.force = False
define mas_updater.timeout = 10 # timeout default

init -1 python:
    # custom displayable for the updater screen
    class MASUpdaterDisplayable(renpy.Displayable):
        # this displayable will handle UpdateVersion on its own while enabling
        # interactions
        # since UpdateVersion occurs in a background thread, we want to 
        # handle most logic in the render function, despite the 
        # event-driven framework
        # we will return -1 upon cancel / ok
        # 1 upon update

        import pygame # mouse stuff
        import time # for timeouts
       
        # CONSTANTS
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        BUTTON_BOT_SPACE = 50
        BUTTON_SPACING = 10

        FRAME_WIDTH = 500
        FRAME_HEIGHT = 250

        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        TEXT_YOFFSET = -15

        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )

        TIMEOUT = 10 # 10 seconds

        # STATES

        # checknig for an update. This should also be the inital state
        # update button disabled, cancel button clickable
        STATE_CHECKING = 0

        # update found
        # we found an update.
        # update and cancel enabled
        STATE_BEHIND = 1

        # no update found
        # we are at the current verison
        # update and cancel hidden, ok button is shown and enabled
        STATE_UPDATED = 2

        # timeout
        # we timed out.
        # Update button becomes try again and is enabled. Cancel button enabled
        STATE_TIMEOUT = 3

        def __init__(self, update_link):
            """
            Constructor
            """
            super(renpy.Displayable, self).__init__()

            self.update_link = update_link

            # background tile
            # hangman frame color (50% trans)
            self.background = Solid(
                "#FFE6F47F", 
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )

            # confirm screen (black, 70%)
            self.confirm = Solid(
                "#000000B2",
                xsize=self.FRAME_WIDTH,
                ysize=self.FRAME_HEIGHT
            )

            # button backs
            button_idle = Image("mod_assets/hkb_idle_background.png")
            button_hover = Image("mod_assets/hkb_hover_background.png")
            button_disabled = Image("mod_assets/hkb_disabled_background.png")

            # ok button text
            button_text_ok_idle = Text(
                "Ok",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_ok_hover = Text(
                "Ok",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # cancel button text
            button_text_cancel_idle = Text(
                "Cancel",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_cancel_hover = Text(
                "Cancel",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # update button text
            button_text_update_idle = Text(
                "Update",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_update_hover = Text(
                "Update",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # retry button text
            button_text_retry_idle = Text(
                "Retry",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_retry_hover = Text(
                "Retry",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # calculate positions
            # top left x, y
            self._confirm_x = int((self.VIEW_WIDTH - self.FRAME_WIDTH) / 2)
            self._confirm_y = int((self.VIEW_HEIGHT - self.FRAME_HEIGHT) / 2)

            # top left, center button x y
            button_center_x = (
                int((self.VIEW_WIDTH - self.BUTTON_WIDTH) / 2) +
                self._confirm_x
            )
            button_center_y = (
                (self._confirm_y + self.FRAME_HEIGHT) - 
                self.BUTTON_BOT_SPACE
            )

            # top left, left button x y
            button_left_x = (
                int(
                    (
                        self.FRAME_WIDTH - 
                        (
                            (2 * self.BUTTON_WIDTH) +
                            self.BUTTON_SPACING
                        )
                    ) / 2
                ) +
                self._confirm_x
            )
            button_left_y = button_center_y

            # create the buttons
            self._button_ok = MASButtonDisplayable(
                button_text_ok_idle,
                button_text_ok_hover,
                button_text_ok_idle,
                button_idle,
                button_hover,
                button_idle,
                button_center_x,
                button_center_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            self._button_cancel = MASButtonDisplayable(
                button_text_cancel_idle,
                button_text_cancel_hover,
                button_text_cancel_idle,
                button_idle,
                button_hover,
                button_idle,
                button_left_x + self.BUTTON_WIDTH + self.BUTTON_SPACING,
                button_left_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            self._button_update = MASButtonDisplayable(
                button_text_update_idle,
                button_text_update_hover,
                button_text_update_idle,
                button_idle,
                button_hover,
                button_disabled,
                button_left_x,
                button_left_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            self._button_retry = MASButtonDisplayable(
                button_text_retry_idle,
                button_text_retry_hover,
                button_text_retry_idle,
                button_idle,
                button_hover,
                button_disabled,
                button_left_x,
                button_left_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            # confirm text
            self._text_checking = Text(
                "Checking for updates...",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_update = Text(
                "New update available!",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_noupdate = Text(
                "No update found.",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self._text_timeout = Text(
                "Connection timed out.",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )

            # grouped buttons
            self._checking_buttons = [
                self._button_update,
                self._button_cancel
            ]
            self._behind_buttons = self._checking_buttons
            self._updated_buttons = [self._button_ok]
            self._timeout_buttons = [
                self._button_retry,
                self._button_cancel
            ]

            # inital state
            self._state = self.STATE_CHECKING

            # inital button states
            self._button_update.disable()

            # inital time 
            self._prev_time = time.time()


        def _checkUpdate(self):
            """
            Does the purely logical update checking
            This will set the appropriate states
            """

            if self._state == self.STATE_CHECKING:
                # checking for updates
                
                if time.time() - self._prev_time > self.TIMEOUT:
                    # we've timed out!
                    self._state = self.STATE_TIMEOUT
                    return

                # check for new version
                latest_version = updater.UpdateVersion(
                    self.update_link,
                    0
                )

                if (
                        latest_version is not None and 
                        latest_version != config.version
                    ):
                    # UpdateVersion returns the new version when update found
                    self._state = self.STATE_BEHIND
                    self._button_update.enable()
                
                elif (
                        latest_version is None and
                        self.update_link in persistent._update_version
                    ):
                    # if update_link is in the update version (which means
                    # we have checked for an update using this url before),
                    # and UpdateVersion returns None, then no update is
                    # available
                    self._state = self.STATE_UPDATED

                # otherwise
                # UpdateVersion has either:
                # - returned the current verison, which means its still
                #   processing
                # - returned None and has never contacted the server 
                #   before (which means update_link is not in 
                #   update_version)


        def render(self, width, height, st, at):
            """
            RENDER
            """

            # check states
            self._checkUpdate()

            # now render
            r = renpy.Render(width, height)

            # starting with backgrounds 
            back = renpy.render(self.background, width, height, st, at)
            confirm = renpy.render(self.confirm, width, height, st, at)

            if self._state == self.STATE_CHECKING:
                # checking for updates
                display_text = renpy.render(
                    self._text_checking,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._checking_buttons

            elif self._state == self.STATE_UPDATED:
                # no update avaiable
                display_text = renpy.render(
                    self._text_noupdate,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._updated_buttons

            elif self._state == self.STATE_BEHIND:
                # update available
                display_text = renpy.render(
                    self._text_update,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._behind_buttons

            else:
                # timed out
                display_text = renpy.render(
                    self._text_timeout,
                    width,
                    height,
                    st,
                    at
                )
                display_buttons = self._timeout_buttons

            # render the buttons
            rendered_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in display_buttons
            ]

            # get display text blit coords
            pw, ph = display_text.get_size()

            # now blit em all
            r.blit(back, (0, 0))
            r.blit(confirm, (self._confirm_x, self._confirm_y))
            r.blit(
                display_text, 
                (
                    int((width - pw) / 2),
                    int((height - ph) / 2) + self.TEXT_YOFFSET
                )
            )
            for vis_b, xy in rendered_buttons:
                r.blit(vis_b, xy)

            # force a redraww so we keep checking udpater
            renpy.redraw(self, 1.0)

            return r


        def event(self, ev, x, y, st):
            """
            EVENT
            """
            if ev.type in self.MOUSE_EVENTS:

                if self._state == self.STATE_CHECKING:
                    # checking for an update state

                    if self._button_cancel.event(ev, x, y, st):
                        # cancel clicked! return -1
                        return -1

                elif self._state == self.STATE_UPDATED:
                    # no update found
                    
                    if self._button_ok.event(ev, x, y, st):
                        # ok clicked! return -1
                        return -1

                elif self._state == self.STATE_BEHIND:
                    # found an update

                    if self._button_update.event(ev, x, y, st):
                        # update clicked! return 1
                        return 1

                    if self._button_cancel.event(ev, x, y, st):
                        # cancel clicked! return -1
                        return -1

                else:
                    # timeout state

                    if self._button_cancel.event(ev, x, y, st):
                        # cancel clicked! return -1
                        return -1

                    if self._button_retry.event(ev, x, y, st):
                        # retry clicked! go back to checking
                        self._button_update.disable()
                        self._prev_time = time.time()
                        self._state = self.STATE_CHECKING

                renpy.redraw(self, 0)

            raise renpy.IgnoreEvent()


label forced_update_now:
    $ mas_updater.force = True

#This file goes through the actions for updating Monika After story
label update_now:
    $import time #this instance of time can stay
    python:
        if persistent._mas_unstable_mode:
            update_link = mas_updater.unstable

        else:
            update_link = mas_updater.regular

        last_updated = persistent._update_last_checked.get(update_link, 0)

        if last_updated > time.time():
            last_updated = 0

    #Make sure the update folder is where it should be
    if not updater.can_update():
        python:
            try: renpy.file(config.basedir + "/update/current.json")
            except:
                try: os.rename(config.basedir + "/game/update", config.basedir + "/update")
                except: pass

    if mas_updater.force:
        $ check_wait = 0
    else:
        # wait 24 hours before updating
        $ check_wait = 3600 * 24

    if time.time()-last_updated > check_wait and updater.can_update():
        if persistent._mas_unstable_mode:
            # use unstabel stuff
            $ update_link = mas_updater.unstable
        else:
            # use regular updates
            $ update_link = mas_updater.regular


        # call the updater displayable
        python:
            ui.add(MASUpdaterDisplayable(update_link))
            updater_selection = ui.interact()

        if updater_selection > 0:
            # user wishes to update
            $ persistent.closed_self = True # we take updates as self closed
            $ updater.update(update_link, restart=True)
    return
