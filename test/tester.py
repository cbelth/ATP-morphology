import unittest
from test_utils import TestUtils
from test_tp_switch_statement import TestTPSwitchStatement
from test_phon_engine import TestPhonEngine
from test_atp import TestATP

'''
A script to run all the test cases.
'''
# load test suites
test_utils_suite = unittest.TestLoader().loadTestsFromTestCase(TestUtils)
test_tp_switch_statement_suite = unittest.TestLoader().loadTestsFromTestCase(TestTPSwitchStatement)
test_phon_engine_suite = unittest.TestLoader().loadTestsFromTestCase(TestPhonEngine)
test_atp_suite = unittest.TestLoader().loadTestsFromTestCase(TestATP)
# combine the test suites
suites = unittest.TestSuite([test_utils_suite,
                             test_tp_switch_statement_suite,
                             test_phon_engine_suite,
                             test_atp_suite])
# run the test suites
unittest.TextTestRunner(verbosity=2).run(suites)
