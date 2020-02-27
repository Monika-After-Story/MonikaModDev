# sprite generation using matrix for night sprites


# this should be after sprite-chart's initialization
init -4 python in mas_sprites:
    import store

    # filter enums
    FLT_DAY = "day"
    FLT_NIGHT = "night"

    # filter dict
    filters = {
        FLT_DAY: store.im.matrix.identity(),
        FLT_NIGHT: store.im.matrix.tint(0.59, 0.49, 0.55),
    }

    # several caches for images

    cache_face = {}
    # the facial expression cache. Facial expressions are the most likely
    # things to overlap across clothing, hair, and ACS, so we should cache them
    # together to maximize performance
    # key:
    #   tuple containing all sprite strings that may be used. None is fine
    #   here. 
    #   [0] - should be the filter code. 
    #   [1] - should be pre/post (0 or 1)
    #   [2] should be lean
    #   [3+] remaining values dependent on type:
    #       * pre - only blush
    #       * post - all values except blush
    # value:
    #   image maniuplator object

    cache_body = {}
    # the body cache. This includes clothes and base sprites.
    # key:
    #   tuple containing strings. 
    #   [0] - should be the filter code.
    #   [1] - shoud be image path
    # value:
    #   image maniuplator object

    cache_hair = {}
    # the hair cache
    # key:
    #   tuple containing strings. 
    #   [0] - should be the filter code.
    #   [1] - should be image path
    # value:
    #   image manipulator object
    
    cache_acs = {}
    # the ACS cache
    # key:
    #   tuple containing strings. 
    #   [0] - should be the filter code.
    #   [1] - second should be image path.
    # value:
    #   image manipulator object

    cache_tc = {}
    # the tablechair cache
    # key:
    #   tuple containing strings
    #   [0] - should be the filter code
    #   [1] - should be either table/chair (0, 1)
    #   [2] - table/chair type
    #   [3] - 0 for no shadow, 1 for shadow (ignored for chairs)
    # value:
    #   image manipulator object


    def _get_imc(im_cache, img_key, flt, img_str):
        """
        Gets an image manipulator from the given cache, generates if not
        found.

        IN:
            im_cache - image manipulator cache to use
            img_key - key to use
            flt - filter to use if generate
            img_str - image string or manipulator to use if gneerate

        RETURNS: image manipulator to use
        """
        if img_key in im_cache:
            return im_cache[img_key]

        new_im = _gen_im(flt, img_str)
        im_cache[img_key] = new_im
        return new_im


    def _gen_im(flt, img_str):
        """
        Generates an image maniuplator
        NOTE: always assumes we have an available filter.

        IN:
            flt - filter to use
            img_str - image path or manipulator to use
        """
        return store.im.MatrixColor(img_str, FILTER_DICT[flt])


    # im-based sprite maker functions
    def _im_accessory(
            im_list,
            acs,
            flt,
            is_sitting,
            arm_state,
            leanpose=None,
            lean=None
    ):
        """
        Adds accessory image manipulator

        IN:
            acs - MASAccessory object
            flt - filter to apply
            is_sitting - True will use sitting pic, False will not
            arm_state - "0" for arms-base-0, "1" for arms-base-1, None for
                neither
            leanpose - current pose
                (Default: None)
            lean - type of lean
                (Default: None)

        OUT:
            im_list - list to add image manipulators to
        """
        # pose map check
        # Since None means we dont show, we are going to assume that the
        # accessory should not be shown if the pose key is missing.
        poseid = acs.pose_map.get(leanpose, None)
        arm_codes = acs.get_arm_split_code(leanpose)

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

        if arm_state is not None:
            
            if arm_state in arm_codes:
                arm_code = ART_DLM + arm_state
            else:
                # we should not render
                return

        else:
            arm_code = ""

        img_str = "".join((
            A_T_MAIN,
            PREFIX_ACS,
#        ))
#        acs_lean_mode(sprite_list, lean)
#        sprite_list.extend((
            acs_str,
            ART_DLM,
            poseid,
            arm_code,
            FILE_EXT,
        ))

        im_list.append(_get_imc(cache_acs, (flt, img_str), flt, img_str))


    def _im_accessory_list(
            im_list,
            acs_list,
            flt,
            is_sitting,
            leanpose=None,
            arm_state=None,
            lean=None
    ):
        """
        Adds accessory image manipulators for a list of accessories

        IN:
            acs_list - list of MASAccessory objects, in order of rendering
            flt - filter to use
            is_sitting - True will use sitting pic, false will not
            arm_state - set to "0" or "1" if we are rendering acs between
                base arms and arm ouftits
            leanpose - arms pose for we are currently rendering
                (Default: None)
            lean - type of lean
                (Default: None)

        OUT:
            im_list - list to add image manipulators to
        """
        if len(acs_list) == 0:
            return

        for acs in acs_list:
            _im_accessory(
                im_list,
                acs,
                flt,
                is_sitting,
                arm_state,
                leanpose,
                lean=lean
            )


    def _im_base_body_nh(im_list, flt, bcode):
        """
        Adds base body image manipulators, no hair
        (equiv of _ms_torso_nh_base)

        IN:
            flt - filter ot use
            bcode- base code to use

        OUT:
            im_list - list to add image manipulators to 
        """
        img_str = "".join((
            B_MAIN,
            BASE_BODY_STR,
            bcode,
            FILE_EXT,
        ))

        im_list.append(_get_imc(cache_body, (flt, img_str), flt, img_str))
    

    def _im_base_body_lean_nh(im_list, lean, flt, bcode):
        """
        Adds base body lean image manipulators, no hair
        (equivalent of _ms_torsoleaning_nh_base)

        IN:
            lean - type of lean
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        img_str = "".join((
            B_MAIN,
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            bcode,
            FILE_EXT,
        ))

        im_list.append(_get_imc(cache_body, (flt, img_str), flt, img_str))


    def _im_body_nh(im_list, clothing, flt, bcode):
        """
        Adds body image manipulators, no hair
        (equiv of _ms_torso_nh)

        IN:
            clothing - type of clothing
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        img_str = "".join((
            C_MAIN,
            clothing,
            "/",
            NEW_BODY_STR,
            ART_DLM,
            bcode,
            FILE_EXT,
        ))

        im_list.append(_get_imc(cache_body, (flt, img_str), flt, img_str))


    def _im_body_lean_nh(im_list, clothing, lean, flt, bcode):
        """
        Adds body leaning image manipulators, no hair
        (equiv of _ms_torsoleaning_nh)

        IN:
            clothing - type of clothing
            lean - type of lean
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        img_str = "".join((
            C_MAIN,
            clothing,
            "/",
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            bcode,
            FILE_EXT,
        ))

        im_list.append(_get_imc(cache_body, (flt, img_str), flt, img_str))


    def _im_body_nh_wbase(
            im_list,
            clothing,
            acs_bse_list,
            bcode,
            flt,
            leanpose,
            lean=None
    ):
        """
        Adds body image manipulators, including base and bse acs, no hair

        IN:
            clothing - type of clothing
            acs_bse_list - acs between base-0 and body-0
            bcode - base code to use
            flt - filter to use
            leanpose - leanpose to pass to accessorylist
            lean - type of lean

        OUT:
            im_list - list to add image manipulators to
        """
        if lean:
            # base-0
            _im_base_body_lean_nh(im_list, lean, flt, bcode)

            # acs_bse
            _im_accessory_list(
                im_list,
                acs_bse_list,
                True,
                leanpose,
                arm_state=bcode,
                lean=lean
            )

            # body-0
            _im_body_lean_nh(im_list, clothing, lean, flt, bcode)

        else:
            # base-0
            _im_base_body_nh(im_list, flt, bcode)

            # acs_bse
            _im_accessory_list(
                im_list,
                acs_bse_list,
                True,
                leanpose,
                arm_state=bcode,
                lean=lean
            )

            # body-0
            _im_body_nh(im_list, clothing, flt, bcode)


    def _im_chair(im_list, chair, flt):
        """
        Adds chair manipulator

        IN:
            chair - type of chair
            flt - filter to use

        OUT:
            im_list - list to add image manipulators to
        """
        img_str = "".join((
            T_MAIN,
            PREFIX_CHAIR,
            chair,
            FILE_EXT,
        ))

        im_list.append(_get_imc(cache_tc, (flt, 1, chair), flt, img_str))

   
    def _im_hair(im_list, hair, flt, hair_sfx, lean):
        """
        Adds hair manipulator

        IN:
            hair - type of hair
            flt - filter to use
            hair_sfx - hair suffix to use (front/back)
            lean - tyoe of lean

        OUT:
            im_list - list to add image manipulators to
        """
        if lean:
            img_str = "".join((
                H_MAIN,
                PREFIX_HAIR_LEAN,
                lean,
                ART_DLM,
                hair,
                hair_sfx,
                FILE_EXT,
            ))

        else:
            img_str = "".join((
                H_MAIN,
                PREFIX_HAIR,
                hair,
                hair_sfx,
                FILE_EXT,
            ))

        im_list.append(_get_imc(cache_hair, (flt, img_str), flt, img_str))


    def _im_table(im_list, table, show_shadow, flt):
        """
        Adds table manipulator

        IN:
            table - type of table
            show_shadow - True if shadow should be included, false if not
            flt filter to use

        OUT:
            im_list - list to add image manipulators to
        """
        img_key = (flt, 0, table, int(show_shadow))
        if img_key in cache_tc:
            im_list.append(cache_tc[img_key])
            return

        # otherwise, we need to create the table sprite, maybe with shadow
        table_str = "".join((
            T_MAIN,
            PREFIX_TABLE,
            table,
            FILE_EXT,
        ))

        # in this case, we may need to use im.Composite
        if show_shadow:
            # need to make shadow
            shdw_str = "".join((
                T_MAIN,
                PREFIX_TABLE,
                table,
                SHADOW_SUFFIX,
                FILE_EXT,
            ))

            new_im = _gen_im(flt, store.im.Composite(
                (1280, 850),
                (0, 0), table_str,
                (0, 0), shdw_str
            ))

        else:
            # no shadow, so just gen table
            new_im = _gen_im(flt, table_str)

        # add to cache and list
        cache_tc[img_key] = new_im
        im_list.append(new_im)
        
