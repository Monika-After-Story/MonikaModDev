# unit testing module
# NOTE: no framework for now

init -1 python in mas_dev_unit_tests:
    import store

    unit_tests = [
        ("JSON - MASPoseMap", "dev_unit_test_json_masposemap", False, False),
        ("MASHistorySaver", "dev_unit_test_mhs", False, False),
    ]

init 10 python in mas_dev_unit_tests:
    from store.mas_moods import MOOD_AREA, MOOD_XALIGN


label dev_unit_tests_show_pass:
    m 1hua "passed"
    return

label dev_unit_tests_show_fail:
    m 1ektsc "!!!FAILED!!!"
    return 

label dev_unit_tests_show_msgs(msg_list, format_text=False):
    $ index = 0
    while index < len(msg_list):
        $ this_msg = msg_list[index]
        if format_text:
            $ this_msg = renpy.substitute(this_msg)
        m 1eua "[this_msg]"
        $ _history_list.pop()
        $ index += 1
    return


label dev_unit_tests_assertEqual(expected, actual):
    if expected == actual:
        call dev_unit_tests_show_pass
    else:
        call dev_unit_tests_show_fail
    return


label dev_unit_tests_assertIsNone(actual):
    if actual is None:
        call dev_unit_tests_show_pass
    else:
        call dev_unit_tests_show_fail
    return 


label dev_unit_tests_assertIsNotNone(actual):
    if actual is not None:
        call dev_unit_tests_show_pass
    else:
        call dev_unit_tests_show_fail
    return


label dev_unit_tests_assertTrue(actual):
    if actual:
        call dev_unit_tests_show_pass
    else:
        call dev_unit_tests_show_fail
    return


label dev_unit_tests_assertFalse(actual):
    if actual:
        call dev_unit_tests_show_fail
    else:
        call dev_unit_tests_show_pass
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_unit_tests",
            category=["dev"],
            prompt="UNIT TESTS",
            pool=True,
            unlocked=True
        )
    )


label dev_unit_tests:
    $ final_item = ("RETURN", False, False, False, 20)
    call screen mas_gen_scrollable_menu(store.mas_dev_unit_tests.unit_tests, store.mas_dev_unit_tests.MOOD_AREA, store.mas_dev_unit_tests.MOOD_XALIGN, final_item)

    if _return and renpy.has_label(_return):
        call expression _return
        m 1tuu "Unit test over"

    return


## unit tests

label dev_unit_test_json_masposemap:
    # TESTING: MASPoseMAP json function
    
    python:
        none_type = type(None)

        # each case is a tuple:
        #   [0]: item to pass into the function (this is assumed to be args)
        #   [1]: type of expected result
        cases = [
            # empty dict
            (({}, False, False), MASPoseMap),
            (({}, False, True), MASPoseMap), # this will give warnings
            (({}, True, False), MASPoseMap),
            (({}, True, True), MASPoseMap),

            # non fallback cases (good)
            (({"default": True}, False, False), MASPoseMap),
            (({"l_default": True}, False, False), MASPoseMap),
            (({
                "default": True,
                "use_reg_for_l": True
            }, False, False), MASPoseMap),
            (({
                "default": True,
                "l_default": True
            }, False, False), MASPoseMap),
            (({
                "p1": True,
                "p2": True,
                "p3": False,
                "p4": True,
                "p5": False,
                "p6": True
            }, False, False), MASPoseMap),

            # non fallback cases (bad)
            (({
                "default": 10,
                "l_default": "bad",
                "use_reg_for_l": 122,
                "p1": "alsobad",
                "p2": {},
                "p3": 23,
                "p4": [],
                "p5": "berybad",
                "p6": -12
            }, False, False), none_type),

            # fallback casese (good)
            (({"default": "steepling"}, False, True), MASPoseMap), # message
            (({"l_default": "steepling"}, False, True), MASPoseMap), # message
            (({
                "default": "crossed",
                "use_reg_for_l": True
            }, False, True), MASPoseMap),
            (({
                "default": "restleftpointright",
                "l_default": "pointright"
            }, False, True), MASPoseMap),
            (({ # message
                "p1": "down",
                "p2": "def|def",
                "p3": "steepling",
                "p4": "restleftpointright",
                "p5": "crossed",
                "p6": "pointright"
            }, False, True), MASPoseMap),

            # fallback cases (bad)
            (({"default": True}, False, True), none_type),
            (({"l_default": 121}, False, True), none_type),
            (({
                "p1": "not a pose",
                "p2": 332,
                "p3": -12,
                "p4": "p5",
                "p5": "default",
                "p6": "def^def"
            }, False, True), none_type),

            # fallback cases with warnings
            (({"default": "steepling"}, False, True), MASPoseMap),
            (({"use_reg_for_l": True}, False, True), MASPoseMap),

            # acs cases (bad)
            (({"default": True}, True, True), none_type),
            (({
                "p1": True,
                "p2": False,
                "p3": 19
            }, True, True), none_type),

            # acs cases (good)
            (({"default": "0"}, True, True), MASPoseMap),

            # extra props
            (({
                "one two": None,
                "oatmeal": False,
            }, False, False), MASPoseMap),
            (({
                "one two": None,
                "oatmeal": False,
            }, False, True), MASPoseMap),

        ]

        for case_args, exp_result in cases:
            errs = []
            warns = []
            actual_result = MASPoseMap.fromJSON(
                *case_args,
                errs=errs,
                warns=warns
            )
            actual_result = type(actual_result)
            if actual_result == exp_result:
                renpy.show("monika 1hua")
                renpy.say(m, "passed")
            else:
                renpy.show("monika 1ektsc")
                renpy.say(m, "!!!FAILED!!!")

            msgs = list(errs)
            msgs.extend(warns)

            if len(msgs) > 0:
                renpy.say(m, "with messages:")
                renpy.call_in_new_context("dev_unit_tests_show_msgs", msgs)


    return
            

label dev_unit_test_mhs:
    python:
        def gen_fresh_mhs():
            return MASHistorySaver("testing", datetime.datetime.now(), {})

    m "CONSTRUCTOR:"
    python:
        test_mhs = gen_fresh_mhs()
    call dev_unit_tests_assertEqual("testing", test_mhs.mhs_id)

    m "getSortKey"
    python:
        dt_test = test_mhs.trigger
        sortkey = MASHistorySaver.getSortKey(test_mhs)
    call dev_unit_tests_assertEqual(dt_test, sortkey)

    m "correctTriggerYear|future same year"
    python:
        dt_test = datetime.datetime.now() + datetime.timedelta(days=1)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
    call dev_unit_tests_assertEqual(dt_test, correct_trig)

    m "correctTriggerYear|future diff year"

    m "correctTriggerYear|past same year"
    python:
        dt_test = datetime.datetime.now() - datetime.timedelta(days=1)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
        dt_test = dt_test.replace(year=dt_test.year + 1)
    call dev_unit_tests_assertEqual(dt_test, correct_trig)

    m "fromTuple|(<future dt>, True)"
    python:
        test_data = (
            datetime.datetime.now() + datetime.timedelta(days=1),
            True
        )
        test_mhs = gen_fresh_mhs()
        test_mhs.fromTuple(test_data)
    call dev_unit_tests_assertEqual(test_data[0], test_mhs.trigger)
    call dev_unit_tests_assertTrue(test_mhs.use_year_before)

    m "fromTuple|(<future dt>, False)"
    python:
        test_data = (
            datetime.datetime.now() + datetime.timedelta(days=1),
            False
        )
        test_mhs = gen_fresh_mhs()
        test_mhs.fromTuple(test_data)
    call dev_unit_tests_assertEqual(test_data[0], test_mhs.trigger)
    call dev_unit_tests_assertFalse(test_mhs.use_year_before)

#    m "fromTuple|(<past dt>, True)"
##    python:
 #       testdat

    m "isActive|continuous"
    python:
        test_mhs = gen_fresh_mhs()
        test_dt = datetime.datetime.now()
    call dev_unit_tests_assertTrue(test_mhs.isActive(test_dt))

    m "isActive|check_dt in range"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 21)
    call dev_unit_tests_assertTrue(test_mhs.isActive(check_dt))

    m "isActive|check_dt not in range"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 3, 10)
    call dev_unit_tests_assertFalse(test_mhs.isActive(check_dt))

    m "isActive|check_dt in range, diff year"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2017, 4, 21)
    call dev_unit_tests_assertTrue(test_mhs.isActive(check_dt))

    m "isActive|check_dt not in range, diff year"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2017, 3, 10)
    call dev_unit_tests_assertFalse(test_mhs.isActive(check_dt))

    m "isActive|check_dt in range, yearprev, ny wrap"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2018, 12, 31)
    call dev_unit_tests_assertTrue(test_mhs.isActive(check_dt))

    m "isActive|check_dt not in range, year prev, ny wrap"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2018, 12, 10)
    call dev_unit_tests_assertFalse(test_mhs.isActive(check_dt))

    m "isActive|check_dt in range, yearfut, ny wrap"
    python:
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2019, 1, 1)
    call dev_unit_tests_assertTrue(test_mhs.isActive(check_dt))

    m "isActive|check_dt






    return
