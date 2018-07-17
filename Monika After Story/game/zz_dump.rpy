## dumps file for unstablers

init 2018 python:


    def mas_eventDataDump():
        """
        Data dump for purely events stats
        """
        import os
        from store.evhand import event_database,farewell_database,greeting_database
        from store.mas_moods import mood_db
        from store.mas_stories import story_database

        # setup filepath
        _ev_stats = "/ev_dump.log"
        _ev_stats_fp = (config.basedir + _ev_stats).replace("\\", "/")

        # setup counting
        class StatCounter(object):
            """
            Temp class to work with stats
            """


            # setup lines
            _ev_finalstatline = (
                "\n---ST ({12}) ---\n" +
                "EV:{0}\n" +
                "PC:{1}\n" +
                "RC:{2}\n" +
                "UC:{3}\n" +
                "LC:{4}\n" +
                "SC:{5}\n" +
                "SSC:{6} - AVG:{7}\n" +
                "PSC:{8} - AVG:{9}\n" +
                "RSC:{10} - AVG:{11}\n"
            )
            _ev_statline = "{0} - p:{1} - r:{2} - u:{3} - s:{4} - sc:{5}\n"


            def __init__(self, name, db):
                """
                IN:
                    name - display name for this database of stats
                    db - the database this stats is associatd with
                """
                self.ev_count = 0
                self.pool_count = 0
                self.rand_count = 0
                self.unlo_count = 0
                self.lock_count = 0
                self.seen_count = 0
                self.show_count = 0
                self.rshow_count = 0
                self.pshow_count = 0
                self.most_seen_ev = None
                self.name = name
                self.db = db


            def _calcAvg(self, num, den):
                """
                average calculator, with built in N/A
                """
                if den == 0:
                    return "N/A"

                return num / float(den)


            def calcAvgs(self):
                """
                Calculates averages
                
                Returns tuple:
                    [0]: show count avg
                    [1]: pool show count avg
                    [2]: rand show count avg
                """
                return (
                    self._calcAvg(self.show_count, self.ev_count),
                    self._calcAvg(self.pshow_count, self.pool_count),
                    self._calcAvg(self.rshow_count, self.rand_count)
                )


            def checkAndReplaceMostSeen(self, ev):
                """
                Checks and replaces most seen if necessary

                IN:
                    ev - ev to check
                """
                if self.most_seen_ev is None:
                    self.most_seen_ev = ev
                elif self.most_seen_ev.shown_count < ev.shown_count:
                    self.most_seen_ev = ev

        
            def inDB(self, ev):
                """
                returns true if the given ev is in this db
                """
                return ev.eventlabel in self.db


            def stat(self, ev):
                """
                adds the given ev to the stats table.
                Doesn't check if this ev belongs to this db

                Returns the value from _seen
                """
                self.checkAndReplaceMostSeen(ev)
                self.show_count += ev.shown_count
                self.ev_count += 1

                if ev.pool:
                    self.pool_count += 1
                    self.pshow_count += ev.shown_count

                if ev.random:
                    self.rand_count += 1
                    self.rshow_count += ev.shown_count

                if ev.unlocked:
                    self.unlo_count += 1
                else:
                    self.lock_count += 1

                _seen = renpy.seen_label(ev.eventlabel)
                if _seen:
                    self.seen_count += 1

                return _seen

        
            def __str__(self):
                """
                to String
                """
                sc_avg, psc_avg, rsc_avg = self.calcAvgs()
                return (
                    self._ev_finalstatline.format(
                        self.ev_count,
                        self.pool_count,
                        self.rand_count,
                        self.unlo_count,
                        self.lock_count,
                        self.seen_count,
                        self.show_count,
                        sc_avg,
                        self.pshow_count,
                        psc_avg,
                        self.rshow_count,
                        rsc_avg,
                        self.name
                    ) + "\n[MOST]: " +
                    self._ev_statline.format(
                        self.most_seen_ev.eventlabel,
                        self.most_seen_ev.pool,
                        self.most_seen_ev.random,
                        self.most_seen_ev.unlocked,
                        "N/A",
                        self.most_seen_ev.shown_count
                    )
                )


            @staticmethod
            def getSortKey(_statcounter):
                """
                Sort key for a statcounter is the number of entries in its
                database
                """
                return len(_statcounter.db)

        # we have 5 databaess to keep track of
        statcounters = [
            StatCounter("events", event_database),
            StatCounter("byes", farewell_database),
            StatCounter("greetings", greeting_database),
            StatCounter("moods", mood_db),
            StatCounter("stories", story_database)
        ]
        statcounters.sort(key=StatCounter.getSortKey, reverse=True)
        def _stat(_scs, ev):
            """
            Short-circuting stat counter

            returns seen value
            """
            for _sc in _scs:
                if _sc.inDB(ev):
                    return _sc.stat(ev)

            return "N/A"

        with open(_ev_stats_fp, "w") as _ev_stats_file:

            _ev_stats_file.write(config.version + "\n\n")
            _ev_stats_file.write(mas_sessionDataDump())

            # gather data
            for ev in mas_all_ev_db.values():
                _seen = _stat(statcounters, ev)

                # print event stats
                _ev_stats_file.write(StatCounter._ev_statline.format(
                    ev.eventlabel,
                    ev.pool,
                    ev.random,
                    ev.unlocked,
                    _seen,
                    ev.shown_count
                ))

            # print final stats (including most seen)
            for _sc in statcounters:
                _ev_stats_file.write(str(_sc))


    def mas_unstableDataDump():
        """
        This is a function called on startup and performs data dumps.

        Please add your data dump to a different file than dumps.log if its 
        a large dump.

        Thank you.
        """
        mas_eventDataDump()


    def mas_sessionDataDump():
        """
        Dumps session data as a string
        """
        if persistent.sessions is None:
            return "No session data found."

        # grab each data element
        first_sesh = persistent.sessions.get("first_session", "N/A")
        total_sesh = persistent.sessions.get("total_sessions", None)
        curr_sesh_st = persistent.sessions.get("current_session_start", "N/A")
        total_playtime = persistent.sessions.get("total_playtime", None)
        last_sesh_ed = persistent.sessions.get("last_session_end", "N/A")

        if total_sesh is not None and total_playtime is not None:
            avg_sesh = total_playtime / total_sesh

        else:
            avg_sesh = "N/A"

        # which ones do we actually have
        def cts(sesh):
            if sesh is None:
                return "N/A"

            return sesh


        # assemble output
        output = [
            first_sesh,
            cts(total_sesh),
            cts(total_playtime),
            avg_sesh,
            curr_sesh_st,
            last_sesh_ed
        ]

        # NOTE: curr_sesh_st -> last session start because it gets updated
        # during ch30
        outstr = (
            "First session: {0}\n" +
            "Total sessions: {1}\n" +
            "Total playtime: {2}\n" + 
            "Avg playtime per session: {3}\n" +
            "Last session start: {4}\n" +
            "Last session end: {5}\n\n"
        )

        return outstr.format(*output)



    if persistent._mas_unstable_mode:
        mas_unstableDataDump()

