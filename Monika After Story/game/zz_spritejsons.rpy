# Module for turning json formats into sprite objects
# NOTE: This DEPENDS on sprite-chart.rpy
#
# NOTE: all JSON formats do NOT have prog points. This is a security thing.
#   prog points will be assumed using the type of sprite object and name.
#
# Shared JSON props:
# {
#   "type": integer type of sprite object this is,
#       - REQUIRED
#       - integer
#       - see the json store below for constants
#   "name": "id"
#       - REQUIRED
#       - id for this sprite object. Must be unqiue for the type of object.
#       - This is also referred to in prog points.
#   "img_sit": "base filename for sitting image",
#       - REQUIRED
#       - do not include extension
#   "pose_map": {Pose Map object},
#       - REQUIRED
#       - this is used differently based on object. For more info, see the
#           PoseMap JSON below.
#   "img_stand": "base filename for standing image",
#       - optional
#       - do not include extension
#       - NOTE: generally, this can be left out. We are unlikely to include
#           standing monika anytime soon.
#       - if not given, we assume no standing image
#   "stay_on_start": True if this sprite object should be saved for startup
#       - optional
#       - boolean
#       - default False
#   "ex_props": {arbitrary properties}
#       - optional
#       - additional properties to apply to this sprite object. used for
#            a variety of things. This will be more publicly documented
#           in the future.
#       - NOTE: arbitrary properties can only exist 1 level. (aka no 
#           collections as values of these props)
#       - keys should be strings.
#       - acceptable values are int/string/bool.
#       - default empty dict
#   "select_info": {Selectable object}
#       - optional
#       - providing this will enable the object to be selected in some
#            activities
#       - see Selectable JSON below for more info
#   "giftname": "filename of the gift that unlocks this item",
#       - optional
#       - NOTE: if not provided, and this item is not unlocked or used 
#           under other means, this item will NOT be selectable or usable.
#       - do not include extension
#       - default None
# }
#
#
# Additional props for ACS:
# {
#   "rec_layer": recommended layer constant,
#       - optional
#       - integer
#       - See MASMonika class for the constants
#       - if not given, we assume PST (post)
#   "priority": render priority
#       - optional
#       - integer.
#       - lower is rendered first
#       - default 10
#   "acs_type": "type of this acs"
#       - optional
#       - this is not necessary, but used in conjunction with mux_type to 
#           remove potential conflicting acs types
#       - an ACS cannot have multiple types, but it can have multiple
#           conflicting types
#       - default None
#   "mux_type": [list of acs types this conflicts with]
#       - optional
#       - used in confjunction with acs_type
#       - must be list of strings
#       - default None
# }
#
# Shared props for HAIR and CLOTHES:
#
# {
#   "fallback": True if the posemap object should be treated as containing
#       fallback codes instead of just enable/disable rules.
#       - optional
#       - boolean
#       - see PoseMap JSONs below for more info
#       - default False
#
# HAIR only props:
#
# {
#   "split": {Pose Map object}
#       - optional
#       - see PoseMap JSONs below for more info
# }
#
# CLOTHES only props:
#
# {
#   "hair_map": {hair string id mappings}
#       - optional
#       - This maps hair string IDs to other hair string IDs. When rendering
#           this clothing item, if the current hair is in this map, the
#           value is used instead.
#       - Use "all" as a key to signify a default for everything to map to.
#       - Use "custom" as a value to map to the generic non-split hair style.
#           This is useful for clothing items with baked hairstyles.
#       - Both keys and values should be strings and should match to an 
#           existing hair ID. 
#       - default empty dict
# }
#
# PoseMap JSONSs
# NOTE: this is used differently based on the sprite object type.
# NOTE: the type is of most props also varies based onusage.
#
# In general:
#
# {
#   "default": value to use as default for all non-leaning poses
#       - optional
#       - default None
#   "l_default": value to use as default for all leaning poses
#       - optional
#       - default None
#   "use_reg_for_l": True will set the l_default value to default.
#       - optional
#       - boolean
#       - basically, this will set the default value for all leaning
#           poses to use the same as non-leaning poses.
#       - default False
#   "p1": value to use for pose 1
#       - optional
#       - This is the "steepling" pose
#       - default None
#   "p2": value to use for pose 2
#       - optional
#       - This is the "crossed" pose
#       - default None
#   "p3": value to use for pose 3
#       - optional
#       - This is the "restleftpointright" pose
#       - default None
#   "p4": value to use for pose 4
#       - optional
#       - This is the "pointright" pose
#       - default None
#   "p5": value to use for pose 5
#       - optional
#       - This is the "leaning-def-def" pose
#       - default None
#   "p6": value to use for pose 6
#       - optional
#       - This is the "down" pose
#       - default None
# }
#       
# ACS (pose_map):
#   Values should be acs ID code (string). This code is part of the filename 
#   for an ACS. This allows you to use a specific ACS image for certain poses.
#
# HAIR (pose_map):
#   If fallback is True, then value should pose names (string). This is used
#       to determine what pose use instead of the desired pose.
#   If fallback is False (default), then value should be (boolean). This is
#       used to determine if a pose should be enabled or disabled for this
#       hair. True values will mean enabled, False means disabled.
#       By default, poses with False values will use steepling instead.
#
# HAIR (split):
#   Values should be booleans. True means the hair is split for this pose. 
#   False means the hair is not split.
#   If this PoseMAp is not given, the hair is assumed to be split for all 
#   poses.
#   This is usually used when a hair is split for upright poses but not
#   leaning poses.
#
# CLOTHES (pose_map):
#   This functions the same as pose_map for HAIR.
#
# Selectables JSON:
#
# {
#   "display_name": "Name that should be shown in a selector menu for this
#       item",
#       - REQUIRED
#   "thumb": "Thumnail code of image",
#       - REQUIRED
#       - do not include extension
#   "group": "id of group this should be selectable with",
#       - REQUIRED
#       - this is like the type of acs/clothing/hair this item should be
#           selectable with
#   "visible_when_locked": True if this item should be visible in selectors
#       even when locked, False if not,
#       - optional
#       - boolean
#       - locked items will show the locked item thumbnail
#       - default True
#   "hover_dlg": [List of text to show when mouse is hovered over this in 
#       selector],
#       - optional
#       - list of strings
#       - lines are picked randomly when hovered
#       - default None
#   "select_dlg": [List of text to show when this item is selected in the
#       selector],
#       - optional
#       - list of strings
#       - lines are picked randomly when selected
#       - default None
# }

# TODO :add dev label to check if prog points are executable

init -21 python in mas_sprites_json:
    import json
    import store
    import store.mas_utils as mas_utils

    # these imports are for the classes
    from store.mas_ev_data_ver import _verify_bool, _verify_str, _verify_int

    log = mas_utils.getMASLog("log/spj")
    log_open = log.open()
    log.raw_write = True

    sprite_station = store.MASDockingStation(
        renpy.config.basedir + "/game/mod_assets/monika/jsons/"
    )
    # docking station for custom sprites. 


    def writelog(msg):
        # new lines always added ourselves
        if log_open:
            log.write(msg)


    ### CONSTANTS
    SP_ACS = 0
    SP_HAIR = 1
    SP_CLOTHES = 2

    SP_CONSTS = (
        SP_ACS,
        SP_HAIR,
        SP_CLOTHES,
    )

    SP_STR = {
        SP_ACS: "ACS",
        SP_HAIR: "HAIR",
        SP_CLOTHES: "CLOTHES",
    }

    def _verify_sptype(val, allow_none=True):
        if val is None:
            return allow_none
        return val in SP_CONSTS


    def _verify_muxtype(val, allow_none=True);
        if val is None:
            return allow_none
        if not isinstance(val, list):
            return False
        for item in val:
            if not _verify_str(item):
                return False

        return True


    ## param names
    ## with verifications
    REQ_SHARED_PARAM_NAMES = {
        # type must be checked first, so its not included in this loop.
#        "type": _verify_sptype,
        "name": _verify_str,
        "img_sit": _verify_str,
        # pose map verificaiton is different
#        "pose_map": None,
    }

    OPT_SHARED_PARAM_NAMES = {
        "img_stand": _verify_str,
        "stay_on_start": _verify_bool,

        # object-based verificatrion is different
#        "ex_props": None,
#        "select_info": None,
        "giftname": _verify_str
    }

    OPT_ACS_PARAM_NAMES = {
        "rec_layer": None, # this is filled out later
        "priority": _verify_int,
        "acs_type": _verify_str,
        "mux_type": _verify_muxtype,
    }

    OPT_HC_SHARED_PARAM_NAMES = {
        "fallback": _verify_bool,
    }

    OPT_HAIR_PARAM_NAMES = {
        # object-based verification is different
#        "split": None,     
    }
    OPT_HAIR_PARAM_NAMES.update(OPT_HC_SHARED_PARAM_NAMES)

    OPT_CLOTH_PARAM_NAMES = {
        # object-based verificaiton is different
#        "hair_map": None,
    }
    OPT_CLOTH_PARAM_NAMES.update(OPT_HC_SHARED_PARAM_NAMES)

    OBJ_BASED_PARAM_NAMES = (
        # this is handled on its own
#        "pose_map",
        "ex_props",
        "select_info",
        "split",
        "hair_map",
    )

    ### LOG CONSTANTS
    ## Global
    READING_FILE = "reading JSON at '{0}'..."
    PARSE_SP = "loading {0} sprite object '{1}'"

    BAD_TYPE = "property '{0}' - expected type {1}, got {2}"
    EXTRA_PROP = "extra property '{0}' found"
    REQ_MISS = "required property '{0}' not found"
    BAD_SPR_TYPE = "invalid sprite type '{0}'"

    ## MASPoseMap
    MPM_BAD_POSE = "property '{0}' - invalid pose '{1}'"
    MPM_FB_DEF = "in fallback mode but default not set"
    MPM_FB_DEF_L = "in fallback mode but leaning default not set"





init 790 python in mas_sprites_json:
    from store.mas_sprites import _verify_pose
    from store.mas_piano_keys import MSG_INFO, MSG_WARN, MSG_ERR, \
        JSON_LOAD_FAILED, FILE_LOAD_FAILED, \
        MSG_INFO_ID, MSG_WARN_ID, MSG_ERR_ID, \
        LOAD_TRY, LOAD_SUCC, LOAD_FAILED, \
        NAME_BAD

    # fill in param name verifications
    OPT_ACS_PARAM_NAMES["rec_layer"] = store.MASMonika._verify_rec_layer

    # other constants
    MSG_INFO_IDD = "        [info]: {0}\n"
    MSG_WARN_IDD = "        [Warning!]: {0}\n"
    MSG_ERR_IDD = "        [!ERROR!]: {0}\n"


    def _validate_type(json_obj):
        """
        Validates the type of this json object.

        Logs errors. Also pops type off

        IN:
            json_obj - json object to validate

        RETURNS: SP constant if valid type, None otherwise
        """
        # check for type existence
        if "type" not in json_obj:
            writelog(MSG_ERR_ID.format(REQ_MISS.format("type")))
            return None

        # type exists, validate
        type_val = json_obj.pop("type")
        if not _verify_sptype(type_val, False):
            writelog(MSG_ERR_ID.format(BAD_SPR_TYPE.format(type(type_val))))
            return None

        # type validated, return it
        return type_val


    def _validate_params(jobj, save_obj, param_dict, required, errs, warns):
        """
        Validates a list of parameters, while also saving said params into
        given save object.

        Errors/Warnings are logged to given lists

        IN:
            jobj - json object to parse
            param_dict - dict of params + verification functiosn
            required - True if the given params are required, False otherwise.

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
        """
        # TODO
        pass


    def addSpriteObject(filepath):
        """
        Adds a sprite object, given its json filepath

        NOTE: most exceptions logged
        NOTE: may raise exceptions

        IN:
            filepath - filepath to the JSON we want to load
        """
        jobj = None
        msgs_err = []
        msgs_warn = []
#        msgs_info = []
        msgs_exprop = []
        sp_obj_params = {}
        sel_params = {}

        writelog(MSG_INFO.format(READING_FILE.format(filepath)))

        # can we read file
        with open(filepath, "r") as jsonfile:
            jobj = json.load(jsonfile)

        # is file json
        if jobj is None:
            writelog(MSG_ERR.format(JSON_LOAD_FAILED.format(filepath)))
            return

        ## this happens in 3 steps:
        # 1. build sprite object according to the json
        #   - this includes PoseMaps
        # 2. build selectable (if provided)
        # 3. Init everything
        #
        # Everything should be wrapped in try/excepts. All exceptions should
        #   be logged, but we include the warning in the function comment
        #   in case.

        # determine type
        sp_type = _validate_type(jobj)
        if sp_type is None:
            return

        # check name and img_sit
        for prop_name

        # NOTE: renpy.loadable("path from game/")

        # log out that we are loading the sprite object and name



init 800 python in mas_sprites_json:
    pass


