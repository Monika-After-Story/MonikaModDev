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


python early in mas_time:
    import time
    import threading
    import random

    import store

    class __Desync(object):
        NONE = 0
        MAJOR = 1
        MINOR = 2
        SYSTEM = 4

    class MASUptimeSyncValidator(object, store.NoRollback):
        """
        Validates uptime using clock
        """
        __SOFT_LIM = 3.3
        __HARD_LIM = 3720.0

        __slots__ = (
            "__log_obj",
            "__last_proc_clock",
            "__last_os_clock",
            "__start_ts",
            "__uptime",
            "__desync",
            "__desyncs",
            "__min_desync_count",
            "__last_min_desync",
            "__th",
        )

        def __init__(self, log=None):
            """
            Constructor:

            IN:
                log - the log object to use for logging purposes
            """
            self.__log_obj = log

            self.__last_proc_clock = 0.0
            self.__last_os_clock = 0.0

            self.__start_ts = 0.0
            self.__uptime = 0.0

            self.__desync = __Desync.NONE
            self.__desyncs = []
            self.__min_desync_count = 0
            self.__last_min_desync = 0.0

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

        def __start(self):
            """
            Starts the validator loop
            """
            self.__start_ts = time.time()
            while True:
                wait_time = float(random.randint(3, 7))
                self.__last_proc_clock = time.clock()
                self.__last_os_clock = time.time()

                time.sleep(wait_time)

                proc_change = time.clock() - self.__last_proc_clock
                os_change = time.time() - self.__last_os_clock

                proc_diff = proc_change - wait_time
                abs_proc_diff = abs(proc_diff)
                os_diff = os_change - wait_time
                abs_os_diff = abs(os_diff)

                self.__uptime += (proc_change if proc_change > 0.0 else wait_time)

                # This is the worst that can happen
                if (
                    (abs_os_diff > self.__HARD_LIM and abs_proc_diff < self.__HARD_LIM)
                    or (abs_os_diff > self.__SOFT_LIM and self.__min_desync_count >= 3)
                ):
                    self.__desync |= __Desync.MAJOR
                    self.__desyncs.append(os_diff)
                    self.__log_warning("Major uptime desync. POSSIBLE CORRUPTION: {} | {}".format(proc_diff, os_diff))
                    return

                # This is probably okay and we can handle smol shifts
                elif abs_os_diff > self.__SOFT_LIM:
                    if abs_proc_diff <= self.__SOFT_LIM:
                        if self.__uptime - self.__last_min_desync < 3600.0:
                            self.__min_desync_count += 1
                        self.__last_min_desync = self.__uptime

                    self.__desync |= __Desync.MINOR
                    self.__desyncs.append(os_diff)
                    self.__log_warning("Minor uptime desync. POSSIBLE CORRUPTION: {} | {}".format(proc_diff, os_diff))
                    return

                # This should never happen, reporting just in case, but probably would be terrible, too
                elif abs_proc_diff > self.__SOFT_LIM:
                    self.__desync |= __Desync.SYSTEM
                    self.__desyncs.append(os_diff)
                    self.__log_warning("Process desync. POSSIBLE SYSTEM ISSUES: {} | {}".format(proc_diff, os_diff))

                # Reset the counter if it's safe
                if (
                    self.__min_desync_count
                    and self.__uptime - self.__last_min_desync > 10800.0
                ):
                    self.__min_desync_count -= 1

        def _get_desyncs(self):
            """
            Returns a list of all desync gaps

            OUT:
                list[float]
            """
            return list(self.__desyncs)

        def _get_uptime(se_Desynclf):
            """
            Returns current update since launch
            """
            return self.__uptime

        def __is_desync(self, kind):
            """
            Returns a boolean indicating if there was a desync

            OUT:
                bool
            """
            return (self.__desync & kind) != 0

        def is_major_desync(self):
            """
            Checks if there was AT LEAST a major desync

            OUT:
                bool
            """
            return self.__is_desync(__Desync.MAJOR)

        def is_minor_desync(self):
            """
            Checks if there was AT LEAST a minor desync

            OUT:
                bool
            """
            return self.__is_desync(__Desync.MINOR)

        def is_system_desync(self):
            """
            Checks if there was AT LEAST a system desync

            OUT:
                bool
            """
            return self.__is_desync(__Desync.SYSTEM)

        def start(self):
            """
            Starts the validator by invoking its logic in a thread
            """
            self.__th = th = threading.Thread(target=self.__start)
            th.daemon = True
            th.start()


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
