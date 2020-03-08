default persistent._mas_player_sesh_log = dict()
default persistent._mas_last_checkout = None

init 10 python:
    mas_scheduling.calculateDailyAverages()

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

    #Dict storing the standard deviation
    STD_DEV_TD_OUT = dict()

    STD_DEV_TD_CHECKOUT = dict()

    __BASE_TIME_LOG = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: []
        }

    def __average_t(time_list):
        """
        Private datetime.time averager

        IN:
            time_list:
                list of datetime.time objects

        OUT:
            datetime.time object representing the average time of the time_list
        """
        hour_sum = 0
        minute_sum = 0
        for _time in time_list:
            hour_sum += _time.hour
            minute_sum += _time.minute

        hour_avg = hour_sum / len(time_list)
        minute_avg = minute_sum / len(time_list)

        return datetime.time(hour=hour_avg, minute=minute_avg)

    def __average_td(timedelta_list):
        """
        Private datetime.timedelta averager

        IN:
            timedelta_list:
                List of datetime.timedelta objects

        OUT:
            datetime.timedelta representing the average timedelta of the timedelta_list
        """
        average_total_seconds = 0

        for td in timedelta_list:
            average_total_seconds += td.total_seconds()

        return datetime.timedelta(seconds=(average_total_seconds / len(timedelta_list)))

    def __getCheckoutList(_type, weekday):
        """
        Private checkout time list getter

        IN:
            _type:
                The type of checkout
            weekday:
                The weekday we want to get the checkout list for
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
        """
        if _type not in store.persistent._mas_player_sesh_log:
            return list()

        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        time_out_list = list()
        for sesh in seshs:
            time_out_list.append(sesh[1])

        return time_out_list

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

        #Complete the log and add our checkin time
        store.persistent._mas_player_sesh_log[_type][_weekday][-1] = (_checkout_time, store.mas_getAbsenceLength())

    def averageTimes(_type, weekday):
        """
        Averages the datetimes.

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


        #Now that we've got the seshs, let's build a list for each
        checkouts = __getCheckoutList(_type, weekday)
        time_outs = __getTimeOutList(_type, weekday)

        avg_checkout = __average_t(checkouts)
        avg_timeout = __average_td(time_outs)

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

        curr_weekday = datetime.datetime.now().weekday()
        for _type in store.persistent._mas_player_sesh_log:
            AVERAGE_T_CHECKOUT[_type], AVERAGE_TD_OUT[_type] = averageTimes(_type, curr_weekday)
            STD_DEV_TD_CHECKOUT[_type], STD_DEV_TD_OUT[_type] = getStandardDeviaton(_type)

    def isWithinAverage(_type, _now=None):
        """
        Checks if the time provided is within the average recorded period

        IN:
            _type:
                Type of checkout we want to check

            _now:
                The time to check if within the average period (datetime.datetime)
                If None, now is assumed

        TODO: Fix this for using datetime.time and datetime.timedelta
        """
        global AVERAGE_T_CHECKOUT
        global AVERAGE_TD_OUT

        if _type not in store.persistent._mas_player_sesh_log:
            return False

        elif _now is None:
            _now = datetime.datetime.now()

        _checkout_average = AVERAGE_T_CHECKOUT[_type]
        _timeout_average = AVERAGE_TD_OUT[_type]

        return _checkout_average <= _now <= _checkout_average + _timeout_average

    def getStandardDeviaton(_type):
        """
        Sets the standard deviation global variables

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

        def toDatetime(_time):
            """
            Parses a datetime.time object into datetime.datetime object

            IN:
                _time:
                    datetime.time object to convert

            OUT:
                datetime.datetime object representing the parsed passed in time

            NOTE: yyyy/mm/dd will all be set to 1 as we only care about the hh/mm values
            """
            return datetime.datetime.combine(
                datetime.datetime(1,1,1),
                _time
            )

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
            #The sum of [(sesh[0] - avg_checkout_time)^2]
            s_chOut += math.pow((toDatetime(sesh[0]) - toDatetime(AVERAGE_T_CHECKOUT[_type])).total_seconds(), 2)

            #The sum of [(sesh[1] - avg_timedelta_out)^2]
            s_tOut += math.pow(sesh[1].total_seconds() - AVERAGE_TD_OUT[_type].total_seconds(), 2)

        #Get N
        amt_entries = len(store.persistent._mas_player_sesh_log[_type][weekday])

        #Finish both ends of this and square root the sigma function divided by N
        return datetime.timedelta(seconds=math.sqrt(s_chOut/amt_entries)), datetime.timedelta(seconds=math.sqrt(s_tOut/amt_entries))
