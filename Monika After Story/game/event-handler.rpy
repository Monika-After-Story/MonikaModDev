# Module that defines functions for story event handling
# Assumes:
#   persistent.event_list
#   persistent.current_monikatopic

# NOTE: proof oc concept
# transform to have monika just chill
image monika_waiting_img:
    "monika 1a"
    1.0
    "monika 1c"
    1.0
    "monika 1h"
    1.0
    "monika 1o"
    1.0
    "monika 1g"
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
        True # last_seen
    )

    # set defaults
    if persistent._mas_event_init_lockdb_template is None:
        persistent._mas_event_init_lockdb_template = mas_init_lockdb_template

    elif len(persistent._mas_event_init_lockdb_template) != len(mas_init_lockdb_template):
        # differing lengths mean we have new items to deal with

        for ev_key in persistent._mas_event_init_lockdb:
            stored_lock_row = persistent._mas_event_init_lockdb[ev_key]

            # splice and dice
            lock_row = list(mas_init_lockdb_template)
            lock_row[0:len(stored_lock_row)] = list(stored_lock_row)
            persistent._mas_event_init_lockdb[ev_key] = tuple(lock_row)

    # set db defaults
    if persistent._mas_event_init_lockdb is None:
        persistent._mas_event_init_lockdb = dict()

    # initalizes LOCKDB for the Event class
    Event.INIT_LOCKDB = persistent._mas_event_init_lockdb

# special store to contain scrollable menu constants
init -1 python in evhand:

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
    LAST_SEEN_DELTA = datetime.timedelta(hours=2)

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

init python:
    import store.evhand as evhand

    def addEvent(event, eventdb=evhand.event_database):
        #
        # Adds an event object to the given eventdb dict
        # Properly checksfor label and conditional statements
        # This function ensures that a bad item is not added to the database
        #
        # IN:
        #   event - the Event object to add to database
        #   eventdb - The Event databse (dict) we want to add to
        #       (Default: evhand.event_database)

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
        ev = eventdb.get(eventlabel, None)

        hideEvent(
            ev,
            lock=lock,
            derandom=derandom,
            depool=depool,
            decond=decond
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

        if event:

            if lock:
                event.unlocked = False

            if derandom:
                event.random = False

            if depool:
                event.pool = False

            if decond:
                event.conditional = None


    def lockEvent(ev):
        """
        Locks the given event object

        IN:
            ev - the event object to lock
        """
        hideEvent(ev, lock=True)


    def lockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Locks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        hideEventLabel(evlabel, lock=True, eventdb=eventdb)


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
        if ev:
            ev.unlocked = True


    def unlockEventLabel(evlabel, eventdb=evhand.event_database):
        """
        Unlocks the given event label

        IN:
            evlabel - event label of the event to lock
            eventdb - Event database to find this label
        """
        unlockEvent(eventdb.get(evlabel, None))


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
        if persistent.current_monikatopic:
            #don't push greetings back on the stack
            if (not persistent.current_monikatopic.startswith('greeting_')
                    and not persistent.current_monikatopic.startswith('i_greeting')
                    and not persistent.current_monikatopic.startswith('bye')
                    and not persistent.current_monikatopic.startswith('ch30_reload')
                ):
                pushEvent(persistent.current_monikatopic)
                pushEvent('continue_event')
                persistent.current_monikatopic = 0
        return


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


# This calls the next event in the list. It returns the name of the
# event called or None if the list is empty or the label is invalid
#
# ASSUMES:
#   persistent.event_list
#   persistent.current_monikatopic
label call_next_event:


    $event_label = popEvent()
    if event_label and renpy.has_label(event_label):
        $ allow_dialogue = False
        if not seen_event(event_label): #Give 15 xp for seeing a new event
            $grant_xp(xp.NEW_EVENT)
        call expression event_label from _call_expression
        $ persistent.current_monikatopic=0

        #if this is a random topic, make sure it's unlocked for prompts
        $ ev = evhand.event_database.get(event_label, None)
        if ev is not None:
            if ev.random and not ev.unlocked:
                python:
                    ev.unlocked=True
                    ev.unlock_date=datetime.datetime.now()

            # increment shown count
            $ ev.shown_count += 1
            $ ev.last_seen = datetime.datetime.now()

        if _return == 'quit':
            $persistent.closed_self = True #Monika happily closes herself
            jump _quit

        # only allow dialogue if the event list is empty
        $ allow_dialogue = len(persistent.event_list) == 0
        show monika 1 at t11 zorder 2 with dissolve #Return monika to normal pose
    else:
        return False

    return event_label

# This either picks an event from the pool or events or, sometimes offers a set
# of three topics to get an event from.
label unlock_prompt:
    python:
        pool_event_keys = Event.filterEvents(evhand.event_database,unlocked=False,pool=True).keys()

        if len(pool_event_keys)>0:
            unlock_event = renpy.random.choice(pool_event_keys)
            evhand.event_database[unlock_event].unlocked = True
            evhand.event_database[unlock_event].unlock_date = datetime.datetime.now()

    return

#The prompt menu is what pops up when hitting the "Talk" button, it shows a list
#of options for talking to Monika, including the ability to ask her questions
#pulled from a random set of prompts.

label prompt_menu:
    $allow_dialogue = False

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

    elif madechoice == "moods":
        call mas_mood_start from _call_mas_mood_start
        if not _return:
            jump prompt_menu

    elif madechoice == "goodbye":
        call mas_farewell_start from _call_select_farewell

    else: #nevermind
        $_return = None

    show monika at t11
    $allow_dialogue = True
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
