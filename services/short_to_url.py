import re
import cherrypy
import sqlite3

from urllib.parse import urlparse

from services import ShortURLBase


class ShortToURL(ShortURLBase):
    """Provides functionality for retrieving original URLs from short URLs."""

    def get_new_id(self, short_path):
        """Get new database ID from converted short_url."""
        try:
            _, short_path = re.split('(/)', short_path.rstrip('/'))[1:]
            db_id = self.convert_short_url_to_id(short_path)
        except ValueError:
            raise cherrypy.HTTPError(400, 'ERROR_SHORT_URL_MALFORMED')

        return db_id


    def get_url_data(self, db_id):
        """Get URL data from database ID."""
        try:
            data = dict(self.get_data_by_id(db_id))
        except (sqlite3.Error, TypeError):
            raise cherrypy.HTTPError(404, 'ERROR_ORIGINAL_URL_NOT_FOUND')

        return data


    def convert_short_url_to_original_url(self, short_url):
        """Take a short url and retrieve the original url.

        Typically supports the GET Method.

        Algorithm:
        1. Take short URL
        2. Convert short URL to DB ID
        3. Do a lookup in DB by ID
        4. Return desired data
        """
        short_url, status = self.escape_url(short_url)
        url_parts_obj = urlparse(short_url)
        short_path = url_parts_obj.path
        db_id = self.get_new_id(short_path)
        data = self.get_url_data(db_id)

        # update data with status info
        data.update(status)

        return data


    def convert_short_url_to_id(self, short_path):
        """Convert short url string to database ID (pk).

        Returns int().
        """
        db_id = 0
        for char in short_path:
            db_id = (db_id * self.BASE) + self.ALPHABET.index(char)

        return db_id
