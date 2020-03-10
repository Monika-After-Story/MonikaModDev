default persistent._mas_player_sesh_log = dict()
default persistent._mas_last_checkout = None

init python in mas_scheduling:
    import datetime
    import store
    import math

    ##GLOBAL VARIABLES

    #Dict storing the average time out timedelta
    # key: type
    # value: average timedelta for the time out
    AVERAGE_TD_OUT = dict()

    #Dict storing the average checkout time
    # key: type
    # value: average checkout time for type
    AVERAGE_T_CHECKOUT = dict()

    #Dict storing the standard deviation timedelta for time out
    # key: type
    # value: standard deviation timedelta for the time out
    STD_DEV_TD_OUT = dict()

    #Dict storing the standard deviation timedelta for checkout time
    # key: type
    # value: standard deviation timedelta for checkout time
    STD_DEV_TD_CHECKOUT = dict()

    #Dict storing the standard error timedelta for time out
    # key: type
    # value: standard error timedelta for time out
    STD_ERR_TD_OUT = dict()

    #Dict storing the standard error timedelta for checkout time
    # key: type
    # value: standard error timedelta for checkout time
    STD_ERR_TD_CHECKOUT = dict()

    #Dict representing the base storage for each type
    __BASE_TIME_LOG = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: []
        }

    GREETING_TYPE_BLACKLIST = [
        None,
        store.mas_greetings.TYPE_LONG_ABSENCE,
        store.mas_greetings.TYPE_SICK,
        store.mas_greetings.TYPE_GAME,
        store.mas_greetings.TYPE_RESTART,
        store.mas_greetings.TYPE_GO_SOMEWHERE,
        store.mas_greetings.TYPE_GENERIC_RET,
        store.mas_greetings.TYPE_HOL_O31_TT
    ]

    def __average_t(time_list, ignore_last=False):
        """
        Private datetime.time averager

        IN:
            time_list:
                list of datetime.time objects
            ignore_last:
                Whether or not we should ignore the last entry in the list
                This should be used if the last entry of the list is a non-completed checkin
                (Default: False)
        OUT:
            datetime.time object representing the average time of the time_list
        """
        hour_sum = 0
        minute_sum = 0

        amt_entries = len(time_list)

        #No point in iterating over one item
        if amt_entries == 1:
            return time_list[0]

        for time_index in range(amt_entries):
            if (
                not ignore_last
                or (ignore_last and time_index != amt_entries - 1)
            ):
                hour_sum += time_list[time_index].hour
                minute_sum += time_list[time_index].minute

        if ignore_last:
            amt_entries -= 1

        hour_avg = hour_sum / amt_entries
        minute_avg = minute_sum / amt_entries


        return datetime.time(hour=hour_avg, minute=minute_avg)

    def __average_td(timedelta_list, ignore_last=False):
        """
        Private datetime.timedelta averager

        IN:
            timedelta_list:
                List of datetime.timedelta objects
            ignore_last:
                Whether or not we should ignore the last entry in the list
                This should be used if the last entry of the list is a non-completed checkin
                (Default: False)

        OUT:
            datetime.timedelta representing the average timedelta of the timedelta_list
        """
        average_total_seconds = 0
        amt_entries = len(timedelta_list)

        #No point in iterating over one item
        if amt_entries == 1:
            return timedelta_list[0]

        for td_index in range(amt_entries):
            if (
                not ignore_last
                or (ignore_last and td_index != amt_entries - 1)
            ):
                average_total_seconds += timedelta_list[td_index].total_seconds()

        if ignore_last:
            amt_entries -= 1

        return datetime.timedelta(seconds=(average_total_seconds / amt_entries))

    def __getCheckoutList(_type, weekday):
        """
        Private checkout time list getter

        IN:
            _type:
                The type of checkout
            weekday:
                The weekday we want to get the checkout list for

        OUT:
            list of time objects of each checkout for the type provided on the weekday provided
        """
        if _type not in store.persistent._mas_player_sesh_log:
            return list()

        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        checkout_time_list = list()
        for sesh in seshs:
            checkout_time_list.append(sesh[0])

        return checkout_time_list

    def __getTimeOutList(_type, weekday):
        """
        Private time out timedelta list getter

        IN:
            _type:
                The type of checkout
            weekday:
                The weekday we want to get the time out list for

        OUT:
            list of timedeltas of each time out for the type provided on the weekday provided
        """
        if _type not in store.persistent._mas_player_sesh_log:
            return list()

        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        time_out_list = list()
        for sesh in seshs:
            time_out_list.append(sesh[1])

        return time_out_list

    def __toDatetime(_time, _now=None):
        """
        Parses a datetime.time object into datetime.datetime object

        IN:
            _time:
                datetime.time object to convert
            _now:
                If provided, will generate a combined datetime using the current time
                (Default: None)
        OUT:
            datetime.datetime object representing the parsed passed in time

        NOTE: yyyy/mm/dd will all be set to 1 if _now is None as we only care about the hh/mm values
        """
        if _now is None:
            _now = datetime.datetime(1, 1, 1)

        return datetime.datetime.combine(
            _now,
            _time
        )

    def isBlacklistedType():
        """
        Checks if the current stored greeting is a blacklisted type

        OUT:
            boolean:
                True if the greeting type is blacklisted
                False otherwise
        """
        global GREETING_TYPE_BLACKLIST

        return store.persistent._mas_greeting_type in GREETING_TYPE_BLACKLIST

    def checkout(_type="general"):
        """
        Logs session end for user

        IN:
            _type:
                The type of farewell used
                (Default: 'general')
        """
        global __BASE_TIME_LOG

        #First, we need to add the type
        if _type not in store.persistent._mas_player_sesh_log:
            store.persistent._mas_player_sesh_log[_type] = __BASE_TIME_LOG.copy()

        #Now we get the current time
        _now = datetime.datetime.now()

        #And log this checkout
        store.persistent._mas_player_sesh_log[_type][_now.weekday()].append((
            _now.time(),
            None
        ))

        #Now log the last set of data which we can use to checkin again
        store.persistent._mas_last_checkout = (_type, _now.weekday())

    def checkin():
        """
        Used to check the user back in (complete the log)

        NOTE: Will do nothing if we don't have a proper last_checkout
        """
        #First, let's make sure we have a last entry
        if not store.persistent._mas_last_checkout:
            return

        #Now, let's get the last entry
        _type, _weekday = store.persistent._mas_last_checkout
        store.persistent._mas_last_checkout = None

        _checkout_time, _out_timedelta = store.persistent._mas_player_sesh_log[_type][_weekday][-1]

        #If the checkin time isn't None, that means the last session had a crash and we didn't check out properly
        if _out_timedelta is not None:
            return

        abs_len = store.mas_getAbsenceLength()

        #If we should log the entry, we'll complete it and add our checkin time
        if shouldLogEntry(_type, _checkout_time, abs_len, _weekday):
            store.persistent._mas_player_sesh_log[_type][_weekday][-1] = (_checkout_time, store.mas_getAbsenceLength())

        #Otherwise, this entry is what we're used to seeing. We can remove it as there's no new data to gain here
        else:
            store.persistent._mas_player_sesh_log[_type][_weekday].pop(-1)

    def averageTimes(_type, weekday):
        """
        Averages the datetime.time and datetime.timedelta objects for the type and weekday provided

        IN:
            _type:
                type of checkout to average
            weekday:
                weekday we'd like to average

        OUT:
            Tuple:
                [0] - average checkout time (datetime.time)
                [1] - average time out (timedelta)
        """
        if _type not in store.persistent._mas_player_sesh_log:
            return datetime.time(), datetime.time()

        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        if not seshs:
            return datetime.time(), datetime.time()

        ignore_last = bool(store.persistent._mas_last_checkout) and _type in store.persistent._mas_last_checkout

        #Now that we've got the seshs, let's build a list for each
        checkouts = __getCheckoutList(_type, weekday)
        time_outs = __getTimeOutList(_type, weekday)

        avg_checkout = __average_t(checkouts, ignore_last)
        avg_timeout = __average_td(time_outs, ignore_last)

        return avg_checkout, avg_timeout

    def calculateDailyAverages(weekday=None):
        """
        Sets the global variables for checkout time averages and time out timedelta averages

        IN:
            weekday:
                if provided, will calculate the daily averages (and set the global variables accordingly)
                to the average checkout time and average time out globals for the weekday provided
                If not provided, the current day of the week is assumed
                (Default: None)

        TODO: Ignore additions to checkin/out if the times fall within the standard deviation, plus purge if list is too big
        storing average elsewhere
        """
        global AVERAGE_TD_OUT
        global AVERAGE_T_CHECKOUT
        global STD_DEV_TD_OUT
        global STD_DEV_TD_CHECKOUT
        global STD_ERR_TD_OUT
        global STD_ERR_TD_CHECKOUT

        curr_weekday = datetime.datetime.now().weekday()
        for _type in store.persistent._mas_player_sesh_log:
            #NOTE: This order is important. Average -> Standard Deviation -> Standard Error
            AVERAGE_T_CHECKOUT[_type], AVERAGE_TD_OUT[_type] = averageTimes(_type, curr_weekday)
            STD_DEV_TD_CHECKOUT[_type], STD_DEV_TD_OUT[_type] = getStandardDeviaton(_type)
            STD_ERR_TD_CHECKOUT[_type], STD_ERR_TD_OUT[_type] = getStandardError(_type)

    def isWithinAverage(_type, _now=None):
        """
        Checks if the time provided is within the average recorded period

        IN:
            _type:
                Type of checkout we want to check
            _now:
                The time to check if within the average period (datetime.datetime)
                If None, now is assumed
                (Default: None)
        """
        global AVERAGE_T_CHECKOUT
        global AVERAGE_TD_OUT

        if _type not in store.persistent._mas_player_sesh_log:
            return False

        elif _now is None:
            _now = datetime.datetime.now()

        _checkout_average_dt = __toDatetime(AVERAGE_T_CHECKOUT[_type], _now)
        _timeout_average = AVERAGE_TD_OUT[_type]

        return _checkout_average_dt <= _now <= _checkout_average_dt + _timeout_average

    def isWithinStandardDeviationCheckout(_type, _now=None):
        """
        Checks if the time provided is within the checkout standard deviation

        IN:
            _type:
                Type of checkout to test
            _now:
                The time to check if within the standard deviation (datetime.datetime)
                If None, now is assumed
                (Default: None)

        OUT:
            Boolean:
                True if we're within the standard deviation for checkout
                False otherwise
        """
        global AVERAGE_T_CHECKOUT
        global STD_DEV_TD_CHECKOUT

        if _type not in store.persistent._mas_player_sesh_log:
            return False

        elif _now is None:
            _now = datetime.datetime.now()

        _checkout_average_dt = __toDatetime(AVERAGE_T_CHECKOUT[_type], _now)

        return _checkout_average_dt - STD_DEV_TD_CHECKOUT[_type] <= _now <= _checkout_average_dt + STD_DEV_TD_CHECKOUT[_type]

    def isWithinStandardDeviationCheckin(_type, _now=None):
        """
        Checks if the time provided is within the standard deviation for time out

        IN:
            _type:
                Type of checkout to test
            _now:
                The time to check if within the standard deviation (datetime.datetime)
                If None, now is assumed
                (Default: None)

        OUT:
            Boolean:
                True if we're within the standard deviation for time out
                False otherwise
        """
        global AVERAGE_T_CHECKOUT
        global AVERAGE_TD_OUT
        global STD_DEV_TD_OUT

        if _type not in store.persistent._mas_player_sesh_log:
            return False

        elif _now is None:
            _now = datetime.datetime.now()

        _checkin_average_dt = __toDatetime(AVERAGE_T_CHECKOUT[_type]) + AVERAGE_TD_OUT

        return _checkin_average_dt - STD_DEV_TD_OUT[_type] <= _now <= _checkin_average_dt + STD_DEV_TD_OUT[_type]

    def getStandardDeviaton(_type):
        """
        Gets the standard deviation for the checkout type provided (for both checkout time and time out)

        IN:
            _type:
                type of checkout to get the standard deviation for

        OUT:
            Tuple:
                [0] - Standard deviation timedelta for checkout time
                [1] - Standard deviation timedelta for return home time
        """
        global AVERAGE_T_CHECKOUT
        global AVERAGE_TD_OUT

        if _type not in store.persistent._mas_player_sesh_log:
            return datetime.timedelta()

        #Get current weekday
        weekday = datetime.datetime.now().weekday()

        s_chOut = 0
        s_tOut = 0
        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        #Before we do anything, we need to verify we have actual values so we don't have a zero division error
        if not seshs:
            return datetime.timedelta(), datetime.timedelta()

        #Now let's isolate functions and calculate. First the sigma
        for sesh in seshs:
            #We want to make sure that there's actually a non-none value here
            if sesh[1]:
                #The sum of [(sesh[0] - avg_checkout_time)^2]
                s_chOut += math.pow((__toDatetime(sesh[0]) - __toDatetime(AVERAGE_T_CHECKOUT[_type])).total_seconds(), 2)

                #The sum of [(sesh[1] - avg_timedelta_out)^2]
                s_tOut += math.pow(sesh[1].total_seconds() - AVERAGE_TD_OUT[_type].total_seconds(), 2)

        #Get N
        amt_entries = len(store.persistent._mas_player_sesh_log[_type][weekday])

        #Finish both ends of this and square root the sigma function divided by N
        return datetime.timedelta(seconds=math.sqrt(s_chOut/amt_entries)), datetime.timedelta(seconds=math.sqrt(s_tOut/amt_entries))

    def getStandardError(_type):
        """
        Gets standard error

        IN:
            _type:
                Type
        """
        global STD_DEV_TD_CHECKOUT
        global STD_DEV_TD_OUT

        #Verify type
        if _type not in store.persistent._mas_player_sesh_log:
            return dateimt.timedelta(), datetime.timedelta()

        #Get the current weekday
        weekday = datetime.datetime.now().weekday()

        #Simplify as this is used in both calculations
        sqrt_amt_entries = math.sqrt(len(store.persistent._mas_player_sesh_log[_type][weekday]))

        #Avoid a zero-division error
        if not sqrt_amt_entries:
            return dateimt.timedelta(), datetime.timedelta()

        #Now calculate the standard errors
        std_err_chkout = datetime.timedelta(seconds=(STD_DEV_TD_CHECKOUT[_type].total_seconds()/sqrt_amt_entries))
        std_err_out = datetime.timedelta(seconds=(STD_DEV_TD_OUT[_type].total_seconds()/sqrt_amt_entries))

        #And return
        return std_err_chkout, std_err_out

    def shouldLogEntry(_type, checkout_time, time_out, weekday):
        """
        Checks to see if the data we're going to store needs to be stored or not

        IN:
            _type:
                Type of entry we want to see if we should log
            checkout_time:
                datetime.time representing the time we checked out
            time_out:
                datetime.timedelta representing the amount of time out
            weekday:
                The weekday of the checkout

        RULES:
            1. We must have at least 10 entries in the log for the type and weekday to ignore
            2. The checkout time must be outside the average time +/- the standard deviation plus standard error to be logged
            3. The time out timedelta must be outside the average time +/- the standard deviation plus standard error to be logged

            NOTE: If EITHER 2 or 3 is True, the log is stored. Only if both are False is it discarded
        """
        global AVERAGE_TD_OUT
        global AVERAGE_T_CHECKOUT
        global STD_DEV_TD_OUT
        global STD_DEV_TD_CHECKOUT
        global STD_ERR_TD_OUT
        global STD_ERR_TD_CHECKOUT


        if len(store.persistent._mas_player_sesh_log[_type][weekday]) <= 10:
            return True

        ##Create the upper and lower bounds
        #For the out timedelta
        upper_bound_td_out = AVERAGE_TD_OUT[_type] + STD_DEV_TD_OUT[_type] + STD_ERR_TD_OUT[_type]
        lower_bound_td_out = AVERAGE_TD_OUT[_type] - STD_DEV_TD_OUT[_type] - STD_ERR_TD_OUT[_type]

        #For the checkout time
        upper_bound_t_checkout = __toDatetime(AVERAGE_T_CHECKOUT[_type]) + STD_DEV_TD_CHECKOUT[_type] + STD_ERR_TD_CHECKOUT[_type]
        lower_bound_t_checkout = __toDatetime(AVERAGE_T_CHECKOUT[_type]) - STD_DEV_TD_CHECKOUT[_type] - STD_ERR_TD_CHECKOUT[_type]

        #Just in case we've got bad data, we'll just forbid this from being saved
        if _time_out is None:
            return False

        #Otherwise, we're down to just the rules
        return (
            not (lower_bound_td_out <= time_out <= upper_bound_td_out)
            or not (lower_bound_t_checkout <= __toDatetime(checkout_time) <= upper_bound_t_checkout)
        )
