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

default persistent._mas_o31_costumes_allowed = None
# true if user gets to see costumes
# this is set once and never touched again

default persistent._mas_o31_in_o31_mode = False
# True if we should be in o31 mode (aka viginette)
# This should be only True if:
#   user is NOT returning monika on o31 from a date/trip taken before o31
#   user's current session started on o31

define mas_o31_marisa_chance = 90
define mas_o31_rin_chance = 10
define mas_o31_in_o31_mode = False

init 101 python:
    # o31 setup
    if persistent._mas_o31_seen_costumes is None:
        persistent._mas_o31_seen_costumes = {
            "marisa": False,
            "rin": False
        }

    if not mas_isO31():
        # disable o31 mode
        persistent._mas_o31_in_o31_mode = False
        

init -11 python in mas_o31_event:
    import store
    import store.mas_dockstat as mds
    import store.mas_ics as mis

    # setup the docking station for o31
    o31_cg_station = store.MASDockingStation(mis.o31_cg_folder)

    # cg available?
    o31_cg_decoded = False


    def decodeImage(key):
        """
        Attempts to decode a cg image

        IN:
            key - o31 cg key to decode

        RETURNS True upon success, False otherwise
        """
        return mds.decodeImages(o31_cg_station, mis.o31_map, [key])

    
    def removeImages():
        """
        Removes decoded images at the end of their lifecycle
        """
        mds.removeImages(o31_cg_station, mis.o31_map)


label mas_holiday_o31_autoload_check:
    # ASSUMPTIONS:
    #   monika is NOT outside
    #   monika is NOT returning home
    #   we are NOT in introduction

    python:
        import random
        mas_skip_visuals = True
        persistent._mas_o31_in_o31_mode = True

        if (
                persistent._mas_o31_current_costume is None
                and persistent._mas_o31_costumes_allowed
            ):
            # select a costume. Once this has been selected, this is what monika
            # will wear until day change

            if random.randint(1,100) <= mas_o31_marisa_chance:
                persistent._mas_o31_current_costume = "marisa"
                selected_greeting = "greeting_o31_marisa"
                store.mas_o31_event.o31_cg_decoded = (
                    store.mas_o31_event.decodeImage("o31mcg")
                )

            else:
                persistent._mas_o31_current_costume = "rin"
                selected_greeting = "greeting_o31_rin"
                # store.mas_o31_event.o31_cg_decoded = (
    #                    store.mas_o31_event.decodeImage("o31rcg")
    #                )

            persistent._mas_o31_seen_costumes[persistent._mas_o31_current_costume] = True

        if persistent._mas_o31_in_o31_mode:
            store.mas_globals.show_vignette = True
            mas_forceRain()

    jump ch30_post_restartevent_check

### o31 images
image mas_o31_marisa_cg = "mod_assets/monika/cg/o31_marisa_cg.png"
image mas_o31_rin_cg = "mod_assets/monika/cg/o31_rin_cg.png"

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
    # TODO handle visuals
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
    # TODO handle visuals
    m "I am rin"
    return

init 5 python:
    addEvent(
        Event(
            persistent.greeting_database,
            eventlabel="greeting_trick_or_treat_back",
            unlocked=True,
            random=True,
            category=[store.mas_greetings.TYPE_TRICK_TREAT]
        ),
        eventdb=evhand.greeting_database
    )

label greeting_trick_or_treat_back:
    # TODO Say something and do things
    m "..."
    return

### o31 farewells
init 5 python:
    if mas_isO31():
        addEvent(
            Event(
                persistent.farewell_database,
                eventlabel="bye_trick_or_treat",
                unlocked=True,
                prompt="I'm going to take you trick or treating",
                pool=True
            ),
            eventdb=evhand.farewell_database
        )

label bye_trick_or_treat:
    # TODO dialogue should go here
    m "Sure thing!"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_TRICK_TREAT
    return 'quit'
