## dumps file for unstablers

init 2018 python:

    def mas_eventDataDump():
        """
        Data dump for purely events stats
        """
        import os
        import store.evhand as evhand

        # setup filepath
        _ev_stats = "/ev_dump.log"
        _ev_stats_fp = (config.basedir + _ev_stats).replace("\\", "/")

        # setup lines
        _ev_statline = "{0} - p:{1} - r:{2} - u:{3} - s:{4} - sc:{5}\n"
        _ev_finalstatline = (
            "\n---ST---\n" +
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

        # setup counting
        ev_count = 0
        pool_count = 0
        rand_count = 0
        unlo_count = 0
        lock_count = 0
        seen_count = 0
        show_count = 0
        rshow_count = 0
        pshow_count = 0
        most_seen_ev = None

        with open(_ev_stats_fp, "w") as _ev_stats_file:

            _ev_stats_file.write(config.version + "\n\n")

            # gather data
            for ev in evhand.event_database.values():

                if most_seen_ev is None:
                    most_seen_ev = ev
                elif most_seen_ev.shown_count < ev.shown_count:
                    most_seen_ev = ev
                
                show_count += ev.shown_count
                ev_count += 1

                if ev.pool:
                    pool_count += 1
                    pshow_count += ev.shown_count

                if ev.random:
                    rand_count += 1
                    rshow_count += ev.shown_count

                if ev.unlocked:
                    unlo_count += 1
                else:
                    lock_count += 1

                _seen = renpy.seen_label(ev.eventlabel)
                if _seen:
                    seen_count += 1

                # print event stats
                _ev_stats_file.write(_ev_statline.format(
                    ev.eventlabel,
                    ev.pool,
                    ev.random,
                    ev.unlocked,
                    _seen,
                    ev.shown_count
                ))

            # most seen 
            _ev_stats_file.write("\n[MOST]: ")
            _ev_stats_file.write(_ev_statline.format(
                most_seen_ev.eventlabel,
                most_seen_ev.pool,
                most_seen_ev.random,
                most_seen_ev.unlocked,
                "N/A",
                most_seen_ev.shown_count
            ))

            # process data
            show_count_avg = show_count / float(ev_count)
            pshow_count_avg = pshow_count / float(pool_count)
            rshow_count_avg = rshow_count / float(rand_count)

            # print final stats
            _ev_stats_file.write(_ev_finalstatline.format(
                ev_count,
                pool_count,
                rand_count,
                unlo_count,
                lock_count,
                seen_count,
                show_count,
                show_count_avg,
                pshow_count,
                pshow_count_avg,
                rshow_count,
                rshow_count_avg
            ))


    def mas_unstableDataDump():
        """
        This is a function called on startup and performs data dumps.

        Please add your data dump to a different file than dumps.log if its 
        a large dump.

        Thank you.
        """
        mas_eventDataDump()


    if persistent._mas_unstable_mode:
        mas_unstableDataDump()

