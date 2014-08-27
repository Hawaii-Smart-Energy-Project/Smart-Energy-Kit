#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'


import sys
import psycopg2
from sek.logger import SEKLogger

DEBUG = 1


class SEKDBUtil(object):
    """
    Utility methods.

    This is the class responsible for actions against databases such as as
    executing SQL statements.

    The database is specified by the database connection.

    DB connections and cursors are passed in as arguments.

    Usage:

        dbUtil = SEKDBUtil()

    Public API:

        executeSQL(cursor: DB cursor, sql: String, exitOnFail: Boolean):Boolean

    """

    def __init__(self):
        """
        Constructor.
        """

        self.logger = SEKLogger(__name__, 'DEBUG')


    def getLastSequenceID(self, conn, tableName, columnName):
        """
        Get last sequence ID value for the given sequence and for the
        given connection.

        :param conn: DB connection
        :param tableName: String for name of the table that the sequence matches
        :param columnName: String for name of the column to which the
        sequence is applied
        :returns: Integer of last sequence value or None if not found.
        """

        if DEBUG:
            print "table name = %s" % tableName
            print "column name = %s" % columnName

        sql = """SELECT currval(pg_get_serial_sequence('"{}"','{}'))""".format(
            tableName, columnName)

        cur = conn.cursor()
        self.executeSQL(cur, sql)

        try:
            row = cur.fetchone()
        except psycopg2.ProgrammingError, e:
            msg = "Failed to retrieve the last sequence value."
            msg += " Exception is %s." % e
            self.logger.log(msg, 'error')
            sys.exit(-1)

        lastSequenceValue = row[0]

        if lastSequenceValue is None:
            raise Exception("Critical error. Last sequence value could not be retrieved.")

        return lastSequenceValue


    def executeSQL(self, cursor, sql, exitOnFail = True):
        """
        Execute SQL given a cursor and a SQL statement.

        The cursor is passed here to allow control of committing outside of
        this class.

        exitOnFail can be toggled to handle cases such as continuing with an
        insert even when duplicate keys are encountered.

        The result rows of a query are accessible through the cursor that is
        passed in. For example:

        rows = cursor.fetchall()

        :param cursor: DB cursor.
        :param sql: String of a SQL statement.
        :returns: Boolean True for success, execution is aborted if there is
        an error.
        """

        success = True
        try:
            cursor.execute(sql)

        except Exception as detail:
            success = False
            msg = "SQL execute failed using {}.".format(sql)
            msg += " The error is: {}.".format(detail)

            self.logger.log(msg, 'error')
            if exitOnFail:
                sys.exit(-1)

        return success


    def getDBName(self, cursor):
        """
        :returns: Name of the current database.
        """

        self.executeSQL(cursor, """select current_database();""")
        row = cursor.fetchone()
        return row


    def tableColumns(self, cursor, table):
        """
        Access column names as a tuple with the names being at index 0.

        :param: cursor: A DB cursor
        :param: table: Name of table to retrieve columns from.
        :returns: List of tuples with column names in the first position.
        """

        sql = """SELECT column_name FROM information_schema.columns WHERE
        table_name='%s';""" % table
        self.executeSQL(cursor, sql)

        return cursor.fetchall()  # Each column is an n-tuple.

    def columns(self, cursor = None, table = None):
        """
        Return column names for a given table.

        :param cursor:
        :param table:
        :return: List of columns.
        """

        if not cursor:
            raise Exception('Cursor not defined.')
        if not table:
            raise Exception('Table not defined.')

        cols = []
        for col in self.tableColumns(cursor, table):
            cols.append(col[0])
        return cols


    def columnsString(self, cursor = None, table = None):
        if not cursor:
            raise Exception('Cursor not defined.')
        if not table:
            raise Exception('Table not defined.')
        return ','.join(item for item in self.columns(cursor, table))
