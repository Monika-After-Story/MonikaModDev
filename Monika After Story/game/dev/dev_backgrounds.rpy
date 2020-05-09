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

        # generate slices
        mn_sr_slices = _mas_build_fake_slices(
            "mn_sr",
            mn_sr_size,
            ml_min,
            ml_max,
            pr_min,
            pr_max
        )
        sr_ss_slices = _mas_build_fake_slices(
            "sr_ss",
            sr_ss_size,
            ml_min,
            ml_max,
            pr_min,
            pr_max
        )
        ss_mn_slices = _mas_build_fake_slices(
            "ss_mn",
            ss_mn_size,
            ml_min,
            ml_max,
            pr_min,
            pr_max
        )

        # now build the filter manager + chunks
        return MASBackgroundFilterManager(

            # mn_sr
            MASBackgroundFilterChunk(
                bool(mn_sr_d),
                mn_sr_slices.pop(),
                None,
                *mn_sr_slices
            ),

            # sr_ss
            MASBackgroundFilterChunk(
                bool(sr_ss_d),
                sr_ss_slices.pop(),
                None,
                *sr_ss_slices
            ),

            # ss_mn
            MASBackgroundFilterChunk(
                bool(ss_mn_d),
                ss_mn_slices.pop(),
                None,
                *ss_mn_slices
            )
        )


    def _mas_build_fake_slices(flt_pfx, size, ml_min, ml_max, pr_min, pr_max):
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

        RETURNS: list of created slices. Last slice is the base slice
        """
        flt_str = flt_pfx + "_{0}"

        # first generate the base slice
        base_slice = _mas_build_random_fake_slice(
            flt_str.format(0),
            ml_min,
            ml_max,
            pr_min,
            pr_max
        )

        # then the other slices
        slices = [
            _mas_build_random_fake_slice(
                flt_str.format(index + 1),
                ml_min,
                ml_max,
                pr_min,
                pr_max
            )
            for index in range(size-1)
        ]

        slices.append(base_slice)

        return slices

    
    def _mas_build_random_fake_slice(flt, ml_min, ml_max, pr_min, pr_max):
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
            random.randint(pr_min, pr_max),
            cache=False
        )



