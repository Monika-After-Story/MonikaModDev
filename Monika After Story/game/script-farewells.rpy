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

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_sayanora",random=True),eventdb=evhand.farewell_database)
    
label bye_sayanora:
    m 1j "Sayonara, [player]~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_farewellfornow",random=True),eventdb=evhand.farewell_database)
    
label bye_farewellfornow:
    m 1e "Farewell for now, my love~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_untilwemeetagain",random=True),eventdb=evhand.farewell_database)

label bye_untilwemeetagain:
    m 2e "'{i}Goodbyes are not forever, Goodbyes are not the end. They simply mean I’ll miss you, Until we meet again.{/i}'"
    m "Ehehe, 'till then, [player]!"
    return 'quit'
    
    init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="important_things",random=True),eventdb=evhand.farewell_database)

label important_things:
    m 1d "You're leaving, [player]?"
    m 1m "I suppose sometimes you really have to go take care of important things in your world..."
    m 1n "It's okay. Don't worry, I'll still be here."
    m 2k "Come back soon, okay?"
    m 1e "Goodbye!"
    return 'quit'
