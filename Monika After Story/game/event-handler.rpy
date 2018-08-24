# Module that defines functions for story event handling
# Assumes:
#   persistent.event_list
#   persistent.current_monikatopic

# NOTE: proof oc concept
# transform to have monika just chill
image monika_waiting_img:
    "monika 1eua"
    1.0
    "monika 1euc"
    1.0
    "monika 1esc"
    1.0
    "monika 1lksdlc"
    1.0
    "monika 1ekd"
    1.0
    repeat

# transform for monika's prompt waiting location
transform prompt_monika:
    tcommon(950,z=0.8)

init -500 python:
    # initalies the locks db

    # the template is the regular starter case for most events
    mas_init_lockdb_template = (
        True, # event label
        False, # prompt
        False, # label
        False, # category
        True, # unlocked
        True, # random
        True, # pool
        True, # conditional
        True, # action
        True, # start_date
        True, # end_date
        True, # unlock_date
        True, # shown_count
        False, # diary_entry
        False, # rules
        True, # last_seen
        False # years
    )

    # set defaults
#    if (
#            persistent._mas_event_init_lockdb_template is not None
#            and len(persistent._mas_event_init_lockdb_template)
#                != len(mas_init_lockdb_template)
#        ):
        # differing lengths mean we have new items to deal with

    # set db defaults
    if persistent._mas_event_init_lockdb is None:
        persistent._mas_event_init_lockdb = dict()

    for ev_key in persistent._mas_event_init_lockdb:
        stored_lock_row = persistent._mas_event_init_lockdb[ev_key]

        if len(mas_init_lockdb_template) != len(stored_lock_row):
            # splice and dice
            lock_row = list(mas_init_lockdb_template)
            lock_row[0:len(stored_lock_row)] = list(stored_lock_row)
            persistent._mas_event_init_lockdb[ev_key] = tuple(lock_row)

    # set the new template
    persistent._mas_event_init_lockdb_template = mas_init_lockdb_template

    # set db defaults
#    if persistent._mas_event_init_lockdb is None:
#        persistent._mas_event_init_lockdb = dict()

    # initalizes LOCKDB for the Event class
    Event.INIT_LOCKDB = persistent._mas_event_init_lockdb


init 850 python:
    # mainly to create centralized database for calendar lookup
    # (and possible general db lookups)
    mas_all_ev_db = dict()
    mas_all_ev_db.update(store.evhand.event_database)
    mas_all_ev_db.update(store.evhand.farewell_database)
    mas_all_ev_db.update(store.evhand.greeting_database)
    mas_all_ev_db.update(store.mas_moods.mood_db)
    mas_all_ev_db.update(store.mas_stories.story_database)
    mas_all_ev_db.update(store.mas_compliments.compliment_database)

    def mas_getEV(ev_label):
        """
        Global get function that retreives an event given the label

        Designed to be used as a wrapper around the mas_all_ev_db dict
        NOTE: only available at RUNTIME

        IN:
            ev_label - eventlabel to find event for

        RETURNS:
            the event object you were looking for, or None if not found
        """
        return mas_all_ev_db.get(ev_label, None)


    def mas_getEVCL(ev_label):
        """
        Global get function that retrieves the calendar label for an event
        given the eventlabel. This is mainly to help with calendar.

        IN:
            ev_label - eventlabel to find calendar label for

        RETURNS:
            the calendar label you were looking for, or "Unknown Event" if
            not found.
        """
        ev = mas_getEV(ev_label)
        if ev is None:
            return "Unknown Event"
        else:
            return ev.label

python early:
    # FLOW CHECK CONSTANTS
    # these define where in game flow should a delayed action be checked
    # these are bit based so you can define multiple using bitwise operations

    # checked during init process
    # NOTE: this is at runlevel 995
    # AKA after the all event database has been built
    MAS_FC_INIT = 1

    # checked during runtime start (aka splash)
    MAS_FC_START = 2

    # checked at end of game (aka quit)
    MAS_FC_END = 4

    # checked during idle, roughly every minute
    MAS_FC_IDLE_ROUTINE = 8

    # checked during idle, only once per session
    # NOTE: in other words, only check when we enter spcaeroom
    MAS_FC_IDLE_ONCE = 16

    MAS_FC_CONSTANTS = [
        MAS_FC_INIT,
        MAS_FC_START,
        MAS_FC_END,
        MAS_FC_IDLE_ROUTINE,
        MAS_FC_IDLE_ONCE
    ]


init -600 python:
    # THE DELAYED ACTION MAP
    # this is the one we actually use when running stuff
    # please note that this is internal use only.
    # right below this is the class definition that should be used for general
    # purpose
    if persistent._mas_delayed_action_list is None:

        # this list will only contain DelayedAction IDs
        # we will match these IDs using the delayed action map.
        persistent._mas_delayed_action_list = list()

    # the runtime version of this list is actually a dict
    # key: ID of the delayed action
    # value: the DelayedAction to perform
    mas_delayed_action_map = dict()

    class MASDelayedAction(object):
        """
        A Delayed action consists of the following:

        All exceptions are logged
      
        id - the unique ID of this DelayedAction
        ev - the event this action is associated with
        conditional - the logical conditional we want to check before performing
            action
            NOTE: this is not checked for correctness
        action - EV_ACTION constant this delayed action will perform
            NOTE: this is not checked for existence
            NOTE: this can also be a callable
                the event would be passd in as ev
                if callable, make this return True upon success and false 
                    othrewise
        flowcheck - FC constant saying when this delayed action should be
            checked
            NOTE: this is not checked for existence
        been_checked - True if this action has been checked this game session
        executed - True if this delayed action has been executed
            - Delayed actions that have been executed CANNOT be executed again
        """
        import store.mas_utils as m_util

        ERR_COND = "[ERROR] delayed action has bad conditional '{0}' | {1}\n"


        def __init__(self, _id, ev, conditional, action, flowcheck):
            """
            Constructor

            NOTE: MAY raise exceptions
            NOTE: also logs exceptions.

            IN:
                _id - id of this delayedAction
                ev - event this action is related to
                conditional - conditional to check to do this action
                action - EV_ACTION constant for this delayed action
                    NOTE: this can also be a callable
                        ev would be passed in as ev
                    If callable, make this return True on success, False
                        otherwise
                flowcheck - FC constant saying when this delaeyd action should
                    be checked
            """
            try:
                eval(conditional)
            except Exception as e:
                self.m_util.writelog(self.ERR_COND.format(
                    conditional,
                    str(e)
                ))
                raise e

            self.conditional = conditional
            self.action = action
            self.flowcheck = flowcheck
            self.been_checked = False
            self.executed = False
            self.ev = ev
            self.id = _id


        def __call__(self):
            """
            Checks if the conditional passes then performs the action

            NOTE: logs exceptions

            RETURNS:
                True on successful action performed, False otherwise
            """
            # NO event? dont even do this
            if self.ev is None or self.executed or self.action is None:
                return False

            # this should already have been checked on start
            try:
                if eval(self.conditional):
                    if self.action in Event.ACTION_MAP:
                        Event.ACTION_MAP[self.action](
                            self.ev, unlock_time=datetime.datetime.now()
                        )
                        self.executed = True

                    else:
                        # action must be a callable
                        self.executed = self.action(ev=self.ev)
                            
            except Exception as e:
                self.m_util.writelog(self.ERR_COND.format(
                    self.conditional,
                    str(e)
                ))                   
#                raise e

            return self.executed

        
        @staticmethod
        def makeWithLabel(_id, ev_label, conditional, action, flowcheck):
            """
            Makes a MASDelayedAction using an eventlabel instead of an event

            IN:
                _id - id of this delayedAction
                ev_label - label of the event this action is related to
                conditional - conditional to check to do to tihs action
                action - EV_ACTION constant for this delayed action
                    NOTE: this can also be a cllable
                        ev would be passed in as ev
                    If callable, make this return True on success, False
                        otherwise
                flowcheck - FC constant saying when this delayed action should
                    be checked
            """
            return MASDelayedAction(
                _id,
                mas_getEV(ev_label),
                conditional,
                action,
                flowcheck
            )


    # now for helper functions for working with delayed actions
    def mas_removeDelayedAction(_id):
        """
        Removes a delayed action with the given ID

        NOTE: this removes from both persistent and the runtime lists

        IN:
            _id - id of the delayed action to remove
        """
        if _id in persistent._mas_delayed_action_list:
            persistent._mas_delayed_action_list.remove(_id)

        if _id in mas_delayed_action_map:
            mas_delayed_action_map.pop(_id)


    def mas_removeDelayedActions_list(_ids):
        """
        Removes a list of delayed actions with given Ids

        IN:
            _ids - list of Ids to remove
        """
        for _id in _ids:
            mas_removeDelayedAction(_id)


    def mas_removeDelayedActions(*args):
        """
        Multiple argument delayed action removal

        Assumes all given args are IDS
        """
        mas_removeDelayedActions_list(args)


    def mas_runDelayedActions(flow):
        """
        Attempts to run currently held delayed actions for the given flow mode

        Delayed actions that are successfully completed are removed from the
        list

        IN:
            flow - FC constant for the current flow
        """
        if flow not in MAS_FC_CONSTANTS:
            return

        # otherwise, lets try going thru the list
        for action_id in list(mas_delayed_action_map):
            action = mas_delayed_action_map[action_id]

            # bitcheck the flow
            if (action.flowcheck & flow) > 0:                        
                if action():
                    # then pop the item if it was successful
                    mas_removeDelayedAction(action_id)

                # we have now checked this action
                action.been_checked = True


    def mas_addDelayedAction(_id):
        """
        Creates a delayed action with the given ID and adds it to the delayed
        action map (runtime)

        NOTE: this handles duplicates, so its better to use this

        NOTE: this also adds to persistent, just in case

        IN:
            _id - id of the delayed action to create
        """
        if _id in mas_delayed_action_map:
            return

        # otherwise, lets get the constructor for the delayedaction
        make_action = store.mas_delact.MAP.get(_id, None)
        if make_action is None:
            return

        # we have a constructor, lets create!
        mas_delayed_action_map[_id] = make_action()

        # and lastlty, check persistent as well
        if _id not in persistent._mas_delayed_action_list:
            persistent._mas_delayed_action_list.append(_id)


    def mas_addDelayedActions_list(_ids):
        """
        Creates delayed actions given a list of Ids

        IN:
            _ids - list of IDS to add
        """
        for _id in _ids:
            mas_addDelayedAction(_id)


    def mas_addDelayedActions(*args):
        """
        Creates delayed actions given ids as args

        assumes each arg is a valid id 
        """
        mas_addDelayedActions_list(args)


init 995 python:
    # this is where we run the init level batch of delayed actions
    mas_runDelayedActions(MAS_FC_INIT)

init -600 python in mas_delact:
    # we can assume store is imported for all mas_delacts
    import store

init 994 python in mas_delact:
    # store containing a map for delayed action mapping

    # delayed action map:
    # key: ID of the delayed action
    # value: function to call that will generate the delayed action object
    #   NOTE: this function MUST be runnable at init level 995.
    #   NOTE: the result delayedaction does NOT have to be runnable at 995.
    MAP = {
        1: _greeting_ourreality_unlock,
        2: _mas_monika_islands_unlock
    }

    # this is also where we initialize the delayed action map
    def loadDelayedActionMap():
        """
        Checks the persistent delayed action list and generates the 
        runtime map of delayed actions
        """
        store.mas_addDelayedActions_list(
            store.persistent._mas_delayed_action_list
        )


    def saveDelayedActionMap():
        """
        Checks the runtime map of delayed actions and saves them into the
        persistent value. 

        NOTE: this does not ADD to the persistent's list. This recreates it
            entirely.
        """
        store.persistent._mas_delayed_action_list = [
            action_id for action_id in store.mas_delayed_action_map
        ]


    # now run the init
    loadDelayedActionMap()

# special store to contain scrollable menu constants
init -1 python in evhand:
    import store

    # this is the event database
    event_database = dict()
    farewell_database = dict()
    greeting_database = dict()

    # special namedtuple type we are using
    from collections import namedtuple

    # used to keep track of menu items in displaying the prompts.
    # menu -> menu to display for this pane
    # cats -> categories this menu has
    _NT_CAT_PANE = namedtuple("_NT_CAT_PANE", "menu cats")

    # RIGHT PANE
#    PREV_X = 30
    RIGHT_X = 1020
#    PREV_Y = 10
    RIGHT_Y = 40
#    PREV_W = 300
    RIGHT_W = 250
    RIGHT_H = 640
#    PREV_XALIGN = -0.08
    RIGHT_XALIGN = -0.10
    RIGHT_AREA = (RIGHT_X, RIGHT_Y, RIGHT_W, RIGHT_H)

    # LEFT PANE
#    MAIN_X = 360
    LEFT_X = 735
#    MAIN_Y = 10
    LEFT_Y = RIGHT_Y
#    MAIN_W = 300
    LEFT_W = RIGHT_W
    LEFT_H = RIGHT_H
#    MAIN_XALIGN = -0.08
    LEFT_XALIGN = -0.10
    LEFT_AREA = (LEFT_X, LEFT_Y, LEFT_W, LEFT_H)

    UNSE_X = 680
    UNSE_Y = 40
    UNSE_W = 560
    UNSE_H = 640
    UNSE_XALIGN = -0.05
    UNSE_AREA = (UNSE_X, UNSE_Y, UNSE_W, UNSE_H)

    # time stuff
    import datetime
    LAST_SEEN_DELTA = datetime.timedelta(hours=6)

    # restart topic blacklist
    RESTART_BLKLST = [
        "mas_crashed_start",
        "monika_affection_nickname"
    ]

    #### delayed action maps
    # how this works:
    #   add a label that should have a delayed action as keys
    #   values should consist of tuple:
    #       [0] -> conditional as string for this action to pass
    #       [1] -> action constant for what should be done (EV_ACTION)
    DELAYED_ACTION_MAP = {
        
    }

    # as well as special functions
    def addIfNew(items, pool):
        #
        # Adds the list of given items to the given pool (assuemd to be list)
        # such that new only new items are added.
        #
        # IN:
        #   item - list of items to add the given pool
        #   pool - pool to be added to
        #
        # RETURNS:
        #   the pool

        for item in items:
            if item not in pool:
                pool.append(item)
        return pool

    def tuplizeEventLabelList(key_list, db):
        #
        # Creates a list of prompt,label tuple pairs using the given key list
        # and db (dict of events)
        #
        # IN:
        #   key_list - list of keys (labels)
        #   db - dict of events
        #
        # RETURNS:
        #   list of tuples of the following format:
        #       [0]: prompt/caption
        #       [1]: eventlabel
        return [(db[x].prompt, x) for x in key_list]


    def _isFuture(ev, date=None):
        """INTERNAL
        Checks if the start_date of the given event happens after the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's start_date is in the future, False otherwise
        """

        # sanity check
        if ev is None:
            return False

        # if no date is passed
        if date is None:
            date = datetime.datetime.now()

        start_date = ev.start_date

        # if we don't have an end date we return false
        if start_date is None:
            return False

        return date < start_date


    def _isPast(ev, date=None):
        """INTERNAL
        Checks if the end_date of the given event happens before the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's end_date is in the past, False otherwise
        """

        # if there's no event to check return False
        if ev is None:
            return False

        # if no date is passed
        if date is None:
            date = datetime.datetime.now()

        end_date = ev.end_date

        # if we don't have an end date we return false
        if end_date is None:
            return False

        return end_date < date


    def _isPresent(ev):
        """INTERNAL
        Checks if current date falls within the given event's start/end date
        range

        IN:
            ev - Event to check the start_time and end_time

        RETURNS:
            True if current time is inside the  Event's start_date/end_date
            interval, False otherwise
        """
        # check we have an event
        if ev is None:
            return False

        start_date = ev.start_date
        end_date = ev.end_date

        current = datetime.datetime.now()

        # return false if either start or end is None
        if start_date is None or end_date is None:
            return False

        return start_date <= current <= end_date


    def _hideEvent(
            event,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        """
        Internalized hideEvent
        """
        if event:

            if lock:
                event.unlocked = False

            if derandom:
                event.random = False

            if depool:
                event.pool = False

            if decond:
                event.conditional = None


    def _hideEventLabel(
            eventlabel,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=event_database
        ):
        """
        Internalized hideEventLabel
        """
        ev = eventdb.get(eventlabel, None)

        _hideEvent(
            ev,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def _lockEvent(ev):
        """
        Internalized lockEvent
        """
        _hideEvent(ev, lock=True)


    def _lockEventLabel(evlabel, eventdb=event_database):
        """
        Internalized lockEventLabel
        """
        _hideEventLabel(evlabel, lock=True, eventdb=eventdb)


    def _unlockEvent(ev):
        """
        Internalized unlockEvent
        """
        if ev:
            ev.unlocked = True


    def _unlockEventLabel(evlabel, eventdb=event_database):
        """
        Internalized unlockEventLabel
        """
        _unlockEvent(eventdb.get(evlabel, None))


init python:
    import store.evhand as evhand
    import datetime

    def addEvent(event, eventdb=evhand.event_database, skipCalendar=False):
        #
        # Adds an event object to the given eventdb dict
        # Properly checksfor label and conditional statements
        # This function ensures that a bad item is not added to the database
        #
        # IN:
        #   event - the Event object to add to database
        #   eventdb - The Event databse (dict) we want to add to
        #       (Default: evhand.event_database)
        #   skipCalendar - flag that marks wheter or not calendar check should
        #       be skipped

        if type(eventdb) is not dict:
            raise EventException("Given db is not of type dict")
        if type(event) is not Event:
            raise EventException("'" + str(event) + "' is not an Event object")
        if not renpy.has_label(event.eventlabel):
            raise EventException("'" + event.eventlabel + "' does NOT exist")
        if event.conditional is not None:
            eval(event.conditional)
#            try:
#                if eval(event.conditional, globals()):
#                    pass
#            except:
#                raise EventException("Syntax error in conditional statement for event '" + event.eventlabel + "'.")
        # if should not skip calendar check and event has a start_date
        if not skipCalendar and type(event.start_date) is datetime.datetime:
            # add it to the calendar database
            store.mas_calendar.addEvent(event)
        # now this event has passsed checks, we can add it to the db
        eventdb.setdefault(event.eventlabel, event)


    def hideEventLabel(
            eventlabel,
            lock=False,
            derandom=False,
            depool=False,
            decond=False,
            eventdb=evhand.event_database
        ):
        #
        # hide an event in the given eventdb by Falsing its unlocked,
        # random, and pool properties.
        #
        # IN:
        #   eventlabel - label of the event to hide
        #   lock - True if we want to lock this event, False otherwise
        #       (Default: False)
        #   derandom - True if we want to unrandom this event, False otherwise
        #       (Default: False)
        #   depool - True if we want to unpool this event, False otherwise
        #       (Default: False)
        #   decond - True if we want to remove the conditional, False otherwise
        #       (Default: False)
        #   eventdb - the event database (dict) we want to reference
        #       (DEfault: evhand.event_database)
        evhand._hideEventLabel(
            eventlabel,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond,
            eventdb=eventdb
        )


    def hideEvent(
            event,
            lock=False,
            derandom=False,
            depool=False,
            decond=False
        ):
        #
        # hide an event by Falsing its unlocked,
        # random, and pool properties.
        #
        # IN:
        #   event - event object we want to hide
        #   lock - True if we want to lock this event, False otherwise
        #       (Default: False)
        #   derandom - True if we want to unrandom this event, False otherwise
        #       (Default: False)
        #   depool - True if we want to unpool this event, False otherwise
        #       (Default: False)
        #   decond - True if we want to remove the conditional, False
        #       otherwise
        #       (Default: False)
        evhand._hideEvent(
            event,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
        )


    def lockEvent(ev):
        """
        Locks the given event object

        IN:
            ev - the event object to lock
        """
        evhand._lockEvent(ev)


    def lockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Locks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        evhand._lockEventLabel(evlabel, eventdb=eventdb)


    def pushEvent(event_label):
        #
        # This pushes high priority or time sensitive events onto the top of
        # the event list
        #
        # IN:
        #   @event_label - a renpy label for the event to be called
        #
        # ASSUMES:
        #   persistent.event_list

        persistent.event_list.append(event_label)
        return

    def queueEvent(event_label):
        #
        # This adds low priority or order-sensitive events onto the bottom of
        # the event list. This is slow, but rarely called and list should be small.
        #
        # IN:
        #   @event_label - a renpy label for the event to be called
        #
        # ASSUMES:
        #   persistent.event_list

        persistent.event_list.insert(0,event_label)
        return


    def unlockEvent(ev):
        """
        Unlocks the given evnet object

        IN:
            ev - the event object to unlock
        """
        evhand._unlockEvent(ev)


    def unlockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Unlocks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        evhand._unlockEventLabel(evlabel, eventdb=eventdb)


    def isFuture(ev, date=None):
        """
        Checks if the start_date of the given event happens after the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's start_date is in the future, False otherwise
        """
        return evhand._isFuture(ev, date=date)


    def isPast(ev, date=None):
        """
        Checks if the end_date of the given event happens before the
        given time.

        IN:
            ev - Event to check the start_time
            date - a datetime object used to check against
                If None is passed it will check against current time
                (Default: None)

        RETURNS:
            True if the Event's end_date is in the past, False otherwise
        """
        return evhand._isPast(ev, date=date)


    def isPresent(ev):
        """
        Checks if current date falls within the given event's start/end date
        range

        IN:
            ev - Event to check the start_time and end_time

        RETURNS:
            True if current time is inside the  Event's start_date/end_date
            interval, False otherwise
        """
        return evhand._isPresent(ev)


    def popEvent(remove=True):
        #
        # This returns the event name for the next event and makes it the
        # current_monikatopic
        #
        # IN:
        #   remove = If False, then just return the name of the event but don't
        #       remove it
        #
        # ASSUMES:
        #   persistent.event_list
        #   persistent.current_monikatopic

        if len(persistent.event_list) == 0:
            return None
        elif remove:
            event_label = persistent.event_list.pop()
            persistent.current_monikatopic = event_label
        else:
            event_label = persistent.event_list[-1]

        return event_label

    def seen_event(event_label):
        #
        # This checks if an event has either been seen or is already on the
        # event list.
        #
        # IN:
        #   event_lable = The label for the event to be checked
        #
        # ASSUMES:
        #   persistent.event_list
        if renpy.seen_label(event_label) or event_label in persistent.event_list:
            return True
        else:
            return False


    def restartEvent():
        #
        # This checks if there is a persistent topic, and if there was push it
        # back on the stack with a little comment.
        #
        # IN:
        #
        if not mas_isRstBlk(persistent.current_monikatopic):
            #don't push greetings back on the stack
            pushEvent(persistent.current_monikatopic)
            pushEvent('continue_event')
            persistent.current_monikatopic = 0
        return


    def mas_isRstBlk(topic_label):
        """
        Checks if the event with the current label is blacklistd from being
        restarted

        IN:
            topic_label - label of the event we are trying to restart
        """
        if not topic_label:
            return True

        if topic_label.startswith("greeting_"):
            return True

        if topic_label.startswith("bye"):
            return True

        if topic_label.startswith("i_greeting"):
            return True

        if topic_label.startswith("ch30_reload"):
            return True

        # check the blacklist
        if topic_label in evhand.RESTART_BLKLST:
            return True

        return False


    def mas_cleanJustSeen(eventlist, db):
        """
        Cleans the given event list of just seen items (withitn the THRESHOLD)
        retunrs not just seen items

        IN:
            eventlist - list of event labels to pick from
            db - database these events are tied to

        RETURNS:
            cleaned list of events (stuff not in the time THREASHOLD)
        """
        import datetime
        now = datetime.datetime.now()
        cleanlist = list()

        for evlabel in eventlist:
            ev = db.get(evlabel, None)

            if ev:
                if ev.last_seen:
                    if now - ev.last_seen >= store.evhand.LAST_SEEN_DELTA:
                        cleanlist.append(evlabel)

                else:
                    cleanlist.append(evlabel)

        return cleanlist


    def mas_cleanJustSeenEV(ev_list):
        """
        Cleans the given event list (of events) of just seen items
        (within the THRESHOLD). Returns not just seen items.
        Basically the same as mas_cleanJustSeen, except for Event object lists

        IN:
            ev_list - list of event objects

        RETURNS:
            cleaned list of events (stuff not in the tiem THRESHOLD)
        """
        import datetime
        now = datetime.datetime.now()
        cleaned_list = list();

        for ev in ev_list:
            if ev.last_seen is not None:
                # this topic has been seen before, must check time
                if now - ev.last_seen >= store.evhand.LAST_SEEN_DELTA:
                    cleaned_list.append(ev)

            else:
                # topic never seen before, its clean!
                cleaned_list.append(ev)

        return cleaned_list


    def mas_unlockPrompt():
        """
        Unlocks a pool event

        RETURNS:
            True if an event was unlocked. False otherwise
        """
        pool_events = Event.filterEvents(
            evhand.event_database,
            unlocked=False,
            pool=True
        )
        pool_event_keys = [
            evlabel
            for evlabel in pool_events
            if "no unlock" not in pool_events[evlabel].rules
        ]

        if len(pool_event_keys)>0:
            sel_evlabel = renpy.random.choice(pool_event_keys)

            evhand.event_database[sel_evlabel].unlocked = True
            evhand.event_database[sel_evlabel].unlock_date = datetime.datetime.now()

            return True

        # otherwise we didnt unlock anything because nothing available
        return False


init 1 python in evhand:
    # mainly to contain action-based functions and fill an appropriate action
    # map
    # all action-based functions are designed for speed, so they don't 
    # do any sort of sanity checks
    # NOTE: do NOT use these in dialogue code. These are designed for
    #   internal use only
    import store
    import datetime

    def actionPush(ev, **kwargs):
        """
        Runs Push Event action for the given event

        IN:
            ev - event to push to event stack
        """
        store.pushEvent(ev.eventlabel)


    def actionQueue(ev, **kwargs):
        """
        Runs Queue event action for the given event

        IN:
            ev - event to queue to event stack
        """
        store.queueEvent(ev.eventlabel)


    def actionUnlock(ev, unlock_time, **kwargs):
        """
        Unlocks an event. Also setse the unlock_date to the given
            unlock time

        IN:
            ev - event to unlock
            unlock_time - time to set unlock_date to
        """
        ev.unlocked = True
        ev.unlock_date = unlock_time


    def actionRandom(ev, **kwargs):
        """
        Randos an event.

        IN:
            ev - event to random
        """
        ev.random = True


    def actionPool(ev, **kwargs):
        """
        Pools an event.

        IN:
            ev - event to pool
        """
        ev.pool = True


    # now to setup the action map
    store.Event.ACTION_MAP = {
        store.EV_ACT_UNLOCK: actionUnlock,
        store.EV_ACT_QUEUE: actionQueue,
        store.EV_ACT_PUSH: actionPush,
        store.EV_ACT_RANDOM: actionRandom,
        store.EV_ACT_POOL: actionPool
    }


# This calls the next event in the list. It returns the name of the
# event called or None if the list is empty or the label is invalid
#
label call_next_event:


    $event_label = popEvent()
    if event_label and renpy.has_label(event_label):

        if not seen_event(event_label): #Give 15 xp for seeing a new event
            $grant_xp(xp.NEW_EVENT)

        $ mas_RaiseShield_dlg()

        call expression event_label from _call_expression
        $ persistent.current_monikatopic=0

        #if this is a random topic, make sure it's unlocked for prompts
        $ ev = evhand.event_database.get(event_label, None)
        if ev is not None:
            if ev.random and not ev.unlocked:
                python:
                    ev.unlocked=True
                    ev.unlock_date=datetime.datetime.now()

        else:
            # othrewise, pull an ev from the all event database
            # so we can log some data
            $ ev = mas_getEV(event_label)

        if ev is not None:
            # increment shown count
            $ ev.shown_count += 1
            $ ev.last_seen = datetime.datetime.now()

        if _return is not None:
            if "derandom" in _return:
                $ ev.random = False

            if "quit" in _return:
                $persistent.closed_self = True #Monika happily closes herself
                jump _quit
            
            if "nocontinue" in _return:
                return False

        show monika 1 at t11 zorder MAS_MONIKA_Z with dissolve #Return monika to normal pose

        # loop over until all events have been called
        if len(persistent.event_list) > 0:
            jump call_next_event

        $ mas_DropShield_dlg()

    else:
        $ mas_DropShield_dlg()

    return False

# keep track of number of pool unlocks
default persistent._mas_pool_unlocks = 0

# This either picks an event from the pool or events or, sometimes offers a set
# of three topics to get an event from.
label unlock_prompt:
    python:
        if not mas_unlockPrompt():
            # we dont have any unlockable pool topics?
            # lets count this so we can use it later
            persistent._mas_pool_unlocks += 1

    return

#The prompt menu is what pops up when hitting the "Talk" button, it shows a list
#of options for talking to Monika, including the ability to ask her questions
#pulled from a random set of prompts.

label prompt_menu:
    $ mas_RaiseShield_dlg()

    python:
        unlocked_events = Event.filterEvents(evhand.event_database,unlocked=True)
        sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

        unseen_events = []
        for event in sorted_event_keys:
            if not seen_event(event):
                unseen_events.append(event)

        repeatable_events = Event.filterEvents(evhand.event_database,unlocked=True,pool=False)
    #Top level menu
    show monika at t21
    #To make the menu line up right we have to build it up manually
    python:
        talk_menu = []
        if len(unseen_events)>0:
            talk_menu.append(("{b}Unseen.{/b}", "unseen"))
        talk_menu.append(("Ask a question.", "prompt"))
        if len(repeatable_events)>0:
            talk_menu.append(("Repeat conversation.", "repeat"))
        talk_menu.append(("I love you!", "love"))
        talk_menu.append(("I'm feeling...", "moods"))
        talk_menu.append(("Goodbye", "goodbye"))
        talk_menu.append(("Nevermind.","nevermind"))

        renpy.say(m, "What would you like to talk about?", interact=False)
        madechoice = renpy.display_menu(talk_menu, screen="talk_choice")

    if madechoice == "unseen":
        call show_prompt_list(unseen_events) from _call_show_prompt_list

    elif madechoice == "prompt":
        call prompts_categories(True) from _call_prompts_categories

    elif madechoice == "repeat":
        call prompts_categories(False) from _call_prompts_categories_1

    elif madechoice == "love":
        $ pushEvent("monika_love")

    elif madechoice == "moods":
        call mas_mood_start from _call_mas_mood_start
        if not _return:
            jump prompt_menu

    elif madechoice == "goodbye":
        call mas_farewell_start from _call_select_farewell

    else: #nevermind
        $_return = None

    show monika at t11
    $ mas_DropShield_dlg()
    jump ch30_loop

label show_prompt_list(sorted_event_keys):
    $ import store.evhand as evhand

    #Get list of unlocked prompts, sorted by unlock date
    python:
        prompt_menu_items = []
        for event in sorted_event_keys:
            prompt_menu_items.append([unlocked_events[event].prompt,event])

    call screen scrollable_menu(prompt_menu_items, evhand.UNSE_AREA, evhand.UNSE_XALIGN)

    $pushEvent(_return)

    return

label prompts_categories(pool=True):

    # this acts as a stack for category lists
    # each item is an _NT_CAT_PANE namedtuple
    $ cat_lists = list()

    $ current_category = list()
    $ import store.evhand as evhand
    $picked_event = False
    python:

        # get list of unlocked events for the master category list
        unlocked_events = Event.filterEvents(
            evhand.event_database,
#            full_copy=True,
#                category=[False,current_category],
            unlocked=True,
            pool=pool
        )

        # add all categories the master category list
        main_cat_list = list()
        no_cat_list = list() # contain events with no categories
        for key in unlocked_events:
            if unlocked_events[key].category:
                evhand.addIfNew(unlocked_events[key].category, main_cat_list)
            else:
                no_cat_list.append(unlocked_events[key])

        # sort the lists
        main_cat_list.sort()
        no_cat_list.sort(key=Event.getSortPrompt)

        # tuplelize the main the category list
        # NOTE: we use a 2nd list here to do displaying, keeping track of the
        # older cat list for checking if a category was picked
        dis_cat_list = [(x.capitalize() + "...",x) for x in main_cat_list]

        # tupelize the event list
#        no_cat_list = evhand.tuplizeEventLabelList(no_cat_list, unlocked_events)
        no_cat_list = [(x.prompt, x.eventlabel) for x in no_cat_list]

        # extend the display cat list with no category items
        dis_cat_list.extend(no_cat_list)

        # push that master list into the category_lists
        cat_lists.append(evhand._NT_CAT_PANE(dis_cat_list, main_cat_list))

    while not picked_event:
        python:
            prev_items, prev_cats = cat_lists[len(cat_lists)-1]

            # in this case, we only want to display the root category list
            if len(current_category) == 0:
                main_items = None

            else:

                # in this case, we have to generate the next menu
                # current_category contains the selected categories, so we
                # need to search using those categories

                # get list of unlocked events
                unlocked_events = Event.filterEvents(
                    evhand.event_database,
#                    full_copy=True,
                    category=(False,current_category),
                    unlocked=True,
                    pool=pool
                )

                # add deeper categories to a list
                # NOTE: not implemented because we dont have subfolders atm.
                #   maybe one day, but we would need a structure to link
                #   main categories to subcats

                # otherwise make sort event list
                no_cat_list = sorted(
                    unlocked_events.values(),
                    key=Event.getSortPrompt
                )

                # but remake into display
                no_cat_list = [(x.prompt, x.eventlabel) for x in no_cat_list]

                # NOTE: if we have subcategories, then we need to make a main
                # pane

                # no cateogries here
                main_cats = []

                # setup items
                main_items = no_cat_list

                """ KEEP this for legacy purposes
#            sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

            prompt_category_menu = []
            #Make a list of categories

            #Make a list of all categories
            subcategories=set([])
            for event in sorted_event_keys:
                if unlocked_events[event].category is not None:
                    new_categories=set(unlocked_events[event].category).difference(set(current_category))
                    subcategories=subcategories.union(new_categories)

            subcategories = list(subcategories)
            for category in sorted(subcategories, key=lambda s: s.lower()):
                #Don't list additional subcategories if adding them wouldn't change the same you are looking at
                test_unlock = Event.filterEvents(evhand.event_database,full_copy=True,category=[False,current_category+[category]],unlocked=True)

                if len(test_unlock) != len(sorted_event_keys):
                    prompt_category_menu.append([category.capitalize() + "...",category])


            #If we do have a category picked, make a list of the keys
            if sorted_event_keys is not None:
                for event in sorted_event_keys:
                    prompt_category_menu.append([unlocked_events[event].prompt,event])
                """

        call screen twopane_scrollable_menu(prev_items, main_items, evhand.LEFT_AREA, evhand.LEFT_XALIGN, evhand.RIGHT_AREA, evhand.RIGHT_XALIGN, len(current_category)) nopredict



        if _return in prev_cats:
            # we selected a category from teh previous pane
            python:
                if len(current_category) > 0:
                    current_category.pop()
                current_category.append(_return)

# TODO: if we have subcategories, this needs to be setup properly
#        elif _return in main_cats:
            # we selected a category in the main pane
#            $ current_category.append(_return)
#            $ cat_lists.append(main_pane)
#            $ is_root = False

#        elif _return == -2: # Thats enough for now
#            $picked_event = True

        elif _return == -1: # go back
            if len(current_category) > 0:
                $ current_category.pop()

        else: # event picked
            $picked_event = True
            $pushEvent(_return)

    return
