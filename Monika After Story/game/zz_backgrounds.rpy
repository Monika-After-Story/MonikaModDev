#Here's where we store our background data
default persistent._mas_background_MBGdata = {}

#START: Class definition
init -10 python:

    class MASBackgroundFilterTypeException(Exception):
        """
        Type exception for MASBackgroundFilter objects
        """

        def __init__(self, obj, mbf_type):
            """
            Constructor

            IN:
                obj - object that was not what we expected
                mbf_type - type we expected
            """
            self.msg = "{0} is not of {1}".format(obj, mbf_type)

        def __str__(self):
            """
            String
            """
            return self.msg


    class MASBackgroundFilterSliceDuplicateException(Exception):
        """
        Exception for when a Background fitler slice is in both a day chunk
        and a night chunk.
        """

        def __init__(self, flt):
            """
            Constructor

            IN:
                flt - the filter name of the offending fitler slice.
            """
            self.msg = "filter '{0}' found in both day chunk and night chunk".format(flt)

        def __str__(self):
            return self.msg


    class MASBackgroundFilterSlice(object):
        """
        Represntation of a filter for a MASBackground.
        this is related to the sprite filters, but gives each filter extra
        oomph. 

        BG filters are designed to be flexible to work with BGs.
        See the MASBackgroundFilterChunk for more info on how this works.

        PROPERTIES:
            name - the name of this filter. This should be a filter ENUM.
                NOTE: this not checked until init level 0
            minlength - the amount of time in seconds that this filter must
                be able to be used for it to be shown. If the filter cannot be
                shown for this amount of time, it will not be shown at all.
            priority - the priority of this filter object. Larger number means
                higher priority. Lower priority means filter will be removed
                first.
            flt - the filter (imagematrix) objects to use. OPTIONAL.
                if this is None, it is assumed the filter data is handled
                elsewhere.
        """
        cache = {}
        # internal cache of MASBackgroundFilterSlice objects to avoid
        #   building duplicates.

        def __init__(self,
                name,
                minlength,
                priority=1,
                flt=None,
                cache=True
        ):
            """
            Constructor

            IN:
                name - name of the filter. This is NOT checked against filter
                    ENUMS until init level 0.
                minlength - amount of time in seconds that this filter must
                    be at least shown for.
                priority - priority of this filter object. Larger number means
                    higher priority.
                    Must be between 1 and 10, inclusive.
                    Defaults to 10 if invalid.
                    (Default: 10)
                flt - imagemanip/matrix compatible filter to use. 
                    only pass in if you wish to use the `add_to_filters` 
                    function
                    (Default: None)
                cache - pass False to not cache this object.
                    Only for debug purposes
                    (Default: True)
            """
            self.name = name
            self.minlength = minlength
            self.flt = flt

            if 1 <= priority <= 10:
                self.priority = priority
            else:
                self.priority = 10

            if cache:
                # store in cache
                self.cache[hash(self)] = self

        def __eq__(self, other):
            """
            EQ implementation.
            Based on hash
            """
            if isinstance(self, other.__class__):
                return hash(self) == hash(other)
            return False

        def __hash__(self):
            """
            Hash implementation. FilterSlices are unique based on name,
            minlength and priority
            """
            return MASBackgroundFilterSlice.gen_hash(
                self.name,
                self.minlength,
                self.priority
            )

        def __ne__(self, other):
            """
            Not equals implementation
            """
            return not self.__eq__(other)

        def __str__(self):
            """
            Slice as string
            """
            return "M: {1:>6}|N: {0} |P: {2}".format(
                self.name,
                self.minlength,
                self.priority
            )

        def add_to_filters(self):
            """
            Adds this filter to the filters dict. Wil fail and log if used
            after init level -1.
            Only works if self.flt is not None.
            """
            if self.flt is not None:
                store.mas_sprites.add_filter(self.name, self.flt)

        @classmethod
        def cachecreate(cls, name, minlength, priority=10, flt=None):
            """
            Builds a MASBackgroundFilterSlice unless we have one in cache

            IN:
                See Constructor

            RETURNS: MASBackgroundFilterSlice object
            """
            hash_key = cls.gen_hash(name, minlength, priority)
            if hash_key in cls.cache:
                return cls.cache[hash_key]

            return MASBackgroundFilterSlice(
                name,
                minlength,
                priority=priority,
                flt=flt
            )

        def can_fit(self, seconds):
            """
            Checks if this filter can fit in the time allotted

            IN:
                seconds - number of seconds to check

            RETURNS: True if this filter can fit in the given number of seconds
                FAlse if not
            """
            return self.minlength <= seconds

        def can_fit_td(self, td):
            """
            Checks if the filter can fit in the time allotted

            IN:
                td - timedelta object to check

            RETURNS: True if this filter can fit in the given timedelta,
                False if not
            """
            return self.minlength <= int(td.total_seconds())

        @staticmethod
        def gen_hash(name, minlength, priority):
            """
            Generates a hash of the components of a MASBackgroundFilterSlice

            IN:
                name - name to use
                minlength - minlength to use
                priority - priority to use

            RETURNS: hash of the object that would be created with the given
                properties.
            """
            return hash("-".join((name, minlength, priority)))

        def verify(self):
            """
            Verifies if this filter's name is a valid filter. Call this
            after init level -1.

            RETURNS: True if filter is valid, False if not
            """
            return store.mas_sprites.is_filter(self.name)


    class MASBackgroundFilterSliceData(object):
        """
        Relates a MASBackgroundFilterSlice to its order and offset

        PROPERTIES:
            offset - the offset associated with this slice
            order - the order associated to this slice
            flt_slice - the slice to associate
        """

        def __init__(self, order, flt_slice):
            """
            Constructor

            IN:
                order - the order for this slice
                flt_slice - the slice to associate with this order
            """
            self.order = order
            self.offset = order
            self.flt_slice = flt_slice

        def __gt__(self, other):
            """
            Greater than uses order
            """
            if isinstance(other, MASBackgroundFilterSliceData):
                return self.order > other.order
            return NotImplemented

        def __lt__(self, other):
            """
            Less than uses order
            """
            if isinstance(other, MASBackgroundFilterSliceData):
                return self.order < other.order
            return NotImplemented

        def __str__(self):
            """
            strings are offset + order + name
            """
            return "{0:>5}|ORD: {1} |{2}".format(
                self.offset,
                self.order,
                self.flt_slice
            )

        def eff_minlength(self):
            """
            Calculates the ending offset assuming min length

            RETURNS: offset + minlength
            """
            return self.offset + self.flt_slice.minlength

        @staticmethod
        def highest_priority(sl_data_list):
            """
            Finds the MASBackgroundFilterSliceData with the highest priority
            and returns its index

            IN:
                sl_data_list - list containig MASBackgroundFilterSliceData
                    objects to check

            RETURNS: index of the MASBackgroundFilterSliceData with the
                highest priority
            """
            h_priority = 0
            h_index = 0
            for index in range(len(sl_data_list)):
                if sl_data_list[index].flt_slice.priority > h_priority:
                    h_priority = sl_data_list[index].flt_slice.priority
                    h_index = index

            return h_index

        @staticmethod
        def lowest_priority(sl_data_list):
            """
            Finds the MASBackgroundFilterSliceData with the lowest priority
            and returns its index

            IN:
                sl_data_list - list containing MASBackgroundFilterSliceData
                    objects to check

            RETURNS: index of the MASBackgroundFilterSliceData with the 
                lowest priority
            """
            l_priority = 10
            l_index = 0
            for index in range(len(sl_data_list)):
                if sl_data_list[index].flt_slice.priority < l_priority:
                    l_priority = sl_data_list[index].flt_slice.priority
                    l_index = index

            return l_index

        @staticmethod
        def sk(obj):
            """
            order sort key
            """
            return obj.order

        @staticmethod
        def sko(obj):
            """
            offset sort key
            """
            return obj.offset


    class MASBackgroundFilterChunk(object):
        """
        Chunk of filters for backgrounds.

        A BG filter chunk is a set of slices that represent a progression
        of filters througout the time range. The slices are handled in a way
        where they are intelligently picked depending on suntimes. This allows
        for handling of cases where there isn't enough time for each slice to
        exist.

        Each slice is a MASBackgroundFilterSlice object. The minlength property
        is used to determine if the object canfit in its allocated time slice.
        Priorities are used to determine the slices to keep. By default we
        try to keep every slice we can. Minlength is also used to determine
        when to swap filters.

        Slices are organized by an order. The order value determines the 
        desired order of slices.
        The base slice is the initial filter to show for a chunk, and will
        always take priority over any other slice.

        Code can be ran during a filter change by passing in function to 
        appropriate param. Any exceptions are caught and loggged.

        PROPERTIES:
            is_day - True if this is a day chunk, False if not
        """

        def __init__(self, is_day, base_slice, pp, *slices):
            """
            Constructor

            IN:
                is_day - True if this is a "Day" chunk. False if not
                base_slice - the initial filter slice to use.
                    This defaults to the highest priority.
                pp - progpoint to run on a filter change (or slice change)
                    the following args are passed to the progpoint:
                        flt_old - the outgoing filter 
                        flt_new - the incoming filter 
                        curr_time - the current time
                    pass None to not use a progpoint
                *slices - slice arguments. Each item should be a 
                    MASBackgroundFilterSlice object
            """
            if not isinstance(base_slice, MASBackgroundFilterSlice):
                raise MASBackgroundFilterTypeException(
                    base_slice,
                    MASBackgroundFilterSlice
                )

            self.is_day = is_day

            self._base_slice = base_slice
            # base filter

            self._slices = []
            # MASBackgroundFilterSliceData objects in standard order

            self._eff_slices = []
            # MASBackgroundFilterSliceData objects that we are actually
            # using in standard order

            self._pp = pp
            # progpoint

            self._index = 0
            # the index in eff_slices of the last filter change

            self._length = 0
            # the last length value passed into build

            self._parse_slices(slices)

        def __str__(self):
            """
            Shows effective slice information
            """
            output = [
                "Current Slice: {0}".format(self._index),
                "Total Length: {0}".format(self._length),
                "Slices:",
            ]

            # calc effective size of base slice
            if len(self._eff_slices) > 0:
                es = self._eff_slices[0].offset
            else:
                es = ""

            # string base slice
            output.append("ES: {0:>5}|    0| BASE |{1}".format(
                es,
                self._base_slice
            ))

            # string other slices
            for index in range(len(self._eff_slices)):

                # determine appropriate end time for eff size
                if index < len(self._eff_slices)-1:
                    endl = self._eff_slices[index+1].offset
                else:
                    endl = self._length

                # string slice
                sl_data = self._eff_slices[index]
                output.append("ES: {0:>5}|{1}".format(
                    endl - sl_data.offset,
                    sl_data
                ))

            return "\n".join(output)

        def _adjust_offset(self, index, amt):
            """
            Adjust offset of all eff_slices, starting from the given index.

            IN:
                index - index to start adjusting offsets.
                amt - amount to add to offsets. can be negative to
                    subtract.
            """
            for sl_data in self._eff_slices[index:]:
                sl_data.offset += amt

        def build(self, length):
            """
            Builds the effective slices array using the given length as
            guidance.

            slices are built in a greedy fashion starting from 0, respecting
            priorities and etc.

            IN:
                length - the amount of seconds this chunk encompasses
            """
            self._length = length

            if len(self._slices) < 1:
                # dont do anything if we dont even have any slices to do
                return

            # always start with the minimum length expansion alg
            leftovers = self._min_fill(length)

            if len(leftovers) > 0:
                # if we have leftovers, then use complex alg
                self._priority_fill(length, leftovers)

            # lastly, expand to fill voids
            self._expand(length)

        def _eff_chunk_min_end(self):
            """
            Gets the minimal chunk end length.

            RETURNS: last eff_slice's eff_offset + its minlength
            """
            if len(self._eff_slices) > 0:
                return self._eff_slices[-1].eff_minlength()

            # if no slices at all, then just the base slice works
            return self._base_slice.minlength

        def _expand(self, length):
            """
            Expands all slices in effective slices until it fills the given 
            length

            IN:
                length - the amount of length we need to fill
            """
            es_count = 1 + len(self._eff_slices)
            diff = length - self._eff_chunk_min_end()

            # make a list of inc amounts for easy looping
            inc_amts = [diff / es_count] * es_count

            # now calculate any leftover amounts and reverse add them
            leftovers = diff % es_count
            index = es_count - 1
            while leftovers > 0 and index >= 0:
                inc_amts[index] += 1
                leftovers -= 1
                index -= 1

            # and lastly, apply each inc amount
            # start by figuring the base slice new length
            st_off = self._base_slice.minlength + inc_amts[0]
            for index in range(es_count-1):
                sl_data = self._eff_slices[index]

                # the new length is always the next slice's start
                sl_data.offset = st_off

                # calculate new length
                st_off += sl_data.flt_slice.minlength + inc_amts[index+1]
            
        def filters(self):
            """
            RETURNS: list of all the filters associatd with this filter chunk
                (list of strings)
                NOTE: does not contain duplicates.
            """
            # use a dict so we only return each filter once
            filters = {}
            for sl_data in self._slices:
                filters[sl_data.flt_slice.name] = None
            filters[self._base_slice.name] = None

            return filters.keys()

        def _min_fill(self, length):
            """
            Fills the effective slices using minlength logic.

            IN:
                length - the length we are filling
            
            RETURNS: leftovers - contains slices that we could not fit. Could 
                be empty if we managed to fit all slices.
            """
            built_length = 0
            index = 0

            # always start with the base
            built_length = self._base_slice.minlength
            self._eff_slices = []

            # add slices
            while built_length < length and index < len(self._slices):
                # retrieve slice info for this index
                curr_sl_data = self._slices[index]

                # add the slice
                curr_sl_data.offset = built_length
                self._eff_slices.append(curr_sl_data)

                # increment built length
                built_length += curr_sl_data.flt_slice.minlength
                index += 1

            if built_length < length:
                # we managed to fit every slice! 
                return []

            # otherwise, we have a leftover slice in some way
            last_sl_data = self._eff_slices.pop()

            # and add any remaining slices
            return [last_sl_data] + self._slices[index:]

        def _parse_slices(self, slices):
            """
            Parses the slices data
            """
            # verify slices
            if len(slices) < 1:
                # no slice data. that is ok
                return

            for index in range(len(slices)):
                bg_flt = slices[index]

                # check slice
                if not isinstance(bg_flt, MASBackgroundFilterSlice):
                    raise MASBackgroundFilterTypeException(
                        base_slice,
                        MASBackgroundFilterSlice
                    )

                # add to slices
                store.mas_utils.insert_sort(
                    self._slices,
                    MASBackgroundFilterSliceData(index, bg_flt),
                    MASBackgroundFilterSliceData.sk
                )

        def _pf_insert(self, index, sl_data):
            """
            Inserts a filter slice offset into the effective slices list 
            based on a starting index.

            IN:
                index - starting index
                sl_data - the slice data to insert
            """
            # get current slice and how long it is
            rm_len = self._eff_slices[index].flt_slice.minlength

            # looop, finding the right place for the sl_off
            while (
                    index < len(self._eff_slices)
                    and self._eff_slices[index] < sl_off
            ):
                self._eff_slices[index].offset -= rm_len
                index += 1

            # we must have the correct location now
            # determine the offset to use
            sl_data.offset = self._eff_slices[index-1].eff_minlength()
            self._eff_slices.insert(index, sl_data)

            # now adjust offsets for all remaining sl datas
            self._adjust_offset(index + 1, sl_data.flt_slice.minlength)

        def _priority_fill(self, length, leftovers):
            """
            Fills the effective slices using priority logic.
            This assumes the eff slices has been filled with minimal logic

            IN:
                length - the amount of length we need to fill
                leftovers - slices that have not been added yet
            """
            # Gist:
            #   1. reverse through the eff_slices, removing elements with
            #       lower priorities than leftovers, and adding high priority
            #       elements from leftovers.
            #   2. stop upon reaching the first slice.

            # highest priority in leftovers
            hpsl_data = leftovers.pop(
                MASBackgroundFilterSliceData.highest_priority(leftovers)
            )

            for es_index in range(len(self._eff_slices)-1, -1, -1):
               
                # get current slice
                csl_data = self._eff_slices[es_index]

                if csl_data.flt_slice.priority < hpsl_data.flt_slice.priority:
                    # current has a lower priority

                    # add the higher priority item
                    self._pf_insert(es_index, hpsl_data)

                    # remove the lower priority item, and store in leftovers
                    leftovers.insert(0, self._eff_slices.pop(es_index))

                    # then clean up the offsets
                    self._adjust_offset(
                        es_index + 1,
                        csl_data.flt_slice.min_length
                    )

                    # and find newest high leftover priority
                    hpsl_data = leftovers.pop(
                        MASBackgroundFilterSliceData.highest_priority(
                            leftovers
                        )
                    )

            # clean up if our current min length is too large
            while (
                    len(self._eff_slices) > 0
                    and self._eff_chunk_min_end() > length
            ):
                # obtain lowest priority filter slice offset object and remove
                llop_index = MASBackgroundFilterSliceData.lowest_priority(
                    self._eff_slices
                )
                lpsl_data = self._eff_slices.pop(llop_index)

                # fix eff offsets
                self._adjust_offset(llop_index, lpsl_data.flt_slice.minlength)

        def verify(self):
            """
            Verifies the filters in this filter Chunk
            Assumed to be called at least at init level 0
            Filters should all exist.

            Exceptions are raised if a bad filter is found.
            """
            for sl_data in self._slices:
                flt_slice = sl_data.flt_slice
                if not flt_slice.verify():
                    raise MASInvalidFilterException(flt_slice.name)


    class MASBackgroundFilterManager(object):
        """
        Filter Management class for backgrounds.

        The BG filter system slices a day into 3 chunks.
        these chunks correspond to the suntimes system.
        MidNight to SunRise (MN - SR)
        SunRise to SunSet (SR - SS)
        SunSet to MidNignt (SS - MN)

        Each chunk is marked day/night, and is used when determining if a 
        filter is day or night. This means two separate chunks with different
        day/night settings can NOT contain same filters. If you need the same
        filter content to be considerd day AND night, make two separate filter
        enums. This is to avoid ambiguities.

        PROPERTIES:
            None
        """

        def __init__(self, mn_sr, sr_ss, ss_mn, pp=None):
            """
            Constructor

            IN:
                mn_sr - MASBackgroundFilterChunk for midnight to sunrise
                sr_ss - MASBackgroundFilterChunk for sunrise to sunset
                ss_mn - MASBackgroundFilterChunk for sunset to midnight
                pp - progpoint to run on a chunk change
                    the following args ar epassed to the progpoint:
                        chunk_old - the outgoing chunk
                        chunk_new - the incoming chunk
                        curr_time - the current time
                    (Default: None)
            """
            if not isinstance(mn_sr, MASBackgroundFilterChunk):
                raise MASBackgroundFilterTypeException(
                    mn_sr,
                    MASBackgroundFilterChunk
                )
            if not isinstance(sr_ss, MASBackgroundFilterChunk):
                raise MASBackgroundFilterTypeException(
                    sr_ss,
                    MASBackgroundFilterChunk
                )
            if not isinstance(ss_mn, MASBackgroundFilterChunk):
                raise MASBackgroundFilterTypeException(
                    ss_mn,
                    MASBackgroundFilterChunk
                )

            self._mn_sr = mn_sr
            # midnight to sunrise

            self._sr_ss = sr_ss
            # sunrise to sunset

            self._ss_mn = ss_mn
            # sunset to midnight

            self._chunks = [self._mn_sr, self._sr_ss, self._ss_mn]
            # ordered chunks for easier swapping

            self._pp = pp
            # progpoint

            self._day_filters = {}
            self._night_filters = {}
            # organized filter dicts
            # key: name of filter
            # value: Ignored
            # NOTE: organized in verify.

            self._chunk_index = 0
            # the index in _chunks of the current chunk

        def __str__(self):
            """
            Shows chunks and curr chunk information
            """
            output = []
            
            # mn to sr chunk
            chunk_name = "Midnight to Sunrise"
            if self._chunk_index == 0:
                chunk_name += "| CURRENT CHUNK"
            output.append(chunk_name)
            output.append(str(self._mn_sr))

            # sr to ss chunk
            chunk_name = "Sunrise to Sunset"
            if self._chunk_index == 1:
                chunk_name += "| CURRENT CHUNK"
            output.append("")
            output.append(chunk_name)
            output.append(str(self._sr_ss))

            # ss to mn chunk
            chunk_name = "Sunset to Midnight"
            if self._chunk_index == 2:
                chunk_name += "| CURRENT CHUNK"
            output.append("")
            output.append(chunk_name)
            output.append(str(self._ss_mn))

            return "\n".join(output)

        def build(self, sunrise, sunset):
            """
            Builds each chunk with the given sunrise and sunset values.

            IN:
                sunrise - sunrise time in number of seconds from midnight
                sunset - sunset time in number of seconds from midnight
            """
            self._mn_sr.build(sunrise)
            self._sr_ss.build(sunset - sunrise)
            self._ss_mn.build((3600 * 24) - sunset)

        def filters(self):
            """
            RETURNS: list of all filters associated with this filter manager
                (list of strings)
                NOTE: does not contain duplicates.
            """
            both = {}
            both.update(self._day_filters)
            both.update(self._night_filters)
            return both.keys()

        def filters_day(self):
            """
            RETURNS: list of all day filters associated with this filter
                manager.
                (list of stirngs)
                NOTE: does not contain duplicates
            """
            return self._day_filters.keys()

        def filters_night(self):
            """
            RETURNS: list of all night filters associated with this filter
                manager.
                (list of strings)
                NOTE: does not contain duplicates
            """
            return self._night_filters.keys()

        def _organize(self):
            """
            Organize filters into day and night dicts
            """
            self._organize_chunk(self._mn_sr)
            self._organize_chunk(self._sr_ss)
            self._organize_chunk(self._ss_mn)

        def _organize_chunk(self, chunk):
            """
            Organizes a single chunk into the day and night dicts

            IN:
                chunk - MASBackgroundFilterChunk to organize
            """
            if chunk.is_day:
                flt_d = self._day_filters
            else:
                flt_d = self._night_filters

            for flt in chunk.filters():
                flt_d[flt] = None

        def verify(self):
            """
            Verifies the filters in this filter manager.
            Assumed to be called at least at init level 0
            Filters cannot be in both day and night chunks. If this happens,
            an exception will be raised.
           
            We also verify filters in each chunk here.
            """
            # first organize filters into day and night
            self._organize()

            # now compare the lists
            for day_flt in self._day_filters:
                if day_flt in self._night_filters:
                    raise MASBackgroundFilterSliceDuplicateException(day_flt)

            # now verify each chunk
            self._mn_sr.verify()
            self._sr_ss.verify()
            self._ss_mn.verify()


    # TODO: the background class needs to decide the filters to use.
    #   *AS WELL AS THE PROGRESSION*
    # TODO: move the current DAY/NIGHT filters from mas_sprites to here.
    # NOTE: I will do this when adding sunset progression
    class MASBackground(object):
        """
        Background class to get display props for bgs

        PROPERTIES:
            background_id - the id which defines this bg
            prompt - button label for the bg
            image_map - Dict mapping all images for the bgs, keys are precip types (See MASWeather)
            hide_calendar - whether or not we display the calendar with this
            hide_masks - whether or not we display the window masks
            disable_progressive - weather or not we disable progesssive weather
            unlocked - whether or not this background is unlocked
            entry_pp - entry programming points for bgs
            exit_pp - exit programming points
            filters - mapping of filters associated with this BG
        """
        import store.mas_background as mas_background
        import store.mas_weather as mas_weather

        def __init__(
            self,
            background_id,
            prompt,
            image_day,
            image_night,
            image_rain_day=None,
            image_rain_night=None,
            image_overcast_day=None,
            image_overcast_night=None,
            image_snow_day=None,
            image_snow_night=None,
            hide_calendar=False,
            hide_masks=False,
            disable_progressive=None,
            unlocked=False,
            entry_pp=None,
            exit_pp=None,
        ):
            """
            Constructor for background objects

            IN:
                background_id:
                    id that defines the background object
                    NOTE: Must be unique

                prompt:
                    button label for this bg

                image_day:
                    the renpy.image object we use for this bg during the day
                    NOTE: Mandatory

                image_night:
                    the renpy.image object we use for this bg during the night
                    NOTE: Mandatory

                image_rain_day:
                    the image tag we use for the background while it's raining (day)
                    (Default: None, not required)

                image_rain_night:
                    the image tag we use for the background while it's raining (night)
                    (Default: None, not required)

                image_overcast_day:
                    the image tag we use for the background while it's overcast (day)
                    (Default: None, not required)

                image_overcast_night:
                    the image tag we use for the background while it's overcast (night)
                    (Default: None, not required)

                image_snow_day:
                    the image tag we use for the background while it's snowing (day)
                    (Default: None, not required)

                image_snow_night:
                    the image tag we use for the background while it's snowing (night)
                    (Default: None, not required)

                hide_calendar:
                    whether or not we want to display the calendar
                    (Default: False)

                hide_masks:
                    weather or not we want to show the windows
                    (Default: False)

                disable_progressive:
                    weather or not we want to disable progressive weather
                    (Default: None, if hide masks is true and this is not provided, we assume True, otherwise False)

                unlocked:
                    whether or not this background starts unlocked
                    (Default: False)

                entry_pp:
                    Entry programming point for the background
                    (Default: None)

                exit_pp:
                    Exit programming point for this background
                    (Default: None)
            """

            if background_id in self.mas_background.BACKGROUND_MAP:
                raise Exception("duplicate background ID")

            self.background_id = background_id
            self.prompt = prompt
            self.image_day = image_day
            self.image_night = image_night


            self.image_map = {
                #Def
                mas_weather.PRECIP_TYPE_DEF: (image_day, image_night),
                #Rain
                mas_weather.PRECIP_TYPE_RAIN: (image_rain_day if image_rain_day else image_day, image_rain_night if image_rain_night else image_night),
                #Overcast
                mas_weather.PRECIP_TYPE_OVERCAST: (image_overcast_day if image_overcast_day else image_day, image_overcast_night if image_overcast_night else image_night),
                #Snow
                mas_weather.PRECIP_TYPE_SNOW: (image_snow_day if image_snow_day else image_day, image_snow_night if image_snow_night else image_night)
            }

            #Then the other props
            self.hide_calendar = hide_calendar
            self.hide_masks = hide_masks

            #Progressive handling
            if disable_progressive is None:
                self.disable_progressive = hide_masks
            else:
                self.disable_progressive = disable_progressive

            self.unlocked = unlocked
            self.entry_pp = entry_pp
            self.exit_pp = exit_pp

            # add to background map
            self.mas_background.BACKGROUND_MAP[background_id] = self


        def __eq__(self, other):
            if isinstance(other, MASBackground):
                return self.background_id == other.background_id
            return NotImplemented


        def __ne__(self, other):
            result = self.__eq__(other)
            if result is NotImplemented:
                return result
            return not result


        def entry(self, old_background):
            """
            Run the entry programming point
            """
            if self.entry_pp is not None:
                self.entry_pp(old_background)


        def exit(self, new_background):
            """
            Run the exit programming point
            """
            if self.exit_pp is not None:
                self.exit_pp(new_background)


        def fromTuple(self, data_tuple):
            """
            Loads data from tuple

            IN:
                data_tuple - tuple of the following format:
                    [0]: unlocked property
            """
            self.unlocked = data_tuple[0]


        def toTuple(self):
            """
            Converts this MASWeather object into a tuple

            RETURNS: tuple of the following format:
                [0]: unlocked property
            """
            return (self.unlocked,)

        def getDayRoom(self, weather=None):
            """
            Returns the day masks to use given the conditions/availablity of present assets
            """
            if weather is None:
                weather = store.mas_current_weather

            return self.image_map[weather.precip_type][0]

        def getNightRoom(self, weather=None):
            """
            Returns the night masks to use given the conditions/availablity of present assets
            """
            if weather is None:
                weather = store.mas_current_weather

            return self.image_map[weather.precip_type][1]

        def getRoomForTime(self, weather=None):
            """
            Gets the room for the current time

            IN:
                weather - get the room bg for the time and weather
                (Default: current weather)
            """
            if weather is None:
                weather = store.mas_current_weather
            if store.mas_isMorning():
                return self.getDayRoom(weather)
            return self.getNightRoom(weather)

        def isChangingRoom(self, old_weather, new_weather):
            """
            If the room has a different look for the new weather we're going into, the room is "changing" and we need to flag this to
            scene change and dissolve the spaceroom in the spaceroom label
            """
            return self.getRoomForTime(old_weather) != self.getRoomForTime(new_weather)

        def isFltDay(self, flt=None):
            """
            Checks if the given filter is considered a "day" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "day" filter according to this bg
            """
            # TODO: a BG will be in charge of which filters are "day" and
            #   which are "night". This will be implemented in the future.
            #   for now we just assume "day" is day and "night" is night
            if flt is None:
                flt = store.mas_sprites.get_filter()

            return flt == store.mas_sprites.FLT_DAY

        def isFltNight(self, flt=None):
            """
            Checks if the given filter is considered a "night" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "night" filter according to this BG
            """
            # TODO: see isFltDay
            return not self.isFltDay(flt)


#Helper methods and such
init -20 python in mas_background:
    import store
    BACKGROUND_MAP = {}
    BACKGROUND_RETURN = "Nevermind"

    def loadMBGData():
        """
        Loads persistent MASBackground data into the weather map

        ASSUMES: background map is already filled
        """
        if store.persistent._mas_background_MBGdata is None:
            return

        for mbg_id, mbg_data in store.persistent._mas_background_MBGdata.iteritems():
            mbg_obj = BACKGROUND_MAP.get(mbg_id, None)
            if mbg_obj is not None:
                mbg_obj.fromTuple(mbg_data)

    def saveMBGData():
        """
        Saves MASBackground data from weather map into persistent
        """
        for mbg_id, mbg_obj in BACKGROUND_MAP.iteritems():
            store.persistent._mas_background_MBGdata[mbg_id] = mbg_obj.toTuple()

    def getUnlockedBGCount():
        """
        Gets the number of unlocked backgrounds
        """
        unlocked_count = 0
        for mbg_obj in BACKGROUND_MAP.itervalues():
            unlocked_count += int(mbg_obj.unlocked)

        return unlocked_count

#START: BG change functions
init 800 python:

    def mas_setBackground(_background):
        """
        Sets the initial bg

        NOTE: We don't handle exit pp's here

        IN:
            _background:
                The background we're changing to
        """
        global mas_current_background
        old_background = mas_current_background
        mas_current_background = _background
        mas_current_background.entry(old_background)

    def mas_changeBackground(new_background, by_user=None):
        """
        changes the background w/o any scene changes

        IN:
            new_background:
                The background we're changing to

            by_user:
                If the user switched the background themselves
        """
        if by_user is not None:
            mas_background.force_background = bool(by_user)

        mas_current_background.exit(new_background)
        mas_setBackground(new_background)

    #Just set us to the normal room here
    mas_current_background = None
    mas_setBackground(mas_background_def)

    #Make sure the bg selector is only available with at least 2 bgs unlocked
    if mas_background.getUnlockedBGCount() < 2:
        mas_lockEVL("monika_change_background","EVE")

#START: Programming points
init -2 python in mas_background:
    import store

    def _def_background_entry(_old):
        """
        Entry programming point for befault background
        """
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

    def _def_background_exit(_new):
        """
        Exit programming point for befault background
        """
        store.mas_lockEVL("mas_monika_islands", "EVE")


#START: bg defs
init -1 python:
    #Default spaceroom
    mas_background_def = MASBackground(
        #Identification
        "spaceroom",
        "Spaceroom",

        #Day/Night
        "monika_day_room",
        "monika_room",

        #Rain Day/Night
        image_rain_day="monika_rain_room",

        image_overcast_day="monika_rain_room",

        image_snow_day="monika_snow_room_day",
        image_snow_night="monika_snow_room_night",

        #Def room should always be unlocked
        unlocked=True,

        #Programming points for the spaceroom
        entry_pp=store.mas_background._def_background_entry,
        exit_pp=store.mas_background._def_background_exit
    )


#START: Image definitions
#Spaceroom
image monika_day_room = "mod_assets/location/spaceroom/spaceroom.png"
image monika_room = "mod_assets/location/spaceroom/spaceroom-n.png"
#Thanks Orca
image monika_rain_room = "mod_assets/location/spaceroom/spaceroom_rain.png"
#Thanks Velius/Orca
image monika_snow_room_day = "mod_assets/location/spaceroom/spaceroom_snow.png"
image monika_snow_room_night = "mod_assets/location/spaceroom/spaceroom_snow-n.png"

#TODO: locking/unlocking of this based on other backgrounds
#START: Location Selector
#init 5 python:
#    # available only if moni affection is affectionate+
#    addEvent(
#        Event(
#            persistent.event_database,
#            eventlabel="monika_change_background",
#            category=["location"],
#            prompt="Can we go somewhere else?",
#            pool=True,
#            unlocked=False,
#            rules={"no unlock": None},
#            aff_range=(mas_aff.AFFECTIONATE, None)
#        )
#    )

label monika_change_background:

    m 1hua "Sure!"

label monika_change_background_loop:

    show monika 1eua at t21

    $ renpy.say(m, "Where would you like to go?", interact=False)

    python:
        # build menu list
        import store.mas_background as mas_background
        import store.mas_moods as mas_moods

        # we assume that we will always have more than 1
        # default should always be at the top
        backgrounds = [(mas_background_def.prompt, mas_background_def, False, False)]

        # build other backgrounds list
        other_backgrounds = [
            (mbg_obj.prompt, mbg_obj, False, False)
            for mbg_id, mbg_obj in mas_background.BACKGROUND_MAP.iteritems()
            if mbg_id != "spaceroom" and mbg_obj.unlocked
        ]

        # sort other backgrounds list
        other_backgrounds.sort()

        # build full list
        backgrounds.extend(other_backgrounds)

        # now add final quit item
        final_item = (mas_background.BACKGROUND_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(backgrounds, mas_ui.SCROLLABLE_MENU_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

    $ sel_background = _return

    show monika at t11

    # return value False? then return
    if sel_background is False:
        m 1eka "Oh, alright."
        m "If you want to go somewhere, just ask, okay?"
        return

    if sel_background == mas_current_background:
        m 1hua "We're here right now, silly."
        m "Try again~"
        jump monika_change_background_loop

    call mas_background_change(sel_background)
    return

#Generic background changing label, can be used if we wanted a sort of story related change
label mas_background_change(new_bg, skip_leadin=False, skip_outro=False):
    # otherwise, we can change the background now
    if not skip_leadin:
        m 1eua "Alright!"
        m 1hua "Let's go, [player]!"

    #Little transition
    hide monika
    scene black
    with dissolve
    pause 2.0

    # finally change the background
    $ mas_changeBackground(new_bg)

    #If we've disabled progressive and hidden masks, then we shouldn't allow weather change
    if new_bg.disable_progressive and new_bg.hide_masks:
        $ mas_weather.temp_weather_storage = mas_current_weather
        $ mas_changeWeather(mas_weather_def)
        $ mas_lockEVL("monika_change_weather", "EVE")

    else:
        if mas_weather.temp_weather_storage is not None:
            $ mas_changeWeather(mas_weather.temp_weather_storage)

        else:
            #If we don't have tempstor, run the startup weather
            $ set_to_weather = mas_shouldRain()
            if set_to_weather is not None:
                $ mas_changeWeather(set_to_weather)
            else:
                $ mas_changeWeather(mas_weather_def)

        #Then we unlock the weather sel here
        $ mas_unlockEVL("monika_change_weather", "EVE")

    call spaceroom(scene_change=True, dissolve_all=True)

    if not skip_outro:
        m 1eua "Here we are!"
        m "Let me know if you want to go somewhere else, okay?"
    return
