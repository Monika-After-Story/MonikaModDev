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
        # in particular, we want a cancel button and a sensistive update
        # button as well an Okay
        # well, we'll figure it out as we go along.
       
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35

        FRAME_WIDTH = 500
        FRAME_HEIGHT = 250

        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        def __init__(self, update_link):
            """
            Constructor
            """
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

            # calculate positions
            self._confirm_x = self.




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


        $ mas_updater.timeout = 10 # set timeout var
#        $ persistent._update_last_checked[update_link] = time.time()
#        $ updater.update(update_link, restart=True)

        # if we reach here, no update occured, probably
#        if mas_updater.timeout <= 0:
            # timeout is empty, show a confirm screen
#            call screen dialog("Timeout occured while checking for updates. Try again later.", Return(True))
            

#        $timeout = 10 # 10 second timeout
#        $ sel_option = None

#        while timeout > 0 and sel_option is None:
            # 10 seconds of update processing
#            $ latest_version = updater.UpdateVersion(update_link, 0)
#            if latest_version is not None and latest_version != config.version:
                # UpdateVersion returns the new version when an update is found
#                $ mode = 0 # version found    

#            elif latest_version is None and update_link in persistent._update_version:
                # if the update_link is in the update version (which means we
                # have checked for an update using this url before), and 
                # UpdateVersion returns None, then no update is available.
#                $ mode = 1 # no update found

#            elif timeout > 0:
                # UpdateVersion has either:
                # - returned the current version, which means its still processing
                # - returned None and has never contacted the server before
                #   ( which means update_link is not in update_version)
#                $ mode = 2 # checking for update

#            else:
                # otherwise, we assume a timeout
#                $ mode = 3 # timeout

#            call screen update_check(Return(True),Return(False),mode)

            # refresh this value
#            if _return != "None":
#                $ sel_option = _return

#            else:
                # wait a second
#                pause 1.0
#                $ timeout -= 1

#        if _sel_option
#            $ persistent.closed_self = True # we take updates as self closed
#            $updater.update(update_link, restart=True)
    return
