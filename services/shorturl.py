import json
import cherrypy
import sys

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


    def standard_json_error(self, error):
        """Send standard Cherrypy error response plus a standardized response through API."""
        cherrypy.response.status = error.status
        return json.dumps(
            dict(
                status=self.short_to_url.STATUS_ERROR,  # just need any subclass of ShortURLBase
                code=error.status,
                error=error._message
            )
        )


    def standard_json_success(self, data):
        """Send standardized success response plus add success status."""
        if not data.get('status'):
            data.update(
                dict(status=self.short_to_url.STATUS_OK)  # just need any subclass of ShortURLBase
            )
        return json.dumps(data)


    def short_to_original_json(self, short_url):
        """[GET] Takes a short url and retrieves the original url.

        Returns Dict() converted to JSON.
        """
        try:
            data = self.short_to_url.convert_short_url_to_original_url(short_url)
        except cherrypy._cperror.HTTPError as e:
            # Note: use dir() to find all attributes of the HTTPError
            # object to access and create custom error responses
            return self.standard_json_error(e)

        return self.standard_json_success(data)


    def original_to_short_json(self, original_url):
        """[POST] Takes a original url and makes it a short url.

        Returns Dict() converted to JSON.
        """
        try:
            data = self.url_to_short.convert_original_url_to_short_url(original_url)
        except cherrypy._cperror.HTTPError as e:
            # Note: use dir() to find all attributes of the HTTPError
            # object to access and create custom error responses
            return self.standard_json_error(e)

        return self.standard_json_success(data)
