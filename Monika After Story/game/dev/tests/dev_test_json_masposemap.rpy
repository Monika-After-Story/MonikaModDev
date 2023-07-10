init -2 python in mas_unittests:
    @testclass
    class JSONMASPoseMapTester(unittest.TestCase):
        prop_mpm_type = "mpm_type"
        prop_default = "default"
        prop_l_default = "l_default"
        prop_urfl = "use_reg_for_l"
        prop_p1 = "p1"
        prop_p2 = "p2"
        prop_p3 = "p3"
        prop_p4 = "p4"
        prop_p5 = "p5"
        prop_p6 = "p6"
        pose1 = "steepling"
        pose2 = "crossed"
        pose3 = "restleftpointright"
        pose4 = "pointright"
        pose5 = "def|def"
        pose6 = "down"
        as_zero = "0"
        as_one = "1"
        as_star = "*"
        as_null = ""
        pa_both = "both_pa"
        pa_left = "left_pa"
        pa_right = "right_pa"
        ic_one = "1"
        ic_zero = "0"
        ic_custom = "special"

        @staticmethod
        def gen_data(jgroup, jdata):
            data = {}
            for index in range(len(jgroup)):
                data[jgroup[index]] = jdata[index]
            return data

        @staticmethod
        def gen_both(bdata):
            return gen_data(MASPoseArms.J_NAME_BOTH, bdata)

        @staticmethod
        def gen_left(ldata):
            return gen_data(MASPoseArms.J_NAME_LEFT, ldata)

        @staticmethod
        def gen_right(rdata):
            return gen_data(MASPoseArms.J_NAME_RIGHT, rdata)

        @staticmethod
        def arms_both(extra=False):
            data = gen_both(("both_pa", True, True))
            if extra:
                data.update({
                    "extra": 123,
                    "extra2": 69,
                })
            return data

        @staticmethod
        def arms_lr(extra=False):
            data = gen_left(("left_pa", True, True))
            data.update(gen_right(("right_pa", True, True)))
            if extra:
                data.update({
                    "extra": 123,
                    "extra2": 10,
                })
            return data

        def test_no_data_passed(self):
            test_data = {}
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("no data passed, should be none"):
                self.assertIsNone(actual)

            with self.subTest("no data passed, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_bad_mpm_type(self):
            test_data = {
                self.prop_mpm_type: "bad"
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("bad mpm type, should be none"):
                self.assertIsNone(actual)

            with self.subTest("bad mpm type, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_invalid_mpm(self):
            test_data = {
                self.prop_mpm_type: -1
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("invalid mpm type, should be none"):
                self.assertIsNone(actual)

            with self.subTest("invalid mpm type, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_bad_use_reg_for_l_type(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_urfl: 10
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("bad use reg for l type, should be none"):
                self.assertIsNone(actual)

            with self.subTest("bad use reg for l type, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("bad use reg for l type, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_valid_types(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
            }
            valid_types = (store.MASPoseMap.MPM_TYPE_FB, store.MASPoseMap.MPM_TYPE_IC)
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0, valid_types)

            with self.subTest("valid types, should be none"):
                self.assertIsNone(actual)

            with self.subTest("valid types, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("valid types, log length should be 1"):
                self.assertEqual(1, len(log))

        # testing all mpm type 0 interactions
        def test_mpm_type_0_no_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, no props, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, no props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 0, no props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 0, no props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 0, no props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 0, no props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 0, no props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 0, no props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, no props, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_0_no_props_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: True
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, no props, default, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, no props, default, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, no props, default, pose2 should be true"):
                self.assertTrue(actual.get(self.pose2, False))

            with self.subTest("mpm type 0, no props, default, pose3 should be true"):
                self.assertTrue(actual.get(self.pose3, False))

            with self.subTest("mpm type 0, no props, default, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, no props, default, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 0, no props, default, pose6 should be true"):
                self.assertTrue(actual.get(self.pose6, False))

            with self.subTest("mpm type 0, no props, default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, no props, default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_0_no_props_invalid_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: 10
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, invalid default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 0, no props, invalid default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_0_no_props_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_l_default: False
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, no props, l_default, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, no props, l_default, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 0, no props, l_default, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 0, no props, l_default, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 0, no props, l_default, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 0, no props, l_default, pose5 should be false"):
                self.assertFalse(actual.get(self.pose5, True))

            with self.subTest("mpm type 0, no props, l_default, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 0, no props, l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, no props, l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_0_no_props_invalid_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_l_default: 10
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, invalid l_default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 0, no props, invalid l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_0_no_props_default_urfl(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: True,
                self.prop_urfl: True
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, default + urfl, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, no props, default + urfl, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, no props, default + urfl, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, no props, default + urfl, pose2 should be true"):
                self.assertTrue(actual.get(self.pose2, False))

            with self.subTest("mpm type 0, no props, default + urfl, pose3 should be true"):
                self.assertTrue(actual.get(self.pose3, False))

            with self.subTest("mpm type 0, no props, default + urfl, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, no props, default + urfl, pose5 should be true"):
                self.assertTrue(actual.get(self.pose5, False))

            with self.subTest("mpm type 0, no props, default + urfl, pose6 should be true"):
                self.assertTrue(actual.get(self.pose6, False))

            with self.subTest("mpm type 0, no props, default + urfl, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, no props, default + urfl, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_0_no_props_default_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: True,
                self.prop_l_default: False
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, no props, default + l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, no props, default + l_default, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, no props, default + l_default, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, no props, default + l_default, pose2 should be true"):
                self.assertTrue(actual.get(self.pose2, False))

            with self.subTest("mpm type 0, no props, default + l_default, pose3 should be true"):
                self.assertTrue(actual.get(self.pose3, False))

            with self.subTest("mpm type 0, no props, default + l_default, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, no props, default + l_default, pose5 should be false"):
                self.assertFalse(actual.get(self.pose5, True))

            with self.subTest("mpm type 0, no props, default + l_default, pose6 should be true"):
                self.assertTrue(actual.get(self.pose6, False))

            with self.subTest("mpm type 0, no props, default + l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, no props, default + l_default, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_0_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                "extra": 123,
                "extra2": 69
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, extra props, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, extra props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 0, extra props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 0, extra props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 0, extra props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 0, extra props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 0, extra props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 0, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, extra props, log length should be 4"):
                self.assertEqual(4, len(log))

        def test_mpm_type_0_valid_1_2_5(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_p1: True,
                self.prop_p2: False,
                self.prop_p5: True,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, valid 1,2,5, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, valid 1,2,5, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, valid 1,2,5, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, valid 1,2,5, pose2 should be false"):
                self.assertFalse(actual.get(self.pose2, True))

            with self.subTest("mpm type 0, valid 1,2,5, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 0, valid 1,2,5, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 0, valid 1,2,5, pose5 should be true"):
                self.assertTrue(actual.get(self.pose5, False))

            with self.subTest("mpm type 0, valid 1,2,5, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 0, valid 1,2,5, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, valid 1,2,5, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_0_valid_3_4_6(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_p3: False,
                self.prop_p4: True,
                self.prop_p6: False,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, valid 3,4,6, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, valid 3,4,6, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, valid 3,4,6, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 0, valid 3,4,6, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 0, valid 3,4,6, pose3 should be false"):
                self.assertFalse(actual.get(self.pose3, True))

            with self.subTest("mpm type 0, valid 3,4,6, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, valid 3,4,6, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 0, valid 3,4,6, pose6 should be false"):
                self.assertFalse(actual.get(self.pose6, True))

            with self.subTest("mpm type 0, valid 3,4,6, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, valid 3,4,6, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_0_valid_all_no_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_p1: True,
                self.prop_p2: False,
                self.prop_p3: False,
                self.prop_p4: True,
                self.prop_p5: True,
                self.prop_p6: False,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, valid all, no defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, valid all, no defaults, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, valid all, no defaults, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, valid all, no defaults, pose2 should be false"):
                self.assertFalse(actual.get(self.pose2, True))

            with self.subTest("mpm type 0, valid all, no defaults, pose3 should be false"):
                self.assertFalse(actual.get(self.pose3, True))

            with self.subTest("mpm type 0, valid all, no defaults, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, valid all, no defaults, pose5 should be true"):
                self.assertTrue(actual.get(self.pose5, False))

            with self.subTest("mpm type 0, valid all, no defaults, pose6 should be false"):
                self.assertFalse(actual.get(self.pose6, True))

            with self.subTest("mpm type 0, valid all, no defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, valid all, no defaults, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_0_valid_all_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: True,
                self.prop_l_default: False,
                self.prop_p1: True,
                self.prop_p2: False,
                self.prop_p3: False,
                self.prop_p4: True,
                self.prop_p5: True,
                self.prop_p6: False,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, valid all, defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, valid all, defaults, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, valid all, defaults, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, valid all, defaults, pose2 should be false"):
                self.assertFalse(actual.get(self.pose2, True))

            with self.subTest("mpm type 0, valid all, defaults, pose3 should be false"):
                self.assertFalse(actual.get(self.pose3, True))

            with self.subTest("mpm type 0, valid all, defaults, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, valid all, defaults, pose5 should be true"):
                self.assertTrue(actual.get(self.pose5, False))

            with self.subTest("mpm type 0, valid all, defaults, pose6 should be false"):
                self.assertFalse(actual.get(self.pose6, True))

            with self.subTest("mpm type 0, valid all, defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, valid all, defaults, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_0_one_invalid_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: True,
                self.prop_l_default: False,
                self.prop_p1: True,
                self.prop_p2: False,
                self.prop_p3: False,
                self.prop_p4: 10,
                self.prop_p5: True,
                self.prop_p6: False,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, one invalid defaults, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 0, one invalid defaults, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_0_valid_all_defaults_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_ED,
                self.prop_default: True,
                self.prop_l_default: False,
                self.prop_p1: True,
                self.prop_p2: False,
                self.prop_p3: False,
                self.prop_p4: True,
                self.prop_p5: True,
                self.prop_p6: False,
                "extra": 123,
                "extra2": 10,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 0, valid all, defaults, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 0, valid all, defaults, extra props, mpm type should be MPM_TYPE_ED"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_ED, actual._mpm_type)

            with self.subTest("mpm type 0, valid all, defaults, extra props, pose1 should be true"):
                self.assertTrue(actual.get(self.pose1, False))

            with self.subTest("mpm type 0, valid all, defaults, extra props, pose2 should be false"):
                self.assertFalse(actual.get(self.pose2, True))

            with self.subTest("mpm type 0, valid all, defaults, extra props, pose3 should be false"):
                self.assertFalse(actual.get(self.pose3, True))

            with self.subTest("mpm type 0, valid all, defaults, extra props, pose4 should be true"):
                self.assertTrue(actual.get(self.pose4, False))

            with self.subTest("mpm type 0, valid all, defaults, extra props, pose5 should be true"):
                self.assertTrue(actual.get(self.pose5, False))

            with self.subTest("mpm type 0, valid all, defaults, extra props, pose6 should be false"):
                self.assertFalse(actual.get(self.pose6, True))

            with self.subTest("mpm type 0, valid all, defaults, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 0, valid all, defaults, extra props, log length should be 2"):
                self.assertEqual(2, len(log))

        # type  1
        def test_mpm_type_1_no_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, no props, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, no props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, no props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, no props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, no props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, no props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, no props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, no props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, no props, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_1_no_props_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: self.pose3,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, no props, default, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, no props, default, pose1 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, no props, default, pose2 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, no props, default, pose3 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, no props, default, pose4 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, no props, default, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, no props, default, pose6 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, no props, default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, no props, default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_1_no_props_invalid_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: "test"
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, invalid default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 1, no props, invalid default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_1_no_props_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_l_default: self.pose3,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, no props, l_default, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, no props, l_default, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, no props, l_default, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, no props, l_default, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, no props, l_default, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, no props, l_default, pose5 should be the same as pose 3"):
                self.assertEqual(self.pose3, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, no props, l_default, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, no props, l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, no props, l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_1_no_props_invalid_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_l_default: "test",
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, invalid l_default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 1, no props, invalid l_default, log length should be 1"):
                self.assertEqual(1, len(log))


        def test_mpm_type_1_no_props_default_urfl(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: self.pose3,
                self.prop_urfl: True
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, default + urfl, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, no props, default + urfl, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, no props, default + urfl, pose1 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, no props, default + urfl, pose2 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, no props, default + urfl, pose3 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, no props, default + urfl, pose4 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, no props, default + urfl, pose5 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, no props, default + urfl, pose6 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, no props, default + urfl, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, no props, default + urfl, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_1_no_props_default_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: self.pose3,
                self.prop_l_default: self.pose4,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, no props, default + l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, no props, default + l_default, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, no props, default + l_default, pose1 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, no props, default + l_default, pose2 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, no props, default + l_default, pose3 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, no props, default + l_default, pose4 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, no props, default + l_default, pose5 should be the same as pose4"):
                self.assertEqual(self.pose4, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, no props, default + l_default, pose6 should be the same as pose3"):
                self.assertEqual(self.pose3, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, no props, default + l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, no props, default + l_default, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_1_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                "extra": 123,
                "extra2": 69
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, extra props, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, extra props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, extra props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, extra props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, extra props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, extra props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, extra props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, extra props, log length should be 4"):
                self.assertEqual(4, len(log))

        def test_mpm_type_1_valid_1_2_5(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_p1: self.pose2,
                self.prop_p2: self.pose3,
                self.prop_p5: self.pose4,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, valid 1,2,5, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, valid 1,2,5, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, valid 1,2,5, pose1 should be the same as pose 2"):
                self.assertEqual(self.pose2, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, valid 1,2,5, pose2 should be the same as pose 3"):
                self.assertEqual(self.pose3, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, valid 1,2,5, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, valid 1,2,5, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, valid 1,2,5, pose5 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, valid 1,2,5, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, valid 1,2,5, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, valid 1,2,5, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_1_valid_3_4_6(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_p3: self.pose2,
                self.prop_p4: self.pose3,
                self.prop_p6: self.pose4,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, valid 3 4 6, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, valid 3 4 6, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, valid 3 4 6, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, valid 3 4 6, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, valid 3 4 6, pose3 should be the same as pose 2"):
                self.assertEqual(self.pose2, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, valid 3 4 6, pose4 should be the same as pose 3"):
                self.assertEqual(self.pose3, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, valid 3 4 6, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, valid 3 4 6, pose6 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, valid 3 4 6, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, valid 3 4 6, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_1_valid_all_no_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_p1: self.pose3,
                self.prop_p2: self.pose4,
                self.prop_p3: self.pose5,
                self.prop_p4: self.pose1,
                self.prop_p5: self.pose6,
                self.prop_p6: self.pose2,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, valid all, no defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, valid all, no defaults, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, valid all, no defaults, pose1 should be the same as pose 3"):
                self.assertEqual(self.pose3, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, valid all, no defaults, pose2 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, valid all, no defaults, pose3 should be the same as pose 5"):
                self.assertEqual(self.pose5, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, valid all, no defaults, pose4 should be the same as pose 1"):
                self.assertEqual(self.pose1, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, valid all, no defaults, pose5 should be the same as pose 6"):
                self.assertEqual(self.pose6, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, valid all, no defaults, pose6 should be the same as pose 2"):
                self.assertEqual(self.pose2, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, valid all, no defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, valid all, no defaults, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_1_valid_all_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: self.pose3,
                self.prop_l_default: self.pose4,
                self.prop_p1: self.pose6,
                self.prop_p2: self.pose4,
                self.prop_p3: self.pose4,
                self.prop_p4: self.pose5,
                self.prop_p5: self.pose2,
                self.prop_p6: self.pose5,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, valid all, defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, valid all, defaults, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, valid all, defaults, pose1 should be the same as pose 6"):
                self.assertEqual(self.pose6, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, valid all, defaults, pose2 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, valid all, defaults, pose3 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, valid all, defaults, pose4 should be the same as pose 5"):
                self.assertEqual(self.pose5, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, valid all, defaults, pose5 should be the same as pose 2"):
                self.assertEqual(self.pose2, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, valid all, defaults, pose6 should be the same as pose 5"):
                self.assertEqual(self.pose5, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, valid all, defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, valid all, defaults, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_1_one_invalid_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: self.pose3,
                self.prop_l_default: self.pose4,
                self.prop_p1: self.pose6,
                self.prop_p2: self.pose4,
                self.prop_p3: 10,
                self.prop_p4: self.pose5,
                self.prop_p5: self.pose2,
                self.prop_p6: self.pose5,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, one invalid defaults, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 1, one invalid defaults, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_1_valid_all_defaults_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_FB,
                self.prop_default: self.pose3,
                self.prop_l_default: self.pose4,
                self.prop_p1: self.pose6,
                self.prop_p2: self.pose4,
                self.prop_p3: self.pose4,
                self.prop_p4: self.pose5,
                self.prop_p5: self.pose2,
                self.prop_p6: self.pose5,
                "extra": 123,
                "extra2": 10,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 1, valid all, defaults, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 1, valid all, defaults, extra props, mpm type should be MPM_TYPE_FB"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_FB, actual._mpm_type)

            with self.subTest("mpm type 1, valid all, defaults, extra props, pose1 should be the same as pose 6"):
                self.assertEqual(self.pose6, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 1, valid all, defaults, extra props, pose2 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 1, valid all, defaults, extra props, pose3 should be the same as pose 4"):
                self.assertEqual(self.pose4, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 1, valid all, defaults, extra props, pose4 should be the same as pose 5"):
                self.assertEqual(self.pose5, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 1, valid all, defaults, extra props, pose5 should be the same as pose 2"):
                self.assertEqual(self.pose2, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 1, valid all, defaults, extra props, pose6 should be the same as pose 5"):
                self.assertEqual(self.pose5, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 1, valid all, defaults, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 1, valid all, defaults, extra props, log length should be 2"):
                self.assertEqual(2, len(log))

        # 2

        def test_mpm_type_2_no_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, no props, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, no props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, no props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, no props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, no props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, no props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, no props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, no props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, no props, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_2_no_props_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: self.as_one,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, no props, default, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, no props, default, pose1 should be the same as default"):
                self.assertEqual(self.as_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, no props, default, pose2 should be the same as default"):
                self.assertEqual(self.as_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, no props, default, pose3 should be the same as default"):
                self.assertEqual(self.as_one, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, no props, default, pose4 should be the same as default"):
                self.assertEqual(self.as_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, no props, default, pose5 should be the same as default"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, no props, default, pose6 should be the same as default"):
                self.assertEqual(self.as_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, no props, default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, no props, default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_2_no_props_invalid_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: "test"
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, invalid default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 2, no props, invalid default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_2_no_props_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_l_default: self.as_star,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, no props, l_default, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, no props, l_default, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, no props, l_default, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, no props, l_default, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, no props, l_default, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, no props, l_default, pose5 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, no props, l_default, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, no props, l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, no props, l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_2_no_props_invalid_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_l_default: "test",
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, invalid l_default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 2, no props, invalid l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_2_no_props_default_urfl(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: self.as_one,
                self.prop_urfl: True
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, default, urfl, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, no props, default, urfl, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, no props, default, urfl, pose1 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, no props, default, urfl, pose2 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, no props, default, urfl, pose3 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, no props, default, urfl, pose4 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, no props, default, urfl, pose5 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, no props, default, urfl, pose6 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, no props, default, urfl, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, no props, default, urfl, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_2_no_props_default_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: self.as_one,
                self.prop_l_default: self.as_star,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, no props, default, l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, no props, default, l_default, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, no props, default, l_default, pose1 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, no props, default, l_default, pose2 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, no props, default, l_default, pose3 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, no props, default, l_default, pose4 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, no props, default, l_default, pose5 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, no props, default, l_default, pose6 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, no props, default, l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, no props, default, l_default, log length should be 1"):
                self.assertEqual(0, len(log))

        def test_mpm_type_2_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                "extra": 123,
                "extra2": 69
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, extra props, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, extra props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, extra props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, extra props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, extra props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, extra props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, extra props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, extra props, log length should be 4"):
                self.assertEqual(4, len(log))

        def test_mpm_type_2_valid_1_2_5(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_p1: self.as_one,
                self.prop_p2: self.as_zero,
                self.prop_p5: self.as_star,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, valid 1 2 5, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, valid 1 2 5, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, valid 1 2 5, pose1 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, valid 1 2 5, pose2 should be the same as as_zero"):
                self.assertEqual(self.as_zero, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, valid 1 2 5, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, valid 1 2 5, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, valid 1 2 5, pose5 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, valid 1 2 5, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, valid 1 2 5, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, valid 1 2 5, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_2_valid_3_4_6(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_p3: self.as_zero,
                self.prop_p4: self.as_star,
                self.prop_p6: self.as_one,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, valid 3 4 6, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, valid 3 4 6, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, valid 3 4 6, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, valid 3 4 6, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, valid 3 4 6, pose3 should be the same as as_zero"):
                self.assertEqual(self.as_zero, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, valid 3 4 6, pose4 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, valid 3 4 6, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, valid 3 4 6, pose6 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, valid 3 4 6, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, valid 3 4 6, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_2_valid_all_no_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_p1: self.as_zero,
                self.prop_p2: self.as_one,
                self.prop_p3: self.as_star,
                self.prop_p4: self.as_one,
                self.prop_p5: self.as_zero,
                self.prop_p6: self.as_star,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, valid all, no defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, valid all, no defaults, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, valid all, no defaults, pose1 should be the same as as_zero"):
                self.assertEqual(self.as_zero, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, valid all, no defaults, pose2 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, valid all, no defaults, pose3 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, valid all, no defaults, pose4 should be the same as as_one"):
                self.assertEqual(self.as_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, valid all, no defaults, pose5 should be the same as as_zero"):
                self.assertEqual(self.as_zero, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, valid all, no defaults, pose6 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, valid all, no defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, valid all, no defaults, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_2_valid_all_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: self.as_zero,
                self.prop_l_default: self.as_one,
                self.prop_p1: self.as_star,
                self.prop_p2: self.as_star,
                self.prop_p3: self.as_star,
                self.prop_p4: self.as_star,
                self.prop_p5: self.as_star,
                self.prop_p6: self.as_star,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, valid all, defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, valid all, defaults, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, valid all, defaults, pose1 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, valid all, defaults, pose2 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, valid all, defaults, pose3 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, valid all, defaults, pose4 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, valid all, defaults, pose5 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, valid all, defaults, pose6 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, valid all, defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, valid all, defaults, log length should be 2"):
                self.assertEqual(0, len(log))

        def test_mpm_type_2_one_invalid_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: self.as_zero,
                self.prop_l_default: self.as_one,
                self.prop_p1: self.as_star,
                self.prop_p2: self.as_star,
                self.prop_p3: "test",
                self.prop_p4: self.as_star,
                self.prop_p5: self.as_star,
                self.prop_p6: self.as_star,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, one invalid defaults, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 2, one invalid defaults, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_2_valid_all_defaults_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_AS,
                self.prop_default: self.as_zero,
                self.prop_l_default: self.as_one,
                self.prop_p1: self.as_star,
                self.prop_p2: self.as_star,
                self.prop_p3: self.as_star,
                self.prop_p4: self.as_star,
                self.prop_p5: self.as_star,
                self.prop_p6: self.as_star,
                "extra": 123,
                "extra2": 69,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 2, valid all, defaults, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 2, valid all, defaults, extra props, mpm type should be MPM_TYPE_AS"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_AS, actual._mpm_type)

            with self.subTest("mpm type 2, valid all, defaults, extra props, pose1 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 2, valid all, defaults, extra props, pose2 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 2, valid all, defaults, extra props, pose3 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 2, valid all, defaults, extra props, pose4 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 2, valid all, defaults, extra props, pose5 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 2, valid all, defaults, extra props, pose6 should be the same as as_star"):
                self.assertEqual(self.as_star, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 2, valid all, defaults, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 2, valid all, defaults, extra props, log length should be 2"):
                self.assertEqual(2, len(log))


        # 4
        def test_mpm_type_4_no_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, no props, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, no props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, no props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, no props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, no props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, no props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, no props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, no props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, no props, log length should be 1"):
                self.assertEqual(2, len(log))

        def test_mpm_type_4_no_props_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: self.ic_one,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, no props, default, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, no props, default, pose1 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, no props, default, pose2 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, no props, default, pose3 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, no props, default, pose4 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, no props, default, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, no props, default, pose6 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, no props, default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, no props, default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_4_no_props_invalid_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: 10,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, invalid default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 4, no props, invalid default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_4_no_props_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_l_default: self.ic_zero,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, no props, l_default, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, no props, l_default, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, no props, l_default, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, no props, l_default, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, no props, l_default, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, no props, l_default, pose5 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, no props, l_default, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, no props, l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, no props, l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_4_no_props_invalid_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_l_default: 10,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, invalid l_default, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 4, no props, invalid l_default, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_4_no_props_default_urfl(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: self.ic_one,
                self.prop_urfl: True
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, default, urfl, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, no props, default, urfl, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, no props, default, urfl, pose1 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, no props, default, urfl, pose2 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, no props, default, urfl, pose3 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, no props, default, urfl, pose4 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, no props, default, urfl, pose5 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, no props, default, urfl, pose6 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, no props, default, urfl, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, no props, default, urfl, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_4_no_props_default_l_default(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: self.ic_one,
                self.prop_l_default: self.ic_zero,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, no props, default, l_default, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, no props, default, l_default, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, no props, default, l_default, pose1 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, no props, default, l_default, pose2 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, no props, default, l_default, pose3 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, no props, default, l_default, pose4 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, no props, default, l_default, pose5 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, no props, default, l_default, pose6 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, no props, default, l_default, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, no props, default, l_default, log length should be 1"):
                self.assertEqual(0, len(log))

        def test_mpm_type_4_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                "extra": 123,
                "extra2": 69
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, extra props, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, extra props, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, extra props, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, extra props, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, extra props, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, extra props, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, extra props, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, extra props, log length should be 4"):
                self.assertEqual(4, len(log))

        def test_mpm_type_4_valid_1_2_5(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_p1: self.ic_one,
                self.prop_p2: self.ic_zero,
                self.prop_p5: self.ic_custom,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, valid 1 2 5, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, valid 1 2 5, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, valid 1 2 5, pose1 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, valid 1 2 5, pose2 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, valid 1 2 5, pose3 should be none"):
                self.assertIsNone(actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, valid 1 2 5, pose4 should be none"):
                self.assertIsNone(actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, valid 1 2 5, pose5 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, valid 1 2 5, pose6 should be none"):
                self.assertIsNone(actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, valid 1 2 5, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, valid 1 2 5, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_4_valid_3_4_6(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_p3: self.ic_custom,
                self.prop_p4: self.ic_one,
                self.prop_p6: self.ic_zero,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, valid 3 4 6, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, valid 3 4 6, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, valid 3 4 6, pose1 should be none"):
                self.assertIsNone(actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, valid 3 4 6, pose2 should be none"):
                self.assertIsNone(actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, valid 3 4 6, pose3 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, valid 3 4 6, pose4 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, valid 3 4 6, pose5 should be none"):
                self.assertIsNone(actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, valid 3 4 6, pose6 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, valid 3 4 6, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, valid 3 4 6, log length should be 2"):
                self.assertEqual(2, len(log))

        def test_mpm_type_4_valid_all_no_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_p1: self.ic_one,
                self.prop_p2: self.ic_custom,
                self.prop_p3: self.ic_zero,
                self.prop_p4: self.ic_zero,
                self.prop_p5: self.ic_one,
                self.prop_p6: self.ic_custom,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, valid all, no defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, valid all, no defaults, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, valid all, no defaults, pose1 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, valid all, no defaults, pose2 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, valid all, no defaults, pose3 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, valid all, no defaults, pose4 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, valid all, no defaults, pose5 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, valid all, no defaults, pose6 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, valid all, no defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, valid all, no defaults, log length should be 0"):
                self.assertEqual(2, len(log))

        def test_mpm_type_4_valid_all_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: self.ic_one,
                self.prop_l_default: self.ic_zero,
                self.prop_p1: self.ic_custom,
                self.prop_p2: self.ic_custom,
                self.prop_p3: self.ic_custom,
                self.prop_p4: self.ic_one,
                self.prop_p5: self.ic_one,
                self.prop_p6: self.ic_zero,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, valid all, defaults, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, valid all, defaults, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, valid all, defaults, pose1 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, valid all, defaults, pose2 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, valid all, defaults, pose3 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, valid all, defaults, pose4 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, valid all, defaults, pose5 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, valid all, defaults, pose6 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, valid all, defaults, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, valid all, defaults, log length should be 0"):
                self.assertEqual(0, len(log))

        def test_mpm_type_4_one_invalid_defaults(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: self.ic_one,
                self.prop_l_default: self.ic_zero,
                self.prop_p1: self.ic_custom,
                self.prop_p2: self.ic_custom,
                self.prop_p3: 10,
                self.prop_p4: self.ic_custom,
                self.prop_p5: self.ic_one,
                self.prop_p6: self.ic_zero,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, one invalid defaults, should be none"):
                self.assertIsNone(actual)

            with self.subTest("mpm type 4, one invalid defaults, log length should be 1"):
                self.assertEqual(1, len(log))

        def test_mpm_type_4_valid_all_defaults_extra_props(self):
            test_data = {
                self.prop_mpm_type: store.MASPoseMap.MPM_TYPE_IC,
                self.prop_default: self.ic_one,
                self.prop_l_default: self.ic_zero,
                self.prop_p1: self.ic_custom,
                self.prop_p2: self.ic_custom,
                self.prop_p3: self.ic_custom,
                self.prop_p4: self.ic_one,
                self.prop_p5: self.ic_one,
                self.prop_p6: self.ic_zero,
                "extra": 123,
                "extra2": 69,
            }
            log = []
            actual = store.MASPoseMap.fromJSON(test_data, log, 0)

            with self.subTest("mpm type 4, valid all, defaults, extra props, should not be none"):
                self.assertIsNotNone(actual)

            with self.subTest("mpm type 4, valid all, defaults, extra props, mpm type should be MPM_TYPE_IC"):
                self.assertEqual(store.MASPoseMap.MPM_TYPE_IC, actual._mpm_type)

            with self.subTest("mpm type 4, valid all, defaults, extra props, pose1 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose1, "test"))

            with self.subTest("mpm type 4, valid all, defaults, extra props, pose2 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose2, "test"))

            with self.subTest("mpm type 4, valid all, defaults, extra props, pose3 should be the same as ic_custom"):
                self.assertEqual(self.ic_custom, actual.get(self.pose3, "test"))

            with self.subTest("mpm type 4, valid all, defaults, extra props, pose4 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose4, "test"))

            with self.subTest("mpm type 4, valid all, defaults, extra props, pose5 should be the same as ic_one"):
                self.assertEqual(self.ic_one, actual.get(self.pose5, "test"))

            with self.subTest("mpm type 4, valid all, defaults, extra props, pose6 should be the same as ic_zero"):
                self.assertEqual(self.ic_zero, actual.get(self.pose6, "test"))

            with self.subTest("mpm type 4, valid all, defaults, extra props, test_data should be empty dict"):
                self.assertEqual({}, test_data)

            with self.subTest("mpm type 4, valid all, defaults, extra props, log length should be 2"):
                self.assertEqual(2, len(log))
