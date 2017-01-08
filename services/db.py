import sqlite3
from pathlib import Path


class DB:
    """Database class for handling operations.

    TODO use SQLAlchemy or similar.
    """

    DB_NAME = 'url_shortener.db'
    DIR_PATH = Path(__file__).resolve().parents[1]  # per http://stackoverflow.com/a/30218825
    # "/" join of PosixPath per http://bugs.python.org/issue21798.
    # still must convert to string for DB connection string use.
    DB_PATH = str(DIR_PATH / DB_NAME)


    def __init__(self):
        """Initialize database connection and assign cursor."""
        self.conn = self.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()


    def __enter__(self):
        """Enter needed to make this a context manager."""
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        """Exit needed to make this a context manager."""
        if exception_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


    def __del__(self):
        """Make sure the connection is closed on cleanup."""
        self.conn.close()


    def connect(self, db_name):
        """Connect to the database and set row factory setting to return object instead of tuple.

        This changing of `row_factory` is for the ability to convert the result to dictionary
        easily. This was the best way I could find in SQLite3 which compared to MySQL's DictCursor.
        """
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn


    def fetch(self, sql, params=()):
        """Get specific result in a dictionary.
        
        Typically used for SELECT statements.
        RETURN: fetched data (single row).
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()


    def insert(self, sql, params=()):
        """Insert specific rows into the database.

        Typically used for INSERT statements.
        RETURN: last inserted (largest) ID.
        """
        self.cursor.execute(sql, params)

        # TODO: replace this with more correct solution
        # get last ID entered because self.cursor.lastrowid is not working
        res = self.cursor.execute('SELECT MAX(id) FROM url')
        max_id = res.fetchone()[0]

        return max_id


    def update(self, sql, params=()):
        """Update specific rows in the database.

        Typically used for UPDATE statements.
        RETURN: affected row count.
        """
        self.cursor.execute(sql, params)
        affected = self.cursor.rowcount
        return affected
