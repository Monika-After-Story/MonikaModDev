# definitions of sprite objects


class StaticSprite(object):
    """
    A static sprite is a sprite that knows its sprite codes and more
    
    PROPERTIES:
        invalid - True if this sprite object should be treated as invalid, 
            False otherwise
    """
    _sprite_map = {
        "position": {
            "1": "steepling",
            "2": "crossed",
            "3": "restleftpointright",
            "4": "pointright",
            "5": ("def", "def"),
            "6": "down",
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
        }
    }

    def __init__(self, spcode):
        """
        Constructor for a static sprite
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
        position = self._sprite_map.get(spcode[0], None)
        if position is None:
            self.invalid = True
            return
        self.position = position

        # 1 - eyes
        eyes = self._sprite_map.get(spcode[1], None)
        if eyes is None:
            self.invalid = True
            return
        self.eyes = eyes

        # 2 - eyebrows
        eyebrows = self._sprite_map.get(spcode[2], None)
        if eyebrows is None:
            self.invalid = True
            return
        self.eyebrows = eyebrows

        # -1 - mouth
        mouth = self._sprite_map.get(spcode[-1], None)
        if mouth is None:
            self.invalid = True
            return
        self.mouth = mouth

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
        # so far, nose is the only default
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
        blush = self._sprite_map.get("".join(prefixes), None)
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
        emote = self._sprite_map.get("".join(prefixes), None)
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
        nose = self._sprite_map.get("".join(prefixes), None)
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
        sweatdrop = self._sprite_map.get("".join(prefixes), None)
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
        tears = self._sprite_map.get("".join(prefixes), None)
        if tears is None:
            return False, 0
    
        # otherwise ok
        self.tears = tears
        return True, 1


