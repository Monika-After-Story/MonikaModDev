# definitions of sprite objects


class StaticSprite(object):
    """
    A static sprite is a sprite that knows its sprite codes and more
    
    PROPERTIES:
        invalid - True if this sprite object should be treated as invalid, 
            False otherwise
    """
    _sprite_map = {
        "is_lean": {
            "1": False,
            "2": False,
            "3": False,
            "4": False,
            "5": True,
            "6": False,
        },
        "position": {
            "1": "steepling",
            "2": "crossed",
            "3": "restleftpointright",
            "4": "pointright",
            "5": ("def", "def"),
            "6": "down",
        },
        "sides": {
            "1": ("1l", "1r"),
            "2": ("1l", "2r"),
            "3": ("2l", "2r"),
            "4": ("2l", "2r"),
            "5": ("", ""),
            "6": ("1l", "1r"),
        },
        "eyes": {
            "e": "normal",
            "w": "wide",
            "s": "sparkle",
            "t": "smug",
            "c": "crazy",
            "r": "right",
            "l": "left",
            "h": "closedhappy",
            "d": "closedsad",
            "k": "winkleft",
            "n": "winkright"
        },
        "eyebrows": {
            "f": "furrowed",
            "u": "up",
            "k": "knit",
            "s": "mid",
            "t": "think"
        },
        "nose": {
            "nd": "def"
        },
        "eyebags": { # NOTE: this is retired
            "ebd": "def"
        },
        "blush": {
            "bl": "lines",
            "bs": "shade",
            "bf": "full"
        },
        "tears": {
            "ts": "streaming",
            "td": "dried",
            "tp": "pooled",
            "tu": "up",
            "tl": "left",
            "tr": "right",
        },
        "sweat": {
            "sdl": "def",
            "sdr": "right"
        },
        "emote": {
            "ec": "confuse"
        },
        "mouth": {
            "a": "smile",
            "b": "big",
            "c": "smirk",
            "d": "small",
            "o": "gasp",
            "u": "smug",
            "w": "wide",
            "x": "disgust",
            "p": "pout",
            "t": "triangle"
        },
        "single": { # everything else will be 3b
            "a": "3a",
            "u": "3a",
        },
        "head": {
            # exact eye - eyebrow - mouth match
            "eua": "a",
            "eub": "b",
            "euc": "c",
            "eud": "d",
            "eka": "e",
            "ekc": "f",
            "ekd": "g",
            "esc": "h",
            "esd": "i",
            "hua": "j",
            "hub": "k",
            "hkb": "l", # sdl
            "lka": "m", # sdl
            "lkb": "n", # sdl
            "lkc": "o", # sdl
            "lkd": "p", # sdl
            "dsc": "q",
            "dsd": "r",
        },
    }

    _tab = " " * 4

    def __init__(self, spcode):
        """
        Constructor for a static sprite
        """
        self._init_props()
        self.spcode = spcode

        self.__process_map = {
            "b": self.__process_blush,
            "e": self.__process_emote,
            "n": self.__process_nose,
            "s": self.__process_s,
            "t": self.__process_tears,
        }

        self.__sub_process_map = {
            "s": {
                "d": self.__process_sweatdrop,
            },
        }

        self._rip_sprite(spcode)
        self._set_defaults()

    def __str__(self):
        """
        To string. This will create a DynamicDisplayable
        """
        if self.invalid:
            return ""

        cnl = ",\n"

        # add the 100% for sure lines
        lines = [
            "image monika ",
            self.spcode,
            "_static = DynamicDisplayable(\n",
            self._tab,
            "mas_drawmonika",
            cnl,
            self._tab,
            "character=monika_chr",
            cnl,
            self._tab,
            "eyebrows=",
            self.eyebrows,
            cnl,
            self._tab,
            "eyes=",
            self.eyes,
            cnl,
            self._tab,
            "nose=",
            self.nose,
            cnl,
            self._tab,
            "mouth=",
            self.mouth,
        ]

        # now for the position lines 
        if self.is_lean:
            # leaning uses both arms and lean, as well as single
            lean, arms = self.position
            lines.extend([
                cnl,
                self._tab,
                "arms=",
                arms,
                cnl,
                self._tab,
                "lean=",
                lean,
                cnl,
                self._tab,
                "single=",
                self.single
            ])

        else:
            # otherwise, only have arms and maybe head/sides
            lines.extend([
                cnl,
                self._tab,
                "arms=",
                self.position
            ])

            if self.head:
                # yes have head
                left, right = self.sides
                lines.extend([
                    cnl,
                    self._tab,
                    "head=",
                    self.head,
                    cnl,
                    self._tab,
                    "left=",
                    left,
                    cnl,
                    self._tab,
                    "right=",
                    right
                ])

        # now for optional parts
        if self.blush is not None:
            lines.extend([
                cnl,
                self._tab,
                "blush=",
                self.blush
            ])

        if self.tears is not None:
            lines.extend([
                cnl,
                self._tab,
                "tears=",
                self.tears
            ])

        if self.sweatdrop is not None:
            lines.extend([
                cnl,
                self._tab,
                "sweat=",
                self.sweatdrop
            ])

        if self.emote is not None:
            lines.extend([
                cnl,
                self._tab,
                "emote=",
                self.emote
            ])

        # done, add final paren
        lines.append("\n)")

        return "".join(lines)

    def spstr(self):
        """
        Creates the sprite code string for use in ATL statements.
        :returns: sp code string. This is form (monika <code>_static)
        """
        return "monika " + self.spcode + "_static"

    def _get_smap(self, mainkey, code, defval):
        """
        Gets a value from the sprite map
        :param mainkey: which part of sprite map to get from
        :param code: the code to lookup
        :param defval: the default value to use
        :returns: the value from sprite map or defval
        """
        return self._sprite_map.get(mainkey, {}).get(code, defval)

    def _init_props(self):
        """
        Sets all starting properties to None
        """
        self.invalid = False
        self.position = None
        self.eyes = None
        self.eyebrows = None
        self.nose = None
        self.blush = None
        self.tears = None
        self.sweatdrop = None
        self.emote = None
        self.mouth = None
        self.is_lean = None
        self.sides = None
        self.single = None
        self.head = None
        self.spcode = None

    def _rip_sprite(self, spcode):
        """
        Takes a sprite code (without _static) and rips it into pieces,
        setting appropriate vars.
        :param spcode: the sprite code to rip (string)
        """
        # NOTE: the sprite code MUST have 4 parts:
        #   [0] - the position
        #   [1] - the eyes
        #   [2] - the eyebrows
        #   [-1] - the mouth
        #
        # all the remaining parts are in a specific order, but each has
        #   a specific prefix. 
        # NOTE: we are retiring eyebag codes (eb_) there is no reason for 
        #   these.
        # (e) will be saved for emotes

        # spcode must be at least 4 charactes
        if len(spcode) < 4:
            self.invalid = True
            return

        # 0 - position
        poscode = spcode[0]
        position = self._get_smap("position", poscode, defval)
        if position is None:
            self.invalid = True
            return
        self.position = position
        self.is_lean = self._get_smap("is_lean", poscode, False)
        self.sides = self._get_smap("sides", poscode, ("", ""))

        # 1 - eyes
        eyecode = spcode[1]
        eyes = self._get_smap("eyes", eyecode, None)
        if eyes is None:
            self.invalid = True
            return
        self.eyes = eyes

        # 2 - eyebrows
        eyebrowcode = spcode[2]
        eyebrows = self._get_smap("eyebrows", eyebrowcode, None)
        if eyebrows is None:
            self.invalid = True
            return
        self.eyebrows = eyebrows

        # -1 - mouth
        mouthcode = spcode[-1]
        mouth = self._get_smap("mouth", mouthcode, None)
        if mouth is None:
            self.invalid = True
            return
        self.mouth = mouth
        self.single = self._get_smap("single", mouthcode, "3b")

        # determine the head (for standing)
        self.head = self._get_smap(
            "head",
            eyecode + eyebrowcode + mouthcode,
            ""
        )

        # now get remaining codes
        spcode = spcode[3:-1]

        # code parse
        index = 0
        while index < len(spcode):
            prefix = spcode[index]
            index += 1
            sprite_added = False

            # determine what function to process this code with
            processor = self.__process_map.get(prefix, None)
            if processor is not None:
                try:
                    sprite_added, increaseby = processor(spcode, index, prefix)
                except:
                    # any sort of exception is a bad state
                    self.invalid = False
                    return

            # if any sprite failed, or we didnt find a prefix
            if not sprite_added:
                self.invalid = True
                return

            # otherwise, we good to continue
            index += increaseby

    def _set_defaults(self):
        """
        Sets defaults of sprites that have defaults
        """
        if self.nose is None:
            self.nose = "def"

    def __process_blush(self, spcode, index, *prefixes):
        """
        Process a blush off the given sprite code at the given index
        :param spcode: the sp code to check
        :param index: the next index to check
        :param prefixes: letters to prefix the code with
        :returns: Tuple of the following format:
            [0] - True if the resulting code was valid, False if not
            [1] - the number of spots to increase the index by
        """
        # cannot have duplicates
        if self.blush is not None:
            return False, 0

        # next letter must be blush type
        prefixes.append(spcode[index])
        blush = self._get_smap("blush", "".join(prefixes), None)
        if blush is None:
            return False, 0

        # otherwise ok
        self.blush = blush
        return True, 1

    def __process_emote(self, spcode, index, *prefixes):
        """
        Processe an emote off the given sprite code at the given index
        :param spcode: the spcode to check
        :param index: the next index to check
        :param prefixes: letters to prefix the code with
        :returns: Tuple of the following format:
            [0] - True if the resulting code was valid, False if not
            [1] - the number of spots to increase the index by
        """
        # cannot have duplicates
        if self.emote is not None:
            return False, 0

        # next letter must be emote type
        prefixes.append(spcode[index])
        emote = self._get_smap("emote", "".join(prefixes), None)
        if emote is None:
            return False, 0

        # otherwise ok
        self.emote = emote
        return True, 1

    def __process_nose(self, spcode, index, *prefixes):
        """
        Processes a nose off the given sprite code at the given index
        :param spcode: the spcode to chek
        :param index: the next index to check
        :param prefixes: letters to prefix the code with
        :returns: Tuple of the following format:
            [0] - True if the resulting code was valid, False if not
            [1] - the number of spots to increas the index by
        """
        # cannot have duplicates
        if self.nose is not None;
            return False, 0

        # next letter must be nose type
        prefixes.append(spcode[index])
        nose = self._get_smap("nose", "".join(prefixes), None)
        if nose is None:
            return False, 0

        # otherwise ok
        self.nose = nose
        return True, 1

    def __process_s(self, spcode, index, *prefixes):
        """
        Processes the s-prefixed spcodes at the given index
        :param spcode: the sp code to check
        :param index: the next index to check
        :param prefixes: letters to prefix the code with
        :returns: Tuple of the following format:
            [0] - True if the resulting code was valid, False if not
            [1] - the number of spots to increase the index by
        """
        midfix = spcode[index]
        index += 1
        sprite_added = False

        processor = self.__sub_process_map["s"].get(midfix, None)

        if processor is not None:
            prefixes.append(midfix)
            sprite_added, increaseby = processor(
                spcode,
                index,
                *prefixes
            )

        # if any sprite failed, or we didnt find a midfix
        if not sprite_added:
            return False, 0

        # otherwise, we good to go
        return True, 1 + increaseby

    def __process_sweatdrop(self, spcode, index, *prefixes):
        """
        Processes a sweatdrop off the given spcode at the given index
        :param spcode: the spcode to check
        :param index: the next index to check
        :param prefixes: letters to prefix the code with
        :returns: Tuple of the following format:
            [0] - True if the sweat drop was valid, False if not
            [1] - the number of spots to increase the index by
        """
        # cannot have dupplicates
        if self.sweatdrop is not None:
            return False, 0

        # next letter must be the sweatdrop type
        prefixes.append(spcode[index])
        sweatdrop = self._get_smap("sweat", "".join(prefixes), None)
        if sweatdrop is None:
            return False, 0

        # otherwise ok
        self.sweatdrop = sweatdrop
        return True, 1

    def __process_tears(self, spcode, index, *prefixes):
        """
        Processes a tear off the given spcode at the given index
        :param spcode: the spcode to check
        :param index: the next index to check
        :param prefixes: letters to prefix the code with
        :returns: Tuple of the following format:
            [0] - True if the tears were valid, False if not
            [1] - the number of spots to increase the index by
        """
        # cannot have duplicates
        if self.tears is not None:
            return False, 0

        # next letter must be the tear type
        prefixes.append(spcode[index])
        tears = self._get_smap("tears", "".join(prefixes), None)
        if tears is None:
            return False, 0
    
        # otherwise ok
        self.tears = tears
        return True, 1


