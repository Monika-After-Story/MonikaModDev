## dumps file for unstablers

init 999 python:

    def mas_eventDataDump():
        """
        Data dump for purely events stats
        """
        import os
        from store.evhand import event_database,farewell_database,greeting_database
        from store.mas_moods import mood_db
        from store.mas_stories import story_database

        try:
            mas_all_ev_db.values()
        except:
            # we dont have access to the main db
            # just drop out for now
            return

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
                "EV:{0}\n" + # total events
                "PC:{1}\n" + # number of pool events
                "PUC:{13}\n" + # number of unlocked pools
                "PLC:{14}\n" + # number of locked pools
                "RC:{2}\n" + # number of random events
                "RUC:{15}\n" + # number of unlokced randoms
                "RLC:{16}\n" + # number of locked randoms
                "UC:{3}\n" + # number of unlocked events
                "LC:{4}\n" + # number of locked events
                "SC:{5}\n" + # number of seen events
                "SSC:{6} - AVG:{7}\n" + # number of shown events - avg
                "PSC:{8} - AVG:{9}\n" + # number of pool showns - avg
                "RSC:{10} - AVG:{11}\n" # number of random showns - avg
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
                self.pool_unlo_count = 0
                self.pool_lock_count = 0
                self.rand_count = 0
                self.rand_unlo_count = 0
                self.rand_lock_count = 0
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

                    if ev.unlocked:
                        self.pool_unlo_count += 1
                    else:
                        self.pool_lock_count += 1

                if ev.random:
                    self.rand_count += 1
                    self.rshow_count += ev.shown_count

                    if ev.unlocked:
                        self.rand_unlo_count += 1
                    else:
                        self.rand_lock_count += 1

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
                        self.name,
                        self.pool_unlo_count,
                        self.pool_lock_count,
                        self.rand_unlo_count,
                        self.rand_lock_count,
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
            _ev_stats_file.write(mas_progressionDataDump())

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
        mas_varDataDump()

    def mas_progressionDataDump():
        """
        Dumps progression data as a string
        """
        return (
            "Last XP rate reset: {0}\n"
            "Hours spent today: {1}\n"
            "XP to next level: {2}\n"
            "Current level: {3}\n"
            "Current xp rate: {4}\n"
            "XP last granted: {5}\n\n"
        ).format(
            persistent._mas_xp_rst,
            persistent._mas_xp_hrx,
            persistent._mas_xp_tnl,
            persistent._mas_xp_lvl,
            mas_xp.xp_rate,
            mas_xp.prev_grant,
        )

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

        if total_sesh and total_playtime is not None:
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


    def mas_varDataDump():
        """
        Dumps other kinds of data.
        """
        import os

        # setup filepath
        _var_data = "/var_dump.log"
        _var_data_fp = os.path.normcase(renpy.config.basedir + _var_data)

        with open(_var_data_fp, "w") as _var_data_file:
            _var_data_file.write(config.version + "\n\n")

            # xp and levels
            _var_data_file.write(
                "LEVELS: {0}\nXPTNL: {1}\nUNLOCKS: {2}\n\n".format(
                    persistent._mas_xp_lvl,
                    persistent._mas_xp_tnl,
                    persistent._mas_pool_unlocks
                )
            )

            if mas_isGameUnlocked("NOU"):
                _total_nou_games = float(store.mas_nou.get_total_games())
                _var_data_file.write(
                    "NOU GAMES: {:.0f}\nMONIKA W/R: {}\nPLAYER W/R: {}\n\n".format(
                        _total_nou_games,
                        (
                            "{:.1%}".format(store.mas_nou.get_wins_for("Monika")/_total_nou_games)
                            if _total_nou_games != 0
                            else "N/A"
                        ),
                        (
                            "{:.1%}".format(store.mas_nou.get_wins_for("Player")/_total_nou_games)
                            if _total_nou_games != 0
                            else "N/A"
                        )
                    )
                )
                del _total_nou_games

            # add data lines here
            #Consumables stuff
            for consumable_id in persistent._mas_consumable_map.keys():
                consumable = mas_getConsumable(consumable_id)

                #Need to account for consumables which were removed
                if consumable:
                    #Some prep
                    dlg_props = consumable.dlg_props

                    ref = dlg_props.get(mas_consumables.PROP_CONTAINER, dlg_props.get(mas_consumables.PROP_OBJ_REF))
                    if ref:
                        _var_data_file.write(
                            "{0}S OF {1} {2}: {3}\n".format(
                                ref.upper(),
                                consumable.disp_name.upper(),
                                "EATEN" if consumable.consumable_type == store.mas_consumables.TYPE_FOOD else "DRANK",
                                consumable.getAmountHad()
                            )
                        )

                    else:
                        _var_data_file.write(
                            "{0}S {1}: {2}\n".format(
                                consumable.disp_name.upper(),
                                "EATEN" if consumable.consumable_type == store.mas_consumables.TYPE_FOOD else "DRANK",
                                consumable.getAmountHad()
                            )
                        )

    def mas_dataDumpFlag():
        """
        Checks if the data dump flag (file) exists
        """
        try:
            return os.path.isfile(
                os.path.normcase(renpy.config.basedir + "/givedata.txt")
            )
        except:
            return False


    if persistent._mas_unstable_mode or mas_dataDumpFlag():
        mas_unstableDataDump()
