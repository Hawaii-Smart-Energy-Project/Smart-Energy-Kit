#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart' \
              '-Energy-Kit/master/BSD-LICENSE.txt'

import unittest

from sek_logger import SEKLogger


# @todo Replace strings with enumeration types.

import re


class SEKLoggerTester(unittest.TestCase):

    def setUp(self):
        self.logger = SEKLogger(__name__, level='DEBUG')
        print 'logger level: %s' % self.logger.loggerLevel

    def testInit(self):
        self.logger.log('Testing init.',level='info')

        self.assertIsNotNone(self.logger)

    def testLogRecording(self):
        self.logger.log('Testing log recording.','info')

        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, 'info')
        self.logger.endRecording()
        self.logger.log("This should not be logged.", 'info')

        result = re.search(msg, self.logger.recording).group(0)

        self.logger.log("recording result: %s" % self.logger.recording)

        self.assertEqual(result, msg)

    def testSilentLogging(self):
        return

        self.logger.log('Testing silent logging.','info')

        msg = "Recording test."

        self.logger.startRecording()
        self.logger.log(msg, 'silent')
        self.logger.endRecording()

        self.assertEqual(self.logger.recording, '')

    def testDebugLogging(self):
        self.logger.log('Testing debug logging','DEBUG')

    def testDoublingOfLoggingOutput(self):
        self.logger.log('This is a test of doubling of logger output at the beginning of a test.')


if __name__ == '__main__':
    unittest.main()
