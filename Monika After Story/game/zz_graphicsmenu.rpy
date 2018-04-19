# graphics selection menu
# we do this instead of the actual one because the real one breaks everything

image mas_dimmed_back = Solid("#000000B2")

transform mas_entire_screen:
    size (1280, 720)

init python in mas_gmenu:

    # this will be true if a renderer has been selected
#    renderer_selected = False

    # this is the selected renderre
    sel_rend = ""

init -1 python:
    
    # custom graphics menu
    class MASGraphicsMenu(renpy.Displayable):
        """
        Custom graphics menu
        """
        import pygame

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

        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )

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
                "Select a renderer to use:",
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self.text_restart = Text(
                "*Changing the renderer requires a restart to take effect",
                font=gui.default_font,
                size=small_text_size,
                color="#ffe6f4",
                outlines=[]
            )
            self.text_current = Text(
                "Current Renderer:",
                font=gui.default_font,
                size=small_text_heading,
                color="#ffe6f4",
                outlines=[]
            )

            # current render display text
            _renderer = self.RENDER_MAP.get(
                self.curr_renderer, 
                self.RENDER_UNK
            )

            self.text_curr_display = Text(
                _renderer,
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[(1, "#ff99D2")]
            )

            # grouped buttons
            self.all_buttons = [
                self.button_auto,
                self.button_gl,
                self.button_dx,
                self.button_sw,
                self.button_ret
            ]

            if not renpy.windows:
                # non windows does not have angle
                self.all_buttons.remove(self.button_dx)

            # disable a button
            if self.curr_renderer == "auto":
                self.button_auto.disable()

            elif self.curr_renderer == "angle":
                self.button_dx.disable()

            elif self.curr_renderer == "gl":
                self.button_gl.disable()

            elif self.curr_renderer == "sw":
                self.button_sw.disable()


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


        def _button_select(self, ev, x, y, st):
            """
            Goes through the list of buttons and return the first non-None 
            value returned

            RETURNS:
                first non-none value returned
            """
            for button in self.all_buttons:
                ret_val = button.event(ev, x, y, st)
                if ret_val:
                    return ret_val

            return None


        def render(self, width, height, st, at):
            """
            RENDER
            """
            # first, do some renders
            back = renpy.render(self.background, width, height, st, at)

            # buttons
            r_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in self.all_buttons
            ]

            # text
            r_txt_ins = renpy.render(self.text_instruct, width, height, st, at)
            r_txt_res = renpy.render(self.text_restart, width, height, st, at)
            r_txt_cur = renpy.render(self.text_current, width, height, st, at)
            r_txt_curd = renpy.render(
                self.text_curr_display,
                width,
                height,
                st,
                at
            )

            # now do some calcs
            insw, insh = r_txt_ins.get_size()
            resw, resh = r_txt_res.get_size()
            curw, curh = r_txt_cur.get_size()
            curdw, curdh = r_txt_curd.get_size()

            insx = self._xcenter(width, insw)
            resx = self._xcenter(width, resw)
            curx = self._xcenter(width, curw)
            curdx = self._xcenter(width, curdw)

            # now we blit!
            r = renpy.Render(width, height)
            r.blit(back, (0, 0))
            r.blit(r_txt_ins, (insx, self.TEXT_L1_Y_START))
            r.blit(r_txt_res, (resx, self.TEXT_L2_Y_START))
            r.blit(r_txt_cur, (curx, self.TEXT_CURR_L1_Y_START))
            r.blit(r_txt_curd, (curdx, self.TEXT_CURR_L2_Y_START))
            for vis_b, xy in r_buttons:
                r.blit(vis_b, xy)

            return r

        def event(self, ev, x, y, st):
            """
            EVENT
            """
            if ev.type in self.MOUSE_EVENTS:
                # we only care about mousu

                sel_rend = self._button_select(ev, x, y, st)

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

            # otherwise continue
            renpy.redraw(self, 0)
            raise renpy.IgnoreEvent()



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

    add "gui/overlay/confirm.png"

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
