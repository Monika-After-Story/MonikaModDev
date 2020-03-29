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
