# graphics selection menu
# we do this instead of the actual one because the real one breaks everything

image mas_dimmed_back = Solid("#000000B2")

transform mas_entire_screen:
    size (1280, 720)

init -1 python:
    
    # custom graphics menu
    class MASGraphicsMenu(renpy.Displayable):
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
        TEXT_CURR_Y_START = 220 # current renderer line

        # RENDER MAP
        RENDER_MAP = {
            "auto": "Automatic",
            "gl": "OpenGL",
            "dx": "Angle/DirectX",
            "sw": "Software"
        }
        RENDER_UNK = "Unknown"

        def __init__(self, curr_renderer):
            """
            Constructor
            """
            super(renpy.Displayable, self).__init__()

            self.curr_renderer = curr_renderer

            # background tile
            self.background = Solid(
                "#000000B2",
                xsize=self.VIEW_WIDTH,
                ysize=self.VIEW_HEIGHT
            )

            # button backs
            button_idle = Image(
                "gui/button/scrollable_menu_idle_background.png"
            )
            button_hover = Image(
                "gui/button/scrollable_menu_hover_background.png"
            )
            button_disable = Image(
                "gui/button/scrollable_menu_disable_background.png"
            )

            # Auto button
            button_text_auto_idle = Text(
                "Automatically Choose",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_auto_hover = Text(
                "Automatically Choose",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # GL button
            button_text_gl_idle = Text(
                "OpenGL",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_gl_hover = Text(
                "OpenGL",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # DirectX button
            button_text_dx_idle = Text(
                "Angle/DirectX",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_dx_hover = Text(
                "Angle/DirectX",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # Software button
            button_text_sw_idle = Text(
                "Software",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_sw_hover = Text(
                "Software",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # Return button
            button_text_ret_idle = Text(
                "Return",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_ret_hover = Text(
                "Return",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # calculate positions
            # top left x,y of button area
            button_x = int((self.VIEW_WIDTH - self.BUTTON_WIDTH) / 2)
            button_y = self.BUTTON_Y_START

            # create teh buttons
            self.button_auto = MASButtonDisplayable(
                button_text_auto_idle,
                button_text_auto_hover,
                button_text_auto_idle,
                button_idle,
                button_hover,
                button_disable,
                button_x,
                button_y,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value="auto"
            )
            self.button_gl = MASButtonDisplayable(
                button_text_gl_idle,
                button_text_gl_hover,
                button_text_gl_idle,
                button_idle,
                button_hover,
                button_disable,
                button_x,
                button_y + self.BUTTON_SPACING + self.BUTTON_HEIGHT,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value="gl"
            )
            self.button_dx = MASButtonDisplayable(
                button_text_dx_idle,
                button_text_dx_hover,
                button_text_dx_idle,
                button_idle,
                button_hover,
                button_disable,
                button_x,
                button_y + (2 * (self.BUTTON_SPACING + self.BUTTON_HEIGHT)),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value="angle"
            )
            self.button_sw = MASButtonDisplayable(
                button_text_sw_idle,
                button_text_sw_hover,
                button_text_sw_idle,
                button_idle,
                button_hover,
                button_disable,
                button_x,
                button_y + (3 * (self.BUTTON_SPACING + self.BUTTON_HEIGHT)),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value="sw"
            )
            self.button_ret = MASButtonDisplayable(
                button_text_ret_idle,
                button_text_ret_hover,
                button_text_ret_idle,
                button_idle,
                button_hover,
                button_disable,
                button_x,
                button_y + (4 * self.BUTTON_HEIGHT) + (5 * self.BUTTON_SPACING),
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound,
                return_value=self.curr_renderer
            )

            # texts
            small_text_size = 18
            small_text_heading = 20
            self.text_instruct = Text(
                "Select a renderer to use:"
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self.text_restart = Text(
                "*Changing the renderer requires a restart to take effect"
                font=gui.default_font,
                size=small_text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self.text_current = Text(
                "Current Renderer:"
                font=gui.default_font,
                size=small_text_heading,
                color="#ffe6f4",
                outlines=[]
            )

            # current render display text
            _renderer = self.RENDER_MAP.get(self.curr_renderer, None)
            if not _renderer:
                _renderer = self.RENDER_UNK

            self.text_curr_display = Text(
                _renderer,
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[(1, "#ff99D2")]
            )

            # grouped buttons
            self.all_buttons = (
                self.button_auto,
                self.button_gl,
                self.button_dx,
                self.button_sw,
                self.button_ret
            )

        # okay continue this later
