# Module that defines static classes used to create the rule tuples used in the
# Event class.
# The static classes are the ones used to manipulate the rule tuples
# Each class has a method named evaluate_rule

init -1 python:
    import datetime

    # special constants for rule type identifiers for the rule dict on Event class
    EV_RULE_RP_SELECTIVE = "rp_selective"
    EV_RULE_RP_NUMERICAL = "rp_numerical"
    EV_RULE_GREET_RANDOM = "greet_random"
    EV_RULE_FAREWELL_RANDOM = "farewell_random"
    EV_RULE_AFF_RANGE = "affection_range"


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
        def create_rule(repeat, advance_by=1, ev=None):
            """
            IN:
                repeat - An EV_NUM_RULE, that determines the time unit we'll be
                    using to increment the start_date and end_date
                advance_by - A positive integer used to determine how many times
                    the desired time unit will be added to start_date and
                    end_date
                    (Default: 1)
                ev - Event to add this rule to. This will replace exisiting
                    rules of the same key.
                    (Default: None)

            RETURNS:
                a dict containing the specified rule with the appropriate key
            """

            # raise exception if repeat is not a valid rule
            if repeat not in EV_NUM_RULES:
                raise Exception("'{0}' is not a valid repeat rule".format(repeat))

            # since repeat is correct we just check if advance by is higher than 0
            if advance_by > 0:

                rule = {EV_RULE_RP_NUMERICAL : (repeat, advance_by)}

                if ev:
                    ev.rules.update(rule)

                # return the dict containing the specified rule
                return rule

            # raise exception since advance by was 0 or lower
            raise Exception("'{0}' is not a valid 'advance_by' rule, it should be higher than 0".format(repeat))

        @staticmethod
        def update_dates(rule, check_time, ev=None, start_end_dates=None):
            """
            Updates the start_date and end_date to be the next possible dates
            checked against check_time

            IN:
                rule - a MASNumericalRepeatRule tuple containing the rules for the
                    appropiate update
                check_time - The time to check and update against
                ev - Event to update as well. This will update the existing
                    rules of the same key.
                    NOTE: this has priority over start_end_dates
                    (Default: None)
                start_end_date - tuple of the following format:
                    [0]: start_date
                    [1]: end_date
                    (Default: None)

            RETURNS:
                A tuple containing the new start_date and end_date. If bad
                values were given, (-1, -1) is returned
            """
            # sanity check
            if ev:
                # priortize event
                start_date = ev.start_date
                end_date = ev.end_date

            elif start_end_dates and len(start_end_dates) >= 2:
                # use range tuple
                start_date, end_date = start_end_dates

            else:
                # user gave us weird values
                return (-1, -1)

            # final check to ensure start and end date are appropriate
            if start_date is None or end_date is None:
                return (-1, -1)

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

            # update event if we have one
            if ev:
                ev.start_date = new_start_date
                ev.end_date = new_end_date

            # return the new dates
            return (new_start_date, new_end_date)

        @staticmethod
        def evaluate_rule(check_time, ev, rule=None, skip_update=False):
            """
            Evaluates the rule given and updates the event's start_date and
            end_date

            IN:
                check_time - The datetime to check the rule against
                ev - The Event to check and update
                rule - a MASNumericalRepeatRule tuple containing the rules for the
                    appropiate update
                    If passed in, we use this instead of the given event's rule
                    (Default: None)
                skip_update - True means we shoudl skip updating the given
                    Event's rule.
                    (Default: False)

            RETURNS:
                True if the event date comply to the rule, False if it doesn't
            """
            # sanity check
            if ev is None:
                return False

            # sanity check if we don' have start_date, end_date
            if ev.start_date is None or ev.end_date is None:
                return False

            # sanity check for a rule to use
            if rule is None:

                if EV_RULE_RP_NUMERICAL not in ev.rules:
                    return False

                # use event's rule if user didn't give us a rule
                rule = ev.rules[EV_RULE_RP_NUMERICAL]

            # if we skipping update, just check
            if skip_update:
                return ev.start_date <= check_time <= ev.end_date

            # call update dates to get the new start and end dates
            start_date, end_date = MASNumericalRepeatRule.update_dates(rule, check_time, ev=ev)

            # finally check if the event is available for the given datetime
            return start_date <= check_time <= end_date


    class MASSelectiveRepeatRule(object):
        """
        Static Class used to create selective repetition rules in tuple form.
        That tuple is then stored in a dict containing this rule name constant.
        Each rule is defined by a list of acceptable values for that rule.
        The rules then are evaluated against the current datetime.
        """

        @staticmethod
        def create_rule(
                seconds=None,
                minutes=None,
                hours=None,
                days=None,
                weekdays=None,
                months=None,
                years=None,
                ev=None
            ):
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
                ev - Event to store this rule in, if not None
                    (Default: None)

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
            rule = {EV_RULE_RP_SELECTIVE : (seconds, minutes, hours, days, weekdays, months, years)}

            if ev:
                ev.rules.update(rule)

            return rule

        @staticmethod
        def evaluate_rule(check_time, ev=None, rule=None):
            """
            Checks if the current_time is valid for the rule

            IN:
                check_time - The time to check against the rule
                ev - Event to check
                    NOTE: this takes prioriy over the rule param
                    (Default: None)
                rule - MASSelectiveRepeatRule to check
                    (Default: None)

            RETURNS:
                A boolean value indicating if the time is in the defined interval
            """
            # check if we have an event that contains the rule we need
            # event rule takes priority so it's checked here
            if ev and EV_RULE_RP_SELECTIVE in ev.rules:
                rule = ev.rules[EV_RULE_RP_SELECTIVE]

            # sanity check if we don't have a rule return False
            if rule is None:
                return False

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
        That tuple is then stored in a dict containing this rule name constant.
        Each rule is defined by a skip_visual boolean and a special random chance.
        skip_visual is used to store if the greeting should be executed without
        executing the normal visual setup, this is useful for special greetings
        random_chance is used to define the 1 in random_chance chance that this
        greeting can be called
        """

        @staticmethod
        def create_rule(skip_visual=False, random_chance=0, ev=None):
            """
            IN:
                skip_visual - A boolean stating wheter we should skip visual
                    initialization
                random_chance - An int used to determine 1 in random_chance
                    special chance for this greeting to appear
                ev - Event to create rule for, if passed in
                    (Default: None)

            RETURNS:
                a dict containing the specified rules
            """

            # random_chance can't be negative
            if random_chance < 0:
                raise Exception("random_chance can't be negative")

            # return the tuple inside a dict
            rule = {EV_RULE_GREET_RANDOM : (skip_visual, random_chance)}

            if ev:
                ev.rules.update(rule)

            return rule


        @staticmethod
        def evaluate_rule(event=None, rule=None):
            """
            IN:
                event - the event to evaluate
                rule - the MASGreetingRule to check it's random_chance

            RETURNS:
                True if the random returned 1
            """
            # check if we have an event that contains the rule we need
            # event rule takes priority so it's checked here
            if event and EV_RULE_GREET_RANDOM in event.rules:
                rule = event.rules[EV_RULE_GREET_RANDOM]

            # sanity check if we don't have a rule return False
            if rule is None:
                return False

            # unpack the tuple for easy access
            skip_visual, random_chance = rule

            # check if random_chance is less or equal to 0 return False
            if random_chance <= 0:
                return False

            # Evaluate randint with a chance of 1 in random_chance
            return renpy.random.randint(1,random_chance) == 1


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

    class MASFarewellRule(object):
        """
        Static Class used to create farewell specific rules in tuple form.
        That tuple is then stored in a dict containing this rule name constant.
        Each rule is defined by a special random chance.
        random_chance is used to define the 1 in random_chance chance that this
        farewell can be called
        """

        @staticmethod
        def create_rule(random_chance, ev=None):
            """
            IN:
                random_chance - An int used to determine 1 in random_chance
                    special chance for this farewell to appear
                ev - Event to create rule for, if passed in
                    (Default: None)

            RETURNS:
                a dict containing the specified rules
            """

            # random_chance can't be negative
            if random_chance < 0:
                raise Exception("random_chance can't be negative")

            # return the rule inside a dict
            rule = {EV_RULE_FAREWELL_RANDOM : random_chance}

            if ev:
                ev.rules.update(rule)

            return rule


        @staticmethod
        def evaluate_rule(event=None, rule=None):
            """
            IN:
                event - the event to evaluate
                rule - the MASFarewellRule to check it's random_chance

            RETURNS:
                True if the random returned 1
            """
            # check if we have an event that contains the rule we need
            # event rule takes priority so it's checked here
            if event and EV_RULE_FAREWELL_RANDOM in event.rules:
                rule = event.rules[EV_RULE_FAREWELL_RANDOM]

            # sanity check if we don't have a rule return False
            if rule is None:
                return False

            # store the rule for easy access
            # keeping this so when we add another rule we'll keep
            # the same code structure, also it's more readable changing the name
            random_chance = rule

            # check if random_chance is less or equal to 0 return False
            if random_chance <= 0:
                return False

            # Evaluate randint with a chance of 1 in random_chance
            return renpy.random.randint(1,random_chance) == 1

    class MASAffectionRule(object):
        """
        Static Class used to create affection specific rules in tuple form.
        That tuple is then stored in a dict containing this rule name constant.
        Each rule is defined by a min and a max determining a range of affection
        to check against.
        """

        @staticmethod
        def create_rule(min, max, ev=None):
            """
            IN:
                min - An int representing the minimal(inclusive) affection required
                    for the event to be available, if None is passed is assumed
                    that there's no minimal affection
                max - An int representing the maximum(inclusive) affection required
                    for the event to be available, if None is passed is assumed
                    that there's no maximum affection
                ev - Event to create rule for, if passed in
                    (Default: None)

            RETURNS:
                a dict containing the specified rules
            """

            # both min and max can't be None at the same time, since that means
            # that this is not affection dependent
            if not min and not max:
                raise Exception("at least min or max must not be None")

            # return the rule inside a dict
            rule = {EV_RULE_AFF_RANGE : (min, max)}

            if ev:
                ev.rules.update(rule)

            return rule


        @staticmethod
        def evaluate_rule(event=None, rule=None, affection=None):
            """
            IN:
                event - the event to evaluate
                rule - the MASAffectionRule to check against
                affection - the affection to check the rule against

            RETURNS:
                True if the current affection is inside the rule range
            """

            # check if we have an event that contains the rule we need
            # event rule takes priority so it's checked here

            if event and EV_RULE_AFF_RANGE in event.rules:
                rule = event.rules[EV_RULE_AFF_RANGE]

            # sanity check if we don't have a rule return False
            if rule is None:
                return False

            # store affection for easy checking
            if not affection:
                affection = persistent._mas_affection["affection"]

            # unpack the rule for easy access
            min, max = rule

            # Evaluate if affection is inside the rule range, in case both are None
            # will return true (however that case should be catched on create_rule)
            return  (affection >= min and not max) or (min <= affection <= max)
