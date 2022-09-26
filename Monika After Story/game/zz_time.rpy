# special time classes in case we have no timezones

python early:

    import pytz.tzinfo

    class MASLocalTz(pytz.tzinfo.StaticTzInfo):
        """
        Special Tz class that we use when we need to do dynamic timezone
        creation because we couldn't find existing timezone data.

        Despite using StaticTzInfo, this does respect DST, in the sense that
        we will use whatever offset the time library tells us to use.
        """
        import time
        _is_dst = False
        _tz_cache = None

        def __repr__(self):
            return "<MASLocalTz {0}>".format(self._utcoffset.total_seconds())

        @staticmethod
        def apply(dt):
            """
            Returns a datetime that has the same time info as the given one
            but with this timezone set to the tzinfo

            NOTE: will raise an error if tzinfo is already set

            IN:
                dt - datetime to generate new datetime with

            RETURNS: new datetime object with same time as previous but
                tzinfo set to an instance of this MASLocalTz
            """
            mas_tz = MASLocalTz.create()
            return mas_tz.localize(dt)

        @classmethod
        def create(cls):
            """
            Generates an instance of this class that is prepared to localize
            a time or whatever.

            NOTE: this caches the timezone

            RETURNS:
                instance of MASLocalTz ready for usage
            """
            if cls._tz_cache is not None:
                return cls._tz_cache

            # in general, assume timezone is correct when loading from time
            tz_offset = 0
            is_dst = False
            if cls.time.daylight != 0 and cls.time.localtime().tm_isdst > 0:
                tz_offset = cls.time.altzone
                is_dst = True
            else:
                tz_offset = cls.time.timezone

            # time's zones do postive if west, negative if east, but tzinfo
            # is expecting the opposite, so flip the values.
            tz_offset *= -1

            tz_obj = MASLocalTz()

            # to prevent issues later, always round to whole number minutes
            tz_obj._utcoffset = datetime.timedelta(minutes=(tz_offset / 60))
            tz_obj._tzname = "Custom MAS Time"
            tz_obj.zone = "MAS"
            tz_obj._is_dst = is_dst

            if cls._tz_cache is None:
                cls._tz_cache = tz_obj

            return tz_obj

        @classmethod
        def reload(cls):
            """
            Reloads the cached localzone

            RETURNS: instance of MASLocalTz ready for usage
            """
            cls._tz_cache = None
            return MASLocalTz.create()


python early in mas_tt_guard:
    import time
    import threading
    import random

    import store

    class MASUptimeSyncValidator(object):
        """
        Validates uptime using clock
        """
        def __init__(self, on_desync=None, log=None):
            """
            Constructor:

            IN:
                on_desync - a function to call on desync
                    NOTE: will be called from another thread
                        make sure it's thread-safe
                log - the log object to use for logging purposes
            """
            self.__on_desync = on_desync
            self.__log_obj = log
            self.__last_os_ts = 0.0
            self.__quit = False
            self.__desyncs = []
            self.__th = None

        def __log(self, kind, *args, **kwargs):
            """
            Logs a message of severity kind

            IN:
                kind - the message kind
                *args - args to pass to the log method
                *kwargs - kwargs to pass to the log method
            """
            if self.__log_obj:
                fn = getattr(self.__log_obj, kind, None)
                if fn:
                    fn(*args, **kwargs)

        def __log_warning(self, *args, **kwargs):
            """
            Logs a warning

            IN:
                *args - args to pass to the log method
                *kwargs - kwargs to pass to the log method
            """
            self.__log("warning", *args, **kwargs)

        def __log_error(self, *args, **kwargs):
            """
            Logs an error

            IN:
                *args - args to pass to the log method
                *kwargs - kwargs to pass to the log method
            """
            self.__log("error", *args, **kwargs)

        def __run_desync_cb(self):
            """
            Tries to run the callback, logs any errors
            """
            if self.__on_desync:
                try:
                    self.__on_desync()
                except Exception as e:
                    self.__log_error("Failed to run desync callback: {}".format(e), exc_info=True)

        def _start(self):
            """
            Starts the validator loop
            """
            LIMIT = 3600.0 * 30.0
            while not self.__quit:
                wait_time = float(random.randint(3, 7))
                self.__last_os_ts = time.time()

                time.sleep(wait_time)

                change = time.time() - self.__last_os_ts
                diff = change - wait_time
                abs_diff = abs(diff)

                if abs_diff > 1.0:
                    if abs_diff > LIMIT:
                        self.__desyncs.append(diff)
                        self.__log_warning("Major uptime desync, possible corruption: {}".format(diff))
                        self.__run_desync_cb()

                    else:
                        self.__log_warning("Minor uptime desync, skipping: {}".format(diff))

        def get_desyncs(self):
            """
            Returns a list of all desync gaps

            OUT:
                list[float]
            """
            return list(self.__desyncs)

        def is_in_desync(self):
            """
            Returns a boolean indicating if there was a desync

            OUT:
                bool
            """
            return bool(self.__desyncs)

        def start(self):
            """
            Starts the validator by invoking its logic in a thread
            """
            self.__th = th = threading.Thread(target=self._start)
            th.daemon = True
            th.start()

        def stop(self):
            """
            Stop the validator on its next loop
            """
            self.__quit = True

        def kill(self):
            """
            Kills the validator by joined its thread
            """
            self.stop()
            if self.__th:
                self.__th.join()


    def enable_tt_ff_mode():
        """
        Enables tt ff mode, hopefully to force people to never ever change clock
        """
        store.persistent._mas_pm_has_went_back_in_time = True
        store._mas_shatterAffection(current_evlabel="[invalid time, possible data corruption]")

    def has_broken_spacetime_fabric():
        """
        Check if the player has fooked up with time
        """
        return (
            store.mas_seenEvent("mas_broke_spacetime_fabric")
            or store.mas_getEVL_shown_count("mas_broke_spacetime_fabric")
        )

    def generate_poem(line_len_range=(4, 31), lines_number_range=(17, 26)):
        """
        Generates a psedo random poem for tt ff
        """
        lines = [
            store.glitchtext(random.randint(*line_len_range))
            for i in range(random.randint(*lines_number_range))
        ]
        lines.append("\n ???\n")
        return "\n ".join(lines)
