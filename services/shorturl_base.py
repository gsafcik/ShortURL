from services import DB


class ShortURLBase:
    """Base for shared functionality of URL shortening services."""

    ALPHABET = str('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    BASE = len(ALPHABET)
    SHORT_URL_BASE = 'http://shortu.rl'


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
