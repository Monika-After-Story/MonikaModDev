
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



# Module that defines functions for story event handling
# Assumes:
#   persistent.event_list
#   persistent.current_monikatopic
init python:

    def addEvent(event, eventdb=persistent.event_database):
        #
        # Adds an event object to the given eventdb dict
        # Properly checksfor label and conditional statements
        # This function ensures that a bad item is not added to the database
        #
        # IN:
        #   event - the Event object to add to database
        #   eventdb - The Event databse (dict) we want to add to
        #       (Default: persistent.event_database)

        if type(eventdb) is not dict:
            raise EventException("Given db is not of type dict")
        if type(event) is not Event:
            raise EventException("'" + str(event) + "' is not an Event object")
        if not renpy.has_label(event.eventlabel):
            raise EventException("'" + event.eventlabel + "' does NOT exist")
        if event.conditional is not None:
            try:
                if eval(event.conditional):
                    pass
            except:
                raise EventException("Syntax error in conditional statement for event '" + event.eventlabel + "'.")

        # now this event has passsed checks, we can add it to the db
        eventdb.setdefault(event.eventlabel, event)

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
                and not persistent.current_monikatopic.startswith('i_greeting')):
                pushEvent(persistent.current_monikatopic)
                pushEvent('continue_event')
            persistent.current_monikatopic = 0
        return



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
        if event_label in monika_random_topics:
            if not persistent.event_database[event_label].unlocked:
                python:
                    persistent.event_database[event_label].unlocked=True
                    persistent.event_database[event_label].unlock_date=datetime.datetime.now()

        if _return == 'quit':
            $persistent.closed_self = True #Monika happily closes herself
            jump _quit

        $ allow_dialogue = True
        show monika 1 at t11 zorder 2 with dissolve #Return monika to normal pose
    else:
        return False

    return event_label

# This either picks an event from the pool or events or, sometimes offers a set
# of three topics to get an event from.
label unlock_prompt:
    python:
        pool_event_keys = Event.filterEvents(persistent.event_database,unlocked=False,pool=True).keys()

        if len(pool_event_keys)>0:
            unlock_event = renpy.random.choice(pool_event_keys)
            persistent.event_database[unlock_event].unlocked = True
            persistent.event_database[unlock_event].unlock_date = datetime.datetime.now()

    return

#The prompt menu is what pops up when hitting the "Talk" button, it shows a list
#of options for talking to Monika, including the ability to ask her questions
#pulled from a random set of prompts.

label prompt_menu:
    $allow_dialogue = False

    python:
        unlocked_events = Event.filterEvents(persistent.event_database,unlocked=True)
        sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

        unseen_events = []
        for event in sorted_event_keys:
            if not seen_event(event):
                unseen_events.append(event)

        repeatable_events = Event.filterEvents(persistent.event_database,unlocked=True,pool=False)
    #Top level menu
    menu:
        m "Pick something to talk about?"

        "{b}Unseen.{/b}" if len(unseen_events)>0:
            call show_prompt_list(unseen_events)

        "Ask a question.":
            call prompts_categories(True)

        "Repeat conversation." if len(repeatable_events)>0:
            call prompts_categories(False)

        "Nevermind":
            $_return = None

    $allow_dialogue = True
    jump ch30_loop

label show_prompt_list(sorted_event_keys):

    #Get list of unlocked prompts, sorted by unlock date
    python:
        prompt_menu_items = []
        for event in sorted_event_keys:
            prompt_menu_items.append([unlocked_events[event].prompt,event])

    hide monika
    show monika_waiting_img zorder 2 at i32
    call screen scrollable_menu(prompt_menu_items)
    hide monika_waiting_img
    show monika 1a zorder 2 at i32

    $pushEvent(_return)

    return

label prompts_categories(pool=True):

    $current_category = []
    $picked_event = False
    while not picked_event:
        python:
            #Get list of unlocked events in this category
            unlocked_events = Event.filterEvents(persistent.event_database,full_copy=True,category=[False,current_category],unlocked=True,pool=pool)
            sorted_event_keys = Event.getSortedKeys(unlocked_events,include_none=True)

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
                test_unlock = Event.filterEvents(persistent.event_database,full_copy=True,category=[False,current_category+[category]],unlocked=True)

                if len(test_unlock) != len(sorted_event_keys):
                    prompt_category_menu.append([category.capitalize() + "...",category])


            #If we do have a category picked, make a list of the keys
            if sorted_event_keys is not None:
                for event in sorted_event_keys:
                    prompt_category_menu.append([unlocked_events[event].prompt,event])

        call screen scrollable_menu(prompt_category_menu) nopredict

        if _return in subcategories:
            $current_category.append(_return)
        else:
            $picked_event = True
            $pushEvent(_return)

    return
