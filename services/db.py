#!/usr/local/bin/python3.5

import os
import sqlite3
from pathlib import Path


# TODO make as an intermediate manager instead
class DB:
    """DB class for handling DB operations."""
    DB_NAME = 'url_shortener.db'
    # per http://stackoverflow.com/a/30218825
    DIR_PATH = Path(__file__).resolve().parents[1]
    # / join of PosixPath per http://bugs.python.org/issue21798.
    # still must convert to string for DB connection string use.
    DB_PATH = str(DIR_PATH / DB_NAME)


    def __init__(self):
        """Initialize DB connection and assign cursor."""
        self.conn = self.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()


    def __enter__(self):
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        self.conn.commit()
        self.conn.close()


    def __del__(self):
        self.conn.close()


    def connect(self, db_name):
        """Connect to the DB with settings."""
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn


    def query(self, sql, params=()):
        """Return specific result in a dictionary."""
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()


    def query_all(self, sql, params=()):
        """Return specific result in a dictionary."""
        print(sql, params)
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()


    def insert(self, sql, params=()):
        """Return specific result in a dictionary."""
        self.cursor.execute(sql, params)

        # TODO: replace this with more correct solution
        # get last ID entered because self.cursor.lastrowid is not working
        res = self.cursor.execute('SELECT MAX(id) FROM url')
        max_id = res.fetchone()[0]
        # print('--->>>', sql, params, self.cursor.lastrowid, max_id)

        return max_id


    def update(self, sql, params=()):
        """Return specific result in a dictionary."""
        self.cursor.execute(sql, params)
        affected = self.cursor.rowcount
        return affected
