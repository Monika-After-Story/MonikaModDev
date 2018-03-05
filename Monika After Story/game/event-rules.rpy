# Module that defines functions for handling game progression and leveling up

init python:

    # special constants for rule type identifiers for rule dict on Event class
    EV_RULE_RP_SELECTIVE = "rp_selective"
    EV_RULE_RP_NUMERICAL = "rp_numerical"


    # special constants for numerical repeat rules
    EV_NUM_RULE_DAY = "day"
    EV_NUM_RULE_WEEK = "week"
    EV_NUM_RULE_MONTH = "month"
    EV_NUM_RULE_YEAR = "year"

    # list of those constants
    EV_NUM_RULES = [
        EV_NUM_RULE_DAY,
        EV_NUM_RULE_WEEK,
        EV_NUM_RULE_MONTH,
        EV_NUM_RULE_YEAR
    ]

    class MASNumericalRepeatRule(object):
        """
        Static Class used to create numerical repetition rules in tuple form.
        Each rule is defined by a repeat which specifies the time interval for
        the repetition and an advance_by which specifies how many of the time
        intervals the next repetition is going to get scheduled.
        The repetition rule increases the event start_date and end_date and
        works seamlessly with the current calendar function.

        """
        @staticmethod
        def create_rule(repeat, advance_by=1):
            """
            IN:
                repeat - An EV_NUM_RULE, that determines the time unit we'll be
                    using to increment the start_date and end_date
                advance_by - A positive integer used to determine how many times
                    the desired time unit will be added to start_date and
                    end_date

            RETURNS:
                a tuple (repeat, advance_by), containing the specified rules

            """
            if repeat not in EV_NUM_RULES:
                raise Exception("'{0}' is not a valid repeat rule".format(repeat))
            elif advance_by > 0:
                return (repeat, advance_by)
            else:
                raise Exception("'{0}' is not a valid 'advance_by' rule, it should be a positive integer".format(repeat))

        @staticmethod
        def update_dates(start_date, end_date, rule, check_time):
            """
            IN:
                start_date - The Event's start date in datetime
                end_date - The Event's end_date in datetime
                rule - a MASNumericalRepeatRule tuple containing the rules for the
                    appropiate update
                check_time - The time to check and update against
            """

            # Check if the event is already in the future so we don't do anything
            if check_time < end_date:
                return (start_date, end_date)
            else:

                # we get the difference between end and start date
                delta = end_date - start_date

                # unpack the tuple for easy manipulation
                repeat, advance_by = rule

                # define and initialize the new_end_date with old end_date
                new_end_date = end_date

                # store current time
                current = datetime.datetime.now()

                # repeat the time additions until we get a date in the future
                while new_end_date < current:

                    # check if the rule is for days
                    if repeat == EV_NUM_RULE_DAY:

                        # use timedelta to add days and get the new_end_date
                        new_end_date = new_end_date + datetime.timedelta(days=advance_by)

                    # check if the rule is for weeks
                    elif repeat == EV_NUM_RULE_WEEK:

                        # use timedelta to add weeks and get the new_end_date
                        new_end_date = new_end_date + datetime.timedelta(weeks=advance_by)

                    # check if the rule is for months
                    elif repeat == EV_NUM_RULE_MONTH:
                        # use the add_months function to add the required amount of months
                        new_end_date = add_months(new_end_date,advance_by)

                    # check if the rule is for years
                    elif repeat == EV_NUM_RULE_YEAR:

                        # use the add_year function to add the required amount of years
                        new_end_date = add_years(new_end_date, advance_by)

                # finally we determine the new_start_date by subtracting the delta
                new_start_date = new_end_date - delta

                # return the new dates
                return (new_start_date, new_end_date)

            @staticmethod
            def evaluate_rule(check_time, ev=None, rule=None):
                if ev is None or rule is None:
                    return False
                ev.start_date, ev.end_date = update_dates(ev.start_date, ev.end_date, rule)
                if ev.start_date <= check_time <= ev.end_date:
                    return True
                return False

    class MASSelectiveRepeatRule(object):
        """
        Static Class used to create selective repetition rules in tuple form.
        Each rule is defined by a list of acceptable values for that rule.
        The rules then are evaluated against the current datetime.
        """

        @staticmethod
        def create_rule(seconds=None, minutes=None, hours=None, days=None, months=None, years=None):
            """
            NOTE: these values are assumed to be the same as stored in datetime

            IN:
                seconds - list of seconds this rule will match to
                minutes - list of minutess this rule will match to
                hours - list of hours this rule will match to
                days - list of days this rule will match to
                months - list of months this rule will match to
                years - list of years this rule will match to

            RETURNS:
                a tuple (seconds, minutes, hours, days, months, years), containing
                the specified rules
            """

            # check if seconds are defined that they are valid
            if seconds and all([(s < 0 and s > 59) for s in seconds]):
                raise Exception("seconds are out of a valid range")

            # check if valid minutes
            if minutes and all([(m < 0 and m > 59) for m in minutes]):
                raise Exception("minutes are out of a valid range")

            # check for invalid hours
            if hours and all([(h < 0 and h > 23) for h in hours]):
                raise Exception("hours are out of a valid range")

            # check for invalid days
            if days and all([(d < 1 and d > 31) for d in days]):
                raise Exception("days are out of a valid range")

            # check for invalid months
            if months and all([(m < 1 and m > 12) for m in months]):
                raise Exception("seconds are out of a valid range")

            # check for invalid years meaning from this year 2018 to 2100
            # Monika should be in our reality by then
            if months and all([(m < 2018 and m > 2100) for m in months]):
                raise Exception("seconds are out of a valid range")

            # return as a tuple
            return (seconds, minutes, hours, days, months, years)

        @staticmethod
        def evaluate_rule(check_time, rule=None):
            """
            Checks if the current_time is valid for the rule

            IN:
                rule - The rule tuple that contains the valid intervals to check
                    against
                check_time - The time to check against the rule

            RETURNS:
                A boolean value indicating if the time is in the defined interval
            """

            # unpack tuple for easy access
            seconds, minutes, hours, days, months, years = rule

            # check if current seconds are in the valid interval
            if seconds and check_time.second not in seconds:
                return False

            # check if current minutes are in the valid interval
            if minutes and check_time.minute not in minutes:
                return False

            # check if current hours are in the valid interval
            if days and check_time.day not in days:
                return False

            # check if current seconds are in the valid interval
            if months and check_time.month not in months:
                return False

            # check if current seconds are in the valid interval
            if years and check_time.year not in years:
                return False

            # since we passed all checks we return true to indicate that we comply
            # to that rule
            return True
