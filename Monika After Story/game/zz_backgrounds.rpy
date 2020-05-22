#Here's where we store our background data
default persistent._mas_background_MBGdata = {}

#Store the persistent background
#Defaults to def (spaceroom)
default persistent._mas_current_background = "def"

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
            maxlength - the amount of time in seconds that this filter can
                be shown. The filter will never be shown more than this amt
                of seconds. If None, then max is unbounded.
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
                maxlength=None,
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
                maxlength - amount of time in seconds that this at most can be
                    shown for.
                    if None, max time is unbounded
                    (Default: None)
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
            self.maxlength = maxlength
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
            return "M: {1:>6}|X: {3:>6}|N: {0} |P: {2}".format(
                self.name,
                self.minlength,
                self.priority,
                self.maxlength
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
        def gen_hash(name, minlength, maxlength, priority):
            """
            Generates a hash of the components of a MASBackgroundFilterSlice

            IN:
                name - name to use
                minlength - minlength to use
                maxlength - maxlength to use
                priority - priority to use

            RETURNS: hash of the object that would be created with the given
                properties.
            """
            return hash("-".join((
                name,
                str(minlength),
                str(maxlength),
                priority
            )))

        def is_max(self, value):
            """
            Checks if the given vlaue is larger than max length.
            If this slice is unbounded, this will always return False

            IN:
                value - value to check

            RETURNS: True if the value is larger than maxlength, False if not
            """
            if self.maxlength is None:
                return False

            return value > self.maxlength

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
            length - the length of this slice data
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
            self.length = flt_slice.minlength

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
            return "{0:>5}|ORD: {1} |AL: {3}|{2}".format(
                self.offset,
                self.order,
                self.flt_slice,
                self.length
            )

        def __len__(self):
            """
            Returns length
            """
            return self.length

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
            for index, sl_data in enumerate(sl_data_list):
                if sl_data.flt_slice.priority > h_priority:
                    h_priority = sl_data.flt_slice.priority
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
            for index, sl_data in enumerate(sl_data_list):
                if sl_data.flt_slice.priority < l_priority:
                    l_priority = sl_data.flt_slice.priority
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

        Code can be ran during a filter change by passing in function to 
        appropriate param. Any exceptions are caught and loggged.

        PROPERTIES:
            is_day - True if this is a day chunk, False if not
        """

        def __init__(self, is_day, pp, *slices):
            """
            Constructor

            IN:
                is_day - True if this is a "Day" chunk. False if not
                pp - progpoint to run on a filter change (or slice change)
                    This is ran multiple times if multiple filter changes
                    occur, but NOT at all if a chunk change occurs.
                    the following args are passed to the progpoint:
                        flt_old - the outgoing filter 
                        flt_new - the incoming filter 
                        curr_time - the current time
                    pass None to not use a progpoint
                *slices - slice arguments. Each item should be a 
                    MASBackgroundFilterSlice object.
                    This should be in the desired order.
                    NOTE: there must be at least one slice with unbounded time
            """
            self.is_day = is_day

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

        def __len__(self):
            """
            Length of this chunk
            """
            return self._length

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

            if length < 1:
                # this chunk has no length. clear it out
                self._eff_slices = []
                return

            if len(self._slices) < 2:
                # with only once slice, just set that slice as the
                # main slice
                sl_data = self._slices[0]
                sl_data.length = length
                sl_data.offset = 0
                self._eff_slices = [sl_data]
                return

            # always start with the minimum length expansion alg
            leftovers = self._min_fill(length)

            if len(leftovers) > 0:
                # if we have leftovers, then use complex alg
                self._priority_fill(length, leftovers)

            # set everyones length to minimum
            for sl_data in self._eff_slices:
                sl_data.length = sl_data.flt_slice.minlength

            # lastly, expand to fill voids
            self._expand(length)

        def current(self):
            """
            Gets current filter

            RETURNS: current filter, or None if could not
            """
            if 0 <= self._index < len(self._eff_slices):
                return self._eff_slices[self._index].flt_slice.name
            return None

        def current_pos(self):
            """
            Generates internal information related to current position

            RETURNS: tuple:
                [0] - current slice index
                [1] - beginning offset of the current slice
                [2] - beginning offset of the next slice
                    NOTE: this is -1 if no next slice
            """
            if 0 <= self._index < len(self._eff_slices)-1:
                next_offset = self._eff_slices[self._index+1].offset
            else:
                next_offset = -1

            return (self._index, self._current_sldata().offset, next_offset)

        def _current_sldata(self):
            """
            Gets current slice data

            RETURNS: current slice data 
            """
            return self._eff_slices[self._index]

        def _eff_chunk_min_end(self):
            """
            Gets the minimal chunk end length.

            RETURNS: last eff_slice's eff_offset + its minlength
            """
            return self._eff_slices[-1].eff_minlength()

        def _expand(self, length):
            """
            Expands all slices in effective slices until it fills the given 
            length

            IN:
                length - the amount of length we need to fill
            """
            es_count = len(self._eff_slices)
            diff = length - self._eff_chunk_min_end()

            # make a list of inc amounts for easy looping
            inc_amts = [diff / es_count] * es_count

            # reverse add lefovers
            store.mas_utils.lo_distribute(
                inc_amts,
                diff % es_count,
                reverse=True
            )

            # apply amounts to values until we are out
            while sum(inc_amts) > 0:
                self._expand_once(inc_amts)

                # reform inc_amts so we continue adding leftover amounts to
                # slices that can still be expanded
                leftovers = store.mas_utils.fz_distribute(inc_amts)
                if leftovers > 0:
                    store.mas_utils.lo_distribute(
                        inc_amts,
                        leftovers,
                        reverse=True,
                        nz=True
                    )

        def _expand_once(self, value_list):
            """
            Runs expansion alg. This will add index-based numbers from the
            given value list to effective slice offsets and subtract added amts
            from the given corresponding position in value list.

            IN:
                value_list - list of amounts to add to individual items in 
                    eff_slices

            OUT:
                value_list - leftover amounts to distribute to eff_slices
            """
            # apply inc amounts
            # start by figuring the base new length
            c_off = 0
            for index in range(len(self._eff_slices)):
                c_off = self._expand_sld(index, value_list, c_off)

        def _expand_sld(self, index, value_list, c_off):
            """
            Expands a slicedata item. Also adjusts value list as appropriate

            IN:
                index - position to expand slice data and value list
                value_list - list of amounts to add to individual items in 
                    eff_slices
                c_off - current offset value

            OUT:
                value_list - value at index changed to leftover amounts or 0

            RETURNS: new current offset value
            """
            # get sl data
            sl_data = self._eff_slices[index]

            # the current offset is always this sl data's new start
            sl_data.offset = c_off

            # how long is this slice?
            sl_len = sl_data.length + value_list[index]

            # if too big, adjust
            if sl_data.flt_slice.is_max(sl_len):
                diff = sl_len - sl_data.flt_slice.maxlength
                value_list[index] = diff
                sl_len = sl_data.flt_slice.maxlength
            else:
                value_list[index] = 0

            # and set new length
            sl_data.length = sl_len

            # calculate next offset
            return c_off + sl_len
            
        def filters(self, ordered=False):
            """
            Gets list of filters

            IN:
                ordered - True will return the filters in an ordered list.
                    This may contain duplicates.

            RETURNS: list of all the filters associatd with this filter chunk
                (list of strings)
            """
            if ordered:
                # ordered list
                return [sl_data.flt_slice.name for sl_data in self._slices]

            # otherwise use a dict so we only return each filter once
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
            index = 1
            # start at the 2nd slice as thats where we start adjusting offsets

            # always start with the first slice
            built_length = self._slices[0].flt_slice.minlength
            self._eff_slices = [self._slices[0]]

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
                raise Exception("No slices found")

            has_unbounded = False
            for index, bg_flt in enumerate(slices):

                # check slice
                if not isinstance(bg_flt, MASBackgroundFilterSlice):
                    raise MASBackgroundFilterTypeException(
                        base_slice,
                        MASBackgroundFilterSlice
                    )

                if bg_flt.maxlength is None:
                    has_unbounded = True
                    bg_flt.priority = 11 # force this slice to be important

                # add to slices
                store.mas_utils.insert_sort(
                    self._slices,
                    MASBackgroundFilterSliceData(index, bg_flt),
                    MASBackgroundFilterSliceData.sk
                )

            if not has_unbounded:
                raise Exception("No unbounded slice found")

            # set offset of initial slice to 0
            self._slices[0].offset = 0

        def _pf_insert(self, index, sl_data):
            """
            Inserts a filter slice offset into the effective slices list 
            based on a starting index.

            IN:
                index - starting index
                sl_data - the slice data to insert
            """
            # looop, finding the right place for the sl_off
            while (
                    index < len(self._eff_slices)
                    and self._eff_slices[index] < sl_data
            ):
                index += 1

            # we must have the correct location now
            # determine the offset to use
            if index == 0:
                sl_data.offset = 0
            else:
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

            # highest priority in leftovers
            hpsl_data = leftovers.pop(
                MASBackgroundFilterSliceData.highest_priority(leftovers)
            )

            for es_index in range(len(self._eff_slices)-1, -1, -1):
               
                # get current slice
                csl_data = self._eff_slices[es_index]

                if csl_data.flt_slice.priority < hpsl_data.flt_slice.priority:
                    # current has a lower priority

                    # remove the lower priority item, and store in leftovers
                    leftovers.insert(0, self._eff_slices.pop(es_index))

                    # then clean up the offsets
                    self._adjust_offset(
                        es_index,
                        csl_data.flt_slice.minlength * -1
                    )

                    # add the higher priority item
                    self._pf_insert(es_index, hpsl_data)

                    # and find newest high leftover priority
                    hpsl_data = leftovers.pop(
                        MASBackgroundFilterSliceData.highest_priority(
                            leftovers
                        )
                    )

            # clean up if our current min length is too large
            while (
                    len(self._eff_slices) > 1
                    and self._eff_chunk_min_end() > length
            ):
                # obtain lowest priority filter slice offset object and remove
                llop_index = MASBackgroundFilterSliceData.lowest_priority(
                    self._eff_slices
                )
                lpsl_data = self._eff_slices.pop(llop_index)

                # fix eff offsets
                self._adjust_offset(
                    llop_index,
                    lpsl_data.flt_slice.minlength * -1
                )

            # ensure first slice has 0 offset
            self._eff_slices[0].offset = 0

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
                pp - progpoint to run on a chunk change.
                    This may run multiple times if multiple chunk changes 
                    have occurred. 
                    the following args are passed to the progpoint:
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

            self._index = 0
            # the index in _chunks of the current chunk

        def __str__(self):
            """
            Shows chunks and curr chunk information
            """
            output = []
            
            # mn to sr chunk
            chunk_name = "Midnight to Sunrise"
            if self._index == 0:
                chunk_name += "| CURRENT CHUNK"
            output.append(chunk_name)
            output.append(str(self._mn_sr))

            # sr to ss chunk
            chunk_name = "Sunrise to Sunset"
            if self._index == 1:
                chunk_name += "| CURRENT CHUNK"
            output.append("")
            output.append(chunk_name)
            output.append(str(self._sr_ss))

            # ss to mn chunk
            chunk_name = "Sunset to Midnight"
            if self._index == 2:
                chunk_name += "| CURRENT CHUNK"
            output.append("")
            output.append(chunk_name)
            output.append(str(self._ss_mn))

            return "\n".join(output)

        def backmap(self, anchors):
            """
            Generates a backwords lookback map with a set of anchors.
            Basically, this creates a mapping of the internal filters such that
            each filter is mapped to an "anchor" filter, based on the order
            of the filters. The lookback for determining an anchor also loops
            upon reaching the end of a day.

            Example:
                Anchors: flt_1, flt_3
                Order: flt_0, flt_1, flt_2, flt_3, flt_4, flt_5
                Resulting mapping:
                    flt_0: flt_3 - (because we loop to flt_5 when looking back
                                    from flt_0)
                    flt_1: flt_1
                    flt_2: flt_1 - (flt_1 is the closest previous anchor from 
                                    flt_2)
                    flt_3: flt_3
                    flt_4: flt_3
                    flt_5: flt_3

            IN:
                anchors - dict of anchors. Set the keys to the anchor filters.

            OUT:
                anchors - the values will be set to lists of all filtesr mapped
                    to those anchors

            RETURNS: reverse map where each filter is a key, and the values are
                anchors.
            """
            if len(anchors) < 1:
                return {}

            # organize all filters in order
            ordered_flts = []
            for chunk in self._chunks:
                ordered_flts.extend(chunk.filters(True))

            if len(ordered_flts) < 1:
                return {}

            # init anchors lists
            for anc_key in anchors:
                anchors[anc_key] = []

            # init reverse map
            r_map = {}

            # loop over filters
            curr_anchor = None
            orphans = []
            for flt in ordered_flts:
                # check for new anchor
                if flt in anchors:
                    curr_anchor = flt

                # now organize
                if curr_anchor is None:
                    # orphans are added to the last anchor
                    orphans.append(flt)

                else:
                    # have anchor, add to lists and maps
                    r_map[flt] = curr_anchor
                    anchors[curr_anchor].append(flt)

            # add orphans to the last filter
            if curr_anchor is not None:
                anchors[curr_anchor].extend(orphans)
                for orphan in orphans:
                    r_map[orphan] = curr_anchor

            return r_map

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

        def current(self):
            """
            Gets current filter

            RETURNS: current filter
            """
            return self._chunks[self._index].current()

        def _current_chunk(self):
            """
            Gets current chunk

            RETURNS: current chunk
            """
            return self._chunks[self._index]

        def current_pos(self):
            """
            Generates internal informatiom related to the current position

            RETURNS: tuple:
                [0] - current chunk index
                [1] - beginning offset of the current chunk
                [2] - beginning offset of the next chunk
                    NOTE: this is -1 if no next chunk
                [3] - current slice index
                [4] - beginning offset of the current slice
                [5] - beginning offset of the next slice
                    NOTE: this is set to the next chunk offset if no next
                        slice
            """
            # current offset is add up chunk lengths
            curr_offset = 0
            for index in range(self._index):
                curr_offset += len(self._chunks[index])

            # next offset is next chunk length + current offset
            if 0 <= self._index < len(self._chunks)-1:
                next_offset = curr_offset + self._chunks[self._index+1]
            else:
                next_offset = -1

            # now get slice info
            sl_index, sl_begin, sl_end = self._current_chunk().current_pos()

            # end sl might be different
            if sl_end < 0:
                sl_end = next_offset

            # and return info
            return (
                self._index,
                curr_offset,
                next_offset,
                sl_index,
                sl_begin,
                sl_end
            )

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

        def is_flt_day(self, flt):
            """
            Checks if the given filter is day according to this filter manager
            NOTE: assumes we are organized already.

            IN:
                flt - filter to check

            RETURNS: True if day, false if not
            """
            return flt in self._day_filters

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

        def progress(self):
            """
            Progresses the filter, running progpoints and updating indexes.

            Progpoint execution rules:
            * progression remains in the same chunk:
                1. progpoint in that chunk is ran for every slice change.
            * progression moves to next chunk:
                1. progpoint from chunk to chunk is ran.
                2. progpoints in the NEW chunk is ran for every slice change.
            * progression moves through multiple chunks:
                1. progpoint from chunk to chunk is ran for every chunk change.
                2. progpoints in the chunk we END UP IN is ran for every
                    slice change.

            RETURNS: the current filter after progression
            """
            # seconds from midnight
            sfmn = store.mas_utils.time2sec(datetime.datetime.now().time())

            # first, determine our current position range
            # TODO


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


    class MASBackgroundFilterMap(object):
        """
        Extension of MASFilterMap.

        Use this to map weather maps to filters.

        NOTE: actual implementation is by wrapping around MASFilterMap.

        NOTE: this is verified after init level -1

        PROPERTIES:
            None
        """

        def __init__(self, **filter_pairs):
            """
            Constructor

            Will throw exceptions if not given MASWeatherMap objects

            IN:
                **filter_pairs - filter=val args to use. Invalid filters are
                    ignored. Values should be MASWeatherMap objects.
            """
            # validate MASWeatherMap objects
            for wmap in filter_pairs.itervalues():
                if not isinstance(wmap, MASWeatherMap):
                    raise TypeError(
                        "Expected MASWeatherMap object, not {0}".format(
                            type(wmap)
                        )
                    )

            self.__mfm = MASFilterMap(
                default=None,
                cache=False,
                **filter_pairs
            )

        def flts(self):
            """
            Gets all filter names in this filter map

            RETURNS: list of all filter names in this map
            """
            return self.__mfm.map.keys()

        def get(self, flt):
            """
            Gets value from map based on filter

            IN:
                flt - filter to lookup

            RETURNS: value for the given filter
            """
            return self.__mfm.get(flt)

        def _mfm(self):
            """
            Returns the intenral MASFilterMap. Only use if you know what you
            are doing.

            RETURNS: MASFilterMap
            """
            return self.__mfm


    def MASBackground(
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
            exit_pp=None
    ):
        """DEPRECATED
        Old-style MASBackground objects.
        This is mapped to a MASFilterableBackground with default 
        (aka pre0.11.3 filters) slice management

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

        RETURNS: MASFilterableBackground object
        """
        # build map data
        img_map_data = {
            store.mas_sprites.FLT_DAY: MASWeatherMap(precip_map={
                store.mas_weather.PRECIP_TYPE_DEF: image_day,
                store.mas_weather.PRECIP_TYPE_RAIN: image_rain_day,
                store.mas_weather.PRECIP_TYPE_OVERCAST: image_overcast_day,
                store.mas_weather.PRECIP_TYPE_SNOW: image_snow_day,
            }),
            store.mas_sprites.FLT_NIGHT: MASWeatherMap(precip_map={
                store.mas_weather.PRECIP_TYPE_DEF: image_night,
                store.mas_weather.PRECIP_TYPE_RAIN: image_rain_night,
                store.mas_weather.PRECIP_TYPE_OVERCAST: image_overcast_night,
                store.mas_weather.PRECIP_TYPE_SNOW: image_snow_night,
            }),
        }

        # build object
        return MASFilterableBackground(
            background_id,
            prompt,
            MASBackgroundFilterMap(**img_map_data),
            store.mas_background.default_MBGFM(),
            hide_calendar=hide_calendar,
            hide_masks=hide_masks,
            disable_progressive=disable_progressive,
            unlocked=unlocked,
            entry_pp=entry_pp,
            exit_pp=exit_pp
        )


    class MASFilterableBackground(object):
        """
        Background class to get display props for bgs

        PROPERTIES:
            background_id - the id which defines this bg
            prompt - button label for the bg
            image_map - MASBackgroundFilterMap object containing mappings of
                filter + weather to images
            hide_calendar - whether or not we display the calendar with this
            hide_masks - whether or not we display the window masks
            disable_progressive - weather or not we disable progesssive weather
            unlocked - whether or not this background is unlocked
            entry_pp - entry programming points for bgs
            exit_pp - exit programming points
        """
        import store.mas_background as mas_background
        import store.mas_weather as mas_weather

        def __init__(self,
            background_id,
            prompt,
            image_map,
            filter_man,
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

                image_map:
                    MASBackgroundFilterMap of bg images to use.
                    Use image tags for MASWeatherMap values.

                filter_man:
                    MASBackgroundFilterManager to use

                backup_img:
                    image tag/image path to use as a backup

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
            # sanity checks
            if background_id in self.mas_background.BACKGROUND_MAP:
                raise Exception("duplicate background ID")
            if not isinstance(image_map, MASBackgroundFilterMap):
                raise TypeError(
                    "Expected MASBackgroundFilterMap, got {0}".format(
                        type(image_map)
                    )
                )
            if not isinstance(filter_man, MASBackgroundFilterManager):
                raise TypeError(
                    "Exepcted MASBackroundFilterManager, got {0}".format(
                        type(filter_man)
                    )
                )

            self.background_id = background_id
            self.prompt = prompt
            self.image_map = image_map
            self._flt_man = filter_man

            # internal mapping of filters to their latest image.
            # see MASBackgroundFilterManager.backmap for explanation.
            # we use this to ensure that every filter has an appropriate
            # set of BG images to use.
            # key: filter
            # value: filter to check for images
            self._flt_img_map = {}

            # reverse map of the above, mapping filters-with-images to lists
            # of dependent filters.
            # key: filter
            # value: list of filters that use the key's images.
            self._flt_img_anc = {}

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

        def build(self):
            """
            Builds filter slices using current suntimes.
            Also builds appropraite BG image maps.

            NOTE: recommended to only call this after the suntimes change or
            on init. Also do this after verifying.
            """
            # build filter slices
            self._flt_man.build(
                persistent._mas_sunrise * 60,
                persistent._mas_sunset * 60
            )

            # now build flt image maps
            self._flt_img_map = self._flt_man.backmap(self._flt_img_anc)

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

        def getRoom(self, flt, weather=None):
            """
            Gets room associated with the given flt and weather
            This performs lookback and other checks to try and find an image.

            Calling this before init level 0 may result in undefined behavior.

            IN:
                flt - filter to check
                weather - weather to check. If None, we use the current
                    weather
                    (Default: None)

            RETURNS: room image, or None if not found
            """
            precip_type = MASWeather.getPrecipTypeFrom(weather)

            # get image using normal ways
            img = self._get_image(flt, precip_type)
            if img is None:
                # no image, so we should try lookback
                m_w_m = self._lookback(flt)
                if m_w_m is not None:
                    img = m_w_m.get(precip_type)

            return img

        def getCurrentRoom(self):
            """
            Gets current Room

            RETURNS: Current room image, may be None if this BG is badly built
            """
            return self.getRoom(self.current())

        def getDayRoom(self, weather=None):
            """DEPRECATED
            Can't use this anymore since there's no single image that defines
            "day" anymore. It's all filter based.
            See getDayRooms instead
            """
            pass

        def getDayRooms(self, weather=None):
            """
            Gets all day images for a weather.

            IN:
                weather - weather to check. If None, we use the current 
                    weather.
                    (Default: None)

            RETURNS: dict of the following format:
                key: flt
                value: day according to the weather.
                NOTE: only filters that have a room with the given weather
                    are returned. No lookback.
            """
            precip_type = MASWeather.getPrecipTypeFrom(weather)

            results = {}
            for flt in self._flt_man.filters_day():
                img = self._get_image(flt, precip_type)
                if img is not None:
                    results[flt] = img

            return results

        def _get_image(self, flt, precip_type):
            """
            Gets image associated with the given flt and precip_type
            does NOT perform lookback checks.

            IN:
                flt - filter to check
                precip_type - precip type to check

            RETURNS: image, or None if not found
            """
            m_w_m = self.image_map.get(flt)
            if m_w_m is None:
                return None
            return m_w_m.get(precip_type)

        def getNightRoom(self, weather=None):
            """DEPRECATED
            Can't use this anymore since there's no single image that defines
            "night" anymore. It's all filter-based
            See getNightRooms instead
            """
            pass

        def getNightRooms(self, weather=None):
            """
            Gets all night images for a weather.

            IN:
                weather - weather to check. If None, we use the current
                    weather.
                    (Default: None)

            RETURNS: dict of the following format:
                key: flt
                value: night according to the weather.
                NOTE: only filters that have a room with the given weather
                    are returned. No lookback.
            """
            precip_type = MASWeather.getPrecipTypeFrom(weather)

            results = {}
            for flt in self._flt_man.filters_night():
                img = self._get_image(flt, precip_type)
                if img is not None:
                    results[flt] = img

            return results

        def getRoomForTime(self, weather=None):
            """
            Gets the room for the current time and desired weather

            NOTE: if you just want current room to use, use getCurrentRoom.

            IN:
                weather - get the room bg for the time and weather
                (Default: current weather)

            RETURNS: room image for the current weather and time
            """
            return self.getRoom(self.current(), weather)

        def isChangingRoom(self, old_weather, new_weather):
            """
            Checks if the room would change because of a change in weather

            IN:
                old_weather - weather to start from
                new_weather - weather to change to

            RETURNS: true if the room would change, False otherwise
            """
            curr_flt = self.current()
            return (
                self._get_image(curr_flt, old_weather.precip_type)
                != self._get_image(curr_flt, new_weather.precip_type)
            )

        def isFltDay(self, flt=None):
            """
            Checks if the given filter is considered a "day" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "day" filter according to this bg
            """
            if flt is None:
                flt = store.mas_sprites.get_filter()

            return self._flt_man.is_flt_day(flt)

        def isFltNight(self, flt=None):
            """
            Checks if the given filter is considered a "night" filter according
            to this background.

            IN:
                flt - filter to check
                    if None, we use the current filter

            RETURNS: True if flt is a "night" filter according to this BG
            """
            return not self.isFltDay(flt)

        def _lookback(self, flt):
            """
            Gets MASWeatherMap for a filter, using lookback

            IN:
                flt - filter to check

            RETURNS: MASWeatherMap, or None if not found
            """
            return self.image_map.get(self._flt_img_map.get(flt))

        def progress(self):
            """
            Progresses the filter.
            """
            # TODO

        def verify(self):
            """
            Verifies all internal filter and weather data is valid.
            Raises exception upon errors.
            Assumed to be called at least at init level 0
            """
            self._flt_man.verify()
            self._verify_img_flts(self._flt_man._day_filters.keys())
            self._verify_img_flts(self._flt_man._night_filters.keys())
            # TODO: anymore?

        def _verify_img_flts(self, flts):
            """
            Verifies that at least one image exists for the given flts.
            Also organizes filters that have a default image

            Raises an exception if no images found

            IN:
                flts - list of filters to check
            """
            img_found = False
            for flt in flts:
                m_w_m = self.image_map.get(flt)
                if m_w_m is not None:
                    img = m_w_m.get(store.mas_weather.PRECIP_TYPE_DEF)
                    if img is not None:
                        img_found = True
                        self._flt_img_anc[flt] = []
                        return

            if not img_found:
                raise Exception("No images found for these filters")


#Helper methods and such
init -20 python in mas_background:
    import store
    BACKGROUND_MAP = {}
    BACKGROUND_RETURN = "Nevermind"


    def default_MBGFM():
        """
        Generates a MASBackgroundFilterManager using the default 
        (aka pre0.11.3) settings.

        RETURNS: MASBackgroundFilterManager object
        """
        return store.MASBackgroundFilterManager(
            store.MASBackgroundFilterChunk(
                False,
                None,
                store.MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            ),
            store.MASBackgroundFilterChunk(
                True,
                None,
                store.MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_DAY,
                    60
                )
            ),
            store.MASBackgroundFilterChunk(
                False,
                None,
                store.MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            ),
        )


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

    def mas_changeBackground(new_background, by_user=None, set_persistent=False):
        """
        changes the background w/o any scene changes

        IN:
            new_background:
                The background we're changing to

            by_user:
                True if the user switched the background themselves

            set_persistent:
                True if we want this to be persistent
        """
        if by_user is not None:
            mas_background.force_background = bool(by_user)

        if set_persistent:
            persistent._mas_current_background = new_background.background_id

        mas_current_background.exit(new_background)
        mas_setBackground(new_background)

    def mas_startupBackground():
        """
        Sets up the spaceroom to start up in the background you left in if it is unlocked and still exists
        """
        if (
            mas_isMoniEnamored(higher=True)
            and persistent._mas_current_background in store.mas_background.BACKGROUND_MAP
            and store.mas_background.BACKGROUND_MAP[persistent._mas_current_background].unlocked
        ):
            background_to_set = store.mas_background.BACKGROUND_MAP[persistent._mas_current_background]
            mas_changeBackground(background_to_set)

            if background_to_set.disable_progressive:
                store.skip_setting_weather = True

        #If for whatever reason, we are no longer able to use the persistent background now, we reset to spaceroom
        else:
            persistent._mas_current_background = "spaceroom"

    def mas_checkBackgroundChangeDelegate():
        """
        Checks to see if the background change delegate should be locked or unlocked and changes its state accordingly

        Key rule: at least 2 available backgrounds
        """
        if mas_background.getUnlockedBGCount() < 2:
            mas_lockEVL("monika_change_background","EVE")
        else:
            mas_unlockEVL("monika_change_background", "EVE")


    #Just set us to the normal room here
    mas_current_background = None
    mas_setBackground(mas_background_def)



#START: Programming points
init -2 python in mas_background:
    import store

    def _def_background_entry(_old):
        """
        Entry programming point for befault background
        """
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

        #NOTE: We check if _old here because it acts as a check for whether or not we're in the init phase
        if _old:
            #Since these holidays demand a specific weather, we'll set them here
            if store.mas_isO31():
                store.mas_changeWeather(store.mas_weather_thunder, by_user=True)

            elif store.mas_isD25():
                store.mas_changeWeather(store.mas_weather_snow, by_user=True)

        #Weather should always be unlocked for spaceroom
        #This catches the potential of a deleted background which does not support weather
        store.mas_unlockEVL("monika_change_weather", "EVE")

    def _def_background_exit(_new):
        """
        Exit programming point for befault background
        """
        store.mas_lockEVL("mas_monika_islands", "EVE")

        #Lock the weather is the background we are changing to does not support it
        if _new.disable_progressive:
            store.mas_lockEVL("monika_change_weather", "EVE")


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

    #Now load data
    store.mas_background.loadMBGData()

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
init 5 python:
    # available only if moni affection is affectionate+
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_change_background",
            category=["location"],
            prompt="Can we go somewhere else?",
            pool=True,
            unlocked=False,
            rules={"no unlock": None},
            aff_range=(mas_aff.ENAMORED, None)
        ),
        restartBlacklist=True
    )

label monika_change_background:
    m 1hua "Sure!"

    #FALL THROUGH

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
        return "prompt"

    if sel_background == mas_current_background:
        m 1hua "We're here right now, silly."
        m "Try again~"
        jump monika_change_background_loop

    call mas_background_change(sel_background, set_persistent=True)
    return

#Generic background changing label, can be used if we wanted a sort of story related change
label mas_background_change(new_bg, skip_leadin=False, skip_outro=False, set_persistent=False):
    # otherwise, we can change the background now
    if not skip_leadin:
        m 1eua "Alright!"
        m 1hua "Let's go, [player]!"

    #Little transition
    hide monika
    scene black
    with dissolve
    pause 2.0

    python:
        #Set persistent
        if set_persistent:
            persistent._mas_current_background = new_bg.background_id

        #Store the old bg for use later
        old_bg = mas_current_background

        #Finally, change the background
        mas_changeBackground(new_bg)

        #If we've disabled progressive and hidden masks, then we shouldn't allow weather change
        if new_bg.disable_progressive and new_bg.hide_masks:
            mas_weather.temp_weather_storage = mas_current_weather
            mas_changeWeather(mas_weather_def)
            mas_lockEVL("monika_change_weather", "EVE")

        else:
            if mas_weather.temp_weather_storage is not None:
                mas_changeWeather(mas_weather.temp_weather_storage)
                #Now reset the temp storage for weather
                mas_weather.temp_weather_storage = None

            else:
                #If we don't have tempstor, run the startup weather
                mas_startupWeather()

            #Then we unlock the weather sel here
            mas_unlockEVL("monika_change_weather", "EVE")

    call spaceroom(scene_change=True, dissolve_all=True)

    if not skip_outro:
        m 1eua "Here we are!"
        m "Let me know if you want to go somewhere else, okay?"
    return
