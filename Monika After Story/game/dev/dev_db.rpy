## special functions to check integrity of systems

init python:

    def _mas_check_ev_type_bool(val, name, report, delim=" | ", str_rep=True):
        if val is not None and not isinstance(val, bool):
            report.extend([delim, "bad ", name, " {0}".format(val)])

    
    def _mas_check_ev_type_dict(val, name, report, delim=" | ", str_rep=True):
        if val is not None and not isinstance(val, dict):
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type_dt(val, name, report, delim=" | ", str_rep=True):
        if val is not None and not isinstance(val, datetime.datetime):
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type_evact(val, name, report, delim=" | ", str_rep=True):
        if val is not None and val not in EV_ACTIONS:
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type_int(val, name, report, delim=" | ", str_rep=True):
        if val is not None and not isinstance(val, int):
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type_str(val, name, report, delim=" | ", str_rep=True):
        if (
                val is not None 
                and not (isinstance(val, str) or isinstance(val, unicode))
            ):
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type_tuli(val, name, report, delim=" | ", str_rep=True):
        if (
                val is not None 
                and not (
                    isinstance(val, list)
                    or isinstance(val, tuple)
                )
            ):
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type_tuli_aff(val, name, report, delim=" | ", str_rep=True):
        if val is not None and not isinstance(val, tuple) and len(val) != 2:
            report.extend([delim, "bad ", name, " {0}".format(val)])


    def _mas_check_ev_type(ev, str_rep=True):
        """
        Checks typers of the given event, then returns a string report

        IN:
            ev - event to check

        RETURNS: single line string report
        """
        report = ["EV: {0}".format(ev.eventlabel)]
        delim = " | "

        _mas_check_ev_type_str(ev.eventlabel, "eventlabel", report, delim)
        _mas_check_ev_type_str(ev.prompt, "prompt", report, delim)
        _mas_check_ev_type_str(ev.label, "label", report, delim)
        _mas_check_ev_type_tuli(ev.category, "category", report, delim)
        _mas_check_ev_type_bool(ev.unlocked, "unlocked", report, delim)
        _mas_check_ev_type_bool(ev.random, "random", report, delim)
        _mas_check_ev_type_bool(ev.pool, "pool", report, delim)
        _mas_check_ev_type_str(ev.conditional, "conditional", report, delim)
        _mas_check_ev_type_evact(ev.action, "action", report, delim)
        _mas_check_ev_type_dt(ev.start_date, "start_date", report, delim)
        _mas_check_ev_type_dt(ev.end_date, "end_date", report, delim)
        _mas_check_ev_type_dt(ev.unlock_date, "unlock_date", report, delim)
        _mas_check_ev_type_int(ev.shown_count, "shown_count", report, delim)
        _mas_check_ev_type_str(ev.diary_entry, "diary_entry", report, delim)
        _mas_check_ev_type_dict(ev.rules, "rules", report, delim)
        _mas_check_ev_type_dt(ev.last_seen, "last_seen", report, delim)
        _mas_check_ev_type_tuli(ev.years, "years", report, delim)
        _mas_check_ev_type_bool(ev.sensitive, "sensitive", report, delim)
        _mas_check_ev_type_tuli_aff(ev.aff_range, "aff_range", report, delim)

        report.append("\n")
        return report


    def _mas_check_ev_type_per(ev_line, str_rep=True):
        """
        Checks typers of the given event line, then returns a string report
        NOTE: this uses data that would be stored in a perdb
        ASSUMES: lines match.

        IN:
            ev_line - line of persistent tuple data to check

        RETURNS: single line string report
        """
        report = ["EV: {0}".format(ev_line[0])]
        delim = " | "

        try:

            _mas_check_ev_type_str(ev_line[0], "eventlabel", report, delim)
            _mas_check_ev_type_str(ev_line[1], "prompt", report, delim)
            _mas_check_ev_type_str(ev_line[2], "label", report, delim)
            _mas_check_ev_type_tuli(ev_line[3], "category", report, delim)
            _mas_check_ev_type_bool(ev_line[4], "unlocked", report, delim)
            _mas_check_ev_type_bool(ev_line[5], "random", report, delim)
            _mas_check_ev_type_bool(ev_line[6], "pool", report, delim)
            _mas_check_ev_type_str(ev_line[7], "conditional", report, delim)
            _mas_check_ev_type_evact(ev_line[8], "action", report, delim)
            _mas_check_ev_type_dt(ev_line[9], "start_date", report, delim)
            _mas_check_ev_type_dt(ev_line[10], "end_date", report, delim)
            _mas_check_ev_type_dt(ev_line[11], "unlock_date", report, delim)
            _mas_check_ev_type_int(ev_line[12], "shown_count", report, delim)
            _mas_check_ev_type_str(ev_line[13], "diary_entry", report, delim)
            _mas_check_ev_type_dict(ev_line[14], "rules", report, delim)
            _mas_check_ev_type_dt(ev_line[15], "last_seen", report, delim)
            _mas_check_ev_type_tuli(ev_line[16], "years", report, delim)
            _mas_check_ev_type_bool(ev_line[17], "sensitive", report, delim)
            _mas_check_ev_type_tuli_aff(ev_line[18], "aff_range", report, delim)

        except Exception as e:
            report.append("FAILED: " + repr(e))

        report.append("\n")
        return report


    def mas_check_event_types(per_db, str_buffer=None, str_rep=True):
        """
        Goes through given persistent database for events and double checks 
        types. Returns a string report.

        IN:
            per_db - persistent db of events to check types of
            str_buffer - the string buffer we should write to.
                If None, we do NO reporting.
            str_rep - UNUSED

        RETURNS:
            string report int he given buffer
        """
        # NOTE: we assume lots of things about the given per_db.
        if str_buffer is None:
            return
        
        for ev_label, ev_line in per_db.iteritems():
            str_buffer.write("".join(_mas_check_ev_type_per(ev_line)))

    def mas_largest_persistent_item():
        """
        Determines largest item in persistent

        RETURNS: tuple of the following format:
            [0] - key of item
            [1] - size of item
        """
        item_size = 0
        item = ""
        for key in persistent.__dict__:
            value_size = sys.getsizeof(persistent.__dict__[key])
            if value_size > item_size:
                item_size = value_size
                item = key

        return (item, item_size)


    def mas_per_dump(item_key):
        """
        Dumps something from persistent

        IN:
            item_key - the string name of the item to dump
        """
        # we do some type checking here
        item = persistent.__dict__[item_key]
        if isinstance(item, dict):
            mas_per_dump_dict(item_key)
        elif isinstance(item, list):
            mas_per_dump_list(item_key)
        elif isinstance(item, set):
            mas_per_dump_list(item_key)
        # NOTE: ignore others for now

    
    def mas_per_dump_dict(dkey):
        """
        Dumps an output of a persistent dict

        IN:
            dkey - the string name of the dict to dump
        """
        with open("perdump", "w") as outfile:
            data = persistent.__dict__[dkey]
            for data_key in data:
                outfile.write("{0}: {1}\n".format(str(data_key), str(data[data_key])))


    def mas_per_dump_list(lkey):
        """
        Dumps an output of a persistent list

        IN:
            lkey - the string name of the list to dump
        """
        with open("perdump", "w") as outfile:
            data = persistent.__dict__[lkey]
            for item in data:
                outfile.write("{0}\n".format(str(item)))


init python in dev_mas_shared:
    import cPickle
    import store
    import store.mas_ev_data_ver as ver

    from collections import defaultdict

    class MASPersistentAnalyzer(object):
        """
        class for analyzing persistent data objects

        PROPERTIES:
            event_db - all events database
                key: eventlabel
                value: EventDBData object
            property_index - index of all event objects
                key: property name
                value: dictionary:
                    key: the value of the property
                        (for category, each tag is a separate value)
                    value: dictionary:
                        key: eventlabel
                        value: EventDBData object
        """

        def __init__(self, in_char):
            """
            IN:
                in_char - pass True if the persisten file is int 
                eh user's charactesr dir. Otherwise we use the 
                loaded persistent
            """
            self.in_char = in_char
            self.clear()
            self.analyze()

        def analyze(self):
            """
            Loads and analyzes persistent data
            """
            # select persistent to load
            if self.in_char:
                pkg = store.mas_docking_station.getPackage("persistent")
                pdata = cPickle.loads(pkg.read().decode("zlib"))
                pkg.close()
            else:
                pdata = store.persistent


            for ev_label in pdata.event_database:
                ev_data = store.EventDBData(pdata.event_database[ev_label])

                # add to primary db
                self.event_db[ev_label] = ev_data

                # add to index db
                for prop_name in store.Event.T_EVENT_NAMES:
                    prop_value = getattr(ev_data, prop_name)

                    # listables need to be split into parts                    
                    # except affection
                    if ver._verify_tuli(prop_value, allow_none=False) and prop_name != "aff_range":
                        for item in prop_value:
                            self.property_index[prop_name][item][ev_label] = ev_data

                    else:
                        self.property_index[prop_name][prop_value][ev_label] = ev_data

        @staticmethod
        def analyze_and_report(in_char, sort_asc):
            """
            Quickly creates an analysis and outputs it for every property.

            IN:
                in_char - True to use persistent from characters, otherwise use ours
                sort_acs - see get_all_and_file
            """
            analyzer = MASPersistentAnalyzer(in_char)

            for prop_name in store.Event.T_EVENT_NAMES:
                file_name = "per-analysis-{0}.txt".format(prop_name)
                analyzer.get_all_and_file(prop_name, sort_asc=sort_asc, file_name=file_name)

        def clear(self):
            """
            Clears data
            """
            self.event_db = {}
            self.property_index = defaultdict(lambda: defaultdict(dict))

        @staticmethod
        def cmp_none_handler(arg1, arg2):
            """
            Specialized cmp function that can handle Nones

            In general, we push Nones to the back.
            """
            if arg1 is None:
                if arg2 is None:
                    return 0

                return 1

            elif arg2 is None:
                return -1

            return cmp(arg1, arg2)

        def get_all_and_file(self,
                prop,
                sort_asc=None,
                file_name="per-analysis.txt",
                only_incl=None
        ):
            """
            Does get_all_for_prop but saves the results directly to file 

            See get_all_for_prop for param doc
            """
            ev_labels, ev_datas = self.get_all_for_prop(
                prop,
                sort_asc=sort_asc,
                only_incl=only_incl
            )

            with open(file_name, "w") as output:

                output.write("FOR PROP: {0}\n".format(prop))

                # determine the first value
                curr_label = ev_labels[0]
                curr_data = ev_datas[curr_label]

                prop_value = getattr(curr_data, prop)

                # this is just so we dont have to print out of loop 
                if prop_value is None:
                    last_value = ""
                else:
                    last_value = None

                for index in range(len(ev_labels)):

                    curr_label = ev_labels[index]
                    curr_data = ev_datas[curr_label]
                    prop_value = getattr(curr_data, prop)

                    if prop_value != last_value:
                        output.write("\n\n============== VALUE: {0}\n".format(prop_value))
                        last_value = prop_value

                    output.write("{0} | {1}\n".format(curr_label, str(curr_data.data_tup)))

        def get_all_for_prop(self, prop, sort_asc=None, only_incl=None):
            """
            Gets all entries for a prop

            IN:
                prop - the property to get
                sort_asc - True to sort ascending
                    False to sort descending
                    None to not sort
                    (Default: None)
                only_incl - pass this in as a dictionary of eventlabels to 
                    only include these in the prop

            RETURNS: tuple:
                [0] - list of sorted event labels
                [1] - dictionary of data:
                    key: eventlabel
                    value: EventDBDAta object
            """
            prop_values = self.property_index.get(prop, {})
            values_sorted = list(prop_values.keys())

            if sort_asc is not None:
                values_sorted = sorted(
                    values_sorted,
                    cmp=MASPersistentAnalyzer.cmp_none_handler,
                    reverse=not sort_asc
                )

            ev_labels = []
            ev_datas = {}
            for value in values_sorted:
                datas = prop_values.get(value, {})

                for ev_label in datas:
                    if only_incl is None or ev_label in only_incl:
                        ev_labels.append(ev_label)
                        ev_datas[ev_label] = datas[ev_label]

            return ev_labels, ev_datas

        def get_matching_value(self, prop, value, only_incl=None):
            """
            Gets index entries for a prop and value

            IN:
                prop - the property to get
                value - the value to get
                only_incl - if passed in, only include entries with 
                    eventlabel in this dict

            RETURNS: dictionary containing all items that match the value for
                a prop:
                key: event label
                value: EventDBData object
                If None is returned, then something was invalid.
            """
            if only_incl is not None and len(only_incl) < 1:
                return {}

            prop_values = self.property_index.get(prop, None)
            if prop_values is None:
                return None

            entries = prop_values.get(value, None)

            if only_incl is None:
                return entries

            # otherwise need to filter
            filtered = {}
            for entry_key in entries:
                if entry_key not in only_incl:
                    filtered[entry_key] = entries[entry_key]

            return filtered

        def multi_val_filter(self, **prop_values):
            """
            Runs get_matching_value multiple times to narrow down based on the given prop values.

            RETURNS: get_matching_vaue return value
            """
            if len(prop_values) < 1:
                return {}

            final_results = None
            for prop in prop_values:
                value = prop_values[prop]

                results = self.get_matching_value(prop, value, only_incl=final_results)
                if results is not None:
                    final_results = results

            if final_results is None:
                return {}

            return final_results

        # add specialty functions here
        @staticmethod
        def report_on_unlocked_pools(in_char, sort_asc=None):
            """
            Runs a report on unlocked pools
            SAved as unlocked-pools.txt

            See analyze_and_report for param doc
            """
            analyzer = MASPersistentAnalyzer(in_char)
            pool_evs = analyzer.get_matching_value("pool", True)
            analyzer.get_all_and_file(
                "unlock_date",
                sort_asc=sort_asc,
                file_name="unlocked-pools.txt",
                only_incl=pool_evs
            )

        @staticmethod
        def report_on_unlocked_randoms(in_char, sort_asc=None):
            """
            Runs a report on unlocked randoms
            Saved as unlocked-rands.txt
            """
            analyzer = MASPersistentAnalyzer(in_char)
            rand_evs = analyzer.get_matching_value("random", True)
            analyzer.get_all_and_file(
                "unlock_date",
                sort_asc=sort_asc,
                file_name="unlocked-rands.txt",
                only_incl=rand_evs
            )
