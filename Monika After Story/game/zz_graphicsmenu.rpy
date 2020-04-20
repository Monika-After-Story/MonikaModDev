# graphics selection menu
# we do this instead of the actual one because the real one breaks everything

image mas_dimmed_back = Solid("#000000B2")

style graphics_menu_choice_button is choice_button:
    padding (5, 5, 5, 5)

transform mas_entire_screen:
    size (1280, 720)

init python in mas_gmenu:

    # this will be true if a renderer has been selected
#    renderer_selected = False

    # this is the selected renderre
    sel_rend = ""

init -1 python:
    from renpy.display.layout import Container
    from renpy.display.behavior import TextButton

    # custom graphics menu
    class MASGraphicsMenu(Container):
        """
        Custom graphics menu
        """

        # CONSTANTS
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        BUTTON_SPACING = 20
        BUTTON_WIDTH = 400
        BUTTON_HEIGHT = 35

        BUTTON_Y_START = 300 # 300 pixels down from the top.
        TEXT_L1_Y_START = 150 # description line
        TEXT_L2_Y_START = 185
        TEXT_CURR_L1_Y_START = 220 # current renderer line
        TEXT_CURR_L2_Y_START = 255

        # RENDER MAP
        RENDER_MAP = {
            "auto": "Automatic",
            "gl": "OpenGL",
            "angle": "Angle/DirectX",
            "sw": "Software"
        }
        RENDER_UNK = "Unknown"

        def __init__(self, curr_renderer, **properties):
            """
            Constructor
            """
            super(MASGraphicsMenu, self).__init__(**properties)

            self.curr_renderer = curr_renderer

            # background tile
            background = Solid(
                "#000000B2",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )
            self.add(background)

            # calculate positions
            # top left x,y of button area
            button_x = int((self.VIEW_WIDTH - self.BUTTON_WIDTH) / 2)
            button_y = self.BUTTON_Y_START

            # create teh buttons
            button_auto = TextButton("Automatically Choose",
                style=style.graphics_menu_choice_button,
                text_style=style.choice_button_text,
                pos=(button_x, button_y),
                xysize=(self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                clicked=lambda: self._select_renderer("auto")
            )
            self.add(button_auto)

            button_gl = TextButton("OpenGL",
                style=style.graphics_menu_choice_button,
                text_style=style.choice_button_text,
                pos=(button_x, button_y + self.BUTTON_SPACING + self.BUTTON_HEIGHT),
                xysize=(self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                clicked=lambda: self._select_renderer("gl")
            )
            self.add(button_gl)

            if renpy.windows:
                button_dx = TextButton("Angle/DirectX",
                    style=style.graphics_menu_choice_button,
                    text_style=style.choice_button_text,
                    pos=(button_x, button_y + 2 * (self.BUTTON_SPACING + self.BUTTON_HEIGHT)),
                    xysize=(self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                    clicked=lambda: self._select_renderer("angle")
                )
                self.add(button_dx)

            button_sw = TextButton("Software",
                style=style.graphics_menu_choice_button,
                text_style=style.choice_button_text,
                pos=(button_x, button_y + 3 * (self.BUTTON_SPACING + self.BUTTON_HEIGHT)),
                xysize=(self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                clicked=lambda: self._select_renderer("sw")
            )
            self.add(button_sw)

            button_ret = TextButton("Return",
                style=style.graphics_menu_choice_button,
                text_style=style.choice_button_text,
                pos=(button_x, button_y + (4 * self.BUTTON_HEIGHT) + (5 * self.BUTTON_SPACING)),
                xysize=(self.BUTTON_WIDTH, self.BUTTON_HEIGHT),
                clicked=lambda: self._select_renderer(self.curr_renderer)
            )
            self.add(button_ret)

            # texts
            small_text_size = 18
            small_text_heading = 20

            text_instruct = Text(
                "Select a renderer to use:",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[],
                xalign=0.5,
                ypos=150
            )
            self.add(text_instruct)

            text_restart = Text(
                "*Changing the renderer requires a restart to take effect",
                font=gui.default_font,
                size=small_text_size,
                color="#ffe6f4",
                outlines=[],
                xalign=0.5,
                ypos=185
            )
            self.add(text_restart)

            text_current = Text(
                "Current Renderer:",
                font=gui.default_font,
                size=small_text_heading,
                color="#ffe6f4",
                outlines=[],
                xalign=0.5,
                ypos=225
            )
            self.add(text_current)

            # current render display text
            _renderer = self.RENDER_MAP.get(
                self.curr_renderer,
                self.RENDER_UNK
            )

            text_curr_display = Text(
                _renderer,
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[(1, "#ff99D2")],
                xalign=0.5,
                ypos=255
            )
            self.add(text_curr_display)

            # disable a button
            if self.curr_renderer == "auto":
                button_auto.clicked = None

            elif self.curr_renderer == "gl":
                button_gl.clicked = None

            elif self.curr_renderer == "angle":
                button_dx.clicked = None

            elif self.curr_renderer == "sw":
                button_sw.clicked = None


        def _select_renderer(self, sel_rend):
            """
            Select renderer.
            """
            if sel_rend:
                # nonNone value returned

                if sel_rend == self.curr_renderer:
                    # this means the user selected back

                    return sel_rend

                # otherwise, user selected a renderer, display the
                # confirmation screen
                store.mas_gmenu.sel_rend = self.RENDER_MAP.get(
                    sel_rend,
                    self.RENDER_UNK
                )
                confirmed = renpy.call_in_new_context(
                    "mas_gmenu_confirm_context"
                )

                if confirmed:
                    # selection made and confirmed
                    return sel_rend

            return None


# label for new context for confirm screen
label mas_gmenu_confirm_context:
    call screen mas_gmenu_confirm(store.mas_gmenu.sel_rend)
    return _return

# confirmation screen for renderer selection
screen mas_gmenu_confirm(sel_rend):
    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _("Switch renderer to " + sel_rend + "?"):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes") action Return(True)
                textbutton _("No") action Return(False)

# gmenu flow start
label mas_gmenu_start:

    # first, retrieve teh current rendeer
    $ curr_render = renpy.config.renderer

    # setup the displayable
    $ ui.add(MASGraphicsMenu(curr_render))
    $ sel_render = ui.interact()

    if sel_render != curr_render:
        # a different renderer was selected, time to adjust the environment
        python:
            env_file = config.basedir + "/environment.txt"
            env_file = env_file.replace("\\", "/")
            env_var = 'RENPY_RENDERER="{0}"'

            if sel_render == "auto":
                # auto pick render, which means we should just remove the
                # env file
                try:
                    os.remove(env_file)

                except:
                    # failure to remove file, open the file and write to it
                    with open(env_file, "w") as outfile:
                        outfile.write(env_var.format("auto"))

            else:
                # otherwise, new renderer, please write the file
                with open(env_file, "w") as outfile:
                    outfile.write(env_var.format(sel_render))

        # now with a new renderer selected, quit
        call screen mas_generic_restart
        $ persistent.closed_self = True
        jump _quit

    return

label mas_choose_renderer_override:
    # if we do this somehow, just quit immediately.
    jump _quit
