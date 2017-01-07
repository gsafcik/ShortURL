import json

from services import DB, URLToShort, ShortToURL


class ShortURL:
    """Provides functionality for shortening URLs and retrieving original URLs.

    URL shortening is based off IDs in the database, not just raw strings. Bijective functions
    (https://en.wikipedia.org/wiki/Bijection) and BASE 62 was chosen as the default after
    researching on Stack Overflow and Google.
    """

    def __init__(self):
        """Initialization instantiations."""
        self.short_to_url = ShortToURL()
        self.url_to_short = URLToShort()


    def short_to_original_json(self, short_url):
        """[GET] Takes a short url and retrieves the original url.

        Returns Dict() converted to JSON.
        """
        data = self.short_to_url.convert_short_url_to_original_url(short_url)

        return json.dumps(data)


    def original_to_short_json(self, original_url):
        """[POST] Takes a original url and makes it a short url.

        Returns Dict() converted to JSON.
        """
        data = self.url_to_short.convert_original_url_to_short_url(original_url)

        return json.dumps(data)
