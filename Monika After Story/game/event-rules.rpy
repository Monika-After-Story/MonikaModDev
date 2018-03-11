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
        Each rule is defined by a repeat which specifies the time interval for
        the repetition and an advance_by which specifies how many of the time
        intervals the next repetition is going to get scheduled.
        The repetition rule increases the event start_date and end_date and
        works seamlessly with the current calendar function.
        """

        # tuple constants
        NUM_RULE_T_NAMES = {
            "repeat":0,
            "advance_by":1
        }

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

            # sanity check if we don't have a rule or event we raise an Exception
            if ev is None or rule is None:
                raise Exception("Evaluate rule needs an Event and a Rule")

            # sanity check 2 if we don' have start_date and end_date we raise an Exception
            if ev.start_date is None or ev.end_date is None:
                raise Exception("Event must contain an start_date and end_date to use Numerical rules")

            # call update dates to get the new start and end dates
            ev.start_date, ev.end_date = MASNumericalRepeatRule.update_dates(ev.start_date, ev.end_date, rule, check_time)

            # finally check if the event is available for the given datetime
            if ev.start_date <= check_time <= ev.end_date:

                return True

            return False

    class MASSelectiveRepeatRule(object):
        """
        Static Class used to create selective repetition rules in tuple form.
        Each rule is defined by a list of acceptable values for that rule.
        The rules then are evaluated against the current datetime.
        """

        # tuple constants
        SEL_RULE_T_NAMES = {
            "seconds":0,
            "minutes":1,
            "hours":2,
            "days":3,
            "weekdays":4,
            "months":5,
            "years":6
        }

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
                a tuple (seconds, minutes, hours, days, months, years), containing
                the specified rules
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

            # return as a tuple
            return (seconds, minutes, hours, days, weekdays, months, years)

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
            seconds, minutes, hours, days, weekdays, months, years = rule

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
        Each rule is defined by a skip_visual boolean and a special random chance.
        skip_visual is used to store if the greeting should be executed without
        executing the normal visual setup, this is useful for special greetings
        random_chance is used to define the 1 in random_chance chance that this
        greeting can be called
        """

        # tuple constants
        GREET_RULE_T_NAMES = {
            "skip_visual":0,
            "random_chance":1
        }

        @staticmethod
        def create_rule(skip_visual=False, random_chance=0):
            """
            IN:
                skip_visual - A boolean stating wheter we should skip visual
                    initialization
                random_chance - An int used to determine 1 in random_chance
                    special chance for this greeting to appear

            RETURNS:
                a tuple (skip_visual, random_chance), containing the specified rules
            """

            # random_chance can't be negative
            if random_chance < 0:
                raise Exception("random_chance can't be negative")

            # return the tuple
            return (skip_visual, random_chance)

        @staticmethod
        def evaluate_rule(rule):
            """
            IN:
                rule - the MASGreetingRule to check it's random_chance

            RETURNS:
                True if the random returned 1
            """

            # check if random_chance is 0 return False
            if rule[MASGreetingRule.GREET_RULE_T_NAMES["random_chance"]] == 0:
                return False

            # Evaluate randint with a chance of 1 in random_chance
            return random.randint(1,rule[MASGreetingRule.GREET_RULE_T_NAMES["random_chance"]]) == 1

        @staticmethod
        def should_skip_visual(rule):

            # returns the skip_visual boolean
            return rule[MASGreetingRule.GREET_RULE_T_NAMES["skip_visual"]]

        @staticmethod
        def check_visual_skip_in_rules(rules):
            """
            checks in the rules dict if the MASGreetingRule exists
            if it exists returns the skip_visual value otherwise returns False

            IN:
                rules - the rules dict to check

            RETURNS:
                The value of skip_visual, False if it doesn't exists
            """

            if EV_RULE_GREET_RANDOM in rules:
                return MASGreetingRule.should_skip_visual(rules[EV_RULE_GREET_RANDOM])
            else:
                return False

    def mas_create_rules(**kwargs):
        """
        helper method used to create Event rules in an easy way,
        it accepts all the current rules arguments and creates
        the appropriate rule for each given argument

        IN:
            MASNumericalRepeatRule args:
                repeat - An EV_NUM_RULE, that determines the time unit we'll be
                    using to increment the start_date and end_date
                advance_by - A positive integer used to determine how many times
                    the desired time unit will be added to start_date and
                    end_date

            MASSelectiveRepeatRule args:
                seconds -  list of seconds this rule will match to
                minutes - list of minutes this rule will match to
                hours - list of hours this rule will match to
                days - list of days this rule will match to
                weekdays - list of weekdays this rule will match to
                months - list of months this rule will match to
                years - list of years this rule will match to

            MASGreetingRule args:
                skip_visual - A boolean stating wheter we should skip visual
                    initialization
                random_chance - An int used to determine 1 in random_chance
                    special chance for this greeting to appear

        RETURNS:
            A dict containing only the defined rules, if no rules were created it
            returns an empty dict
        """

        # empty dict to store the created rules
        rules = dict()

        # if no arguments given return an empty dict
        if kwargs is None:
            return rules

        # check if we have any of the possible arguments for Greeting rule
        if any((True for x in MASGreetingRule.GREET_RULE_T_NAMES.keys() if x in kwargs.keys())):

            # retrieve values from the arguments
            skip_visual = False
            random_chance = 0

            if "skip_visual" in kwargs:
                skip_visual = kwargs["skip_visual"]
            if "random_chance" in kwargs:
                random_chance = kwargs["random_chance"]

            # create the rule and add it to rules
            rules[EV_RULE_GREET_RANDOM] = MASGreetingRule.create_rule(skip_visual,random_chance)

        # check if we have any of the possible arguments for Selective repeat rule
        if any((True for x in MASSelectiveRepeatRule.SEL_RULE_T_NAMES.keys() if x in kwargs.keys())):

            # retrieve values from the arguments
            seconds = None
            minutes = None
            hours = None
            days = None
            weekdays = None
            months = None
            years = None

            if "seconds" in kwargs:
                seconds = kwargs["seconds"]
            if "minutes" in kwargs:
                minutes = kwargs["minutes"]
            if "hours" in kwargs:
                hours = kwargs["hours"]
            if "days" in kwargs:
                days = kwargs["days"]
            if "weekdays" in kwargs:
                weekdays = kwargs["weekdays"]
            if "months" in kwargs:
                months = kwargs["months"]
            if "years" in kwargs:
                years = kwargs["years"]

            # create the rule and add it to rules
            rules[EV_RULE_RP_SELECTIVE] = MASSelectiveRepeatRule.create_rule(seconds, minutes, hours, days, weekdays, months, years)

        # check if we have any of the possible arguments for Selective repeat rule
        if any((True for x in MASNumericalRepeatRule.NUM_RULE_T_NAMES.keys() if x in kwargs.keys())):

            # retrieve values from the arguments
            repeat = None
            advance_by = 1

            if "repeat" in kwargs:
                repeat = kwargs["repeat"]
            if "advance_by" in kwargs:
                advance_by = kwargs["advance_by"]

            # create the rule and add it to rules
            rules[EV_RULE_RP_NUMERICAL] = MASNumericalRepeatRule.create_rule(repeat, advance_by)

        # return the rules dict
        return rules
