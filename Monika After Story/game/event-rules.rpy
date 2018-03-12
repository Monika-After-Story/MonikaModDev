# Module that defines static classes used to create the rule tuples used in the
# Event class.
# The static classes are the ones used to manipulate the rule tuples
# Each class has a method named evaluate_rule

init python:
    import datetime
    import random

    # special constants for rule type identifiers for the rule dict on Event class
    EV_RULE_RP_SELECTIVE = "rp_selective"
    EV_RULE_RP_NUMERICAL = "rp_numerical"
    EV_RULE_GREET_RANDOM = "greet_random"


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
        That tuple is then stored in a dict containing this rule name constant.
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
                a dict containing the specified rule with the appropriate key
            """

            # raise exception if repeat is not a valid rule
            if repeat not in EV_NUM_RULES:
                raise Exception("'{0}' is not a valid repeat rule".format(repeat))

            # since repeat is correct we just check if advance by is higher than 0
            if advance_by > 0:

                # return the dict containing the specified rule
                return {EV_RULE_RP_NUMERICAL : (repeat, advance_by)}

            # raise exception since advance by was 0 or lower
            raise Exception("'{0}' is not a valid 'advance_by' rule, it should be higher than 0".format(repeat))

        @staticmethod
        def update_dates(start_date, end_date, rule, check_time):
            """
            Updates the start_date and end_date to be the next possible dates
            checked against check_time
            IN:
                start_date - The Event's start date in datetime
                end_date - The Event's end_date in datetime
                rule - a MASNumericalRepeatRule tuple containing the rules for the
                    appropiate update
                check_time - The time to check and update against

            RETURNS:
                A tuple containing the new start_date and end_date
            """

            # Check if the event is already in the future so we don't do anything
            if check_time < end_date:
                return (start_date, end_date)

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
        def evaluate_rule(check_time, ev, rule=None):
            """
            Evaluates the rule given and updates the event's start_date and
            end_date

            IN:
                check_time - The datetime to check the rule against
                ev - The Event's to check
                rule - a MASNumericalRepeatRule tuple containing the rules for the
                    appropiate update

            RETURNS:
                True if the event date comply to the rule, False if it doesn't
            """

            rule_to_check = None

            # if the event contains the rule use that one
            if EV_RULE_RP_NUMERICAL in ev.rules:
                rule_to_check = ev.rules[EV_RULE_RP_NUMERICAL]

            # if we have a rule use that one instead
            if rule:
                rule_to_check = rule

            # sanity check if we don' have start_date, end_date and a rule we return False
            if ev.start_date is None or ev.end_date is None or rule_to_check is None:
                return False

            # call update dates to get the new start and end dates
            ev.start_date, ev.end_date = MASNumericalRepeatRule.update_dates(ev.start_date, ev.end_date, rule_to_check, check_time)

            # finally check if the event is available for the given datetime
            if ev.start_date <= check_time <= ev.end_date:
                return True

            return False

    class MASSelectiveRepeatRule(object):
        """
        Static Class used to create selective repetition rules in tuple form.
        That tuple is then stored in a dict containing this rule name constant.
        Each rule is defined by a list of acceptable values for that rule.
        The rules then are evaluated against the current datetime.
        """

        @staticmethod
        def create_rule(seconds=None, minutes=None, hours=None, days=None, weekdays=None, months=None, years=None):
            """
            NOTE: these values are assumed to be the same as stored in datetime

            IN:
                seconds - list of seconds this rule will match to
                minutes - list of minutess this rule will match to
                hours - list of hours this rule will match to
                days - list of days this rule will match to
                weekdays - list of weekdays this rule will match to
                months - list of months this rule will match to
                years - list of years this rule will match to

            RETURNS:
                a dict containing the specified rules
            """

            # check if seconds are defined that they are valid
            if seconds and any([(s < 0 or s > 59) for s in seconds]):
                raise Exception("seconds are out of a valid range")

            # check if valid minutes
            if minutes and any([(m < 0 or m > 59) for m in minutes]):
                raise Exception("minutes are out of a valid range")

            # check for invalid hours
            if hours and any([(h < 0 or h > 23) for h in hours]):
                raise Exception("hours are out of a valid range")

            # check for invalid days
            if days and any([(d < 1 or d > 31) for d in days]):
                raise Exception("days are out of a valid range")

            # check for invalid weekdays
            if weekdays and any([(d < 0 or d > 6) for d in weekdays]):
                raise Exception("weekdays are out of a valid range")

            # check for invalid months
            if months and any([(m < 1 or m > 12) for m in months]):
                raise Exception("months are out of a valid range")

            # check for invalid years meaning from this year 2018 to 2100
            # Monika should be in our reality by then
            if years and any([(y < 2018 or y > 2100) for y in years]):
                raise Exception("seconds are out of a valid range")

            # return as a dict
            return {EV_RULE_RP_SELECTIVE : (seconds, minutes, hours, days, weekdays, months, years)}

        @staticmethod
        def evaluate_rule(check_time, event=None, rule=None):
            """
            Checks if the current_time is valid for the rule

            IN:
                rule - The rule tuple that contains the valid intervals to check
                    against
                check_time - The time to check against the rule

            RETURNS:
                A boolean value indicating if the time is in the defined interval
            """

            rule_to_check = None

            #check if we have a rule defined
            if rule:
                rule_to_check = rule

            # check if we have an event that contains the rule we need
            # event rule takes priority so it's checked here
            if event and EV_RULE_RP_SELECTIVE in event.rules:
                rule_to_check = event.rules[EV_RULE_RP_SELECTIVE]

            # sanity check if we don't have a rule return False
            if rule_to_check is None:
                return False

            # unpack tuple for easy access
            seconds, minutes, hours, days, weekdays, months, years = rule_to_check

            # check if current seconds are in the valid interval
            if seconds and check_time.second not in seconds:
                return False

            # check if current minutes are in the valid interval
            if minutes and check_time.minute not in minutes:
                return False

            # check if hours are in the valid interval
            if hours and check_time.hour not in hours:
                return False

            # check if days are in the valid interval
            if days and check_time.day not in days:
                return False

            # check if weekdays are in the valid interval
            if weekdays and check_time.weekday() not in weekdays:
                return False

            # check if current months are in the valid interval
            if months and check_time.month not in months:
                return False

            # check if current years are in the valid interval
            if years and check_time.year not in years:
                return False

            # since we passed all checks we return true to indicate that we comply
            # to that rule
            return True

    class MASGreetingRule(object):
        """
        Static Class used to create greeting specific rules in tuple form.
        That tuple is then stored in a dict containing this rule name constant.
        Each rule is defined by a skip_visual boolean and a special random chance.
        skip_visual is used to store if the greeting should be executed without
        executing the normal visual setup, this is useful for special greetings
        random_chance is used to define the 1 in random_chance chance that this
        greeting can be called
        """

        @staticmethod
        def create_rule(skip_visual=False, random_chance=0):
            """
            IN:
                skip_visual - A boolean stating wheter we should skip visual
                    initialization
                random_chance - An int used to determine 1 in random_chance
                    special chance for this greeting to appear

            RETURNS:
                a dict containing the specified rules
            """

            # random_chance can't be negative
            if random_chance < 0:
                raise Exception("random_chance can't be negative")

            # return the tuple
            return {EV_RULE_GREET_RANDOM : (skip_visual, random_chance)}

        @staticmethod
        def evaluate_rule(event=None, rule=None):
            """
            IN:
                event - the event to evaluate
                rule - the MASGreetingRule to check it's random_chance

            RETURNS:
                True if the random returned 1
            """

            rule_to_check = None

            #check if we have a rule defined
            if rule:
                rule_to_check = rule

            # check if we have an event that contains the rule we need
            # event rule takes priority so it's checked here
            if event and EV_RULE_GREET_RANDOM in event.rules:
                rule_to_check = event.rules[EV_RULE_GREET_RANDOM]

            # sanity check if we don't have a rule return False
            if rule_to_check is None:
                return False

            # unpack the tuple for easy access
            skip_visual, random_chance = rule_to_check

            # check if random_chance is 0 return False
            if random_chance == 0:
                return False

            # Evaluate randint with a chance of 1 in random_chance
            return random.randint(1,random_chance) == 1

        @staticmethod
        def should_skip_visual(event=None, rule=None):
            """
            IN:
                event - the event to evaluate, gets priority
                rule - the MASGreetingRule to evaluate

            RETURNS:
                True if the rule is True to skip_visual
            """

            # returns the skip_visual boolean
            if event and EV_RULE_GREET_RANDOM in event.rules:
                return event.rules[EV_RULE_GREET_RANDOM][0]

            # returns the skip_visual boolean of the rule
            if rule:
                return rule[0]
                
            # False since there was no rule to check
            return False
