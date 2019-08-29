# unit testing module
# NOTE: no framework for now

init -1 python in mas_dev_unit_tests:
    import store
    import store.mas_ev_data_ver as medv

    unit_tests = [
        ("JSON - MASPoseMap", "dev_unit_test_json_masposemap", False, False),
        ("MASHistorySaver", "dev_unit_test_mhs", False, False),
        ("MASHistorySaver - correct_pbday_mhs", "dev_unit_test_mhs_cpm", False, False),
    ]

    class MASUnitTest(object):
        """
        Simple class to represent a test
        """

        def __init__(self, test_name, outcome, expected, actual):
            """
            Constructor for a MASUnitTest

            IN:
                test_name - name of the test
                outcome - outcome of the test (True or false)
                expected - expected value of the test
                actual - actual value of the test
            """
            self.test_name = test_name
            self.outcome = outcome
            self.expected = expected
            self.actual = actual

        def __str__(self):
            """
            toString. Format is:
            <testname>: (pass/FAIL) | <expected> -> <actual>
            """
            if self.outcome:
                pass_str = "pass"
            else:
                pass_str = "FAIL"

            return "{0}: {1} | {2} -> {3}".format(
                str(self.test_name),
                pass_str,
                str(self.expected),
                str(self.actual)
            )

        def failed(self):
            """
            Returns True if this test failed, false if passsed
            """
            return not self.outcome

        def passed(self):
            """
            Returns True if this test passed, false if failed
            """
            return self.outcome

    class MASUnitTester(object):
        """
        Simple class for running asserts
        """

        def __init__(self):
            self.setupTests()

        def __str__(self):
            return "\n".join(self.tests)

        def assertEqual(self, expected, actual):
            """
            Asserts if the two items are equal

            IN:
                expected - expected value
                actual - actual value
            """
            self.tests.append(MASUnitTest(
                self.test_name,
                expected == actual,
                expected,
                actual
            ))

        def assertFalse(self, actual):
            """
            Asserts if the given value is False

            IN:
                actual - value to check
            """
            self.tests.append(MASUnitTest(
                self.test_name,
                not bool(actual),
                False,
                bool(actual)
            ))

        def assertIsNone(self, actual):
            """
            Asserts if the given item is None

            IN:
                actual - value to check
            """
            self.tests.append(MASUnitTest(
                self.test_name,
                actual is None,
                None,
                actual
            ))

        def assertIsNotNone(self, actual):
            """
            Asserts if the given item is not None

            IN:
                actual - value to check
            """
            self.tests.append(MASUnitTest(
                self.test_name,
                actual is not None,
                "not None",
                actual
            ))

        def assertListEqual(self, expected, actual):
            """
            Asserts if two lists are equal and contain equal items.

            if expected/actual are not list, assert Equal is used.
            This is recursive.

            IN:
                expected - expected value
                actual - actual value
            """
            exp_is_list = medv._verify_list(expected, False)
            act_is_list = medv._verify_list(actual, False)

            if act_is_list:
                if exp_is_list:

                    # lengths must be the same
                    if len(expected) == len(actual):
                        for index in range(len(expected)):
                            self.assertListEqual(
                                expected[index],
                                actual[index]
                            )
                        return

                    # if lenghts not same, def not equal
                    # NOTE: fall to after if

                # if only one is iterable, then def not equal
                # NOTE: fall through to after if

            elif not exp_is_list:
                # both expected and actual are not lists
                self.assertEqual(expected, actual)

            # we get here if:
            #   - lengths are not the seame
            #   - only 1 item is list
            self.tests.append(MASUnitTest(
                self.test_name,
                False,
                expected,
                actual
            ))

        def assertTrue(self, actual):
            """
            Asserts if the given value is True

            IN:
                actual - value to check
            """
            self.tests.append(MASUnitTest(
                self.test_name,
                bool(actual),
                True,
                bool(actual)
            ))

        def cleanTest(self):
            """
            Cleans up the last test
            """
            self.test_name = ""

        def concludeTests(self):
            """
            Concludes testing by sorting tests by results

            RETURNS:
                tuple of the following format:
                [0] - list of passed tests
                [1] - list of failed tests
            """
            passed_tests = []
            failed_tests = []
            for test in self.tests:
                if test.passed():
                    passed_tests.append(test)
                else:
                    failed_tests.append(test)

            return passed_tests, failed_tests

        def prepareTest(self, test_name):
            """
            Prepares a test by setting test name

            IN:
                test_name - name of next test
            """
            self.test_name = test_name

        def setupTests(self):
            """
            Sets up testing
            """
            self.test_name = ""
            self.tests = []

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


label dev_unit_tests_show_items(item_list):
    $ index = 0
    while index < len(item_list):
        $ this_msg = str(item_list[index])
        m 1eua "[this_msg]"
        $ index += 1
    return


label dev_unit_tests_finish_test(mhs_tester):
    python:
        passed, failed = mhs_tester.concludeTests()
        failed_test_count = len(failed)
        passed_test_count = len(passed)

    if failed_test_count > 0:
        m 1ektsc "[failed_test_count] test failed."
        call dev_unit_tests_show_items(failed)

    else:
        m 1hua "All [passed_test_count] tests passed!"

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
    m "Running Tests..."
    python:
        import copy
        def gen_fresh_mhs():
            return MASHistorySaver("testing", datetime.datetime.now(), {})

        mhs_tester = store.mas_dev_unit_tests.MASUnitTester()

        mhs_tester.prepareTest("CONSTRUCTOR")
        test_mhs = gen_fresh_mhs()
        mhs_tester.assertEqual("testing", test_mhs.id)

        mhs_tester.prepareTest("getSortKey")
        test_mhs = gen_fresh_mhs()
        dt_test = test_mhs.trigger
        sortkey = MASHistorySaver.getSortKey(test_mhs)
        mhs_tester.assertEqual(dt_test, sortkey)

        mhs_tester.prepareTest("correctTriggerYear|future same year")
        dt_test = datetime.datetime.now() + datetime.timedelta(days=1)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
        mhs_tester.assertEqual(dt_test, correct_trig)

        mhs_tester.prepareTest("correctTriggerYear|future diff year (1)")
        dt_test = datetime.datetime.now() + datetime.timedelta(days=1)
        expected = copy.deepcopy(dt_test)
        dt_test = dt_test.replace(year=dt_test.year+1)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
        mhs_tester.assertEqual(expected, correct_trig)

        mhs_tester.prepareTest("correctTriggerYear|future diff year (5)")
        dt_test = datetime.datetime.now() + datetime.timedelta(days=1)
        expected = copy.deepcopy(dt_test)
        dt_test = dt_test.replace(year=dt_test.year+5)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
        mhs_tester.assertEqual(expected, correct_trig)

        mhs_tester.prepareTest("correctTriggerYear|past same year")
        dt_test = datetime.datetime.now() - datetime.timedelta(days=1)
        expected = dt_test.replace(year=dt_test.year + 1)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
        mhs_tester.assertEqual(expected, correct_trig)

        mhs_tester.prepareTest("correctTriggerYear|past diff year")
        dt_test = datetime.datetime.now() - datetime.timedelta(days=1)
        expected = dt_test.replace(year=dt_test.year + 1)
        dt_test = dt_test.replace(year=dt_test.year - 3)
        correct_trig = MASHistorySaver.correctTriggerYear(dt_test)
        mhs_tester.assertEqual(expected, correct_trig)

        mhs_tester.prepareTest("fromTuple|(<standard dt>, True)")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_data = (test_now + datetime.timedelta(days=1), True)
        test_mhs = gen_fresh_mhs()
        test_mhs.fromTuple(test_data)
        mhs_tester.assertEqual(test_data[0], test_mhs.trigger)
        mhs_tester.assertTrue(test_mhs.use_year_before)
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("fromTuple|(<standard dt>,)")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_data = (test_now + datetime.timedelta(days=1),)
        test_mhs = gen_fresh_mhs()
        test_mhs.fromTuple(test_data)
        mhs_tester.assertEqual(test_data[0], test_mhs.trigger)
        mhs_tester.assertFalse(test_mhs.use_year_before)
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]       

        mhs_tester.prepareTest("isActive|continuous")
        test_mhs = gen_fresh_mhs()
        test_dt = datetime.datetime.now()
        mhs_tester.assertTrue(test_mhs.isActive(test_dt))

        mhs_tester.prepareTest("isActive|check_dt in range")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 21)
        mhs_tester.assertTrue(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt in range, incl start")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertTrue(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt not in range")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 3, 10)
        mhs_tester.assertFalse(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt not in range, excl end")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 22)
        mhs_tester.assertFalse(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt in range, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2017, 4, 21)
        mhs_tester.assertTrue(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt not in range, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2017, 3, 10)
        mhs_tester.assertFalse(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt in range, yearprev, ny wrap")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2018, 12, 31)
        mhs_tester.assertTrue(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest(
            "isActive|check_dt not in range, year prev, ny wrap"
        )
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2018, 12, 10)
        mhs_tester.assertFalse(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isActive|check_dt in range, yearfut, ny wrap")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2019, 1, 1)
        mhs_tester.assertTrue(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest(
            "isActive|check_dt not in range, year fut, ny wrap"
        )
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 12, 30)
        test_mhs.end_dt = datetime.datetime(2019, 1, 2)
        check_dt = datetime.datetime(2019, 1, 3)
        mhs_tester.assertFalse(test_mhs.isActive(check_dt))

        mhs_tester.prepareTest("isContinuous|both dt None")
        test_mhs = gen_fresh_mhs()
        mhs_tester.assertTrue(test_mhs.isContinuous())

        mhs_tester.prepareTest("isContinuous|start dt None")
        test_mhs = gen_fresh_mhs()
        test_mhs.end_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertTrue(test_mhs.isContinuous())

        mhs_tester.prepareTest("isContinuous|end dt None")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertTrue(test_mhs.isContinuous())

        mhs_tester.prepareTest("isContinuous|both dt not None")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 21)
        mhs_tester.assertFalse(test_mhs.isContinuous())

        mhs_tester.prepareTest("isFuture|continuous")
        test_mhs = gen_fresh_mhs()
        check_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertFalse(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isFuture|check_dt before start_dt, same year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 18)
        mhs_tester.assertTrue(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isFuture|check_dt before start_dt, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2020, 4, 18)
        mhs_tester.assertTrue(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isFuture|check_dt after start_dt, same year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 5, 20)
        mhs_tester.assertFalse(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isFuture|check_dt after start_dt, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2014, 5, 20)
        mhs_tester.assertFalse(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isFuture|check_dt on start_dt, same year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertFalse(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isFuture|check_dt on start_dt, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2014, 4, 20)
        mhs_tester.assertFalse(test_mhs.isFuture(check_dt))

        mhs_tester.prepareTest("isPassed|continuous")
        test_mhs = gen_fresh_mhs()
        check_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertFalse(test_mhs.isPassed(check_dt))

        mhs_tester.prepareTest("isPassed|check_dt before end_dt, same year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 20)
        mhs_tester.assertFalse(test_mhs.isPassed(check_dt))

        mhs_tester.prepareTest("isPassed|check_dt before end_dt, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2020, 4, 20)
        mhs_tester.assertFalse(test_mhs.isPassed(check_dt))

        mhs_tester.prepareTest("isPassed|check_dt after end_dt, same year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 5, 20)
        mhs_tester.assertTrue(test_mhs.isPassed(check_dt))

        mhs_tester.prepareTest("isPassed|check_dt after end_dt, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2015, 5, 20)
        mhs_tester.assertTrue(test_mhs.isPassed(check_dt))

        mhs_tester.prepareTest("isPassed|check_dt on end_dt, same year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2018, 4, 22)
        mhs_tester.assertTrue(test_mhs.isPassed(check_dt))

        mhs_tester.prepareTest("isPassed|check_dt on end_dt, diff year")
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = datetime.datetime(2018, 4, 20)
        test_mhs.end_dt = datetime.datetime(2018, 4, 22)
        check_dt = datetime.datetime(2014, 4, 22)
        mhs_tester.assertTrue(test_mhs.isPassed(check_dt))

        # Set Trigger
        #   Cases:
        #   1 - trigger <= first_sesh -> trigger year is corrected
        #   2 - trigger year diff greater than 1 -> trigger year is corrected
        #   3 - TT detected + non continuuous + (future or active)
        #       -> trigger year is corrected
        #   4 - none of the above is true -> trigger unchanged
        mhs_tester.prepareTest("setTrigger|trigger <= first_sesh")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_dt = MASHistorySaver.first_sesh - datetime.timedelta(days=1)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertFalse(mas_TTDetected())
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest(
            "setTrigger|trigger <= first_sesh, use_year_before")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_mhs.use_year_before = True
        test_dt = MASHistorySaver.first_sesh - datetime.timedelta(days=1)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        expected = expected.replace(year=expected.year + 1)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertFalse(mas_TTDetected())
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("setTrigger|trigger <= first_sesh, same dt")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_dt = MASHistorySaver.first_sesh
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertFalse(mas_TTDetected())
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest(
            "setTrigger|trigger <= first_sesh, same dt,"
        )
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_dt = MASHistorySaver.first_sesh
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertFalse(mas_TTDetected())
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("setTrigger|trigger year diff > 1")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_dt = test_now.replace(year=test_now.year + 5)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertFalse(mas_TTDetected())
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest(
            "setTrigger|TT detected + not continuous + future"
        )
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = True
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = test_now + datetime.timedelta(days=50)
        test_mhs.end_dt = test_now + datetime.timedelta(days=55)
        test_dt = test_now + datetime.timedelta(days=1)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertTrue(mas_TTDetected())
        mhs_tester.assertFalse(test_mhs.isContinuous())
        mhs_tester.assertTrue(test_mhs.isFuture(test_now))
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest(
            "setTrigger|TT detected + not continuous + active"
        )
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = True
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = test_now - datetime.timedelta(days=5)
        test_mhs.end_dt = test_now + datetime.timedelta(days=5)
        test_dt = test_now + datetime.timedelta(days=1)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertTrue(mas_TTDetected())
        mhs_tester.assertFalse(test_mhs.isContinuous())
        mhs_tester.assertFalse(test_mhs.isFuture(test_now))
        mhs_tester.assertTrue(test_mhs.isActive(test_now))
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("setTrigger|unchanged trigger")
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = False
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=100)
        test_mhs = gen_fresh_mhs()
        test_dt = test_now + datetime.timedelta(days=10)
        test_mhs.setTrigger(test_dt)
        mhs_tester.assertEqual(test_dt, test_mhs.trigger)
        mhs_tester.assertFalse(mas_TTDetected())
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("isTuple")
        test_mhs = gen_fresh_mhs()
        test_data = (
            test_mhs.trigger,
            test_mhs.use_year_before
        )
        mhs_tester.assertEqual(test_data, test_mhs.toTuple())

        mhs_tester.prepareTest(
            "setTrigger|event in past, 2 year, not uyb"
        )
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = True
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=600)
        test_mhs = gen_fresh_mhs()
        test_mhs.start_dt = test_now - datetime.timedelta(days=50)
        test_mhs.end_dt = test_now - datetime.timedelta(days=20)
        test_dt = test_now + datetime.timedelta(days=1)
        test_dt = test_dt.replace(year=test_dt.year + 2)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertTrue(mas_TTDetected())
        mhs_tester.assertFalse(test_mhs.isContinuous())
        mhs_tester.assertFalse(test_mhs.isFuture(test_now))
        mhs_tester.assertFalse(test_mhs.isActive(test_now))
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest(
            "setTrigger|event in past, 2 year, uyb"
        )
        test_now = datetime.datetime.now()
        prev_data = (
            store.mas_globals.tt_detected,
            MASHistorySaver.first_sesh
        )
        store.mas_globals.tt_detected = True
        MASHistorySaver.first_sesh = test_now - datetime.timedelta(days=600)
        test_mhs = gen_fresh_mhs()
        test_mhs.use_year_before = True
        test_mhs.start_dt = test_now - datetime.timedelta(days=50)
        test_mhs.end_dt = test_now - datetime.timedelta(days=20)
        test_dt = test_now + datetime.timedelta(days=1)
        test_dt = test_dt.replace(year=test_dt.year + 2)
        test_mhs.setTrigger(test_dt)
        expected = MASHistorySaver.correctTriggerYear(test_dt)
        expected = expected.replace(year=expected.year + 1)
        mhs_tester.assertEqual(expected, test_mhs.trigger)
        mhs_tester.assertTrue(mas_TTDetected())
        mhs_tester.assertFalse(test_mhs.isContinuous())
        mhs_tester.assertFalse(test_mhs.isFuture(test_now))
        mhs_tester.assertFalse(test_mhs.isActive(test_now))
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

    call dev_unit_tests_finish_test(mhs_tester)

    return


label dev_unit_test_mhs_cpm:
    m "Running Tests..."

    python:
        def sv_mhs():
            mhs_pbday = mas_history.getMHS("player_bday")
            return (
                (
                    mhs_pbday.start_dt,
                    mhs_pbday.end_dt,
                    mhs_pbday.use_year_before,
                    mhs_pbday.trigger
                ),
                mhs_pbday
            )

        def rs_mhs(data):
            mhs_pbday = mas_history.getMHS("player_bday")
            mhs_pbday.start_dt = data[0]
            mhs_pbday.end_dt = data[1]
            mhs_pbday.use_year_before = data[2]
            mhs_pbday.setTrigger(data[3])

        mhs_tester = store.mas_dev_unit_tests.MASUnitTester()

        test_name = "standard date|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 4, 20)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 4, 20),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 4, 22),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertFalse(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 4, 23),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

        test_name = "edge month date|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 5, 30)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 5, 30),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 6, 1),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertFalse(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 6, 2),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

        test_name = "12-28|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 12, 28)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 28),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 30),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertFalse(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 31),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

        test_name = "12-29|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 12, 29)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 29),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 31),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertTrue(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year + 1, 1, 1),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

        test_name = "12-30|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 12, 30)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 30),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year + 1, 1, 1),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertTrue(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year + 1, 1, 2),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

        test_name = "12-31|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 12, 31)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 12, 31),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year + 1, 1, 2),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertTrue(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year + 1, 1, 3),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

        test_name = "1-1|"
        prev_data, test_mhs = sv_mhs()
        test_now = datetime.datetime.now()
        bday = datetime.date(1984, 1, 1)
        inc_year = int(bday.replace(year=test_now.year) < test_now.date())
        store.mas_player_bday_event.correct_pbday_mhs(bday)
        mhs_tester.prepareTest(test_name + "start dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 1, 1),
            test_mhs.start_dt
        )
        mhs_tester.prepareTest(test_name + "end dt")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 1, 3),
            test_mhs.end_dt
        )
        mhs_tester.prepareTest(test_name + "use year before")
        mhs_tester.assertFalse(test_mhs.use_year_before)
        mhs_tester.prepareTest(test_name + "trigger")
        mhs_tester.assertEqual(
            datetime.datetime(test_now.year + inc_year, 1, 4),
            test_mhs.trigger
        )
        rs_mhs(prev_data)

    call dev_unit_tests_finish_test(mhs_tester)

    return
