#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.github.com/Hawaii-Smart-Energy-Project/Smart' \
              '-Energy-Kit/master/BSD-LICENSE.txt'

import smtplib
from datetime import datetime
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import Encoders

from sek_logger import SEKLogger


class SEKNotifier(object):
    """
    Provides notification service functionality for MSG data processing.

    Email settings are stored in the local configuration.

    Constructor Parameters:
    connector
    dbUtil
    user
    password
    fromaddr
    toaddr
    testing_toaddr
    smtp_server_and_port

    @todo document usage with new params

    Usage:

    from msg_notifier import MSGNotifier
    self.notifier = MSGNotifier()

    Public API:

    sendNotificationEmail(msgBody, testing = False):
        Send msgBody as a notification to the mailing list defined in the
        config file.

    sendMailWithAttachments(msgBody, files = None, testing = False)
        Send msgBody with files attached as a notification to the mailing
        list defined in the config file.
    """

    def __init__(self, connector = None, dbUtil = None, user = '',
                 password = '', fromaddr = '', toaddr = '', testing_toaddr = '',
                 smtp_server_and_port = ''):
        """
        Constructor.
        """
        # @todo Validate params.

        self.user = user
        self.password = password
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.testing_toaddr = testing_toaddr
        self.smtp_server_and_port = smtp_server_and_port
        self.logger = SEKLogger(__name__, 'info')
        self.connector = connector
        self.conn = self.connector.connectDB()
        self.cursor = self.conn.cursor()
        self.dbUtil = dbUtil
        self.noticeTable = 'NotificationHistory'
        self.notificationHeader = "This is a message from the Hawaii Smart " \
                                  "Energy Project MSG Project notification " \
                                  "system.\n\n"

        self.noReplyNotice = """\n\nThis email account is not monitored. No
        replies will originate from this account.\n\nYou are receiving this
        message because you are on the recipient list for notifications for
        the Hawaii Smart Energy Project."""


    def sendNotificationEmail(self, msgBody = '', testing = False):
        """
        This is for sending simple messages versus sending multipart messages
        with attachments.

        :param msgBody: The body of the message to be sent.
        :param testing: True if running in testing mode.
        :returns: True for success, False for an error.
        """

        errorOccurred = False

        toaddr = ''
        if testing:
            toaddr = self.testing_toaddr
        else:
            toaddr = self.toaddr

        server = smtplib.SMTP(self.smtp_server_and_port)

        try:
            server.starttls()
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP STARTTLS: {}".format(detail),
                            'ERROR')

        try:
            server.login(self.user, self.password)
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP login: %s" % detail, 'ERROR')

        senddate = datetime.now().strftime('%Y-%m-%d')
        subject = "HISEP Notification"

        msgHeader = "Date: {}\r\nFrom: {}\r\nTo: {}\r\nSubject: {" \
                    "}\r\nX-Mailer: My-Mail\r\n\r\n".format(senddate,
                                                            self.fromaddr,
                                                            toaddr, subject)

        msgBody = self.notificationHeader + msgBody

        msgBody += self.noReplyNotice

        try:
            self.logger.log("Send email notification.", 'INFO')
            server.sendmail(self.fromaddr, self.toaddr, msgHeader + msgBody)
            server.quit()
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP sendmail: {}".format(detail),
                            'ERROR')

        return errorOccurred != True


    def sendMailWithAttachments(self, msgBody, files = None, testing = False):
        """
        Send email along with attachments.

        :param msgBody: String containing the body of the messsage to send.
        :param files: List of file paths. This is a mutable argument that
        should be handled carefully as the default is defined only once.
        :param testing: True if running in testing mode.
        :returns: True if no exceptions are raised.
        """

        if files is None:
            files = []

        sys.stderr.write("Sending multipart email.\n")
        if testing:
            self.logger.log("Notification testing mode is ON.\n", 'info')

        errorOccurred = False
        assert type(files) == list

        send_to = ''
        if testing:
            send_to = self.testing_toaddr
        else:
            send_to = self.toaddr

        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = send_to
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = "HISEP Notification"

        msg.attach(MIMEText(msgBody))

        for f in files:
            sys.stderr.write("Attaching file %s.\n" % f)
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(f, "rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        server = smtplib.SMTP(self.smtp_server_and_port)

        try:
            server.starttls()
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP STARTTLS: %s" % detail,
                            'ERROR')

        try:
            server.login(self.user, self.password)
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP login: %s" % detail, 'ERROR')

        self.logger.log("Send email notification.", 'INFO')

        try:
            server.sendmail(self.fromaddr, send_to, msg.as_string())
        except smtplib.SMTPException as detail:
            errorOccurred = True
            self.logger.log("Exception during SMTP sendmail: %s" % detail,
                            'ERROR')

        server.quit()

        if errorOccurred == False:
            self.logger.log('No exceptions occurred.\n', 'info')

        return errorOccurred


    def recordNotificationEvent(self, noticeType = ''):
        """
        Save a notification event to the notification history.
        :param table: String
        :param noticeType: String
        :returns: Boolean
        """

        cursor = self.cursor
        sql = """INSERT INTO "{}" ("notificationType", "notificationTime")
        VALUES ('{}', NOW())""".format(self.noticeTable, noticeType)
        success = self.dbUtil.executeSQL(cursor, sql)
        self.conn.commit()
        if not success:
            raise Exception('Exception while saving the notification time.')
        return success
