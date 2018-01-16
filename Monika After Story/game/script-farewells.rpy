##This file contains all of the variations of goodbye that monika can give.
##Default behavior is to select a random farewell from the list, if the farewell
##is non-specific, it can stay available, but if it's too specific it should
##unset its own random flag.

init 5 python:
    addEvent(Event(eventlabel="monika_leaving_already",random=True),eventdb=persistent.farewell_database)

label monika_leaving_already:
    m 1c "Aww, leaving already?"
    m 1e "It's really sad whenever you have to go..."
    m 3a "Just be sure to come back as soon as you can, okay?"
    m "I love you so much, [player]. Stay safe!"
    #Don't show this farewell again
    $persistent.farewell_database["monika_leaving_already"].random=False
    return 'quit'

init 5 python:
    addEvent(Event(eventlabel="monika_goodbye",random=True),eventdb=persistent.farewell_database)

label monika_goodbye:
    m 1c "Goodbye, [player]!"
    return 'quit'
