# Monika's sprites!
# To add new images, use the sprite adder tool in MonikaModDev/tools/toolsmenu
#
###### SPRITE CODE (IMG010)
#
# The sprite code system is a way of picking an appropriate sprite without
# having to look up what the sprite looks like.
# All expressions use this code system. the original 19 expressions (with
# counterparts have been aliased to the correct code system. Please avoid
# using the og 19+ coutnerparts)
#
# For aliases, see [IMG032]
#
# The sprite code system consists of:
# <pose number><eyes type><eyebrow type><nose type><eyebag type><blush type>
# <tears type><sweat type><emote type><mouth type>
#
# Only <pose number><eyes type><eyebrow type><mouth type> are required
#
# Here are the available values for each type:
# <pose number> - arms/body pose to use
#   1 - resting on hands (steepling)
#   2 - arms crossed (crossed)
#   3 - resting on left arm, pointing to the right (restleftpointright)
#   4 - pointing right (pointright)
#   5 - leaning (def)
#   6 - arms down (down)
#
# <eyes type> - type of eyes
#   e - normal eyes (normal)
#   w - wide eyes (wide)
#   s - sparkly eyes (sparkle)
#   t - straight/smug eyes (smug)
#   c - crazy eyes (crazy)
#   r - look right eyes (right)
#   l - look left eyes (left)
#   h - closed happy eyes (closedhappy)
#   d - closed sad eyes (closedsad)
#   k - left eye wink (winkleft)
#   n - right eye wink (winkright)
#
# <eyebrow type> - type of eyebrow
#   f - furrowed / angery (furrowed)
#   u - up / happy (up)
#   k - knit / upset / concerned (knit)
#   s - straight / normal / regular (mid)
#   t - thinking (think)
#
# <nose type> - type of nose
#   nd - default nose (def) NOTE: UNUSED
#
# <eyebag type> - type of eyebags
#   ebd - default eyebags (def) NOTE: UNUSED
#
# <blush type> - type of blush
#   bl - blush lines (lines)
#   bs - blush shade (shade)
#   bf - full blush / lines and shade blush (full)
#
# <tears type> - type of tears
#   ts - tears streaming / running (streaming)
#   td - dried tears (dried)
#   tl - tears, single stream, left eye (left)
#   tr - tears, single stream, right eye (right)
#   tp - like dried tears but with no redness (pooled)
#   tu - tears, single stream, both eyes (up)
#
# <sweat type> - type of sweat drop
#   sdl - sweat drop left (def)
#   sdr - sweat drop right (right)
#
# <emote type> - type of emote
#   ec - confusion emote (confuse) NOTE: UNUSED
#
# <mouth type> - type of mouth
#   a - smile (smile)
#   b - open smile (big)
#   c - apathetic / straight mouth / neither smile nor frown (smirk)
#   d - open mouth (small)
#   o - gasp / open mouth (gasp)
#   u - smug (smug)
#   w - wide / open mouth (wide)
#   x - disgust / grit teeth (disgust)
#   p - tsundere/ puffy cheek (pout)
#   t - triangle (triangle)
#
# For example, the expression code 1sub is:
#   1 - resting on hands pose
#   s - sparkly eyes
#   u - happy eyebrows
#   b - big open smile
#
# NOTE:
# not every possible combination has been created as an image. If you want
# a particular expression, make a github issue about it and why we need it.
#
# hmmmmmm (1etecc)

# This defines a dynamic displayable for Monika whose position and style changes
# depending on the variables is_sitting and the function morning_flag
define is_sitting = True

# accessories list
default persistent._mas_acs_pre_list = []
default persistent._mas_acs_bbh_list = []
default persistent._mas_acs_bfh_list = []
default persistent._mas_acs_afh_list = []
default persistent._mas_acs_mid_list = []
default persistent._mas_acs_pst_list = []

# zoom levels
default persistent._mas_zoom_zoom_level = None

default persistent._mas_force_clothes = False
# Set to True if the user manually set clothes

default persistent._mas_force_hair = False
# Set to True if the user manually set hair

image monika g1:
    "monika/g1.png"
    xoffset 35 yoffset 55
    parallel:
        zoom 1.00
        linear 0.10 zoom 1.03
        repeat
    parallel:
        xoffset 35
        0.20
        xoffset 0
        0.05
        xoffset -10
        0.05
        xoffset 0
        0.05
        xoffset -80
        0.05
        repeat
    time 1.25
    xoffset 0 yoffset 0 zoom 1.00
    "monika 3"

image monika g2:
    block:
        choice:
            "monika/g2.png"
        choice:
            "monika/g3.png"
        choice:
            "monika/g4.png"
    block:
        choice:
            pause 0.05
        choice:
            pause 0.1
        choice:
            pause 0.15
        choice:
            pause 0.2
    repeat

define m = DynamicCharacter('m_name', image='monika', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

#empty desk image, used when Monika is no longer in the room.
#image emptydesk = im.FactorScale("mod_assets/emptydesk.png", 0.75)
image emptydesk = ConditionSwitch(
    "morning_flag", "mod_assets/emptydesk.png",
    "not morning_flag", "mod_assets/emptydesk-n.png"
)

image mas_finalnote_idle = "mod_assets/poem_finalfarewell_desk.png"

image mas_roses = ConditionSwitch(
    "morning_flag",
    "mod_assets/monika/a/acs-roses-0.png",
    "not morning_flag",
    "mod_assets/monika/a/acs-roses-0-n.png"
)

### bday stuff
define mas_bday_cake_lit = False
image mas_bday_cake = ConditionSwitch(
    "morning_flag and mas_bday_cake_lit",
    "mod_assets/location/spaceroom/bday/birthday_cake_lit.png",
    "morning_flag and not mas_bday_cake_lit",
    "mod_assets/location/spaceroom/bday/birthday_cake.png",
    "not morning_flag and mas_bday_cake_lit",
    "mod_assets/location/spaceroom/bday/birthday_cake_lit-n.png",
    "not morning_flag and not mas_bday_cake_lit",
    "mod_assets/location/spaceroom/bday/birthday_cake-n.png"
)
image mas_bday_banners = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/bday/birthday_decorations.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/bday/birthday_decorations-n.png"
)
image mas_bday_balloons = ConditionSwitch(
    "morning_flag",
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons_sens.png",
    "not morning_flag",
    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons-n_sens.png"
#    "morning_flag",
#    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons.png",
#    "not morning_flag",
#    "mod_assets/location/spaceroom/bday/birthday_decorations_balloons-n.png"
)

init -5 python in mas_sprites:
    # specific image generation functions
    import store

    # main art path
    MOD_ART_PATH = "mod_assets/monika/"
    STOCK_ART_PATH = "monika/"

    # delimiters
    ART_DLM = "-"

    # important keywords
    KW_STOCK_ART = "def"

    ### other paths:
    # H - hair
    # C - clothing
    # F - face parts
    # A - accessories
    # S - standing
    # T - table
    H_MAIN = MOD_ART_PATH + "h/"
    C_MAIN = MOD_ART_PATH + "c/"
    F_MAIN = MOD_ART_PATH + "f/"
    A_MAIN = MOD_ART_PATH + "a/"
    S_MAIN = MOD_ART_PATH + "s/"
    T_MAIN = MOD_ART_PATH + "t/"

    # sitting standing parts
#    S_MAIN = "standing/"

    # facial parts
    F_T_MAIN = F_MAIN
#    F_S_MAIN = F_MAIN + S_MAIN

    # accessories parts
    A_T_MAIN = A_MAIN

    ### End paths

    # location stuff for some of the compsoite
    LOC_REG = "(1280, 850)"
    LOC_LEAN = "(1280, 850)"
    LOC_Z = "(0, 0)"
    LOC_STAND = "(960, 960)"

    # composite stuff
    I_COMP = "LiveComposite"
    L_COMP = "LiveComposite"
    TRAN = "Transform"

    # zoom
    ZOOM = "zoom="

    default_zoom_level = 3

    if store.persistent._mas_zoom_zoom_level is None:
        store.persistent._mas_zoom_zoom_level = default_zoom_level
        zoom_level = default_zoom_level

    else:
        zoom_level = store.persistent._mas_zoom_zoom_level

    zoom_step = 0.05
    default_value_zoom = 1.25
    value_zoom = default_value_zoom
    max_zoom = 20

    # adjustable location stuff
    default_x = 0
    default_y = 0
    adjust_x = default_x
    adjust_y = default_y
#    y_step = 40
    y_step = 20

    # adding optimized initial parts of the sprite string
    PRE_SPRITE_STR = TRAN + "(" + L_COMP + "("

    # Prefixes for files
    PREFIX_TORSO = "torso" + ART_DLM
    PREFIX_TORSO_LEAN = "torso-leaning" + ART_DLM
    PREFIX_BODY = "body" + ART_DLM
    PREFIX_BODY_LEAN = "body-leaning" + ART_DLM
    PREFIX_HAIR = "hair" + ART_DLM
    PREFIX_HAIR_LEAN = "hair-leaning" + ART_DLM
    PREFIX_ARMS = "arms" + ART_DLM
    PREFIX_ARMS_LEAN = "arms-leaning" + ART_DLM
    PREFIX_FACE = "face" + ART_DLM
    PREFIX_FACE_LEAN = "face-leaning" + ART_DLM
    PREFIX_ACS = "acs" + ART_DLM
    PREFIX_ACS_LEAN = "acs-leaning" + ART_DLM
    PREFIX_EYEB = "eyebrows" + ART_DLM
    PREFIX_EYES = "eyes" + ART_DLM
    PREFIX_NOSE = "nose" + ART_DLM
    PREFIX_MOUTH = "mouth" + ART_DLM
    PREFIX_SWEAT = "sweatdrop" + ART_DLM
    PREFIX_EMOTE = "emote" + ART_DLM
    PREFIX_TEARS = "tears" + ART_DLM
    PREFIX_EYEG = "eyebags" + ART_DLM
    PREFIX_BLUSH = "blush" + ART_DLM
    PREFIX_TABLE = "table" + ART_DLM

    # suffixes
    NIGHT_SUFFIX = ART_DLM + "n"
    FHAIR_SUFFIX  = ART_DLM + "front"
    BHAIR_SUFFIX = ART_DLM + "back"
    FILE_EXT = ".png"

    # other const
    DEF_BODY = "def"
    NEW_BODY_STR = PREFIX_BODY + DEF_BODY

    ## string builder constants
    BS_ACS = "".join((
        A_T_MAIN,
        PREFIX_ACS,
        "{0}", # acs img sit
        ART_DLM,
        "{1}", # poseid
        "{2}", # n_suffix
        FILE_EXT,
    ))

    BS_HAIR_U = "".join((
        H_MAIN,
        PREFIX_HAIR,
        "{0}", # hair img sit
        "{1}", # hair suffix
        "{2}", # night suffix
        FILE_EXT,
    ))

    BS_HAIR_L = "".join((
        H_MAIN,
        PREFIX_HAIR_LEAN,
        "{0}", # lean
        ART_DLM,
        "{1}", # hair img sit
        "{2}", # hair suffix
        "{3}", # night suffix
        FILE_EXT,
    ))

    BS_TORSO = "".join((
        C_MAIN,
        "{0}/", # clothing img sit
        PREFIX_TORSO,
        "{1}", # hair img sit
        "{2}", # night suffix
        FILE_EXT,
    ))

    BS_TORSO_L = "".join((
        C_MAIN,
        "{0}/", # clothign img sit
        PREFIX_TORSO_LEAN,
        "{1}", # hair img sit
        ART_DLM,
        "{2}", # lean
        "{3}", # night suffix
        FILE_EXT,
    ))

    BS_BODY_U = "".join((
        C_MAIN,
        "{0}/", # clothing img sit
        NEW_BODY_STR,
        "{1}", # night suffix
        FILE_EXT,
    ))

    BS_BODY_L = "".join((
        C_MAIN,
        "{0}/", # clothing img sit
        PREFIX_BODY_LEAN,
        "{1}", # lean
        "{2}", # night suffix
        FILE_EXT,
    ))

    BS_ARMS_NH_U = "".join((
        C_MAIN,
        "{0}/", # clothing img sit
        PREFIX_ARMS,
        "{1}", # arms
        "{2}", # night sfufix
        FILE_EXT,
    ))

    BS_ARMS_NH_L = "".join((
        C_MAIN,
        "{0}/", # clothing img sit
        PREFIX_ARMS_LEAN,
        "{1}", # lean
        ART_DLM,
        "{2}", # arms
        "{3}", # night suffix
        FILE_EXT,
    ))

    ## BLK010
    # ACCESSORY BLACKLIST
    lean_acs_blacklist = [
        "test"
    ]

    # list of available hairstyles
    HAIRS = [
        "def", # ponytail
        "down" # hair down
    ]

    # list of available clothes
    CLOTHES = [
        "def" # school uniform
    ]

    # zoom adjuster
    def adjust_zoom():
        """
        Sets the value zoom to an appropraite amoutn based on the current
        zoom level.
        NOTE: also sets the persistent save for zoom
        """
        global value_zoom, adjust_y
        if zoom_level > default_zoom_level:
            value_zoom = default_value_zoom + (
                (zoom_level-default_zoom_level) * zoom_step
            )
            adjust_y = default_y + ((zoom_level-default_zoom_level) * y_step)

        elif zoom_level < default_zoom_level:
            value_zoom = default_value_zoom - (
                (default_zoom_level-zoom_level) * zoom_step
            )
            adjust_y = default_y
        else:
            # zoom level is at 10
            value_zoom = default_value_zoom
            adjust_y = default_y

        store.persistent._mas_zoom_zoom_level = zoom_level


    def reset_zoom():
        """
        Resets the zoom to the default value
        NOTE: also set sthe persistent save for zoom
        """
        global zoom_level
        zoom_level = default_zoom_level
        adjust_zoom()


    def zoom_out():
        """
        zooms out to the farthest zoom level
        NOTE: also sets the persistent save for zoom
        """
        global zoom_level
        zoom_level = 0
        adjust_zoom()


    # tryparses for the hair and clothes
    # TODO: adjust this for docking station when ready
    def tryparsehair(_hair, default="def"):
        """
        Returns the given hair if it exists, or the default if not exist

        IN:
            _hair - hair to check for existence
            default - default if hair dont exist

        RETURNS:
            the hair if it exists, or default if not
        """
        if _hair in HAIRS:
            return _hair

        return default


    # TODO: adjust this for docking station when ready
    def tryparseclothes(_clothes, default="def"):
        """
        Returns the given clothes if it exists, or the default if not exist

        IN:
            _clothes - clothes to check for existence
            default - default if clothes dont exist

        RETURNS:
            the clothes if it exists, or default if not
        """
        if _clothes in CLOTHES:
            return _clothes

        return default


    ## Accessory dictionary
    ACS_MAP = dict()

    ## hair dictionary
    HAIR_MAP = dict()

    ## clothes dictionary
    CLOTH_MAP = dict()

    ### SP CONSTANTS
    SP_ACS = store.mas_sprites_json.SP_ACS
    SP_HAIR = store.mas_sprites_json.SP_HAIR
    SP_CLOTHES = store.mas_sprites_json.SP_CLOTHES

    SP_MAP = {
        SP_ACS: ACS_MAP,
        SP_HAIR: HAIR_MAP,
        SP_CLOTHES: CLOTH_MAP
    }

    ## Pose list
    # NOTE: do NOT include leans in here.
    POSES = [
        "steepling",
        "crossed",
        "restleftpointright",
        "pointright",
        "down"
    ]

    ## lean poses
    # NOTE: these should be like:
    #   lean|arms
    # NOTE: do NOT include regular poses in here
    L_POSES = [
        "def|def"
    ]

    # all poses 
    # this is purely for iterative purposes
    ALL_POSES = []
    ALL_POSES.extend(POSES)
    ALL_POSES.extend(L_POSES)

    # sprite exprop - list of topics
    EXPROP_TOPIC_MAP = {
        "left-hair-strand-eye-level": [
            "monika_hairclip_select"
        ],
    }

    # sprite acs type - topic
    ACSTYPE_TOPIC_MAP = {
        "ribbon": "monika_ribbon_select"
    }

    def _verify_uprightpose(val):
        return val in POSES


    def _verify_leaningpose(val):
        return val in L_POSES


    def _verify_pose(val, allow_none=True):
        if val is None:
            return allow_none
        return _verify_uprightpose(val) or _verify_leaningpose(val)


    def acs_lean_mode(sprite_list, lean):
        """
        NOTE: DEPRECATED

        Adds the appropriate accessory prefix dpenedong on lean

        IN:
            sprite_list - list to add sprites to
            lean - type of lean
        """
        if lean:
            sprite_list.extend((
                PREFIX_ACS_LEAN,
                lean,
                ART_DLM
            ))

        else:
            sprite_list.append(PREFIX_ACS)


    def face_lean_mode(lean):
        """
        Returns the appropriate face prefix depending on lean

        IN:
            lean - type of lean

        RETURNS:
            appropriat eface prefix string
        """
        if lean:
            return "".join((
                PREFIX_FACE_LEAN,
                lean,
                ART_DLM
            ))

        return PREFIX_FACE


    def create_remover(acs_type, group):
        """
        Creates a remover ACS

        IN:
            acs_type - acs type for the remover. This is also used in mux_type
            group - group of selectables this ACS remover should be linked to
                This is used in the naming of the ACS.

        RETURNS: remover ACS object
        """
        remover_acs = store.MASAccessory(
            group + "-remover",
            "ribbon_blank",
            store.MASPoseMap(
                default="0",
                use_reg_for_l=True
            ),
            stay_on_start=False,
            acs_type=acs_type,
            mux_type=[acs_type]
        )
        init_acs(remover_acs)
        return remover_acs

    def init_acs(mas_acs):
        """
        Initlializes the given MAS accessory into a dictionary map setting

        IN:
            mas_acs - MASAccessory to initialize
        """
        if mas_acs.name in ACS_MAP:
            raise Exception(
                "MASAccessory name '{0}' already exists.".format(mas_acs.name)
            )

        # otherwise, unique name
        ACS_MAP[mas_acs.name] = mas_acs


    def init_hair(mas_hair):
        """
        Initlializes the given MAS hairstyle into a dictionary map setting

        IN:
            mas_hair - MASHair to initialize
        """
        if mas_hair.name in HAIR_MAP:
            raise Exception(
                "MASHair name '{0}' already exists.".format(mas_hair.name)
            )

        # otherwise, unique name
        HAIR_MAP[mas_hair.name] = mas_hair


    def init_clothes(mas_cloth):
        """
        Initlializes the given MAS clothes into a dictionary map setting

        IN:
            mas_clothes - MASClothes to initialize
        """
        if mas_cloth.name in CLOTH_MAP:
            raise Exception(
                "MASClothes name '{0}' already exists.".format(mas_cloth.name)
            )

        # otherwise, unique name
        CLOTH_MAP[mas_cloth.name] = mas_cloth


    def rm_acs(acs):
        """
        Deletes an ACS by removing it from the map

        IN:
            acs - ACS to remove
        """
        if acs.name in ACS_MAP:
            ACS_MAP.pop(acs.name)


    def night_mode(isnight):
        """
        Returns the appropriate night string
        """
        if isnight:
            return NIGHT_SUFFIX

        return ""


    def lock_exprop_topics(exprop):
        """
        Locks topics with the given exprop

        IN:
            exprop - extended property to lock associated topics wtih
        """
        topic_list = EXPROP_TOPIC_MAP.get(exprop, None)
        if topic_list is not None:
            for topic in topic_list:
                store.mas_lockEVL(topic, "EVE")


    def lock_acstype_topics(acs_type):
        """
        Locks topics with the given acs type

        IN:
            acstype - acs type to lock assicated topics with
        """
        topic_label = ACSTYPE_TOPIC_MAP.get(acs_type, None)
        if topic_label is not None:
            store.mas_lockEVL(topic_label, "EVE")


    def unlock_exprop_topics(exprop):
        """
        Unlocks topics with the given exprop

        IN:
            exprop - extended property to unlock associated topics with
        """
        topic_list = EXPROP_TOPIC_MAP.get(exprop, None)
        if topic_list is not None:
            for topic in topic_list:
                store.mas_unlockEVL(topic, "EVE")


    def unlock_acstype_topics(acs_type):
        """
        Unlocks topics with the given acs type

        IN:
            acstype - acs type to unlock associated topics with
        """
        topic_label = ACSTYPE_TOPIC_MAP.get(acs_type, None)
        if topic_label is not None:
            store.mas_unlockEVL(topic, "EVE")


    def should_disable_lean(lean, arms, character):
        """
        Figures out if we need to disable the lean or not based on current
        character settings

        IN:
            lean - lean type we want to do
            arms - arms type involved with lean
            character - MASMonika object

        RETURNS:
            True if we should disable lean, False otherwise
        """
        if lean is None:
            return False

        # otherwise check blacklist elements
        if len(character.lean_acs_blacklist) > 0:
            # monika is wearing a blacklisted accessory
            return True

        larms = lean + "|" + arms

        if not character.hair.pose_map.l_map.get(larms, False):
            return True

        if not character.clothes.pose_map.l_map.get(larms, False):
            return True

        # otherwise, this is good
        return False


    def build_loc():
        """
        RETURNS location string for the sprite
        """
        return "".join(("(", str(adjust_x), ",", str(adjust_y), ")"))


    def get_sprite(sprite_type, sprite_name):
        """
        Returns the sprite object with the given sprite name and sprite type.
        Or None if we couldn't find one.
        """
        # NOTE: we have to use the module because we need updated maps.
        sprite_map = SP_MAP.get(sprite_type, None)
        if sprite_map is None:
            return None

        # otherwise we have a map
        return sprite_map.get(sprite_name, None)


    # special mas monika functions


    def acs_rm_exit_pre_change(temp_space, moni_chr, rm_acs, acs_loc):
        """
        Runs before exit point runs for acs

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            rm_acs - acs we are removing
            acs_loc - acs location to rm this acs from
        """
        pass


    def acs_rm_exit_pst_change(temp_space, moni_chr, rm_acs, acs_loc):
        """
        Runs after exit point runs runs for acs

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            rm_acs - acs we are removing
            acs_loc -  acs location to rm this acs from
        """
        if store.mas_selspr.in_prompt_map(rm_acs.acs_type):
            store.mas_selspr.set_prompt(rm_acs.acs_type, "wear")


    def acs_wear_mux_pre_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs before mux type acs are removed

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        pass


    def acs_wear_mux_pst_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs after mux type acs removed, before insertion 

        IN:
            temp space - temp space
            moni_chr - MASMonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        pass


    def acs_wear_entry_pre_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs after insertion, before entry pooint

        IN:
            temp_space - temp space
            moni_chr - MASmonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        pass


    def acs_wear_entry_pst_change(temp_space, moni_chr, new_acs, acs_loc):
        """
        Runs after entry point

        IN:
            temp_space - temp space
            moni_chr - MASMonika object
            new_acs - acs we are adding
            acs_loc - acs location to wear this acs
        """
        if store.mas_selspr.in_prompt_map(new_acs.acs_type):
            store.mas_selspr.set_prompt(new_acs.acs_type, "change")


    def clothes_exit_pre_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs pre clothes change code. This code is ran prior to clothes being
        changed and prior to exit prog point

        IN:
            temp_space - temporary dictionary space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        pass


    def clothes_exit_pst_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs after exit prog point is ran, before the actual change.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        desired_ribbon = prev_cloth.getprop("desired-ribbon")
        if (
                desired_ribbon is not None
                and desired_ribbon in ACS_MAP
                and moni_chr.is_wearing_hair_with_exprop("ribbon")
        ):
            temp_ribbon = temp_storage.get("hair.ribbon", None)
            if temp_ribbon is None:
                moni_chr.remove_acs(ACS_MAP[desired_ribbon])

            else:
                _acs_wear_if_wearing_acs(
                    moni_chr,
                    ACS_MAP[desired_ribbon],
                    temp_ribbon
                )


    def clothes_entry_pre_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs after change, before entry prog point.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        pass


    def clothes_entry_pst_change(temp_space, moni_chr, prev_cloth, new_cloth):
        """
        Runs after entry prog point

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_cloth - current clothes
            new_cloth - clothes we are changing to
        """
        desired_ribbon = new_cloth.getprop("desired-ribbon")
        if (
                desired_ribbon is not None
                and desired_ribbon in ACS_MAP
                and moni_chr.is_wearing_hair_with_exprop("ribbon")
        ):
            prev_ribbon = moni_chr.get_acs_of_type("ribbon")
            if prev_ribbon != store.mas_acs_ribbon_blank:
                temp_storage["hair.ribbon"] = prev_ribbon

            moni_chr.wear_acs(ACS_MAP[desired_ribbon])

    
    
    def hair_exit_pre_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs pre hair change code. This code is ran prior to hair being
        changed and prior to exit prog point.

        IN:
            temp_space - temporary dictionary space
            moni_chr - MASMonika object
            prev_hair - current hair
            new_hair - hair we are changing to
        """
        pass


    def hair_exit_pst_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs after exit prog point is ran, before the actual change.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_hair - current hair
            new_hair - hair we are changing to
        """
        pass


    def hair_entry_pre_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs after change, before entry prog point.

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            preV_hair - current hair
            new_hair - hair we are changing to
        """
        pass


    def hair_entry_pst_change(temp_space, moni_chr, prev_hair, new_hair):
        """
        Runs after entry prog point

        IN:
            temp_space - temp dict space
            moni_chr - MASMonika object
            prev_hair - current hair
            new_hair - hair we are changing to
        """
        startup = temp_space.get("startup", False)

        if new_hair.hasprop("ribbon"):
            # new hair is enabled for ribbon

            if new_hair.hasprop("ribbon-restore"):
                temp_ribbon = temp_storage.get("hair.ribbon", None)

                # dont force ribbon on startup
                if not startup and temp_ribbon is not None:
                    # force ribbon means that we need to force a ribbon
                    _acs_wear_if_not_wearing_type(
                        moni_chr,
                        "ribbon",
                        temp_ribbon
#                        temp_storage.get(
#                            "hair.ribbon",
#                            store.mas_acs_ribbon_def
#                        )
                    )

            elif new_hair.hasprop("ribbon-off"):
                # take ribbon off for this hairstyle
                _acs_ribbon_save_and_remove(moni_chr)

            if not moni_chr.is_wearing_clothes_with_exprop("baked outfit"):
                # unlock selector for ribbons if you have more than one
                store.mas_filterUnlockGroup(SP_ACS, "ribbon")

            # also change name of the ribbon select prompt
            if moni_chr.is_wearing_acs_type("ribbon"):
                store.mas_selspr.set_prompt("ribbon", "change")
            else:
                store.mas_selspr.set_prompt("ribbon", "wear")

        else:
            # new hair not enabled for ribbon
            _acs_ribbon_save_and_remove(moni_chr)


    # sprite maker functions


    def _ms_accessory(
            sprite_list,
            loc_str,
            acs,
            n_suffix,
            issitting,
            pose=None,
            lean=None
        ):
        """
        Adds accessory string

        IN:
            sprite_list - list to add sprites to
            loc_str - location string
            acs - MASAccessory object
            n_suffix - night suffix to use
            issitting - True will use sitting pic, false will not
            pose - current pose
                (Default: None)
            lean - type of lean
                (Default: None)
        """
        # pose map check
        # Since None means we dont show, we are going to assume that the
        # accessory should be shown if the pose key is missing.
        if lean:
            poseid = acs.pose_map.l_map.get(lean + "|" + pose, None)

            # NOTE: we dont care about leaning as a part of filename
#            if acs.pose_map.use_reg_for_l:
                # clear lean if dont want to use it for rendering
#                lean = None

        else:
            poseid = acs.pose_map.map.get(pose, None)

        if poseid is None:
            # a None here means we should shouldnt' even show this acs
            # for this pose. Weird, but maybe it happens?
            return

        if issitting:
            acs_str = acs.img_sit

        elif acs.img_stand:
            acs_str = acs.img_stand

        else:
            # standing string is null or None
            return

        sprite_list.extend((
            ",",
            loc_str, 
            ',"',
            A_T_MAIN,
            PREFIX_ACS,
#        ))
#        acs_lean_mode(sprite_list, lean)
#        sprite_list.extend((
            acs_str,
            ART_DLM,
            poseid,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_accessorylist(
            sprite_list,
            loc_str, 
            acs_list,
            n_suffix,
            issitting,
            pose=None,
            lean=None
        ):
        """
        Adds accessory strings for a list of accessories

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            acs_list - list of MASAccessory object, in order of rendering
            n_suffix - night suffix to use
            issitting - True will use sitting pic, false will not
            pose - arms pose for we are currently rendering
                (Default: None)
            lean - type of lean
                (Default: None)
        """
        if len(acs_list) == 0:
            return

        temp_acs_list = []

        for acs in acs_list:
            temp_temp_acs_list = []
            _ms_accessory(
                temp_temp_acs_list,
                loc_str,
                acs,
                n_suffix,
                issitting,
                pose,
                lean=lean
            )

            if len(temp_temp_acs_list) > 0:
                temp_acs_list.extend(temp_temp_acs_list)

        if len(temp_acs_list) == 0:
            return

        # otherwise, we could render at least 1 accessory

        # pop the last comman
#        temp_acs_list.pop()

        # NOTE: there is currently no diff between reg and lean
#        if lean:
#            loc_str = LOC_LEAN
#
#        else:
#            loc_str = LOC_REG

        # add the sprites to the list
#        sprite_list.extend((
#            ",",
#            pos_str,
#            ",",
#            L_COMP,
#            "(",
#            LOC_REG,
#            loc_str,
#            ","
#        ))
        sprite_list.extend(temp_acs_list)
#        sprite_list.append(")")


    def _ms_arms(sprite_list, clothing, arms, n_suffix):
        """
        Adds arms string

        IN:
            sprite_list - list to add sprite strings to
            clothing - type of clothing
            arms - type of arms
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_ARMS,
            arms,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_arms_nh(sprite_list, loc_str, clothing, lean, arms, n_suffix):
        """
        Adds arms string, no hair
        delegate.

        IN:
            sprite_list - lits to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            lean - lean type
            arms - arms type
            n_suffix - night suffix to use
        """
#        sprite_list.extend((
#            L_COMP,
#            "(",
#            loc_str,
#            ",",
#            LOC_Z,
#            ',"'
#        ))

        if lean:
            _ms_arms_nh_leaning(
                sprite_list,
                loc_str,
                clothing,
                lean,
                arms,
                n_suffix
            )

        else:
            _ms_arms_nh_up(sprite_list, loc_str, clothing, arms, n_suffix)

        # add final part
#        sprite_list.append('")')


    def _ms_arms_nh_up(sprite_list, loc_str, clothing, arms, n_suffix):
        """
        Adds arms string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            arms - type of arms
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_ARMS,
            arms,
            n_suffix,
            FILE_EXT,
            '"',
        ))


    def _ms_arms_nh_leaning(
            sprite_list,
            loc_str,
            clothing,
            lean,
            arms,
            n_suffix
        ):
        """
        Adds arms string (leaning

        IN:
            sprite_list - list to add sprite strings to
            loc_str - locaiton string
            clothing - type of clothing
            lean - lean type
            arms - type of arms
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_ARMS_LEAN,
            lean,
            ART_DLM,
            arms,
            n_suffix,
            FILE_EXT,
            '"',
        ))


    def _ms_blush(sprite_list, loc_str, blush, n_suffix, f_prefix):
        """
        Adds blush string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            blush - type of blush
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_BLUSH,
            blush,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_body(
            sprite_list,
            loc_str,
            clothing,
            hair,
            n_suffix,
            lean=None,
            arms=""
        ):
        """
        Adds body string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string to use
            clothing - type of clothing
            hair - type of hair
            n_suffix - night suffix to use
            lean - type of lean
                (Default: None)
            arms - type of arms
                # NOTE: DEPRECATED
                (Default: "")
        """
#        sprite_list.extend((
#            I_COMP,
#            "(",
#            loc_str,
#            ","
#        ))

        if lean:
            # leaning is a single parter
            _ms_torsoleaning(
                sprite_list,
                loc_str, 
                clothing,
                hair,
                lean,
                n_suffix,
            )

        else:
            # not leaning is a 2parter
            _ms_torso(sprite_list, loc_str, clothing, hair, n_suffix),
#            sprite_list.append(",")
#            _ms_arms(sprite_list, clothing, arms, n_suffix)

        # add the rest of the parts
#        sprite_list.append(")")


    def _ms_body_nh(
            sprite_list,
            loc_str,
            clothing,
            n_suffix,
            lean=None,
        ):
        """
        Adds body string, with no hair

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            n_suffix - night suffix to use
            lean - type of lean
                (Default: None)
        """
#        sprite_list.extend((
#            I_COMP,
#            "(",
#            loc_str,
#            ","
#        ))

        if lean:
            _ms_torsoleaning_nh(
                sprite_list,
                loc_str,
                clothing,
                lean,
                n_suffix,
            )

        else:
            _ms_torso_nh(sprite_list, loc_str, clothing, n_suffix)

        # add the rest of the parts
#        sprite_list.append(")")


    def _ms_emote(sprite_list, loc_str, emote, n_suffix, f_prefix):
        """
        Adds emote string

        IN:
            sprite_list - list to add sprite strings to
            emote - type of emote
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_EMOTE,
            emote,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_eyebags(sprite_list, eyebags, n_suffix, f_prefix):
        """
        Adds eyebags string

        IN:
            sprite_list - list to add sprite strings to
            eyebags - type of eyebags
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            LOC_Z,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_EYEG,
            eyebags,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_eyebrows(sprite_list, loc_str, eyebrows, n_suffix, f_prefix):
        """
        Adds eyebrow strings

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            eyebrows - type of eyebrows
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_EYEB,
            eyebrows,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_eyes(sprite_list, loc_str, eyes, n_suffix, f_prefix):
        """
        Adds eye string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            eyes - type of eyes
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_EYES,
            eyes,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_face(
            sprite_list,
            loc_str,
            eyebrows,
            eyes,
            nose,
            mouth,
            n_suffix,
            lean=None,
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Adds face string
        (the order these are drawn are in order of argument)

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            n_suffix - night suffix to use
            lean - type of lean
                (Default: None)
            eyebags - type of eyebags
                (Default: None)
            sweat - type of sweat drop
                (Default: None)
            blush - type of blush
                (Default: None)
            tears - type of tears
                (Default: None)
            emote - type of emote
                (Default: None)
        """
#        sprite_list.extend((
#            I_COMP,
#            "(",
#            loc_str,
#        ))

        # setup the face prefix string
        f_prefix = face_lean_mode(lean)

        # now for the required parts
        _ms_eyes(sprite_list, loc_str, eyes, n_suffix, f_prefix)
        _ms_eyebrows(sprite_list, loc_str, eyebrows, n_suffix, f_prefix)
        _ms_nose(sprite_list, loc_str, nose, n_suffix, f_prefix)
        _ms_mouth(sprite_list, loc_str, mouth, n_suffix, f_prefix)

        # and optional parts
#        if eyebags:
#            sprite_list.append(",")
#            _ms_eyebags(sprite_list, eyebags, n_suffix, f_prefix)

        if sweat:
            _ms_sweat(sprite_list, loc_str, sweat, n_suffix, f_prefix)

        if blush:
            _ms_blush(sprite_list, loc_str, blush, n_suffix, f_prefix)

        if tears:
            _ms_tears(sprite_list, loc_str, tears, n_suffix, f_prefix)

        if emote:
            _ms_emote(sprite_list, loc_str, emote, n_suffix, f_prefix)

        # finally the last paren
#        sprite_list.append(")")


    def _ms_hair(sprite_list, loc_str, hair, n_suffix, front_split, lean):
        """
        Creates split hair string for leaning

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string to use
            hair - type of hair
            n_suffix - night suffix to use
            front_split - True means use front split, False means use back
            lean - type of lean
        """
        if front_split:
            hair_suffix = FHAIR_SUFFIX

        else:
            hair_suffix = BHAIR_SUFFIX

#        sprite_list.extend((
#            L_COMP,
#            "(",
#            loc_str,
#            ",",
#            LOC_Z,
#            ',"'
#        ))

        if lean:
            _ms_hair_leaning(
                sprite_list,
                loc_str,
                hair,
                n_suffix,
                hair_suffix,
                lean
            )

        else:
            _ms_hair_up(sprite_list, loc_str, hair, n_suffix, hair_suffix)

        # add final paren
#        sprite_list.append('")')


    def _ms_hair_up(sprite_list, loc_str, hair, n_suffix, hair_suffix):
        """
        Creates split hair string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string to use
            hair - type of hair
            n_suffix - night suffix to use
            hair_suffix - hair suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            H_MAIN,
            PREFIX_HAIR,
            hair,
            hair_suffix,
            n_suffix,
            FILE_EXT,
            '"',
        ))


    def _ms_hair_leaning(
            sprite_list,
            loc_str,
            hair,
            n_suffix,
            hair_suffix,
            lean
        ):
        """
        Creates split hair string for leaning

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string to use
            hair - type of hair
            n_suffix - night suffix to use
            hair_suffix - hair suffix to use
            lean - type of lean
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            H_MAIN,
            PREFIX_HAIR_LEAN,
            lean,
            ART_DLM,
            hair,
            hair_suffix,
            n_suffix,
            FILE_EXT,
            '"',
        ))


    def _ms_head(clothing, hair, head):
        """
        Creates head string

        IN:
            clothing - type of clothing
            hair - type of hair
            head - type of head

        RETURNS:
            head string
        """
        # NOTE: untested
        return "".join([
            build_loc(),
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            head,
            FILE_EXT,
            '"'
        ])


    def _ms_left(clothing, hair, left):
        """
        Creates left side string

        IN:
            clothing - type of clothing
            hair - type of hair
            left - type of left side

        RETURNS:
            left side stirng
        """
        # NOTE UNTESTED
        return "".join([
            build_loc(),
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            left,
            FILE_EXT,
            '"'
        ])


    def _ms_mouth(sprite_list, loc_str, mouth, n_suffix, f_prefix):
        """
        Adds mouth string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            mouth - type of mouse
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_MOUTH,
            mouth,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_nose(sprite_list, loc_str, nose, n_suffix, f_prefix):
        """
        Adds nose string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            nose - type of nose
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        # NOTE: if we never get a new nose, we can just optimize this to
        #   a hardcoded string
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_NOSE,
            nose,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_right(clothing, hair, right):
        """
        Creates right body string

        IN:
            clothing - type of clothing
            hair - type of hair
            right - type of right side

        RETURNS:
            right body string
        """
        # NOTE: UNTESTED
        return "".join([
            build_loc(),
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            head,
            FILE_EXT,
            '"'
        ])


    def _ms_sitting(
            clothing,
            hair,
            hair_split,
            eyebrows,
            eyes,
            nose,
            mouth,
            isnight,
            acs_pre_list,
            acs_bbh_list,
            acs_bfh_list,
            acs_afh_list,
            acs_mid_list,
            acs_pst_list,
            lean=None,
            arms="",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None,
            table="def"
        ):
        """
        Creates sitting string

        IN:
            clothing - type of clothing
            hair - type of hair
            hair_split - true if hair is split into 2 layers
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will genreate night string, false will not
            acs_pre_list - sorted list of MASAccessories to draw prior to body
            acs_bbh_list - sroted list of MASAccessories to draw between back
                hair and body
            acs_bfh_list - sorted list of MASAccessories to draw between body
                and front hair
            acs_afh_list - sorted list of MASAccessories to draw between front
                hair and face
            acs_mid_list - sorted list of MASAccessories to draw between body
                and arms
            acs_pst_list - sorted list of MASAccessories to draw after arms
            lean - type of lean
                (Default: None)
            arms - type of arms
                (Default: "")
            eyebags - type of eyebags
                (Default: None)
            sweat - type of sweatdrop
                (Default: None)
            blush - type of blush
                (Default: None)
            tears - type of tears
                (Default: None)
            emote - type of emote
                (Default: None)
            table - type of table
                (Default: "def")

        RETURNS:
            sitting stirng
        """
        # location string from build loc
        loc_build_str = build_loc()
        loc_build_tup = (",", loc_build_str, ",")

        # night suffix?
        n_suffix = night_mode(isnight)

        # initial portions of list
        sprite_str_list = [
            PRE_SPRITE_STR,
            LOC_REG,
        ]

        ## NOTE: render order:
        #   1. pre-acs - every acs that should render before the body
        #   2. back-hair - back portion of hair (split mode)
        #   3. post-back-hair-acs - acs that should render after back hair, but
        #       before body (split mode)
        #   4. body - the actual body (does not include arms in split mode)
        #   5. table - the table/desk
        #   6. pre-front-hair-acs - acs that should render after body, but
        #       before front hair (split mode)
        #   7. front-hair - front portion of hair (split mode)
        #   8. front-hair-face acs - acs that should render after front hair
        #       but before face (split mode)
        #   9. face - face expressions
        #   10. mid - acs that render between body and arms
        #   11. arms - arms (split mode, lean mode)
        #   12. post-acs - acs that should render after basically everything

        # NOTE: acs in split hair locations end up being rendered at mid
        #   if current split is False


        # 1. pre accessories
        _ms_accessorylist(
            sprite_str_list,
            loc_build_str,
            acs_pre_list,
            n_suffix,
            True,
            arms,
            lean=lean
        )

        # positoin setup
        #sprite_str_list.extend(loc_build_tup)

        if hair_split:

            # 2. back-hair
            _ms_hair(
                sprite_str_list,
                loc_build_str,
                hair,
                n_suffix,
                False,
                lean
            )

            # 3. post back hair acs
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_bbh_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # position setup
            #sprite_str_list.extend(loc_build_tup)

            # 4. body
            _ms_body_nh(
                sprite_str_list,
                loc_build_str,
                clothing,
                n_suffix,
                lean=lean
            )

            # positon setup
            #sprite_str_list.extend(loc_build_tup)

            # 5. Table
            _ms_table(sprite_str_list, loc_build_str, table, n_suffix)

            # 6. pre-front hair acs
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_bfh_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # position setup
            #sprite_str_list.extend(loc_build_tup)

            # 7. front-hair
            _ms_hair(
                sprite_str_list,
                loc_build_str,
                hair,
                n_suffix,
                True,
                lean
            )

            # 8. post-front hair acs
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_afh_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # position setup
            #sprite_str_list.extend(loc_build_tup)

            # 9. face
            _ms_face(
                sprite_str_list,
                loc_build_str,
                eyebrows,
                eyes,
                nose,
                mouth,
                n_suffix,
                lean=lean,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            )


            # 10. between body and arms acs
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_mid_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            #sprite_str_list.extend(loc_build_tup)

            # 11. arms
            _ms_arms_nh(
                sprite_str_list,
                loc_build_str,
                clothing,
                lean,
                arms,
                n_suffix
            )

        else:
            # in thise case, 2,6 are skipped.

            # 4. body
            _ms_body(
                sprite_str_list,
                loc_build_str,
                clothing,
                hair,
                n_suffix,
                lean=lean,
                arms=arms
            )

            # positon setup
            #sprite_str_list.extend(loc_build_tup)

            # 5. Table
            _ms_table(sprite_str_list, loc_build_str, table, n_suffix)

            # 6. post back hair acs gets rendered right after body instead
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_bbh_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # 7. pre-front hair acs gets rendered before arms instead
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_bfh_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # 8. post-front hair acs
            # NOTE: this is consdiered before face
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_afh_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # position setup
            #sprite_str_list.extend(loc_build_tup)

            # 9. face
            _ms_face(
                sprite_str_list,
                loc_build_str,
                eyebrows,
                eyes,
                nose,
                mouth,
                n_suffix,
                lean=lean,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            )

            # 10. between body and arms acs
            _ms_accessorylist(
                sprite_str_list,
                loc_build_str,
                acs_mid_list,
                n_suffix,
                True,
                arms,
                lean=lean
            )

            # no lean means ARMS
            if not lean:
                # position setup
                #sprite_str_list.extend(loc_build_tup)

                # 11. arms
                #   NOTE: force no lean here
                _ms_arms_nh(
                    sprite_str_list,
                    loc_build_str,
                    clothing,
                    None,
                    arms,
                    n_suffix
                )


        # 12. after arms acs
        _ms_accessorylist(
            sprite_str_list,
            loc_build_str,
            acs_pst_list,
            n_suffix,
            True,
            arms,
            lean=lean
        )

        # zoom
        sprite_str_list.extend((
            "),",
            ZOOM,
            str(value_zoom),
            ")"
        ))

        return "".join(sprite_str_list)


    def _ms_standing(clothing, hair, head, left, right, acs_list):
        """
        Creates the custom standing string
        This is different than the stock ones because of image location

        IN:
            clothing - type of clothing
            hair - type of hair
            head - type of head
            left - type of left side
            right - type of right side
            acs_list - list of MASAccessory objects
                NOTE: this should the combined list because we don't have
                    layering in standing mode

        RETURNS:
            custom standing sprite
        """
        # NOTE: UNTESTED
        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            _ms_left(clothing, hair, left),
            ",",
            _ms_right(clothing, hair, right),
            ",",
            _ms_head(clothing, hair, head),
            _ms_accessorylist(acs_list, False, False),
            ")"
        ])


    def _ms_standingstock(head, left, right, acs_list, single=None):
        """
        Creates the stock standing string
        This is different then the custom ones because of image location

        Also no night version atm.

        IN:
            head - type of head
            left - type of left side
            right - type of right side
            acs_list - list of MASAccessory objects
                NOTE: this should be the combined list because we don't have
                    layering in standing mode
            single - type of single standing picture.
                (Defualt: None)

        RETURNS:
            stock standing string
        """
        # TODO: update this to work with the more optimized system for
        # building sprites
        if single:
            return "".join([
                I_COMP,
                "(",
                LOC_STAND,
                ",",
                build_loc(),
                ',"',
                STOCK_ART_PATH,
                single,
                FILE_EXT,
                '"',
#                _ms_accessorylist(acs_list, False, False),
                ")"
            ])

        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            build_loc(),
            ',"',
            STOCK_ART_PATH,
            left,
            FILE_EXT,
            '",',
            build_loc(),
            ',"',
            STOCK_ART_PATH,
            right,
            FILE_EXT,
            '",',
            build_loc(),
            ',"',
            STOCK_ART_PATH,
            head,
            FILE_EXT,
            '"',
#            _ms_accessorylist(acs_list, False, False),
            ")"
        ])


    def _ms_sweat(sprite_list, loc_str, sweat, n_suffix, f_prefix):
        """
        Adds sweatdrop string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            sweat -  type of sweatdrop
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_SWEAT,
            sweat,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_table(sprite_list, loc_str, table, n_suffix):
        """
        Adds table string 

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            table - type of table
            n_suffix - night suffix to use
        """
        # NOTE: testing without I COMP since we only have 1 image
        sprite_list.extend((
            ",",
            loc_str, 
            ',"',
            T_MAIN,
            PREFIX_TABLE,
            table,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_tears(sprite_list, loc_str, tears, n_suffix, f_prefix):
        """
        Adds tear string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            tears - type of tears
            n_suffix - night suffix to use
            f_prefix - face prefix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            F_T_MAIN,
            f_prefix,
            PREFIX_TEARS,
            tears,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_torso(sprite_list, loc_str, clothing, hair, n_suffix):
        """
        Adds torso string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            hair - type of hair
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str, 
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_TORSO,
            hair,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_torso_nh(sprite_list, loc_str, clothing, n_suffix):
        """
        Adds torso string, no hair

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str, 
            ',"',
            C_MAIN,
            clothing,
            "/",
            NEW_BODY_STR,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_torsoleaning(sprite_list, loc_str, clothing, hair, lean, n_suffix):
        """
        Adds torso leaning string

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            hair - type of ahri
            lean - type of leaning
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_TORSO_LEAN,
            hair,
            ART_DLM,
            lean,
            n_suffix,
            FILE_EXT,
            '"'
        ))


    def _ms_torsoleaning_nh(sprite_list, loc_str, clothing, lean, n_suffix):
        """
        Adds torso leaning string, no hair

        IN:
            sprite_list - list to add sprite strings to
            loc_str - location string
            clothing - type of clothing
            lean - type of leaning
            n_suffix - night suffix to use
        """
        sprite_list.extend((
            ",",
            loc_str,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_BODY_LEAN,
            lean,
            n_suffix,
            FILE_EXT,
            '"'
        ))


# Dynamic sprite builder
# retrieved from a Dress Up Renpy Cookbook
# https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=30643

init -2 python:
#    import renpy.store as store
#    import renpy.exports as renpy # we need this so Ren'Py properly handles rollback with classes
#    from operator import attrgetter # we need this for sorting items
    import math
    from collections import namedtuple

    # Monika character base
    class MASMonika(renpy.store.object):
        import store.mas_sprites as mas_sprites

        # CONSTANTS
        PRE_ACS = 0 # PRE ACCESSORY (before body)
        MID_ACS = 1 # MID ACCESSORY (right before arms)
        PST_ACS = 2 # post accessory (after arms)
        BBH_ACS = 3 # betweeen Body and Back Hair accessory
        BFH_ACS = 4 # between Body and Front Hair accessory
        AFH_ACS = 5 # between face and front hair accessory

        # valid rec layers
        REC_LAYERS = (
            PRE_ACS,
            MID_ACS,
            PST_ACS,
            BBH_ACS,
            BFH_ACS,
            AFH_ACS
        )


        def __init__(self):
            """
            Constructor
            """
            self.name="Monika"
            self.haircut="default"
            self.haircolor="default"
            self.skin_hue=0 # monika probably doesn't have different skin color
            self.lipstick="default" # i guess no lipstick

            self.clothes = mas_clothes_def # default clothes is school outfit
            self.hair = mas_hair_def # default hair is the usual whtie ribbon
            #self.table = mas_table_def # default table 

            # list of lean blacklisted accessory names currently equipped
            self.lean_acs_blacklist = []

            # accesories to be rendereed before anything
            self.acs_pre = []

            # accessories to be rendered after back hair, before body
            self.acs_bbh = []

            # accessories to be rendered after body, before front hair
            self.acs_bfh = []

            # accessories to be rendered after fornt hair, before arms
            self.acs_afh = []

            # accessories to be rendreed between body and face expressions
            self.acs_mid = []

            # accessories to be rendered last
            self.acs_pst = []

            self.hair_hue=0 # hair color?

            # setup acs dict
            self.acs = {
                self.PRE_ACS: self.acs_pre,
                self.MID_ACS: self.acs_mid,
                self.PST_ACS: self.acs_pst,
                self.BBH_ACS: self.acs_bbh,
                self.BFH_ACS: self.acs_bfh,
                self.AFH_ACS: self.acs_afh
            }

            # use this dict to map acs IDs with which acs list they are in.
            # this will increase speed of removal and checking.
            self.acs_list_map = {}

            # LOCK VARS
            # True if we should block any changes to hair
            self.lock_hair = False

            # True if we should block any chnages to clothes
            self.lock_clothes = False

            # True if we should block any changes to cas
            self.lock_acs = False


        def __get_acs(self, acs_type):
            """
            Returns the accessory list associated with the given type

            IN:
                acs_type - the accessory type to get

            RETURNS:
                accessory list, or None if the given acs_type is not valid
            """
            return self.acs.get(acs_type, None)


        def _load(self,
                _clothes_name,
                _hair_name,
                _acs_pre_names,
                _acs_bbh_names,
                _acs_bfh_names,
                _acs_afh_names,
                _acs_mid_names,
                _acs_pst_names,
                startup=False
            ):
            """
            INTERNAL

            load function using names/IDs

            IN:
                _clothes_name - name of clothing to load
                _hair_name - name of hair to load
                _acs_pre_names - list of pre acs names to load
                _acs_bbh_names - list of bbh acs names to load
                _acs_bfh_names - list of bfh acs names to load
                _acs_afh_names - list of afh acs names to load
                _acs_mid_names - list of mid acs names to load
                _acs_pst_names - list of pst acs names to load,
                startup - True if we are loading on start, False if not
                    (Default: False)
            """
            # clothes and hair
            self.change_outfit(
                store.mas_sprites.CLOTH_MAP[_clothes_name],
                store.mas_sprites.HAIR_MAP[_hair_name],
                startup=startup
            )

            # acs
            self._load_acs(_acs_pre_names, self.PRE_ACS)
            self._load_acs(_acs_bbh_names, self.BBH_ACS)
            self._load_acs(_acs_bfh_names, self.BFH_ACS)
            self._load_acs(_acs_afh_names, self.AFH_ACS)
            self._load_acs(_acs_mid_names, self.MID_ACS)
            self._load_acs(_acs_pst_names, self.PST_ACS)


        def _load_acs(self, per_acs, acs_type):
            """
            Loads accessories from the given persistent into the given
            acs type.

            IN:
                per_acs - persistent list to grab acs from
                acs_type - acs type to load acs into
            """
            for acs_name in per_acs:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs:
                    self.wear_acs_in(_acs, acs_type)


        def _load_acs_obj(self, acs_objs, acs_type):
            """
            Loads accessories from a given list of accessory objects into
            the given acs type

            IN:
                acs_objs - list of acs to load
                acs_type - acs type to load acs into
            """
            for _acs in acs_objs:
                # must verify sprite before loading
                if _acs.name in store.mas_sprites.ACS_MAP:
                    self.wear_acs_in(_acs, acs_type)


        def _save_acs(self, acs_type, force_acs=False):
            """
            Generates list of accessory names to save to persistent.

            IN:
                acs_type - acs type to build acs names list
                force_acs - True means to save acs even if stay_on_start is
                    False
                    (Default: False)

            RETURNS:
                list of acs names to save to persistent
            """
            return [
                acs.name
                for acs in self.acs[acs_type]
                if force_acs or acs.stay_on_start
            ]


        def _save_acs_obj(self, acs_type, force_acs=False):
            """
            Generaltes list of acs objects to save

            IN:
                acs_type - acs type to buld acs list
                force_acs - True means to save acs even if stay_on_start is
                    False
                    (Default: False)

            RETURNS:
                list of acs objects to save
            """
            return [
                acs
                for acs in self.acs[acs_type]
                if force_acs or acs.stay_on_start
            ]


        @staticmethod
        def _verify_rec_layer(val, allow_none=True):
            if val is None:
                return allow_none
            return val in MASMonika.REC_LAYERS


        def change_clothes(self, new_cloth, by_user=None, startup=False):
            """
            Changes clothes to the given cloth. also sets the persistent
            force clothes var to by_user, if its not None

            IN:
                new_cloth - new clothes to wear
                by_user - True if this action was mandated by the user, False
                    if not. If None, we do NOT set the forced clothes var
                    (Default: None)
                startup - True if we are loading on startup, False if not
                    When True, we dont respect locking
                    (Default: False)
            """
            if self.lock_clothes and not startup:
                return

            # setup temp space
            temp_space = {
                "by_user": by_user,
                "startup": startup,
            }

            prev_cloth = self.clothes

            # run pre clothes change logic
            store.mas_sprites.clothes_exit_pre_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )

            # exit point
            self.clothes.exit(self, new_clothes=new_cloth)

            # post exit, pre change
            store.mas_sprites.clothes_exit_pst_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )

            # change
            self.clothes = new_cloth

            # post change, pre entry
            store.mas_sprites.clothes_entry_pre_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )

            # entry point
            self.clothes.entry(self, prev_clothes=prev_cloth)

            # post entry point
            store.mas_sprites.clothes_entry_pst_change(
                temp_space,
                self,
                prev_cloth,
                new_cloth
            )

            if by_user is not None:
                persistent._mas_force_clothes = bool(by_user)


        def change_hair(self, new_hair, by_user=None, startup=False):
            """
            Changes hair to the given hair. also sets the persistent force
            hair var to by_user, if its not None

            IN:
                new_hair - new hair to wear
                by_user - True if this action was mandated by the user, False
                    if not. If None, we do NOT set the forced hair var
                    (Default: None)
                startup - True if we are loading on startup, False if not
                    When True, we dont respect locking
                    (Default: False)
            """
            if self.lock_hair and not startup:
                return

            # setup temp space
            temp_space = {
                "by_user": by_user,
                "startup": startup,
            }

            prev_hair = self.hair

            # run pre hair change logic
            store.mas_sprites.hair_exit_pre_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )

            # exit point
            self.hair.exit(self, new_hair=new_hair)

            # post exit , pre hair change
            store.mas_sprites.hair_exit_pst_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )

            # change
            self.hair = new_hair

            # post change, pre entry
            store.mas_sprites.hair_entry_pre_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )

            # entry point
            self.hair.entry(self, prev_hair=prev_hair)

            # post entry point
            store.mas_sprites.hair_entry_pst_change(
                temp_space,
                self,
                prev_hair,
                new_hair
            )

            if by_user is not None:
                persistent._mas_force_hair = bool(by_user)


        def change_outfit(
                self,
                new_cloth,
                new_hair,
                by_user=None,
                startup=False
            ):
            """
            Changes both clothes and hair. also sets the persisten forced vars
            to by_user, if its not None

            IN:
                new_cloth - new clothes to wear
                new_hair - new hair to wear
                by_user - True if this action ws mandated by user, False if not
                    If None, we do NOT set the forced vars
                    (Default: None)
                startup - True if we are loading on startup, False if not
                    (Default: False)
            """
            self.change_clothes(new_cloth, by_user=by_user, startup=startup)
            self.change_hair(new_hair, by_user=by_user, startup=startup)


        def get_acs_of_exprop(self, exprop, get_all=False):
            """
            Gets the acs objects currently being work of a given ex prop

            IN:
                exprop - extended property to check for
                get_all - True means we get all acs being worn of this exprop
                    False will return the first one
                    (Default: False)

            RETURNS: single matching acs or None if get_all is False, list of 
                matching acs or empty list if get_all is True.
            """
            if get_all:
                acs_items = []
            else:
                acs_items = None

            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.hasprop(exprop):
                    if get_all:
                        acs_items.append(_acs)

                    else:
                        return _acs

            return acs_items


        def get_acs_of_type(self, acs_type, get_all=False):
            """
            Gets the acs objects currently being worn of a given type.

            IN:
                acs_type - acs type to check for
                get_all - True means we get all acs being worn of this type,
                    False will just return the first one
                    (Default: False)

            RETURNS: single matchin acs or None if get_all is False. list of
                matching acs or empty list if get_all is True.
            """
            if get_all:
                acs_items = []
            else:
                acs_items = None

            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.acs_type == acs_type:
                    if get_all:
                        acs_items.append(_acs)
                    else:
                        return _acs

            return acs_items


        def get_outfit(self):
            """
            Returns the current outfit

            RETURNS:
                tuple:
                    [0] - current clothes
                    [1] - current hair
            """
            return (self.clothes, self.hair)


        def is_wearing_acs(self, accessory):
            """
            Checks if currently wearing the given accessory

            IN:
                accessory - accessory to check

            RETURNS:
                True if wearing accessory, false if not
            """
            return accessory.name in self.acs_list_map


        def is_wearing_acs_with_exprop(self, exprop):
            """
            Checks if currently wearing any accessory with given exprop

            IN:
                exprop - extended property to check

            RETURNS: True if wearing accessory, False if not
            """
            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.hasprop(exprop):
                    return True

            return False


        def is_wearing_acs_type(self, acs_type):
            """
            Checks if currently wearing any accessory with given type

            IN:
                acs_type - accessory type to check

            RETURNS: True if wearing acccesroy, False if not
            """
            for acs_name in self.acs_list_map:
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.acs_type == acs_type:
                    return True

            return False


        def is_wearing_acs_types(self, *acs_types):
            """
            multiple arg version of is_wearing_acs_type

            IN:
                *acs_types - any number of acs types to check

            RETURNS: True if any the ACS types checks are True, False if not
            """
            for acs_type in acs_types:
                if self.is_wearing_acs_type(acs_type):
                    return True

            return False


        def is_wearing_acs_in(self, accessory, acs_type):
            """
            Checks if the currently wearing the given accessory as the given
            accessory type

            IN:
                accessory - accessory to check
                acs_type - accessory type to check

            RETURNS:
                True if wearing accessory, False if not
            """
            acs_list = self.__get_acs(acs_type)

            if acs_list is not None:
                return accessory in acs_list

            return False


        def is_wearing_clothes_with_exprop(self, exprop):
            """
            Checks if we are currently wearing clothes with the given exprop

            IN:
                exprop - extended property to check

            RETURNS: True if wearing clothes with the exprop, False if not
            """
            return self.clothes.hasprop(exprop)


        def is_wearing_hair_with_exprop(self, exprop):
            """
            Checks if we are currently wearing hair with the given exprop

            IN:
                exprop - extend property to check

            RETURNS: True if wearing hair with the exprop, False if not
            """
            return self.hair.hasprop(exprop)


        def load(self, startup=False):
            """
            Loads hair/clothes/accessories from persistent.

            IN:
                startup - True if loading on start, False if not
                    When True, we dont respesct locking
                    (Default: False)
            """
            self._load(
                store.persistent._mas_monika_clothes,
                store.persistent._mas_monika_hair,
                store.persistent._mas_acs_pre_list,
                store.persistent._mas_acs_bbh_list,
                store.persistent._mas_acs_bfh_list,
                store.persistent._mas_acs_afh_list,
                store.persistent._mas_acs_mid_list,
                store.persistent._mas_acs_pst_list,
                startup=startup
            )


        # TODO: consider adding startup to this
        def load_state(self, _data, as_prims=False):
            """
            Loads clothes/hair/acs from a tuple data format that was saved
            using the save_state function.

            IN:
                _data - data to load from. tuple of the following format:
                    [0]: clothes data
                    [1]: hair data
                    [2]: pre acs data
                    [3]: bbh acs data
                    [4]: bfh acs data
                    [5]: afh acs data
                    [6]: mid acs data
                    [7]: pst acs data
                as_prims - True if this data was saved as primitive data types,
                    false if as objects
                    (Default: False)
            """
            if as_prims:
                # for prims, we can just call an existing function
                self._load(*_data)
                return

            # otherwise, we need to set things ourselves
            # clothes and hair
            self.change_outfit(_data[0], _data[1])

            # acs
            self._load_acs_obj(_data[2], self.PRE_ACS)
            self._load_acs_obj(_data[3], self.BBH_ACS)
            self._load_acs_obj(_data[4], self.BFH_ACS)
            self._load_acs_obj(_data[5], self.AFH_ACS)
            self._load_acs_obj(_data[6], self.MID_ACS)
            self._load_acs_obj(_data[7], self.PST_ACS)


        def reset_all(self, by_user=None):
            """
            Resets all of monika

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, we do NOT set force vars.
                    (Default: None)
            """
            self.reset_clothes(by_user)
            self.reset_hair(by_user)
            self.remove_all_acs()


        def remove_acs(self, accessory):
            """
            Removes the given accessory. this uses the map to determine where
            the accessory is located.

            IN:
                accessory - accessory to remove
            """
            self.remove_acs_in(
                accessory,
                self.acs_list_map.get(accessory.name, None)
            )


        def remove_acs_exprop(self, exprop):
            """
            Removes all ACS of given exprop.

            IN:
                exprop - exprop to check for
            """
            for acs_name in self.acs_list_map.keys():
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.hasprop(exprop):
                    self.remove_acs_in(_acs, self.acs_list_map[acs_name])


        def remove_acs_mux(self, mux_types):
            """
            Removes all ACS with a mux type in the given list.

            IN:
                mux_types - list of acs_types to remove from acs
            """
            for acs_name in self.acs_list_map.keys():
                _acs = store.mas_sprites.ACS_MAP.get(acs_name, None)
                if _acs and _acs.acs_type in mux_types:
                    self.remove_acs_in(_acs, self.acs_list_map[acs_name])


        def remove_acs_in(self, accessory, acs_type):
            """
            Removes the given accessory from the given accessory list type

            IN:
                accessory - accessory to remove
                acs_type - ACS type
            """
            if self.lock_acs:
                return

            acs_list = self.__get_acs(acs_type)
            temp_space = {
                "acs_list": acs_list,
            }

            if acs_list is not None and accessory in acs_list:

                # run pre exit point code
                store.mas_sprites.acs_rm_exit_pre_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )

                # run programming point
                accessory.exit(self)

                # run post exit code
                store.mas_sprites.acs_rm_exit_pst_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )

                # cleanup blacklist
                if accessory.name in self.lean_acs_blacklist:
                    self.lean_acs_blacklist.remove(accessory.name)

                # cleanup mapping
                if accessory.name in self.acs_list_map:
                    self.acs_list_map.pop(accessory.name)

                # now remove
                acs_list.remove(accessory)


        def remove_all_acs(self):
            """
            Removes all accessories from all accessory lists
            """
            self.remove_all_acs_in(self.PRE_ACS)
            self.remove_all_acs_in(self.BBH_ACS)
            self.remove_all_acs_in(self.BFH_ACS)
            self.remove_all_acs_in(self.AFH_ACS)
            self.remove_all_acs_in(self.MID_ACS)
            self.remove_all_acs_in(self.PST_ACS)


        def remove_all_acs_in(self, acs_type):
            """
            Removes all accessories from the given accessory type

            IN:
                acs_type - ACS type to remove all
            """
            if self.lock_acs:
                return

            if acs_type in self.acs:
                # need to clear blacklisted
                for acs in self.acs[acs_type]:
                    # run programming point
                    acs.exit(self)

                    # cleanup blacklist
                    if acs.name in self.lean_acs_blacklist:
                        self.lean_acs_blacklist.remove(acs.name)

                    # remove from mapping
                    if acs.name in self.acs_list_map:
                        self.acs_list_map.pop(acs.name)

                self.acs[acs_type] = list()


        def reset_clothes(self, by_user=None):
            """
            Resets clothing to default

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, then we do NOT set force clothed vars
                    (Default: None)
            """
            self.change_clothes(mas_clothes_def, by_user)


        def reset_hair(self, by_user=None):
            """
            Resets hair to default

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, then we do NOT set forced hair vars
                    (Default: None)
            """
            self.change_hair(mas_hair_def, by_user)


        def reset_outfit(self, by_user=None):
            """
            Resetse clothing and hair to default

            IN:
                by_user - True if this action was mandated by user, False if
                    not. If None, then we do NOT set forced vars
                    (Default: None)
            """
            self.reset_clothes(by_user)
            self.reset_hair(by_user)


        def save(self, force_hair=False, force_clothes=False, force_acs=False):
            """
            Saves hair/clothes/acs to persistent

            IN:
                force_hair - True means we force hair saving even if
                    stay_on_start is False
                    (Default: False)
                force_clothes - True means we force clothes saving even if
                    stay_on_start is False
                    (Default: False)
                force_acs - True means we force acs saving even if
                    stay_on_start is False
                    (Default: False)
            """
            # hair and clothes
            if force_hair or self.hair.stay_on_start:
                store.persistent._mas_monika_hair = self.hair.name

            if force_clothes or self.clothes.stay_on_start:
                store.persistent._mas_monika_clothes = self.clothes.name

            # acs
            store.persistent._mas_acs_pre_list = self._save_acs(
                self.PRE_ACS,
                force_acs
            )
            store.persistent._mas_acs_bbh_list = self._save_acs(
                self.BBH_ACS,
                force_acs
            )
            store.persistent._mas_acs_bfh_list = self._save_acs(
                self.BFH_ACS,
                force_acs
            )
            store.persistent._mas_acs_afh_list = self._save_acs(
                self.AFH_ACS,
                force_acs
            )
            store.persistent._mas_acs_mid_list = self._save_acs(
                self.MID_ACS,
                force_acs
            )
            store.persistent._mas_acs_pst_list = self._save_acs(
                self.PST_ACS,
                force_acs
            )


        def save_state(self,
                force_hair=False,
                force_clothes=False,
                force_acs=False,
                as_prims=False
            ):
            """
            Saves hair/clothes/acs to a tuple data format that can be loaded
            later using the load_state function.

            IN:
                force_hair - True means force hair saving even if stay_on_start
                    is False. If False and stay_on_start is False, the default
                    hair will be returned.
                    (Default: False)
                force_clothes - True meanas force clothes saving even if
                    stay_on_start is False. If False and stay_on_start is
                    False, the default clothes will be returned.
                    (Default: False)
                force_acs - True means force acs saving even if stay_on_start
                    is False. At minimum, this will be an empty list.
                    (Default: False)
                as_prims - True means to save the data as primitive types
                    for persistent saving. False will save the data as
                    objects.
                    (Default: False)

            RETURNS tuple of the following format:
                [0]: clothes data (Default: mas_clothes_def)
                [1]: hair data (Default: mas_hair_def)
                [2]: pre acs data (Default: [])
                [3]: bbh acs data (Default: [])
                [4]: bfh acs data (Default: [])
                [5]: afh acs data (Default: [])
                [6]: mid acs data (Default: [])
                [7]: pst acs data (Default: [])
            """
            # determine which clothes to save
            if force_clothes or self.clothes.stay_on_start:
                cloth_data = self.clothes
            else:
                cloth_data = mas_clothes_def

            # determine which hair to save
            if force_hair or self.hair.stay_on_start:
                hair_data = self.hair
            else:
                hair_data = mas_hair_def

            # determine acs to save as well as final data for hair and clothes
            if as_prims:
                cloth_data = cloth_data.name
                hair_data = hair_data.name
                pre_acs_data = self._save_acs(self.PRE_ACS, force_acs)
                bbh_acs_data = self._save_acs(self.BBH_ACS, force_acs)
                bfh_acs_data = self._save_acs(self.BFH_ACS, force_acs)
                afh_acs_data = self._save_acs(self.AFH_ACS, force_acs)
                mid_acs_data = self._save_acs(self.MID_ACS, force_acs)
                pst_acs_data = self._save_acs(self.PST_ACS, force_acs)

            else:
                pre_acs_data = self._save_acs_obj(self.PRE_ACS, force_acs)
                bbh_acs_data = self._save_acs_obj(self.BBH_ACS, force_acs)
                bfh_acs_data = self._save_acs_obj(self.BFH_ACS, force_acs)
                afh_acs_data = self._save_acs_obj(self.AFH_ACS, force_acs)
                mid_acs_data = self._save_acs_obj(self.MID_ACS, force_acs)
                pst_acs_data = self._save_acs_obj(self.PST_ACS, force_acs)

            # finally return results
            return (
                cloth_data,
                hair_data,
                pre_acs_data,
                bbh_acs_data,
                bfh_acs_data,
                afh_acs_data,
                mid_acs_data,
                pst_acs_data
            )


        def wear_acs(self, acs):
            """
            Wears the given accessory in that accessory's recommended
            spot, as defined by the accessory.

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, acs.get_rec_layer())


        def wear_acs_in(self, accessory, acs_type):
            """
            Wears the given accessory

            IN:
                accessory - accessory to wear
                acs_type - accessory type (location) to wear this accessory
            """
            if self.lock_acs or accessory.name in self.acs_list_map:
                # we never wear dupes
                return

            acs_list = self.__get_acs(acs_type)
            temp_space = {
                "acs_list": acs_list,
            }

            if acs_list is not None and accessory not in acs_list:

                # run pre exclusion code
                store.mas_sprites.acs_wear_mux_pre_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )

                # run mutual exclusion for acs
                if accessory.mux_type is not None:
                    self.remove_acs_mux(accessory.mux_type)

                # run post exclusion code
                store.mas_sprites.acs_wear_mux_pst_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )

                # now insert the acs
                mas_insertSort(acs_list, accessory, MASAccessory.get_priority)

                # add to mapping
                self.acs_list_map[accessory.name] = acs_type

                if accessory.name in mas_sprites.lean_acs_blacklist:
                    self.lean_acs_blacklist.append(accessory.name)

                # run pre entry
                store.mas_sprites.acs_wear_entry_pre_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )

                # run programming point for acs
                accessory.entry(self)

                # run post entry
                store.mas_sprites.acs_wear_entry_pst_change(
                    temp_space,
                    self,
                    accessory,
                    acs_type
                )


        def wear_acs_pre(self, acs):
            """
            Wears the given accessory in the pre body accessory mode

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.PRE_ACS)


        def wear_acs_bbh(self, acs):
            """
            Wears the given accessory in the post back hair accessory loc

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.BBH_ACS)


        def wear_acs_bfh(self, acs):
            """
            Wears the given accessory in the pre front hair accesory log

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.BFH_ACS)


        def wear_acs_afh(self, acs):
            """
            Wears the given accessory in the between front hair and arms
            acs log

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.AFH_ACS)


        def wear_acs_mid(self, acs):
            """
            Wears the given accessory in the mid body acessory mode

            IN:
                acs - acessory to wear
            """
            self.wear_acs_in(acs, self.MID_ACS)


        def wear_acs_pst(self, acs):
            """
            Wears the given accessory in the post body accessory mode

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.PST_ACS)


    # hues, probably not going to use these
#    hair_hue1 = im.matrix([ 1, 0, 0, 0, 0,
#                        0, 1, 0, 0, 0,
#                        0, 0, 1, 0, 0,
#                        0, 0, 0, 1, 0 ])
#    hair_hue2 = im.matrix([ 3.734, 0, 0, 0, 0,
#                        0, 3.531, 0, 0, 0,
#                        0, 0, 1.375, 0, 0,
#                        0, 0, 0, 1, 0 ])
#    hair_hue3 = im.matrix([ 3.718, 0, 0, 0, 0,
#                        0, 3.703, 0, 0, 0,
#                        0, 0, 3.781, 0, 0,
#                        0, 0, 0, 1, 0 ])
#    hair_hue4 = im.matrix([ 3.906, 0, 0, 0, 0,
#                        0, 3.671, 0, 0, 0,
#                        0, 0, 3.375, 0, 0,
#                        0, 0, 0, 1, 0 ])
#    skin_hue1 = hair_hue1
#    skin_hue2 = im.matrix([ 0.925, 0, 0, 0, 0,
#                        0, 0.840, 0, 0, 0,
#                        0, 0, 0.806, 0, 0,
#                        0, 0, 0, 1, 0 ])
#    skin_hue3 = im.matrix([ 0.851, 0, 0, 0, 0,
#                        0, 0.633, 0, 0, 0,
#                        0, 0, 0.542, 0, 0,
#                        0, 0, 0, 1, 0 ])
#
#    hair_huearray = [hair_hue1,hair_hue2,hair_hue3,hair_hue4]
#
#    skin_huearray = [skin_hue1,skin_hue2,skin_hue3]

    # pose map helps map poses to an image
    class MASPoseMap(renpy.store.object):
        """
        The Posemap helps connect pose names to images

        This is done via a dict containing pose names and where they
        map to.

        There is also a seperate dict to handle lean variants
        """
        from store.mas_sprites import POSES, L_POSES
        import store.mas_sprites_json as msj


        # all params
        CONS_PARAM_NAMES = (
            "default", 
            "l_default",
            "use_reg_for_l",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "p6",
        )


        def __init__(self,
                # NOTE: when updating params, make sure to modify param name
                #   lists above accordingly.
                default=None,
                l_default=None,
                use_reg_for_l=False,
                p1=None,
                p2=None,
                p3=None,
                p4=None,
                p5=None,
                p6=None
            ):
            """
            Constructor

            If None is passed in for any var, we assume that no image should
            be shown for that pose

            NOTE: all defaults are None

            IN:
                default - default pose id to use for poses that are not
                    specified (aka are None).
                l_default - default pose id to use for lean poses that are not
                    specified (aka are None).
                use_reg_for_l - if True and default is not None and l_default
                    is None, then we use the default instead of l_default
                    when rendering for lean poses
                p1 - pose id to use for pose 1
                    - steepling
                p2 - pose id to use for pose 2
                    - crossed
                p3 - pose id to use for pose 3
                    - restleftpointright
                p4 - pose id to use for pose 4
                    - pointright
                p5 - pose id to use for pose 5
                    - LEAN: def|def
                p6 - pose id to use for pose 6
                    - down
            """
            self.map = {
                self.POSES[0]: p1,
                self.POSES[1]: p2,
                self.POSES[2]: p3,
                self.POSES[3]: p4,
                self.POSES[4]: p6
            }
            self.l_map = {
                self.L_POSES[0]: p5
            }
            self.use_reg_for_l = use_reg_for_l

            self.__set_posedefs(self.map, default)
            if use_reg_for_l and l_default is None and default is not None:
                self.__set_posedefs(self.l_map, default)
            else:
                self.__set_posedefs(self.l_map, l_default)

            # use all map for quick pose lookup
            self.__all_map = {}
            self.__all_map.update(self.map)
            self.__all_map.update(self.l_map)


        def __set_posedefs(self, pose_dict, _def):
            """
            Sets pose defaults

            IN:
                pose_dict - dict of poses
                _def - default to use here
            """
            for k in pose_dict:
                if pose_dict[k] is None:
                    pose_dict[k] = _def


        def get(self, pose, defval):
            """
            Get passed to the internal pose map
            only because its common to call get on this object. 

            IN:
                pose - pose to get from pose map
                defval - default value to return if pose not found

            RETURNS:
                value of pose in internal dict, or defval if not found
            """
            return self.__all_map.get(pose, defval)


        @classmethod
        def fromJSON(cls, json_obj, is_acs, is_fallback, errs, warns):
            """
            Builds a MASPoseMap given a JSON format of it

            IN:
                json_obj - json object to parse
                is_acs - True if the MASPoseMap should be built with acs
                    in mind, False otherwise.
                is_fallback - True if the MASPoseMap should be built with
                    fallback mode in mind, False otherwise.
                    NOTE: if is_acs is True, this is ignored

            OUT:
                errs - list to save error message to
                warns - list to save warning messages to

            RETURNS: MASPoseMap object built using the JSON, or None if failed
            """
            isbad = False

            if is_acs:
                is_fallback = False

            # go through the json object and validate everything
            for prop_name in json_obj.keys():
                if prop_name in cls.CONS_PARAM_NAMES:
                    prop_val = json_obj[prop_name]
            
                    if is_acs and prop_name != "use_reg_for_l":

                        if not cls.msj._verify_str(prop_val):
                            # acs mode must be strings
                            isbad = True
                            errs.append(cls.msj.MSG_ERR_IDD.format(
                                cls.msj.MPM_ACS_BAD_POSE_TYPE.format(
                                    prop_name,
                                    str,
                                    type(prop_val)
                                )
                            ))

                    elif is_fallback and prop_name != "use_reg_for_l":

                        if not cls.msj._verify_pose(prop_val):
                            # fallback mode must verify pose
                            isbad = True
                            errs.append(cls.msj.MSG_ERR_IDD.format(
                                cls.msj.MPM_BAD_POSE.format(prop_name, prop_val)
                            ))

                    elif not cls.msj._verify_bool(prop_val):
                        # otherwise, we in non fallback mode or
                        # verifying the one boolean
                        isbad = True
                        errs.append(cls.msj.MSG_ERR_IDD.format(
                            cls.msj.BAD_TYPE.format(
                                prop_name,
                                bool,
                                type(prop_val)
                            )
                        ))

                    # else case is a valid param

                else:
                    # prop name NOT part of MASPoseMap. log as warning.
                    json_obj.pop(prop_name)
                    warns.append(cls.msj.MSG_WARN_IDD.format(
                        cls.msj.EXTRA_PROP.format(prop_name)
                    ))

            # now for suggestsions based on defaults
            # I am expecting that we will have more ACS than outfits.
            if is_acs or is_fallback:
                _param_default = json_obj.get("default", None)
                _param_l_default = json_obj.get("l_default", None)
                _param_urfl = json_obj.get("use_reg_for_l", False)
                    
                if _param_default is None:
                    # we suggest using default when in fallback mode or acs
                    if is_acs:
                        warn_msg = cls.msj.MPM_ACS_DEF

                    else:
                        warn_msg = cls.msj.MPM_FB_DEF

                    warns.append(cls.msj.MSG_WARN_IDD.format(warn_msg))

                if _param_l_default is None and not _param_urfl:
                    # we suggest using lean default when in fallback mode or 
                    #   acs
                    # and not using reg for l
                    if is_acs:
                        warn_msg = cls.msj.MPM_ACS_DEF_L

                    else:
                        warn_msg = cls.msj.MPM_FB_DEF_L

                    warns.append(cls.msj.MSG_WARN_IDD.format(warn_msg))

            # finally check for valid params
            if isbad:
                return None

            return cls(**json_obj)


    # base class for MAS sprite things
    class MASSpriteBase(renpy.store.object):
        """
        Base class for MAS sprite objects

        PROPERTIES:
            name - name of the item
            img_sit - filename of the sitting version of the item
            img_stand - filename of the standing version of the item
            pose_map - MASPoseMap object that contains pose mappings
            stay_on_start - determines if the item stays on startup
            entry_pp - programmign point to call when wearing this sprite
                the MASMonika object that is being changed is fed into this
                function
                NOTE: this is called after the item is added to MASMonika
            exit_pp - programming point to call when taking off this sprite
                the MASMonika object that is being changed is fed into this
                function
                NOTE: this is called before the item is removed from MASMonika
            is_custom - True if this is a custom object. False if not.
                NOTE: this must be set AFTER object creation
        """
        import store.mas_sprites_json as msj


        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=False,
                entry_pp=None,
                exit_pp=None,
                ex_props={}
            ):
            """
            MASSpriteBase constructor

            IN:
                name - name of this item
                img_sit - filename of the sitting image
                pose_map - MASPoseMAp object that contains pose mappings
                img_stand - filename of the standing image
                    If this is not passed in, this is considered blacklisted
                    from standing sprites.
                    (Default: "")
                stay_on_start - True means the item should reappear on startup
                    False means the item should always drop when restarting.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: empty dict)
            """
            self.__sp_type = -1
            self.name = name
            self.img_sit = img_sit
            self.img_stand = img_stand
            self.stay_on_start = stay_on_start
            self.pose_map = pose_map
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp
            self.ex_props = ex_props
            self.is_custom = False

            if type(pose_map) != MASPoseMap:
                raise Exception("PoseMap is REQUIRED")


        def __eq__(self, other):
            """
            Equality override
            """
            if isinstance(other, MASSpriteBase):
                return self.name == other.name

            return NotImplemented


        def __ne__(self, other):
            """
            Not equal override
            """
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result


        def addprop(self, prop):
            """
            Adds the given prop to the ex_props list

            IN:
                prop - prop to add
            """
            self.ex_props[prop] = True


        def entry(self, _monika_chr, **kwargs):
            """
            Calls the entry programming point if it exists

            IN:
                _monika_chr - the MASMonika object being changed
                **kwargs - other keyword args to pass
            """
            if self.entry_pp is not None:
                self.entry_pp(_monika_chr, **kwargs)


        def exit(self, _monika_chr, **kwargs):
            """
            Calls the exit programming point if it exists

            IN:
                _monika_chr - the MASMonika object being changed
                **kwargs - other keyword args to pass
            """
            if self.exit_pp is not None:
                self.exit_pp(_monika_chr, **kwargs)


        def getprop(self, prop, defval=None):
            """
            Gets the exprop

            IN:
                prop - prop to get
                defval - default value to return if prop not found
            """
            return self.ex_props.get(prop, defval)

    
        def gettype(self):
            """
            Gets the type of this sprite object

            RETURNS: type of this sprite object
            """
            return self.__sp_type


        def hasprogpoints(self):
            """
            RETURNS: true if this sprite object has at least 1 non-null prog
                point, False otherwise
            """
            return self.entry_pp is not None or self.exit_pp is not None


        def hasprop(self, prop):
            """
            Checks if this sprite object has the given prop

            IN:
                prop - prop in ex_props to look for

            RETURNS: True if this sprite object has the ex_prop, False if not
            """
            return prop in self.ex_props


        def rmprop(self, prop):
            """
            Removes the prop from this sprite's ex_props, if it exists

            IN:
                prop - prop to remove

            RETURNS: True if the prop was found and removed, False otherwise
            """
            if prop in self.ex_props:
                self.ex_props.pop(prop)
                return True

            return False


        @staticmethod
        def sortkey(sprite_base):
            """
            Returns the sorting key of the given MASSpriteBase object
            """
            if isinstance(sprite_base, MASSpriteBase):
                return sprite_base.name

            return ""


    class MASSpriteFallbackBase(MASSpriteBase):
        """
        MAS sprites that can use pose maps as fallback maps.

        PROPERTIES:
            fallback - If true, the PoseMap contains fallbacks that poses
                will revert to. If something is None, then it means to
                blacklist.

        SEE MASSpriteBase for inherited properties
        """

        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=False,
                fallback=False,
                entry_pp=None,
                exit_pp=None,
                ex_props={}
            ):
            """
            MASSpriteFallbackBase constructor

            IN:
                name - name of this item
                img_sit - filename of the sitting image for this item
                pose_map - MASPoseMap object that contains pose mappings or
                    fallback mappings
                img_stand - filename of the stnading image
                    If this is not passed in, this is considered blacklisted
                    from standing sprites.
                    (Default: "")
                stay_on_start - True means the item should reappear on startup
                    False means the item should always drop when restarting
                    (Default: False)
                fallback - True means the MASPoseMap includes fallback codes
                    for each pose instead of just enable/disable rules.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: empty dict)
            """
            super(MASSpriteFallbackBase, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                entry_pp,
                exit_pp,
                ex_props
            )
            self.__sp_type = -2
            self.fallback = fallback


        def get_fallback(self, pose, lean):
            """
            Gets the fallback pose for a given pose or lean

            NOTE: the fallback variable is NOT checked

            Lean is checked first if its not None.

            IN:
                pose - pose to retrieve fallback for
                lean - lean to retrieve fallback for

            RETURNS:
                tuple fo thef ollowing format:
                [0]: arms type
                    - default for this is steepling
                [1]: lean type
                    - defualt for this is None
            """
            # now check for fallbacks
            if lean is not None:
                # we have a lean, check for fallbacks
                fb_lean = self.pose_map.l_map.get(lean + "|" + pose, None)

                # no fallback? assume steepling
                if fb_lean is None:
                    return ("steepling", None)

                # a pipe means we are dealing with a lean fallback
                if "|" in fb_lean:
                    return fb_lean.split("|")

                # otherwise we can assume its an arms fall back
                return (fb_lean, None)

            # otherwise check the pose
            return (self.pose_map.map.get(pose, "steepling"), None)


    # instead of clothes, these are accessories
    class MASAccessory(MASSpriteBase):
        """
        MASAccesory objects

        PROPERTIES:
            rec_layer - recommended layer to place this accessory
            priority - render priority. Lower is rendered first
            acs_type - an optional type to help organize acs
            mux_type - list of acs types that we shoudl treat
                as mutally exclusive with this type. Basically if this acs is
                worn, all acs with a type in this property are removed.

        SEE MASSpriteBase for inherited properties
        """


        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                rec_layer=MASMonika.PST_ACS,
                priority=10,
                stay_on_start=False,
                entry_pp=None,
                exit_pp=None,
                acs_type=None,
                mux_type=None,
                ex_props={}
            ):
            """
            MASAccessory constructor

            IN:
                name - name of this accessory
                img_sit - file name of the sitting image
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - file name of the standing image
                    IF this is not passed in, we assume the standing version
                        has no accessory.
                    (Default: "")
                rec_layer - recommended layer to place this accessory
                    (Must be one the ACS types in MASMonika)
                    (Default: MASMonika.PST_ACS)
                priority - render priority. Lower is rendered first
                    (Default: 10)
                stay_on_start - True means the accessory is saved for next
                    startup. False means the accessory is dropped on next
                    startup.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                acs_type - type, for ease of organization of acs
                    This works with mux type to determine if an ACS can work
                    with another ACS.
                    (Default: None)
                mux_type - list of acs types that should be
                    mutually exclusive with this acs.
                    this works with acs_type to determine if this works with
                    other ACS.
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: empty dict)

            """
            super(MASAccessory, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                entry_pp,
                exit_pp,
                ex_props
            )
            self.__rec_layer = rec_layer
            self.__sp_type = store.mas_sprites_json.SP_ACS
            self.priority=priority
            self.acs_type = acs_type
            self.mux_type = mux_type

            # this is for "Special Effects" like a scar or a wound, that
            # shouldn't be removed by undressing.
#            self.can_strip=can_strip

        @staticmethod
        def get_priority(acs):
            """
            Gets the priority of the given accessory

            This is for sorting
            """
            return acs.priority


        def get_rec_layer(self):
            """
            Returns the recommended layer ofr this accessory

            RETURNS:
                recommend MASMOnika accessory type for this accessory
            """
            return self.__rec_layer


        def _build_loadstrs(self):
            """
            Builds list of strings for this sprite object that represent the
            image paths that this sprite object would use.

            RETURNS: list of strings 
            """
            loadstrs = []

            # loop over MASPoseMap for pose ids
            for pose in store.mas_sprites.ALL_POSES:
                poseid = self.pose_map.get(pose, "_ignore")

                # add both day and night versions
                loadstrs.append(store.mas_sprites.BS_ACS.format(
                    self.img_sit,
                    poseid,
                    ""
                ))
                loadstrs.append(store.mas_sprites.BS_ACS.format(
                    self.img_sit,
                    poseid,
                    store.mas_sprites.NIGHT_SUFFIX
                ))

            return loadstrs


    class MASHair(MASSpriteFallbackBase):
        """
        MASHair objects

        Representations of hair items

        PROPERTIES:
            split - MASPoseMap object that determins if a pose has split hair
                or not.
                if a pose has True, it is split. False or None means no split.

        SEE MASSpriteFallbackBase for inherited properties

        POSEMAP explanations:
            Use an empty string to
        """

        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=True,
                fallback=False,
                entry_pp=None,
                exit_pp=None,
                split=None,
                ex_props={}
            ):
            """
            MASHair constructor

            IN;
                name - name of this hairstyle
                img_sit - filename of the sitting image for this hairstyle
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - filename of the standing image for this hairstyle
                    If this is not passed in, this is considered blacklisted
                        from standing sprites.
                    (Default: "")
                stay_on_strat - True means the hairstyle should reappear on
                    startup. False means a restart clears the hairstyle
                    (Default: True)
                fallback - True means the MASPoseMap includes fallback codes
                    for each pose instead of just enable/disable rules.
                    (Default: False)
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                split - MASPoseMap object saying which hair has splits or Not.
                    If None, we assume hair has splits for everything.
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: empty dict)
            """
            super(MASHair, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                fallback,
                entry_pp,
                exit_pp,
                ex_props
            )
            self.__sp_type = store.mas_sprites_json.SP_HAIR

            if split is not None and type(split) != MASPoseMap:
                raise Exception("split MUST be PoseMap")

            self.split = split


        def _build_loadstrs(self):
            """
            Bulids list of strings for this psrite object that reprsent the
            image paths that this sprite object wuld use.

            RETURNS: list of strings
            """
            loadstrs = []
            all_split = self.split is None

            # loop over poses and only return strings for ones that
            # are split
            for pose in store.mas_sprites.POSES:
                if all_split or self.split.get(pose, False):
                    # need front
                    loadstrs.append(store.mas_sprites.BS_HAIR_U.format(
                        self.img_sit,
                        store.mas_sprites.FHAIR_SUFFIX,
                        ""
                    ))
                    loadstrs.append(store.mas_sprites.BS_HAIR_U.format(
                        self.img_sit,
                        store.mas_sprites.FHAIR_SUFFIX,
                        store.mas_sprites.NIGHT_SUFFIX
                    ))

                    # and back
                    loadstrs.append(store.mas_sprites.BS_HAIR_U.format(
                        self.img_sit,
                        store.mas_sprites.BHAIR_SUFFIX,
                        ""
                    ))
                    loadstrs.append(store.mas_sprites.BS_HAIR_U.format(
                        self.img_sit,
                        store.mas_sprites.BHAIR_SUFFIX,
                        store.mas_sprites.NIGHT_SUFFIX
                    ))

            # and for leaning
            for lpose in store.mas_sprites.L_POSES:
                lean = lpose.partition("|")[0]
                if all_split or self.split.get(lpose, False):
                    # front
                    loadstrs.append(store.mas_sprites.BS_HAIR_L.format(
                        lean,
                        self.img_sit,
                        store.mas_sprites.FHAIR_SUFFIX,
                        ""
                    ))
                    loadstrs.append(store.mas_sprites.BS_HAIR_L.format(
                        lean,
                        self.img_sit,
                        store.mas_sprites.FHAIR_SUFFIX,
                        store.mas_sprites.NIGHT_SUFFIX
                    ))

                    # back
                    loadstrs.append(store.mas_sprites.BS_HAIR_L.format(
                        lean,
                        self.img_sit,
                        store.mas_sprites.BHAIR_SUFFIX,
                        ""
                    ))
                    loadstrs.append(store.mas_sprites.BS_HAIR_L.format(
                        lean,
                        self.img_sit,
                        store.mas_sprites.BHAIR_SUFFIX,
                        store.mas_sprites.NIGHT_SUFFIX
                    ))

            return loadstrs


    class MASClothes(MASSpriteFallbackBase):
        """
        MASClothes objects

        Representations of clothes

        PROPERTIES:
            hair_map - dict of available hair styles for these clothes
                keys should be hair name properites. Values should also be
                hair name properties.
                use "all" to signify a default hair style for all mappings that
                are not found.

        SEE MASSpriteFallbackBase for inherited properties
        """
        import store.mas_sprites as mas_sprites


        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                stay_on_start=False,
                fallback=False,
                hair_map={},
                entry_pp=None,
                exit_pp=None,
                ex_props={}
            ):
            """
            MASClothes constructor

            IN;
                name - name of these clothes
                img_sit - filename of the sitting image for these clothes
                pose_map - MASPoseMap object that contains pose mappings
                img_stand - filename of the standing image for these clothes
                    If this is not passed in, this is considered blacklisted
                        from standing sprites.
                    (Default: "")
                stay_on_start - True means the clothes should reappear on
                    startup. False means a restart clears the clothes
                    (Default: False)
                fallback - True means the MASPoseMap includes fallback codes
                    for each pose instead of just enable/disable rules
                    (Default: False)
                hair_map - dict of available hair styles and what they map to
                    These should all be strings. To signify a default, add
                    a single item called "all" with the value being the hair
                    to map to.
                    NOTE: use the name property for hairstyles.
                    (Default: {})
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    sprite object.
                    (Default: empty dict)
            """
            super(MASClothes, self).__init__(
                name,
                img_sit,
                pose_map,
                img_stand,
                stay_on_start,
                fallback,
                entry_pp,
                exit_pp,
                ex_props
            )
            self.__sp_type = store.mas_sprites_json.SP_CLOTHES

            self.hair_map = hair_map

            # add defaults if we need them
            if "all" in hair_map:
                for hair_name in mas_sprites.HAIR_MAP:
                    if hair_name not in self.hair_map:
                        self.hair_map[hair_name] = self.hair_map["all"]


        def get_hair(self, hair):
            """
            Given a hair type, grabs the available mapping for this hair type

            IN:
                hair - hair type to get mapping for

            RETURNS:
                the hair mapping to use inplace for the given hair type
            """
            return self.hair_map.get(hair, self.hair_map.get("all", hair))


        def has_hair_map(self):
            """
            RETURNS: True if we have a mapping to check, False otherwise
            """
            return len(self.hair_map) > 0


        def _build_loadstrs(self):
            """
            Builds list of strings for this sprite object that represent the
            image paths that this sprite object would use.

            RETURNS: list of strings
            """
            # case 1: (split hair)
            #   body-<type>.png
            #   body-<type>-n.png
            #   body-leaning-<type>.png
            #   body-leaning-<type>-n.png
            #   arms-<pose>.png
            #   arms-<pose>-n.png
            #   arms-leaning-<type>-<arms>.png
            #   arms-leaning-<type>-<arms>-n.png
            #
            # case 2: (non split hair)
            #   torso-<hair>.png
            #   torso-<hair>-n.png
            #   torso-leaning-<hair>-<lean>.png
            #   torso-leaning-<hair>-<lean>-n.png
            #   arms-<pose>.png
            #   arms-<pose>-n.png
            #
            # NOTE: JSONs will NOT support non-split hair.
            #   aka ONLY CASE 1 IS SUPPORTED
            to_verify = []

            # starting with body types
            to_verify.append(store.mas_sprites.BS_BODY_U.format(
                self.img_sit,
                ""
            ))
            to_verify.append(store.mas_sprites.BS_BODY_U.format(
                self.img_sit,
                store.mas_sprites.NIGHT_SUFFIX
            ))

            # body leaning
            # this needs to iterate over leaning types
            for lpose in store.mas_sprites.L_POSES:
                lean = lpose.partition("|")[0]
                to_verify.append(store.mas_sprites.BS_BODY_L.format(
                    self.img_sit,
                    lean,
                    ""
                ))
                to_verify.append(store.mas_sprites.BS_BODY_L.format(
                    self.img_sit,
                    lean,
                    store.mas_sprites.NIGHT_SUFFIX
                ))

            # arms
            for pose in store.mas_sprites.POSES:
                to_verify.append(store.mas_sprites.BS_ARMS_NH_U.format(
                    self.img_sit,
                    pose,
                    ""
                ))
                to_verify.append(store.mas_sprites.BS_ARMS_NH_U.format(
                    self.img_sit,
                    pose,
                    store.mas_sprites.NIGHT_SUFFIX
                ))

            # arms leaning
            for lpose in store.mas_sprites.L_POSES:
                lean, pipe_sep, arms = lpose.partition("|")
                to_verify.append(store.mas_sprites.BS_ARMS_NH_L.format(
                    self.img_sit,
                    lean,
                    arms,
                    ""
                ))
                to_verify.append(store.mas_sprites.BS_ARMS_NH_L.format(
                    self.img_sit,
                    lean,
                    arms,
                    store.mas_sprites.NIGHT_SUFFIX
                ))

            return to_verify


    # The main drawing function...
    def mas_drawmonika(
            st,
            at,
            character,

            # requried sitting parts
            eyebrows,
            eyes,
            nose,
            mouth,

            # optional sitting parts
            lean=None,
            arms="steepling",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None,

            # optional standing parts
            head="",
            left="",
            right="",
            stock=True,
            single=None
        ):
        """
        Draws monika dynamically
        NOTE: custom standing stuff not ready for usage yet.
        NOTE: the actual drawing of accessories happens in the respective
            functions instead of here.
        NOTE: because of how clothes, hair, and body is tied together,
            monika can only have 1 type of clothing and 1 hair style
            at a time.

        IN:
            st - renpy related
            at - renpy related
            character - MASMonika character object
            eyebrows - type of eyebrows (sitting)
            eyes - type of eyes (sitting)
            nose - type of nose (sitting)
            mouth - type of mouth (sitting)
            head - type of head (standing)
            left - type of left side (standing)
            right - type of right side (standing)
            lean - type of lean (sitting)
                (Default: None)
            arms - type of arms (sitting)
                (Default: "steepling")
            eyebags - type of eyebags (sitting)
                (Default: None)
            sweat - type of sweatdrop (sitting)
                (Default: None)
            blush - type of blush (sitting)
                (Default: None)
            tears - type of tears (sitting)
                (Default: None)
            emote - type of emote (sitting)
                (Default: None)
            stock - True means we are using stock standing, False means not
                (standing)
                (Default: True)
            single - type of single standing image (standing)
                (Default: None)
        """

        # gather accessories
        acs_pre_list = character.acs.get(MASMonika.PRE_ACS, [])
        acs_bbh_list = character.acs.get(MASMonika.BBH_ACS, [])
        acs_bfh_list = character.acs.get(MASMonika.BFH_ACS, [])
        acs_afh_list = character.acs.get(MASMonika.AFH_ACS, [])
        acs_mid_list = character.acs.get(MASMonika.MID_ACS, [])
        acs_pst_list = character.acs.get(MASMonika.PST_ACS, [])

        # are we sitting or not
        if is_sitting:

            if store.mas_sprites.should_disable_lean(lean, arms, character):
                # set lean to None if its on the blacklist
                # NOTE: this function checks pose_maps
                lean = None
                arms = "steepling"

            # fallback adjustments:
            if character.hair.fallback:
                arms, lean = character.hair.get_fallback(arms, lean)

            if character.clothes.fallback:
                arms, lean = character.clothes.get_fallback(arms, lean)

            # get the mapped hair for the current clothes
            if character.clothes.has_hair_map():
                hair = store.mas_sprites.HAIR_MAP.get(
                    character.clothes.get_hair(character.hair.name),
                    mas_hair_def
                )

            else:
                hair = character.hair

            # determine hair split
            if hair.split is None:
                hair_split = True

            elif lean:
                # we assume split if lean not found
                hair_split = hair.split.get(lean + "|" + arms, True)

            else:
                # not leaning, still assume true if arms not found
                hair_split = hair.split.get(arms, True)


            cmd = store.mas_sprites._ms_sitting(
                character.clothes.img_sit,
                hair.img_sit,
                hair_split,
                eyebrows,
                eyes,
                nose,
                mouth,
                not morning_flag,
                acs_pre_list,
                acs_bbh_list,
                acs_bfh_list,
                acs_afh_list,
                acs_mid_list,
                acs_pst_list,
                lean=lean,
                arms=arms,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            )

        else:
        # TODO: this is missing img_stand checks
        # TODO change this to an elif and else the custom stnading mode
#        elif stock:
            # stock standing mode
            cmd = store.mas_sprites._ms_standingstock(
                head,
                left,
                right,
                [], # TODO maybe need a ring in standing mode?
                single=single
            )

#        else:
            # custom standing mode

        return eval(cmd),None # Unless you're using animations, you can set refresh rate to None

# Monika
define monika_chr = MASMonika()

#### IMAGE START (IMG030)
# Image are created using a DynamicDisplayable to allow for runtime changes
# to sprites without having to remake everything. This saves us on image
# costs.
#
# To create a new image, these parts are required:
#   eyebrows, eyes, nose, mouth (for sitting)
#   head, left, right OR a single image (for standing)
#
# Optional parts for sitting is:
#   sweat, tears, blush, emote, eyebags
#
# Non-leaning poses require an ARMS part.
# leaning poses require a LEAN part.
#
# For more information see mas_drawmonika function
#
#### FOLDER IMAGE RULES: (IMG031)
# To ensure that the images are created correctly, all images must be placed in
# a specific folder heirarchy.
#
# mod_assets/monika/f/<facial expressions>
# mod_assets/monika/c/<clothing types>/<body/arms/poses>
# mod_assets/monika/h/<hair types>
# mod_assets/monika/a/<accessories>
#
# All layers must have a night version, which is denoted using the -n suffix.
# All leaning layers must have a non-leaning fallback
#
## FACIAL EXPRESSIONS:
# Non leaning filenames:
#   face-{face part type}-{face part name}{-n}.png
#   (ie: face-mouth-big.png / face-mouth-big-n.png)
# leaning filenames:
#   face-leaning-{lean type}-{face part type}-{face part name}{-n}.png
#   (ie: face-leaning-eyes-sparkle.png / face-leaning-eyes-sparkle-n.png)
#
## BODY / POSE:
# NEW
# Non leaning:
#   body-def{-n}.png
#   arms-{arms name}{-n}.png
# Leaning:
#   body-leaning-{lean type}{-n}.png
#   arms-leaning-{lean type}-{arms pose}{-n}.png
#
# OLD:
# Non leaning filenames / parts:
#   torso-{hair type}{-n}.png
#   arms-{arms name}{-n}.png
#   (ie: torso-def.png / torso-def-n.png)
#   (ie: arms-def-steepling.png / arms-def-steepling-n.png)
# Leaning filenames:
#   torso-leaning-{hair type}-{lean name}{-n}.png
#   (ie: torso-leaning-def-def.png / torso-leaning-def-def-n.png)
#
## HAIR:
# hair-{hair type}-{front/back}{-n}.png
#

# NOTE: all sprites moved to sprite-chart-00

### [IMG032]
# Image aliases
# NOTE: if you want to use a standing sprite, it must be one of these
#   HOWEVER: you may need to use the static variants because not every
#   sprite has closed eye versions.
#   The only sprite combos with closed eyes standing are _sc and _sd.
#   everything else does not have a closed eye variant. sux to succ

# pose 1
image monika 1 = "monika 1esa"
image monika 1a = "monika 1eua"
image monika 1b = "monika 1eub"
image monika 1c = "monika 1euc"
image monika 1d = "monika 1eud"
image monika 1e = "monika 1eka"
image monika 1f = "monika 1ekc"
image monika 1g = "monika 1ekd"
image monika 1h = "monika 1esc"
image monika 1i = "monika 1esd"
image monika 1j = "monika 1hua"
image monika 1k = "monika 1hub"
image monika 1l = "monika 1hksdlb"
image monika 1ll = "monika 1hksdrb"
image monika 1m = "monika 1lksdla"
image monika 1mm = "monika 1rksdla"
image monika 1n = "monika 1lksdlb"
image monika 1nn = "monika 1rksdlb"
image monika 1o = "monika 1lksdlc"
image monika 1oo = "monika 1rksdlc"
image monika 1p = "monika 1lksdld"
image monika 1pp = "monika 1rksdld"
image monika 1q = "monika 1dsc"
image monika 1r = "monika 1dsd"

# pose 2
image monika 2 = "monika 2esa"
image monika 2a = "monika 2eua"
image monika 2b = "monika 2eub"
image monika 2c = "monika 2euc"
image monika 2d = "monika 2eud"
image monika 2e = "monika 2eka"
image monika 2f = "monika 2ekc"
image monika 2g = "monika 2ekd"
image monika 2h = "monika 2esc"
image monika 2i = "monika 2esd"
image monika 2j = "monika 2hua"
image monika 2k = "monika 2hub"
image monika 2l = "monika 2hksdlb"
image monika 2ll = "monika 2hksdrb"
image monika 2m = "monika 2lksdla"
image monika 2mm = "monika 2rksdla"
image monika 2n = "monika 2lksdlb"
image monika 2nn = "monika 2rksdlb"
image monika 2o = "monika 2lksdlc"
image monika 2oo = "monika 2rksdlc"
image monika 2p = "monika 2lksdld"
image monika 2pp = "monika 2rksdld"
image monika 2q = "monika 2dsc"
image monika 2r = "monika 2dsd"

# pose 3
image monika 3 = "monika 3esa"
image monika 3a = "monika 3eua"
image monika 3b = "monika 3eub"
image monika 3c = "monika 3euc"
image monika 3d = "monika 3eud"
image monika 3e = "monika 3eka"
image monika 3f = "monika 3ekc"
image monika 3g = "monika 3ekd"
image monika 3h = "monika 3esc"
image monika 3i = "monika 3esd"
image monika 3j = "monika 3hua"
image monika 3k = "monika 3hub"
image monika 3l = "monika 3hksdlb"
image monika 3ll = "monika 3hksdrb"
image monika 3m = "monika 3lksdla"
image monika 3mm = "monika 3rksdla"
image monika 3n = "monika 3lksdlb"
image monika 3nn = "monika 3rksdlb"
image monika 3o = "monika 3lksdlc"
image monika 3oo = "monika 3rksdlc"
image monika 3p = "monika 3lksdld"
image monika 3pp = "monika 3rksdld"
image monika 3q = "monika 3dsc"
image monika 3r = "monika 3dsd"

# pose 4
image monika 4 = "monika 4esa"
image monika 4a = "monika 4eua"
image monika 4b = "monika 4eub"
image monika 4c = "monika 4euc"
image monika 4d = "monika 4eud"
image monika 4e = "monika 4eka"
image monika 4f = "monika 4ekc"
image monika 4g = "monika 4ekd"
image monika 4h = "monika 4esc"
image monika 4i = "monika 4esd"
image monika 4j = "monika 4hua"
image monika 4k = "monika 4hub"
image monika 4l = "monika 4hksdlb"
image monika 4ll = "monika 4hksdrb"
image monika 4m = "monika 4lksdla"
image monika 4mm = "monika 4rksdla"
image monika 4n = "monika 4lksdlb"
image monika 4nn = "monika 4rksdlb"
image monika 4o = "monika 4lksdlc"
image monika 4oo = "monika 4rksdlc"
image monika 4p = "monika 4lksdld"
image monika 4pp = "monika 4rksdld"
image monika 4q = "monika 4dsc"
image monika 4r = "monika 4dsd"

# pose 5
image monika 5 = "monika 5eua"
image monika 5a = "monika 5eua"
image monika 5b = "monika 5euc"

### [IMG040]
# Custom animated sprites
# Currently no naming convention, but please keep them somehwat consistent
# with the current setup:
# <pose number>ATL_<short descriptor>
#
# NOTE: if we do blinking, please make that a separate section from this

image monika 6ATL_cryleftright:
    block:

        # select an image
        block:
            choice:
                "monika 6lktsc"
            choice:
                "monika 6rktsc"

        # select a wait time
        block:
            choice:
                0.9
            choice:
                1.0
            choice:
                0.5
            choice:
                0.7
            choice:
                0.8

        repeat

# similar to cryleft and right
# meant for DISTRESSED
image monika 6ATL_lookleftright:

    # select image
    block:
        choice:
            "monika 6rkc"
        choice:
            "monika 6lkc"

    # select a wait time
    block:
        choice:
            5.0
        choice:
            6.0
        choice:
            7.0
        choice:
            8.0
        choice:
            9.0
        choice:
            10.0
    repeat

### [IMG045]
# special purpose ATLs that cant really be used for other things atm

# Below 0 to upset affection
image monika ATL_0_to_upset:

    # 1 time this part
    "monika 1esc"
    5.0

    # repeat this part
    block:
        # select image
        block:
            choice 0.95:
                "monika 1esc"
            choice 0.05:
                "monika 5tsc"

        # select wait time
        block:
            choice:
                10.0
            choice:
                12.0
            choice:
                14.0
            choice:
                16.0
            choice:
                18.0
            choice:
                20.0

        repeat

# affectionate
image monika ATL_affectionate:
    # select image
    block:
        choice 0.02:
            "monika 1eua"
            1.0
            choice:
                "monika 1sua"
                4.0
            choice:
                "monika 1kua"
                1.5
            "monika 1eua"

        choice 0.98:
            choice 0.94898:
                "monika 1eua"
            choice 0.051020:
                "monika 1hua"

    # select wait time
    block:
        choice:
            20.0
        choice:
            22.0
        choice:
            24.0
        choice:
            26.0
        choice:
            28.0
        choice:
            30.0

    repeat

# enamored
image monika ATL_enamored:

    # 1 time this part
    "monika 1eua"
    5.0

    # repeat
    block:
        # select image
        block:
            choice 0.02:
                "monika 1eua"
                1.0
                choice:
                    "monika 1sua"
                    4.0
                choice:
                    "monika 1kua"
                    1.5
                "monika 1eua"

            choice 0.98:
                choice 0.765306:
                    "monika 1eua"
                choice 0.112245:
                    "monika 5esu"
                choice 0.061224:
                    "monika 5tsu"
                choice 0.061224:
                    "monika 1huu"

        # select wait time
        block:
            choice:
                20.0
            choice:
                22.0
            choice:
                24.0
            choice:
                26.0
            choice:
                28.0
            choice:
                30.0

        repeat

# love
image monika ATL_love:

    # 1 time this parrt
    "monika 1eua"
    5.0

    # repeat
    block:
        # select image
        block:
            choice 0.02:
                "monika 1eua"
                1.0
                choice:
                    "monika 1sua"
                    4.0
                choice:
                    "monika 1kua"
                    1.5
                "monika 1eua"

            choice 0.98:
                choice 0.510104:
                    "monika 1eua"
                choice 0.255102:
                    "monika 5esu"
                choice 0.091837:
                    "monika 5tsu"
                choice 0.091837:
                    "monika 1huu"
                choice 0.051020:
                    "monika 5eubla"

        # select wait time
        block:
            choice:
                20.0
            choice:
                22.0
            choice:
                24.0
            choice:
                26.0
            choice:
                28.0
            choice:
                30.0

        repeat


### [IMG050]
# condition-switched images for old school image selecting
image monika idle = ConditionSwitch(
    "mas_isMoniBroken(lower=True)", "monika 6ckc",
    "mas_isMoniDis()", "monika 6ATL_lookleftright",
    "mas_isMoniUpset()", "monika 2efc",
    "mas_isMoniNormal() and mas_isBelowZero()", "monika ATL_0_to_upset",
    "mas_isMoniHappy()", "monika 1eua",
    "mas_isMoniAff()", "monika ATL_affectionate",
    "mas_isMoniEnamored()", "monika ATL_enamored",
    "mas_isMoniLove()", "monika ATL_love",
    "True", "monika 1esa",
    predict_all=True
)


### [IMG100]
# chibi monika sprites
image chibika smile = "gui/poemgame/m_sticker_1.png"
image chibika sad = "mod_assets/other/m_sticker_sad.png"
image chibika 3 = "gui/poemgame/m_sticker_2.png"

#Ghost monika
image ghost_monika: 
    "mod_assets/other/ghost_monika.png" 
    zoom 1.25
