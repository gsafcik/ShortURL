import cherrypy
import sys
import sqlite3

from urllib.parse import urljoin

from services import DB, ShortURLBase


class URLToShort(ShortURLBase):
    """Provides functionality for shortening URLs from original URLs."""

    def convert_original_url_to_short_url(self, original_url):
        """Take an original url and make it a short url.

        Typically supports the POST Method.

        Algorithm:
        1. Take original URL, insert original URL into DB, return ID
        2. Convert ID to short url
        3. Return desired data
        """
        original_url, status = self.escape_url(original_url)
        try:
            db_id = self.insert_orig_url_into_db(original_url)
        except (sqlite3.Error, TypeError):
            raise cherrypy.HTTPError(400, 'ERROR_URL_DATA_NOT_PROCESSED')

        short_url = self.convert_id_to_short_url(db_id)

        try:
            self.insert_short_url_into_db(short_url, original_url, db_id)
            data = dict(self.get_data_by_id(db_id))
        except (sqlite3.Error, TypeError):
            raise cherrypy.HTTPError(404, 'ERROR_URL_DATA_NOT_FOUND')

        data.update(status)

        return data


    def insert_orig_url_into_db(self, original_url):
        """Return a DB ID."""
        sql = """
            INSERT INTO url (original_url)
                 VALUES (?)
        """
        params = (original_url,)
        with DB() as db:
            db_id = db.insert(sql, params)

        return db_id


    def insert_short_url_into_db(self, short_url, original_url, db_id):
        """Return a DB ID."""
        sql = """
            UPDATE url
               SET short_url = ?
             WHERE original_url = ?
               AND id = ?  -- to be sure
        """
        params = (short_url, original_url, db_id)
        with DB() as db:
            affected = db.update(sql, params)

        return affected


    def convert_id_to_short_url(self, db_id):
        """Convert database ID (pk) to shortened url string.

        Returns str().
        """
        short_url = ''
        while db_id > 0:
            short_url = self.ALPHABET[db_id % self.BASE] + short_url
            db_id = db_id // self.BASE  # floor div
        return urljoin(self.SHORT_URL_BASE, short_url)
