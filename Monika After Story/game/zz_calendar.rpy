# Calendar module
# A custom made Calendar like UI to help managing date based events
# Contains also a store named mas_calendar which includes helper functions
# to add Events to the calendar

init -1 python:

    import json
    from store.mas_calendar import CAL_TYPE_EV,CAL_TYPE_REP

    class CustomEncoder(json.JSONEncoder):
        """
        Custom JSONEncoder used to process sets
        """
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)


    class MASCalendar(renpy.Displayable):
        """
        Custom Calendar UI, can be used to display the events that are dependent
        on dates or to allow user to pick a date

        """

        import pygame
        import datetime
        import store.evhand as evhand
        from store.mas_calendar import CAL_TYPE_REP
        #import store.mas_calendar as calendar

        # CONSTANTS

        # view port size
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        # exit button position and size
        EXIT_BUTTON_WIDTH = 74
        EXIT_BUTTON_HEIGHT = 74
        EXIT_BUTTON_X = 1040
        EXIT_BUTTON_Y = 60

        # day name related sizes
        DAY_BUTTON_WIDTH = 128
        DAY_BUTTON_HEIGHT = 65
        DAY_NAME_BUTTON_HEIGHT = 35

        # initial position for displaying things inside the calendar
        INITIAL_POSITION_X = 193
        INITIAL_POSITION_Y = 155

        # position for the title
        TITLE_POSITION_Y = 115
        TITLE_POSITION_X_1 = 560
        TITLE_POSITION_X_2 = 530

        # size for the arrow like button selectors
        ARROW_BUTTON_SIZE = 20

        # Size of the day number and displayed data inside a day block
        CALENDAR_DAY_TEXT_SIZE = 12

        # X inside the close button size
        CALENDAR_CLOSE_X_SIZE = 45

        # Return values for constant buttons
        CALENDAR_CLOSE = "CLOSE" # closes the calendar
        CALENDAR_MONTH_INCREASE = "MONTH_INCR" # signals to increase the current selected month
        CALENDAR_MONTH_DECREASE = "MONTH_DECR" # signals to decrease the current selected month
        CALENDAR_YEAR_INCREASE = "YEAR_INCR" # signals to increase the current selected year
        CALENDAR_YEAR_DECREASE = "YEAR_DECR" # signals to decrease the current selected month

        # Color used for the day number
        TEXT_DAY_COLOR = "#000000" # PINK: "#ffb0ed"

        # Month names constant array
        MONTH_NAMES = ["Unknown", "January", "Febuary",
            "March", "April", "May", "June", "July",
            "August", "September", "October",
            "November", "December"]

        # Day names constant array
        DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday"]

        # Format used for calendar display
        DATE_DISPLAY_FORMAT = "\t  \t  \t  \t  \t  \t  \t  {0}\n{1}\n{2}\n{3}"

        # Events to which Calendar buttons will check for
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )

        # pane constants
        EVENT_X = 800
        EVENT_Y = 40
        EVENT_W = 450
        EVENT_H = 640
        EVENT_XALIGN = 0.54
        EVENT_AREA = (EVENT_X, EVENT_Y, EVENT_W, EVENT_H)
        EVENT_RETURN = "< Go back"

        def __init__(self, select_date=False):
            """
            Constructor for the custom calendar.

            IN:
                select_date - a boolean that indicates how this calendar is going to
                    do, True indicates that it will select a day, False means that it
                    will only be for displaying events.
                    (Default: False)
            """
            super(renpy.Displayable, self).__init__()

            # The calendar background
            self.calendar_background = renpy.displayable("mod_assets/calendar/calendar_bg.png")

            # Can we select dates?
            self.can_select_date = select_date
            # testing
            # calendar.saveCalendarDatabase(CustomEncoder, evhand.calendar_database)
            # testing
            # store.mas_calendar.calendar_database[6][6]["test"] = ((CAL_TYPE_REP,"test",list()))
            # store.mas_calendar.calendar_database[6][6]["test2"] = ((CAL_TYPE_REP,"test2",list()))
            # store.mas_calendar.calendar_database[6][6]["tes"] = ((CAL_TYPE_REP,"tes",list()))
            # store.mas_calendar.calendar_database[6][6]["test3"] = ((CAL_TYPE_REP,"test3",list()))
            # store.mas_calendar.calendar_database[6][6]["test5"] = ((CAL_TYPE_REP,"test5",list()))
            # store.mas_calendar.calendar_database[6][6]["test6"] = ((CAL_TYPE_REP,"test6",list()))
            # store.mas_calendar.calendar_database[6][6]["test7"] = ((CAL_TYPE_REP,"test7",list()))

            # database
            self.database = store.mas_calendar.calendar_database

            # background mask
            self.background = Solid(
                "#000000B2",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )

            # default calendar view to current month
            # keep reference to it in case it may need it later
            self.today = datetime.date.today()

            self.selected_month = self.today.month
            self.selected_year = self.today.year

            # store all buttons for easy rendering
            self.const_buttons = []
            self.day_buttons = []

            # button backgrounds
            button_close = Image(
                "mod_assets/calendar/calendar_close.png"
            )
            button_close_hover = Image(
                "mod_assets/calendar/calendar_close_hover.png"
            )
            button_day_name = Image(
                "mod_assets/calendar/calendar_day_name_bg.png"
            )
            button_left_arrow = Image(
                "mod_assets/calendar/calendar_left_arrow.png"
            )
            button_right_arrow = Image(
                "mod_assets/calendar/calendar_right_arrow.png"
            )
            button_left_arrow_hover = Image(
                "mod_assets/calendar/calendar_left_arrow_hover.png"
            )
            button_right_arrow_hover = Image(
                "mod_assets/calendar/calendar_right_arrow_hover.png"
            )

            # Change title depending on flag
            if select_date:
                self.title_position_x = self.TITLE_POSITION_X_2
                self.text_title = Text(
                    "Select a Date",
                    font=gui.default_font,
                    size=33,
                    color="#ffffff",
                    outlines=[]
                )
            else:
                self.title_position_x = self.TITLE_POSITION_X_1
                self.text_title = Text(
                    "Calendar",
                    font=gui.default_font,
                    size=33,
                    color="#ffffff",
                    outlines=[]
                )

            # iterate over the days
            i = 0
            for day in self.DAY_NAMES:

                # Generate as buttons the day names

                button_day_text = Text(
                    day,
                    font=gui.default_font,
                    size=17,
                    color=self.TEXT_DAY_COLOR,
                    outlines=[]
                )

                button_day_button = MASButtonDisplayable(
                    button_day_text,
                    button_day_text,
                    button_day_text,
                    button_day_name,
                    button_day_name,
                    button_day_name,
                    self.INITIAL_POSITION_X + (i * self.DAY_BUTTON_WIDTH),
                    self.INITIAL_POSITION_Y + self.DAY_NAME_BUTTON_HEIGHT,
                    self.DAY_BUTTON_WIDTH,
                    self.DAY_NAME_BUTTON_HEIGHT,
                    hover_sound=None,
                    activate_sound=None,
                    return_value=None
                )

                # add them to the const_buttons array
                self.const_buttons.append(button_day_button)
                i = i + 1

            # close button
            button_text_close = Text(
                "X",
                font=gui.default_font,
                size=self.CALENDAR_CLOSE_X_SIZE,
                color="#ffb0ed",
                outlines=[]
            )

            button_text_close_hover = Text(
                "X",
                font=gui.default_font,
                size=self.CALENDAR_CLOSE_X_SIZE,
                color="#ffd3f4",
                outlines=[]
            )

            self.button_exit = MASButtonDisplayable(
                button_text_close,
                button_text_close_hover,
                button_text_close,
                button_close,
                button_close_hover,
                button_close,
                self.EXIT_BUTTON_X,
                self.EXIT_BUTTON_Y,
                self.EXIT_BUTTON_WIDTH,
                self.EXIT_BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_CLOSE
            )

            # empty text label used for the buttons that require an image
            # these aren't Image buttons mostly cause I find easier to keep
            # it constant with the UI related buttons
            button_empty_text = Text(
                "",
                font=gui.default_font,
                size=12,
                color="#ffb0ed",
                outlines=[]
            )

            # actual buttons that decrease/ increase the month and year values
            self.button_month_decrease = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_left_arrow,
                button_left_arrow_hover,
                button_left_arrow,
                self.INITIAL_POSITION_X + 70,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_MONTH_DECREASE
            )

            self.button_month_increase = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_right_arrow,
                button_right_arrow_hover,
                button_right_arrow,
                self.INITIAL_POSITION_X + 300,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_MONTH_INCREASE
            )

            self.button_year_decrease = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_left_arrow,
                button_left_arrow_hover,
                button_left_arrow,
                self.INITIAL_POSITION_X + 525,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_YEAR_DECREASE
            )

            self.button_year_increase = MASButtonDisplayable(
                button_empty_text,
                button_empty_text,
                button_empty_text,
                button_right_arrow,
                button_right_arrow_hover,
                button_right_arrow,
                self.INITIAL_POSITION_X + 770,
                self.INITIAL_POSITION_Y + 10,
                self.ARROW_BUTTON_SIZE,
                self.ARROW_BUTTON_SIZE,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.CALENDAR_YEAR_INCREASE
            )

            # add buttons to the const_buttons array
            self.const_buttons.append(self.button_exit)
            self.const_buttons.append(self.button_month_decrease)
            self.const_buttons.append(self.button_month_increase)
            self.const_buttons.append(self.button_year_decrease)
            self.const_buttons.append(self.button_year_increase)

            # call set up day buttons to fill up the calendar
            self._setupDayButtons()


        def _setupDayButtons(self):
            """
            Sets up the day buttons used in the calendar
            """

            # button backgrounds
            button_day_bg = Image(
                "mod_assets/calendar/calendar_day_bg.png"
            )

            button_day_bg_disabled = Image(
                "mod_assets/calendar/calendar_day_disabled_bg.png"
            )

            button_day_bg_hover = Image(
                "mod_assets/calendar/calendar_day_hover_bg.png"
            )


            # constant month and year text labels
            self.text_current_month = Text(
                self.MONTH_NAMES[self.selected_month],
                font=gui.default_font,
                size=21,
                color=self.TEXT_DAY_COLOR,
                outlines=[]
            )

            self.text_current_year = Text(
                str(self.selected_year),
                font=gui.default_font,
                size=21,
                color=self.TEXT_DAY_COLOR,
                outlines=[]
            )

            # init day buttons array
            self.day_buttons = []

            # get relevant date info
            day = datetime.timedelta(days=1)
            first_day = datetime.datetime(self.selected_year, self.selected_month, 1)

            # get the first_day of the week that has the first day of current month
            while first_day.weekday() != 6:
                first_day = first_day - day

            # init the array that will hold the dates we're displaying
            self.dates = []

            # get all the dates we'll be displaying  and store them on the array
            for i in range(42):
                self.dates.append(first_day + datetime.timedelta(days=i))

            # get this month's events
            events = self.database[self.selected_month]

            # calculation to determine the initial y position
            initial_y = self.INITIAL_POSITION_Y + (self.DAY_NAME_BUTTON_HEIGHT * 2)

            # iterate over rows and columns to create our calendar ui
            for i in range(6):

                for j in range(7):

                    # helper vars for day processing
                    current_date = self.dates[j + (i * 7)]
                    ret_val = None
                    many_events = False
                    bg_disabled = button_day_bg_disabled

                    # current day events display helpers
                    event_labels = list()
                    third_label = ""

                    # if this day is on the current month process the events that it may have
                    if current_date.month == self.selected_month:
                        _todays_events = events[current_date.day]

                        # iterate through them
                        for k in _todays_events:
                            e = _todays_events[k]

                            # check for event type
                            if e[0] == CAL_TYPE_EV:
                                # retrieve the event
                                ev = mas_getEV(k)

                                if self._isEvInYear(ev, self.selected_year):
                                    event_labels.append(mas_getEVCL(k))

                            # non event type
                            if e[0] == CAL_TYPE_REP:
                                # if the year is not None or it's contained in it's range
                                if e[2] is not None and ( not e[2] or self.selected_year in e[2]):
                                    # add the non event
                                    event_labels.append(e[1])


                        # if we have exactly 3 events
                        if len(event_labels) == 3:
                            # third_label should hold the event text
                            third_label = event_labels[2]
                        if len(event_labels) > 3:
                            many_events = True
                            if self.can_select_date:
                                third_label = "and more events"
                            else:
                                third_label = "(Click to see more)"
                                ret_val = event_labels

                    # if we don't have any labels or less than 2
                    if not event_labels or len(event_labels) < 2:

                        # we can safely add 2 empty ones
                        event_labels.append("")
                        event_labels.append("")

                    # Add button behaviour to it
                    if current_date.month == self.selected_month:
                        bg_disabled = button_day_bg

                        if self.can_select_date:
                            ret_val = current_date

                    day_button_text = Text(
                        self.DATE_DISPLAY_FORMAT.format(str(current_date.day), event_labels[0], event_labels[1], third_label),
                        font=gui.default_font,
                        size=self.CALENDAR_DAY_TEXT_SIZE,
                        color=self.TEXT_DAY_COLOR,
                        outlines=[]
                    )

                    day_button = MASButtonDisplayable(
                        day_button_text,
                        day_button_text,
                        day_button_text,
                        button_day_bg,
                        button_day_bg_hover,
                        bg_disabled,
                        self.INITIAL_POSITION_X + (j * self.DAY_BUTTON_WIDTH),
                        initial_y + (i * self.DAY_BUTTON_HEIGHT),
                        self.DAY_BUTTON_WIDTH,
                        self.DAY_BUTTON_HEIGHT,
                        hover_sound=gui.hover_sound,
                        activate_sound=gui.activate_sound,
                        return_value=ret_val
                    )

                    # if this day isn't on the current month
                    if current_date.month != self.selected_month or (not self.can_select_date and not many_events):
                        # disable the button
                        day_button.disable()


                    self.day_buttons.append(day_button)


        def _showScrollableEventList(self,events):
            """
            Displays the events contained in the events list
            said list is a list of Strings to show
            """

            event_list_title = ("Events for the day:", False, True)

            # build list
            event_list_items = [(e, False, False) for e in events]

            # final quit item
            final_item = (self.EVENT_RETURN, False, False, False, 20)

            # call scrollable pane
            renpy.call_in_new_context("mas_show_calendar_detail", event_list_items, self.EVENT_AREA, self.EVENT_XALIGN, first_item=event_list_title, final_item=final_item)


        def _xcenter(self, v_width, width):
            """
            Returns the appropriate X location to center an object with the
            given width

            IN:
                v_width - width of the view
                width - width of the object to center

            RETURNS:
                appropiate X coord to center
            """
            return int((v_width - width) / 2)


        def _buttonSelect(self, ev, x, y, st):
            """
            Goes through the list of buttons and return the first non-None
            value returned

            RETURNS:
                first non-none value returned
            """

            #iterate over both lists
            for button in self.const_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val

            for button in self.day_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val

            return None


        def _changeYear(self, ascend=True):
            """
            Changes the currently selected year by incrementing or decrementing it by one
            and refreshes the view

            IN:
                ascend - flag that indicates wheter increment or decrement
                    (Defaults to True)
            """
            if ascend:
                self.selected_year = self.selected_year + 1
            else:
                self.selected_year = self.selected_year - 1
            self._setupDayButtons()


        def _changeMonth(self, ascend=True):
            """
            Changes the currently selected month by incrementing or decrementing it by one
            and refreshes the view

            IN:
                ascend - flag that indicates wheter increment or decrement
                    (Defaults to True)
            """
            if ascend:

                self.selected_month = self.selected_month + 1

                # check if we need to increment the year
                if self.selected_month >=13:
                    self.selected_month = 1
                    self.selected_year = self.selected_year + 1
            else:

                self.selected_month = self.selected_month - 1

                # check if  we need to decrement the year
                if self.selected_month <=0:
                    self.selected_month = 12
                    self.selected_year = self.selected_year - 1
            self._setupDayButtons()


        def _isEvInYear(self, ev, year):
            """
            Checks if the given event should appear in the given year.

            IN:
                ev - event to check
                year - year to check

            RETURNS: True if the given event belongs in the given year,
                False otherwise
            """
            if ev.years is not None:
                # empty list means we should always repeat this event
                # otherwise we can just check if the given year is in the list
                return len(ev.years) == 0 or year in ev.years

            # otherwise, we check start date year
            return ev.start_date is not None and ev.start_date.year == year


        def render(self, width, height, st, at):

            # render mask
            back = renpy.render(self.background, width, height, st, at)

            # Create a render for the background.
            calendar_bg = renpy.render(self.calendar_background, width, height, st, at)

            # Calendar title
            calendar_title = renpy.render(self.text_title, width, height, st, at)

            # displayable month and year labels
            month_label = renpy.render(self.text_current_month, width, height, st, at)

            year_label = renpy.render(self.text_current_year, width, height, st, at)

            # now do some calcs
            monw, monh = month_label.get_size()
            yearw, yearh = year_label.get_size()

            monthx = self._xcenter(380, monw)
            yearx = self._xcenter(380, yearw) + 460

            # Get the size of the child.
            self.width, self.height = calendar_bg.get_size()

            # Create the render we will return.
            r = renpy.Render(width, height)

            # blit the constant elements that make this UI
            r.blit(back,(0,0))

            r.blit(calendar_bg, (192, 103))

            r.blit(month_label, (self.INITIAL_POSITION_X + monthx, self.INITIAL_POSITION_Y + 8))

            r.blit(year_label, (self.INITIAL_POSITION_X + yearx, self.INITIAL_POSITION_Y + 8))

            r.blit(calendar_title, (self.title_position_x, self.TITLE_POSITION_Y))

            # blit the constant buttons
            c_r_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in self.const_buttons
            ]

            for vis_b, xy in c_r_buttons:
                r.blit(vis_b, xy)

            # blit the calendar buttons
            cal_r_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in self.day_buttons
            ]

            for vis_b, xy in cal_r_buttons:
                r.blit(vis_b, xy)

            # Return the render.
            return r


        def event(self, ev, x, y, st):

            # we only care about mouse
            if ev.type in self.MOUSE_EVENTS:

                # get the value from buttons
                sel_action = self._buttonSelect(ev, x, y, st)

                if sel_action:

                    # nonNone value returned

                    if sel_action == self.CALENDAR_CLOSE:

                        # this means the user selected close
                        return ""

                    #if we have a datetime
                    if isinstance(sel_action, datetime.datetime):

                        # return it
                        return sel_action

                    if isinstance(sel_action, type(list())):
                        self._showScrollableEventList(sel_action)

                    # check for month/year decrements and increments
                    if sel_action == self.CALENDAR_YEAR_INCREASE:
                        self._changeYear()

                    if sel_action == self.CALENDAR_YEAR_DECREASE:
                        self._changeYear(False)

                    if sel_action == self.CALENDAR_MONTH_INCREASE:
                        self._changeMonth()

                    if sel_action == self.CALENDAR_MONTH_DECREASE:
                        self._changeMonth(False)

            # otherwise continue
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()

# calendar utils
init -10 python in mas_calendar:
    # special constants for Calendar Event types
    CAL_TYPE_EV = 1
    CAL_TYPE_REP = 2


init -1 python in mas_calendar:
    import datetime
    import json
    import renpy

    ### Calendar database stores events for repeating / processing and more.
    #
    # The first layer organizes the events by month.
    # The second layer organizes the events by day.
    # The third layer contains the events in dicts, key being the eventlabel
    #   and the value the fourth layer element, this to prevent duplicates
    # The fourth layer the event tuple, which consists of the following:
    #   [0]: type of item this is (event or just a label)
    #       (CAL_TYPE_EV, CAL_TYPE...)
    #   [1]: key / identifier of this item (eventlabel if an event, some other
    #       key for a label)
    #   [2]: list of years this event exists in
    #       IF None, this event repeats anually forever
    calendar_database = dict()
    for i in range(1,13):
        calendar_database[i] = dict()
        for j in range(1,32):
            calendar_database[i][j] = dict()

    # st/nd/rd/th mapping
    NUM_MAP = {
        1: "st",
        2: "nd",
        3: "rd",
        11: "th",
        12: "th",
        13: "th"
    }


    def _formatDay(day):
        """
        Properly formats the given day so it displays with the correct
        suffixes.

        IN:
            day - day to get a nice display string

        RETURNS:
            nice display string for the day
        """
        return str(day) + NUM_MAP.get(day, "th")


    def _formatYears(years):
        """
        Properly formats the given years var so it says a user friendly
        way to show years.

        Basically if years is:
        0 - ""
        1 - "last year"
        2+ - "x years ago"

        IN:
            years - number of years to get a nice display string

        RETURNS:
            nice display string for the years
        """
        if years <= 0:
            return ""

        if years == 1:
            return "last year"

        return str(years) + " years ago"


    def genFriendlyDispDate(_datetime):
        """
        Generates a display date using the given datetime
        This creates a display date in the format:
            Month Day, Year
        However, this is somewhat variable.

        If it is the same as the current year, the year is not provided.
        If the date is whithin a year of the current date, year is not
        provided.
        If the year is last year and greater than a year of the current date,
        "last year on <month> <day>"
        If the year is within 2-10 years ago, then "x years ago on <month>
        <day>" is used.
        Otherwise, the actual 4 digit year is used.

        If the days / months are the same, then "x years ago to this date"
        is used.

        IN:
            _datetime - datetime object to create good display date

        RETURNS:
            tuple of the following format:
            [0]: nicely formatted display date, suitable for conversation
            [1]: timedelta between today and the given _datetime
        """
        # the month is always fine to take out
        disp_month = _datetime.strftime("%B")

        # display day is easy
        disp_day = _formatDay(_datetime.day)

        # to find out year, we need now
        _today = datetime.date.today()
        _date = _datetime.date()
        _day_diff = _today - _date
        _year_diff = _today.year - _date.year

        # the list of strings to join
        _cout = list()

        if _today.month == _date.month and _today.day == _date.day:
            # same day, just a diff year (probably)

            if _year_diff == 0:
                # it's today!
                _cout = [
                    "today"
                ]

            else:
                # okay but srs, we know theres a year diff here
                _cout = [
                    _formatYears(_year_diff),
                    "on this date"
                ]


        elif _day_diff.days <= 365: # within a year
            # same year, diff month
            _cout = [disp_month, disp_day]

        elif _year_diff <= 10:
            # within 10 years
            _cout = [
                _formatYears(_year_diff),
                "on",
                disp_month,
                disp_day
            ]

        else:
            # more than 10? use the 4 digit year
            _cout = [
                disp_month,
                disp_day,
                ",",
                str(_date.year)
            ]

        # now return the formatting string + diff
        return (" ".join(_cout), _day_diff)


    def saveCalendarDatabase(encoder, database):
        """
        Saves the passed database as a json file named db.mcal

        IN:
            - encoder a json.JSONEncoder to be used for encoding
                the database
            - database a dict containing the events
        """
        with open(renpy.config.savedir + '/db.mcal', 'w') as fp:
            json.dump(database, fp, cls=encoder)

    def loadCalendarDatabase():
        """
        Returns the database read from the file renpy.config.savedir + '/db.mcal'
        as a dict

        RETURNS:
            a dict containing the events for the calendar

        """
        with open(renpy.config.savedir + '/db.mcal', 'r') as fp:
            return json.load(fp)


    ### ADD FUNCTIONS
    def __addEvent_md(ev_label, month, day):
        """
        Adds an event to the calendar at a precise month / day

        NOTE: no sanity checks are done for month / day

        IN:
            ev_label - eventlabel of the event to add
            month - month to add to
            day - day to add to
        """
        calendar_database[month][day][ev_label] = ((
            CAL_TYPE_EV,
        ))


    def _addRepeatable_md(identifier, display_label, month, day, year_param):
        """
        Adds a repeatable to the calendar at a precise month / day

        NOTE: no sanity checks are done for month / day

        IN:
            identifier - label of the event that it's unique
            display_label - label that will be displayed
            month - month to add to
            day - day to add to
            year_param - data to put in the year part of the tuple
        """
        calendar_database[month][day][identifier] = ((
            CAL_TYPE_REP,
            display_label,
            year_param
        ))


    def addEvent(ev):
        """
        Adds an event to the calendar accoridng to its start_date and end_date
        properties. If start_date is not set in the given event,
        this function will do nothing.

        IN:
            ev - event to add
        """
        if ev.start_date is None:
            return

        if ev.end_date is None:
            # if we don't have an end date, we assume that this is a single day
            # event only.
            addEvent_evdt(ev, ev.start_date)

        else:
            # otherwise, we need to iterate and add the appropriate days
            _delta = datetime.timedelta(days=1)
            curr_date = ev.start_date

            while curr_date < ev.end_date:
                addEvent_evdt(ev, curr_date)
                curr_date += _delta


    def addEvent_evd(ev, _date):
        """
        Adds an event to the calendar at a preicse date.

        IN:
            ev - event to add
            _date - datetime.date to add to
        """
        __addEvent_md(
            ev.eventlabel,
            _date.month,
            _date.day
        )


    def addEvent_evdt(ev, _datetime):
        """
        Adds an event to the calendar at a precise datetime.

        IN:
            ev - event to add
        """
        addEvent_evd(ev, _datetime.date())


    def addRepeatable(identifier, display_label, month, day, year_param):
        """
        Adds a repeatable to the calendar at a precise month / day
        Sanity checks are done for month / day

        IN:
            identifier - label of the event that it's unique
            display_label - label that will be displayed
            month - month to add to
            day - day to add to
            year_param - data to put in the year part of the tuple
        """
        if month in range(1,13) and day in range(1,32):
            _addRepeatable_md(identifier, display_label, month, day, year_param)


    def addRepeatable_d(identifier, display_label, _date, year_param):
        """
        Adds a repeatable to the calendar at precise datetime.date

        IN:
            identifier - identifier of the repeatable to add
            display_label - label that will be displayed
            _date - datetime.date to add to
            year_param - data to put in the year part of the tuple
        """
        _addRepeatable_md(
            identifier,
            display_label,
            _date.month,
            _date.day,
            year_param
        )


    def addRepeatable_dt(identifier, display_label, _datetime, year_param):
        """
        Adds a repeatable to the calendar at a precise datetime

        IN:
            identifier - identifier of the repeatable to add
            display_label - label that will be displayed
            _datetime - datetime to add to
            year_param - data to put in the year part of the tuple
        """
        addRepeatable_d(
            identifier,
            display_label,
            _datetime.date(),
            year_param
        )


    ### REMOVAL FUNCTIONS
    def _findEvent_md(ev_label, month, day):
        """
        Finds the event tuple from the calendar at a precise month / day.

        NOTE: no sanity checks are done for month / day

        IN:
            ev_label - eventlabel of the event to find
            month - month we should look at for finding
            day - day we should look at for finding

        RETURNS:
            the event tuple if it was found, None otherwise
        """
        _events = calendar_database[month][day]

        if ev_label in _events:
            _ev = _events[ev_label]
            if _ev[0] == CAL_TYPE_EV:
                # NOTE: we still check for event type in the case that a non
                #   event was added to the _events dict and was given a key
                #   that is also an eventlabel. We should avoid doing this,
                #   but it's certainly possible.
                return _ev

        return None


    def _findRepeatable_md(identifier, month, day):
        """
        Finds the repeatable dtuple from the calendar at a precise month / day

        NOTE: no sanity checks are done for month / day

        IN:
            identifier - the id of the repeatable to find
            month - month we should look at for finding
            day - day we should look at for finding

        RETURNS:
            the repeatable tuple if itw as found, None otherwise
        """
        _events = calendar_database[month][day]

        if identifier in _events:
            _rp = _events[identifier]
            if _rp[0] == CAL_TYPE_REP:
                # NOTE: we still check for repetable type in the case that an
                #   event was added to the _events dict and was given a key
                #   that is also an identifier. We should avoid doing this,
                #   but it's certainly possible.
                return _rp

        return None


    def _removeEvent(ev_label, remove_all=False):
        """
        Removs an event from the calendar.

        NOTE: O(n^2) efficieny, please avoid using this.

        IN:
            ev_label - eventlabel of the event to remove
            remove_all - SEE removeEvent_el
        """
        for month in range(1,13):
            _removeEvent_m(ev_label, month, remove_all=remove_all)


    def _removeEvent_d(ev_label, day, remove_all=False):
        """
        Removes an event from the calendar on a particular day.

        NOTE:
            no sanity checks are done for day.

        IN:
            ev_label - eventlabel of the event to remove
            day - day we should look at for removal
            remove_all - SEE removeEvent_el
        """
        for month in range(1,13):
            if not remove_all and _removeEvent_md(ev_label, month, day):
                return


    def _removeEvent_m(ev_label, month, remove_all=False):
        """
        Removes an event from the calendar in a particular month.

        NOTE:
            no sanity checks are done for month

        IN:
            ev_label - eventlabel of the event to remove
            month - month we should look at for removal
            remove_all - SEE removeEvent_el
        """
        for day in range(1,32):
            if not remove_all and _removeEvent_md(ev_label, month, day):
                return


    def _removeEvent_md(ev_label, month, day):
        """
        Removes an event from the calendar at a precise month / day.

        NOTE: no sanity checks are done for month / day

        IN:
            ev_label - eventlabel of the event to remove
            month - month we should look at for removal
            day - day we should look at for removal

        RETURNS:
            True if we removed something, False otherwise
        """
        ev_tup = _findEvent_md(ev_label, month, day)

        if ev_tup is not None:
            calendar_database[month][day].pop(ev_label)
            return True

        return False


    def _removeRepeatable(identifier):
        """
        Removes a repeatable from teh calendar.

        NOTE: O(n^2) efficiency, please avoid using this.

        IN:
            identifier - identifier of the repeatable to remove
        """
        for month in range(1,13):
            _removeRepeatable_m(identifier, month)


    def _removeRepeatable_d(identifier, day):
        """
        Removes a repeatable from teh calendar in a particular month.

        NOTE: no sanity checks are done for day

        IN:
            identifier - identifier of the repeatable to remove
            day - day we should look at for removal
        """
        for month in range(1,13):
            if _removeRepeatable_md(identifier, month, day):
                return


    def _removeRepeatable_m(identifier, month):
        """
        Removes a repeatable from the calendar in a particular month.

        NOTE: no sanity checks are done for month

        IN:
            identifier - identifier of the repeatable to remove
            month - month we should look at for removal
        """
        for day in range(1,32):
            if _removeRepeatable_md(identifier, month, day):
                return


    def _removeRepeatable_md(identifier, month, day):
        """
        Removes a repeatable from teh calendar at a precise month / day.

        NOTE: no sanity checks are done for month / day

        IN:
            identifider - identifier of the repeatable to remove
            month - month we should look at for removal
            day - day we should look at for removal

        RETURNS:
            True if we removed somethign, False otherwise
        """
        rp_tup = _findRepeatable_md(identifier, month, day)

        if rp_tup is not None:
            calendar_database[month][day].pop(identifier)
            return True

        return False


    def removeEvent(ev):
        """
        Removes an event from the calendar using it's start_date and end_date
        properties.

        IN:
            ev - event to remove
        """
        if ev.start_date is None:
            return

        if ev.end_date is None:
            # no end date means we assume it's a single day to remove
            removeEvent_evdt(ev, ev.start_date)

        else:
            # otherwise we iterate over a range
            _delta = datetime.timedelta(days=1)
            curr_date = ev.start_date

            while curr_date < ev.end_date:
                removeEvent_evdt(ev, curr_date)
                curr_date += _delta


    def removeEvent_eld(ev_label, _date):
        """
        Removes an event from the calendar at a precise date.

        IN:
            ev_label - eventlabel of the event to remove
            _date - datetime.date we should look at for event removal
        """
        _removeEvent_md(ev_label, _date.month, _date.day)


    def removeEvent_evd(ev, _date):
        """
        Removes an event from the calendar at a precise date.

        IN:
            ev - event to remove
            _date - datetime.date we should look at for event removal
        """
        removeEvent_eld(ev.eventlabel, _date)


    def removeEvent_eldt(ev_label, _datetime):
        """
        Removes an event from the calendar at a precise datetime.

        IN:
            ev_label - eventlabel of the event to remove
            _datetime - datetime we should look at for event removal
        """
        removeEvent_eld(ev_label, _datetime.date())


    def removeEvent_evdt(ev, _datetime):
        """
        Removes and event from the calendar at a precise datetime.

        IN:
            ev - event to remove
            _datetime - datetime.date we should look at for removal
        """
        removeEvent_eldt(ev.eventlabel, _datetime)


    def removeEvent_el(ev_label, month=None, day=None, remove_all=False):
        """
        Removes an event from the calendar.

        NOTE: The default params will check EVERY SINGLE calendar spot for the
        event to remove. It is considered HIGHLY INEFFICIENT. Try to use the
        other removeEvent functions if possible, or narrow the search using
        month and day.

        NOTE:
            Using both month and day will do the same check as removeEvent_eld

        IN:
            ev_label - eventlabel of the event to remove
            month - If given (and a valid month), will only check the calendar
                in the given month.
                (Default: None)
            day - If given (and a valid day), will only check the calendar
                for the given day for each month
                (Default: None)
            remove_all - True means we remove every single occurence of the
                given eventlabel. False means we only remove the first one we
                find.
                (Default: False)
        """
        # inital sanity checks
        if month not in range(1,13):
            month = None

        if day not in range(1,32):
            day = None

        # now to see what operation we are doing
        if month is not None and day is not None:
            # ideally we want the user to pass in a month and day
            _removeEvent_md(ev_label, month, day)

        elif month is not None:
            # probably common to clean a month of an event
            _removeEvent_m(ev_label, month, remove_all=remove_all)

        elif day is not None:
            # less common to clean a particular day of each month
            _removeEvent_d(ev_label, day, remove_all=remove_all)

        else:
            # full scan. hopefully no one does this
            _removeEvent(ev_label, remove_all=remove_all)


    def removeEvent_ev(ev, month=None, day=None, remove_all=False):
        """
        Removes an event from the calendar.

        SEE removeEvent_el for important NOTES regarding this function.

        IN:
            ev - event to remove
            month - SEE removeEvent_el
            day - SEE removeEvent_el
            remove_all - SEE removeEvent_el
        """
        removeEvent_el(
            ev.eventlabel,
            month=month,
            day=day,
            remove_all=remove_all
        )


    def removeRepeatable(identifier, month=None, day=None):
        """
        Removes a repeatable from the calendar.

        NOTE: The default params will check EVERY SINGLE calendar spot for the
        repeatable to remove. It is considered HIGHLY INEFFICIENT. Try to use
        the other removeRepeatable functions if possible, or narrow the search
        using month and day.

        IN:
            identifier - identifier of the repeatable to remove
            month - If given (and a valid month), will only check the calendar
                in the given month.
                (Default: None)
            day - If given (and a valid day), will only check the calendar for
                the given day for reach month
                (Default: None)
        """
        # inital sanity checks
        if month not in range(1,13):
            month = None

        if day not in range(1,32):
            day = None

        # now to see which operation we are doing
        if month is not None and day is not None:
            # ideally we want the user to pass in a month and day
            _removeRepeatable_md(identifier, month, day)

        elif month is not None:
            # probably common to clean a month
            _removeRepeatable_m(identifier, month)

        elif day is not None:
            # less common to clean a particular day of a month
            _removeRepeatable_d(identifier, day)

        else:
            # full scan, hopefully no one does this
            _removeRepeatable(identifier)


    def removeRepeatable_d(identifier, _date):
        """
        Removes a repeatable from teh calendar at a precise datetime.date

        IN:
            identifier - identifier of the repeatable to remove
            _date - datetime.date we should look at for removal
        """
        _removeRepeatable_md(identifier, _date.month, _date.day)


    def removeRepeatable_dt(identifier, _datetime):
        """
        Removes a repeatable from teh calendar at aprecise datetime

        IN:
            identifier - identifier of the repeatable to remove
            _datetime - datetime we should look at for removal
        """
        removeRepeatable_d(identifier, _datetime.date())


# add repeatable events
init python:

    import store.mas_calendar as calendar

    calendar.addRepeatable("New years day","New years day",month=1,day=1,year_param=list())
    calendar.addRepeatable("Valentine","Valentine's day",month=2,day=14,year_param=list())
    calendar.addRepeatable("White day","White day",month=3,day=14,year_param=list())
    calendar.addRepeatable("April Fools","Day I become an AI",month=4,day=1,year_param=list())
    calendar.addRepeatable("Monika's Birthday","My Birthday",month=9,day=22,year_param=list())
    calendar.addRepeatable("Halloween","Halloween",month=10,day=31,year_param=list())
    calendar.addRepeatable("Christmas eve","Christmas eve",month=12,day=24,year_param=list())
    calendar.addRepeatable("Christmas","Christmas",month=12,day=25,year_param=list())
    calendar.addRepeatable("New year's eve","New year's eve",month=12,day=31,year_param=list())

    # add inital session
    if (
        persistent.sessions is not None
        and "first_session" in persistent.sessions
        and persistent.sessions["first_session"] is not None
    ):
        calendar.addRepeatable_dt(
            "first_session",
            "<3",
            persistent.sessions["first_session"],
            year_param=[persistent.sessions["first_session"].year]
        )


init 100 python:
    # calendar related but later

    def mas_chgCalEVul(number_of_days):
        """
        Changes the conditionals / actions / and more of the monika start date
        topic so it unlocks after the given number of days

        IN:
            number_of_days - number of days before unlocking the monika start
                date topic
        """
        ev = store.evhand.event_database.get("monika_dating_startdate", None)
        if ev is None:
            return

        # okay we have an event to work with
        _now = datetime.datetime.now()

        ev.conditional = "".join([
            "datetime.datetime.now() - datetime.datetime(",
            str(_now.year),
            ",",
            str(_now.month),
            ",",
            str(_now.day),
            ") >= datetime.timedelta(days=",
            str(number_of_days),
            ")"
        ])
        ev.action = EV_ACT_UNLOCK
        ev.unlocked = False

        if "monika_dating_startdate" in persistent._seen_ever:
            persistent._seen_ever.pop("monika_dating_startdate")


# wrap it up in a screen
screen mas_calendar_screen(select_date=False):

    zorder 51

    add MASCalendar(select_date)
        #xalign 0.5
        #yalign 0.5

label mas_show_calendar_detail(items,area,align,first_item,final_item):
    call screen mas_calendar_events_scrollable_list(items, area, align, first_item=first_item, final_item=final_item)
    return


# Scrollable labels with return. This one takes the following params:
# IN:
#   items - list of items to display in the menu. Each item must be a tuple of
#       the following format:
#           [0]: label text
#           [2]: True if we want the label italics, False if not
#           [3]: True if we want the button bold, False if not
#   display_area - defines the display area of the menu. Tuple of the following
#       format:
#           [0]: x coordinate of menu
#           [1]: y coordinate of menu
#           [2]: width of menu
#           [3]: height of menu
#   scroll_align - alignment of vertical scrollbar
#   first_item - represents the first item(usually the title) of the list
#       tuple of the following format:
#           [0]: text of the button
#           [1]: return value of the button
#           [2]: True if we want the button italics, False if not
#           [3]: True if we want the button bold, False if not
#           [4]: integer spacing between this button and the regular buttons
#               NOTE: must be >= 0
#       (Default: None)
#   final_item - represents the final (usually quit item) of the menu
#       tuple of the following format:
#           [0]: text of the button
#           [1]: return value of the button
#           [2]: True if we want the button italics, False if not
#           [3]: True if we want the button bold, False if not
#           [4]: integer spacing between this button and the regular buttons
#               NOTE: must be >= 0
#       (Default: None)
#   mask - hex color that will be used for the mask that will cover the screen
#       if None there won't be any mask
#   frame - route to the image used as backround for the list
screen mas_calendar_events_scrollable_list(items, display_area, scroll_align, first_item=None, final_item=None, mask="#000000B2", frame="mod_assets/calendar/calendar_bg.png"):
        style_prefix "scrollable_menu"

        zorder 51

        if mask:
            add Solid(mask)

        fixed:
            area display_area
            if frame:
                add Frame(frame, 60, 60)

            bar adjustment prev_adj style "vscrollbar" xalign scroll_align

            viewport:
                yadjustment prev_adj
                mousewheel True

                vbox:

                    if first_item:

                        text _(first_item[0]):
                            if first_item[1]:
                                italic True
                            if first_item[2]:
                                bold True
                            xpos 0.2
                            ypos 0.5

                    null height 30


                    for item_prompt,is_italic,is_bold in items:
                        text item_prompt:
                            if is_italic:
                                italic True
                            if is_bold:
                                bold True
                            xpos 0.05


                    if final_item:
                        if final_item[4] > 0:
                            null height final_item[4]

                        textbutton _(final_item[0]):
                            if final_item[2]:
                                text_italic True
                            if final_item[3]:
                                text_bold True
                            background None
                            hover_sound gui.hover_sound
                            activate_sound gui.activate_sound

                            action Return(final_item[1])


label _first_time_calendar_use:
    m 1eub "Oh, I see you noticed that pretty calendar hanging in the wall, [player]"
    m "It helps me to keep track of important events, ehehe~"
    m 1hua "Here, let me show you."
    show monika 1a

    call mas_start_calendar_read_only

    m 1hua "Pretty cool, right?"
    m 1eua "Feel free to check the calendar whenever you want."
    m 1rksdlb "Except for when I'm in the middle of talking, of course."

    $ store.hkb_button.enabled = True
    $ persistent._mas_first_calendar_check = True
    return

label _mas_start_calendar(select_date=True):

    python:
        HKBHideButtons()

    call screen mas_calendar_screen(select_date)

    python:
        HKBShowButtons()

    return _return

label mas_start_calendar_read_only:
    call _mas_start_calendar(select_date=False)
    return _return

label mas_start_calendar_select_date:
    call _mas_start_calendar(select_date=True)
    return _return

# labels for easy testing
#
# label testing_calendar:
#     m "I'm opening up the calendar"
#     call mas_start_calendar_select_date
#     if _return:
#         m "I got the value [_return]"
#     else:
#         m "You closed without selecting a date"
#     return
