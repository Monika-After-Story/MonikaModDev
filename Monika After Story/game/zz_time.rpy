# special time classes in case we have no timezones

python early:

    from pytz import tzinfo as pytz.tzinfo

    class MASLocalTz(pytz.tzinfo.StaticTzInfo):
        """
        Special Tz class that we use when we need to do dynamic timezone
        creation because we couldn't find existing timezone data.

        Despite using StaticTzInfo, this does respect DST, in the sense that
        we will use whatever offset the time library tells us to use.
        """
