#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'

import unittest


class DBConnectorTester(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    RUN_SELECTED_TESTS = True

    if RUN_SELECTED_TESTS:

        tests = []

        # For testing:
        # selected_tests = []

        mySuite = unittest.TestSuite()
        for t in tests:
            mySuite.addTest(DBConnectorTester(t))
        unittest.TextTestRunner().run(mySuite)
    else:
        unittest.main()
