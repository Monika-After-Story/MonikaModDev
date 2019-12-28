default persistent._mas_current_drink = {
    "brew time": None,
    "drink time": None,
    "drink": None,
}

default persistent._mas_consumable_map = dict()

init python in mas_consumables:
    TYPE_DRINK = 0
    TYPE_FOOD = 1
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
            split_list - list of split hours
            consumable_chance - likelihood of Monika to keep having this consumable
            consumable_low - bottom bracket of consume time
            consumable_high - top bracket of consume time
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
            consumable_high
        ):
            """
            MASConsumableDrink constructor

            IN:
                consumable_id - id for the consumable
                    NOTE: Must be unique

                disp_name - Friendly display name (for use in dialogue)

                start_end_tuple_list - list of tuples storing (start_hour, end_hour)

                acs - MASAccessory object for this consumable

                consumable_chance - chance for Monika to continue having this consumable

                consumable_low - low bracket for Monika to have this consumable

                consumable_high - high bracket for Monika to have this consumable
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

            #Add this to the map
            if consumable_type not in store.mas_consumables.consumable_map:
                store.mas_consumables.consumable_map[consumable_type] = dict()

            store.mas_consumables.consumable_map[consumable_type][consumable_id] = self

            #Now we need to set up data if not already set
            if consumable_id not in persistent._mas_consumable_map:
                persistent._mas_consumable_map[consumable_id] = {
                    "enabled": False,
                    "times_had": 0
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

    class MASConsumableFood(MASConsumable):
        """
        MASConsumableFood class

        Inherits from MASConsumable
        """
        def __init__(
            self,
            consumable_id,
            disp_name,
            start_end_tuple_list,
            acs,
            consumable_chance,
            consumable_low,
            consumable_high
        ):
            raise NotImplementedError

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
            brew_chance - likelihood of Monika to brew this consumable drink
            consumable_chance - likelihood of Monika to keep drinking this consumable drink
            brew_low - bottom bracket of brew time
            brew_high - top bracket of brew time
            consumable_low - bottom bracket of drink time
            consumable_high - top bracket of drink time
        """

        #Constants:
        BREW_FINISH_EVL = "mas_finished_brewing"
        DRINK_FINISH_EVL = "mas_finished_drinking"

        def __init__(
            self,
            consumable_id,
            disp_name,
            container,
            start_end_tuple_list,
            acs,
            split_list,
            consumable_chance=80,
            consumable_low=10*60,
            consumable_high=2*3600,
            brew_chance=80,
            brew_low=2*60,
            brew_high=4*60
        ):
            """
            MASConsumableDrink constructor

            IN:
                consumable_id - id for the consumable
                    NOTE: Must be unique

                disp_name - Friendly diaply name (for use in dialogue)

                start_end_tuple_list - list of tuples storing (start_hour, end_hour)

                acs - MASAccessory object for this consumable drink

                split_list - list of split hours for brewing

                brew_chance - chance for Monika to brew this drink
                    (Default: 80/100)
                    NOTE: If set to None or 0, this will not be considered brewable

                consumable_chance - chance for Monika to continue drinking this drink
                    (Default: 80/100)

                brew_low - low bracket for brew time
                    (Default: 2 minutes)
                    NOTE: If set to None, this will not be considered brewable

                brew_high - high bracket for brew time
                    (Default: 4 minutes)
                    NOTE: If set to None, this will not be considered brewable

                consumable_low - low bracket for Monika to drink this drink
                    (Default: 10 minutes)

                consumable_high - high bracket for Monika to drink this drink
                    (Default: 2 hours)
            """
            if consumable_id in store.mas_consumables.consumable_map:
                raise Exception("consumable {0} already exists.".format(consumable_id))

            super(MASConsumableDrink, self).__init__(
                consumable_id,
                disp_name,
                mas_consumables.TYPE_DRINK,
                start_end_tuple_list,
                acs,
                consumable_chance,
                consumable_low,
                consumable_high
            )

            self.container=container
            self.split_list=split_list
            self.brew_low=brew_low
            self.brew_high=brew_high
            self.brew_chance=brew_chance

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
            brew_ev = mas_getEV(MASConsumableDrink.BREW_FINISH_EVL)
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
            drinking_time = datetime.timedelta(0, random.randint(self.consumable_low, self.consumable_high))

            #Setup the stop time for the cup
            persistent._mas_current_drink["drink time"] = _start_time + drinking_time

            #Setup the event conditional
            drink_ev = mas_getEV(MASConsumableDrink.DRINK_FINISH_EVL)
            drink_ev.conditional = (
                "persistent._mas_current_drink['drink time'] is not None "
                "and datetime.datetime.now() > persistent._mas_current_drink['drink time']"
            )
            drink_ev.action = EV_ACT_QUEUE

            #Increment cup count
            self.increment()

        def reset(self):
            """
            Resets the events for the consumable and resets the current consumable drink
            """
            #Get evs
            brew_ev = mas_getEV(MASConsumableDrink.BREW_FINISH_EVL)
            drink_ev = mas_getEV(MASConsumableDrink.DRINK_FINISH_EVL)

            #Hide cup/mug
            monika_chr.remove_acs(self.acs)

            #Reset the events
            brew_ev.conditional = None
            brew_ev.action = None
            drink_ev.conditional = None
            drink_ev.action = None

            #And remove them from the event list
            mas_rmEVL(MASConsumableDrink.BREW_FINISH_EVL)
            mas_rmEVL(MASConsumableDrink.DRINK_FINISH_EVL)

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

        def brewable(self):
            """
            Checks if this drink is brewable

            OUT:
                boolean:
                    - True if this drink has:
                        1. brew_high
                        2. brew_low
                        3. brew_chance

                    - False otherwise
            """
            return (
                not self.brew_chance
                or self.brew_low is None
                or self.brew_high is None
            )

        @staticmethod
        def _getCurrentDrink():
            """
            Gets the MASConsumableDrink object for the current drink or None if we're not drinking

            OUT:
                - Current MASConsumableDrink if drinking
                - None if not drinking
            """
            return mas_getConsumableDrink(persistent._mas_current_drink["drink"])

    #START: Global functions
    def mas_getConsumableDrink(consumable_id):
        """
        Gets the consumable drink by id.

        IN:
            consumable_id - consumable to Get

        OUT:
            MASConsumableDrink object if found, None otherwise
        """
        if mas_consumables.TYPE_DRINK not in mas_consumables.consumable_map:
            return None
        return store.mas_consumables.consumable_map[mas_consumables.TYPE_DRINK].get(consumable_id, None)


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
        if mas_consumables.TYPE_DRINK not in mas_consumables.consumable_map:
            return []

        return [
            drink
            for drink in mas_consumables.consumable_map[mas_consumables.TYPE_DRINK].itervalues()
            if drink.enabled() and drink.isDrinkTime()
        ]

#START: consumable drink defs:
init 11 python:
    MASConsumableDrink(
        consumable_id="coffee",
        disp_name="coffee",
        container="cup",
        start_end_tuple_list=[(5, 12)],
        acs=mas_acs_mug,
        split_list=[9]
    )

    MASConsumableDrink(
        consumable_id="hotchocolate",
        disp_name="hot chocolate",
        container="cup",
        start_end_tuple_list=[(19,22)],
        acs=mas_acs_hotchoc_mug,
        split_list=[21]
    )

#START: Finished brewing/drinking events
init 5 python:
    import random
    # this event has like no params beause its only pushed
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
    # this event has like no params beause its only pushed
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="mas_finished_drinking",
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )


label mas_finished_drinking:
    # monika only gets a new cup between 6am and noon
    $ current_drink = MASConsumableDrink._getCurrentDrink()
    $ get_new_cup = current_drink.isDrinkTime()

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
        $ current_drink.reset()

    else:
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