import sqlite3

from services import DB


class SQLite3DBSetup(object):
    """Setup Initial Database Schema."""

    @staticmethod
    def setup_database():
        """Create the SQLite3DB table."""
        with sqlite3.connect(DB.DB_PATH) as conn:
            sql = """
                CREATE TABLE IF NOT EXISTS url (
                    id INTEGER PRIMARY KEY NOT NULL,
                    original_url TEXT,
                    short_url TEXT,
                    created dateTIME DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW'))
                )
            """
            conn.execute(sql)
