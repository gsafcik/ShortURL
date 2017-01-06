#!/usr/local/bin/python3.5

import sqlite3

from services import DB


# TODO make as an intermediate manager instead
class DBSetup:
    """Setup Database."""


    @staticmethod
    def setup_database():
        """Create the DB table.

        "Prep SQL" used here because answers on SO from 7 years ago no longer work.
         -  SQL: UPDATE SQLITE_SEQUENCE SET SEQ=1000 WHERE NAME='url' per
            http://stackoverflow.com/a/692871 does NOT work.
         - WORK AROUND: Manually INSERTING at wanted_ID - 1 works but it's ugly. Can not DELETE it and
                        still have SQLite3 remember last ID so it remains.
         - TODO: use a more official method if available.
                 use DB class.
        """
        with sqlite3.connect(DB.DB_PATH) as conn:
            sql_prep_0 = """
                DROP TABLE IF EXISTS url
            """
            sql = """
                CREATE TABLE IF NOT EXISTS url (
                    id INTEGER PRIMARY KEY NOT NULL,
                    original_url TEXT,
                    short_url TEXT,
                    created dateTIME DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))
                )
            """
            sql_prep = """
                INSERT INTO url (id, original_url, short_url) VALUES (999, '', '')
            """
            # conn.execute(sql_prep_0)  # TESTING ONLY
            conn.execute(sql)
            # TODO add test for this otherwise UNIQUE contraint error will be raised
            # conn.execute(sql_prep)  # so ugly