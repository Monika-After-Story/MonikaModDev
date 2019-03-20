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
# CLOTHES (hair_map):
#   Values should be strings. because hair might be mapped to user-custom
#   hairs, full hair validation will happen after all objects are validated
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
    from store.mas_ev_data_ver import _verify_bool, _verify_str, \
        _verify_int, _verify_list

    log = mas_utils.getMASLog("log/spj")
    log_open = log.open()
    log.raw_write = True

    sprite_station = store.MASDockingStation(
        renpy.config.basedir + "/game/mod_assets/monika/jsons/"
    )
    # docking station for custom sprites. 

    # verification lists
    hm_key_delayed_veri = []
    # keys that are missing will give warnings

    hm_val_delayed_veri = []
    # vals tha tar emissing will give errors


    def writelog(msg):
        # new lines always added ourselves
        if log_open:
            log.write(msg)


    def writelogs(msgs):
        # writes multiple msges given list
        if log_open:
            for msg in msgs:
                log.write(msg)


    ### LOG CONSTANTS
    ## Global
    READING_FILE = "reading JSON at '{0}'..."
    SP_LOADING = "loading {0} sprite object '{1}'..."

    BAD_TYPE = "property '{0}' - expected type {1}, got {2}"
    EXTRA_PROP = "extra property '{0}' found"
    REQ_MISS = "required property '{0}' not found"
    BAD_SPR_TYPE = "invalid sprite type '{0}'"
    BAD_ACS_LAYER = "invalid ACS layer '{0}'"
    BAD_LIST_TYPE = "property '{0}' index '{0}' - expected type {1}, got {2}"

    ## MASPoseMap
    MPM_LOADING = "loading MASPoseMap in '{0}'..."
    MPM_SUCCESS = "MASPoseMap '{0}' loaded successfully!"
    MPM_BAD_POSE = "property '{0}' - invalid pose '{1}'"
    MPM_FB_DEF = "in fallback mode but default not set"
    MPM_FB_DEF_L = "in fallback mode but leaning default not set"

    ## Hair Map
    HM_LOADING = "loading hair_map..."
    HM_SUCCESS = "hair_map loaded successfully!"
    HM_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    HM_BAD_V_TYPE = "value for key '{0}' - expected type {1}, got {2}"
    HM_MISS_ALL = "hair_map does not have key 'all' set."

    ## ex_props
    EP_LOADING = "loading ex_props..."
    EP_SUCCESS = "ex_props loaded successfully!"
    EP_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    EP_BAD_V_TYPE = "value for key '{0}' - expected type int/str/bool, got {1}"



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

    ## param names
    ## with expected types and verifications, as well as msg to
    ##  show when verification fails.
    ##      (if None, we use the default bad type)
    REQ_SHARED_PARAM_NAMES = {
        # type must be checked first, so its not included in this loop.
#        "type": _verify_sptype,
        "name": (str, _verify_str),
        "img_sit": (str, _verify_str),
        # pose map verificaiton is different
#        "pose_map": None,
    }

    OPT_SHARED_PARAM_NAMES = {
        "img_stand": (str, _verify_str),
        "stay_on_start": (bool, _verify_bool),

        # object-based verificatrion is different
#        "ex_props": None,
#        "select_info": None,

        "giftname": (str, _verify_str),
    }

    OPT_ACS_PARAM_NAMES = {
        # this is handled differently
#        "rec_layer": None, 
#        "mux_type": (None, _verify_muxtype, 

        "priority": (int, _verify_int),
        "acs_type": (str, _verify_str),
    }

    OPT_HC_SHARED_PARAM_NAMES = {
        "fallback": (bool, _verify_bool),
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

    ## special param name groups
    OBJ_BASED_PARAM_NAMES = (
        "pose_map",
        "ex_props",
        "select_info",
        "split",
        "hair_map",
    )

    # NOTE: renpy.loadable("path from game/")
    IMG_BASED_PARAM_NAMES = (
        "img_sit",
        "img_stand"
    )


init 790 python in mas_sprites_json:
    from store.mas_sprites import _verify_pose, HAIR_MAP
    from store.mas_piano_keys import MSG_INFO, MSG_WARN, MSG_ERR, \
        JSON_LOAD_FAILED, FILE_LOAD_FAILED, \
        MSG_INFO_ID, MSG_WARN_ID, MSG_ERR_ID, \
        LOAD_TRY, LOAD_SUCC, LOAD_FAILED, \
        NAME_BAD

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


    def _validate_mux_type(json_obj, errs):
        """
        Validates mux_type of this json object

        IN:
            json_obj - json object to validate
        
        OUT:
            errs - list to save error messages to
                if nothing was addeed to this list, the mux_type is valid

        RETURNS: mux_type found. May be None
        """
        if "mux_type" not in json_obj:
            return None

        # otherwise it exists
        mux_type = json_obj.pop("mux_type")

        if not _verify_list(mux_type):
            # not list is bad
            errs.append(MSG_ERR_ID.format(BAD_TYPE.format(
                "mux_type",
                list,
                type(mux_type)
            )))
            return None

        # otherwise, verify each element of this list
        for index in range(len(mux_type)):
            acs_type = mux_type[index]
            if not _verify_str(acs_type):
                errs.append(MSG_ERR_ID.format(BAD_LIST_TYPE.format(
                    "mux_type",
                    index,
                    str,
                    type(acs_type)
                )))
                # NOTE: we log these but still return the muxtype.
                #   it is up to the caller to check for messages
                #   to determine if the item is valid

        return mux_type


    def _validate_params(
            jobj, 
            save_obj, 
            param_dict,
            required,
            errs,
            err_base
        ):
        """
        Validates a list of parameters, while also saving said params into
        given save object.

        Errors/Warnings are logged to given lists

        IN:
            jobj - json object to parse
            param_dict - dict of params + verification functiosn
            required - True if the given params are required, False otherwise.
            err_base - base format string to use for errors

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
        """
        # if required, we do not accept Nones
        allow_none = not required

        for param_name, verifier_info in param_dict.iteritems():
            if param_name in jobj:
                param_val = jobj.pop(param_name)
                desired_type, verifier = verifier_info
        
                if not verifier(param_val, allow_none):
                    # failed verification
                    errs.append(err_base.format(BAD_TYPE.format(
                        param_name,
                        desired_type,
                        type(param_val)
                    )))

                else:
                    # otherwise, good, transfer the property over
                    # and continue
                    save_obj[param_name] = param_val

            elif required:
                # this was a required param, add error
                errs.append(err_base.format(REQ_MISS.format(param_name)))


    def _validate_acs(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates ACS-specific properties, as well as acs pose map

        Props validated:
            - rec_layer
            - priority
            - acs_type
            - mux_type
            - pose_map

        IN:
            jobj - json object to pasrse
            obj_based - dict of object-based items
                (contains pose_map)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
                NOTE: does NOT write errs
            warns - list to save warning messages to
                NOTE: MAY WRITE WARNS
            infos - list to save info messages to
        """
        # validate ez to validate props
        # priority
        # acs_type
        _validate_params(jobj, save_obj, False, errs, MSG_ERR_ID)
        if len(errs) > 0:
            return

        # now for rec_layer
        if "rec_layer" in jobj:
            rec_layer = jobj.pop("rec_layer")

            if not store.MASMonika._verify_rec_layer(rec_layer):
                errs.append(MSG_ERR_ID.format(BAD_ACS_LAYER.format(rec_layer)))
                return

            # otherwise valid
            save_obj["rec_layer"] = rec_layer

        # now for mux_type
        mux_type = _validate_mux_type(jobj, errs)
        if len(errs) > 0:
            return

        # otherwise valid
        save_obj["mux_type"] = mux_type

        # now for pose map
        writelog(MSG_INFO_ID.format(MPM_LOADING.format("pose_map")))

        # pose map must exist for us to reach this point.
        pose_map = store.MASPoseMap.fromJSON(
            obj_based.pop("pose_map"),
            False,
            errs,
            warns
        )
        if pose_map is None or len(errs) > 0:
            writelogs(warns)
            return

        # Valid pose map!
        # write out warns
        writelogs(warns)

        # and succ
        writelog(MSG_INFO_ID.format(MPM_SUCCESS.format("pose_map")))
        save_obj["pose_map"] = pose_map


    def _validate_fallbacks(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates fallback related properties and pose map

        Props validated:
            - fallback
            - pose_map

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains pose_map)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        # validate fallback
        _validate_params(jobj, save_obj, False, errs, MSG_ERR_ID)
        if len(errs) > 0:
            return

        # valid fallback? determine it
        fallback = save_obj.get("fallback", False)

        # now parse pose map
        writelog(MSG_INFO_ID.format(MPM_LOADING.format("pose_map")))
        pose_map = store.MASPoseMap.fromJSON(
            obj_based.pop("pose_map"),
            fallback,
            errs,
            warns
        )
        if pose_map is None or len(errs) > 0:
            writelogs(warns)
            return

        # valid pose map!
        # write out warns
        writelogs(warns)

        # and successful
        writelog(MSG_INFO_ID.format(MPM_SUCCESS.format("pose_map")))
        save_obj["pose_map"] = pose_map


    def _validate_hair(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates HAIR related properties
        
        Props validated:
            - split

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains split)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list ot save warning messages to
            infos - list to save info messages to
        """
        # validate split
        if "split" not in obj_based:
            # no split found, not a problem
            return

        # split exists, lets get and validate
        writelog(MSG_INFO_ID.format(MPM_LOADING.format("split")))
        split = store.MASPoseMap.fromJSON(
            obj_based.pop("split"),
            False,
            errs,
            warns
        )
        if split is None or len(errs) > 0:
            writelogs(warns)
            return

        # valid pose map!
        # write out wrans
        writelogs(warns)

        # and success
        writelog(MSG_INFO_ID.format(MPM_SUCCESS.format("split")))
        save_obj["split"] = split


    def _validate_clothes(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates CLOTHES related properties

        Props validated:
            - hair_map

        IN:
            jobj - json object to parse
            obj_based - dict of objected-baesd items
                (contains split)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        # validate hair_map
        if "hair_map" not in obj_based:
            # no hair map found, not a problem
            return

        # hair map exists, get and validate
        writelog(MSG_INFO_ID.format(HM_LOADING))
        hair_map = obj_based.pop("hair_map")

        for hair_key,hair_value in hair_map.iteritems():
            # start with type validations

            # key
            if _verify_str(hair_key):
                if hair_key != "all" and not in HAIR_MAP:
                    hm_key_delayed_veri.append(hair_key)
            else:
                errs.append(MSG_ERR_IDD.format(HM_BAD_K_TYPE.format(
                    hair_key,
                    str,
                    type(hair_key)
                )))

            # value
            if _verify_str(hair_value):
                if hair_value not in HAIR_MAP:
                    hm_val_delayed_veri.append(hair_value)

            else:
                errs.append(MSG_ERR_IDD.format(HM_BAD_V_TYPE.format(
                    hair_key,
                    str,
                    type(hair_value)
                )))

        # recommend "all"
        if "all" not in hair_map:
            writelog(MSG_WARN_IDD.format(HM_MISS_ALL))

        # check for no errors
        if len(errs) > 0:
            return

        # hair map loaded! verification will happen later.
        writelog(MSG_INFO_ID.format(HM_SUCCESS))
        save_obj["hair_map"] = hair_map


    def _validate_ex_props(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates ex_props proprety

        Props validated:
            - ex_props

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains ex_props)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        # validate ex_props
        if "ex_props" not in obj_based:
            return

        # ex_props exists, get and validate
        writelog(MSG_INFO_ID.format(EP_LOADING))
        ex_props = obj_based.pop("ex_props")

        for ep_key,ep_val in ex_props.iteritems():
            if not _verify_str(ep_key):
                errs.append(MSG_ERR_IDD.format(EP_BAD_K_TYPE.format(
                    ep_key,
                    str,
                    type(ep_key)
                )))

            if not (
                    _verify_str(ep_val)
                    or _verify_bool(ep_val)
                    or _verify_int(ep_val)
                ):
                errs.append(MSG_ERR_IDD.format(EP_BAD_V_TYPE.format(
                    ep_key,
                    type(ep_val)
                )))

        # check for no errors
        if len(errs) > 0:
            return

        # otherwise, we can say successful loading!
        writelog(MSG_INFO_ID.format(EP_SUCCESS))
        save_obj["ex_props"] = ex_props


    def _validate_selectable(jobj, save_obj, obj_based, errs, warns, infos):
        """
        Validates selectable 

        Props validated:
            - select_info

        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains select_info)

        OUT:
            save_obj - dict to save data to
            errs - list to save error messages to
            warns - list to save warning messages to
            infos - list to save info messages to
        """
        # validate select_info
        if "select_info" not in obj_based:
            return

        # select_info exists, get and validate
        select_info = obj_based.pop("select_info")
        # TODO


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
        msgs_info = []
        msgs_exprop = []
        obj_based_params = {}
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
        _validate_params(jobj, sp_obj_params, True, msgs_err, MSG_ERR_ID)
        if len(msgs_errs) > 0:
            writelogs(msgs_errs)
            return

        # log out that we are loading the sprite object and name
        writelog(MSG_INFO.format(LOADING_SP.format(
            SP_STR.get(sp_type),
            sp_obj_params.get("name")
        )))

        # check for existence of pose_map property. We will not validate until
        # later.
        if "pose_map" not in jobj:
            writelog(MSG_ERR_ID.format(REQ_MISS.format("pose_map")))
            return

        # move object-based params out of the jobj
        for param_name in OBJ_BASED_PARAM_NAMES:
            if param_name in jobj:
                obj_based_params[param_name] = jobj.pop(param_name)

        # validate optional shared params
        _validate_params(jobj, sp_obj_params, False, msgs_err, MSG_ERR_ID)
        if len(msgs_errs) > 0:
            writelogs(msgs_errs)
            return

        # now for specific params
        if sp_type == SP_ACS:
            # ACS
            _validate_acs(
                jobj,
                sp_obj_params,
                obj_based_params,
                msgs_err,
                msgs_warn,
                msgs_info
            )
            if len(msgs_err) > 0:
                writelogs(msgs_err)
                return

            # clear lists
            msgs_warn = []

        else:
            # hair / clothes
            _validate_fallbacks(
                jobj,
                sp_obj_params,
                obj_based_params,
                msgs_err,
                msgs_warn,
                msgs_info
            )
            if len(msgs_err) > 0:
                writelogs(msgs_warn)
                writelogs(msgs_err)
                return

            # clear lists
            msgs_warn = []

            if sp_type == SP_HAIR:
                _validate_hair(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    msgs_err,
                    msgs_warn,
                    msgs_info
                )
                if len(msgs_err) > 0:
                    writelogs(msgs_warn)
                    writelogs(msgs_err)
                    return

            else:
                # must be clothes
                _validate_clothes(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    msgs_err,
                    msgs_warn,
                    msgs_info
                )
                if len(msgs_err) > 0:
                    writelogs(msgs_warn)
                    writelogs(msgs_err)
                    return

            # clear lists
            msgs_warn = []

        # back to shared acs/hair/clothes stuff
        _validate_ex_props(
            jobj,
            sp_obj_params,
            obj_based_params,
            msgs_err,
            msgs_warn,
            msgs_info
        )
        if len(msgs_err) > 0:
            writelogs(msgs_warn)
            writelogs(msgs_err)
            return

        # clear lists
        msgs_warn = []
            

        # TODO:
        #   verifying:
        #       select_info
        #   saving:
        #       giftname
        #   processing
        #       progpoints
            






init 800 python in mas_sprites_json:
    pass


