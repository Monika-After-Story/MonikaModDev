python early in mas_unittests:
    import store
    import sys
    import unittest

    test_suite = unittest.TestSuite()
    _loader = unittest.TestLoader()
    _runner = unittest.TextTestRunner()

    def run_tests():
        result = _runner.run(test_suite)

        if not result.wasSuccessful():
            raise Exception("Unit tests failed.")
            # Ensure a non-zero exit code because lint hook failures don't cause lint to error.
            sys.exit(1)

    def testclass(cls):
        test_suite.addTest(_loader.loadTestsFromTestCase(cls))
        return cls

init 1000 python in mas_unittests:
    renpy.config.lint_hooks.append(run_tests)
