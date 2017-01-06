#!/usr/local/bin/python3.5

import json
import re

from urllib.parse import urlparse, urljoin

from services import DB


class URLShortener:
    # BASE 62

    alphabet = str('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    base = len(alphabet)
    SHORT_URL_BASE = 'http://shortu.rl'


    def convert_short_url_to_original_url(self, short_url):
        """[GET] Takes a short url and gets original url.

        Algorithm:
        1. Take short URL
        2. Convert short URL to DB ID
        3. Do a lookup in DB by ID
        4. Return JSON encoded data (see `columns_str` in `get_data_by_id()`)
        """
        url_parts_obj = urlparse(short_url)
        short_path = url_parts_obj.path
        db_id = self.convert_short_url_to_id(short_path)

        data = dict(self.get_data_by_id(db_id))

        return json.dumps(data)


    def convert_original_url_to_short_url(self, original_url):
        """[POST] Takes a original url and makes it a short url.

        Algorithm:
        1. Take original URL, insert original URL into DB, return ID
        2. Convert ID to short url
        3. Return JSON encoded data (see `columns_str` in `get_data_by_id()`)
        """
        db_id = self.insert_orig_url_into_db(original_url)
        short_url = self.convert_id_to_short_url(db_id)
        affected = self.insert_short_url_into_db(short_url, original_url, db_id)

        data = dict(self.get_data_by_id(db_id))

        return json.dumps(data)


    def get_data_by_id(self, db_id):
        """Retrieve data by Database ID."""
        columns_str = 'original_url, short_url, created'
        sql = """
            SELECT {}
              FROM url
             WHERE id = ?  -- to be sure
        """.format(columns_str)
        params = (db_id,)
        with DB() as db:
            data = db.query(sql, params)

        return data


    def insert_short_url_into_db(self, short_url, original_url, db_id):
        """Returns DB ID."""
        sql = """
            UPDATE url
               SET short_url = ?
             WHERE original_url = ?
               AND id = ?  -- to be sure
        """

        # sql_check = """
        #     SELECT * FROM url ORDER BY id DESC
        # """
        params = (short_url, original_url, db_id)
        with DB() as db:
            affected = db.update(sql, params)
            # print('affected:', affected)
            # print('>>>>>>', db.query_all(sql_check))

        return affected


    def insert_orig_url_into_db(self, original_url):
        """Returns DB ID."""
        sql = """
            INSERT INTO url (original_url)
                 VALUES (?)
        """
        params = (original_url,)
        with DB() as db:
            db_id = db.insert(sql, params)

        return db_id


    def convert_id_to_short_url(self, db_id):
        """Convert database ID (pk) to shortened url string.
        
        Returns str().
        """
        short_url = ''
        while db_id > 0:
            short_url = self.alphabet[db_id % self.base] + short_url
            db_id = db_id // self.base  # floor div
        return urljoin(self.SHORT_URL_BASE, short_url)

    def convert_short_url_to_id(self, short_path):
        """Convert short url string to database ID (pk).

        Returns int().
        """
        delimeter, short_url = re.split('(/)', short_path)[1:]

        db_id = 0
        for char in short_url:
            db_id = (db_id * self.base) + self.alphabet.index(char)
        return db_id
