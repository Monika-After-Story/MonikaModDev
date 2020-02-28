# sprite generation using matrix for night sprites


init -99 python in mas_sprites:
    # NOTE: this must be after -100 and -101

    import store

    # do a file check for disabling im mode
    disable_im = store.is_file_present("no_matrix")


# this should be after sprite-chart's initialization
init -4 python in mas_sprites:

    # filter enums
    FLT_DAY = "day"
    FLT_NIGHT = "night"

    # filter dict
    FILTERS = {
        FLT_DAY: store.im.matrix.identity(),
        FLT_NIGHT: store.im.matrix.tint(0.59, 0.49, 0.55),
    }

    def _decide_filter():
        """
        Returns the appropriate filter to use

        NOTE: this is currently not how we want to do this going forward.
        Once we decide on lighting progression, then have this function call
        that code.

        RETURNS: desired filter
        """
        if store.morning_flag:
            return FLT_DAY

        return FLT_NIGHT

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
    #   [2] - type of lean
    #   [3+] remaining values dependent on type:
    #       * pre - only blush
    #       * post - all values except blush
    # value:
    #   image maniuplator object or None if no facial expression for this
    #   combo.

    cache_arms = {}
    # the arms cache. This includes clothes and base sprites.
    # key:
    #   tuple containing strings.
    #   [0] - filter code
    #   [1] - base code
    #   [2] - clothing type, "base" for base arms
    #   [3] - leanpose
    # value:
    #   image manipulator object OR None if no arms needed for this combo

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


    def _a2c(im_cache, img_key, im_obj):
        """
        Adds an image manipulator to the given cache

        IN:
            img_key - image key to use
            im_obj - image manipulator to save

        OUT:
            im_cache - cache to svae image manipultor to
        """
        # NOTE: no render
        #im_cache[img_key] = im_obj

        # NOTE: with render
        im_cache[img_key] = im_obj.load()


    def _add_mpa_imc(
            im_list, 
            mpa,
            pfx_list,
            flt,
            bcode,
            clothing,
            leanpose
    ):
        """
        Adds an image manipulator for MASPoseArms, if needed.

        IN:
            mpa - MASPoseArms to get image manipulator for
            pfx_list - prefix list to generate image string with
            sfx_list - suffix list to generate image string with
            flt - filter code to use
            bcode - base code to use
            clothing - clothing to use
            leanpose - leanpose to use

        OUT:
            im_list - list to add image manipulator to if needed
        """
        img_key = (flt, bcode, clothing, leanpose)
        day_key = None
        if img_key in cache_arms:
            if cache_arms[img_key] is not None:
                im_list.append(cache_arms[img_key])

            return

        elif flt != "day":
            # try checking for day version
            day_key = _dayify(img_key)
            if day_key in cache_arms:
                if cache_arms[day_key] is None:
                    # no image for this key, let the main key know
                    cache_arms[img_key] = None

                else:
                    # otherwise generate from day image
                    im_list.append(_gar_imc(
                        cache_arms,
                        img_key,
                        flt,
                        cache_arms[day_key]
                    ))

                return

        # sfx list is always the same
        sfx_list = (ART_DLM, bcode, FILE_EXT)

        # TODO: change this when we change to 3 layred arms
        use_front = bcode == "1"

        # NOTE: we are trying to limit branching as much as possible
        # so this code will likely have repeats

        # otherwise need to generate the new arms (maybe)
        if mpa.both is not None:
            # need to generate for the both case

            # but check based on bcode
            if use_front:
                if mpa.both_front:
                    im_list.append(_gdgar_imc(
                        cache_arms,
                        img_key,
                        flt,
                        "".join(pfx_list + (mpa.both,) + sfx_list),
                        day_key
                    ))
                    return

            elif mpa.both_back:
                im_list.append(_gdgar_imc(
                    cache_arms,
                    img_key,
                    flt,
                    "".join(pfx_list + (mpa.both,) + sfx_list),
                    day_key
                ))
                return

            # otherwise, we dont need to use any image here.
            cache_arms[img_key] = None
            cache_arms[day_key] = None
            return

        # we might need to generate for left and right
        lstr = None
        rstr = None
        if mpa.left is not None:
            if use_front:
                if mpa.left_front:
                    lstr = "".join(pfx_list + (mpa.left,) + sfx_list)

            elif mpa.left_back:
                lstr = "".join(pfx_list + (mpa.left,) + sfx_list)

        if mpa.right is not None:
            if use_front:
                if mpa.right_front:
                    rstr = "".join(pfx_list + (mpa.right,) + sfx_list)

            elif mpa.right_back:
                rstr = "".join(pfx_list + (mpa.right,) + sfx_list)

        # now generate im compsite if needed
        if lstr:
            if rstr:
                # need composite
                im_list.append(_gdgar_imc(
                    cache_arms,
                    img_key,
                    flt,
                    store.im.Composite((1280, 850),
                        (0, 0), lstr,
                        (0, 0), rstr
                    ),
                    day_key
                ))

            else:
                # just left arm
                im_list.append(_gdgar_imc(
                    cache_arms,
                    img_key,
                    flt,
                    lstr,
                    day_key
                ))

        elif rstr:
            # just right arm
            im_list.append(_gdgar_imc(cache_arms, img_key, flt, rstr, day_key))

        else:
            # no arms at all
            cache_arms[img_key] = None
            cache_arms[day_key] = None


    def _cgetg_imc(im_cache, img_key, flt, img_str):
        """
        Checks the given cache for the image manipulator,
        GETs the image manipulator if found, 
        Generates if not found.

        IN:
            im_cache - image manipulator cache to use
            img_key - key to use
            flt - filter to use if generate
            img_str - image string or manipulator to use if gneerate

        OUT:
            im_cache - may have the new image manipulator added to it

        RETURNS: image manipulator to use
        """
        if img_key in im_cache:
            return im_cache[img_key]

        if flt != "day":
            return _gdar_imc(im_cache, img_key, flt, img_str)

        return _gar_imc(im_cache, img_key, flt, img_str)


    def _dayify(img_key):
        """
        Dayifies the given image key.
        DAying simply replaces the filter portion of the key with "day"

        IN:
            img_key - image key to dayify

        RETURNS: dayified key
        """
        img_key_list = list(img_key)
        img_key_list[0] = "day"
        return tuple(img_key_list)


    def _gar_imc(im_cache, img_key, flt, img_str):
        """
        Generates an image manipulator
        Adds it to the cache
        Returns the image manip

        IN:
            img_key - key to use
            flt - filter to use
            img_str - image string ot manipulator to use

        OUT:
            im_cache - cache to add image manipulator to

        RETURNS: the new image manipulator
        """
        new_im = _gen_im(flt, img_str)
        im_cache[img_key] = new_im
        return new_im


    def _gdar_imc(im_cache, img_key, flt, img_str):
        """
        Generates an image manipulator, checking for a
        Day image first.
        Adds it to the cache
        Returns the image manip

        IN:
            img_key - key to use
            flt - filter to use
            img_str - image string ot manipulator to use

        OUT:
            im_cache - cache to add image manipulator to

        RETURNS: the new image manipulator
        """
        # try checking for day cache before generating
        day_img_key = _dayify(img_key)
        if day_img_key in im_cache:
            # if we have day, we can apply filter to it
            new_im = im_cache[day_img_key]

        else:
            # otherwise, we should make sure a day image is set
            new_im = _gar_imc(im_cache, day_img_key, "day", img_str)

        # then generate with the day image
        return _gar_imc(im_cache, img_key, flt, new_im)


    def _gdgar_imc(im_cache, img_key, flt, img_str, day_key):
        """
        Generates a 
        Day image manipulator, then 
        Generates the desired image manipulator,
        Adds both to their respective caches
        Returns the image manipulator

        IN:
            img_key - key to use
            flt - filter to use
            img_str - image string ot manipulator to use
            day_key - day key to use
                pass in None to just do regular gar

        OUT:
            im_cache - cache to add image manipulator to

        RETURNS: the new image manipulator
        """
        if day_key is None:
            return _gar_imc(im_cache, img_key, flt, img_str)

        # otherwise genreate day first, then the desired one
        day_im = _gar_imc(im_cache, day_key, "day", img_str)
        return _gar_imc(im_cache, img_key, flt, day_im)
    

    def _gen_im(flt, img_str):
        """
        GENerates an image maniuplator
        NOTE: always assumes we have an available filter.

        IN:
            flt - filter to use
            img_str - image path or manipulator to use

        RETURNS: generated image manipulator
        """
        # NOTE: no render
        return store.im.MatrixColor(img_str, FILTERS[flt])


    def _gen_im_disp(im_list):
        """
        Generates a LiveComposite (which is just a Fixed) displayable given a 
        list of image manipulators. This uses the positions defined by
        zoom. (adjustx, adjusty)

        IN:
            im_list - list of image manipulators we generated

        RETURNS: displayable to use
        """
        # TODO: we could even cache this. See mas_drawmonika_im

        # fiirst setup the Fixed disp
        props = {}
        props.setdefault("style", "image_placement")
        disp = renpy.display.layout.Fixed(
            xmaximum=LOC_W,
            ymaximum=LOC_H,
            xminimum=LOC_W,
            yminimum=LOC_H,
            **props
        )

        # now add the image manips
        for img_man in im_list:
            disp.add(renpy.display.layout.Position(
                img_man,
                xpos=adjust_x,
                xanchor=0,
                ypos=adjust_y,
                yanchor=0
            ))

        return disp


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

        if is_sitting:
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

        im_list.append(_cgetg_imc(cache_acs, (flt, img_str), flt, img_str))


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


    def _im_arms_base_nh(im_list, bpose, leanpose, flt, bcode):
        """
        Adds arms base image manipulator
        (equiv to _ms_arms_nh_up_base)

        IN:
            bpose - MASPoseArms to use
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        _add_mpa_imc(
            im_list,
            bpose,
            (
                B_MAIN,
                PREFIX_ARMS,
            ),
            flt,
            bcode,
            "base",
            leanpose
        )


    def _im_arms_base_lean_nh(im_list, bpose, lean, leanpose, flt, bcode):
        """
        Adds arms base lean image manipulator
        (eqiv to _ms_arms_nh_leaning_base)

        IN:
            bpose - MASPoseArms to use
            lean - type of lean
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        _add_mpa_imc(
            im_list,
            bpose,
            (
                B_MAIN,
                PREFIX_ARMS_LEAN,
                lean,
                ART_DLM,
            ),
            flt,
            bcode,
            "base",
            leanpose
        )


    def _im_arms_nh(im_list, apose, clothing, leanpose, flt, bcode):
        """
        Adds arms image manipulator
        (equiv to _ms_arms_nh_up_arms)

        IN:
            apose - MASPoseARms to use
            clothing - type of clothing
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        _add_mpa_imc(
            im_list,
            apose,
            (
                C_MAIN,
                clothing,
                "/",
                PREFIX_ARMS,
            ),
            flt,
            bcode,
            clothing,
            leanpose
        )


    def _im_arms_lean_nh(im_list, apose, clothing, lean, leanpose, flt, bcode):
        """
        Adds arms lean image manipulator
        (equiv to _ms_arms_nh_leaning_arms)

        IN:
            apose - MASPoseArms to use
            clothing - type of clothing
            lean - type of lean
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        _add_mpa_imc(
            im_list,
            apose,
            (
                C_MAIN,
                clothing,
                "/",
                PREFIX_ARMS_LEAN,
                lean,
                ART_DLM,
            ),
            flt,
            bcode,
            clothing,
            leanpose
        )


    def _im_arms_nh_wbase(
            im_list,
            bpose,
            apose,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            bcode
    ):
        """
        Adds arms manipulators, no hair, with baes

        IN:
            bpose - MASPoseArms for base
            apose - MASPoseArms for outfit
            clothing - type of clothing
            acs_ase_list - acs between arms-base-0 and arms-0
            leanpose - leanpose to pass to accessorylist
            lean - lean to use
            flt - filter to use
            bcode - base code to use

        OUT:
            im_list - list to add image manipulators to
        """
        if lean:
            # arms-base-0
            _im_arms_base_lean_nh(im_list, bpose, lean, leanpose, flt, bcode)

            # acs-ase
            _im_accessory_list(
                im_list,
                acs_ase_list,
                flt,
                True,
                leanpose,
                arm_state=bcode,
                lean=lean
            )

            if apose is not None:
                # arms-0
                _im_arms_lean_nh(
                    im_list,
                    apose,
                    clothing,
                    lean,
                    leanpose,
                    flt,
                    bcode
                )

        else:
            # arms-base-0
            _im_arms_base_nh(im_list, bpose, leanpose, flt, bcode)

            # acs-ase
            _im_accessory_list(
                im_list,
                acs_ase_list,
                flt,
                True,
                leanpose,
                arm_state=bcode,
                lean=lean
            )

            if apose is not None:
                # arms-0
                _im_arms_nh(im_list, apose, clothing, leanpose, flt, bcode)


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

        im_list.append(_cgetg_imc(cache_body, (flt, img_str), flt, img_str))
    

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

        im_list.append(_cgetg_imc(cache_body, (flt, img_str), flt, img_str))


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

        im_list.append(_cgetg_imc(cache_body, (flt, img_str), flt, img_str))


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

        im_list.append(_cgetg_imc(cache_body, (flt, img_str), flt, img_str))


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

        im_list.append(_cgetg_imc(cache_tc, (flt, 1, chair), flt, img_str))


    def _im_face(
            im_list,
            eyes,
            eyebrows,
            nose,
            mouth,
            flt,
            fpfx,
            lean,
            sweat,
            tears,
            emote
        ):
        """
        Adds face image manipulators

        IN:
            eyes - type of eyes
            eyebrows - type of eyebrows
            nose - type of nose
            mouth - type of mouth
            flt - filter to use
            fpfx - face prefix to use
            lean - type of lean to use
            sweat - type of sweat drop
            tears - type of tears
            emote - type of emote

        OUT:
            im_list - list to add image manipulators to
        """
        img_key = (
            flt,
            1,
            lean,
            eyes,
            eyebrows,
            nose,
            mouth,
            sweat,
            tears,
            emote
        )
        day_key = None
        if img_key in cache_face:
            im_list.append(cache_face[img_key])
            return

        elif flt != "day":
            # try using day key
            day_key = _dayify(img_key)
            if day_key in cache_face:
                im_list.append(_gar_imc(
                    cache_face,
                    img_key,
                    flt,
                    cache_face[day_key]
                ))
                return

        # othewise need to generate

        # we will always have at least four images to composite
        img_str_list = [
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_EYES,
                eyes,
                FILE_EXT,
            )),
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_EYEB,
                eyebrows,
                FILE_EXT,
            )),
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_NOSE,
                nose,
                FILE_EXT,
            )),
            (0, 0),
            "".join((
                F_T_MAIN,
                fpfx,
                PREFIX_MOUTH,
                mouth,
                FILE_EXT,
            )),
        ]

        # check for others
        if sweat:
            img_str_list.extend((
                (0,0),
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_SWEAT,
                    sweat,
                    FILE_EXT,
                ))
            ))

        if tears:
            img_str_list.extend((
                (0, 0),
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_TEARS,
                    tears,
                    FILE_EXT,
                ))
            ))

        if emote:
            img_str_list.extend((
                (0, 0),
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_EMOTE,
                    emote,
                    FILE_EXT,
                ))
            ))

        # generate imComposite
        im_list.append(_gdgar_imc(
            cache_face,
            img_key,
            flt, 
            store.im.Composite((1280, 850), *img_str_list),
            day_key
        ))


    def _im_face_pre(im_list, flt, fpfx, lean, blush):
        """
        Adds face image manipulators that go before hair

        IN:
            flt - filter to use
            fpfx - face prefix to use
            lean - type of lean to use
            blush - type of blush

        OUT:
            im_list - list to add image manipulators to
        """
        img_key = (flt, 0, lean, blush)
        day_key = None
        if img_key in cache_face:
            if cache_face[img_key] is not None:
                im_list.append(cache_face[img_key])

            return

        elif flt != "day":
            # try checking for day version
            day_key = _dayify(img_key)
            if day_key in cache_face:
                if cache_face[day_key] is None:
                    # no image for this key, let the main key know
                    cache_face[img_key] = None

                else:
                    # otherwse generate from day
                    im_list.append(_gar_imc(
                        cache_face,
                        img_key,
                        flt,
                        cache_face[day_key]
                    ))

                return

        # NOTE: since theres only 1 thing here, we wont do anything fancy

        # otherwise, time to generate the im
        if blush:
            im_list.append(_gdgar_imc(
                cache_face,
                img_key,
                flt, 
                "".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_BLUSH,
                    blush,
                    FILE_EXT
                )),
                day_key
            ))
            return

        # otherwise nothing here
        cache_face[img_key] = None
        cache_face[day_key] = None

   
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

        im_list.append(_cgetg_imc(cache_hair, (flt, img_str), flt, img_str))


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
        day_key = None
        if img_key in cache_tc:
            im_list.append(cache_tc[img_key])
            return

        elif flt != "day":
            # try checking for day version
            day_key = _dayify(img_key)
            if day_key in cache_tc:
                im_list.append(_gar_imc(
                    cache_tc,
                    img_key,
                    flt,
                    cache_tc[day_key]
                ))
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
            # no shadow, so just table
            new_im = table_str

        # add to cache and list
        im_list.append(_gdgar_imc(cache_tc, img_key, flt, new_im, day_key))
        

# main sprite compilation

    def _im_sitting(
            clothing,
            hair,
            base_pose,
            arms_pose,
            eyebrows,
            eyes,
            nose,
            mouth,
            flt,
            acs_pre_list,
            acs_bbh_list,
            acs_bse_list,
            acs_bba_list,
            acs_ase_list,
            acs_bab_list,
            acs_bfh_list,
            acs_afh_list,
            acs_mid_list,
            acs_pst_list,
            leanpose,
            lean,
            arms,
            eyebags,
            sweat,
            blush,
            tears,
            emote,
            table,
            chair,
            show_shadow
    ):
        """
        Creates a list of image manipulators in order of desired render.

        IN:
            clothing - type of clothing
            hair - type of hair
            base_pose - MASPoseArms for base
            arms_pose - MASPoseArms for outfit
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            flt - filter to use
            acs_pre_list - sorted list of MASAccessories to draw prior to body
            acs_bbh_list - sroted list of MASAccessories to draw between back
                hair and body
            acs_bse_list - sorted list of MASAccessories to draw between base
                body and outfit
            acs_bba_list - sorted list of MASAccessories to draw between 
                body and back arms
            acs_ase_list - sorted list of MASAccessories to draw between base
                arms and outfit
            acs_bab_list - sorted list of MASAccessories to draw between
                back arms and boobs
            acs_bfh_list - sorted list of MASAccessories to draw between boobs
                and front hair
            acs_afh_list - sorted list of MASAccessories to draw between front
                hair and face
            acs_mid_list - sorted list of MASAccessories to draw between body
                and arms
            acs_pst_list - sorted list of MASAccessories to draw after arms
            leanpose - lean and arms together
            lean - type of lean
            arms - type of arms
            eyebags - type of eyebags
            sweat - type of sweatdrop
            blush - type of blush
            tears - type of tears
            emote - type of emote
            table - type of table
            chair - type of chair
            show_shadow - True will show shadow, false will not

        RETURNS: list of image manipulators
        """
        # NOTE: render order
        #   1. pre-acs - every acs that should render before anything
        #   2. back-hair - back portion of hair (split mode)
        #   3. bbh-acs - acs between Body and Back Hair
        #   4. chair - chair sprite
        #   5. base-0 - the base back part of body
        #   6. bse-acs - between base and body-0
        #   7. body-0 - the back part of body (no arms in split mode)
        #   8. table - the table/desk
        #   9. bba-acs - acs between Body and Back Arms
        #   10. arms-base-0 - the base back part of arm
        #   11. ase-acs-0 - between base arms and clothes, back part
        #   12. arms-0 - the back part of arms
        #   13. bab-acs - acs between Back Arms and Body-1
        #   14. base-1 - the base front part of body
        #   15. bse-acs - between base and body-1
        #   16. body-1 - the front part of body (boobs)
        #   17. bfh-acs - acs between Body and Front Hair
        #   18. face-pre - pre front hair facial expressions
        #   19. front-hair - front portion of hair (split mode)
        #   20. afh-acs - acs betweem Arms and Front Hair
        #   21. face - facial expressions
        #   22. mid-acs - acs between face and front arms
        #   23. arms-base-1 - the base front part of arms
        #   24. ase-acs-1 - between base arms and clothes, front part
        #   25. arms-1 - front arms
        #   26. pst-acs - acs after everything

        # initial values
        fpfx = face_lean_mode(lean)
        im_list = []

        # 1. pre-acs
        _im_accessory_list(
            im_list,
            acs_pre_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 2. back hair
        _im_hair(im_list, hair, flt, BHAIR_SUFFIX, lean)

        # 3. bbh-acs
        _im_accessory_list(
            im_list,
            acs_bbh_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 4. chair
        _im_chair(im_list, chair, flt)

        # 5. base-0
        # 6. bse-acs-0
        # 7. body-0
        _im_body_nh_wbase(
            im_list,
            clothing,
            acs_bse_list,
            "0",
            flt,
            leanpose,
            lean=lean
        )

        # 8. table
        _im_table(im_list, table, show_shadow, flt)

        # 9. bba-acs
        _im_accessory_list(
            im_list,
            acs_bba_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 10. arms-base-0
        # 11. ase-acs-0
        # 12. arms-0
        _im_arms_nh_wbase(
            im_list,
            base_pose,
            arms_pose,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "0"
        )

        # 13. bab-acs
        _im_accessory_list(
            im_list,
            acs_bab_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 14. base-1
        # 15. bse-acs-1
        # 16. body-1
        _im_body_nh_wbase(
            im_list,
            clothing,
            acs_bse_list,
            "1",
            flt,
            leanpose,
            lean=lean
        )

        # 17. bfh-acs
        _im_accessory_list(
            im_list,
            acs_bfh_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 18. face-pre
        _im_face_pre(im_list, flt, fpfx, lean, blush)

        # 19. front-hair
        _im_hair(im_list, hair, flt, FHAIR_SUFFIX, lean)

        # 20. afh-acs
        _im_accessory_list(
            im_list,
            acs_afh_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 21. face
        _im_face(
            im_list,
            eyes,
            eyebrows,
            nose,
            mouth,
            flt,
            fpfx,
            lean,
            sweat,
            tears,
            emote
        )

        # 22. mid-acs
        _im_accessory_list(
            im_list,
            acs_mid_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        # 23. arms-base-1
        # 24. ase-acs-1
        # 25. arms-1
        _im_arms_nh_wbase(
            im_list,
            base_pose,
            arms_pose,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "1"
        )

        # 26. pst-acs
        _im_accessory_list(
            im_list,
            acs_pst_list,
            flt,
            True,
            leanpose,
            lean=lean
        )

        return im_list


init -2 python:


    def mas_drawmonika_im(
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
            head="a",
            left="1l",
            right="1r",
            stock=True,
            single=None
        ):
        """
        Draws monika dynamically, using image manipulators
        See mas_drawmonika for more info.

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
        if not is_sitting or character.clothes.hasprop("baked outfit"):
            # image manips are only defined for sitting
            return mas_drawmonika(
                st, at, character,
                eyebrows, eyes, nose, mouth,
                lean, arms, eyebags, sweat, blush, tears, emote,
                head, left, right, stock, single
            )

        # gather accessories
        acs_pre_list = character.acs.get(MASMonika.PRE_ACS, [])
        acs_bbh_list = character.acs.get(MASMonika.BBH_ACS, [])
        acs_bse_list = character.acs.get(MASMonika.BSE_ACS, [])
        acs_bba_list = character.acs.get(MASMonika.BBA_ACS, [])
        acs_ase_list = character.acs.get(MASMonika.ASE_ACS, [])
        acs_bab_list = character.acs.get(MASMonika.BAB_ACS, [])
        acs_bfh_list = character.acs.get(MASMonika.BFH_ACS, [])
        acs_afh_list = character.acs.get(MASMonika.AFH_ACS, [])
        acs_mid_list = character.acs.get(MASMonika.MID_ACS, [])
        acs_pst_list = character.acs.get(MASMonika.PST_ACS, [])

        # NOTE: we also do not support baked

        # detremine all poses-specifc data to use:
        # [0] - lean to use
        # [1] - leanpose to use
        # [2] - arms to use
        # [3] - hair to use
        # [4] - base pose to use
        # [5] - arms pose to use
        pose_data = character._determine_poses(lean, arms)

        # determine filter to use
        flt = store.mas_sprites._decide_filter()

        # generate sprite displayable (and image manips)
        sprite = store.mas_sprites._gen_im_disp(store.mas_sprites._im_sitting(
            character.clothes.img_sit,
            pose_data[3].img_sit,
            pose_data[4],
            pose_data[5],
            eyebrows,
            eyes,
            nose,
            mouth,
            flt,
            acs_pre_list,
            acs_bbh_list,
            acs_bse_list,
            acs_bba_list,
            acs_ase_list,
            acs_bab_list,
            acs_bfh_list,
            acs_afh_list,
            acs_mid_list,
            acs_pst_list,
            pose_data[1],
            pose_data[0],
            pose_data[2],
            eyebags,
            sweat,
            blush,
            tears,
            emote,
            character.tablechair.table,
            character.tablechair.chair,
            character.tablechair.has_shadow
        ))

        # finally apply zoom 
        return Transform(sprite, zoom=store.mas_sprites.value_zoom), None


    def mas_drawemptydesk_im(st, at, character):
        """
        draws the table dynamically. includes ACS that should stay on desk.
        NOTE: uses image manips.
        NOTE: this is assumed to be used with empty desk ONLY
        NOTE: sitting only

        IN:
            st - renpy related
            at - renpy realted
            character - MASMonika character object
        """
        # in drawtable mode, only pst acs that stay on desk matter
        acs_pst_list = [
            acs
            for acs in character.acs.get(MASMonika.PST_ACS, [])
            if acs.keep_on_desk
        ]

        # prepare image manips
        im_list = []

        # decide the filter
        flt = store.mas_sprites._decide_filter()
        
        # now build the chair
        store.mas_sprites._im_chair(im_list, character.tablechair.chair, flt)

        # then the able
        store.mas_sprites._im_table(
            im_list,
            character.tablechair.table,
            False.
            flt
        )

        # then the pst acs we got
        store.mas_sprites._im_accessorylist(
            im_list,
            acs_pst_list,
            flt,
            True,
            "steepling"
        )

        # generate sprite displayable
        sprite = store.mas_sprites._gen_im_disp(im_list)

        # finally appyl zoom and return
        return Transform(sprite, zoom=store.mas_sprites.value_zoom), None 


