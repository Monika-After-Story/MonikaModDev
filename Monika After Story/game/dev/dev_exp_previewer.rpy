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
            unlocked=True
        )
    )

label dev_exp_previewer:
    # show monika at t21
    hide monika
    window hide

    python hide:
        HKBHideButtons()
        prev_flt = store.mas_sprites.get_filter()
        # store.mas_sprites.set_filter(store.mas_sprites.FLT_DAY)
        prev_zoom = store.mas_sprites.zoom_level
        store.mas_sprites.reset_zoom()
        prev_moni_state = monika_chr.save_state(True, True, True)
        monika_chr.reset_outfit()

        ui.add(MASExpPreviewer())
        result = ui.interact()

        monika_chr.reset_outfit()
        monika_chr.load_state(prev_moni_state)
        store.mas_sprites.zoom_level = prev_zoom
        store.mas_sprites.adjust_zoom()
        store.mas_sprites.set_filter(prev_flt)
        HKBShowButtons()

    show monika at i11
    window auto

    return


init 999 python:
    class MASExpPreviewer(renpy.Displayable):
        """
        we are about to go there
        """
        import pygame
        import store.mas_sprites as mas_sprites

        # CONSTANTS
        VIEW_WIDTH = config.screen_width
        VIEW_HEIGHT = config.screen_height

        MARGIN = 10

        PANEL_X = int((VIEW_WIDTH // 2) + 100)
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

        BUTTON_X_COPY = PANEL_X + MARGIN
        BUTTON_Y_COPY = (PANEL_Y + PANEL_HEIGHT) - (BUTTON_HEIGHT + MARGIN)

        BUTTON_X_PASTE = BUTTON_X_COPY + BUTTON_WIDTH + MARGIN
        BUTTON_Y_PASTE = BUTTON_Y_COPY

        BUTTON_X_RESET = BUTTON_X_PASTE + BUTTON_WIDTH + MARGIN
        BUTTON_Y_RESET = BUTTON_Y_COPY

        BUTTON_X_DONE = PANEL_X + PANEL_WIDTH - (BUTTON_WIDTH + MARGIN)
        BUTTON_Y_DONE = BUTTON_Y_COPY

        # sprite code y
        # sprite code x is genrated later, since this should be centered
        SC_Y = MARGIN + PANEL_Y

        # x coord to start the selected text
        SEL_TX_X = PANEL_X + BUTTON_LX_START + SQ_BUTTON_WIDTH

        # with of selected text space
        SEL_TX_W = BUTTON_RX_START - (BUTTON_LX_START + SQ_BUTTON_WIDTH)

        TEXT_SIZE = 40

        SPR_FOUND = "#ffe6f4"

        MONI_X = 0
        MONI_Y = 0

        # STATES for which monika to show

        # use blit to render monika
        STATE_VALID = 1
        # use show + interaction to render monika
        STATE_INVALID = 0

        ### image name maps
        # for building the real deal sprites

        # list of leaning poses so we know
        # format:
        #   [0]: lean
        #   [1]: arm
        LEAN_SMAP = {
            "5": ("def", "def")
        }

        # Map between sprite code letters and image names
        IMG_NAMES_MAP = {
            "arms": mas_sprite_decoder.ARM_MAP,
            "eyes": mas_sprite_decoder.EYE_MAP,
            "eyebrows": mas_sprite_decoder.EYEBROW_MAP,
            "nose": {
                "nd": "def"
            },
            "eyebags": {
                "ebd": "def"
            },
            "blush": mas_sprite_decoder.BLUSH_MAP,
            "tears": mas_sprite_decoder.TEAR_MAP,
            "sweat": mas_sprite_decoder.SWEAT_MAP,
            # "emote": {
            #     "ec": "confuse"
            # },
            "mouth": mas_sprite_decoder.MOUTH_MAP
        }
        # Same as above, but reversed - image names to sprite code letters
        REVERSE_IMG_NAMES_MAP = {key: {v: k for k, v in sub_map.iteritems()} for key, sub_map in IMG_NAMES_MAP.iteritems()}

        ### sprite code maps
        SEL_TX_MAP = {
            "arms": {
                "1": "Resting on Hands",
                "2": "Crossed",
                "3": "Rest Left, Point Right",
                "4": "Point Right",
                "5": "Leaning",
                "6": "Down",
                "7": "Down Left, Point Right",
            },
            "eyes": {
                "e": "Normal",
                "w": "Wide",
                "s": "Sparkle",
                "t": "Smug",
                "c": "Crazy",
                "r": "Look Right",
                "l": "Look Left",
                "h": "Closed (Happy)",
                "d": "Closed (Sad)",
                "k": "Wink Left",
                "n": "Wink Right",
                "f": "Soft",
                "m": "Smug Left",
                "g": "Smug Right",
            },
            "eyebrows": {
                "f": "Furrowed",
                "u": "Up",
                "k": "Knit",
                "s": "Straight",
                "t": "Thinking"
            },
            "nose": {
                "nd": "Default"
            },
            "eyebags": {
                "ebd": "Default"
            },
            "blush": {
                "bl": "Line Blush",
                "bs": "Shade Blush",
                "bf": "Full Blush"
            },
            "tears": {
                "ts": "Streaming Tears",
                "td": "Dried Tears",
                "tp": "Pooled Tears",
                "tu": "Tearing Up",
                "tl": "Tearing Up (Left)",
                "tr": "Tearing Up (Right)",
            #    "th": "Closed Happy Tears",
            #    "tc": "Closed Sad Tears",
            },
            "sweat": {
                "sdl": "Left Sweat Drop",
                "sdr": "Right Sweat Drop"
            },
            # "emote": {
            #     "ec": "Confusion"
            # },
            "mouth": {
                "a": "Smile",
                "b": "Open Smile",
                "c": "Straight / Smirk",
                "d": "Small Open",
                "o": "Gasp",
                "u": "Smug",
                "w": "Wide Open",
                "x": "Grit Teeth",
                "p": "Pout",
                "t": "Triangle",
            #    "g": "Disgust",
            },
            "torso": {
                "def": "School Uniform",
                "blazerless": "S. Uniform (Blazerless)",
                "marisa": "Witch Costume",
            #    "rin": "Neko Costume",
                "santa": "Santa Monika",
                "sundress_white": "Sundress (White)",
                "blackdress": "Formal Dress (Black)",
            },
            "hair": {
                "def": "Ponytail",
                "down": "Down",
            #    "bun": "Bun"
            },
            "time": {
                "day": "Day",
                "night": "Night"
            }
        }

        ### Text map
        LABELS = [
            "Pose: ",
            "Eyes: ",
            "Eyebrows: ",
            "Nose: ",
            "Eyebags: ",
            "Blush: ",
            "Tears: ",
            "Sweat: ",
            # "Emote: ",
            "Mouth: ",
            "Clothes: ",
            "Hair: ",
            "Filter: "
        ]

        ROWS = len(LABELS)

        ### button retvals
        SQ_BUTTON_RETVALS = [
            "arms",
            "eyes",
            "eyebrows",
            "nose",
            "eyebags",
            "blush",
            "tears",
            "sweat",
            # "emote",
            "mouth",
            "torso",
            "hair",
            "time"
        ]

        ### Available codes
        NOSE_DEF = "nd"
        # sprite code map
        SPRITE_CODE_MAP = {
            "arms": [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
            ],
            "eyes": [
                "e",
                "w",
                "s",
                "t",
                "c",
                "r",
                "l",
                "h",
                "d",
                "k",
                "n",
                "f",
                "m",
                "g",
            ],
            "eyebrows": [
                "f",
                "u",
                "k",
                "s",
                "t"
            ],
            "nose": [
                "nd"
            ],
            "eyebags": [
                None,
                "ebd"
            ],
            "blush": [
                None,
                "bl",
                "bs",
                "bf"
            ],
            "tears": [
                None,
                "ts",
                "td",
                "tp",
                "tu",
            #    "tl",
            #    "tr",
            #    "th",
            #    "tc",
            ],
            "sweat": [
                None,
                "sdl",
                "sdr"
            ],
            # "emote": [
            #     None,
            #     "ec"
            # ],
            "mouth": [
                "a",
                "b",
                "c",
                "d",
                "o",
                "u",
                "w",
                "x",
                "p",
                "t",
            #    "g",
            ],
            "torso": [
                "def",
                "blazerless",
                "marisa",
                # "rin",
                "santa",
                "sundress_white",
                "blackdress",
            ],
            "hair": [
                "def",
                "down",
            #    "bun"
            ],
            "time": [ # actually means Filter now
                "day",
                "night",
            ]
        }

        # modifier map, for special cases. Currently this should be used
        # as appenders to image names
        # NOTE: each expression may use this differently.
        MOD_MAP = mas_sprite_decoder.MOD_MAP

        # list of keys that matter for a sprite code
        SPRITE_CODE_PARTS = [
            "arms",
            "eyes",
            "eyebrows",
            "nose",
            "eyebags",
            "blush",
            "tears",
            "sweat",
            # "emote",
            "mouth"
        ]

        # selection text index map
        INDEX_MAP = {
            k: id_
            for id_, k in enumerate(SQ_BUTTON_RETVALS)
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

            # update torsos with spritepacked sprites
            torso_map = self.SEL_TX_MAP["torso"]
            torso_list = self.SPRITE_CODE_MAP["torso"]
            for sel in store.mas_selspr.CLOTH_SEL_MAP.itervalues():
                spr = sel.get_sprobj()
                if spr.is_custom and spr.name not in torso_map:
                    torso_map[spr.name] = sel.display_name
                    torso_list.append(spr.name)

            # background tile
            self.background = Solid(
                "#000000B2",
                xsize=self.PANEL_WIDTH,
                ysize=self.PANEL_HEIGHT
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
            button_y_list = [
                self.ROW_Y_START + (
                    x * (self.ROW_SPACING + self.SQ_BUTTON_HEIGHT)
                )
                for x in range(self.ROWS)
            ]

            # actual left buttons
            self.button_ls = [
                MASButtonDisplayable.create_stb(
                    "<",
                    True,
                    button_lx,
                    button_y_list[x],
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
                MASButtonDisplayable.create_stb(
                    ">",
                    True,
                    button_rx,
                    button_y_list[x],
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

            # Copy button
            self.button_copy = MASButtonDisplayable.create_stb(
                "Copy",
                False,
                self.BUTTON_X_COPY,
                self.BUTTON_Y_COPY,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            # Paste button
            self.button_paste = MASButtonDisplayable.create_stb(
                "Paste",
                False,
                self.BUTTON_X_PASTE,
                self.BUTTON_Y_PASTE,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            # Reset button
            self.button_reset = MASButtonDisplayable.create_stb(
                "Reset",
                False,
                self.BUTTON_X_RESET,
                self.BUTTON_Y_RESET,
                self.BUTTON_WIDTH,
                self.BUTTON_HEIGHT,
                hover_sound=gui.hover_sound,
                activate_sound=gui.activate_sound
            )

            # Done button
            self.button_done = MASButtonDisplayable.create_stb(
                "Done",
                False,
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
            self.all_buttons.append(self.button_copy)
            self.all_buttons.append(self.button_paste)
            self.all_buttons.append(self.button_reset)
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

            ### selection map

            # map of directional functions to sprite piece
            self._selectors = {
                "arms": self._sel_arms,
                "blush": self._sel_blush,
                # "emote": self._sel_emote,
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
                # "emote": 0,
                "eyes": 0,
                "eyebags": 0,
                "eyebrows": 1,
                "hair": 0,
                "mouth": 0,
                "nose": 0,
                "sweat": 0,
                "tears": 0,
                "time": 0 if store.mas_current_background.isFltDay() else 1,
                "torso": 0
            }

            # build the Text objects
            self.curr_sel_txts = self._build_sel_texts()

            # current sprite code as a string
            self.curr_spr_code = self._build_spr_code()

            # did the sprite chnage?
            self.sprite_changed = True

            # sprite as  atransform
            self.spr_tran = self._create_sprite()

            # need to check which render state we should be in
            if self.spr_tran is None:
                # dont need to change anything here
                self.state = self.STATE_INVALID


            else:
                # blit mode needs some adjustments
                self.state = self.STATE_VALID

        def _adj_sel(self, direct, key):
            """
            Generically does a selection change.

            IN:
                direct - direction to move
                key - key to use in selection map
            """
            self.curr_sel[key] = self._select(
                self.SPRITE_CODE_MAP[key],
                direct,
                self.curr_sel[key]
            )

        def _create_sprite(self):
            """
            Generates the sprite Transform using the sprite chart functions

            RETURNS the created Transform, or None if that failed
            """
            _arms = self._get_spr_code("arms")
            if _arms in self.LEAN_SMAP:
                _lean, _arms = self.LEAN_SMAP[_arms]
            else:
                _lean = None
                _arms = self._get_img_name("arms")

            img_eyes = self._get_img_name("eyes")

            try:
                trn, rfr = mas_drawmonika_rk(
                    0.0,# st
                    0.0,# at
                    monika_chr,# character
                    self._get_img_name("eyebrows"),
                    img_eyes,
                    self._get_img_name("nose"),
                    self._get_img_name("mouth"),
                    head="",
                    left="",
                    right="",
                    lean=_lean,
                    arms=_arms,
                    eyebags=self._get_img_name("eyebags"),
                    sweat=self._get_img_name("sweat"),
                    blush=self._get_img_name("blush"),
                    tears=self._get_img_tears("tears", img_eyes),
                    # emote=self._get_img_name("emote")
                )
                # now we need to modify the transform a little bit
                return store.i21(
                    Transform(
                        trn,
                        zoom=0.90,
                        alpha=1.00
                    )
                )

            except:
                # the eval failed because we didnt have an image
                return None

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
                direct - direction to move in (+ -> / - <-),
                    aswell as the number of indexes to move by
                currdex - cureent index

            RETURNS:
                index of the next selection
            """
            if len(choices) <= 1 or direct == 0:
                # only 1 choice? just return 0
                return 0

            while direct != 0:
                # Lets move right
                if direct > 0:
                    direct -= 1
                    currdex += 1

                    if currdex >= len(choices):
                        # went past right, wrap to left
                        currdex = 0

                # Lets move left
                elif direct < 0:
                    direct += 1
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
            monika_chr.change_hair(mas_sprites.HAIR_MAP.get(
                self._get_spr_code("hair"),
                mas_hair_def
            ))

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
            self.mas_sprites.set_filter(self._get_spr_code("time"))

        def _sel_torso(self, direct):
            self._adj_sel(direct, "torso")
            self._update_sel_tx("torso")
            monika_chr.change_clothes(mas_sprites.CLOTH_MAP.get(
                self._get_spr_code("torso"),
                mas_clothes_def
            ))


        ######################### button functions ###########################

        def _disable_singles(self):
            """
            Goes through the left / right button lists and disables buttons
            that only have single selection avaialble
            """
            for button in self.button_ls:
                if len(self.SPRITE_CODE_MAP[button.return_value]) < 2:
                    button.disable()

            for button in self.button_rs:
                if len(self.SPRITE_CODE_MAP[button.return_value]) < 2:
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
            for key in self.SPRITE_CODE_PARTS:
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
            # 2. SPRITE_CODE_MAP has the lists of sprite codes arranged by index
            spr_code = self.SPRITE_CODE_MAP[key][self.curr_sel[key]]
            if nose and spr_code == self.NOSE_DEF:
                return None

            return spr_code

        def _reset(self):
            """
            Resets exp params
            """
            changed = False
            for key in self.SPRITE_CODE_PARTS:
                current_index = self.curr_sel[key]
                new_index = 0 if key != "eyebrows" else 1
                direction = new_index - current_index
                if direction != 0:
                    changed = True
                    self._selectors[key](direction)

            if changed:
                self.sprite_changed = True

        def _from_spr_code(self, spr_code):
            """
            Attempts to parse a sprite code and then updates the selectors accordingly

            IN:
                spr_code - sprite code
            """
            # Sanity check so we don't process something crazy from the buffer
            if not spr_code or not 0 < len(spr_code) < 25:
                return

            spr_code = spr_code.strip(" \t\n\r").lower()
            try:
                exp_kwargs = mas_sprite_decoder.parse_exp_to_kwargs(
                    spr_code
                )

            except:
                # Assuming invalid sprite code
                return

            changed = False

            for key in self.SPRITE_CODE_PARTS:
                # Add bits that might not be present in the given code
                exp_kwargs.setdefault(key, None)

            for key, value in exp_kwargs.iteritems():
                # Skip the keys we don't need
                if (
                    key in self.SPRITE_CODE_MAP
                    and key in self.REVERSE_IMG_NAMES_MAP
                ):
                    # None means it's something that isn't in the code
                    # So we just reset to default - 0
                    if value is None:
                        new_index = 0 if key != "eyebrows" else 1

                    # Otherwise have to do a lookup to find the new index
                    else:
                        spr_code_letter = self.REVERSE_IMG_NAMES_MAP[key][value]
                        new_index = self.SPRITE_CODE_MAP[key].index(spr_code_letter)

                    # Now move the selectors
                    current_index = self.curr_sel[key]
                    direction = new_index - current_index
                    if direction != 0:
                        changed = True
                        self._selectors[key](direction)

            if changed:
                self.sprite_changed = True

        def _update_spr_code(self):
            """
            Updates sprite code using the current selection map
            """
            self.curr_spr_code = self._build_spr_code()


        ####################### image based functions ########################

        def _get_img_name(self, key):
            """
            Gets the image name for a given sprite key

            IN:
                key - what image name do we need

            RETURNS the image name we need
            """
            spr_code = self._get_spr_code(key, False)
            if spr_code is None:
                return None

            return self.IMG_NAMES_MAP[key][spr_code]

        def _get_img_tears(self, key, eyes):
            """
            Custom name generator for tear expressions, as they vary on
            eyes.

            IN:
                key - what image name do we need
                eyes - current eyes as img name

            REUTRNS the image name we need
            """
            tears_name = self._get_img_name(key)

            # check for the mapping
            tears_map = self.MOD_MAP.get(key, None)
            if tears_map is None:
                return tears_name

            # check for specific tears in the mapping
            tears_mappings = tears_map.get(tears_name, None)
            if tears_mappings is None:
                return tears_name

            # check for eyes in the mapping
            if eyes in tears_mappings:
                return tears_name + eyes

            # otherwise just tears
            return tears_name


        ####################### render / event ###############################


        def render(self, width, height, st, at):
            """
            RENDER
            """
            render = renpy.Render(width, height)

            # Moni render
            if self.state == self.STATE_VALID:
                try:
                    spr_tran = self.spr_tran
                    spr_tran_surf = renpy.render(
                        spr_tran, width, height, st, at
                    )

                except:
                    # this failed to render
                    self.state = self.STATE_INVALID
                    spr_tran = store.i21(Placeholder("girl"))
                    spr_tran_surf = renpy.render(
                        spr_tran, width, height, st, at
                    )

                finally:
                    render.place(spr_tran, x=self.MONI_X, y=self.MONI_Y, render=spr_tran_surf)
                    self.sprite_changed = False

            # BG render
            bg_surf = renpy.render(self.background, width, height, st, at)
            render.blit(bg_surf, (self.PANEL_X, self.PANEL_Y))

            # Spr code render
            spr_code_text_color = self.SPR_FOUND
            spr_code_text = Text(
                "Sprite Code: " + self.curr_spr_code,
                font=gui.default_font,
                size=self.TEXT_SIZE,
                color=spr_code_text_color,
                outlines=[]
            )
            spr_code_text_surf = renpy.render(spr_code_text, width, height, st, at)
            render.blit(spr_code_text_surf, (self.LBL_X, self.SC_Y))

            # Text renders, do both text and sel texts together for efficiency
            for x in range(self.ROWS):
                # text
                text_surf = renpy.render(self.labels[x], width, height, st, at)
                text_blit_coords = (self.LBL_X, self.lbl_y_list[x])
                render.blit(text_surf, text_blit_coords)

                # Selected text
                sel_text_surf = renpy.render(
                    self.curr_sel_txts[x],
                    width,
                    height,
                    st,
                    at
                )
                _surf_w, _surf_h = sel_text_surf.get_size()
                sel_text_blit_coords = (
                    self._seltx_xcenter(_surf_w),
                    self.lbl_y_list[x]
                )
                render.blit(sel_text_surf, sel_text_blit_coords)

            # Buttons renders
            for b in self.all_buttons:
                render.blit(
                    renpy.render(b, width, height, st, at),
                    (b.xpos, b.ypos)
                )

            return render

        def event(self, ev, x, y, st):
            """
            EVENT
            """
            if ev.type in self.MOUSE_EVENTS:
                # Are we done?
                if self.button_done.event(ev, x, y, st):
                    return True

                # Check left/right buttons
                elif self._left_button_select(ev, x, y, st) or self._right_button_select(ev, x, y, st):
                    # Processing is done later
                    pass

                # Check copy button
                elif self.button_copy.event(ev, x, y, st):
                    pygame.scrap.put(pygame.SCRAP_TEXT, self.curr_spr_code)

                # Check paste button
                elif self.button_paste.event(ev, x, y, st):
                    new_spr_code = pygame.scrap.get(pygame.SCRAP_TEXT)
                    self._from_spr_code(new_spr_code)

                elif self.button_reset.event(ev, x, y, st):
                    self._reset()

                # Redraw if needed
                if self.sprite_changed:
                    # if this is None, we just dont render it
                    self.spr_tran = self._create_sprite()

                    if self.spr_tran is None:
                        self.state = self.STATE_INVALID

                    else:
                        self.state = self.STATE_VALID

                    # Rereender
                    renpy.redraw(self, 0)
                    # Run gc
                    renpy.restart_interaction()

                return None
            raise renpy.IgnoreEvent()
