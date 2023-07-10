init 1 python in mas_unittests:
    import datetime
    from unittest.mock import create_autospec

    @testclass
    class TestStrictCanPickle(unittest.TestCase):
        can_pickle = (True, False)
        cannot_pickle = (False, False)
        recur_error = (False, True)

        good_iter_data = [1, 2, True, "test"]
        bad_iter_data = [1, 2, True, object(), "test"]

        good_dict_data = { 1: 2, True: "test" }
        bad_dict_data_key = { 1: 2, object(): True, "test": 100 }
        bad_dict_data_val = { 1: 2, True: object(), "test": 100}

        recur_dict = {}
        recur_list = [ recur_dict ]
        recur_dict[10] = recur_list

        class FakeTzInfo(datetime.tzinfo):
            def utcoffset(self, dt):
                return datetime.timedelta()

            def dst(self, dt):
                return datetime.timedelta()

            def tzname(self, dt):
                return "Fake/Timezone"

        # none check
        def test_none_check(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle(None)
            )

        # non-structure types
        def test_strings_check(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle("test")
            )

        def test_bool_check(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle(bool(1))
            )

        def test_numbers_check(self):
            with self.subTest("numbers check: int"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(int(1))
                )

            with self.subTest("numbers check: float"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(float(1))
                )

            with self.subTest("numbers check: complex"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(complex(1))
                )

        def test_date_timedelta_check(self):
            with self.subTest("date timedelta check: timedelta"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(datetime.timedelta())
                )

            with self.subTest("date timedelta check: date"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(datetime.date.today())
                )

        # datetime special
        def test_datetime_time_no_tzinfo(self):
            with self.subTest("datetime, time - no tzinfo: datetime"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(datetime.datetime.utcnow())
                )

            with self.subTest("datetime, time - no tzinfo: time"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(datetime.time())
                )

        def test_datetime_time_with_tzinfo(self):
            with self.subTest("datetime, time - with tzinfo: datetime"):
                self.assertEqual(
                    self.cannot_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(datetime.datetime.now(self.FakeTzInfo()))
                )

                self.assertEqual(
                    self.cannot_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(datetime.time(tzinfo=self.FakeTzInfo()))
                )

        # lists
        def test_lists_empty(self):
            with self.subTest("list - empty: builtin"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(
                        store.mas_ev_data_ver.builtins.list()
                    )
                )

            with self.subTest("list - empty: RevertableList via list()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(list())
                )

            with self.subTest("list - empty: RevertableList via []"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle([])
                )

            with self.subTest("list - empty: RevertableList via RevertableList()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(renpy.python.RevertableList())
                )

        def test_list_with_good_values(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle(self.good_iter_data)
            )

        def test_list_with_bad_values(self):
            self.assertEqual(
                self.cannot_pickle,
                store.mas_ev_data_ver._strict_can_pickle(self.bad_iter_data)
            )

        def test_list_recursion(self):
            self.assertEqual(
                self.recur_error,
                store.mas_ev_data_ver._strict_can_pickle(self.recur_list)
            )

        # sets
        def test_sets_empty(self):
            with self.subTest("sets - empty: builtin"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(
                        store.mas_ev_data_ver.builtins.set()
                    )
                )

            with self.subTest("sets - empty: builtin frozenset"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(
                        store.mas_ev_data_ver.builtins.frozenset()
                    )
                )

            with self.subTest("sets - empty: set()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(set())
                )

            with self.subTest("sets - empty: frozenset()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(frozenset())
                )

            with self.subTest("sets - empty: RevertableSet()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(renpy.python.RevertableSet())
                )

        def test_sets_with_good_values(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle(set(self.good_iter_data))
            )

        def test_sets_with_bad_values(self):
            self.assertEqual(
                self.cannot_pickle,
                store.mas_ev_data_ver._strict_can_pickle(set(self.bad_iter_data))
            )

        # tuple
        def test_tuple_with_good_values(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle(tuple(self.good_iter_data))
            )

        def test_tuple_with_bad_values(self):
            self.assertEqual(
                self.cannot_pickle,
                store.mas_ev_data_ver._strict_can_pickle(tuple(self.bad_iter_data))
            )

        # dicts
        def test_dict_empty(self):
            with self.subTest("dict - empty: builtin"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(
                        store.mas_ev_data_ver.builtins.dict()
                    )
                )

            with self.subTest("dict - empty: {}"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle({})
                )

            with self.subTest("dict - empty: dict()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(dict())
                )

            with self.subTest("dict - empty: RevertableDict()"):
                self.assertEqual(
                    self.can_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(renpy.python.RevertableDict())
                )

        def test_dict_with_good_values(self):
            self.assertEqual(
                self.can_pickle,
                store.mas_ev_data_ver._strict_can_pickle(self.good_dict_data)
            )

        def test_dict_with_bad_values(self):
            with self.subTest("dict - bad values: key"):
                self.assertEqual(
                    self.cannot_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(self.bad_dict_data_key)
                )

            with self.subTest("dict - bad values: value"):
                self.assertEqual(
                    self.cannot_pickle,
                    store.mas_ev_data_ver._strict_can_pickle(self.bad_dict_data_val)
                )

        def test_dict_recursion(self):
            self.assertEqual(
                self.recur_error,
                store.mas_ev_data_ver._strict_can_pickle(self.recur_dict)
            )
