## holiday info goes here
#
# TOC
#   [HOL010] - O31

############################### O31 ###########################################
# [HOL010]

default persistent._mas_o31_current_costume = None
# None - no costume
# "marisa" - witch costume
# "rin" - neko costume

default persistent._mas_o31_seen_costumes = None
# dict containing seen costumes for o31

default persistent._mas_o31_costume_greeting_seen = False
# set to true after seeing a costume greeting

define mas_o31_marisa_chance = 90
define mas_o31_rin_chance = 10

init 101 python:
    # o31 setup
    if persistent._mas_o31_seen_costumes is None:
        persistent._mas_o31_seen_costumes = {
            "marisa": False,
            "rin": False
        }

label mas_holiday_o31_autoload_check:
    $ import random
    $ mas_skip_visuals = True

    if persistent._mas_o31_current_costume is None:
        # select a costume. Once this has been selected, this is what monika
        # will wear until day change

        if random.randint(1,100) <= mas_o31_marisa_chance:
            $ persistent._mas_o31_current_costume = "marisa"
            $ selected_greeting = "greeting_o31_marisa"
            # TODO: decode the apprporiate cg

        else:
            $ persistent._mas_o31_current_costume = "rin"
            $ selected_greeting = "greeting_o31_rin"
            # TODO: decode the apprporiate cg

        $ persistent._mas_o31_seen_costumes[persistent._mas_o31_current_costume] = True

    jump ch30_post_restartevent_check


### o31 greetings
init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_marisa",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_o31_marisa:
    m "I am marisa"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_o31_rin",
            unlocked=True,
            category=[store.mas_greetings.TYPE_HOL_O31]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_o31_rin:
    m "I am rin"
    return
