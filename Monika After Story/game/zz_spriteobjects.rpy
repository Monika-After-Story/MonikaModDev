# All Sprite objects belong here
#
# For documentation on classes, see sprite-chart
#
# quicklinks:
#   [SPR010] - Hair programming points
#   [SPR020] - Clothes programming points
#   [SPR030] - ACS programming points
#   [SPR110] - Hair sprite objects
#   [SPR120] - Clothes sprite objects
#   [SPR130] - ACS sprite objects
#   [SPR230] - ACS variables

init -2 python in mas_sprites:
    # all progrmaming points should go here
    # organize by type then id
    # ASSUME all programming points only run at runtime
    import store

    temp_storage = dict()
    # all programming points have access to this storage var.
    # use names + an identifier as keys so you wont collide
    # NOTE: this will NOT be maintained on a restart

    ######### HAIR [SPR010] ###########
    # available kwargs:
    #   entry:
    #       prev_hair - previously worn hair
    #   exit:
    #       new_hair - hair that is to be worn

    def _hair_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for ponytail
        """
        # wear a ribbon, we do this always to enforce monika's ribbon as a
        # separate acs.
        if not _moni_chr.is_wearing_acs_type("ribbon"):
            _last_ribbon = temp_storage.get(
                "hair.ribbon",
                store.mas_acs_ribbon_def
            )
            _moni_chr.wear_acs(_last_ribbon)

        #Unlock the selector for ribbons since you now have more than one (if you only had def before)
        if len(store.mas_selspr.filter_acs(True, group="ribbon")) > 1:
            store.mas_unlockEVL("monika_ribbon_select", "EVE")


    def _hair_def_exit(_moni_chr, **kwargs):
        """
        Exit programming point for ponytail
        """
        pass


    def _hair_down_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair down
        """
        # if wearing a ribbon, take it off
        # NOTE: we save the ribbon in temp storage as a courtesy
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        if prev_ribbon is not None:
            if prev_ribbon != store.mas_acs_ribbon_blank:
                temp_storage["hair.ribbon" ] = prev_ribbon
            _moni_chr.remove_acs(prev_ribbon)

        # lock ribbon select
        store.mas_lockEVL("monika_ribbon_select", "EVE")


    def _hair_down_exit(_moni_chr, **kwargs):
        """
        Exit programming point for hair down
        """
        pass


    def _hair_bun_entry(_moni_chr, **kwargs):
        """
        Entry programming point for hair bun
        """
        # wear a ribbon, we do this always to enforce monika's ribbon as a
        # separate acs.
        if not _moni_chr.is_wearing_acs_type("ribbon"):
            _last_ribbon = temp_storage.get(
                "hair.ribbon",
                store.mas_acs_ribbon_def
            )
            _moni_chr.wear_acs(_last_ribbon)

        #Unlock the selector for ribbons since you now have more than one (if you only had def before)
        if len(store.mas_selspr.filter_acs(True, group="ribbon")) > 1:
            store.mas_unlockEVL("monika_ribbon_select", "EVE")


    ######### CLOTHES [SPR020] ###########
    # available kwargs:
    #   entry:
    #       prev_clothes - prevoiusly worn clothes
    #   exit:
    #       new_clothes - clothes that are to be worn

    def _clothes_def_entry(_moni_chr, **kwargs):
        """
        Entry programming point for def clothes
        """
        pass
        # TODO: need to add ex prop checking and more
        # so we can rmeove bare acs

    def _clothes_rin_entry(_moni_chr, **kwargs):
        """
        Entry programming point for rin clothes
        """
        # TODO: handle other promise ring types
        temp_storage["clothes.rin"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2=None,
            p3="1",
            p4=None,
            p5="5old",
            p6=None
        )

        # hide hair down select
        store.mas_lockEVL("monika_hair_select", "EVE")

        # hide hairdown greeting
#        store.mas_lockEVL("greeting_hairdown", "GRE")

        # wearing rin clothes means we wear custom blank ribbon if we are
        # wearing a ribbon
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        if (
                prev_ribbon is not None 
                and prev_ribbon != store.mas_acs_ribbon_blank
            ):
            temp_storage["hair.ribbon"] = prev_ribbon
            _moni_chr.wear_acs(store.mas_acs_ribbon_blank)

        # lock hair so we dont get ribbon issues
        _moni_chr.lock_hair = True

        # lock ribbon select
        store.mas_lockEVL("monika_ribbon_select", "EVE")

        # remove ear rose
        _moni_chr.remove_acs(store.mas_acs_ear_rose)

        # TODO: need to add ex prop checking and more
        # so we can rmeove bare acs


    def _clothes_rin_exit(_moni_chr, **kwargs):
        """
        Exit programming point for rin clothes
        """
        rin_map = temp_storage.get("clothes.rin", None)
        if rin_map is not None:
            store.mas_acs_promisering.pose_map = rin_map

        # unlock hair down select, if needed
        if len(store.mas_selspr.filter_hair(True)) > 1:
            store.mas_unlockEVL("monika_hair_select", "EVE")

        # unlock hair down greeting if not unlocked
#        if not store.mas_SELisUnlocked(mas_hair_down, 1):
#            store.mase_unlockEVL("greeting_hairdown", "GRE")
        
        # wear previous ribbon if we are wearing blank ribbon
        # NOTE: we are gauanteed to be wearing blank ribbon when wearing
        # these clothes. Regardless, we should always restore to what we
        # have previously saved.
        if _moni_chr.is_wearing_acs_type("ribbon"):
            _last_ribbon = temp_storage.get(
                "hair.ribbon",
                store.mas_acs_ribbon_def
            )
            _moni_chr.wear_acs(_last_ribbon)

        # unlock hair
        _moni_chr.lock_hair = False

        #Unlock the selector for ribbons since you now have more than one (if you only had def before)
        if len(store.mas_selspr.filter_acs(True, group="ribbon")) > 1:
            store.mas_unlockEVL("monika_ribbon_select", "EVE")


    def _clothes_marisa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for marisa clothes
        """
        # TODO: handle other promise ring types
        temp_storage["clothes.marisa"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2="6",
            p3="1",
            p4=None,
            p5=None,
            p6=None
        )

        # hide hair down select
        store.mas_lockEVL("monika_hair_select", "EVE")

        # hide hairdown greeting
#        store.mas_lockEVL("greeting_hairdown", "GRE")

        # wearing marisa clothes means we wear custom blank ribbon if we are
        # wearing a ribbon
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        if (
                prev_ribbon is not None 
                and prev_ribbon != store.mas_acs_ribbon_blank
            ):
            temp_storage["hair.ribbon"] = prev_ribbon
            _moni_chr.wear_acs(store.mas_acs_ribbon_blank)

        # lock hair so we dont get ribbon issues
        _moni_chr.lock_hair = True

        # lock ribbon select
        store.mas_lockEVL("monika_ribbon_select", "EVE")

        # remove ear rose
        _moni_chr.remove_acs(store.mas_acs_ear_rose)

        # TODO: need to add ex prop checking and more
        # so we can rmeove bare acs


    def _clothes_marisa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for marisa clothes
        """
        marisa_map = temp_storage.get("clothes.marisa", None)
        if marisa_map is not None:
            store.mas_acs_promisering.pose_map = marisa_map

        # unlock hair down select, if needed
        if len(store.mas_selspr.filter_hair(True)) > 1:
            store.mas_unlockEVL("monika_hair_select", "EVE")

        # unlock hair down greeting if not unlocked
#        if not store.mas_SELisUnlocked(mas_hair_down, 1):
#            store.mase_unlockEVL("greeting_hairdown", "GRE")

        # wear previous ribbon if we are wearing blank ribbon
        if _moni_chr.is_wearing_acs_type("ribbon"):
            _last_ribbon = temp_storage.get(
                "hair.ribbon",
                store.mas_acs_ribbon_def
            )
            _moni_chr.wear_acs(_last_ribbon)

        # unlock hair
        _moni_chr.lock_hair = False

        #Unlock the selector for ribbons since you now have more than one (if you only had def before)
        if len(store.mas_selspr.filter_acs(True, group="ribbon")) > 1:
            store.mas_unlockEVL("monika_ribbon_select", "EVE")


    def _clothes_santa_entry(_moni_chr, **kwargs):
        """
        Entry programming point for santa clothes
        """
        # TODO: handle other promise ring types
        temp_storage["clothes.santa"] = store.mas_acs_promisering.pose_map
        store.mas_acs_promisering.pose_map = store.MASPoseMap(
            p1=None,
            p2="7",
            p3="1",
            p4=None,
            p5=None,
            p6=None
        )

        # wearing a ribbon? switch to the wine ribbon always
        prev_ribbon = _moni_chr.get_acs_of_type("ribbon")
        if prev_ribbon is not None:
            if prev_ribbon != store.mas_acs_ribbon_blank:
                temp_storage["hair.ribbon"] = prev_ribbon
            _moni_chr.wear_acs(store.mas_acs_ribbon_wine)

        # NOTE: revaluate if this looks bad on santa
        # remove ear rose
        _moni_chr.remove_acs(store.mas_acs_ear_rose)


    def _clothes_santa_exit(_moni_chr, **kwargs):
        """
        Exit programming point for santa clothes
        """
        santa_map = temp_storage.get("clothes.santa", None)
        if santa_map is not None:
            store.mas_acs_promisering.pose_map = santa_map

        # go back to previous ribbon if wearing wine ribbon
        if _moni_chr.is_wearing_acs(store.mas_acs_ribbon_wine):
            _last_ribbon = temp_storage.get(
                "hair.ribbon",
                store.mas_acs_ribbon_def
            )
            _moni_chr.wear_acs(_last_ribbon)

        # TODO: need to add ex prop checking and more
        # so we can rmeove bare acs


    def _clothes_sundress_white_entry(_moni_chr, **kwargs):
        """
        Entry programming point for sundress white
        """
        _moni_chr.wear_acs(store.mas_acs_hairties_bracelet_brown)
        _moni_chr.wear_acs(store.mas_acs_musicnote_necklace_gold)


    def _clothes_sundress_white_exit(_moni_chr, **kwargs):
        """
        Exit programming point for sundress white
        """
        # TODO: dont remve the bracelet.
        #   non-bare arms clothes should remove the bracelet
        _moni_chr.remove_acs(store.mas_acs_hairties_bracelet_brown)
        _moni_chr.remove_acs(store.mas_acs_musicnote_necklace_gold)


    ######### ACS [SPR030] ###########
    # available kwargs:
    #   NONE

    def _acs_quetzalplushie_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie acs
        """
        #We need to unlock/random monika_plushie since the plush is active
        store.mas_showEVL('monika_plushie','EVE',_random=True)

    def _acs_quetzalplushie_exit(_moni_chr, **kwargs):
        """
        Exit programming point for quetzal plushie acs
        """
        # remove the santa hat if we are removing the plushie
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_santahat)

        # also remove antlers
        _moni_chr.remove_acs(store.mas_acs_quetzalplushie_antlers)

        #Since no more plush, we need to lock/derandom monika_plushie
        store.mas_hideEVL('monika_plushie','EVE',derandom=True)

    def _acs_quetzalplushie_santahat_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie santa hat acs
        """
        # need to wear the quetzal plushie if we putting the santa hat on
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_quetzalplushie_antlers_entry(_moni_chr, **kwargs):
        """
        Entry programming point for quetzal plushie antlers acs
        """
        # need to wear the quetzal plushie if we putting the antlers on
        _moni_chr.wear_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_entry(_moni_chr, **kwargs):
        """
        Entry programming point for heartchoc acs
        """
        #We only want to be temporarily moving the plush if not on f14
        #Since we keep the chocs post reaction if it is f14

        # TODO: might need to make a center version of santa hat
        #   or just make heartchoc not giftable during d25

        if not (store.mas_isF14() or store.mas_isD25Season()):
            if _moni_chr.is_wearing_acs(store.mas_acs_quetzalplushie):
                _moni_chr.wear_acs(store.mas_acs_center_quetzalplushie)

        else:
            _moni_chr.remove_acs(store.mas_acs_quetzalplushie)


    def _acs_heartchoc_exit(_moni_chr, **kwargs):
        """
        Exit programming point for heartchoc acs
        """
        if _moni_chr.is_wearing_acs(store.mas_acs_center_quetzalplushie):
            _moni_chr.wear_acs(store.mas_acs_quetzalplushie)



init -1 python:
    # HAIR (SPR110)
    # Hairs are representations of image objects with propertes
    #
    # NAMING:
    # mas_hair_<hair name>
    #
    # <hair name> MUST BE UNIQUE
    #
    # NOTE: see the existing standards for hair file naming
    # NOTE: PoseMaps are used to determin which lean types exist for
    #   a given hair type, NOT filenames
    #
    # NOTE: the fallback system:
    #   by setting fallback to True, you can use the fallback system to
    #   make poses fallback to a different pose. NOTE: non-lean types CANNOT
    #   fallback to a lean type. Lean types can fallback to anything.
    #
    #   When using the fallback system, map poses to the pose/lean types
    #   that you want to fallback on.
    #   AKA: to make pose 2 fallback to steepling, do `p2="steepling"`
    #   To make everything fallback to steepling, do `default="steepling"`
    #   This means that steepling MUST exist for the fallback system to work
    #   perfectly.
    #
    # NOTE: template:
    ### HUMAN UNDERSTANDABLE NAME OF HAIR STYLE
    ## hairidentifiername
    # General description of the hair style

    ### PONYTAIL WITH RIBBON (default)
    ## def
    # Monika's default hairstyle, aka the ponytail
    # thanks Ryuse/Iron707/Taross/Metisz/Tri/JMO
    mas_hair_def = MASHair(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        entry_pp=store.mas_sprites._hair_def_entry,
        exit_pp=store.mas_sprites._hair_def_exit,
        ex_props={
            "ribbon": True
        }
    )
    store.mas_sprites.init_hair(mas_hair_def)
    store.mas_selspr.init_selectable_hair(
        mas_hair_def,
        "Ponytail",
        "ponytail",
        "hair",
        select_dlg=[
            "Do you like my ribbon, [player]?"
        ]
    )
    store.mas_selspr.unlock_hair(mas_hair_def)

    ### DOWN
    ## down
    # Hair is down, not tied up
    # thanks Ryuse/Finale/Iron707/Taross/Metisz/Tri/JMO
    mas_hair_down = MASHair(
        "down",
        "down",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        entry_pp=store.mas_sprites._hair_down_entry,
        exit_pp=store.mas_sprites._hair_down_exit,
#        split=False
    )
    store.mas_sprites.init_hair(mas_hair_down)
    store.mas_selspr.init_selectable_hair(
        mas_hair_down,
        "Down",
        "down",
        "hair",
        select_dlg=[
            "Feels nice to let my hair down..."
        ]
    )

    ### BUN WITH RIBBON
    ## bun
    # Hair tied into a bun, using the ribbon
    # thanks Ryuse/Iron707/Taross
    mas_hair_bun = MASHair(
        "bun",
        "bun",
        MASPoseMap(
            default=True,
            p5=False
        ),
        entry_pp=store.mas_sprites._hair_bun_entry,
        ex_props={
            "ribbon": True
        }
#        split=False
    )
    store.mas_sprites.init_hair(mas_hair_bun)

    ### CUSTOM
    ## custom
    # Not a real hair object. If an outfit uses this, it's assumed that the
    # actual clothes have the hair baked into them.
    mas_hair_custom = MASHair(
        "custom",
        "custom",
        MASPoseMap(),

        # NOTE: custom disables hair splitting.
        split=MASPoseMap(
            default=False,
            use_reg_for_l=True
        ),
    )
    store.mas_sprites.init_hair(mas_hair_custom)


init -1 python:
    # THIS MUST BE AFTER THE HAIR SECTION
    # CLOTHES (SPR120)
    # Clothes are representations of image objects with properties
    #
    # NAMING:
    # mas_clothes_<clothes name>
    #
    # <clothes name> MUST BE UNIQUE
    #
    # NOTE: see the existing standards for clothes file naming
    # NOTE: PoseMaps are used to determine which lean types exist for
    #  a given clothes type, NOT filenames
    #
    # NOTE: see IMG015 for info about the fallback system
    #
    # NOTE: template
    ### HUMAN UNDERSTANDABLE NAME OF THIS CLOTHES
    ## clothesidentifiername
    # General description of the clothes

    ### SCHOOL UNIFORM (default)
    ## def
    # Monika's school uniform
    # thanks Ryuse/Velius94 (Jacket)
    mas_clothes_def = MASClothes(
        "def",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_def_entry,
    )
    store.mas_sprites.init_clothes(mas_clothes_def)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_def,
        "School Uniform",
        "schooluniform",
        "clothes",
        visible_when_locked=True,
        hover_dlg=None,
        select_dlg=[
            "Ready for school!"
        ]
    )
    store.mas_selspr.unlock_clothes(mas_clothes_def)

    ### MARISA COSTUME
    ## marisa
    # Witch costume based on Marisa
    # thanks SovietSpartan
    mas_clothes_marisa = MASClothes(
        "marisa",
        "def",
        MASPoseMap(
            p1="steepling",
            p2="crossed",
            p3="restleftpointright",
            p4="pointright",
            p6="down"
        ),
        fallback=True,
        hair_map={
            "all": "custom"
        },
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_marisa_entry,
        exit_pp=store.mas_sprites._clothes_marisa_exit,
        ex_props={
            "forced hair": True
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_marisa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_marisa,
        "Witch Costume",
        "marisa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Just an ordinary costume, ~ze."
        ]
    )


    ### RIN COSTUME
    ## rin
    # Neko costume based on Rin
    # thanks SovietSpartan
    mas_clothes_rin = MASClothes(
        "rin",
        "def",
        MASPoseMap(
            p1="steepling",
            p2="crossed",
            p3="restleftpointright",
            p4="pointright",
            p6="down"
        ),
        fallback=True,
        hair_map={
            "all": "custom"
        },
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_rin_entry,
        exit_pp=store.mas_sprites._clothes_rin_exit,
        ex_props={
            "forced hair": True
        }
    )
    store.mas_sprites.init_clothes(mas_clothes_rin)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_rin,
        "Neko Costume",
        "rin",
        "clothes",
        visible_when_locked=False,
        hover_dlg=[
            "~nya?",
            "n-nya..."
        ],
        select_dlg=[
            "Nya!"
        ]
    )

    ### SANTA MONIKA
    ## santa
    # Monika with Santa costume
    # thanks Ryuse
    mas_clothes_santa = MASClothes(
        "santa",
        "def",
        # NOTE: this is disabled until santa is using new leaning
#        MASPoseMap(
#            default=True,
#            use_reg_for_l=True
#        ),
        MASPoseMap(
            p1="steepling",
            p2="crossed",
            p3="restleftpointright",
            p4="pointright",
            p6="down"
        ),
        fallback=True,
        hair_map={
            "bun": "def"
        },
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_santa_entry,
        exit_pp=store.mas_sprites._clothes_santa_exit
    )
    store.mas_sprites.init_clothes(mas_clothes_santa)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_santa,
        "Santa Costume",
        "santa",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Merry Christmas!",
            "What kind of {i}presents{/i} do you want?",
            "Happy holidays!"
        ]
    )

    ### SUNDRESS (WHITE)
    ## sundress_white
    # The casual outfit from vday
    # thanks @EntonyEscX
    mas_clothes_sundress_white = MASClothes(
        "sundress_white",
        "def",
        MASPoseMap(
            default=True,
            use_reg_for_l=True,
        ),
        stay_on_start=True,
        entry_pp=store.mas_sprites._clothes_sundress_white_entry,
        exit_pp=store.mas_sprites._clothes_sundress_white_exit,
    )
    store.mas_sprites.init_clothes(mas_clothes_sundress_white)
    store.mas_selspr.init_selectable_clothes(
        mas_clothes_sundress_white,
        "Sundress (White)",
        "sundress_white",
        "clothes",
        visible_when_locked=False,
        hover_dlg=None,
        select_dlg=[
            "Are we going anywhere special today, [player]?",
            "I've always loved this outfit...",
        ],
    )


init -1 python:
    # ACCESSORIES (SPR130)
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
    # acs name - name of the accessory (shoud be unique)
    # pose id - identifier to map this image to a pose (should be unique
    #       per accessory)
    #
    # NOTE: pleaes preface each accessory with the following commen template
    # this is to ensure we hvae an accurate description of what each accessory
    # is:
    ### HUMAN UNDERSTANDABLE NAME OF ACCESSORY
    ## accessoryidentifiername
    # General description of what the object is, where it is located

    # TODO: this should be sorted by alpha, using the ID
    ### COFFEE MUG
    ## mug
    # Coffee mug that sits on Monika's desk
    # thanks Ryuse/EntonyEscX
    mas_acs_mug = MASAccessory(
        "mug",
        "mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"]
    )
    store.mas_sprites.init_acs(mas_acs_mug)

    ### ROSE EAR ACCESSORY
    ## ear_rose
    # rose that is placed on Monika's ear
    # thanks jmwall
    mas_acs_ear_rose = MASAccessory(
        "ear_rose",
        "ear_rose",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=False,
        rec_layer=MASMonika.PST_ACS,
    )
    store.mas_sprites.init_acs(mas_acs_ear_rose)

    ### HAIRTIES BRACELET (BROWN)
    ## hairties_bracelet_brown
    # The bracelet Monika wore in the vday outfit
    # thanks EntonyEscX
    mas_acs_hairties_bracelet_brown = MASAccessory(
        "hairties_bracelet_brown",
        "hairties_bracelet_brown",
        MASPoseMap(
            p1="1",
            p2="2",
            p3="1",
            p4="4",
            p5="5",
            p6=None
        ),
        stay_on_start=True,
        acs_type="wrist-bracelet",
        mux_type=["wrist-bracelet"],
        ex_props={
            "bare wrist": True,
        }
    )
    store.mas_sprites.init_acs(mas_acs_hairties_bracelet_brown)

    ### HEART-SHAPED DESK CHOCOLATES
    ## heartchoc
    # heart-shaped chocolate box to be placed on Monika's desk
    # NOTE: anyone remember who made these?
    mas_acs_heartchoc = MASAccessory(
        "heartchoc",
        "heartchoc",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="chocs",
        #Can't mux this since this has special handling via programming points
        entry_pp=store.mas_sprites._acs_heartchoc_entry,
        exit_pp=store.mas_sprites._acs_heartchoc_exit
    )
    store.mas_sprites.init_acs(mas_acs_heartchoc)

    ### HOT CHOCOLATE MUG
    ## hotchoc_mug
    # Coffee mug that sits on Monika's desk
    # thanks Ryuse/EntonyEscX
    mas_acs_hotchoc_mug = MASAccessory(
        "hotchoc_mug",
        "hotchoc_mug",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="mug",
        mux_type=["mug"]
    )
    store.mas_sprites.init_acs(mas_acs_hotchoc_mug)

    ### MUSIC NOTE NECKLACE (GOLD)
    ## musicnote_necklace_gold
    # The necklace Monika wore in the vday outfit
    # thanks EntonyEscX
    mas_acs_musicnote_necklace_gold = MASAccessory(
        "musicnote_necklace_gold",
        "musicnote_necklace_gold",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="necklace",
        mux_type=["necklace"],
        ex_props={
            "bare collar": True,
        },
        rec_layer=MASMonika.BFH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_musicnote_necklace_gold)

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
        stay_on_start=True,
        acs_type="ring",
        ex_props={
            "bare hands": True
        }
    )
    store.mas_sprites.init_acs(mas_acs_promisering)

    ### QUETZAL PLUSHIE
    ## quetzalplushie
    # Quetzal plushie that sits on Monika's desk
    # thanks aldo
    mas_acs_quetzalplushie = MASAccessory(
        "quetzalplushie",
        "quetzalplushie",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_q",

        # NOTE: this shouldn't be muxed with heart choc as heart choc 
        #   needs to add mid version of this
        mux_type=["plush_mid"],
        entry_pp=store.mas_sprites._acs_quetzalplushie_entry,
        exit_pp=store.mas_sprites._acs_quetzalplushie_exit
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie)

    ### QUETZAL PLUSHIE ANTLERS
    ## quetzalplushie_antlers
    # Antlers for the Quetzal Plushie
    # Thanks Finale
    mas_acs_quetzalplushie_antlers = MASAccessory(
        "quetzalplushie_antlers",
        "quetzalplushie_antlers",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=12,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_antlers_entry
    )

    ### QUETZAL PLUSHIE (CENTER)
    ## quetzalplushie_mid
    # version of the plushie that is on the center of the desk
    mas_acs_center_quetzalplushie = MASAccessory(
        "quetzalplushie_mid",
        "quetzalplushie_mid",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=False,
        acs_type="plush_mid",
        mux_type=["plush_q"],
    )
    store.mas_sprites.init_acs(mas_acs_center_quetzalplushie)

    ### QUETZAL PLUSHIE SANTA HAT
    ## quetzalplushie_santahat
    # Santa hat for the Quetzal Plushie
    # Thanks Finale
    mas_acs_quetzalplushie_santahat = MASAccessory(
        "quetzalplushie_santahat",
        "quetzalplushie_santahat",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        entry_pp=store.mas_sprites._acs_quetzalplushie_santahat_entry
    )
    store.mas_sprites.init_acs(mas_acs_quetzalplushie_santahat)

    ### BLACK RIBBON
    ## ribbon_black
    # Black ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_black = MASAccessory(
        "ribbon_black",
        "ribbon_black",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_black)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_black,
        "Ribbon (Black)",
        "ribbon_black",
        "ribbon",
        hover_dlg=[
            "That's pretty formal, [player]."
        ],
        select_dlg=[
            "Are we going somewhere special, [player]?"
        ]
    )

    ### BLANK RIBBON
    ## ribbon_blank
    # Blank ribbon for use in ponytail/bun with custom outfits
    mas_acs_ribbon_blank = MASAccessory(
        "ribbon_blank",
        "ribbon_blank",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blank)

    ### BLUE RIBBON
    ## ribbon_blue
    # Blue ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_blue = MASAccessory(
        "ribbon_blue",
        "ribbon_blue",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_blue)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_blue,
        "Ribbon (Blue)",
        "ribbon_blue",
        "ribbon",
        hover_dlg=[
            "Like the ocean..."
        ],
        select_dlg=[
            "Great choice, [player]!"
        ]
    )

    ### DARK PURPLE RIBBON
    ## ribbon_dark_purple
    # Dark purple ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_darkpurple = MASAccessory(
        "ribbon_dark_purple",
        "ribbon_dark_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_darkpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_darkpurple,
        "Ribbon (Dark Purple)",
        "ribbon_dark_purple",
        "ribbon",
        hover_dlg=[
            "I love that color!"
        ],
        select_dlg=[
            "Lavender is a nice change of pace."
        ]
    )

    ### EMERALED RIBBON
    ## ribbon_emeraled
    # Emerald ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_emerald = MASAccessory(
        "ribbon_emerald",
        "ribbon_emerald",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_emerald)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_emerald,
        "Ribbon (Emerald)",
        "ribbon_emerald",
        "ribbon",
        hover_dlg=[
            "I've always loved this color...",
        ],
        select_dlg=[
            "It's just like my eyes!"
        ]
    )

    ### WHITE RIBBON
    ## ribbon_def
    # White ribbon (the default) for ponytail/bun hairstyles
    mas_acs_ribbon_def = MASAccessory(
        "ribbon_def",
        "ribbon_def",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_def)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_def,
        "Ribbon (White)",
        "ribbon_def",
        "ribbon",
        hover_dlg=[
            "Do you miss my old ribbon, [player]?"
        ],
        select_dlg=[
            "Back to the classics!"
        ]
    )

    ### GRAY RIBBON
    ## ribbon_gray
    # Gray ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_gray = MASAccessory(
        "ribbon_gray",
        "ribbon_gray",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_gray)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_gray,
        "Ribbon (Gray)",
        "ribbon_gray",
        "ribbon",
        hover_dlg=[
            "Like a warm, rainy day..."
        ],
        select_dlg=[
            "That's a really unique color, [player]."
        ]
    )

    ### GREEN RIBBON
    ## ribbon_green
    # Green ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_green = MASAccessory(
        "ribbon_green",
        "ribbon_green",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_green)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_green,
        "Ribbon (Green)",
        "ribbon_green",
        "ribbon",
        hover_dlg=[
            "That's a lovely color!"
        ],
        select_dlg=[
            "Green, just like my eyes!"
        ]
    )

    ### LIGHT PURPLE RIBBON
    ## ribbon_light_purple
    # Light purple ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_lightpurple = MASAccessory(
        "ribbon_light_purple",
        "ribbon_light_purple",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_lightpurple)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_lightpurple,
        "Ribbon (Light Purple)",
        "ribbon_light_purple",
        "ribbon",
        hover_dlg=[
            "This purple looks pretty nice, right [player]?"
        ],
        select_dlg=[
            "Really has a spring feel to it."
        ]
    )

    ### PEACH RIBBON
    ## ribbon_peach
    # Peach ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_peach = MASAccessory(
        "ribbon_peach",
        "ribbon_peach",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_peach)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_peach,
        "Ribbon (Peach)",
        "ribbon_peach",
        "ribbon",
        hover_dlg=[
            "That's beautiful!"
        ],
        select_dlg=[
            "Just like autumn leaves..."
        ]
    )

    ### PINK RIBBON
    ## ribbon_pink
    # Pink ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_pink = MASAccessory(
        "ribbon_pink",
        "ribbon_pink",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_pink)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_pink,
        "Ribbon (Pink)",
        "ribbon_pink",
        "ribbon",
        hover_dlg=[
            "Looks cute, right?"
        ],
        select_dlg=[
            "Good choice!"
        ]
    )

    ### PLATINUM RIBBON
    ## ribbon_platinum
    # Platinum ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_platinum = MASAccessory(
        "ribbon_platinum",
        "ribbon_platinum",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_platinum)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_platinum,
        "Ribbon (Platinum)",
        "ribbon_platinum",
        "ribbon",
        hover_dlg=[
            "That's an interesting color, [player].",
        ],
        select_dlg=[
            "I'm quite fond of it, actually."
        ]
    )

    ### RED RIBBON
    ## ribbon_red
    # Red ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_red = MASAccessory(
        "ribbon_red",
        "ribbon_red",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_red)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_red,
        "Ribbon (Red)",
        "ribbon_red",
        "ribbon",
        hover_dlg=[
            "Red is a beautiful color!"
        ],
        select_dlg=[
            "Just like roses~"
        ]
    )

    ### RUBY RIBBON
    ## ribbon_ruby
    # Ruby ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_ruby = MASAccessory(
        "ribbon_ruby",
        "ribbon_ruby",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_ruby)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_ruby,
        "Ribbon (Ruby)",
        "ribbon_ruby",
        "ribbon",
        hover_dlg=[
            "That's a beautiful shade of red."
        ],
        select_dlg=[
            "Doesn't it look pretty?"
        ]
    )

    ### SAPPHIRE RIBBON
    ## ribbon_sapphire
    # Sapphire ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_sapphire = MASAccessory(
        "ribbon_sapphire",
        "ribbon_sapphire",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_sapphire)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_sapphire,
        "Ribbon (Sapphire)",
        "ribbon_sapphire",
        "ribbon",
        hover_dlg=[
            "Like a clear summer sky..."
        ],
        select_dlg=[
            "Nice choice, [player]!"
        ]
    )

    ### SILVER RIBBON
    ## ribbon_silver
    # Silver ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_silver = MASAccessory(
        "ribbon_silver",
        "ribbon_silver",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_silver)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_silver,
        "Ribbon (Silver)",
        "ribbon_silver",
        "ribbon",
        hover_dlg=[
            "I like the look of this one.",
            "I've always loved silver."
        ],
        select_dlg=[
            "Nice choice, [player]."
        ]
    )

    ### TEAL RIBBON
    ## ribbon_teal
    # Teal ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_teal = MASAccessory(
        "ribbon_teal",
        "ribbon_teal",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_teal)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_teal,
        "Ribbon (Teal)",
        "ribbon_teal",
        "ribbon",
        hover_dlg=[
            "Looks really summer-y, right?"
        ],
        select_dlg=[
            "Just like a summer sky."
        ]
    )

    ### WINE RIBBON
    ## ribbon_wine
    # Wine ribbon for ponytail/bun hairstyles. This matches the santa outfit
    # thanks Ryuse/Ronin
    mas_acs_ribbon_wine = MASAccessory(
        "ribbon_wine",
        "ribbon_wine",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_wine)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_wine,
        "Ribbon (Wine)",
        "ribbon_wine",
        "ribbon",
        hover_dlg=[
            "That's a great color!"
        ],
        select_dlg=[
            "Formal! Are you taking me somewhere special, [player]?"
        ]
    )

    ### YELLOW RIBBON
    ## ribbon_yellow
    # Yellow ribbon for ponytail/bun hairstyles
    # thanks Ronin
    mas_acs_ribbon_yellow = MASAccessory(
        "ribbon_yellow",
        "ribbon_yellow",
        MASPoseMap(
            default="0",
            p5="5"
        ),
        stay_on_start=True,
        acs_type="ribbon",
        mux_type=["ribbon"],
        rec_layer=MASMonika.BBH_ACS
    )
    store.mas_sprites.init_acs(mas_acs_ribbon_yellow)
    store.mas_selspr.init_selectable_acs(
        mas_acs_ribbon_yellow,
        "Ribbon (Yellow)",
        "ribbon_yellow",
        "ribbon",
        hover_dlg=[
            "This color reminds me of a nice summer day!"
        ],
        select_dlg=[
            "Great choice, [player]!"
        ]
    )

    ### DESK ROSES
    ## roses
    # roses to be placed on Monika's desk
    # NOTE: who made these?
    mas_acs_roses = MASAccessory(
        "roses",
        "roses",
        MASPoseMap(
            default="0",
            use_reg_for_l=True
        ),
        priority=11,
        stay_on_start=False,
        acs_type="flowers",
    )
    store.mas_sprites.init_acs(mas_acs_roses)

#### ACCCESSORY VARIABLES (SPR230)
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

### HOT CHOCOLATE MUG ###

# NOTE: please use consumable framework when ever that is created
# NOTE: so we dont get dum things, use _mas_c for all future consumable-based
#   calculations. Everything will get replcaed with a more concrete storage
#   system in the future, anyway.

default persistent._mas_acs_enable_hotchoc = False
# True enables hot chocolate, False disables

default persistent._mas_c_hotchoc_been_given = False
# True means the user has given monika hotchoc before, False means no

default persistent._mas_c_hotchoc_brew_time = None
# datetime that hot choco started being made. None if not being made

default persistent._mas_c_hotchoc_cup_done = None
# datetime that monika will finish her hotchoc. MNone means she is not drining

default persistent._mas_c_hotchoc_cups_drank = 0
# number of cups of hotchoc monika has drank

define mas_coffee.HOTCHOC_TIME_START = 19
# hour that hotchoc time begins (inclusive)

define mas_coffee.HOTCHOC_TIME_END = 22
# hour that hotchoc time ends (exclusive)

define mas_coffee.HOTCHOC_BREW_DRINK_SPLIT = 21
# similar to coffee split, but for hotchocolate

### QUETZAL PLUSHIE ###
default persistent._mas_acs_enable_quetzalplushie = False
# True enables plushie, False disables plushie

### PROMISE RING ###
default persistent._mas_acs_enable_promisering = False
# True enables promise ring, False disables promise ring
