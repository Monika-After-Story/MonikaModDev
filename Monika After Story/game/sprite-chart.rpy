# Monika's sprites!
# To add a new image, please scroll to the IMAGE section (IMG030)
# Accesories are in (IMG020)
#
###### SPRITE CODE (IMG010)
#
# The sprite code system is a way of picking an appropriate sprite without
# having to look up what the sprite looks like.
# All expressions use this code system. the original 19 expressions (with
# counterparts have been aliased to the correct code system. Please avoid
# using the og 19+ coutnerparts)
#
# For aliases, see (IMG032)
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
#   c - crazy eyes (crazy) NOTE: UNUSED
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
default persistent._mas_acs_pre_list = list()
default persistent._mas_acs_mid_list = list()
default persistent._mas_acs_pst_list = list()

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

init -5 python in mas_sprites:
    # specific image generation functions

    # main art path
    MOD_ART_PATH = "mod_assets/monika/"
    STOCK_ART_PATH = "monika/"

    # delimiters
    ART_DLM = "-"

    # important keywords
    KW_STOCK_ART = "def"

    ### other paths:
    # H - hair (and body by connection)
    # C - clothing
    # T - sitting
    # S - standing
    # F - face parts
    # A - accessories
    C_MAIN = MOD_ART_PATH + "c/"
    F_MAIN = MOD_ART_PATH + "f/"
    A_MAIN = MOD_ART_PATH + "a/"
    S_MAIN = MOD_ART_PATH + "s/"

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
    ZOOM = "zoom=1.25"

    # Prefixes for files
    PREFIX_BODY = "torso" + ART_DLM
    PREFIX_ARMS = "arms" + ART_DLM
    PREFIX_BODY_LEAN = "torso-leaning" + ART_DLM
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

    # suffixes
    NIGHT_SUFFIX = ART_DLM + "n"
    FILE_EXT = ".png"

    ### [BLK001]
    # non leanable clothes
    lean_clothes_blacklist = [
        "test"
    ]

    ### [BLK002]
    # non leanable hair
    lean_hair_blacklist = [
#        "down",  # Thanks to Trilasent for giving us leaning hair downs
        "bun"
    ]

    ### [BLK003]
    # non leanable accessories
    lean_acs_blacklist = [
#        "mug"
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

    # tryparses for the hair and clothes
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
    # NOTE: do NOT include regular poses in here
    L_POSES = [
        "def"
    ]

    def acs_lean_mode(lean):
        """
        Returns the appropriate accessory prefix dpenedong on lean

        IN:
            lean - type of lean

        RETURNS:
            appropratie accessory prefix
        """
        if lean:
            return "".join([PREFIX_ACS_LEAN, lean, ART_DLM])

        return PREFIX_ACS


    def face_lean_mode(lean):
        """
        Returns the appropriate face prefix depending on lean

        IN:
            lean - type of lean

        RETURNS:
            appropriate face prefix
        """
        if lean:
            return "".join([PREFIX_FACE_LEAN, lean, ART_DLM])

        return PREFIX_FACE


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


    def night_mode(isnight):
        """
        Returns the appropriate night string
        """
        if isnight:
            return NIGHT_SUFFIX

        return ""


    def should_disable_lean(lean, character):
        """
        Figures out if we need to disable the lean or not based on current
        character settings

        IN:
            lean - lean type we want to do
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

        if character.hair in lean_hair_blacklist:
            # blacklisted hair
            return True

        if character.clothes in lean_clothes_blacklist:
            # blacklisted clothes
            return True

        # otherwise, this is good
        return False


    # sprite maker functions


    def _ms_accessory(acs, isnight, issitting, pose=None, lean=None):
        """
        Creates accessory string

        IN:
            acs - MASAccessory object
            isnight - True will generate night string, false will not
            issitting - True will use sitting pic, false will not
            pose - current pose
                (Default: None)
            lean - type of lean
                (Default: None)

        RETURNS:
            accessory string
        """
        if acs.no_lean:
            # the lean version is the same as regular
            lean = None

        # pose map check
        # Since None means we dont show, we are going to assume that the
        # accessory should be shown if the pose key is missing.
        if lean:
            poseid = acs.pose_map.l_map.get(lean, None)

            if acs.pose_map.use_reg_for_l:
                # clear lean if dont want to use it for rendering
                lean = None

        else:
            poseid = acs.pose_map.map.get(pose, None)

        if poseid is None:
            # a None here means we should shouldnt' even show this acs
            # for this pose. Weird, but maybe it happens?
            return ""

        if issitting:
            acs_str = acs.img_sit

        elif acs.img_stand:
            acs_str = acs.img_stand

        else:
            # standing string is null or None
            return ""

        return "".join([
            LOC_Z,
            ',"',
            A_T_MAIN,
            acs_lean_mode(lean),
            acs_str,
            ART_DLM,
            poseid,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_accessorylist(acs_list, isnight, issitting, pose=None, lean=None):
        """
        Creates accessory strings for a list of accessories

        IN:
            acs_list - list of MASAccessory object, in order of rendering
            isnight - True will generate night string, false will not
            issitting - True will use sitting pic, false will not
            pose - arms pose for we are currently rendering
                (Default: None)
            lean - type of lean
                (Default: None)

        RETURNS:
            accessory string list
        """
        if len(acs_list) == 0:
            return ""

        acs_gen = [
            _ms_accessory(acs, isnight, issitting, pose, lean=lean)
            for acs in acs_list
        ]

        return "," + ",".join([
            _acs
            for _acs in acs_gen
            if len(_acs) > 0
        ])


    def _ms_arms(clothing, arms, isnight):
        """
        Creates arms string

        IN:
            clothing - type of clothing
            arms - type of arms
            isnight - True will generate night string, false will not

        RETURNS:
            arms string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_ARMS,
            arms,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_blush(blush, isnight, lean=None):
        """
        Creates blush string

        IN:
            blush - type of blush
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            blush string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_BLUSH,
            blush,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_body(clothing, hair, isnight, lean=None, arms=""):
        """
        Creates body string

        IN:
            clothing - type of clothing
            hair - type of hair
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)
            arms - type of arms
                (Default: "")

        RETURNS:
            body string
        """
        if lean:
            # leaning is a single parter
            body_str = ",".join([
                LOC_LEAN,
                _ms_torsoleaning(clothing, hair, lean, isnight)
            ])

        else:
            # not leaning is a 2parter
            body_str = ",".join([
                LOC_REG,
                _ms_torso(clothing, hair, isnight),
                _ms_arms(clothing, arms, isnight)
            ])

        # add the rest of the parts
        return "".join([
            I_COMP,
            "(",
            body_str,
            ")"
        ])


    def _ms_emote(emote, isnight, lean=None):
        """
        Creates emote string

        IN:
            emote - type of emote
            isnight - True will generate night string, false will not
            lean - type of lean
                (Dfeualt: None)

        RETURNS:
            emote string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EMOTE,
            emote,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyebags(eyebags, isnight, lean=None):
        """
        Creates eyebags string

        IN:
            eyebags - type of eyebags
            isnight - True will generate night string, false will not
            lean - type of lean
                (Dfeault: None)

        RETURNS:
            eyebags string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYEG,
            eyebags,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyebrows(eyebrows, isnight, lean=None):
        """
        Creates eyebrow string

        IN:
            eyebrows - type of eyebrows
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            eyebrows string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYEB,
            eyebrows,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyes(eyes, isnight, lean=None):
        """
        Creates eyes string

        IN:
            eyes - type of eyes
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            eyes stirng
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYES,
            eyes,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_face(
            eyebrows,
            eyes,
            nose,
            mouth,
            isnight,
            lean=None,
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Create face string
        (the order these are drawn are in order of argument)

        IN:
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will generate a night string, false will not
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

        RETURNS:
            face string
        """
        subparts = list()

        # lean checking
        if lean:
            subparts.append(LOC_LEAN)

        else:
            subparts.append(LOC_REG)

        # now for the required parts
        subparts.append(_ms_eyes(eyes, isnight, lean=lean))
        subparts.append(_ms_eyebrows(eyebrows, isnight, lean=lean))
        subparts.append(_ms_nose(nose, isnight, lean=lean))
        subparts.append(_ms_mouth(mouth, isnight, lean=lean))

        # and optional parts
        if eyebags:
            subparts.append(_ms_eyebags(eyebags, isnight, lean=lean))

        if sweat:
            subparts.append(_ms_sweat(sweat, isnight, lean=lean))

        if blush:
            subparts.append(_ms_blush(blush, isnight, lean=lean))

        if tears:
            subparts.append(_ms_tears(tears, isnight, lean=lean))

        if emote:
            subparts.append(_ms_emote(emote, isnight, lean=lean))

        # alright, now build the face string
        return "".join([
            I_COMP,
            "(",
            ",".join(subparts),
            ")"
        ])


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
            LOC_Z,
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
            LOC_Z,
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


    def _ms_mouth(mouth, isnight, lean=None):
        """
        Creates mouth string

        IN:
            mouth - type of mouse
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            mouth string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_MOUTH,
            mouth,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_nose(nose, isnight, lean=None):
        """
        Creates nose string

        IN:
            nose - type of nose
            isnight - True will genreate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            nose string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_NOSE,
            nose,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


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
            LOC_Z,
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
            eyebrows,
            eyes,
            nose,
            mouth,
            isnight,
            acs_pre_list,
            acs_mid_list,
            acs_pst_list,
            lean=None,
            arms="",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Creates sitting string

        IN:
            clothing - type of clothing
            hair - type of hair
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will genreate night string, false will not
            acs_pre_list - sorted list of MASAccessories to draw prior to body
            acs_mid_list - sorted list of MASAccessories to draw between body
                and face
            acs_pst_list - sorted list of MASAccessories to draw after face
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

        RETURNS:
            sitting stirng
        """
        if lean:
            loc_str = LOC_LEAN

        else:
            loc_str = LOC_REG

        return "".join([
            TRAN,
            "(",
            L_COMP,
            "(",
            loc_str,
            _ms_accessorylist(acs_pre_list, isnight, True, arms, lean=lean),
            ",",
            LOC_Z,
            ",",
            _ms_body(clothing, hair, isnight, lean=lean, arms=arms),
            _ms_accessorylist(acs_mid_list, isnight, True, arms, lean=lean),
            ",",
            LOC_Z,
            ",",
            _ms_face(
                eyebrows,
                eyes,
                nose,
                mouth,
                isnight,
                lean=lean,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            ),
            _ms_accessorylist(acs_pst_list, isnight, True, arms, lean=lean),
            "),",
            ZOOM,
            ")"
        ])


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
        if single:
            return "".join([
                I_COMP,
                "(",
                LOC_STAND,
                ",",
                LOC_Z,
                ',"',
                STOCK_ART_PATH,
                single,
                FILE_EXT,
                '"',
                _ms_accessorylist(acs_list, False, False),
                ")"
            ])

        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            LOC_Z,
            ',"',
            STOCK_ART_PATH,
            left,
            FILE_EXT,
            '",',
            LOC_Z,
            ',"',
            STOCK_ART_PATH,
            right,
            FILE_EXT,
            '",',
            LOC_Z,
            ',"',
            STOCK_ART_PATH,
            head,
            FILE_EXT,
            '"',
            _ms_accessorylist(acs_list, False, False),
            ")"
        ])


    def _ms_sweat(sweat, isnight, lean=None):
        """
        Creates sweatdrop string

        IN:
            sweat -  type of sweatdrop
            isnight - True will generate night string, false will not
            lean - type of lean
                (Defualt: None)

        RETURNS:
            sweatdrop string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_SWEAT,
            sweat,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_tears(tears, isnight, lean=None):
        """
        Creates tear string

        IN:
            tears - type of tears
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            tear strring
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_TEARS,
            tears,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_torso(clothing, hair, isnight):
        """
        Creates torso string

        IN:
            clothing - type of clothing
            hair - type of hair
            isnight - True will generate night string, false will not

        RETURNS:
            torso string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_BODY,
            hair,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_torsoleaning(clothing, hair, lean, isnight):
        """
        Creates leaning torso string

        IN:
            clothing - type of clothing
            hair - type of ahri
            lean - type of leaning
            isnight - True will genreate night string, false will not

        RETURNS:
            leaning torso string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_BODY_LEAN,
            hair,
            ART_DLM,
            lean,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


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
        PRE_ACS = 0 # PRE ACCESSORY
        MID_ACS = 1 # MID ACCESSORY
        PST_ACS = 2 # post accessory

        def __init__(self, pre_acs=[], mid_acs=[], pst_acs=[]):
            """
            IN:
                pre_acs - list of pre accessories to load with
                mid_acs - list of mid accessories to load with
                pst_acs - list of pst accessories to load with
            """
            self.name="Monika"
            self.haircut="default"
            self.haircolor="default"
            self.skin_hue=0 # monika probably doesn't have different skin color
            self.lipstick="default" # i guess no lipstick
            self.clothes = "def" # default clothes is school outfit
            self.hair = "def" # default hair is the usual whtie ribbon

            # list of lean blacklisted accessory names currently equipped
            self.lean_acs_blacklist = []

            # accesories to be rendereed before the body
            self.acs_pre = []

            # accessories to be rendreed between body and face expressions
            self.acs_mid = []

            # accessories to be rendered last
            self.acs_post = []

            self.hair_hue=0 # hair color?

            # setup acs dict
            self.acs = {
                self.PRE_ACS: self.acs_pre,
                self.MID_ACS: self.acs_mid,
                self.PST_ACS: self.acs_post
            }


        def __get_acs(self, acs_type):
            """
            Returns the accessory list associated with the given type

            IN:
                acs_type - the accessory type to get

            RETURNS:
                accessory list, or None if the given acs_type is not valid
            """
            return self.acs.get(acs_type, None)


        def change_clothes(self, new_cloth):
            """
            Changes clothes to the given cloth

            IN:
                new_cloth - new clothes to wear
            """
            self.clothes = new_cloth


        def change_hair(self, new_hair):
            """
            Changes hair to the given hair

            IN:
                new_hair - new hair to wear
            """
            self.hair = new_hair


        def change_outfit(self, new_cloth, new_hair):
            """
            Changes both clothes and hair

            IN:
                new_cloth - new clothes to wear
                new_hair - new hair to wear
            """
            self.change_clothes(new_cloth)
            self.change_hair(new_hair)


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
            return (
                self.is_wearing_acs_in(accessory, self.PST_ACS)
                or self.is_wearing_acs_in(accessory, self.MID_ACS)
                or self.is_wearing_acs_in(accessory, self.PRE_ACS)
            )


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


        def reset_all(self):
            """
            Resets all of monika
            """
            self.reset_clothes()
            self.reset_hair()
            self.remove_all_acs()


        def remove_acs(self, accessory):
            """
            Removes the given accessory from all the accessory lists

            IN:
                accessory - accessory to remove
            """
            self.remove_acs_in(accessory, self.PRE_ACS)
            self.remove_acs_in(accessory, self.MID_ACS)
            self.remove_acs_in(accessory, self.PST_ACS)


        def remove_acs_in(self, accessory, acs_type):
            """
            Removes the given accessory from the given accessory list type

            IN:
                accessory - accessory to remove
                acs_type - ACS type
            """
            acs_list = self.__get_acs(acs_type)

            if acs_list is not None and accessory in acs_list:
                acs_list.remove(accessory)

            if accessory.name in self.lean_acs_blacklist:
                self.lean_acs_blacklist.remove(accessory.name)


        def remove_all_acs(self):
            """
            Removes all accessories from all accessory lists
            """
            self.remove_all_acs_in(self.PRE_ACS)
            self.remove_all_acs_in(self.MID_ACS)
            self.remove_all_acs_in(self.PST_ACS)


        def remove_all_acs_in(self, acs_type):
            """
            Removes all accessories from the given accessory type

            IN:
                acs_type - ACS type to remove all
            """
            if acs_type in self.acs:
                # need to clear blacklisted
                for acs in self.acs[acs_type]:
                    if acs.name in self.lean_acs_blacklist:
                        self.lean_acs_blacklist.remove(acs.name)

                self.acs[acs_type] = list()


        def reset_clothes(self):
            """
            Resets clothing to default
            """
            self.clothes = "def"


        def reset_hair(self):
            """
            Resets hair to default
            """
            self.hair = "def"


        def reset_outfit(self):
            """
            Resetse clothing and hair to default
            """
            self.reset_clothes()
            self.reset_hair()


        def wear_acs_in(self, accessory, acs_type):
            """
            Wears the given accessory

            IN:
                accessory - accessory to wear
                acs_type - accessory type (location) to wear this accessory
            """
            acs_list = self.__get_acs(acs_type)

            if acs_list is not None and accessory not in acs_list:
                mas_insertSort(acs_list, accessory, MASAccessory.get_priority)

                if accessory.name in mas_sprites.lean_acs_blacklist:
                    self.lean_acs_blacklist.append(accessory.name)


        def wear_acs_pre(self, acs):
            """
            Wears the given accessory in the pre body accessory mode

            IN:
                acs - accessory to wear
            """
            self.wear_acs_in(acs, self.PRE_ACS)


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

        def __init__(self,
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
                    - LEAN: def
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


    # instead of clothes, these are accessories
    class MASAccessory(renpy.store.object):
        """
        MASAccesory objects

        PROPERTIES:
            name - name of the accessory
            img_sit - filename of the sitting version of the accessory
            img_stand - filename of the standing version of the accessory
            priority - render priority of the accessory. Lower is rendred
                first
        """


        def __init__(self,
                name,
                img_sit,
                pose_map,
                img_stand="",
                rec_layer=MASMonika.PST_ACS,
                priority=10,
                no_lean=False,
                stay_on_start=False
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
                no_lean - True means the leaning versions are the same as the
                    regular versions (which means we don't need lean variants)
                    False means otherwise
                    NOTE: This means that the non-lean version works for ALL
                    LEANING VERSIONS. If at least one lean version doesn't
                    work, then you need separate versions, sorry.
                    (Default: False)
                stay_on_start - True means the accessory is saved for next
                    startup. False means the accessory is dropped on next
                    startup.
                    (Default: False)
            """
            self.name = name
            self.img_sit = img_sit
            self.img_stand = img_stand
            self.__rec_layer = rec_layer
            self.priority=priority
            self.no_lean = no_lean
            self.stay_on_start = stay_on_start
            self.pose_map = pose_map

            if type(pose_map) != MASPoseMap:
                raise Exception("PoseMap is REQUIRED")

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

            # required standing parts
            head,
            left,
            right,

            # optional sitting parts
            lean=None,
            arms="steepling",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None,

            # optional standing parts
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
        acs_mid_list = character.acs.get(MASMonika.MID_ACS, [])
        acs_pst_list = character.acs.get(MASMonika.PST_ACS, [])

        # are we sitting or not
        if is_sitting:

            if store.mas_sprites.should_disable_lean(lean, character):
                # set lean to None if its on the blacklist
                lean = None

            cmd = store.mas_sprites._ms_sitting(
                character.clothes,
                character.hair,
                eyebrows,
                eyes,
                nose,
                mouth,
                not morning_flag,
                acs_pre_list,
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
        # TODO change this to an elif and else the custom stnading mode
#        elif stock:
            # stock standing mode
            cmd = store.mas_sprites._ms_standingstock(
                head,
                left,
                right,
                acs_all_list,
                single=single
            )

#        else:
            # custom standing mode

        return eval(cmd),None # Unless you're using animations, you can set refresh rate to None

# Monika
define monika_chr = MASMonika()

init -1 python:
    # ACCESSORIES (IMG020)
    # Accessories are reprsentation of image objects with properties
    # Pleaes refer to MASAccesory to understand all the properties
    #
    # NAMING SCHEME:
    # mas_acs_<accessory name>
    #
    # <accessory name> MUST BE UNIQUE
    #
    # File naming:
    # Accessories should be named like:
    #   acs-<acs identifier/name>-<pose id>-<night suffix>
    #
    # Leaning:
    #   acs-leaning-<leantype>-<acs identifier/name>-<pose id>-<night suffix>
    #
    # acs name - name of the accessory (shoud be unique)
    # pose id - identifier to map this image to a pose (should be unique
    #       per accessory)
    # leantype - leaning type, if appropriate
    #
    # NOTE: pleaes preface each accessory with the following commen template
    # this is to ensure we hvae an accurate description of what each accessory
    # is:
    ### HUMAN UNDERSTANDABLE NAME OF ACCESSORY
    ## accessoryidentifiername
    # General description of what the object is, where it is located

    ### COFFEE MUG
    ## mug
    # Coffee mug that sits on Monika's desk
    mas_acs_mug = MASAccessory(
        "mug",
        "mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True
    )
    store.mas_sprites.init_acs(mas_acs_mug)

    ### PROMISE RING
    ## promisering
    # Promise ring that can be given to Monika
    mas_acs_promisering = MASAccessory(
        "promisering",
        "promisering",
        MASPoseMap(
            p1=None,
            p2="4",
            p3="1",
            p4=None,
            p5="5",
            p6=None
        ),
        stay_on_start=True
    )
    store.mas_sprites.init_acs(mas_acs_promisering)
    ### QUETZAL PLUSHIE
    ## qplushie
    # Quetzal plushie that sits on Monika's desk
    mas_acs_quetzalplushie = MASAccessory(
        "quetzalplushie",
        "quetzalplushie",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie)

#### ACCCESSORY VARIABLES (IMG025)
# variables that accessories may need for enabling / disabling / whatever
# please comment the groups and usage like so:
### accessory name
# <var>
# <var comment>

### COFFEE MUG

default persistent._mas_acs_enable_coffee = False
# True enables coffee, False disables coffee

default persistent._mas_coffee_been_given = False
# True means user has given monika coffee before, False means no

default persistent._mas_coffee_brew_time = None
# datetime that coffee startd brewing. None if coffe not brewing

default persistent._mas_coffee_cup_done = None
# datetime that monika will finish her coffee. None means she isnt drinking any

default persistent._mas_coffee_cups_drank = 0
# number of cups of coffee monika has drank

define mas_coffee.BREW_LOW = 2*60
# lower bound of seconds it takes to brew some coffee

define mas_coffee.BREW_HIGH = 4*60
# upper bound of seconds it takes to brew some coffee

define mas_coffee.DRINK_LOW = 10 * 60
# lower bound of seconds it takes for monika to drink coffee

define mas_coffee.DRINK_HIGH = 2 * 3600
# upper bound of seconds it takes for monika to drink coffee

define mas_coffee.BREW_CHANCE = 80
# percent chance out of 100 that we are brewing coffee during the appropriate
# times

define mas_coffee.DRINK_CHANCE = 80
# percent chance out of 100 that we are drinking coffee during the appropriate
# times

define mas_coffee.COFFEE_TIME_START = 5
# hour that coffee time begins (inclusive)

define mas_coffee.COFFEE_TIME_END =  12
# hour that coffee time ends (exclusive)

define mas_coffee.BREW_DRINK_SPLIT = 9
# hour between the coffee times where brewing turns to drinking
# from COFFEE_TIME_START to this time, brew chance is used
# from this time to COFFEE_TIME_END, drink chance is used

### QUETZAL PLUSHIE ###
default persistent._mas_acs_enable_quetzalplushie = False
# True enables plushie, False disables plushie

### PROMISE RING ###
default persistent._mas_acs_enable_promisering = False
# True enables plushie, False disables plushie

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
# mod_assets/monika/a/<accessories> NOTE: UNTESTED, do not use
#
# All layers must have a night version, which is denoted using the -n suffix.
# All leaning layers must have a non-leaning fallback
#
## FACIAL EXPRESSIONS:
# Non leaning filenames:
#   face-{face part type}-{face part name}{-n}.png
#   (ie: face-mouth-big.png / face-mouth-big-n.png)
# leaning filenames:
#   face-leaning-{face part type}-{face part name}{-n}.png
#   (ie: face-leaning-eyes-sparkle.png / face-leaning-eyes-sparkle-n.png)
#
## BODY / POSE:
# Non leaning filenames / parts:
#   torso-{hair type}{-n}.png
#   arms-{arms name}{-n}.png
#   (ie: torso-def.png / torso-def-n.png)
#   (ie: arms-def-steepling.png / arms-def-steepling-n.png)
# Leaning filenames:
#   torso-leaning-{hair type}-{lean name}{-n}.png
#   (ie: torso-leaning-def-def.png / torso-leaning-def-def-n.png)
#
#
#
#

image monika 1esa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 2esa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 3esa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 4esa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 1eua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1euc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eka = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ekc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1ekd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1esc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1esd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1huu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)


image monika 1hksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1eksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1eksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1dsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)


image monika 1dsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eft = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)


image monika 1efw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1efp = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1eftsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1eksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1wfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wuo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wubsw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1wubso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1subftsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full",
    tears="streaming"
)

image monika 1sublo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1suo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hka = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="l",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1kua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="winkleft",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1sua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1sfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1sub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1sutsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1tfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tkx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tku = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1tsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1rsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rssdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1lfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1lssdrc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1rksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1rksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lksdlw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1rksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1lssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1lsbssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right",
    blush="shade"
)

image monika 1lsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1lkbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1wkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="e",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1lftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1lktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1dfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dsbso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1dftdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1duu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1dubsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dubssdru = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade",
    sweat="right"
)

image monika 1hfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1hksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="right"
)

image monika 1hubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1hkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1dkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1skbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1skbla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1hkbla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1dkbla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines"
)

image monika 1tubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1subfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1hubfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1ekbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1dkbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1dkbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1ekbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1dktub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="up"
)

image monika 1dktua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="up"
)

image monika 1ektua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="up"
)

image monika 1ektsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1wuw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wka = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1wub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1lkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="shade"
)

image monika 1lkbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 1lkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="r",
    left="1l",
    right="1r",
    arms="steepling",
    blush="lines",
    tears="pooled"
)

image monika 1wubfsdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full",
    sweat="def"
)

image monika 1rusdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1ektda = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1ektdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1ektdd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="dried"
)

image monika 1wkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1wktsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1dktpc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="pooled"
)

image monika 1dktsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 1ektpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="pooled"
)

image monika 1ektsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="f",
    left="1l",
    right="1r",
    arms="steepling",
    tears="streaming"
)

image monika 2eua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2euc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eka = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ekc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ekd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2esc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2esd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2hksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2dsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eft = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)


image monika 2efw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2efo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2eftsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2eksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2wfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wuo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wubsw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2wubso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2subftsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full",
    tears="streaming"
)

image monika 2sub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2sutsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2tfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tku = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)
image monika 2dkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)


image monika 2tsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2rsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2rfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2lfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lssdrc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2rksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2eksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lksdlw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2rksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2lssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2lsbssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right",
    blush="shade"
)

image monika 2lsbssdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def",
    blush="shade"
)

image monika 2lsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2lkbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2lftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2lktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2dfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dsbso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2dftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2dftdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed",
    tears="dried"
)

image monika 2duu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2dubsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2dubssdru = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade",
    sweat="right"
)

image monika 2hfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2hksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="right"
)

image monika 2hubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2tubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2subfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2hubfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2ekbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2dkbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2ekbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2ekp = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="pout",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2tfp = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2lfp = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="pout",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2ektsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="1l",
    right="2r",
    arms="crossed",
    tears="streaming"
)

image monika 2wuw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2wubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2lkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    blush="shade"
)

image monika 2lkbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 2wubfsdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full",
    sweat="def"
)

image monika 2wkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2rkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 3eua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3euc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eka = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3ekc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3ekd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3esc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3esd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3wkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)


image monika 3lksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3dsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eft = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)


image monika 3efw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3efo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3eftsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3eksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3wfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wuo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wubsw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3wubso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3subftsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full",
    tears="streaming"
)

image monika 3sub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3sutsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3tfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tkx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tku = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)
image monika 3dkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)


image monika 3tsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3tsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3rkbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3rsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rssdrc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3rssdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rssdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3rktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3lfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="pooled"
)

image monika 3dkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="pooled"
)

image monika 3lkbltpa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="lines",
    tears="pooled"
)

image monika 3lfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3lssdrc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3rksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lksdlw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3rksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3lssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3lsbssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right",
    blush="shade"
)

image monika 3lsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lkbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3lktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3dfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dsbso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3dftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3dftdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="dried"
)

image monika 3duu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3dubsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3dubssdru = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade",
    sweat="right"
)

image monika 3hfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3hksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="right"
)

image monika 3hubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3tubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3tsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3subfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)


image monika 3hubfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3ekbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3dkbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3ekb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3ekbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3ektda = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="dried"
)

image monika 3ektsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright",
    tears="streaming"
)

image monika 3wuw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3wubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3lkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="shade"
)

image monika 3lkbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 3wubfsdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full",
    sweat="def"
)

image monika 3wkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 4eua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4euc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eka = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4ekc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4ekd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4esc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4esd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)


image monika 4hksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4dsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dsd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eft = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="triangle",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4efo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="gasp",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4eftsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4eksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4wfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4wfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="smile",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wuo = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wubsw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4wubso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="gasp",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4subftsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full",
    tears="streaming"
)

image monika 4sub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4sutsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4tfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tkx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="disgust",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tku = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="2r",
    arms="pointright"
)
image monika 4dkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="2r",
    arms="pointright"
)
image monika 4tkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright"
)


image monika 4tsb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4tsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4rkbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4rsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4rssdrc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4rfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4rktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4lfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="disgust",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smug",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="big",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="wide",
    head="i",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lud = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4lssdrc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4rksdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rksdlb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lksdlw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="wide",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4rksdla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="def"
)

image monika 4lssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4lsbssdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right",
    blush="shade"
)

image monika 4lsbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4lkbsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4lftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4lktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4dfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="big",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dsbso = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="gasp",
    head="r",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4dftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4dftdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright",
    tears="dried"
)

image monika 4duu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4dubsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4dubssdru = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade",
    sweat="right"
)

image monika 4hfx = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="disgust",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smug",
    head="j",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedhappy",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4hksdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="2r",
    arms="pointright",
    sweat="right"
)

image monika 4hubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4tubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="smug",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4subfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)


image monika 4hubfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4ekbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4dkbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4ekbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4ektsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="r",
    left="2l",
    right="2r",
    arms="pointright",
    tears="streaming"
)

image monika 4wuw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="r",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 4wubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4lkbsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="shade"
)

image monika 4lkbfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

image monika 4wubfsdld = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="small",
    head="o",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full",
    sweat="def"
)

image monika 4wkd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="wide",
    nose="def",
    mouth="small",
    head="b",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 5eua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    single="3a"
)

image monika 5euc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5esu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    lean="def",
    single="3a"
)

image monika 5tsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    lean="def",
    single="3a"
)

image monika 5hubfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5hubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5hub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5hua = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5efa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5esbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5ekbfa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    blush="full",
    single="3b"
)

image monika 5eubla = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    blush="lines",
    single="3b"
)

image monika 5wubfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5wuw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5eubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5rubfsdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    sweat="right",
    lean="def",
    single="3b"
)

image monika 5rubfsdru = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    sweat="right",
    lean="def",
    single="3b"
)

image monika 5rubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5rubfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5rusdrb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    sweat="right",
    lean="def",
    single="3b"
)

image monika 5rusdru = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    sweat="right",
    lean="def",
    single="3b"
)


image monika 5rub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5ruu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="right",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5eubfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5eub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5rsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5rkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5rfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5lfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5lkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5lsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 5lubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5lubfu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    blush="full",
    lean="def",
    single="3b"
)

image monika 5luu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="smug",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

# bored
image monika 5tsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="smirk",
    head="",
    left="",
    right="",
    lean="def",
    single="3b"
)

image monika 6dubsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6dubsu = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="closedsad",
    nose="def",
    mouth="smug",
    head="j",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 6ektsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6ektdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6ektsa = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6ektda = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6lktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6rktsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6rksdlc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    sweat="def"
)

image monika 6dsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dstsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6lktdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6dstdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6dfc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dfd = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6dftdc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="dried"
)

image monika 6lftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6dftsc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="down",
    tears="streaming"
)

image monika 6tst = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="mid",
    eyes="smug",
    nose="def",
    mouth="triangle",
    head="q",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6wfw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="furrowed",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="i",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6rkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="right",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6lkc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6sub = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="sparkle",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6ckc = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="knit",
    eyes="crazy",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="1r",
    arms="down"
)

image monika 6wubsw = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="wide",
    nose="def",
    mouth="wide",
    head="b",
    left="1l",
    right="1r",
    arms="down",
    blush="shade"
)

image monika 1lubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="1r",
    arms="steepling",
    blush="full"
)

image monika 2lubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="1l",
    right="2r",
    arms="crossed",
    blush="full"
)

image monika 3lubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright",
    blush="full"
)

image monika 4lubfb = DynamicDisplayable(
    mas_drawmonika,
    character=monika_chr,
    eyebrows="up",
    eyes="left",
    nose="def",
    mouth="big",
    head="a",
    left="2l",
    right="2r",
    arms="pointright",
    blush="full"
)

### [IMG032]
# Image aliases

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
