# Module that defines functions for story event handling
# Assumes:
#   persistent.event_list
#   persistent.current_monikatopic
init python:

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

    def callNextEvent():
        #
        # This calls the next event in the list. It returns the name of the
        # event called or None if the list is empty or the label is invalid
        #
        # IN:
        #
        # ASSUMES:
        #   persistent.event_list
        #   persistent.current_monikatopic

        event_label = popEvent()
        if event_label and renpy.has_label(event_label):
            globals()['allow_dialogue'] = False
            previous_topic = persistent.current_monikatopic
            state_change = renpy.call_in_new_context(event_label)
            persistent.current_monikatopic=previous_topic
            if event_label in monika_random_topics:
                monika_random_topics.remove(event_label)
            if state_change == 'quit':
                renpy.quit(0)
            globals()['allow_dialogue'] = True
        else:
            return None

        return event_label

    def restartEvent():
        #
        # This checks if there is a persistent topic, and if there was push it
        # back on the stack with a little comment.
        #
        # IN:
        #
        if persistent.current_monikatopic:
            #don't push greetings back on the stack
            if not persistent.current_monikatopic.startswith('greeting_'):
                pushEvent(persistent.current_monikatopic)
                pushEvent('continue_event')
            persistent.current_monikatopic = 0
        return
