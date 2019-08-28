# unit testing module
# NOTE: no framework for now

init -1 python in mas_dev_unit_tests:
    import store
    import store.mas_ev_data_ver as medv

    unit_tests = [
        ("JSON - MASPoseMap", "dev_unit_test_json_masposemap", False, False),
        ("JSON - MASPoseArms", "dev_unit_test_json_masposearms", False, False),
        (
            "JSON - MASPoseArms - JGroup",
            "dev_unit_test_json_masposearms_jgroup",
            False,
            False
        ),
        ("MASHistorySaver", "dev_unit_test_mhs", False, False),
    ]

    class MASUnitTest(object):
        """
        Simple class to represent a test
        """

        def __init__(self, test_name, outcome, expected, actual, ovrstr=None):
            """
            Constructor for a MASUnitTest

            IN:
                test_name - name of the test
                outcome - outcome of the test (True or false)
                expected - expected value of the test
                actual - actual value of the test
                ovrstr - if passed, then we display this instead of
                    the standard expected/actual string
            """
            self.test_name = test_name
            self.outcome = outcome
            self.expected = expected
            self.actual = actual
            self.ovrstr = ovrstr

        def __str__(self):
            """
            toString. Format is:
            <testname>: (pass/FAIL) | <expected> -> <actual>
            """
            if self.outcome:
                pass_str = "pass"
            else:
                pass_str = "FAIL"

            if self.ovrstr is None:
                ea_str = "{0} -> {1}".format(
                    str(self.expected),
                    str(self.actual)
                )
            else:
                ea_str = ovrstr

            return "{0}: {1} | {2}".format(
                str(self.test_name),
                pass_str,
                ea_str
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
        LEN_STR = "len mismatch: expected {0} -> actual {1}"
        KEY_STR = "expected key {0}, not found in actual"
        KEY_STR_A = "extra keys found in actual: {0}"

        def __init__(self):
            self.setupTests()

        def __str__(self):
            return "\n".join(self.tests)

        def _assertDictEqual(self, expected, actual):
            """
            Internal dict assertion. Assumes that given items are dicts.

            IN:
                expected - expected value
                actual - actual value

            RETURNS: True if equal, False if not
            """
            # lengths must be the same
            if len(expected) != len(actual):
                self.tests.append(MASUnitTest(
                    self.test_name,
                    False,
                    expected,
                    actual,
                    ovrstr=self.LEN_STR.format(len(expected), len(actual))
                ))
                return False

            # now check keys + values 
            a_keys = sorted(actual.keys())
            for e_key in expected:
                
                if e_key not in a_keys:
                    self.tests.append(MASUnitTest(
                        self.test_name,
                        False,
                        e_key,
                        None,
                        ovrstr=self.KEY_STR.format(e_key)
                    ))
                    return False

                # pop key off 
                a_keys.remove(e_key)
                if not self.assertEqual(expected[e_key], actual[e_key]):
                    return False

            # if any keys remain in a, then we had a mismatch 
            if len(a_keys) > 0:
                self.tests.append(MASUnitTest(
                    self.test_name,
                    False,
                    expected,
                    actual,
                    ovrstr=self.KEY_STR_A.format(a_keys)
                ))
                return False

            return True

        def _assertListEqual(self, expected, actual):
            """
            Internal list assertion. Assumes that the given items are lists.

            IN:
                expected - expected value
                actual - actual value

            RETURNS: True if equal, False if not
            """
            # lengths must be the same
            if len(expected) != len(actual):
                self.tests.append(MASUnitTest(
                    self.test_name,
                    False,
                    expected,
                    actual,
                    ovrstr=self.LEN_STR.format(len(expected), len(actual))
                ))
                return False

            # otherwise check each element
            for index in range(len(expected)):
                if not self.assertEqual(expected[index], actual[index]):
                    return False

            return True

        def assertDictEqual(self, expected, actual):
            """
            Asserts if two dicts are equal and contain equal items

            If expected/actual are not dict, assertListEqual is used
            this is recursive.
            """
            if (
                    medv._verify_dict(expected, False)
                    and medv._verify_dict(actual, False)
            ):
                return self._assertDictEqual(expected, actual)

            # otherwise use assEqual
            return self.assertEqual(expected, actual)

        def assertEqual(self, expected, actual):
            """
            Asserts if the two items are equal

            IN:
                expected - expected value
                actual - actual value

            RETURNS: True if equal, False if not
            """
            # First, delegate to the correct type
            if (
                    medv._verify_dict(expected, False)
                    and medv._verify_dict(actual, False)
            ):
                return self._assertDictEqual(expected, actual)

            elif (
                    medv._verify_list(expected, False)
                    and medv._verify_list(actual, False)
            ):
                return self._assertListEqual(expected, actual)

            # otherwise, we compare the two directly
            outcome = expected == actual
            self.tests.append(MASUnitTest(
                self.test_name,
                outcome,
                expected,
                actual
            ))
            return outcome

        def assertFalse(self, actual):
            """
            Asserts if the given value is False

            IN:
                actual - value to check

            RETURNS: True if False, False if not
            """
            outcome = not bool(actual)
            self.tests.append(MASUnitTest(
                self.test_name,
                outcome,
                False,
                bool(actual)
            ))
            return outcome

        def assertIsNone(self, actual):
            """
            Asserts if the given item is None

            IN:
                actual - value to check

            RETURNS: True if None, False if not
            """
            outcome = actual is None
            self.tests.append(MASUnitTest(
                self.test_name,
                outcome,
                None,
                actual
            ))
            return outcome

        def assertIsNotNone(self, actual):
            """
            Asserts if the given item is not None

            IN:
                actual - value to check

            RETURNS: True if not None, False if None
            """
            outcome = actual is not None
            self.tests.append(MASUnitTest(
                self.test_name,
                outcome,
                "not None",
                actual
            ))
            return outcome

        def assertListEqual(self, expected, actual):
            """
            Asserts if two lists are equal and contain equal items

            if expected/actual are not list, we use assertEqual.

            IN:
                expected - expected value
                actual - actual value

            RETURNS: True if equal, False if not
            """
            if (
                    medv._verify_list(expected, False)
                    and medv._verify_list(actual, False)
            ):
                return self._assertListEqual(expected, actual)

            # otherwise, use assertEqual, which should fail in most
            # circumstances
            return self.assertEqual(expected, actual)

        def assertTrue(self, actual):
            """
            Asserts if the given value is True

            IN:
                actual - value to check

            RETURNS: True if True, False if not
            """
            outcome = bool(actual)
            self.tests.append(MASUnitTest(
                self.test_name,
                outcome,
                True,
                bool(actual)
            ))
            return outcome

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

    if failed_test_count > 0:
        m 1ektsc "[failed_test_count] test failed."
        call dev_unit_tests_show_items(failed)

    else:
        m 1hua "All tests passed!"

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

    if _return == "RETURN":
        return

    if renpy.has_label(_return):
        call expression _return
        m 1tuu "Unit test over"
        jump dev_unit_tests

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


label dev_unit_test_json_masposearms:
    python:
        def gen_data(jgroup, jdata):
            data = {}
            for index in range(len(jgroup)):
                data[jgroup[index]] = jdata[index]
            return data

        def gen_both(bdata):
            return gen_data(MASPoseArms.J_NAME_BOTH, bdata)

        def gen_left(ldata):
            return gen_data(MASPoseArms.J_NAME_LEFT, ldata)

        def gen_right(rdata):
            return gen_data(MASPoseArms.J_NAME_RIGHT, rdata)

        bargs = MASPoseArms.J_NAME_BOTH
        largs = MASPoseArms.J_NAME_LEFT
        rargs = MASPoseArms.J_NAME_RIGHT
        mpa_tester = store.mas_dev_unit_tests.MASUnitTester()
        
        mpa_tester.prepareTest("no data passed")
        test_data = {}
        actual = MASPoseArms.fromJSON(test_data, [], 0)
        mpa_tester.assertIsNone(actual.both)
        mpa_tester.assertIsNone(actual.both_back)
        mpa_tester.assertIsNone(actual.both_front)
        mpa_tester.assertIsNone(actual.left)
        mpa_tester.assertIsNone(actual.left_back)
        mpa_tester.assertIsNone(actual.left_front)
        mpa_tester.assertIsNone(actual.right)
        mpa_tester.assertIsNone(actual.right_back)
        mpa_tester.assertIsnone(actual.right_front)

        mpa_tester.prepareTest("no data passed, extra props")
        test_data = {}
        ex_data = {
            "extra": 123
        }
        test_data.update(ex_data)
        actual = MASPoseArms.fromJson(test_data, [], 0)
        mpa_tester.assertIsNone(actual.both)
        mpa_tester.assertIsNone(actual.both_back)
        mpa_tester.assertIsNone(actual.both_front)
        mpa_tester.assertIsNone(actual.left)
        mpa_tester.assertIsNone(actual.left_back)
        mpa_tester.assertIsNone(actual.left_front)
        mpa_tester.assertIsNone(actual.right)
        mpa_tester.assertIsNone(actual.right_back)
        mpa_tester.assertIsnone(actual.right_front)
        mpa_tester.assertEqual(ex_data, test_data)

    return


label dev_unit_test_json_masposearms_jgroup:
    m "Running Tests..."
    python:
        def gen_data(jgroup, jdata):
            data = {}
            for index in range(len(jgroup)):
                data[jgroup[index]] = jdata[index]
            return data

        prop_name = "prop_name"
        prop_back = "prop_back"
        prop_front = "prop_front"
        prop_args = (prop_name, prop_back, prop_front)
        mpa_tester = store.mas_dev_unit_tests.MASUnitTester()

        mpa_tester.prepareTest("prop_name not exist")
        test_data = gen_data(prop_args, (1, 2, 3))
        test_data.pop(prop_name)
        mpa_tester.assertIsNone(MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        ))
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("prop_name is None")
        test_data = gen_data(prop_args, (None, 2, 3))
        mpa_tester.assertIsNone(MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        ))
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("prop_name is not str")
        test_data = gen_data(prop_args, (1, True, False))
        mpa_tester.assertIsNone(MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        ))
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("prop_back is not bool")
        test_data = gen_data(prop_args, ("test", 1, False))
        mpa_tester.assertIsNone(MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        ))
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("prop_front is not bool")
        test_data = gen_data(prop_args, ("test", True, 1))
        mpa_tester.assertIsNone(MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        ))
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("valid props, data created")
        expected = ("test", True, False)
        test_data = gen_data(prop_args, expected)
        actual = MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        )
        mpa_tester.assertEqual(expected, actual)
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("valid props, no back, data created")
        test_data = gen_data(prop_args, ("test", True, True))
        test_data.pop(prop_back)
        expected = ("test", False, True)
        actual = MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        )
        mpa_tester.assertEqual(expected, actual)
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("valid props, no front,data created")
        test_data = gen_data(prop_args, ("test", True, True))
        test_data.pop(prop_front)
        expected = ("test", True, False)
        actual = MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        )
        mpa_tester.assertEqual(expected, actual)
        mpa_tester.assertEqual(0, len(test_data))

        mpa_tester.prepareTest("valid props, data created, extra props")
        expected = ("test", True, False)
        test_data = gen_data(prop_args, expected)
        ex_data = {
            "extra": 123
        }
        test_data.update(ex_data)
        actual = MASPoseArms._fromJSON_parseJGroup(
            test_data,
            prop_args,
            [],
            0
        )
        mpa_tester.assertEqual(expected, actual)
        mpa_tester.assertEqual(ex_data, test_data)

    call dev_unit_tests_finish_test(mpa_tester)

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
        #   2 - trigger.year > now.year + 1 -> trigger yera is corrected
        #   3 - TT detected + not continuous + (isFuture or isActive)
        #   4 - none of the above cases are True -> trigger year is unchanged
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
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("setTrigger|trigger.year > now.year + 1")
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
        store.mas_globals.tt_detected = prev_data[0]
        MASHistorySaver.first_sesh = prev_data[1]

        mhs_tester.prepareTest("isTuple")
        test_mhs = gen_fresh_mhs()
        test_data = (
            test_mhs.trigger,
            test_mhs.use_year_before
        )
        mhs_tester.assertEqual(test_data, test_mhs.toTuple())

    call dev_unit_tests_finish_test(mhs_tester)

    return
