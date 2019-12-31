#TODO: Update scripts to transfer given consumables (coffee/hotchoc)
#TODO: Delete the following vars:
#   - persistent._mas_acs_enable_coffee
#   - persistent._mas_coffee_been_given
#   - persistent._mas_acs_enable_hotchoc
#   - persistent._mas_c_hotchoc_been_given
#TODO: Stock existing users with some coffee/hotchoc

default persistent._mas_current_drink = {
    "brew time": None,
    "drink time": None,
    "drink": None,
}

default persistent._mas_consumable_map = dict()

init python in mas_consumables:
    #Consumable types for sorting in the consumable map
    TYPE_DRINK = 0
    TYPE_FOOD = 1

    #Dict of dicts:
    #consumable_map = {
    #   0: {"consumable_id": MASConsumableDrink},
    #   1: {"consumable_id": MASConsumableFood}
    #}
    consumable_map = dict()


init 10 python:
    #MASConsumable class
    class MASConsumable():
        """
        Base class for consumables

        PROPERTIES:
            consumable_id - id of the consumable
            disp_name - friendly name for this consumable
            consumable_type - type of consumable this is:
                0 - Drink
                1 - Food
            start_end_tuple_list - list of (start_hour, end_hour) tuples
            acs - MASAccessory to display for the consumable
            consumable_chance - likelihood of Monika to keep having this consumable
            consumable_low - bottom bracket of consume time
            consumable_high - top bracket of consume time
            late_entry_list - list of integers storing the hour which would be considered a late entry
            max_re_serve - amount of times Monika can go back for another serving of this consumable
        """

        def __init__(
            self,
            consumable_id,
            disp_name,
            consumable_type,
            start_end_tuple_list,
            acs,
            consumable_chance,
            consumable_low,
            consumable_high,
            late_entry_list=None,
            max_re_serve=None
        ):
            """
            MASConsumable constructor

            IN:
                consumable_id - id for the consumable
                    NOTE: Must be unique

                disp_name - Friendly display name (for use in dialogue)

                consumable_type - Type of this consumable:
                    0 - Drink
                    1 - Food

                start_end_tuple_list - list of tuples storing (start_hour, end_hour)

                acs - MASAccessory object for this consumable

                consumable_chance - chance for Monika to continue having this consumable

                consumable_low - low bracket for Monika to have this consumable

                consumable_high - high bracket for Monika to have this consumable

                late_entry_list - list of integers storing the hour which would be considered a late entry
                    If None, the start values from start_end_tuple_list are assumed
                    NOTE: Must have the same length as start_end_tuple_list
                    (Default: None)

                max_re_serve - amount of times Monika can get a re-serving of this consumable
                    NOTE: If None, Monika can get as many re-servings as she wants, provided chance and time range is met
                    (Default: None)
            """
            if (
                consumable_type in store.mas_consumables.consumable_map
                and consumable_id in store.mas_consumables.consumable_map[consumable_type]
            ):
                raise Exception("consumable {0} already exists.".format(consumable_id))

            self.consumable_id=consumable_id
            self.consumable_type=consumable_type
            self.disp_name=disp_name
            self.start_end_tuple_list=start_end_tuple_list
            self.acs=acs
            self.consumable_chance=consumable_chance
            self.consumable_low=consumable_low
            self.consumable_high=consumable_high

            if late_entry_list is None:
                self.late_entry_list=[]

                for start, end in start_end_tuple_list:
                    self.late_entry_list.append(start)
            else:
                self.late_entry_list=late_entry_list

            self.max_re_serve=max_re_serve
            self.re_serves_had=0

            #Add this to the map
            if consumable_type not in store.mas_consumables.consumable_map:
                store.mas_consumables.consumable_map[consumable_type] = dict()

            store.mas_consumables.consumable_map[consumable_type][consumable_id] = self

            #Now we need to set up data if not already set
            if consumable_id not in persistent._mas_consumable_map:
                persistent._mas_consumable_map[consumable_id] = {
                    "enabled": False,
                    "times_had": 0,
                    "servings_left": 0
                }

        def enabled(self):
            """
            Checks if this consumable is enabled

            OUT:
                boolean:
                    - True if this consumable is enabled
                    - False otherwise
            """
            return persistent._mas_consumable_map[self.consumable_id]["enabled"]

        def enable(self):
            """
            Enables the consumable
            """
            persistent._mas_consumable_map[self.consumable_id]["enabled"] = True

        def disable(self):
            """
            Disables the consumable
            """
            persistent._mas_consumable_map[self.consumable_id]["enabled"] = False

        def increment(self):
            """
            Increments the amount of times Monika has had the consumable
            """
            persistent._mas_consumable_map[self.consumable_id]["times_had"] += 1

        def shouldHave(self, _now=None):
            """
            Checks if we should have this consumable now

            CONDITIONS:
                1. We're within the consumable time range
                2. We pass the chance check to have this consumable
                3. We have not met/exceeded the maximum re-serve amount

            IN:
                _now - datetime.datetime to check if we're within the timerange for this consumable
                If None, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we should have this consumable (passes above conditions)
                    - False otherwise

            NOTE: This does NOT anticipate splits/preparation
            """
            #First, let's check if we've reached the max re-serve point
            if self.max_re_serve is not None and self.re_serves_had == self.max_re_serve:
                return False

            if _now is None:
                _now = datetime.datetime.now()

            _chance = random.randint(1, 100)

            for start_time, end_time in self.start_end_tuple_list:
                if start_time <= _now.hour < end_time and _chance <= self.consumable_chance:
                    return True
            return False

        def hasServing(self):
            """
            Checks if we have a serving of this consumable in order to use it

            OUT:
                boolean:
                    - True if we have at least 1 serving left of the consumable
                    - False otherwise
            """
            return persistent._mas_consumable_map[self.consumable_id]["servings_left"] > 0

        def restock(self, servings=100):
            """
            Adds more servings of the consumable

            IN:
                servings - amount of servings to add
                (Default: 100)
            """
            persistent._mas_consumable_map[self.consumable_id]["servings_left"] += servings

        def getStock(self):
            """
            Gets the amount of servings left of a consumable

            OUT:
                integer:
                    - The amount of servings left for the consumable
            """
            return persistent._mas_consumable_map[self.consumable_id]["servings_left"]

        def use(self, amount=1):
            """
            Uses a serving of this consumable

            IN:
                amount - amount of servings to use up
                (Default: 1)
            """
            servings_left = persistent._mas_consumable_map[self.consumable_id]["servings_left"]

            if servings_left - amount < 0:
                persistent._mas_consumable_map[self.consumable_id]["servings_left"] = 0
            else:
                persistent._mas_consumable_map[self.consumable_id]["servings_left"] -= amount

        def re_serve(self):
            """
            Increments the re-serve count
            """
            self.re_serves_had += 1

        def isLateEntry(self, _now=None):
            """
            Checks if we should load with a consumable already out or not

            IN:
                _now - datetime.datetime to check if we're within the time for the consumable
                If none, now is assumed
                (Default: None)

            OUT:
                boolean:
                    - True if we should load in with consumable already out
                    - False otherwise
            """
            if _now is None:
                _now = datetime.datetime.now()

            for index in range(len(self.start_end_tuple_list)):
                #Bit of setup
                _start, _end = self.start_end_tuple_list[index]
                late_hour = self.late_entry_list[index]

                if (
                    _start <= _now.hour < _end
                    and _now.hour >= late_hour
                ):
                    return True
            return False

        def absentUse(self, servings, days_absent):
            """
            Checks how many servings of the consumable Monika will have used in the player's absence

            IN:
                servings - amount of servings per having of the consumable
                days_absent - amount of days the player was absent
            """
            chance = random.randint(1, 100)
            for day in range(days_absent):
                if chance <= self.consumable_chance:
                    self.use(servings)


    class MASConsumableFood(MASConsumable):
        """
        MASConsumableFood class

        Inherits from MASConsumable

        TODO: Consumable food implementation
        """
        def __init__(
            self,
            consumable_id,
            disp_name,
            start_end_tuple_list,
            acs,
            consumable_chance,
            consumable_low,
            consumable_high,
            late_entry_list=None,
            max_re_serve=None
        ):
            raise NotImplementedError

            super(MASConsumableFood, self).__init__(
                consumable_id,
                disp_name,
                start_end_tuple_list,
                acs,
                consumable_chance,
                consumable_low,
                consumable_high,
                late_entry_list,
                max_re_serve
            )

    #MASConsumableDrink class
    class MASConsumableDrink(MASConsumable):
        """
        MASConsumableDrink class

        Inherits from MASConsumable (See that class for info on properties)

        PROPERTIES:
            consumable_id - id of the consumable
            disp_name - friendly name for this consumable
            container - the container of this drink (cup, mug, glass, bottle, etc)
            start_end_tuple_list - list of (start_hour, end_hour) tuples
            acs - MASAccessory to display for the drink
            split_list - list of split hours
            late_entry_list - list of integers storing the hour which would be considered a late entry
            max_re_serve - amount of times Monika can get a refill of this drink
            consumable_chance - likelihood of Monika to keep drinking this consumable drink
            brew_low - bottom bracket of brew time
            brew_high - top bracket of brew time
            consumable_low - bottom bracket of drink time
            consumable_high - top bracket of drink time
            done_drink_until - the time until Monika can randomly have this drink again
            get_drink_evl - evl to use for getting the drink
            finish_brew_evl - evl to use when finished brewing
            finish_drink_evl - evl to use when finished drinking
        """

        #Constants:
        BREW_FINISH_EVL = "mas_finished_brewing"
        DRINK_FINISH_EVL = "mas_finished_drinking"
        DRINK_GET_EVL = "mas_get_drink"
        DEF_DONE_DRINK_TD = datetime.timedelta(hours=2)

        def __init__(
            self,
            consumable_id,
            disp_name,
            container,
            start_end_tuple_list,
            acs,
            split_list,
            late_entry_list=None,
            max_re_serve=None,
            consumable_chance=80,
            consumable_low=10*60,
            consumable_high=2*3600,
            brew_low=2*60,
            brew_high=4*60,
            get_drink_evl=None,
            finish_brew_evl=None,
            finish_drink_evl=None
        ):
            """
            MASConsumableDrink constructor

            IN:
                consumable_id - id for the consumable
                    NOTE: Must be unique

                disp_name - Friendly diaply name (for use in dialogue)

                container - containment for this consumable (cup/mug/bottle/etc)

                start_end_tuple_list - list of tuples storing (start_hour, end_hour)

                late_entry_list - list of times storing when we should load in with a drink already out

                max_re_serve - amount of times Monika can get a refill of this drink
                    (Default: None)

                acs - MASAccessory object for this consumable drink

                split_list - list of split hours for brewing

                consumable_chance - chance for Monika to continue drinking this drink
                    (Default: 80/100)

                consumable_low - low bracket for Monika to drink this drink
                    (Default: 10 minutes)

                consumable_high - high bracket for Monika to drink this drink
                    (Default: 2 hours)

                brew_low - low bracket for brew time
                    (Default: 2 minutes)
                    NOTE: If set to None, this will not be considered brewable

                brew_high - high bracket for brew time
                    (Default: 4 minutes)
                    NOTE: If set to None, this will not be considered brewable

                get_drink_evl - evl to use for getting the drink. If None, a generic is assumed
                    (Default: None)

                finish_brew_evl - evl to use when finished brewing. If None, a generic is assumed
                    (Default: None)

                finish_drink_evl - evl to use when finished drinking. If None, a generic is assumed
                    (Default: None
            """

            super(MASConsumableDrink, self).__init__(
                consumable_id,
                disp_name,
                mas_consumables.TYPE_DRINK,
                start_end_tuple_list,
                acs,
                consumable_chance,
                consumable_low,
                consumable_high,
                late_entry_list,
                max_re_serve
            )

            self.container=container
            self.split_list=split_list
            self.brew_low=brew_low
            self.brew_high=brew_high

            #EVLs:
            self.get_drink_evl = get_drink_evl if get_drink_evl is not None else MASConsumableDrink.DRINK_GET_EVL
            self.finish_brew_evl = finish_brew_evl if finish_brew_evl is not None else MASConsumableDrink.BREW_FINISH_EVL
            self.finish_drink_evl = finish_drink_evl if finish_drink_evl is not None else MASConsumableDrink.DRINK_FINISH_EVL

            #Timeout prop
            self.done_drink_until=None

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
            brew_ev = mas_getEV(self.finish_brew_evl)
            brew_ev.conditional = (
                "persistent._mas_current_drink['brew time'] is not None "
                "and (datetime.datetime.now() - "
                "persistent._mas_current_drink['brew time']) "
                "> datetime.timedelta(0, {0})"
            ).format(end_brew)
            brew_ev.action = EV_ACT_QUEUE

            #Now we set what we're drinking
            persistent._mas_current_drink["drink"] = self.consumable_id

        def drink(self, _start_time=None, skip_leadin=False):
            """
            Allows Monika to drink this consumable drink
            (Sets up the finished drinking event)

            IN:
                _start_time - time to start brewing. If none, now is assumed
                skip_leadin - whether or not we should push the event where Monika gets something to drink
            """
            if _start_time is None:
                _start_time = datetime.datetime.now()

            #Delta for drinking
            drinking_time = datetime.timedelta(0, random.randint(self.consumable_low, self.consumable_high))

            #Setup the stop time for the cup
            persistent._mas_current_drink["drink time"] = _start_time + drinking_time

            #Setup the event conditional
            drink_ev = mas_getEV(self.finish_drink_evl)
            drink_ev.conditional = (
                "persistent._mas_current_drink['drink time'] is not None "
                "and datetime.datetime.now() > persistent._mas_current_drink['drink time']"
            )
            drink_ev.action = EV_ACT_QUEUE

            if skip_leadin:
                persistent._mas_current_drink["drink"] = self.consumable_id
                monika_chr.wear_acs_pst(self.acs)

            #If this isn't a brewable type and we don't have a current drink, we should push the ev
            elif not self.brewable() and not MASConsumableDrink._getCurrentDrink():
                persistent._mas_current_drink["drink"] = self.consumable_id
                pushEvent(MASConsumableDrink.DRINK_GET_EVL)

            #Increment cup count
            self.increment()

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
                    - True if we're within the drink time(s) of this drink (and drink is brewable)
                    - False otherwise
            """
            if not self.brewable():
                return False

            if _now is None:
                _now = datetime.datetime.now()

            _chance = random.randint(1, 100)

            for split in self.split_list:
                if _now.hour < split and _chance <= self.consumable_chance:
                    return True
            return False

        def brewable(self):
            """
            Checks if this drink is brewable

            OUT:
                boolean:
                    - True if this drink has:
                        1. brew_high
                        2. brew_low

                    - False otherwise
            """
            return self.brew_low is not None and self.brew_high is not None

        def checkCanDrink(self, _now=None):
            """
            Checks if we can drink this drink again
            """
            #First, if this is None, we return True
            if self.done_drink_until is None:
                return True

            #Otherwise, we need to do a comparison
            elif _now is None:
                _now = datetime.datetime.now()

            if _now >= self.done_drink_until:
                self.done_drink_until = None
                return True
            return False

        @staticmethod
        def _reset():
            """
            Resets the events for the consumable and resets the current consumable drink
            """
            #Get current drink
            current_drink = MASConsumableDrink._getCurrentDrink()

            #If we've got a current drink, let's hide it and get rid of the amount of re-serves
            if current_drink:
                monika_chr.remove_acs(current_drink.acs)
                current_drink.re_serves_had = 0

                #Get evs
                brew_ev = mas_getEV(current_drink.finish_brew_evl)
                drink_ev = mas_getEV(current_drink.finish_drink_evl)

                #Reset the events
                brew_ev.conditional = None
                brew_ev.action = None
                drink_ev.conditional = None
                drink_ev.action = None

                #And remove them from the event list
                mas_rmEVL(current_drink.finish_brew_evl)
                mas_rmEVL(current_drink.finish_drink_evl)

            #Now we clean the persist var
            persistent._mas_current_drink["brew time"] = None
            persistent._mas_current_drink["drink time"] = None
            persistent._mas_current_drink["drink"] = None

        @staticmethod
        def _getCurrentDrink():
            """
            Gets the MASConsumableDrink object for the current drink or None if we're not drinking

            OUT:
                - Current MASConsumableDrink if drinking
                - None if not drinking
            """
            return mas_getConsumableDrink(persistent._mas_current_drink["drink"])

        @staticmethod
        def _isDrinking():
            """
            Checks if we're currently drinking something right now
            """
            return persistent._mas_current_drink["drink"] and persistent._mas_current_drink["drink time"]

        @staticmethod
        def _getDrinksForTime(_now=None):
            """
            Gets a list of all consumable drinks active at this time

            IN:
                _now - datetime.datetime object representing current time
                If None, now is assumed
                (Default: None)

            OUT:
                list of consumable drink objects enabled and within time range
            """
            if store.mas_consumables.TYPE_DRINK not in store.mas_consumables.consumable_map:
                return []

            return [
                drink
                for drink in mas_consumables.consumable_map[mas_consumables.TYPE_DRINK].itervalues()
                if drink.enabled() and drink.hasServing() and drink.checkCanDrink() and drink.isDrinkTime()
            ]

        @staticmethod
        def _validatePersistentData():
            """
            Verifies that the data stored in persistent._mas_current_drink is valid to the drinks currently set up

            NOTE: If the persistent data stored isn't valid, it is reset.
            """
            if MASConsumableDrink._isDrinking() and not MASConsumableDrink._getCurrentDrink():
                persistent._mas_current_drink = {
                    "brew time": None,
                    "drink time": None,
                    "drink": None
                }

        @staticmethod
        def _checkDrink(startup=False):
            """
            Logic to handle Monika drinking a consumable both on startup and during runtime

            IN:
                startup - Whether or not we should check for a late entry
                (Default: False)
            """
            #Step one: what can we drink right now?
            drinks = MASConsumableDrink._getDrinksForTime()

            #Validate
            MASConsumableDrink._validatePersistentData()

            drink = MASConsumableDrink._getCurrentDrink()

            #Wear the acs if we don't have it out for some reason
            if MASConsumableDrink._isDrinking() and not monika_chr.is_wearing_acs(drink.acs):
                monika_chr.wear_acs_pst(drink.acs)

            #If we have no drinks, then there's no point in doing anything
            if not drinks:
                if (
                    MASConsumableDrink._isDrinking()
                    and (not drink.isStillDrink() and mas_getCurrSeshStart() > persistent._mas_current_drink["drink time"])
                ):
                    MASConsumableDrink._reset()
                return

            #If we're currently brewing or drinking, we don't need to do anything else
            if persistent._mas_current_drink["drink"] is not None:
                return

            #Otherwise, step two: what are we drinking?
            drink = random.choice(drinks)

            #Setup some vars
            _now = datetime.datetime.now()

            #Time to drink!
            #First, clear vars so we start fresh
            MASConsumableDrink._reset()

            #First, should we even have this?
            if drink.shouldHave():
                #If we brew, we brew for 7 chages worth (to acct for refills)
                if drink.brewable():
                    drink.use(amount=7)

                #Otherwise, if it's a non-brewable, just one
                else:
                    drink.use()

                #Are we loading in after the time? If so, we should already have the drink out. No brew, just drink
                if startup and drink.isLateEntry():
                    drink.drink(skip_leadin=True)

                else:
                    #If this is a brewable, we should brew it
                    if drink.brewable() and drink.shouldBrew(_now):
                        drink.brew()

                    #Otherwise, we'll just set up drinking
                    elif not drink.brewable():
                        drink.drink()

        @staticmethod
        def _absentUse():
            """
            Runs a check on all consumable drinks and subtracts the amount used
            """
            consumable_drinks = store.mas_consumables.consumable_map[store.mas_consumables.TYPE_DRINK]
            _days = mas_getAbsenceLength().days

            for drink in consumable_drinks.itervalues():
                if drink.brewable():
                    drink.absentUse(servings=7, days_absent=_days)
                else:
                    drink.absentUse(servings=4, days_absent=_days)

    #START: Global functions
    def mas_getConsumable(consumable_type, consumable_id):
        """
        Gets a consumable object by type and id

        IN:
            consumable_type - Type of consumable to look for:
                0 - Drink
                1 - Food
            consumable_id - id of the consumable

        OUT:
            Consumable object:
                If TYPE_DRINK, MASConsumableDrink
                If TYPE_FOOD, MASConsumableFood
                If not found, None
        """
        if consumable_type not in mas_consumables.consumable_map:
            return
        return store.mas_consumables.consumable_map[consumable_type].get(consumable_id)

    def mas_getConsumableDrink(consumable_id):
        """
        Gets the consumable drink by id.

        IN:
            consumable_id - consumable to get

        OUT:
            MASConsumableDrink object if found, None otherwise
        """
        return mas_getConsumable(
            store.mas_consumables.TYPE_DRINK,
            consumable_id
        )

    def mas_getConsumableFood(consumable_id):
        """
        Gets the consumable food by id.

        IN:
            consumable_id - consumable to get

        OUT:
            MASConsumableFood object if found, None otherwise
        """
        return mas_getConsumable(
            store.mas_consumables.TYPE_FOOD,
            consumable_id
        )

#START: consumable drink defs:
init 11 python:
    MASConsumableDrink(
        consumable_id="coffee",
        disp_name="coffee",
        container="cup",
        start_end_tuple_list=[(5, 12)],
        acs=mas_acs_mug,
        split_list=[9],
        late_entry_list=[7]
    )

    MASConsumableDrink(
        consumable_id="hotchocolate",
        disp_name="hot chocolate",
        container="cup",
        start_end_tuple_list=[(19,22)],
        acs=mas_acs_hotchoc_mug,
        split_list=[21],
        late_entry_list=[20]
    )

#START: Finished brewing/drinking events
init 5 python:
    import random
    #This event gets its params via _startupDrinkLogic()
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_brewing",
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label mas_finished_brewing:
    $ current_drink = MASConsumableDrink._getCurrentDrink()

    if (not mas_canCheckActiveWindow() or mas_isFocused()) and not store.mas_globals.in_idle_mode:
        m 1esd "Oh, my [current_drink.disp_name] is ready."

    #Moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    #This line is here so it looks better when we hide monika
    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        #Idle pauses and then progresses on its own
        m 1eua "I'm going to grab some [current_drink.disp_name]. I'll be right back.{w=1}{nw}"

    else:
        m 1eua "Hold on a moment."

    #Monika is off screen
    hide monika with dissolve

    #Transition stuffs
    $ renpy.pause(1.0, hard=True)

    #Wear drink acs
    $ monika_chr.wear_acs_pst(current_drink.acs)
    #Reset brew time
    $ persistent._mas_current_drink["brew time"] = None
    #Start drinking
    $ current_drink.drink()

    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"
    return

###Drinking done
init 5 python:
    import random
    #Like finshed_brewing, this event gets its params from
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_drinking",
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label mas_finished_drinking:
    #Get the current drink and see how we should act here
    $ current_drink = MASConsumableDrink._getCurrentDrink()
    $ get_new_cup = (
        current_drink.shouldHave()
        and (current_drink.brewable() or (not current_drink.brewable() and current_drink.hasServing()))
    )

    if (not mas_canCheckActiveWindow() or mas_isFocused()) and not store.mas_globals.in_idle_mode:
        m 1esd "Oh, I've finished my [current_drink.disp_name]."

    #Moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        if get_new_cup:
            #It's drinking time
            m 1eua "I'm going to get some more [current_drink.disp_name]. I'll be right back.{w=1}{nw}"

        else:
            m 1eua "I'm going to put this [current_drink.container] away. I'll be right back.{w=1}{nw}"

    else:
        if get_new_cup:
            m 1eua "I'm going to get another [current_drink.container]."

        m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statemetns so we can properly add / remove the mug
    $ renpy.pause(1.0, hard=True)

    #Should we get some more?
    if not get_new_cup:
        $ MASConsumableDrink._reset()
        #We'll just set up a time when we can have this drink again
        $ current_drink.done_drink_until = datetime.datetime.now() + MASConsumableDrink.DEF_DONE_DRINK_TD

    else:
        $ current_drink.drink()
        $ current_drink.re_serve()

        #Non-brewables are per refill, so they'll run out a bit faster
        if not current_drink.brewable():
            $ current_drink.use()

    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_get_drink",
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label mas_get_drink:
    $ current_drink = MASConsumableDrink._getCurrentDrink()

    #Moving this here so she uses this line to 'pull her chair back'
    $ curr_zoom = store.mas_sprites.zoom_level
    call monika_zoom_transition_reset(1.0)

    show emptydesk at i11 zorder 9

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "I'm going to get a [current_drink.container] of [current_drink.disp_name]. I'll be right back.{w=1}{nw}"

    else:
        m 1eua "I'm going to get a [current_drink.container] of [current_drink.disp_name]."
        m 1eua "Hold on a moment."

    # monika is off screen
    hide monika with dissolve

    # wrap these statemetns so we can properly add / remove the mug
    $ renpy.pause(1.0, hard=True)
    $ monika_chr.wear_acs_pst(current_drink.acs)
    $ renpy.pause(4.0, hard=True)

    show monika 1eua at i11 zorder MAS_MONIKA_Z with dissolve
    hide emptydesk

    # 1 second wait so dissolve is complete before zooming
    $ renpy.pause(0.5, hard=True)
    call monika_zoom_transition(curr_zoom, 1.0)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1hua "Back!{w=1.5}{nw}"

    else:
        m 1eua "Okay, what else should we do today?"
    return
