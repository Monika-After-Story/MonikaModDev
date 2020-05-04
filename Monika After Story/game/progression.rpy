# Module that defines functions for handling game progression and leveling up


default persistent._mas_xp_rst = datetime.date.today()
# date we last reset the xp lvl rate

default persistent._mas_xp_hrx = 0.0
# number of hours we have spent with monika today (and have been used for xp)

default persistent._mas_xp_tnl = 420.0
# amount of xp to reach the next level

default persistent._mas_xp_lvl = 0
# current level


init python in mas_xp:
    import math
    import datetime
    import store
    import store.mas_utils as mas_utils


    RATE_HOUR = 2
    # the amount of hours we use per rate

    DEF_XP_RATE = 60.0
    # amount of xp gain per hour

    XP_LVL_RATE = 420.0
    # amount of xp per lvl

    xp_rate = DEF_XP_RATE
    # how much xp / hour
    # always start at 60, but this changes overtime

    prev_grant = datetime.datetime.now()
    # previous time we ran the grant xp alg


    def _calc(xp_rate, start, end, hrx):
        """
        Calculates xp gained within a range

        IN:
            xp_rate - starting rate to calc xp with
            start - datetime to begin calculating xp with
            end - datetime to end calculating xp with
            hrx - hours today that have already been applied to xp

        RETURNS: tuple:
            [0] - xp gained
            [1] - new xp_rate to use
            [2] - new amount of hours that we have applied xp rate to
        """
        xp_gain = 0.0

        # obtain hour pieces so we can figure out the amt to apply rate on
        diff_hr = mas_utils.td2hr(end - start)
        hrx_i, hrx_f = mas_utils.floatsplit(hrx)

        # determine amt of time we applied the current rate to
        comp_amt = RATE_HOUR - (hrx_f + (hrx_i % 2))

        # and use that to determine how much time shoud be applied to
        # current rate
        if comp_amt > diff_hr:
            # since diff is smaller than completion, we just need to apply
            # current rate to diff amt
            xp_gain += diff_hr * xp_rate

        else:
            # since diff is larger/equal than completion, apply the
            # current rate to the comp amt and run alg on the remaining
            xp_gain += comp_amt * xp_rate
            alg_amt = diff_hr - comp_amt
            gains, xp_rate = calc_by_hours(alg_amt, xp_rate / 2.0)
            xp_gain += gains

        return xp_gain, xp_rate, hrx + diff_hr


    def calc():
        """
        Calculates xp gained since last call to calc

        Sets globals as needed

        RETURN: amt of xp gained since last call to calc
        """
        global xp_rate, prev_grant

        now = datetime.datetime.now()

        # calculate xp gained
        xp_gain, xp_rate, new_hrx = _calc(
            xp_rate,
            prev_grant,
            now,
            store.persistent._mas_xp_hrx
        )

        # now set state values as appropriate
        prev_grant = now
        store.persistent._mas_xp_hrx = new_hrx

        return xp_gain


    def calc_by_hours(duration, start_rate):
        """
        Calculates toatl xp gain given a duration (in hours) and starting rate
        using the new XP model

        IN:
            duration - amt of time to grant xp for (hours)
            start_rate - the rate to start calculating with

        RETURNS: tuple of the following format:
            [0] - amt of xp gained (float)
            [1] - new rate (float)
        """
        # Alg is as follows
        # 1. first 2 hours of playtime is used at the given start rate
        # 2. every subsequent 2 hours is gets multipled by half the given
        #   rate. This is recurisve
        # 3. once the rate is below 1, the rate stays at 1

        hours = duration
        rate = start_rate
        xp = 0

        while hours > 0:

            if rate > 1:
                if hours < RATE_HOUR:
                    xp += hours * rate

                else:
                    xp += RATE_HOUR * rate
                    rate /= 2.0

                hours -= RATE_HOUR

            else:
                xp += hours * 1
                hours = 0
                rate = 1

        return xp, rate


    def calc_by_time(duration, start_rate):
        """
        Calculates total xp gain given a duration and starting rate using
        the new XP model

        IN:
            duration - amount of time to grant xp for (timedelta)
            start_rate - the rate to start calctuing with

        RETURNS: tuple of the following format:
            [0] - amt of xp gained (float)
            [1] - new rate (float)
        """
        return calc_by_hours(mas_utils.td2hr(duration), start_rate)


    def _grant(xp, xptnl):
        """
        Internal version of grant. dont use

        IN:
            xp - amount of xp to grant
            xptnl - current xp to next level

        RETURNS: tuple:
            [0] - lvls gained
            [1] - new xp tnl
        """
        if xp < xptnl:
            # no levels to be added
            return 0, xptnl - xp

        # add levels
        lvl_gained, xp_remain = _level_rxp(xp - xptnl)

        # 1 level for going over the tnl
        return 1 + lvl_gained, XP_LVL_RATE - xp_remain


    def _grant_on_pt():
        """
        Grants xp by calcuating avgs using the current playtime

        RETURNS: tuple:
            [0] - lvls gained
            [1] - new xp tnl
        """
        total_pt_hr = mas_utils.td2hr(store.mas_getTotalPlaytime())
        dsf = float(
            (datetime.date.today() - store.mas_getFirstSesh().date()).days
        )

        if dsf > 0:
            # calculate xp based on avg playtime per day
            xp_gained, rate = calc_by_hours(total_pt_hr / dsf, DEF_XP_RATE)

            # apply that as xp
            return _grant(xp_gained * dsf, XP_LVL_RATE)

        return 0, XP_LVL_RATE


    def _grant_xp(xp):
        """
        Grant abitrary xp. You better have a good reason to use this.

        IN:
            xp - arbitrary xp to grant
        """
        # grant xp
        lvl_gained, new_xptnl = _grant(xp, store.persistent._mas_xp_tnl)

        # unlock prompts
        for x in range(lvl_gained):
            store.queueEvent("unlock_prompt")

        # set xp and lvls
        store.persistent._mas_xp_lvl += lvl_gained
        store.persistent._mas_xp_tnl = new_xptnl


    def grant():
        """
        Grants xp based on current state. Meant for use by ch30 code
        """
        # no gain for time travelers
        if store.mas_TTDetected():
            return

        _grant_xp(calc())


    def _level(xp):
        """
        gets level using based on an amt of xp

        NOTE: do NOT use this to determine level. use level() instead

        IN:
            xp - amt of xp to calculate level for

        RETURNS: level based on xp
        """
        # new xp model
        lvls, lvls_f = _level_rxp(xp)
        return lvls


    def _level_rxp(xp):
        """
        Gets gained levels and remaining xp

        IN:
            xp - amt of xp to calculate level for

        RETURNS: tuple of the following format:
            [0] - lvls gained
            [1] - remainig xp
        """
        lvls, lvl_frac = mas_utils.floatsplit(xp / XP_LVL_RATE)
        return lvls, lvl_frac * XP_LVL_RATE


    def level():
        """
        Gets current level

        RETURNS: current level
        """
        return store.persistent._mas_xp_lvl


    def set_xp_rate():
        """
        Sets xp rate based on session time today
        Also resets reset date if appropriate

        NOTE: assumes that we are calling this once at a new session start
        """
        global xp_rate

        today = datetime.date.today()

        if store.persistent._mas_xp_rst < today:
            # today's date is newer than previous reset date, we are good
            # to reset to full default
            store.persistent._mas_xp_rst = today
            store.persistent._mas_xp_hrx = 0.0
            xp_rate = DEF_XP_RATE
            return

        if today < store.persistent._mas_xp_rst:
            # you time traveled or you crossed the date line.
            if not store.mas_TTDetected():
                # must have crossed the date line. you get a pass for now
                store.persistent._mas_xp_rst = today
                store.persistent._mas_xp_hrx = 0.0
                xp_rate = DEF_XP_RATE
            return

        # otherwise, we need to look at hrx data
        xp_rate = (
            DEF_XP_RATE / (2.0 ** int(store.persistent._mas_xp_hrx / 2.0))
        )
        if xp_rate < 1:
            xp_rate = 1.0


init python:

    def grant_xp(experience):
        """DEPRECATED
        This does not do anything anymore. Around for compatibility
        purposes
        """
        pass


    def get_level():
        """DEPRECATED
        This does not do anything anymore. Around for compatibility purposes
        """
        return 0
