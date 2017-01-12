import html

from services import DB


class ShortURLBase(object):
    """Base for shared functionality of URL shortening services."""

    ALPHABET = str('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    BASE = len(ALPHABET)
    SHORT_URL_BASE = 'http://52.8.43.12'

    STATUS_OK = 'OK'
    STATUS_ERROR = 'ERROR'
    STATUS_MODIFIED = 'MODIFIED'


    def escape_url(self, url):
        """Don't trust the URL."""
        status = dict()
        escaped_url = html.escape(url)
        if escaped_url is not url:
            status = dict(status=self.STATUS_MODIFIED)
        return escaped_url, status


    def get_data_by_id(self, db_id):
        """Retrieve data by Database ID."""
        columns_str = 'original_url, short_url, created'
        sql = """
            SELECT {}
              FROM url
             WHERE id = ?
        """.format(columns_str)
        params = (db_id,)
        with DB() as db:
            data = db.fetch(sql, params)

        return data
