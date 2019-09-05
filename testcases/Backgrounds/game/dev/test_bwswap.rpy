#Allow bg selector for this
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_bgsel",
            category=["dev"],
            prompt="TEST BGSWAP",
            pool=True,
            unlocked=True
        )
    )

label dev_bgsel:

    m 1hua "Sure!"

label dev_bgsel_loop:

    show monika 1eua at t21

    $ renpy.say(m, "What background would you like?", interact=False)

    python:
        # build menu list
        import store.mas_background as mas_background
        import store.mas_moods as mas_moods

        # we assume that we will always have more than 1
        # default should always be at the top
        backgrounds = [(mas_background_def.prompt, mas_background_def, False, False)]

        # build other backgrounds list
        other_backgrounds = [
            (mbg_obj.prompt, mbg_obj, False, False)
            for mbg_id, mbg_obj in mas_background.BACKGROUND_MAP.iteritems()
            if mbg_id != "spaceroom"
        ]

        # sort other backgrounds list
        other_backgrounds.sort()

        # build full list
        backgrounds.extend(other_backgrounds)

        # now add final quit item
        final_item = (mas_background.BACKGROUND_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(backgrounds, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item)

    $ sel_background = _return

    show monika at t11

    # return value False? then return
    if sel_background is False:
        m 1eka "Oh, alright."
        m "If you want to go somewhere, just ask, okay?"
        return

    if sel_background == mas_current_background:
        m 1hua "We're here right now, silly."
        m "Try again~"
        jump dev_bgsel_loop

    call mas_background_change(sel_background, True, True)
    return

init -1 python:
    #Default spaceroom
    mas_background_test = MASBackground(
        #Identification
        "test",
        "Test",

        #Day/Night
        image_day="test_bgroom_def",
        image_night="test_bgroom_def_night",

        #Rain Day/Night
        image_rain_day="test_bgroom_rain",
        image_rain_night="test_bgroom_rain_night",

        #Overcast Day/Night
        image_overcast_day="test_bgroom_overcast",
        image_overcast_night="test_bgroom_overcast_night",

        #Snow Day/Night
        image_snow_day="test_bgroom_snow",
        image_snow_night="test_bgroom_snow_night",

        #These masks don't get windows or calendar
        hide_calendar=True,
        hide_masks=True,

        #For the sake of testing, we do want progressive
        disable_progressive=False,

        #Test room should always be unlocked
        unlocked=True,
    )

#START: Image defs
#Day
image test_bgroom_def = "mod_assets/location/test/test-def.png"
image test_bgroom_overcast = "mod_assets/location/test/test-overcast.png"
image test_bgroom_rain = "mod_assets/location/test/test-rain.png"
image test_bgroom_snow = "mod_assets/location/test/test-snow.png"

#Night
image test_bgroom_def_night = "mod_assets/location/test/test-def-n.png"
image test_bgroom_overcast_night = "mod_assets/location/test/test-overcast-n.png"
image test_bgroom_rain_night = "mod_assets/location/test/test-rain-n.png"
image test_bgroom_snow_night = "mod_assets/location/test/test-snow-n.png"