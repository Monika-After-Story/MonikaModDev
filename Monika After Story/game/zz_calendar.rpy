# Calendar

init python:

    import math

    class MASCalendar(renpy.Displayable):
        """
        Calendar
        """

        import pygame
        import datetime

        # CONSTANTS
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        EXIT_BUTTON_WIDTH = 74
        EXIT_BUTTON_HEIGHT = 74
        EXIT_BUTTON_X = 1040
        EXIT_BUTTON_Y = 60

        DAY_BUTTON_WIDTH = 128
        DAY_BUTTON_HEIGHT = 65
        DAY_NAME_BUTTON_HEIGHT = 35

        INITIAL_POSITION_X = 193
        INITIAL_POSITION_Y = 155

        CALENDAR_DAY_TEXT_SIZE = 17

        CALENDAR_CLOSE_X_SIZE = 45

        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )


        def __init__(self, select_date=False):

            # Pass additional properties on to the renpy.Displayable
            # constructor.
            super(renpy.Displayable, self).__init__()

            # The calendar background
            self.calendar_background = renpy.displayable("mod_assets/calendar/calendar_bg.png")

            # Can we select dates?
            self.can_select_date = select_date

            # background tile
            self.background = Solid(
                "#000000B2",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )

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
            button_day_name = Image(
                "mod_assets/calendar/calendar_day_name_bg.png"
            )

            # 440 110
            if select_date:
                self.text_title = Text(
                    "Select a Date",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#ffffff",
                    outlines=[]
                )
            else:
                self.text_title = Text(
                    "Calendar",
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#ffffff",
                    outlines=[]
                )

            days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                "Friday", "Saturday"]

            i = 0
            for day in days:

                button_day_text = Text(
                    day,
                    font=gui.default_font,
                    size=self.CALENDAR_DAY_TEXT_SIZE,
                    color="#ffb0ed",
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
                self.const_buttons.append(button_day_button)
                i = i + 1


            button_text_close = Text(
                "X",
                font=gui.default_font,
                size=self.CALENDAR_CLOSE_X_SIZE,
                color="#ffb0ed",
                outlines=[]
            )

            self.button_exit = MASButtonDisplayable(
                button_text_close,
                button_text_close,
                button_text_close,
                button_close,
                button_close,
                button_close,
                self.EXIT_BUTTON_X,
                self.EXIT_BUTTON_Y,
                self.EXIT_BUTTON_WIDTH,
                self.EXIT_BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value="Close"
            )

            self.const_buttons.append(self.button_exit)
            self._setup_day_buttons()


        def _setup_day_buttons(self):
            self.day_buttons = []
            day = datetime.timedelta(days=1)
            first_day = datetime.datetime(self.selected_year, self.selected_month, 1)

            button_day_bg = Image(
                "mod_assets/calendar/calendar_day_bg.png"
            )

            while first_day.weekday() != 6:
                first_day = first_day - day

            self.dates = []

            for i in range(42):
                self.dates.append(first_day + datetime.timedelta(days=i))

            initial_y = self.INITIAL_POSITION_Y + (self.DAY_NAME_BUTTON_HEIGHT * 2)

            for i in range(6):

                for j in range(7):

                    current_date = self.dates[j + (i * 7)]
                    ret_val = None
                    hover_sound = None
                    activate_sound = None

                    if self.can_select_date and current_date.month == self.selected_month:
                        ret_val = date
                        hover_sound = gui.hover_sound
                        activate_sound = gui.activate_sound

                    day_button_text = Text(
                        str(current_date.day),
                        font=gui.default_font,
                        size=self.CALENDAR_DAY_TEXT_SIZE,
                        color="#ffb0ed",
                        outlines=[]
                    )

                    day_button = MASButtonDisplayable(
                        day_button_text,
                        day_button_text,
                        day_button_text,
                        button_day_bg,
                        button_day_bg,
                        button_day_bg,
                        self.INITIAL_POSITION_X + (j * self.DAY_BUTTON_WIDTH),
                        initial_y + (i * self.DAY_BUTTON_HEIGHT),
                        self.DAY_BUTTON_WIDTH,
                        self.DAY_BUTTON_HEIGHT,
                        hover_sound=hover_sound,
                        activate_sound=activate_sound,
                        return_value=ret_val
                    )

                    self.day_buttons.append(day_button)


        def render(self, width, height, st, at):

            # render mask
            back = renpy.render(self.background, width, height, st, at)

            # Create a render for the background.
            calendar_bg = renpy.render(self.calendar_background, width, height, st, at)

            # Get the size of the child.
            self.width, self.height = calendar_bg.get_size()

            # Create the render we will return.
            r = renpy.Render(width, height)

            r.blit(back,(0,0))

            # Blit (draw) the child's render to our render.
            r.blit(calendar_bg, (192, 103))

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

        def _button_select(self, ev, x, y, st):
            """
            Goes through the list of buttons and return the first non-None
            value returned

            RETURNS:
                first non-none value returned
            """
            for button in self.const_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val

            for button in self.day_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val

            return None


        def event(self, ev, x, y, st):

            if ev.type in self.MOUSE_EVENTS:
                # we only care about mouse
                sel_action = self._button_select(ev, x, y, st)

                if sel_action:
                    # nonNone value returned

                    if sel_action == "Close":
                        # this means the user selected close

                        return ""

                    if isinstance(sel_action, datetime.datetime):

                        return sel_action

            # otherwise continue
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()


screen mas_calendar_screen(select_date=False):

    zorder 51

    add MASCalendar(False)
        #xalign 0.5
        #yalign 0.5

label mas_start_calendar(select_date=False):

    call screen mas_calendar_screen(select_date)

    # return value?
    if _return:

        m "got a return value [_return]"
        return _return

    m "No returned value"

    return
