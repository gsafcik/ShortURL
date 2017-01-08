import re
import cherrypy
import sys
import sqlite3

from urllib.parse import urlparse

from services import DB, ShortURLBase


class ShortToURL(ShortURLBase):
    """Provides functionality for retrieving original URLs from short URLs."""

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

        try:
            db_id = self.convert_short_url_to_id(short_path)
        except ValueError:
            # if short_path is empty string, etc
            raise cherrypy.HTTPError(400, 'ERROR_MALFORMED_REQUEST')


        try:
            data = dict(self.get_data_by_id(db_id))
        except (sqlite3.Error, TypeError):
            raise cherrypy.HTTPError(404, 'ERROR_ORIGINAL_URL_NOT_FOUND')

        data.update(status)
        
        return data


    def convert_short_url_to_id(self, short_path):
        """Convert short url string to database ID (pk).

        Returns int().
        """
        delimeter, short_url = re.split('(/)', short_path)[1:]

        db_id = 0
        for char in short_url:
            db_id = (db_id * self.BASE) + self.ALPHABET.index(char)
        return db_id
