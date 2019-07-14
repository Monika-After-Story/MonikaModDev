#Here's where we store our background data
default persistent._mas_background_MBGdata = {}

#START: Class definition
init -10 python:
    class MASBackground(object):
        """
        Background class to get display props for bgs

        PROPERTIES:
            background_id - the id which defines this bg
            prompt - button label for the bg
            image_day - the day background image object
            image_night - the night background image object
            hide_calendar - whether or not we display the calendar with this
            hide_masks - whether or not we display the window masks
            hide_table - whether or not we want to have the table present
            unlocked - whether or not this background is unlocked
            entry_pp - entry programming points for bgs
            exit_pp - exit programming points
        """
        import store.mas_background as mas_background

        def __init__(
            self,
            background_id,
            prompt,
            image_day,
            image_night,
            hide_calendar=False,
            hide_masks=False,
            hide_table=False,
            unlocked=False,
            entry_pp=None,
            exit_pp=None
        ):
            """
            Constructor for background objects

            IN:
                background_id:
                    id that defines the background object
                    NOTE: Must be unique

                prompt:
                    button label for this bg

                image_day:
                    the renpy.image object we use for this bg during the day
                    NOTE: Mandatory

                image_night:
                    the renpy.image object we use for this bg during the night
                    NOTE: Mandatory

                hide_calendar:
                    whether or not we want to display the calendar
                    (Default: False)

                hide_masks:
                    weather or not we want to show the windows
                    (Default: False)

                hide_table:
                    whether or not we want to hide the table
                    NOTE: currently has no effect
                    (Default: False)

                unlocked:
                    whether or not this background starts unlocked
                    (Default: False)

                entry_pp:
                    Entry programming point for the background
                    (Default: None)

                exit_pp:
                    Exit programming point for this background
                    (Default: None)
            """

            if background_id in self.mas_background.BACKGROUND_MAP:
                raise Exception("duplicate background ID")

            if mas_background.areBGsLoadable(background_id):
                self.background_id = background_id
                self.prompt = prompt
                self.image_day = image_day
                self.image_night = image_night
                self.hide_calendar = hide_calendar
                self.hide_masks = hide_masks
                self.hide_table = hide_table
                self.unlocked = unlocked
                self.entry_pp = entry_pp
                self.exit_pp = exit_pp

                # add to background map
                self.mas_background.BACKGROUND_MAP[background_id] = self

            else:
                #Silently fail this, but log it.
                store.mas_utils.writelog("[ERROR]: Failed to load background: " + prompt + ". Files are missing.")


        def __eq__(self, other):
            if isinstance(other, MASBackground):
                return self.background_id == other.background_id
            return NotImplemented


        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result


        def entry(self, old_background):
            """
            Run the entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_background)


        def exit(self, new_background):
            """
            Run the exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_background)


        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]


        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)


#Helper methods and such
init -20 python in mas_background:
    BACKGROUND_MAP = {}
    BACKGROUND_RETURN = "Nevermind"

    def buildBGPaths(background_id, night=False):
        """
        Builds the path to the bg images

        IN:
            background_id:
                The filename expected

            night:
                Whether or not to get the night version
        """
        pfx = "mod_assets/location/" + background_id + "/"
        if night:
            return pfx + background_id + "-n.png"
        return pfx + background_id + ".png"

    def areBGsLoadable(background_id):
        """
        Checks if we can load the bgs
        """
        return renpy.loadable(buildBGPaths(background_id)) and renpy.loadable(buildBGPaths(background_id,True))

    def loadMBGData():
        """
        Loads persistent MASBackground data into the weather map

        ASSUMES: background map is already filled
        """
        if store.persistent._mas_background_MBGdata is None:
            return

        for mbg_id, mbg_data in store.persistent._mas_background_MBGdata.iteritems():
            mbg_obj = BACKGROUND_MAP.get(mbg_id, None)
            if mbg_obj is not None:
                mbg_obj.fromTuple(mbg_data)

    def saveMBGData():
        """
        Saves MASBackground data from weather map into persistent
        """
        for mbg_id, mbg_obj in BACKGROUND_MAP.iteritems():
            store.persistent._mas_background_MBGdata[mbg_id] = mbg_obj.toTuple()


#START: BG change functions
init 800 python:

    def mas_setBackground(_background):
        """
        Sets the initial bg

        NOTE: We don't handle exit pp's here

        IN:
            _background:
                The background we're changing to
        """
        global mas_current_background
        old_background = mas_current_background
        mas_current_background = _background
        mas_current_background.entry(old_background)

    def mas_changeBackground(new_background, by_user=None):
        """
        changes the background w/o any scene changes

        IN:
            new_background:
                The background we're changing to

            by_user:
                If the user switched the background themselves
        """
        if by_user is not None:
            mas_background.force_background = bool(by_user)

        mas_current_background.exit(new_background)
        mas_setBackground(new_background)

    #Just set us to the normal room here
    mas_current_background = None
    mas_setBackground(mas_background_def)

    #Make sure the bg selector is only available with the right amount of bgs unlocked
    if len([
        (mbg_obj.prompt, mbg_obj, False, False)
        for mbg_id, mbg_obj in mas_background.BACKGROUND_MAP.iteritems()
        if mbg_obj.unlocked
        ]
        ) < 2:
        mas_lockEVL("monika_change_background","EVE")

#START: Programming points
init -2 python in mas_background:
    import store

    def _def_background_entry(_old):
        """
        Entry programming point for befault background
        """
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

    def _def_background_exit(_new):
        """
        Exit programming point for befault background
        """
        store.mas_lockEVL("mas_monika_islands", "EVE")


#START: bg defs
init -1 python:
    #Default spaceroom
    mas_background_def = MASBackground(
        #Identification
        "spaceroom",
        "Spaceroom",

        #Day/Night
        "monika_day_room",
        "monika_room",

        #Def room should always be unlocked
        unlocked=True,

        #Programming points for the spaceroom
        entry_pp=store.mas_background._def_background_entry,
        exit_pp=store.mas_background._def_background_exit
    )


#START: Image definitions
#Spaceroom
image monika_day_room = "mod_assets/location/spaceroom/spaceroom.png"
image monika_room = "mod_assets/location/spaceroom/spaceroom-n.png"

#START: Location Selector
init 5 python:
    # available only if moni affection is affectionate+
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_background",
            category=["location"],
            prompt="Can we go somewhere else?",
            pool=True,
            unlocked=True,
            rules={"no unlock": None},
            aff_range=(mas_aff.AFFECTIONATE, None)
        )
    )

label monika_change_background:

    m 1hua "Sure!"

label monika_change_background_loop:

    show monika 1eua at t21

    $ renpy.say(m, "Where would you like to go?", interact=False)

    python:
        # build menu list
        import store.mas_background as mas_background
        import store.mas_moods as mas_moods

        # we assume that we will always have more than 1
        # default should always be at the top
        backgrounds = [(mas_background_def.prompt, mas_background_def, False, False)]

        # build other backgrounds list
        other_backgrounds = [
            (mbg_obj.prompt, mbg_obj, False, False)
            for mbg_id, mbg_obj in mas_background.BACKGROUND_MAP.iteritems()
            if mbg_id != "spaceroom" and mbg_obj.unlocked
        ]

        # sort other backgrounds list
        other_backgrounds.sort()

        # build full list
        backgrounds.extend(other_backgrounds)

        # now add final quit item
        final_item = (mas_background.BACKGROUND_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(backgrounds, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item)

    $ sel_background = _return

    show monika at t11

    # return value False? then return
    if sel_background is False:
        m 1eka "Oh, alright."
        m "If you want to go somewhere, just ask, okay?"
        return

    if sel_background == mas_current_background:
        m 1hua "We're here right now, silly."
        m "Try again~"
        jump monika_change_background_loop

    $ skip_outro = False
    $ skip_leadin = False

    # otherwise, we can change the background now
    if not skip_leadin:
        m 1eua "Alright!"
        m 1hua "Let's go, [player]!"

    #Little transition
    hide monika
    scene black
    with dissolve
    pause 2.0

    # finally change the background
    $ mas_changeBackground(sel_background)

    if sel_background.skip_masks:
        $ mas_weather.temp_weather_storage = mas_current_weather
        $ mas_changeWeather(mas_weather_def)
        $ mas_lockEVL("monika_change_weather", "EVE")

    else:
        if mas_weather.temp_weather_storage is not None:
            $ mas_changeWeather(mas_weather.temp_weather_storage)

        else:
            #If we don't have tempstor, run the startup weather
            $ set_to_weather = mas_shouldRain()
            if set_to_weather is not None:
                $ mas_changeWeather(set_to_weather)
            else:
                $ mas_changeWeather(mas_weather_def)

        $ mas_unlockEVL("monika_change_weather", "EVE")

    call spaceroom(scene_change=True, dissolve_all=True)

    if not skip_outro:
        m 1eua "Here we are!"
        m "Let me know if you want to go somewhere else, okay?"
    return