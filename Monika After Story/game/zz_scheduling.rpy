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

    ##CONSTANTS

    #Const representing the maximum standard error amount (as a timedelta) which would let us be confident in our data
    MAX_TD_CONF = datetime.timedelta(minutes=5)

    #Const representing the minimum amount of time from the average (as a timedelta) which we can be confident in our data
    MIN_TD_CONF = datetime.timedelta(minutes=1)

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

    #Const
    #List holding all greeting types which are blacklisted from storing schedule data
    GREETING_TYPE_BLACKLIST = [
        None,
        store.mas_greetings.TYPE_LONG_ABSENCE,
        store.mas_greetings.TYPE_SICK,
        store.mas_greetings.TYPE_GAME,
        store.mas_greetings.TYPE_EAT_GENERIC,
        store.mas_greetings.TYPE_RESTART,
        store.mas_greetings.TYPE_GO_SOMEWHERE,
        store.mas_greetings.TYPE_GENERIC_RET,
        store.mas_greetings.TYPE_HOL_O31_TT
    ]

    ##START: Low level setup
    #START: Private functions
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
        #Firstly, make sure we have the type in the sesh log, otherwise there's no point in doing anything
        if _type not in store.persistent._mas_player_sesh_log:
            return list()

        #Get seshes
        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        #Build list
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
        #Firstly, make sure we have the type in the sesh log, otherwise there's no point in doing anything
        if _type not in store.persistent._mas_player_sesh_log:
            return list()

        #Get seshes
        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        #And build the list
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

    #START: Utility functions for logging
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

        #Firstly, ensure we have at least 10 entries before proceeding to check if we should ignore
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

        #Otherwise, we're down to the second two rules
        return (
            not (lower_bound_td_out <= time_out <= upper_bound_td_out)
            or not (lower_bound_t_checkout <= __toDatetime(checkout_time) <= upper_bound_t_checkout)
        )

    def calculateDailyAverages(weekday=None):
        """
        Sets the global variables for checkout time averages and time out timedelta averages

        IN:
            weekday:
                if provided, will calculate the daily averages (and set the global variables accordingly)
                to the average checkout time and average time out globals for the weekday provided
                If not provided, the current day of the week is assumed
                (Default: None)

        TODO: purge if list is too big, storing average elsewhere
        """
        global AVERAGE_TD_OUT
        global AVERAGE_T_CHECKOUT
        global STD_DEV_TD_OUT
        global STD_DEV_TD_CHECKOUT
        global STD_ERR_TD_OUT
        global STD_ERR_TD_CHECKOUT

        for _type in store.persistent._mas_player_sesh_log:
            #NOTE: This order is important. Average -> Standard Deviation -> Standard Error
            AVERAGE_T_CHECKOUT[_type], AVERAGE_TD_OUT[_type] = getAverages(_type)
            STD_DEV_TD_CHECKOUT[_type], STD_DEV_TD_OUT[_type] = getStandardDeviaton(_type)
            STD_ERR_TD_CHECKOUT[_type], STD_ERR_TD_OUT[_type] = getStandardError(_type)

    #START: Calculations for average/standard deviation/standard error
    def getAverages(_type):
        """
        Averages the datetime.time and datetime.timedelta objects for the type and weekday provided

        IN:
            _type:
                type of checkout to average

        OUT:
            Tuple:
                [0] - average checkout time (datetime.time)
                [1] - average time out (timedelta)
        """
        #First, need to make sure we have this type
        if _type not in store.persistent._mas_player_sesh_log:
            return datetime.time(), datetime.time()

        #Now let's get the weekday
        weekday = datetime.datetime.now().weekday()

        #Then get our sessions
        seshs = store.persistent._mas_player_sesh_log[_type][weekday]

        #If this is empty, we'll return both as empty times
        if not seshs:
            return datetime.time(), datetime.time()

        #We need to see if we should ignore the last entry for this iteration as it might be an incomplete log
        ignore_last = bool(store.persistent._mas_last_checkout) and _type in store.persistent._mas_last_checkout

        #Now that we've got the seshs, let's build a list for each
        checkouts = __getCheckoutList(_type, weekday)
        time_outs = __getTimeOutList(_type, weekday)

        #And get the averages
        avg_checkout = __average_t(checkouts, ignore_last)
        avg_timeout = __average_td(time_outs, ignore_last)

        return avg_checkout, avg_timeout

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

        #Data verification
        if _type not in store.persistent._mas_player_sesh_log:
            return datetime.timedelta()

        #Get current weekday
        weekday = datetime.datetime.now().weekday()

        #Do some setup
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
            return datetime.timedelta(), datetime.timedelta()

        #Get the current weekday
        weekday = datetime.datetime.now().weekday()

        #Simplify as this is used in both calculations
        sqrt_amt_entries = math.sqrt(len(store.persistent._mas_player_sesh_log[_type][weekday]))

        #Avoid a zero-division error
        if not sqrt_amt_entries:
            return datetime.timedelta(), datetime.timedelta()

        #Now calculate the standard errors
        std_err_chkout = datetime.timedelta(seconds=(STD_DEV_TD_CHECKOUT[_type].total_seconds()/sqrt_amt_entries))
        std_err_out = datetime.timedelta(seconds=(STD_DEV_TD_OUT[_type].total_seconds()/sqrt_amt_entries))

        #And return
        return std_err_chkout, std_err_out

    ##END: Low level setup


    ##START: Checkin/out functions
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

    def checkout(_type):
        """
        Logs session end for user

        IN:
            _type:
                The type of farewell used
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

    #START: End user functions
    #NOTE: For the following functions, we check using the average time for checkout and average timedelta for time out
    #With the combination of the standard deviation as our variance bounds
    def normallyOutNow(_type, _now=None):
        """
        Checks if the player is normally out for _type now

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
        global STD_DEV_TD_CHECKOUT
        global STD_DEV_TD_OUT

        #If we don't have the type, we return False as we have no data and cannot assume
        if _type not in store.persistent._mas_player_sesh_log:
            return False

        #Otherwise, let's get to work
        elif _now is None:
            _now = datetime.datetime.now()

        #Get our checkout average and timeout average
        _checkout_average_dt = __toDatetime(AVERAGE_T_CHECKOUT[_type], _now)
        _timeout_average = AVERAGE_TD_OUT[_type]

        return _checkout_average_dt - STD_DEV_TD_CHECKOUT[_type] <= _now <= _checkout_average_dt + _timeout_average + STD_DEV_TD_OUT

    def normallyLeavesNow(_type, _now=None):
        """
        Checks if the player normally leaves for _type now

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

        #Data verification
        if _type not in store.persistent._mas_player_sesh_log:
            return False

        #Otherwise, let's do the work
        elif _now is None:
            _now = datetime.datetime.now()

        #Get average checkout datetime
        _checkout_average_dt = __toDatetime(AVERAGE_T_CHECKOUT[_type], _now)

        return _checkout_average_dt - STD_DEV_TD_CHECKOUT[_type] <= _now <= _checkout_average_dt + STD_DEV_TD_CHECKOUT[_type]

    def normallyReturnsNow(_type, _now=None):
        """
        Checks if the player normally returns now for the given type

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

        #Data verification
        if _type not in store.persistent._mas_player_sesh_log:
            return False

        #Otherwise let's get to work
        elif _now is None:
            _now = datetime.datetime.now()

        #Build the average return datetime
        _checkin_average_dt = __toDatetime(AVERAGE_T_CHECKOUT[_type], _now) + AVERAGE_TD_OUT[_type]

        return _checkin_average_dt - STD_DEV_TD_OUT[_type] <= _now <= _checkin_average_dt + STD_DEV_TD_OUT[_type]

    def isReliable_tCheckout(_type):
        """
        Checks if the checkout time is within the reliable error range

        IN:
            _type:
                Type of checkout to test

        OUT:
            boolean:
                True if the standard error for checkout time is within the reliable error timedelta
                False otherwise
        """
        global MAX_TD_CONF
        global MIN_TD_CONF
        global STD_ERR_TD_CHECKOUT

        #Type check
        if _type not in STD_DEV_TD_CHECKOUT:
            return False

        return MIN_TD_CONF <= STD_DEV_TD_CHECKOUT[_type] <= MAX_TD_CONF

    def isReliable_tOut(_type):
        """
        Checks if the time out is within the reliable error range

        IN:
            _type:
                Typ of checkout to test

        OUT:
            boolean:
                True if the standard error for time out is within the reliable error timedelta
                False otherwise
        """
        global MAX_TD_CONF
        global MIN_TD_CONF
        global STD_ERR_TD_OUT

        #Type check
        if _type not in STD_DEV_TD_OUT:
            return False

        return MIN_TD_CONF <= STD_DEV_TD_OUT[_type] <= MAX_TD_CONF

#START: Scheduling topics
default persistent._mcal_event_map = dict()

#Startup calendar setup
init 700 python:
    for date, ev_list in persistent._mcal_event_map.iteritems():
        for mcal_event in ev_list:
            store.mas_calendar.addRepeatable_d(
                mcal_event["id"],
                mcal_event["name"],
                date,
                [] if mcal_event["repeatable"] else [date.year]
            )


#START: calendar event setup
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_calendar_event_setup",
            category=['calendar'],
            prompt="Can you put something on the calendar please?",
            unlocked=True,
            pool=True,
        )
    )

label mas_calendar_event_setup:
    m 1hub "Sure!"

    label .sel_day_loop:
        m 3eua "What day would you like the event to be on?"
        call mas_start_calendar_select_date

        if not _return:
            m 1eka "Oh, alright."

            m 1eua "Do you want to pick another date?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want to pick another date?{fast}"

                "Yes.":
                    m 1eub "Okay, [player]!"
                    jump .sel_day_loop

                "No.":
                    m 3eka "Alright, [player]."
                    m 3eua "Just let me know if you want me to remind you of something."
                    return

        #Now that we've got a date, let's make sure it's valid
        $ selected_date = _return.date()

        if selected_date < datetime.date.today():
            m 1hksdlb "We can't do something in the past silly."
            m 3hua "Try again~"
            jump .sel_day_loop

        else:
            m 1eua "Okay, [player]."
            m 3eua "What would you like to call the event?"
            label .sel_name_loop:
                $ ev_name = renpy.input("What would you like to call the event?", allow=letters_only+numbers_only, length=20).strip('\t\n\r')

                if mas_getCalendarEvent(ev_name, selected_date):
                    # TODO: exp here pls
                    m "[player], we already have an event with that name planned on that date!"
                    m 3eua "Choose another name."
                    jump .sel_name_loop

            m "Would you like me to repeat this event for you?{nw}"
            $ _history_list.pop()
            menu:
                m "Would you like me to repeat this event for you?{fast}"

                "Yes please.":
                    $ repeatable = True

                "No thanks.":
                    $ repeatable = False

            #TODO: How often would you like me to repeat this?

            m "Would you like me to remove the event after it ends?{nw}"
            $ _history_list.pop()
            menu:
                m "Would you like me to remove the event after it ends?{fast}"

                "Yes.":
                    $ auto_remove = True

                "No.":
                    $ auto_remove = False

            m 1hua "Perfect!"
            m 2dsa "Now let me just write that down.{w=0.5}.{w=0.5}.{nw}"

            $ mas_registerCalendarEvent(ev_name, selected_date, ev_category="custom", _repeat=repeatable, auto_remove=auto_remove)

            m 1hua "And done!"

    if persistent._mcal_event_map:
       $ mas_unlockEVL("mas_calendar_event_removal", "EVE")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_calendar_event_removal",
            prompt="Can you remove something from the calendar?",
            category=['calendar'],
            pool=True,
            unlocked=False,
            rules={"no unlock": None}
        )
    )

label mas_calendar_event_removal:
    $ removed_event = False

    m 1hub "Sure!"
    m 1eua "Pick the date which has the event you want to remove."

    label .sel_day_loop:
        call mas_start_calendar_select_date

        if not _return:
            m 1eka "Oh, alright."

            label .pick_again_menu:
                m 1eua "Would you like to pick another date?{nw}"
                $ _history_list.pop()
                menu:
                    m "Would you like to pick another date?{fast}"

                    "Yes.":
                        m 1eub "Okay, [player]!"
                        $ removed_event = False
                        jump .sel_day_loop

                    "No.":
                        m 3eka "Alright, [player]."
                        return

        #Now that we've got a date, let's make sure it's valid
        $ selected_date = _return.date()

        if selected_date not in persistent._mcal_event_map:
            m 1rksdlb "[player]... You never added something to the calendar on that date."
            jump .pick_again_menu

        else:
            label .remove_ev_loop:
                $ ev_list = persistent._mcal_event_map[selected_date]

                if len(ev_list) == 1:
                    if not removed_event:
                        m 3eua "Alright [player].{w=0.5} {nw}"
                        m 2esa "Let me just remove that for you.{w=0.5}.{w=0.5}.{nw}"

                    else:
                        m "Let me remove that last event from that day.{w=0.5}.{w=0.5}.{nw}"
                    $ mas_removeCalendarEvent(ev_list[0]["name"], selected_date)
                    m 1hub "Done!"

                    # TODO: exp
                    if persistent._mcal_event_map:
                        m "Would you like to remove something else?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Would you like to remove something else?{fast}"

                            "Yes.":
                                m 1eub "Okay, [player]!"
                                $ removed_event = False
                                jump .sel_day_loop

                            "No.":
                                m "Alright."

                else:
                    if not removed_event:
                        m 3eua "Looks like you've added more than one event on that day."

                    else:
                        m 3eua "Looks like you have more than one event on that day left, [player]."
                    show monika 1eua

                    python:
                        mcal_events = mas_buildMCalEventNameListMenu(selected_date)

                        final_item = ("Nevermind.", False, False, False, 20)

                        renpy.say(m, "Which event would you like to remove?", interact=False)

                    call screen mas_gen_scrollable_menu(mcal_events, mas_ui.SCROLLABLE_MENU_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, final_item)

                    $ selected_event = _return

                    if selected_event:
                        m 3eua "Alright [player].{w=0.5} {nw}"
                        m 2dsa "Let me just remove that for you.{w=0.5}.{w=0.5}.{nw}"
                        $ mas_removeCalendarEvent(selected_event, selected_date)
                        m 1hub "Done!"
                        # TODO: exp
                        if len(persistent._mcal_event_map) == 1:
                            $ button_yes = "Yes."
                        else:
                            $ button_yes = "Yes, from the same date."

                        m "Would you like to remove another event?{nw}"
                        $ _history_list.pop()
                        menu:
                            m "Would you like to remove another event?{fast}"

                            "Yes, from another date." if len(persistent._mcal_event_map) > 1:
                                m 1eub "Okay, [player]!"
                                jump .sel_day_loop

                            "[button_yes]":
                                m 1eub "Okay, [player]!"
                                $ removed_event = True
                                jump .remove_ev_loop

                            "No.":
                                m "Alright."

                    else:
                        m 1eka "Alright [player]."

    if not persistent._mcal_event_map:
       $ mas_lockEVL("mas_calendar_event_removal", "EVE")

    return

label mas_calendar_reminder:
    $ todays_event_str = mas_buildVerbalList(mas_buildMCalEventNameList())
    $ display_notif(m_name, ["It's [todays_event_str], [player]!"], "Reminders")
    if len(todays_event_str) == 1:
        m 1hub "It's [todays_event_str], [player]!"

    else:
        m 1eua "Hey, [player]!"
        m 3hub "Today's [todays_event_str]!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_scheduling_player_set_vacation_interval",
            prompt="I'm taking a vacation",
            # TODO: should it go in 'you' or 'calendar'?
            category=['calendar'],
            pool=True,
            unlocked=True
        )
    )

label mas_scheduling_player_set_vacation_interval:
    # TODO: what if you're alreay on vacation? Like you get some more days off?
    m "Taking a break from work, [player]?"
    m "Thanks for letting me know."
    m "Maybe I'll find something fun for us to do..."
    m "Could you tell me the timeframe of your vacation? {w=0.5}{nw}"
    extend "I'm your girlfriend after all~"
    # TODO: this's kinda forcibly? Like you have to choose
    # maybe ask if the player is ok to tell it?
    # TODO: what if the player don't know the end date?
    call mas_scheduling_select_interval
    # this _return should contain either a tuple of dates or None

    return

# NOTE: you'll need to queue this event via your scheduling system
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_scheduling_monika_ask_vacation_interval"
        )
    )

label mas_scheduling_monika_ask_vacation_interval:
    m "[player]..."
    m "I noticed that you've skipped some of your working days lately."
    m "It's just a guess, but..."
    m "Did you take some days off?{nw}"
    $ _history_list.pop()
    menu:
        m "Did you take some days off?{fast}"

        "Yes.":
            m "Oh, that's cool!"
            m "Do you mind if I ask the timeframe of your vacation?"
            call mas_scheduling_select_interval
            # this _return should contain either a tuple of dates or None

        "No.":
            m "Oh, alright."

        # "I got sick":
        #     pass

        # "I changed my working schedule.":
        #     pass
    return

label mas_scheduling_select_interval:
    label .sel_interval_loop:
        m "Please select two dates: the day it starts and the day it ends."
        call mas_start_calendar_select_dates
        $ vacation_interval = _return

    if not vacation_interval:
        m "[player], you need to choose a day."
        jump .sel_interval_loop

    elif len(vacation_interval) < 2:
        m "You need to select two dates, [player]."
        jump .sel_interval_loop

    elif vacation_interval[0] > vacation_interval[1]:
        m 1rksdlb "The vacation can't end in the past, [player]."
        m "Choose again~"
        jump .sel_interval_loop

    # we passed all checks, now let's ask the player if they chose the right dates
    $ text = mas_dateRangeToSpeech(vacation_interval[0], vacation_interval[1])

    m 3eua "So it's [text], right?{nw}"
    $ _history_list.pop()
    menu:
        m "So it's [text], right?{fast}"

        "Yes.":
            # TODO: she could mention what it's a long vacation or just a few days off
            m 1hub "Alright!"
            m "I hope the both of us will be able to enjoy your vacation~"
            m "Ahaha~"

        "No.":
            m 1eka "Oh, then... {w=0.5}{nw}"
            extend 3hua "Would you like to choose another two dates?{nw}"
            $ _history_list.pop()
            menu:
                m "Oh, then... Would you like to choose another two dates?{fast}"

                "Yes.":
                    jump .sel_interval_loop

                "No.":
                    m 1eka "Okay."
                    m "I really would like to spend more time with you~"
                    m "And getting some rest would never hurt you!"
                    m "Please let me know when you'll have a vacation."
                    return None

    return vacation_interval
