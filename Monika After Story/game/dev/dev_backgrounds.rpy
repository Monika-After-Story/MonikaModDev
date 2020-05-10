# test module for backgrounds

init 100 python:

    def mas_build_mbgfm(
            mn_sr_size,
            mn_sr_d,
            sr_ss_size,
            sr_ss_d,
            ss_mn_size,
            ss_mn_d,
            ml_min,
            ml_max,
            pr_min,
            pr_max,
            mx_min,
            mx_max
    ):
        """
        Generates a MASBackgroundFilterManager using sample number of slice 
        sizes.

        NOTE: verify is NOT called

        IN:
            mn_sr_size - how many slices to use for the mn_sr chunk
            mn_sr_d - passed to the is_day param
            sr_ss_size - how many slices to use for the sr_ss chunk
            sr_ss_d - passed to the is_day param
            ss_mn_size - how many slices to use for the ss_mn chunk
            ss_mn_d - passed to the is_day param
            ml_min - minimum minlength time to use in seconds
                NOTE: if larger than ml_max, ml_max takes precedence
            ml_max - max minlength time to use in seconds
            pr_min - min priority to use (must be 1-10)
                NOTE: if larger than pr_max, pr_max takes precedence
            pr_max - max priority to use (must be 1-10)
            mx_min - minimum maxlength time to use in seconds
                NOTE: if larger than mx_max, mx_max takes precdence
            mx_max - minimum maxlength time to use in seconds

        RETURNS: MASBackgroundFilterManager object with the given settings
        """
        # validate input
        if mn_sr_size < 1:
            mn_sr_size = 1
        if sr_ss_size < 1:
            sr_ss_size = 1
        if ss_mn_size < 1:
            ss_mn_size = 1
        if ml_min > ml_max:
            ml_min = ml_max
        if pr_min > pr_max:
            pr_min = pr_max
        if mx_min > mx_max:
            mx_min = mx_max

        # generate slices
        mn_sr_slices = _mas_build_fake_slices(
            "mn_sr",
            mn_sr_size,
            ml_min,
            ml_max,
            pr_min,
            pr_max,
            mx_min,
            mx_max
        )
        sr_ss_slices = _mas_build_fake_slices(
            "sr_ss",
            sr_ss_size,
            ml_min,
            ml_max,
            pr_min,
            pr_max,
            mx_min,
            mx_max
        )
        ss_mn_slices = _mas_build_fake_slices(
            "ss_mn",
            ss_mn_size,
            ml_min,
            ml_max,
            pr_min,
            pr_max,
            mx_min,
            mx_max
        )

        # now build the filter manager + chunks
        return MASBackgroundFilterManager(

            # mn_sr
            MASBackgroundFilterChunk(
                bool(mn_sr_d),
                None,
                *mn_sr_slices
            ),

            # sr_ss
            MASBackgroundFilterChunk(
                bool(sr_ss_d),
                None,
                *sr_ss_slices
            ),

            # ss_mn
            MASBackgroundFilterChunk(
                bool(ss_mn_d),
                None,
                *ss_mn_slices
            )
        )


    def _mas_build_fake_slices(
            flt_pfx,
            size,
            ml_min,
            ml_max,
            pr_min,
            pr_max,
            mx_min,
            mx_max
    ):
        """
        Builds fake slices with the given size

        NOTE: no sanity checks so dont screw up

        IN:
            flt_pfx - prefix to use for each slice filter
            size - number of slices to make
            ml_min - min minlength time to use in seconds
            ml_max - max minlength time ot use in seconds
            pr_min - min priority to use
            pr_max - max priority to use
            mx_min - min maxlength time to use in seconds
            mx_max - max maxlength time ot use in seconds

        RETURNS: list of created slices. 
        """
        flt_str = flt_pfx + "_{0}"

        # then the other slices
        slices = [
            _mas_build_random_fake_slice(
                flt_str.format(index),
                ml_min,
                ml_max,
                pr_min,
                pr_max,
                mx_min,
                mx_max
            )
            for index in range(size)
        ]

        # pick an unbounded
        ub_index = random.randint(0, len(slices)-1)
        slices[ub_index].maxlength = None

        return slices

    
    def _mas_build_random_fake_slice(
            flt,
            ml_min,
            ml_max,
            pr_min,
            pr_max,
            mx_min,
            mx_max
    ):
        """
        Builds a fake slice with the given filter name and randomized
        minlength and pr based on the given values

        IN:
            flt - filter name to use
            See _mas_build_fake_slices for the other props

        RETURNS: MASBackgroundFilterSlice object
        """
        return MASBackgroundFilterSlice(
            flt,
            random.randint(ml_min, ml_max),
            maxlength=random.randint(mx_min, mx_max),
            priority=random.randint(pr_min, pr_max),
            cache=False
        )


    def mas_qb_mbgfm():
        return mas_build_mbgfm(
            10,
            False,
            20,
            True,
            8,
            False,
            300,
            60*20,
            1,
            10,
            60*30,
            60*40
        )


    def mas_qb_mbgfm_otm():
        return mas_build_mbgfm(
            1,
            False,
            2,
            True,
            50,
            False,
            60*5,
            60*20,
            1,
            10,
            60*30,
            60*40
        )


    def mas_qb_mbgfm_irl():
        """
        once slice for everything except day, which uses a 5 minute sunrise
        and sunset
        """
        return MASBackgroundFilterManager(
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice(
                    "night_0",
                    5*60,
                    priority=10,
                    cache=False
                )
            ),
            MASBackgroundFilterChunk(
                True,
                None,
                MASBackgroundFilterSlice(
                    "sunrise",
                    2*60,
                    5*60,
                    10,
                    cache=False
                ),
                MASBackgroundFilterSlice(
                    "day_0",
                    5*60,
                    priority=9,
                    cache=False
                ),
                MASBackgroundFilterSlice(
                    "sunset",
                    2*60,
                    5*60,
                    10,
                    cache=False
                )
            ),
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice(
                    "night_0",
                    5*60,
                    priority=10,
                    cache=False
                )
            )
        )


    def _mas_qb_alg_test(spread=False):
        """
        Test alg and write output to log

        IN:
            spread - pass True to use expand_sld instead of expand_once
        """
        with open("test.log", "w") as logout:
            logout.write("START ========================\n")
            abc = mas_qb_mbgfm()
            logout.write(str(abc))

            logout.write("\n\nMINFILL =========================\n")
            length = 37800
            abc._mn_sr._length = length
            abc._mn_sr._min_fill(length)
            logout.write(str(abc))

            logout.write("\n\nEXPAND - build dist\n")
            es_count = len(abc._mn_sr._eff_slices)
            diff = length - abc._mn_sr._eff_chunk_min_end()
            inc_amts = [diff / es_count] * es_count
            logout.write("DIST: ")
            logout.write(str(inc_amts))
            logout.write("\n")

            mas_utils.lo_distribute(
                inc_amts,
                diff % es_count,
                reverse=True
            )
            logout.write("LO DIST: ")
            logout.write(str(inc_amts))
            logout.write("\n")

            logout.write("\n\nEXPAND - once\n")
            if spread:
                c_off = 0
                for index in range(len(abc._mn_sr._eff_slices)):
                    new_off = abc._mn_sr._expand_sld(index, inc_amts, c_off)
                    logout.write("{0} -> {1} | {2}\n".format(
                        c_off,
                        new_off,
                        inc_amts
                    ))
                    c_off = new_off

            else: 
                abc._mn_sr._expand_once(inc_amts)
            logout.write(str(abc))

            logout.write("\n\nDIST: ")
            logout.write(str(inc_amts))
            logout.write("\nFZ DIST: ")
            mas_utils.fz_distribute(inc_amts)
            logout.write(str(inc_amts))
            logout.write("\n")

            logout.write("\n\nEXPAND - twice\n")
            if spread:
                c_off = 0
                for index in range(len(abc._mn_sr._eff_slices)):
                    new_off = abc._mn_sr._expand_sld(index, inc_amts, c_off)
                    logout.write("{0} -> {1} | {2}\n".format(
                        c_off,
                        new_off,
                        inc_amts
                    ))
                    c_off = new_off

            else: 
                abc._mn_sr._expand_once(inc_amts)
            logout.write(str(abc))

            logout.write("\n\nDIST: ")
            logout.write(str(inc_amts))
            logout.write("\nFZ DIST: ")
            mas_utils.fz_distribute(inc_amts)
            logout.write(str(inc_amts))
            logout.write("\n")

            logout.flush()


    def _mas_qb_fast_a(abc):
        """
        Pass in a mbgfm, unbuilt
        """
        import traceback
        with open("test.log", "w") as logout:
            try:
                abc.build(persistent._mas_sunrise * 60, persistent._mas_sunset * 60)
            except Exception as e:
                traceback.print_exc(file=logout)
                logout.write("\n\n\n")
            logout.write(str(abc))
            logout.flush()


    def _mas_qb_fast():
        """
        Makes somethign and writes it out
        """
        import traceback
        with open("test.log", "w") as logout:
            abc = mas_qb_mbgfm()
            try:
                abc.build(persistent._mas_sunrise * 60, persistent._mas_sunset * 60)
            except Exception as e:
                traceback.print_exc(file=logout)
                logout.write("\n\n\n")
            logout.write(str(abc))
            logout.flush()




