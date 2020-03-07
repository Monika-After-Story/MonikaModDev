default persistent._mas_player_sesh_log = dict()
default persistent._mas_last_checkout = None

init 10 python:
    mas_scheduling.calculateDailyAverages()

init python in mas_scheduling:
    import datetime
    import store

    ##GLOBAL VARIABLES

    #Dict storing the average time out timedelta
    # key: type
    # value: average timedelta for the time out
    AVERAGE_TD_OUT = dict()

    #Dict storing the average checkout time
    # key: type
    # value: average checkout time for type
    AVERAGE_T_CHECKOUT = dict()

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
            _now,
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

    def calculateDailyAverages():
        """
        Sets the global variables for checkout time averages and time out timedelta averages
        """
        global AVERAGE_TD_OUT
        global AVERAGE_T_CHECKOUT

        curr_weekday = datetime.datetime.now().weekday()
        for _type in store.persistent._mas_player_sesh_log:
            AVERAGE_T_CHECKOUT[_type], AVERAGE_TD_OUT[_type] = averageTimes(_type, curr_weekday)
