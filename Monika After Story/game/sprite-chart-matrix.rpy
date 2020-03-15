# sprite generation using matrix for night sprites
# TODO: look at adding a highlight option to ACS/Clothes/Hair

python early:
# Custom filter renderable

# uncomment this if you want syntax highlighting support on vim
#init -1 python:

    class MASFilterable(renpy.Displayable):
        """
        Special displayable that adjusts its image based on filter.
        Also includes surface caching, if desired.

        PROPERTIES:
            rendered_surface - render for this displayable. Can be used for
                caching.
            flt - filter we last used
        """

        def __init__(self, 
                focus=None,
                default=False,
                style='default',
                _args=None,
                **properties
        ):
            """
            Constructor

            IN:
                All params are passed to Displayable
            """
            super(renpy.Displayable, self).__init__(
                focus=focus,
                default=default,
                style=style,
                _args=_args,
                **properties
            )
            self.rendered_surface = None
            self.flt = None

        # NOTE: extended classes should impelement the render function.


    # TODO: use this wwith standard sprites. (think ConditionSwitch with
    #   morning flag. NOTE: wait until room deco as that is where this will
    #   actually matter.
    class MASFilterableSprite(MASFilterable):
        """
        Basic filterable sprite that changes for filter.
        This has NO x/y support

        PROPERTIES:
            img_obj - the Image object represnting this sprite
        """

        def __init__(self,
                image_path,
                focus=None,
                default=False,
                style='default',
                _args=None,
                **properties
        ):
            """
            Constructor

            IN:
                image_path - image path (or Image) of the sprite to use
                remaining properties are sent to Displayable
            """
            super(MASFilterable, self).__init__(
                focus=focus,
                default=default,
                style=style,
                _args=_args,
                **properties
            )
            self.img_obj = Image(image_path)

        def render(self, width, height, st, at):
            curr_flt = store.mas_sprites._decide_filter()
            if curr_flt != self.flt or self.rendered_surface is None:
                # need new render
                self.flt = curr_flt

                # prepare filtered image
                new_img = store.mas_sprites._gen_im(self.flt, self.img_obj)

                # render and blit
                render = renpy.render(new_img, width, height, st, at)
                rv = renpy.Render(width, height)
                rv.blit(render, (0, 0))

                # save
                self.rendered_surface = rv

            return self.rendered_surface

        def visit(self):
            return [self.img_obj]


init -99 python in mas_sprites:
    # NOTE: this must be after -100 and -101

    import store

    # do a file check for disabling im mode
    disable_im = store.is_file_present("no_matrix")


# this should be after sprite-chart's initialization
init -4 python in mas_sprites:
    # NOTE: render_key

    Y_OFFSET = -130

    # TODO: please consider ways we can get submods to add their own filtesr
    #   likely via APIs that they can use to add filters.
    #   We should also move filter definitions to -99. 
    # TODO: consider making the filter dict use Curryables so custom filters
    #   can use non-Matrixcolor-based logic

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

    # cache ids
    CID_FACE = 1 # NOTE: we should not use highlights for this
    CID_ARMS = 2
    CID_BODY = 3
    CID_HAIR = 4
    CID_ACS = 5
    CID_TC = 6
    CID_HL = 7

    # several caches for images

    CACHE_TABLE = {
        CID_FACE: {},
        # the facial expression cache. Facial expressions are the most likely
        # things to overlap across clothing, hair, and ACS, so we should cache 
        # them together to maximize performance
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
        #   image manip containing render, or None if should not be rendered

        CID_ARMS: {},
        # the arms cache. This includes clothes and base sprites.
        # key:
        #   tuple containing strings.
        #   [0] - filter code
        #   [1] - base code
        #   [2] - clothing type, "base" for base arms
        #   [3] - leanpose
        # value:
        #   image manip containing render, or None if should not be rendered

        CID_BODY: {},
        # the body cache. This includes clothes and base sprites.
        # key:
        #   tuple containing strings. 
        #   [0] - should be the filter code.
        #   [1] - shoud be image path
        # value:
        #   image manip containing render, or None if should not be rendered

        CID_HAIR: {},
        # the hair cache
        # key:
        #   tuple containing strings. 
        #   [0] - should be the filter code.
        #   [1] - should be image path
        # value:
        #   image manip containing render, or None if should not be rendered
   
        CID_ACS: {},
        # the ACS cache
        # key:
        #   tuple containing strings. 
        #   [0] - should be the filter code.
        #   [1] - acs name (id)
        #   [3] - poseid
        #   [4] - arm code
        # value:
        #   image manip containing render, or None if should not be rendered

        CID_TC: {},
        # the tablechair cache
        # key:
        #   tuple containing strings
        #   [0] - should be the filter code
        #   [1] - should be either table/chair (0, 1)
        #   [2] - table/chair type
        #   [3] - 0 for no shadow, 1 for shadow (ignored for chairs)
        # value:
        #   image manip containing render, or None if should not be rendered

        CID_HL: {},
        # the highlight cache
        # key:
        #   tuple containing:
        #   [0] - cache ID - determines what sprite this highlight is for
        #   [1+] - the sprite's key
        # value:
        #   Image object, or None if should not be rendered
    }

    MFM_CACHE = {}
    # MASFilterMap cache
    # key: hash value of a MASFilterMAp
    # value: MASFilterMap for a hash value

    class MASMonikaRender(store.MASFilterable):
        """
        custom rendering class for MASMonika. This does caching and rendering
        at the same time.

        INHERED PROPS:
            rendered_surface - the render for this displayable.
                If we our render is called more than once, then this is
                reutrned.
            flt - filter we are using (string)

        PROPERTIES:
            render_keys - list of tuples of the following format:
                [0] - key of an image to generate. used to check cache
                [1] - cache ID of the cache to use
                [2] - ImageBase to build the image, IF NOT IN CACHE.
                    This should be set to None if we are sure a surf
                    object is in the cache.
                [3] - ImageBase to build the highlight. Set to None if no
                    no highlight or in cache.
            xpos - xposition to blit objects with
            ypos - yposition to blit objects with
            width - width to render objects with
            height - height to render objects with
        """

        def __init__(self, render_keys, flt, xpos, ypos, width, height):
            """
            Constructor for a MASMOnikaRender object

            IN:
                render_keys - image keys and ImageBase if needed. 
                    See props.
                flt - filter we are using (string)
                xpos - xposition to blit objects with
                ypos - yposition to blit objects with
                width - width to render objects with
                height - height to render objects with
            """
            super(store.MASFilterable, self).__init__()
            self.render_keys = render_keys
            self.rendered_surface = None
            self.xpos = xpos
            self.ypos = ypos
            self.width = width
            self.height = height
            self.flt = flt

        def _l_render_hl(self, render_list, render_key, st, at):
            """
            Retrieves highlight image from cache, or renders if needed

            IN:
                render_key - tuple of the following format
                    [0] - key of image to generate
                    [1] - cache ID of the cache to use
                    [2] - ImageBase to build the image
                    [3] - ImageBase to build the highlight
                st - renpy related
                at - renpy related

            OUT:
                render_list - list to add render to, if needed
            """
            # NOTE: face will never have highlight (for now)
            if render_key[1] == store.mas_sprites.CID_FACE:
                return None

            # add cache id to front for highlight key
            hl_key = (render_key[1],) + render_key[0]

            # check highlight cache
            img_base = store.mas_sprites._cs_im(
                hl_key,
                store.mas_sprites.CID_HL,
                render_key[3]
            )

            if img_base is not None:
                render_list.append(renpy.render(
                    img_base,
                    self.width,
                    self.height,
                    st, at
                ))


        def _render_surf(self, render_key, st, at):
            """
            Retrieves surf image from cache, or renders if needed

            IN:
                render_key - tuple of the following format:
                    [0] - key of image to generate
                    [1] - cache ID of the cache to use
                    [2] - ImageBase to build the image
                    [3] - ImageBase to build the highlight
                st - renpy related
                at - renpy related

            RETURNS: rendered surf image to use
            """
            # render this bitch
            new_surf = renpy.render(
                store.mas_sprites._cgen_im(
                    self.flt,
                    render_key[0],
                    render_key[1],
                    render_key[2]
                ),
                self.width,
                self.height,
                st, at
            )

            #new_surf = renpy.display.im.load_surface(
            #    store.mas_sprites._gen_im(self.flt, img_base)
            #)
            return new_surf

        def render(self, width, height, st, at):
            """
            Render function
            """
            curr_flt = store.mas_sprites._decide_filter()
            if self.rendered_surface is None or curr_flt != self.flt:
                self.flt = curr_flt
                renders = []
                for render_key in self.render_keys:
                    renders.append(self._render_surf(render_key, st, at))
                    self._l_render_hl(renders, render_key, st, at)

                # blit all
                rv = renpy.Render(width, height)
                for render in renders:
                    rv.blit(render, (self.xpos, self.ypos + Y_OFFSET))

                self.rendered_surface = rv

            return self.rendered_surface

        def visit(self):
            """
            Returns a list of displayables we obtain
            NOTE: will also save to our cache
            """
            self.flt = store.mas_sprites._decide_filter()
            disp_list = []
            for render_key in self.render_keys:
                store.mas_sprites._cgha_im(disp_list, self.flt, render_key)

            return disp_list


    def _add_mpa_rk(
            rk_list, 
            mpa,
            pfx_list,
            flt,
            bcode,
            clothing_t,
            leanpose
    ):
        """
        Adds render key for MASPoseArms, if needed.

        IN:
            mpa - MASPoseArms to make render key for
            pfx_list - prefix list to generate image string with
            flt - filter code to use
            bcode - base code to use
            clothing - type of clothing to use
            leanpose - leanpose to use

        OUT:
            rk_list - render key list to add render keys to
        """
        # check cache
        img_key = (flt, bcode, clothing_t, leanpose)
        cache_arms = _gc(CID_ARMS)
        day_key = None
        if img_key in cache_arms:
            if cache_arms[img_key] is not None:
                rk_list.append((img_key, CID_ARMS, None, None))

            return

        elif flt != FLT_DAY:
            # try checking if day version is None
            day_key = _dayify(img_key)
            if cache_arms.get(day_key, True) is None:
                # no image for this key, let the main key know
                cache_arms[img_key] = None
                return

        # get arm data
        arm_data = mpa.get(bcode, flt)
        if len(arm_data) == 0:
            # no arms to render
            cache_arms[img_key] = None
            cache_arms[day_key] = None
            return

        # if only 1 item , then dont need to composite
        if len(arm_data) < 2:
            img_tup, hl_tup = arm_data[0]

            # geneate image base
            img_base = store.Image("".join(pfx_list + img_tup + (FILE_EXT,)))

            # determine highlight
            if len(hl_tup) > 0:
                hl_img = store.Image("".join(pfx_list + hl_tup + (FILE_EXT,)))
            else:
                hl_img = None

            rk_list.append((img_key, CID_ARMS, img_base, hl_img))
            return

        # more than 1 item, need to composite
        arm_comp_args = [LOC_WH]
        hl_comp_args = [LOC_WH]

        for arm in arm_data:
            img_tup, hl_tup = arm
            arm_comp_args.append((0, 0))
            arm_comp_args.append("".join(pfx_list + img_tup + (FILE_EXT,)))

            if len(hl_tup) > 0:
                hl_comp_args.append((0, 0))
                hl_comp_args.append("".join(pfx_list + hl_tup + (FILE_EXT,)))

        # now generate composites
        img_comp = store.im.Composite(*arm_comp_args)
        if len(hl_comp_args) > 1:
            hl_comp = store.im.Composite(*hl_comp_args)
        else:
            hl_comp = None

        # and add results
        rk_list.append((img_key, CID_ARMS, img_comp, hl_comp))


    def _bhli(img_list, hlcode):
        """
        Builds a 
        High-
        Light
        Image using the base image path

        IN:
            img_list - list of strings that form the base image string
                NOTE: we assume that the last item in this string is the 
                FILE_EXT. This also assumes highlight codes are always inserted
                right before the file extension.
            hlcode - highlight code to use. Can be None.

        RETURNS: Image to use for highlight, or None if no highlight.
        """
        if hlcode is None:
            return None

        # otherwise list copy and splice
        hl_list = list(img_list)
        hl_list[-1:-1] = [HLITE_SUFFIX, hlcode]
        return store.Image("".join(hl_list))


    def _cgen_im(flt, key, cid, img_base):
        """
        Checks cache for an im, 
        GENerates the im if not found

        IN:
            flt - filter to use
            key - key of the image
            cid - cache ID of the cache to use
            img_base - ImageBase to build the image

        RETURNS: Image Manipulator for this render
        """
        img_cache = _gc(cid)
        if key in img_cache:
            return img_cache[key]

        # generate the im and cache it
        new_im = _gen_im(flt, img_base)
        img_cache[key] = new_im
        return new_im


    def _cgha_im(render_list, flt, render_key):
        """
        Checks cache of an image
        Generates the im if not found, and sets
        Highlight if needed.
        Adds IMs to the given render list

        NOTE: should only be used by the visit function

        IN:
            flt - filter to use
            render_key - tuple of the following format:
                [0] - key of the image to generate
                [1] - cache ID of the cahce to use
                [2] - ImageBase to build the image
                [3] - ImageBase to build the highlight
            st - renpy related
            at - renpy related

        OUT:
            render_list - list to add IMs to
        """
        img_key, cid, img_base, hl_base = render_key
        img_cache = _gc(cid)
        hl_key = _hlify(img_key, cid)
        if img_key in img_cache:
            render_list.append(img_base)

            # check for highlight
            # NOTE: if the img key exists in the cache, then we know for sure
            #   that the highlight must be in the cache already
            hl_base = _gc(CID_HL).get(hl_key, None)
            if hl_base is not None:
                render_list.append(hl_base)
            return

        # otherwise, we need to generate the im (and maybe hl) and cache it
        new_im = _gen_im(flt, img_base)
        img_cache[img_key] = new_im
        render_list.append(new_im)

        # check for highlight
        _gc(CID_HL)[hl_key] = hl_base
        if hl_base is not None:
            render_list.append(hl_base)


    def _cs_im(key, cid, img_base):
        """
        Checks cache for an im
        Stores the img_base if not found

        IN:
            key - key of the image
            cid - cache ID of the cache to use
            img_base - ImageBase to build the image

        RETURNS: ImageBase
        """
        img_cache = _gc(cid)
        if key in img_cache:
            return img_cache[key]

        # store then return
        img_cache[key] = img_base
        return img_base


    def _dayify(img_key):
        """
        Dayifies the given image key.
        DAying simply replaces the filter portion of the key with "day"

        IN:
            img_key - image key to dayify

        RETURNS: dayified key
        """
        img_key_list = list(img_key)
        img_key_list[0] = FLT_DAY
        return tuple(img_key_list)


    def _gc(cid):
        """
        Gets the
        Cache

        IN:
            cid - cache ID of the cache to get

        RETURNS: cache, or empty dict if cache not found
        """
        return CACHE_TABLE.get(cid, {})


    def _gen_im(flt, img_base):
        """
        GENerates an image maniuplator
        NOTE: always assumes we have an available filter.

        IN:
            flt - filter to use
            img_base - image path or manipulator to use

        RETURNS: generated render key
        """
        # NOTE: no render
        return store.im.MatrixColor(img_base, FILTERS[flt])


    def _gen_im_disp(rk_list):
        """DEPRECATED
        Generates a LiveComposite (which is just a Fixed) displayable given a 
        list of render keys. This uses the positions defined by
        zoom. (adjustx, adjusty)

        IN:
            rk_list - list of render keys we generated

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
        for img_man in rk_list:
            disp.add(renpy.display.layout.Position(
                img_man,
                xpos=adjust_x,
                xanchor=0,
                ypos=adjust_y,
                yanchor=0
            ))

        return disp


    def _hlify(key, cid):
        """
        Highlightifies the given key.
        Highlightifying is just prefixing the key with the cid

        IN:
            key - key to highlightify
            cid - cid to use when highlighting

        RETURNS: highlightified key
        """
        return (cid,) + key


    # rk-based sprite maker functions
    def _rk_accessory(
            rk_list,
            acs,
            flt,
            arm_split,
            leanpose=None
    ):
        """
        Adds accessory render key if needed

        IN:
            acs - MASAccessory object
            flt - filter to apply
            arm_split - see MASAccessory.arm_split for codes. None for no 
                codes at all.
            leanpose - current pose
                (Default: None)

        OUT:
            rk_list - list to add render keys to
        """
        # pose map check
        # Since None means we dont show, we are going to assume that the
        # accessory should not be shown if the pose key is missing.
        poseid = acs.pose_map.get(leanpose, None)

        # get arm code if needed
        # NOTE: we can be sure that a nonsplit acs will not be used in 
        #   a split context.
        if arm_split is None:
            arm_code = ""

        elif arm_split in acs.get_arm_split_code(leanpose):
            arm_code = ART_DLM + arm_split

        else:
            # we should not render
            arm_code = None

        # now we can generate the key and check cache
        img_key = (flt, acs.name, poseid, arm_code)
        cache_acs = _gc(CID_ACS)
        day_key = None
        if img_key in cache_acs:
            if cache_acs[img_key] is not None:
                rk_list.append((img_key, CID_ACS, None, None))

            return

        elif flt != FLT_DAY:
            # check of day version is none
            day_key = _dayify(img_key)
            if cache_acs.get(day_key, True) is None:
                # no image for this key, let main key know
                cache_acs[img_key] = None
                return

        # now check other acs-related elements that may stop render
        if poseid is None or arm_code is None:
            # a None here means we should shouldnt' even show this acs
            # for this pose. Weird, but maybe it happens?
            cache_acs[img_key] = None
            cache_acs[day_key] = None
            return

        # build img list minus file extensions
        img_list = [
            A_T_MAIN,
            PREFIX_ACS,
            acs.img_sit,
            ART_DLM,
            poseid,
            arm_code,
            FILE_EXT,
        ]
      
        # finally add the render key
        rk_list.append((
            img_key,
            CID_ACS,
            store.Image("".join(img_list)),
            _bhli(img_list, acs.opt_gethlc(poseid, flt, arm_split))
        ))


    def _rk_accessory_list(
            rk_list,
            acs_list,
            flt,
            leanpose=None,
            arm_split=None
    ):
        """
        Adds accessory render keys for a list of accessories

        IN:
            acs_list - list of MASAccessory objects, in order of rendering
            flt - filter to use
            arm_split - set to MASAccessory.arm_split code if we are rendering
                arm_split-affected ACS. If None, we use standard algs.
                (Default: None)
            leanpose - arms pose for we are currently rendering
                (Default: None)

        OUT:
            rk_list - list to add render keys to
        """
        if len(acs_list) == 0:
            return

        for acs in acs_list:
            _rk_accessory(
                rk_list,
                acs,
                flt,
                arm_split,
                leanpose
            )


    def _rk_arms_base_nh(rk_list, bpose, leanpose, flt, bcode):
        """
        Adds arms base render keys
        (equiv to _ms_arms_nh_up_base)

        IN:
            bpose - MASPoseArms to use
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_mpa_rk(
            rk_list,
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


    def _rk_arms_base_lean_nh(rk_list, bpose, lean, leanpose, flt, bcode):
        """
        Adds arms base lean render key
        (eqiv to _ms_arms_nh_leaning_base)

        IN:
            bpose - MASPoseArms to use
            lean - type of lean
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_mpa_rk(
            rk_list,
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


    def _rk_arms_nh(rk_list, apose, clothing, leanpose, flt, bcode):
        """
        Adds arms render key
        (equiv to _ms_arms_nh_up_arms)

        IN:
            apose - MASPoseARms to use
            clothing - MASClothes object
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_mpa_rk(
            rk_list,
            apose,
            (
                C_MAIN,
                clothing.img_sit,
                "/",
                PREFIX_ARMS,
            ),
            flt,
            bcode,
            clothing.img_sit,
            leanpose
        )


    def _rk_arms_lean_nh(rk_list, apose, clothing, lean, leanpose, flt, bcode):
        """
        Adds arms lean render key
        (equiv to _ms_arms_nh_leaning_arms)

        IN:
            apose - MASPoseArms to use
            clothing - MASClothes object
            lean - type of lean
            leanpose - leanpose to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        _add_mpa_rk(
            rk_list,
            apose,
            (
                C_MAIN,
                clothing.img_sit,
                "/",
                PREFIX_ARMS_LEAN,
                lean,
                ART_DLM,
            ),
            flt,
            bcode,
            clothing.img_sit,
            leanpose
        )


    def _rk_arms_nh_wbase(
            rk_list,
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
        Adds arms render keys, no hair, with baes

        IN:
            bpose - MASPoseArms for base
            apose - MASPoseArms for outfit
            clothing - MASClothes object
            acs_ase_list - acs between arms-base-0 and arms-0
            leanpose - leanpose to pass to accessorylist
            lean - lean to use
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        if lean:
            # arms-base-0
            _rk_arms_base_lean_nh(rk_list, bpose, lean, leanpose, flt, bcode)

            # acs-ase
            _rk_accessory_list(rk_list, acs_ase_list, flt, leanpose, bcode)

            if apose is not None:
                # arms-0
                _rk_arms_lean_nh(
                    rk_list,
                    apose,
                    clothing,
                    lean,
                    leanpose,
                    flt,
                    bcode
                )

        else:
            # arms-base-0
            _rk_arms_base_nh(rk_list, bpose, leanpose, flt, bcode)

            # acs-ase
            _rk_accessory_list(rk_list, acs_ase_list, flt, leanpose, bcode)

            if apose is not None:
                # arms-0
                _rk_arms_nh(rk_list, apose, clothing, leanpose, flt, bcode)


    def _rk_base_body_nh(rk_list, flt, bcode):
        """
        Adds base body render keys, no hair
        (equiv of _ms_torso_nh_base)

        IN:
            flt - filter ot use
            bcode- base code to use

        OUT:
            rk_list - list to add render keys to 
        """
        img_str = "".join((
            B_MAIN,
            BASE_BODY_STR,
            bcode,
            FILE_EXT,
        ))

        # cache check
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return

        rk_list.append((img_key, CID_BODY, store.Image(img_str), None))
    

    def _rk_base_body_lean_nh(rk_list, lean, flt, bcode):
        """
        Adds base body lean render keys, no hair
        (equivalent of _ms_torsoleaning_nh_base)

        IN:
            lean - type of lean
            flt - filter to use
            bcode - base code to use

        OUT:
            rk_list - list to add render keys to
        """
        img_str = "".join((
            B_MAIN,
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            bcode,
            FILE_EXT,
        ))

        # cache check
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return

        rk_list.append((img_key, CID_BODY, store.Image(img_str), None))


    def _rk_body_nh(rk_list, clothing, flt, bcode, leanpose):
        """
        Adds body render keys, no hair
        (equiv of _ms_torso_nh)

        IN:
            clothing - MASClothes object
            flt - filter to use
            bcode - base code to use
            leanpose - leanpose to use

        OUT:
            rk_list - list to add render keys to
        """
        img_list = (
            C_MAIN,
            clothing.img_sit,
            "/",
            NEW_BODY_STR,
            ART_DLM,
            bcode,
            FILE_EXT,
        )
        img_str = "".join(img_list)

        # cache check
        img_key = (flt, img_str)
        if img_key in _gc(CID_BODY):
            rk_list.append((img_key, CID_BODY, None, None))
            return

        # otherwise build ImageBase
        rk_list.append((
            img_key,
            CID_BODY,
            store.Image(img_str),
            _bhli(img_list, clothing.gethlc(leanpose, flt, bcode)),
        ))


    def _rk_body_lean_nh(rk_list, clothing, lean, flt, bcode, leanpose):
        """
        Adds body leaning render keys, no hair
        (equiv of _ms_torsoleaning_nh)

        IN:
            clothing - MASClothes object
            lean - type of lean
            flt - filter to use
            bcode - base code to use
            leanpose - leanpose to use

        OUT:
            rk_list - list to add render keys to
        """
        # build img str
        img_list = (
            C_MAIN,
            clothing.img_sit,
            "/",
            PREFIX_BODY_LEAN,
            lean,
            ART_DLM,
            bcode,
            FILE_EXT,
        )
        img_str = "".join(img_list)

        # key check
        img_key = (flt, img_str)
        cache_body = _gc(CID_BODY)
        if img_key in cache_body:
            rk_list.append((img_key, CID_BODY, None, None))
            return

        # otherwise need to build ImageBase
        rk_list.append((
            img_key,
            CID_BODY,
            store.Image(img_str),
            _bhli(img_list, clothing.gethlc(leanpose, flt, bcode))
        ))


    def _rk_body_nh_wbase(
            rk_list,
            clothing,
            acs_bse_list,
            bcode,
            flt,
            leanpose,
            lean=None
    ):
        """
        Adds body render keys, including base and bse acs, no hair

        IN:
            clothing - MASClothes object
            acs_bse_list - acs between base-0 and body-0
            bcode - base code to use
            flt - filter to use
            leanpose - leanpose to pass to accessorylist
            lean - type of lean

        OUT:
            rk_list - list to add render keys to
        """
        if lean:
            # base-0
            _rk_base_body_lean_nh(rk_list, lean, flt, bcode)

            # acs_bse
            _rk_accessory_list(rk_list, acs_bse_list, flt, leanpose, bcode)

            # body-0
            _rk_body_lean_nh(rk_list, clothing, lean, flt, bcode, leanpose)

        else:
            # base-0
            _rk_base_body_nh(rk_list, flt, bcode)

            # acs_bse
            _rk_accessory_list(rk_list, acs_bse_list, flt, leanpose, bcode)

            # body-0
            _rk_body_nh(rk_list, clothing, flt, bcode, leanpose)


    def _rk_chair(rk_list, mtc, flt):
        """
        Adds chair render key

        IN:
            mtc - MASTableChair object
            flt - filter to use

        OUT:
            rk_list - list to add render keys to
        """
        # check cache
        img_key = (flt, 1, mtc.chair)
        cache_tc = _gc(CID_TC)
        if img_key in cache_tc:
            rk_list.append((img_key, CID_TC, None, None))
            return

        # otherwise build it
        img_list = (
            T_MAIN,
            PREFIX_CHAIR,
            mtc.chair,
            FILE_EXT,
        )
        img_str = "".join(img_list)

        rk_list.append((
            img_key,
            CID_TC,
            store.Image(img_str),
            _bhli(
                img_list,
                store.MASHighlightMap.o_fltget(mtc.hl_map, "c", flt)
            )
        ))


    def _rk_face(
            rk_list,
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
        Adds face render keys

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
            rk_list - list to add render keys to
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
        cache_face = _gc(CID_FACE)
        if img_key in cache_face:
            if cache_face[img_key] is not None:
                rk_list.append((img_key, CID_FACE, None, None))
            return

        elif flt != FLT_DAY:
            # try using day key
            day_key = _dayify(img_key)
            if cache_face.get(day_key, True) is None:
                # no image for this key, let main key know
                cache_face[img_key] = None
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
        rk_list.append((
            img_key,
            CID_FACE,
            store.im.Composite((1280, 850), *img_str_list),
            None
        ))


    def _rk_face_pre(rk_list, flt, fpfx, lean, blush):
        """
        Adds face render keys that go before hair

        IN:
            flt - filter to use
            fpfx - face prefix to use
            lean - type of lean to use
            blush - type of blush

        OUT:
            rk_list - list to add render keys to
        """
        img_key = (flt, 0, lean, blush)
        day_key = None
        cache_face = _gc(CID_FACE)
        if img_key in cache_face:
            if cache_face[img_key] is not None:
                rk_list.append((img_key, CID_FACE, None, None))

            return

        elif flt != FLT_DAY:
            # try checking for day version
            day_key = _dayify(img_key)
            if cache_face.get(day_key, True) is None:
                # no image for this key, let the main key know
                cache_face[img_key] = None
                return

        # NOTE: since theres only 1 thing here, we wont do anything fancy

        # otherwise, time to generate the im
        if blush:
            rk_list.append((
                img_key, 
                CID_FACE,
                store.Image("".join((
                    F_T_MAIN,
                    fpfx,
                    PREFIX_BLUSH,
                    blush,
                    FILE_EXT
                ))),
                None,
            ))
            return

        # otherwise nothing here
        cache_face[img_key] = None
        cache_face[day_key] = None

   
    def _rk_hair(rk_list, hair, flt, hair_key, leanpose, lean):
        """
        Adds hair render key

        IN:
            hair - MASHair object
            flt - filter to use
            hair_key - hair key to use (front/back)
            leanpose - leanpose to use
            lean - tyoe of lean

        OUT:
            rk_list - list to add render keys to
        """
        # build img str
        if lean:
            img_list = (
                H_MAIN,
                PREFIX_HAIR_LEAN,
                lean,
                ART_DLM,
                hair.img_sit,
                ART_DLM,
                hair_key,
                FILE_EXT,
            )

        else:
            img_list = (
                H_MAIN,
                PREFIX_HAIR,
                hair.img_sit,
                ART_DLM,
                hair_key,
                FILE_EXT,
            )

        # genreate string for key check
        img_str = "".join(img_list)

        # key check
        img_key = (flt, img_str)
        cache_hair = _gc(CID_HAIR)
        if img_key in cache_hair:
            rk_list.append((img_key, CID_HAIR, None, None))
            return

        # otherwise need to build ImageBase
        rk_list.append((
            img_key,
            CID_HAIR,
            store.Image(img_str),
            _bhli(img_list, hair.gethlc(leanpose, flt, hair_key)),
        ))


    def _rk_table(rk_list, tablechair, show_shadow, flt):
        """
        Adds table render key

        IN:
            table - MASTableChair object
            show_shadow - True if shadow should be included, false if not
            flt filter to use

        OUT:
            rk_list - list to add render keys to
        """
        img_key = (flt, 0, tablechair.table, int(show_shadow))
        if img_key in _gc(CID_TC):
            rk_list.append((img_key, CID_TC, None, None))
            return

        # otherwise, we need to create the table sprite, maybe with shadow
        table_list = (
            T_MAIN,
            PREFIX_TABLE,
            tablechair.table,
            FILE_EXT,
        )
        table_str = "".join(table_list)

        # in this case, we may need to use im.Composite
        if show_shadow:
            # need to make shadow
            shdw_list = (
                T_MAIN,
                PREFIX_TABLE,
                tablechair.table,
                SHADOW_SUFFIX,
                FILE_EXT,
            )
            shdw_str = "".join(shdw_list)

            new_im = _gen_im(flt, store.im.Composite(
                (1280, 850),
                (0, 0), table_str,
                (0, 0), shdw_str
            ))

            # determine highlight
            hl_img = _bhli(
                shdw_list,
                store.MASHighlightMap.o_fltget(tablechair.hl_map, "ts", flt)
            )

        else:
            # no shadow, so just table
            new_im = store.Image(table_str)

            # determine highlight
            hl_img = _bhli(
                table_list,
                store.MASHighlightMap.o_fltget(tablechair.hl_map, "t", flt)
            )

        # add to list
        rk_list.append((img_key, CID_TC, new_im, hl_img))
        

# main sprite compilation

    def _rk_sitting(
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
            acs_bat_list,
            acs_mat_list,
            acs_mab_list,
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
            tablechair,
            show_shadow
    ):
        """
        Creates a list of render keys in order of desired render.

        IN:
            clothing - MASClothes object
            hair - MASHair object
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
            acs_bat_list - sorted list of MASAccessories to draw between back
                arms and table
            acs_mat_list - sorted list of MASAccessories to draw between
                middle arms and table
            acs_mab_list - sorted list of MASAccessories to draw between
                middle arms and boobs
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
            tablechair - MASTableChair object
            show_shadow - True will show shadow, false will not

        RETURNS: list of render keys
        """
        # NOTE: render order
        #   1. pre-acs - every acs that should render before anything
        #   2. back-hair - back portion of hair (split mode)
        #   3. bbh-acs - acs between Body and Back Hair
        #   4. chair - chair sprite
        #   5. base-0 - the base back part of body
        #   6. bse-acs - between base and body-0
        #   7. body-0 - the back part of body (no arms in split mode)
        #   8. bba-acs - acs between Body and Back Arms
        #   9. arms-base-0 - the base back part of arm
        #   10. ase-acs-0 - between base arms and clothes, back part
        #   11. arms-0 - the back part of arms
        #   12. bat-acs - acs between Back Arms and Table
        #   13. table - the table/desk
        #   14. mat-acs acs between Middle Arms and Table
        #   15. arms-base-5 - the base middle part of arm
        #   16. ase-acs-5 - between base arms and clothes, middle part
        #   17. arms-5 - the middle part of arms
        #   18. mab-acs - acs between Middle Arms and Body-1
        #   19. base-1 - the base front part of body
        #   20. bse-acs - between base and body-1
        #   21. body-1 - the front part of body (boobs)
        #   22. bfh-acs - acs between Body and Front Hair
        #   23. face-pre - pre front hair facial expressions
        #   24. front-hair - front portion of hair (split mode)
        #   25. afh-acs - acs betweem Arms and Front Hair
        #   26. face - facial expressions
        #   27. mid-acs - acs between face and front arms
        #   28. arms-base-10 - the base front part of arms
        #   29. ase-acs-10 - between base arms and clothes, front part
        #   30. arms-10 - front arms
        #   31. pst-acs - acs after everything

        # initial values
        fpfx = face_lean_mode(lean)
        rk_list = []

        # 1. pre-acs
        _rk_accessory_list(rk_list, acs_pre_list, flt, leanpose)

        # 2. back hair
        _rk_hair(rk_list, hair, flt, BHAIR, leanpose, lean)

        # 3. bbh-acs
        _rk_accessory_list(rk_list, acs_bbh_list, flt, leanpose)

        # 4. chair
        _rk_chair(rk_list, tablechair, flt)

        # 5. base-0
        # 6. bse-acs-0
        # 7. body-0
        _rk_body_nh_wbase(
            rk_list,
            clothing,
            acs_bse_list,
            "0",
            flt,
            leanpose,
            lean=lean
        )

        # 8. bba-acs
        _rk_accessory_list(rk_list, acs_bba_list, flt, leanpose)

        # 9. arms-base-0
        # 10. ase-acs-0
        # 11. arms-0
        _rk_arms_nh_wbase(
            rk_list,
            base_pose,
            arms_pose,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "0"
        )

        # 12. bat-acs
        _rk_accessory_list(rk_list, acs_bat_list, flt, leanpose)

        # 13. table
        _rk_table(rk_list, tablechair, show_shadow, flt)

        # TODO: add acs layer here (MAT - middle arms and table)
        # 14. mat-acs
        _rk_accessory_list(rk_list, acs_mat_list, flt, leanpose)

        # 15. arms-base-5
        # 16. ase-acs-5
        # 17. arms-5
        _rk_arms_nh_wbase(
            rk_list,
            base_pose,
            arms_pose,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "5"
        )

        # 18. mab-acs
        _rk_accessory_list(rk_list, acs_mab_list, flt, leanpose)

        # 19. base-1
        # 20. bse-acs-1
        # 21. body-1
        _rk_body_nh_wbase(
            rk_list,
            clothing,
            acs_bse_list,
            "1",
            flt,
            leanpose,
            lean=lean
        )

        # 22. bfh-acs
        _rk_accessory_list(rk_list, acs_bfh_list, flt, leanpose)

        # 23. face-pre
        _rk_face_pre(rk_list, flt, fpfx, lean, blush)

        # 24. front-hair
        _rk_hair(rk_list, hair, flt, FHAIR, leanpose, lean)

        # 25. afh-acs
        _rk_accessory_list(rk_list, acs_afh_list, flt, leanpose)

        # 26. face
        _rk_face(
            rk_list,
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

        # 27. mid-acs
        _rk_accessory_list(rk_list, acs_mid_list, flt, leanpose)

        # 28. arms-base-1
        # 29. ase-acs-1
        # 30. arms-1
        _rk_arms_nh_wbase(
            rk_list,
            base_pose,
            arms_pose,
            clothing,
            acs_ase_list,
            leanpose,
            lean,
            flt,
            "10"
        )

        # 31. pst-acs
        _rk_accessory_list(rk_list, acs_pst_list, flt, leanpose)

        return rk_list


init -2 python:

    # TODO: make MASFilterMap hashable, then setup caching
    class MASFilterMap(object):
        """
        The FilterMap connects filters to values

        PROPERTIES:
            map - dict containg filter to string map
                key: filter constant
                value: string or, None if no highlight
        """
        import store.mas_sprites_json as msj

        def __init__(self, default=None, **filter_pairs):
            """
            Constructor

            IN:
                default - default code to apply to all filters
                    (Default: None)
                **filter_pairs - filter=val args to use. invalid filters are
                    ignored.
                    See FILTERS dict. Example:
                        day=None
                        night="0"
            """
            self.map = MASFilterMap.clean_flt_pairs(default, filter_pairs)
            store.mas_sprites.MFM_CACHE[hash(self)] = self

        def __eq__(self, other):
            """
            Equals implementation.
            MASFilterMaps are equal based on their internal tuple/hash var
            """
            if isinstance(self, other.__class__):
                return hash(self) == hash(other)
            return False

        def __hash__(self):
            """
            Hashable implementation.
            MASFilterMaps are uniqued based on their internal map
            """
            return MASFilterMap.flt_hash(self.map)

        def __ne__(self, other):
            """
            Not equals implmentation.
            MASFilterMaps are not equal based on their internal tuple/hash var
            """
            return not self.__eq__(other)

        def get(self, flt, defval=None):
            """
            Gets value from map based on filter

            IN:
                flt - filter to lookup
                defval - default value to reutrn if filter not found
                    (Default: None)

            RETURNS: value for given filter
            """
            return self.map.get(flt, defval)

        def unique_values(self):
            """
            Gets all unique non-None values in this filter map

            RETURNS: list of all non-NOne and unique values in this filter
                map
            """
            vals = []
            for key in self.map:
                if self.map[key] not in vals:
                    vals.append(self.map[key])

            return vals

        @staticmethod
        def cachecreate(default=None, **filter_pairs):
            """
            Creates a MASFilterMap object ONLY if it is not in the filtermap
            cache.

            IN:
                default - See constructor for MASFilterMap
                **filter_pairs - See constructor for MASFilterMap

            RETURNS: MASFilterMap object to use
            """
            hash_value = MASFilterMap.flt_hash(MASFilterMap.clean_flt_pairs(
                default,
                filter_pairs
            ))

            if hash_value in store.mas_sprites.MFM_CACHE:
                return store.mas_sprites.MFM_CACHE[hash_value]

            # otherwise generate the MFM. It will be added to teh cache in
            #  the constructor
            return MASFilterMap(default=default, **filter_pairs)

        @staticmethod
        def clean_flt_pairs(default, filter_pairs):
            """
            cleans given filter pairs, setting defaults and only using valid
            filter keys.

            IN:
                default - default code to apply to all filters
                filter_pairs - filter pair dict:
                    key: filter as string
                    value: code to use as string

            RETURNS: dict with cleaned filter pairs
            """
            output = {}
            
            # cehck existing filter keys and apply defaults
            for flt in store.mas_sprites.FILTERS:
                output[flt] = filter_pairs.get(flt, default)

            return output

        @staticmethod
        def flt_hash(flt_pairs):
            """
            Generates a hash based on the given filter pairs

            IN:
                flt_pairs - dict of the following format:
                    key: filter as string
                    value: code to use as string
                    NOTE: default is assumed to already been set

            RETURNS: hash that would be generated by a MASFilterMAp created 
                with the given filter pairs
            """
            # hash a tuple of this filtermap's map's values, using None for
            # empty spaces
            return hash(tuple([
                flt_pairs.get(flt, None)
                for flt in store.mas_sprites.FILTERS
            ]))

        @classmethod
        def fromJSON(cls, json_obj, msg_log, ind_lvl):
            """
            Builds a MASFilterMap given a JSON format of it

            IN:
                json_obj - JSOn object to parse
                ind_lvl - indent lvl

            OUT:
                msg_log - list to add messages to

            RETURNS: MASFilterMap object build using the JSON, or None if
                failed
            """
            return None
            # TODO:


    def mas_drawmonika_rk(
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
        Draws monika dynamically, using render keys
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
        acs_bat_list = character.acs.get(MASMonika.BAT_ACS, [])
        acs_mat_list = character.acs.get(MASMonika.MAT_ACS, [])
        acs_mab_list = character.acs.get(MASMonika.MAB_ACS, [])
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

        # generate sprite displayable
        sprite = store.mas_sprites.MASMonikaRender(
            store.mas_sprites._rk_sitting(
                character.clothes,
                pose_data[3],
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
                acs_bat_list,
                acs_mat_list,
                acs_mab_list,
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
                character.tablechair,
                character.tablechair.has_shadow
            ),
            flt,
            store.mas_sprites.adjust_x,
            store.mas_sprites.adjust_y,
            store.mas_sprites.LOC_W,
            store.mas_sprites.LOC_H
        )

        # finally apply zoom 
        return Transform(sprite, zoom=store.mas_sprites.value_zoom), None


    def mas_drawemptydesk_rk(st, at, character):
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
        rk_list = []

        # decide the filter
        flt = store.mas_sprites._decide_filter()
        
        # now build the chair
        store.mas_sprites._rk_chair(rk_list, character.tablechair, flt)

        # then the able
        store.mas_sprites._rk_table(
            rk_list,
            character.tablechair,
            False,
            flt
        )

        # then the pst acs we got
        store.mas_sprites._rk_accessory_list(
            rk_list,
            acs_pst_list,
            flt,
            "steepling"
        )

        # generate sprite displayable
        sprite = store.mas_sprites.MASMonikaRender(
            rk_list,
            flt,
            store.mas_sprites.adjust_x,
            store.mas_sprites.adjust_y,
            store.mas_sprites.LOC_W,
            store.mas_sprites.LOC_H
        )

        # finally appyl zoom and return
        return Transform(sprite, zoom=store.mas_sprites.value_zoom), None 



