##This file contains all of the variations of goodbye that monika can give.
##Default behavior is to select a random farewell from the list, if the farewell
##is non-specific, it can stay available, but if it's too specific it should
##unset its own random flag.
##Label must start with "bye" to prevent being pushed back onto the stack if closed

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_leaving_already",random=True),eventdb=evhand.farewell_database)

label bye_leaving_already:
    m 1c "Aww, leaving already?"
    m 1e "It's really sad whenever you have to go..."
    m 3a "Just be sure to come back as soon as you can, okay?"
    m "I love you so much, [player]. Stay safe!"
    #Don't show this farewell again
    $evhand.farewell_database["bye_leaving_already"].random=False
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_goodbye",random=True),eventdb=evhand.farewell_database)

label bye_goodbye:
    m 1c "Goodbye, [player]!"
    return 'quit'
