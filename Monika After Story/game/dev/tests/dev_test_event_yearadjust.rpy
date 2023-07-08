init python in mas_unittests:
    @testclass
    class TestEventYearadjust(unittest.TestCase):
        @staticmethod
        def add_years(in_dt, diff):
            return store.mas_utils.add_years(in_dt, diff)

        def test_is_current(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt - datetime.timedelta(days=1)
            end_dt = now_dt + datetime.timedelta(days=1)
            expected = (start_dt, end_dt, False)
            actual = store.Event._yearAdjust(start_dt, end_dt, [])

            self.assertEqual(expected, actual)

        def test_is_current_same_as_start(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt
            end_dt = now_dt + datetime.timedelta(days=1)
            expected = (start_dt, end_dt, False)
            actual = store.Event._yearAdjust(start_dt, end_dt, [])

            self.assertEqual(expected, actual)

        def test_is_current_no_years_forced(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt - datetime.timedelta(days=1)
            end_dt = now_dt + datetime.timedelta(days=1)
            expected = (
                self.add_years(start_dt, 1),
                self.add_years(end_dt, 1),
                True
            )
            actual = store.Event._yearAdjust(start_dt, end_dt, [], force=True)

            self.assertEqual(expected, actual)

        def test_before_now_same_year(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt - datetime.timedelta(days=10)
            end_dt = now_dt - datetime.timedelta(days=5)
            expected = (
                self.add_years(start_dt, 1),
                self.add_years(end_dt, 1),
                True
            )
            actual = store.Event._yearAdjust(start_dt, end_dt, [])

            self.assertEqual(expected, actual)

        def test_before_now_diff_year(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt - datetime.timedelta(days=400)
            end_dt = now_dt - datetime.timedelta(days=380)
            expected = (
                self.add_years(start_dt, 2),
                self.add_years(end_dt, 2),
                True
            )
            actual = store.Event._yearAdjust(start_dt, end_dt, [])

            self.assertEqual(expected, actual)

        def test_ahead_now_same_year(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt + datetime.timedelta(days=5)
            end_dt = now_dt + datetime.timedelta(days=10)
            expected = (start_dt, end_dt, False)
            actual = store.Event._yearAdjust(start_dt, end_dt, [])

            self.assertEqual(expected, actual)

        def test_ahead_now_diff_year(self):
            import datetime

            now_dt = datetime.datetime.now()
            start_dt = now_dt + datetime.timedelta(days=380)
            end_dt = now_dt + datetime.timedelta(days=400)
            expected = (
                self.add_years(start_dt, -1),
                self.add_years(end_dt, -1),
                True
            )
            actual = store.Event._yearAdjust(start_dt, end_dt, [])

            self.assertEqual(expected, actual)
