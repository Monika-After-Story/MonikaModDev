default persistent._mas_current_drink = {
    "brew time": None,
    "drink time": None,
    "drink": None,
}

init python in mas_consumables:
    consumable_map = dict()


init 10 python:
    #MASConsumableDrink class
    class MASConsumableDrink:
        """
        MASConsumableDrink class

        PROPERTIES:
            consumable_id - id of the consumable
            enabled_var - persistent var indicating if this is enabled
            finished_brewing_evl - eventlabel of the finished brewing event
            finished_drinking_evl - eventlabel of the finished drinking event
            start_end_tuple_list - list of (start_hour, end_hour) tuples
            counter_var - persistent cups of x drank var
            drink_acs - acs to display for the drink
            split_list - list of split hours
            brew_chance - likelihood of Monika to brew this consumable drink
            drink_chance - likelihood of Monika to keep drinking this consumable drink
            brew_low - bottom bracket of brew time
            brew_high - top bracket of brew time
            drink_low - bottom bracket of drink time
            drink_high - top bracket of drink time
        """
        def __init__(
            self,
            consumable_id,
            enabled_var,
            finished_brewing_evl,
            finished_drinking_evl,
            start_end_tuple_list,
            counter_var,
            drink_acs,
            split_list,
            brew_chance=80,
            drink_chance=80,
            brew_low=2*60,
            brew_high=4*60,
            drink_low=10*60,
            drink_high=2*3600
        ):
            """
            MASConsumableDrink constructor

            IN:
                consumable_id - id for the consumable
                    NOTE: Must be unique

                enabled_var - persistent var setting this as enabled or disabled
                    NOTE: must be persistent

                finished_brewing_evl - eventlabel for the finished brewing event
                    NOTE: must have an event object associated

                finished_drinking_evl - eventlabel for the finished drinking event
                    NOTE: must have an event object associated

                start_end_tuple_list - list of tuples storing (start_hour, end_hour)

                counter_var - persistent var for counting the amount of cups drank
                    NOTE: must be persistent

                drink_acs - MASAccessory object for this consumable drink

                split_list - list of split hours for brewing

                brew_chance - chance for Monika to brew this drink
                    (Default: 80/100)

                drink_change - chance for Monika to continue drinking this drink
                    (Default: 80/100)

                brew_low - low bracket for brew time
                    (Default: 2 minutes)

                brew_high - high bracket for brew time
                    (Default: 4 minutes)

                drink_low - low bracket for Monika to drink this drink
                    (Default: 10 minutes)

                drink_high - high bracket for Monika to drink this drink
                    (Default: 2 hours)
            """
            if consumable_id in store.mas_consumables.consumable_map:
                raise Exception("consumable {0} already exists.".format(consumable_id))

            elif not mas_getEV(finished_brewing_evl):
                raise Exception("No event object with eventlabel {0} exists".format(finished_brewing_evl))

            elif not mas_getEV(finished_drinking_evl):
                raise Exception("No event object with eventlabel {0} exists".format(finished_drinking_evl))

            self.consumable_id=consumable_id
            self.enabled_var=enabled_var
            self.finished_brewing_evl=finished_brewing_evl
            self.finished_drinking_evl=finished_drinking_evl
            self.start_end_tuple_list=start_end_tuple_list
            self.brew_low=brew_low
            self.brew_high=brew_high
            self.drink_low=drink_low
            self.drink_high=drink_high
            self.counter_var=counter_var
            self.drink_acs=drink_acs
            self.split_list=split_list
            self.brew_chance=brew_chance
            self.drink_chance=drink_chance

            store.mas_consumables.consumable_map[consumable_id] = self

        def enabled(self):
            """
            Checks the flag to see if this consumable drink is enabled
            """
            return bool(persistent.__dict__[self.enabled_var])

        def brew(self, _start_time=None):
            """
            Starts brewing the drink
            (Sets up the finished brewing event)

            IN:
                _start_time - time to start brewing. If none, now is assumed
            """
            if _start_time is None:
                _start_time = datetime.datetime.now()

            #Start brew
            persistent._mas_current_drink['brew time'] = _start_time
    
            #Calculate end brew time
            end_brew = random.randint(self.brew_low, self.brew_high)
    
            #Setup the event conditional
            brew_ev = mas_getEV(self.finished_brewing_evl)
            brew_ev.conditional = (
                "persistent._mas_current_drink['brew time'] is not None "
                "and (datetime.datetime.now() - "
                "persistent._mas_current_drink['brew time']) "
                "> datetime.timedelta(0, {0})"
            ).format(end_brew)
            brew_ev.action = EV_ACT_QUEUE

            #Now we set what we're drinking
            persistent._mas_current_drink["drink"] = self.consumable_id

        def drink(self, _start_time=None):
            """
            Allows Monika to drink this consumable drink
            (Sets up the finished drinking event)

            IN:
                _start_time - time to start brewing. If none, now is assumed
            """
            if _start_time is None:
                _start_time = datetime.datetime.now()

            #Delta for drinking
            drinking_time = datetime.timedelta(0, random.randint(self.drink_low, self.drink_high))

            #Setup the stop time for the cup
            persistent._mas_current_drink["drink time"] = _start_time + drinking_time

            #Setup the event conditional
            drink_ev = mas_getEV(self.finished_drinking_evl)
            drink_ev.conditional = (
                "persistent._mas_current_drink['drink time'] is not None "
                "and datetime.datetime.now() > persistent._mas_current_drink['drink time']"
            )
            drink_ev.action = EV_ACT_QUEUE

            #Increment cup count
            persistent.__dict__[self.counter_var] += 1

        def reset(self):
            """
            Resets the events for the consumable and resets the current consumable drink
            """
            #Get evs
            brew_ev = mas_getEV(self.finished_brewing_evl)
            drink_ev = mas_getEV(self.finished_drinking_evl)

            #Hide cup/mug
            monika_chr.remove_acs(self.drink_acs)

            #Reset the events
            brew_ev.conditional = None
            brew_ev.action = None
            drink_ev.conditional = None
            drink_ev.action = None
            mas_rmEVL(brew_ev.eventlabel)
            mas_rmEVL(drink_ev.eventlabel)

            #Now we clean the persist var
            persistent._mas_current_drink["brew time"] = None
            persistent._mas_current_drink["drink time"] = None
            persistent._mas_current_drink["drink"] = None

        def isStillBrew(self, _now):
            """
            Checks if we're still brewing something

            IN:
                _now - datetime.datetime object representing current time

            OUT:
                boolean:
                    - True if we're still brewing something
                    - False otherwise
            """
            _time = persistent._mas_current_drink["brew time"]
            return (
                _time is not None
                and _time.date() == _now.date()
                and self.isDrinkTime(_time)
            )

        def isStillDrink(self, _now=None):
            """
            Checks if we're still drinking something

            IN:
                _now - datetime.datetime object representing current time
                If none, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we're still brewing something
                    - False otherwise
            """
            if _now is None:
                _now = datetime.datetime.now()

            _time = persistent._mas_current_drink["drink time"]
            return _time is not None and _now < _time

        def isDrinkTime(self, _now=None):
            """
            Checks if we're in the time range for this drink

            IN:
                _now - datetime.datetime to check if we're within the time for
                If none, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we're within the drink time(s) of this drink
                    - False otherwise
            """
            if _now is None:
                _now = datetime.datetime.now()

            for start_time, end_time in self.start_end_tuple_list:
                if start_time <= _now.hour < end_time:
                    return True
            return False

        def shouldBrew(self, _now=None):
            """
            Checks if we're in the time range for this drink

            IN:
                _time - datetime.datetime to check if we're within the time for
                If none, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we're within the drink time(s) of this drink
                    - False otherwise
            """

            if _now is None:
                _now = datetime.datetime.now()

            _chance = random.randint(1, 100)

            for split in self.split_list:
                if _now.hour < split and _chance <= self.brew_chance:
                    return True
            return False


    def mas_getConsumableDrink(consumable_id):
        """
        Gets the consumable drink by id.

        IN:
            consumable_id - consumable to Get

        OUT:
            MASConsumableDrink object if found, None otherwise
        """
        return store.mas_consumables.consumable_map.get(consumable_id, None)


    def mas_getDrinksForTime(_now=None):
        """
        Gets a list of all consumable drinks active at this time

        IN:
            _now - datetime.datetime object representing current time
            If None, now is assumed
            (Default: None)

        OUT:
            list of consumable drink objects enabled and within time range
        """
        return [
            drink
            for drink in mas_consumables.consumable_map.itervalues()
            if drink.enabled() and drink.isDrinkTime()
        ]

#START: consumable drink defs:
init 11 python:
    MASConsumableDrink(
        consumable_id="coffee",
        enabled_var="_mas_acs_enable_coffee",
        finished_brewing_evl="mas_coffee_finished_brewing",
        finished_drinking_evl="mas_coffee_finished_drinking",
        start_end_tuple_list=[(5, 12)],
        counter_var="_mas_coffee_cups_drank",
        drink_acs=mas_acs_mug,
        split_list=[9]
    )

    MASConsumableDrink(
        consumable_id="hotchocolate",
        enabled_var="_mas_acs_enable_hotchoc",
        finished_brewing_evl="mas_c_hotchoc_finished_brewing",
        finished_drinking_evl="mas_c_hotchoc_finished_drinking",
        start_end_tuple_list=[(19,22)],
        counter_var="_mas_c_hotchoc_cups_drank",
        drink_acs=mas_acs_hotchoc_mug,
        split_list=[21]
    )