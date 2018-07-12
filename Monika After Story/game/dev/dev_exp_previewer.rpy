# special module that contains a screen dedicated to expression prevewing. 
# we really needed this lol.

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_exp_previewer",
            category=["dev"],
            prompt="EXP PREVIEW",
            pool=True,
            random=True,
            unlocked=True
        )
    )

label dev_exp_previewer:
    # call a screen
    show monika at t21
    window hide

    $ HKBHideButtons()
    $ prev_mflag = morning_flag
    $ monika_chr.reset_outfit()
    $ morning_flag = True

    $ ui.add(MASExpPreviewer())
    $ result = ui.interact()

    $ monika_chr.reset_outfit()
    $ morning_flag = prev_mflag
    $ HKBShowButtons()

    window auto
    return


init 1000 python:
    class MASExpPreviewer(renpy.Displayable):
        """
        we are about to go there
        """
        import pygame

        # CONSTANTS
        VIEW_WIDTH = 1280
        VIEW_HEIGHT = 720

        MARGIN = 10

        PANEL_X = int((VIEW_WIDTH / 2) + 100)
        PANEL_Y = MARGIN

        PANEL_WIDTH = VIEW_WIDTH - PANEL_X - MARGIN
        PANEL_HEIGHT = VIEW_HEIGHT - (2 * MARGIN)

        ROW_SPACING = 10
        BUTTON_WIDTH = 120
        BUTTON_HEIGHT = 35
        SQ_BUTTON_WIDTH = 35
        SQ_BUTTON_HEIGHT = 35

        ROW_Y_START = 70 + MARGIN
        BUTTON_LX_START  = 150
        BUTTON_RX_START = PANEL_WIDTH - MARGIN - SQ_BUTTON_WIDTH

        # labels x
        # label y is a list generated later
        LBL_X = MARGIN + PANEL_X

        BUTTON_X_DONE = PANEL_X + PANEL_WIDTH - (BUTTON_WIDTH + MARGIN)
        BUTTON_Y_DONE = (PANEL_Y + PANEL_HEIGHT) - (BUTTON_HEIGHT + MARGIN)

        # sprite code y
        # sprite code x is genrated later, since this should be centered
        SC_Y = MARGIN + PANEL_Y

        # x coord to start the selected text
        SEL_TX_X = PANEL_X + BUTTON_LX_START + SQ_BUTTON_WIDTH

        # with of selected text space
        SEL_TX_W = BUTTON_RX_START - (BUTTON_LX_START + SQ_BUTTON_WIDTH)

        TEXT_SIZE = 40

        ROWS = 13

        ### sprite code maps

        # otherwise known as clothes
        TORSO_MAP = {
            "def": "School Uniform"
        }

        # aka pose
        ARMS_MAP = {
            1: "Resting on Hands",
            2: "Crossed",
            3: "Rest Left, Point Right",
            4: "Point Right",
            5: "Leaning",
            6: "Down"
        }

        HAIR_MAP = {
            "def": "Ponytail",
            "down": "Down",
            "bun": "Bun"
        }

        EYE_MAP = {
            "e": "Normal",
            "w": "Wide",
            "s": "Sparkle",
            "t": "Smug",
            "c": "Crazy",
            "r": "Look Right",
            "l": "Look Left",
            "h": "Closed (Happy)",
            "d": "Closed (Sad)"
        }

        EYEBROW_MAP = {
            "f": "Furrowed",
            "u": "Up",
            "k": "Knit",
            "s": "Straight"
        }

        NOSE_MAP = {
            "nd": "Default"
        }

        EYEBAG_MAP = {
            "ebd": "Default"
        }

        BLUSH_MAP = {
            "bl": "Line Blush",
            "bs": "Shade Blush",
            "bf": "Full Blush"
        }

        TEARS_MAP = {
            "ts": "Streaming Tears",
            "td": "Dried Tears"
        }

        SWEAT_MAP = {
            "sdl": "Left Sweat Drop",
            "sdr": "Right Sweat Drop"
        }

        EMOTE_MAP = {
            "ec": "Confusion"
        }

        MOUTH_MAP = {
            "a": "Smile",
            "b": "Open Smile",
            "c": "Straight / Smirk",
            "d": "Small Open",
            "o": "Gasp",
            "u": "Smug",
            "w": "Wide Open",
            "x": "Grit Teeth",
            "p": "Pout",
            "t": "Triangle"
        }

        TIME_MAP = {
            0: "Day",
            1: "Night"
        }

        # sel tex map
        SEL_TX_MAP = {
            "torso": TORSO_MAP,
            "arms": ARMS_MAP,
            "hair": HAIR_MAP,
            "eyes": EYE_MAP,
            "eyebrows": EYEBROW_MAP,
            "nose": NOSE_MAP,
            "eyebags": EYEBAG_MAP,
            "blush": BLUSH_MAP,
            "tears": TEARS_MAP,
            "sweat": SWEAT_MAP,
            "emote": EMOTE_MAP,
            "mouth": MOUTH_MAP,
            "time": TIME_MAP
        }


        ### Available codes
        TORSO_SC = [
            "def"
        ]

        ARMS_SC = [
            1,
            2,
            3,
            4,
            5,
            6
        ]

        HAIR_SC = [
            "def",
            "down",
            "bun"
        ]

        EYE_SC = [
            "e",
            "w",
            "s",
            "t",
            "c",
            "r",
            "l",
            "h",
            "d"
        ]

        EYEBROW_SC = [
            "f",
            "u",
            "k",
            "s"
        ]

        NOSE_DEF = "nd"
        NOSE_SC = [
            "nd"
        ]

        EYEBAG_SC = [
            None,
            "ebd"
        ]

        BLUSH_SC = [
            None,
            "bl",
            "bs",
            "bf"
        ]

        TEARS_SC = [
            None,
            "ts",
            "td"
        ]

        SWEAT_SC = [
            None,
            "sdl",
            "sdr"
        ]

        EMOTE_SC = [
            None,
            "ec"
        ]

        MOUTH_SC = [
            "a",
            "b",
            "c",
            "d",
            "o",
            "u",
            "w",
            "x",
            "p",
            "t"
        ]

        TIME_SC = [
            0,
            1
        ]


        ### Text map
        LABELS = [
            "Clothes: ",
            "Pose: ",
            "Hair: ",
            "Eyes: ",
            "Eyebrows: ",
            "Nose: ",
            "Eyebags: ",
            "Blush: ",
            "Tears: ",
            "Sweat: ",
            "Emote: ",
            "Mouth: ",
            "Time: "
        ]

    
        ### button retvals
        SQ_BUTTON_RETVALS = [
            "torso",
            "arms",
            "hair",
            "eyes",
            "eyebrows",
            "nose",
            "eyebags",
            "blush",
            "tears",
            "sweat",
            "emote",
            "mouth",
            "time"
        ]


        # sprite code map
        SC_MAP = {
            "torso": TORSO_SC,
            "arms": ARMS_SC,
            "hair": HAIR_SC,
            "eyes": EYE_SC,
            "eyebrows": EYEBROW_SC,
            "nose": NOSE_SC,
            "eyebags": EYEBAG_SC,
            "blush": BLUSH_SC,
            "tears": TEARS_SC,
            "sweat": SWEAT_SC,
            "emote": EMOTE_SC,
            "mouth": MOUTH_SC,
            "time": TIME_SC
        }

        # list of keys that matter for a sprite code
        SC_PARTS = [
            "arms",
            "eyes",
            "eyebrows",
            "nose",
            "eyebags",
            "blush",
            "tears",
            "sweat",
            "emote",
            "mouth"
        ]


        # selection text index map
        INDEX_MAP = {
            "torso": 0,
            "arms": 1,
            "hair": 2,
            "eyes": 3,
            "eyebrows": 4,
            "nose": 5,
            "eyebags": 6,
            "blush": 7,
            "tears": 8,
            "sweat": 9,
            "emote": 10,
            "mouth": 11,
            "time": 12
        }

            


        # pygame stuff
        MOUSE_EVENTS = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEBUTTONDOWN
        )



        def __init__(self):
            """
            Creates the Expression previewer displayable
            """
            super(renpy.Displayable, self).__init__()

            # background tile
            self.background = Solid(
                "#000000B2",
                xsize=self.PANEL_WIDTH,
                ysize=self.PANEL_HEIGHT
            )

            ### setup images
            # buttons:
            button_idle = Image("mod_assets/hkb_idle_background.png")
            button_hover = Image("mod_assets/hkb_hover_background.png")
            button_disabled = Image("mod_assets/hkb_disabled_background.png")
            sq_button_idle = Image(
                "mod_assets/buttons/squares/square_idle.png"
            )
            sq_button_hover = Image(
                "mod_assets/buttons/squares/square_hover.png"
            )
            sq_button_disabled = Image(
                "mod_assets/buttons/squares/square_disabled.png"
            )

            # button text
            button_text_left_idle = Text(
                "<",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_left_hover = Text(
                "<",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )
            button_text_right_idle = Text(
                ">",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_right_hover = Text(
                ">",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )

            # calculat positions
            button_lx = self.PANEL_X + self.BUTTON_LX_START
            button_rx = self.PANEL_X + self.BUTTON_RX_START
            # 14 options:
            # torso
            # arms
            # hair
            # eyes
            # eyebrows
            # tears
            # nose
            # eyebags
            # blush
            # tears
            # sweat
            # emote
            # mouth
            # day / night

            # button y coords
            self.button_ly_list = [
                self.ROW_Y_START + (
                    x * (self.ROW_SPACING + self.SQ_BUTTON_HEIGHT)
                )
                for x in range(self.ROWS)
            ]
            self.button_ry_list = list(self.button_ly_list)

            # actual left buttons
            self.button_ls = [
                MASButtonDisplayable(
                    button_text_left_idle,
                    button_text_left_hover,
                    button_text_left_idle,
                    sq_button_idle,
                    sq_button_hover,
                    sq_button_disabled,
                    button_lx,
                    self.button_ly_list[x],
                    self.SQ_BUTTON_WIDTH,
                    self.SQ_BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound,
                    return_value=self.SQ_BUTTON_RETVALS[x]
                )
                for x in range(self.ROWS)
            ]

            # actual right buttons
            self.button_rs = [
                MASButtonDisplayable(
                    button_text_right_idle,
                    button_text_right_hover,
                    button_text_right_idle,
                    sq_button_idle,
                    sq_button_hover,
                    sq_button_disabled,
                    button_rx,
                    self.button_ry_list[x],
                    self.SQ_BUTTON_WIDTH,
                    self.SQ_BUTTON_HEIGHT,
                    hover_sound=gui.hover_sound,
                    activate_sound=gui.activate_sound,
                    return_value=self.SQ_BUTTON_RETVALS[x]
                )
                for x in range(self.ROWS)
            ]

            # disable buttons that arent needed
            self._disable_singles()

            # Done button
            button_text_done_idle = Text(
                "Done",
                font=gui.default_font,
                size=gui.text_size,
                color="#000",
                outlines=[]
            )
            button_text_done_hover = Text(
                "Done",
                font=gui.default_font,
                size=gui.text_size,
                color="#fa9",
                outlines=[]
            )
    
            self.button_done = MASButtonDisplayable(
                button_text_done_idle,
                button_text_done_hover,
                button_text_done_idle,
                button_idle,
                button_hover,
                button_disabled,
                self.BUTTON_X_DONE,
                self.BUTTON_Y_DONE,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            # have all buttons so render is faster
            self.all_buttons = list()
            self.all_buttons.extend(self.button_ls)
            self.all_buttons.extend(self.button_rs)
            self.all_buttons.append(self.button_done)

            ## texts

            # category labels
            # text poisiotns
            self.lbl_y_list = [
                self.ROW_Y_START + (
                    x * (self.ROW_SPACING + self.SQ_BUTTON_HEIGHT)
                )
                for x in range(self.ROWS)
            ]

            # and actual text labels
            self.labels = [
                Text(
                    lbl,
                    font=gui.default_font,
                    size=gui.text_size,
                    color="#ffe6f4",
                    outlines=[]
                )
                for lbl in self.LABELS
            ]

            
            # sprite code text is generated on the FLY 


            ### selection map

           # map of directional functions to sprite piece
            self._selectors = {
                "arms": self._sel_arms,
                "blush": self._sel_blush,
                "emote": self._sel_emote,
                "eyes": self._sel_eyes,
                "eyebags": self._sel_eyebags,
                "eyebrows": self._sel_eyebrows,
                "hair": self._sel_hair,
                "mouth": self._sel_mouth,
                "nose": self._sel_nose,
                "sweat": self._sel_sweat,
                "tears": self._sel_tears,
                "time": self._sel_time,
                "torso": self._sel_torso
            }

            # current selection of items
            # this needs to be a dict
            # this should be set to default options
            self.curr_sel = {
                "arms": 0,
                "blush": 0,
                "emote": 0,
                "eyes": 0,
                "eyebags": 0,
                "eyebrows": 1,
                "hair": 0,
                "mouth": 0,
                "nose": 0,
                "sweat": 0,
                "tears": 0,
                "time": 0,
                "torso": 0
            }

            # build the Text objects
            self.curr_sel_txts = self._build_sel_texts()

            # current sprite code as a string
            self.curr_spr_code = self._build_spr_code()

            # did the sprite chnage?
            self.sprite_changed = True


        def _adj_sel(self, direct, key):
            """
            Generically does a selection change.

            IN:
                direct - direction to move
                key - key to use in selection map
            """
            self.curr_sel[key] = self._select(
                self.SC_MAP[key],
                direct,
                self.curr_sel[key]
            )

           
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


        def _seltx_xcenter(self, width):
            """
            Returns appropraite X location to center the selection text object
            with the given width.

            NOTE: This is soley meant for use with selection text 

            IN:
                with - width of the selection text

            RETURNS:
                appropraite X coord to center
            """
            return self._xcenter(self.SEL_TX_W, width) + self.SEL_TX_X


        def _select(self, choices, direct, currdex):
            """
            Returns the index of the next possible selection, given a direction

            IN:
                choices - list of choices we have
                direct - direction to move in (+ -> / - <-)
                currdex - cureent index

            RETURNS:
                index of the next selection
            """
            if len(choices) <= 1 or direct == 0:
                # only 1 choice? just return 0
                return 0

            if direct > 0:
                # lets move right
                currdex += 1

                if currdex >= len(choices):
                    # went past right, wrap to left
                    currdex = 0

            elif direct < 0:
                # lets move left
                currdex -= 1

                if currdex < 0:
                    # went past left, wrap to right
                    currdex = len(choices) - 1

            return currdex


        def _left_button_select(self, ev, x, y, st):
            """
            Process a left button click

            RETURNS:
                True if we processed a left button click. False otherwise
            """
            for button in self.button_ls:
                ret_val = button.event(ev, x, y, st)
                if ret_val is not None:
                    self._selectors[ret_val](-1)
                    self.sprite_changed = True
                    return True

            return False


        def _right_button_select(self, ev, x, y, st):
            """
            Process a right button click

            RETURNS:
                True if we processed a right button click. False otherwise
            """
            for button in self.button_rs:
                ret_val = button.event(ev, x, y, st)
                if ret_val is not None:
                    self._selectors[ret_val](1)
                    self.sprite_changed = True
                    return True

            return False


        ############## selection map functions ###############################
        ## all of these functions are given a direction param
        # If the direct is positive, selection is moved right.
        # otherwise, direct is moved left

        def _sel_arms(self, direct): 
            self._adj_sel(direct, "arms")
            self._update_spr_code()
            self._update_sel_tx("arms")


        def _sel_blush(self, direct):
            self._adj_sel(direct, "blush")
            self._update_spr_code()
            self._update_sel_tx("blush")


        def _sel_emote(self, direct):
            self._adj_sel(direct, "emote")
            self._update_spr_code()
            self._update_sel_tx("emote")


        def _sel_eyes(self, direct):
            self._adj_sel(direct, "eyes")
            self._update_spr_code()
            self._update_sel_tx("eyes")


        def _sel_eyebags(self, direct):
            self._adj_sel(direct, "eyebags")
            self._update_spr_code()
            self._update_sel_tx("eyebags")


        def _sel_eyebrows(self, direct):
            self._adj_sel(direct, "eyebrows")
            self._update_spr_code()
            self._update_sel_tx("eyebrows")


        def _sel_hair(self, direct):
            self._adj_sel(direct, "hair")
            self._update_sel_tx("hair")
            monika_chr.change_hair(self._get_spr_code("hair"))


        def _sel_mouth(self, direct):
            self._adj_sel(direct, "mouth")
            self._update_spr_code()
            self._update_sel_tx("mouth")


        def _sel_nose(self, direct):
            self._adj_sel(direct, "nose")
            self._update_spr_code()
            self._update_sel_tx("nose")


        def _sel_sweat(self, direct):
            self._adj_sel(direct, "sweat")
            self._update_spr_code()
            self._update_sel_tx("sweat")


        def _sel_tears(self, direct):
            self._adj_sel(direct, "tears")
            self._update_spr_code()
            self._update_sel_tx("tears")
       

        def _sel_time(self, direct):
            self._adj_sel(direct, "time")
            self._update_sel_tx("time")
            global morning_flag
            morning_flag = self.curr_sel["time"] == 0


        def _sel_torso(self, direct):
            self._adj_sel(direct, "torso")
            self._update_sel_tx("torso")
            monika_chr.change_clothes(self._get_spr_code("torso"))


        ######################### button functions ###########################

        def _disable_singles(self):
            """
            Goes through the left / right button lists and disables buttons
            that only have single selection avaialble
            """
            for button in self.button_ls:
                if len(self.SC_MAP[button.return_value]) < 2:
                    button.disable()

            for button in self.button_rs:
                if len(self.SC_MAP[button.return_value]) < 2:
                    button.disable()


        ############################# selection text functions ###############
       
    
        def _build_sel_tx(self, key):
            """
            Builds a Text object using the given key

            IN:
                key - key to build text object

            RETURNS:
                text object
            """
            return Text(
                self._get_sel_tx(key),
                font=gui.default_font,
                size=gui.text_size,
                color="#ffe6f4",
                outlines=[]
            )


        def _build_sel_texts(self):
            """
            Builds a list of Text objects using the current selection map

            RETURNS:
                list of Text objects, in proper display order
            """
            return [
                self._build_sel_tx(key)
                for key in self.SQ_BUTTON_RETVALS
            ]


        def _get_sel_tx(self, key):
            """
            Gets the selection text for a given sprite key

            IN:
                key - what sprite do we need selection text for

            RETURNS:
                the selection text for that sprite
            """
            # How this works:
            # 1. SEL_TX_MAP has the selection text for a sprite code
            spr_code = self._get_spr_code(key, nose=False)

            if spr_code is None:
                return "None"

            return self.SEL_TX_MAP[key][spr_code]


        def _update_sel_tx(self, key):
            """
            Updates the selection for a given key:

            IN:
                key - key to update selection text
            """
            self.curr_sel_txts[self.INDEX_MAP[key]] = self._build_sel_tx(key)


        ######################## sprite code functions #######################


        def _build_spr_code(self):
            """
            Builds sprite code using the current selection map

            RETURNS:
                the current sprite code
            """
            _codes = list()
            for key in self.SC_PARTS:
                spr_code = self._get_spr_code(key)
                if spr_code is not None:
                    _codes.append(str(spr_code))

            return "".join(_codes)


        def _get_spr_code(self, key, nose=True):
            """
            Get sprite code for a given sprite key

            IN:
                key - what sprite code do we need 
                nose - set to True to do special handling for the nose
                    (effectilye make the default nose work with sprite code),
                    False will retrive it raw
                    (Default: True)

            RETURNS:
                the sprite code we need
            """
            # HOW this works:
            # 1. curr_sel has the index for the current selection for a sprite
            # 2. SC_MAP has the lists of sprite codes arranged by index
            spr_code = self.SC_MAP[key][self.curr_sel[key]]
            if nose and spr_code == self.NOSE_DEF:
                return None

            return spr_code


        def _update_spr_code(self):
            """
            Updates sprite code using the current selection map
            """
            self.curr_spr_code = self._build_spr_code()


        ####################### render / event ###############################


        def render(self, width, height, st, at):
            """
            RENDER
            """
            # renders
            back = renpy.render(self.background, width, height, st, at)

            # buttons
            r_buttons = [
                (
                    x.render(width, height, st, at),
                    (x.xpos, x.ypos)
                )
                for x in self.all_buttons
            ]

            # do both text and sel texts together for efficiency
            r_texts = list()
            r_sel_txts = list()
            for x in range(self.ROWS):

                # text
                r_texts.append((
                    renpy.render(self.labels[x], width, height, st, at),
                    (self.LBL_X, self.lbl_y_list[x])
                ))

                # selected text
                _r_sel_tx = renpy.render(
                    self.curr_sel_txts[x], 
                    width, 
                    height, 
                    st, 
                    at
                )

                rst_w, rst_h = _r_sel_tx.get_size()
                
                r_sel_txts.append((
                    _r_sel_tx,
                    (self._seltx_xcenter(rst_w), self.lbl_y_list[x])
                ))


            # sprite code 
            spr_txt = Text(
                "Sprite Code: " + self.curr_spr_code,
                font=gui.default_font,
                size=self.TEXT_SIZE,
                color="#ffe6f4",
                outlines=[]
            )
            r_spr_code = renpy.render(spr_txt, width, height, st, at)


            # and blit
            r = renpy.Render(width, height)
            r.blit(back, (self.PANEL_X, self.PANEL_Y))
            r.blit(r_spr_code, (self.LBL_X, self.SC_Y))
            for vis_t, xy in r_texts:
                r.blit(vis_t, xy)
            for vis_t, xy in r_sel_txts:
                r.blit(vis_t, xy)
            for vis_b, xy in r_buttons:
                r.blit(vis_b, xy)

            if self.sprite_changed:
                renpy.show(str("monika " + self.curr_spr_code))
                renpy.restart_interaction()
                self.sprite_changed = False

            return r


        def event(self, ev, x, y, st):
            """
            EVENT
            """
            if ev.type in self.MOUSE_EVENTS:

                if self.button_done.event(ev, x, y, st):
                    # testing we done
                    return True

                # othrewise, check left buttons
                if not self._left_button_select(ev, x, y, st):
                    self._right_button_select(ev, x, y, st)

                # rereender
                renpy.redraw(self, 0)

            # otherwise continue
            raise renpy.IgnoreEvent()
