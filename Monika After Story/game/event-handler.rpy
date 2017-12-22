# Module that defines functions for story event handling
# Assumes:
#   persistent.event_list
#   persistent.current_monikatopic
init python:

 def pushPoem (_poem_name):
        #
        # Adds the poem to an event list for poems that will be shown
        #
        #
        #
        # ASSUMES
        #   persistent.poem_list
        #
        persistent.seen_poem_list.insert(0, _poem_name)
        current_poem.append(_poem_name)
        return

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

    if not current_poem == []: #Check if any commands inputed (such as poem request)
        
        
        #should probably stick a thing in to resume from a poem that may have crashed or soemthing
        $ poem_commentary = "response_" + current_poem[0]
        $ allow_dialogue = False
        
        call expression poem_commentary
        
        $ current_poem = []
        if persistent.seen_poem_list[0] in monika_random_poems:
            $ monika_random_poems.remove(persistent.seen_poem_list[0])
       
        $ allow_dialogue = True
        show monika 1 at tinstant zorder 2 #Return monika to normal pose

    $event_label = popEvent()
    if event_label and renpy.has_label(event_label):

        $ allow_dialogue = False
        call expression event_label from _call_expression
        $ persistent.current_monikatopic=0

        if event_label in monika_random_topics:
            $monika_random_topics.remove(event_label)

        if _return == 'quit':
            $persistent.closed_self = True #Monika happily closes herself
            $ renpy.quit(0)

        $ allow_dialogue = True
        show monika 1 at t11 zorder 2 with dissolve #Return monika to normal pose
    else:
        return False

    return event_label
