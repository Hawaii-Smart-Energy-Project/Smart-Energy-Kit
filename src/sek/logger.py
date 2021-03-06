#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides logging services for projects of the Hawaii Smart Energy Project.

Setting self.shouldRecord=True provides a way of collecting all logging output
for the instantiated logger into self.recording.

Usage:

from sek_logger import SEKLogger
self.logger = SEKLogger(__name__)

The logger level is configurable by passing a predefined logging level.

    self.logger = SEKLogger(__name__, '${LOGGING_LEVEL}')

The name parameter is used to pass the calling class. The optional logging level
level corresponds to the levels used in the logging module. It is useful for
filtering logging output. For example, if the logger is instantiated using

    self.logger = SEKLogger(__name__, 'INFO')

then debugging level logging statements such as

    self.logger.log('A debug message.', 'DEBUG')

will not be printed.

Important Note:
The logging level is individually configured for each class where it is
instantiated. Getting the desired output requires setting the level within
each instance.

Public API:

log(message:String, level:String)
    Output a logging message at the specified logging level.

startRecoring()
    Starting recording of log messages to self.recording.

endRecording()
    End recording of log messages.

"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart' \
              '-Energy-Kit/master/BSD-LICENSE.txt'

import sys
import logging
from io import StringIO
from colorlog import ColoredFormatter

CRITICAL = logging.CRITICAL
DEBUG = logging.DEBUG
ERROR = logging.ERROR
INFO = logging.INFO
SILENT = logging.NOTSET
WARNING = logging.WARNING

class SEKLogger(object):
    """
    This class provides logging functionality.

    It supports recording of log output by setting self.shouldRecord = True.
    The recorded output is then available in self.recording.

    Logging levels correspond to those in the logging module.

    Levels can also be set using the following strings:
    info, warning, error, silent, debug, critical

    Usage:
    from sek.logger import SEKLogger, CRITICAL, ERROR, WARNING, INFO, DEBUG, SILENT
    logger = SEKLogger(__name__, [${LOGGER_LEVEL}])

    where the logger level is optional.
    """

    def __init__(self, caller, level = INFO, useColor = True):
        """
        Constructor.

        :param caller: Object that is calling this class.
        :param level: String for logger level in ('info', 'error', 'warning',
        'silent', 'debug', 'critical')
        :param useColor: Boolean if True, color output is used via colorlog.
        """

        self.logger = logging.getLogger(caller)

        self.ioStream = StringIO()

        self.streamHandlerStdErr = logging.StreamHandler(sys.stderr)
        self.streamHandlerString = logging.StreamHandler(self.ioStream)
        self.streamHandlerStdErr.setLevel(DEBUG)
        self.streamHandlerString.setLevel(DEBUG)

        formatterString = logging.Formatter(
            u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if not useColor:
            formatterStdErr = logging.Formatter(
                u'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            # Use colored output:
            formatterStdErr = ColoredFormatter(
                u'%(log_color)s%(asctime)s - %(name)s - %(bold)s%(levelname)s: '
                u'%(reset)s%(message)s', reset = True,
                log_colors = {'DEBUG': 'green', 'INFO': 'blue',
                              'WARNING': 'yellow', 'ERROR': 'red',
                              'CRITICAL': 'red', })

        self.streamHandlerStdErr.setFormatter(formatterStdErr)
        self.streamHandlerString.setFormatter(formatterString)

        self.loggerLevel = level

        # The log level that is set here provides the cut-off point for future
        # calls to log that are responsible for the actual log messages.

        # The log level here has a slightly different meaning than the log
        # level used in the call to self.logger.log().

        if type(level) == type(''):
            level = level.lower()

            # Support string based types:
            if level == 'info':
                self.loggerLevel = INFO
            elif level == 'warning':
                self.loggerLevel = WARNING
            elif level == 'error':
                self.loggerLevel = ERROR
            elif level == 'silent':
                self.loggerLevel = SILENT
            elif level == 'debug':
                self.loggerLevel = DEBUG
            elif level == 'critical':
                self.loggerLevel = CRITICAL
            else:
                pass

        # Messages equal to and above the logging level will be logged.

        # Setting the level here is essential to get output from the logger.
        self.logger.setLevel(self.loggerLevel)

        self.recordingBuffer = []
        self.recording = ''
        self.shouldRecord = False
        self.logCounter = 0


    def logAndWrite(self, message):
        """
        With a given string, write it to stderr and return its value for
        appending to a running log.

        Nothing is added to the message. Therefore, if linefeeds are desired
        they should be included explicitly.

        :param message: String message to be logged.
        :returns: String for the message.
        """

        sys.stderr.write(message)
        return message


    def log(self, message = '', level = INFO, color = None):
        """
        Write a log message.

        Logging levels are

        * critical
        * debug
        * error
        * info
        * silent
        * warning

        :param message: String for a message to be logged.
        :param level: String for an optional logging level.
        :param color: not supported yet.
        """

        self.logger.addHandler(self.streamHandlerStdErr)
        if self.shouldRecord:
            self.logger.addHandler(self.streamHandlerString)

        loggerLevel = level

        if type(level) == type(''):
            level = level.lower()

            if level == 'info':
                loggerLevel = INFO
            elif level == 'warning':
                loggerLevel = WARNING
            elif level == 'debug':
                loggerLevel = DEBUG
            elif level == 'error':
                loggerLevel = ERROR
            elif level == 'silent':
                loggerLevel = SILENT
            elif level == 'critical':
                loggerLevel = CRITICAL
            else:
                pass

        if loggerLevel != None:
            self.logger.log(loggerLevel, message)

            if self.shouldRecord:
                # The recording buffer is a cumulative copy of the logging
                # output. At each iteration, the buffer plus the new output is
                # appended to the list.
                self.recordingBuffer.append(
                    '{}'.format((self.ioStream.getvalue())))
                self.recording = self.recordingBuffer[-1]

            for handler in self.logger.handlers:
                # The flushes here apparently don't have any effect on the
                # logger.
                handler.flush()
                self.ioStream.flush()
                self.logger.removeHandler(handler)

            self.logCounter += 1
        else:
            raise Exception("Invalid logger level {}.".format(level))


    def startRecording(self):
        self.shouldRecord = True

    def endRecording(self):
        self.shouldRecord = False
