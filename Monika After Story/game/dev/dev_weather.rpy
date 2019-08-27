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
    call screen mas_gen_scrollable_menu(weathers, mas_moods.MOOD_AREA, mas_moods.MOOD_XALIGN, final_item)

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


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_weather_sampler",
            category=["dev"],
            prompt="SAMPLE WEATHER",
            pool=True,
            unlocked=True
        )
    )

label dev_weather_sampler:
    m 1eua "Lets sample some weather."
    $ store.mas_weather.shouldRainToday()
    m "Make sure to set 'persistent._mas_should_rain_today` to what you want."
    m "It is currently [persistent._mas_should_rain_today]."

    m 1eua "sample size please"
    $ sample_size = renpy.input("enter sample size", allow="0123456789")
    $ sample_size = store.mas_utils.tryparseint(sample_size, 10000)
    if sample_size > 10000:
        $ sample_size = 10000 # anyhting longer takes too long
    $ str_sample_size = str(sample_size)

    m 1eua "using sample size of [str_sample_size]"

    python:
        # prepare data:
        results = {
            "default": 0
        }
        totals = 0

        # loop over sample size
        for count in range(sample_size):
            got_weather = mas_shouldRain()
            totals += 1
            
            if got_weather is None:
                results["default"] += 1

            elif got_weather.prompt in results:
                results[got_weather.prompt] += 1

            else:
                results[got_weather.prompt] = 0

        # done with sampling, output results
        with open(renpy.config.basedir + "/weather_sample", "w") as outdata:
            for weather_name, count in results.iteritems():
                outdata.write("{0},{1} -> {2}\n".format(
                    weather_name,
                    count,
                    count/float(totals)
                ))

    m "check files for 'weather_sample' for more info."
    return

