# testin gweather
init 5 python:
    # available only if moni affection is normal+
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_change_weather",
            category=["dev"],
            prompt="TEST WEATHER CHANGE",
            pool=True,
            unlocked=True
        )
    )

label dev_change_weather:
    show monika at t21

    python:
        # build menu list
        import store.mas_weather as mas_weather
        import store.mas_moods as mas_moods

        # we assume that we will always have more than 1
        # default should always be at the top
        weathers = [(mas_weather_def.prompt, mas_weather_def, False, False)]

        # build other weather list
        other_weathers = [
            (mw_obj.prompt, mw_obj, False, False)
            for mw_id, mw_obj in mas_weather.WEATHER_MAP.iteritems()
            if mw_id != "def"
        ]

        # sort other weather list
        other_weathers.sort()

        # build full list
        weathers.extend(other_weathers)

        # now add final quit item
        final_item = (mas_weather.WEAT_RETURN, False, False, False, 20)

    # call scrollable pane
    call screen mas_gen_scrollable_menu(weathers, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item=final_item)

    # return value False? then return
    if _return is False or mas_current_weather == _return:
        return

    # otherwise, we can change the weather now
    # NOTE: here is where youc an react to a weather change
    # TODO: react to changing weather to rain if you like/nolike
    # TODO: react to thunder in the same vein as rain
    # TODO: maybe react to snow?

    # finally change the weather
    call mas_change_weather(_return)

    m "If you want to change the weather again, just ask me, okay?"

    return
