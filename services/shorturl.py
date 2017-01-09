import cherrypy

from services import URLToShort, ShortToURL


class ShortURL(object):
    """Provides functionality for shortening URLs and retrieving original URLs.

    URL shortening is based off IDs in the database, not just raw strings. Bijective functions
    (https://en.wikipedia.org/wiki/Bijection) and BASE 62 was chosen as the default after
    researching on Stack Overflow and Google.
    """

    def __init__(self):
        """Initialization instantiations."""
        self.short_to_url = ShortToURL()
        self.url_to_short = URLToShort()


    def standardize_error(self, error):
        """Send standard Cherrypy error response plus a standardized response through API."""
        cherrypy.response.status = error.status
        return dict(
            status=self.short_to_url.STATUS_ERROR,  # just need any subclass of ShortURLBase
            code=error.status,
            error=error._message
        )


    def standardize_success(self, data):
        """Send standardized success response plus add success status."""
        if not data.get('status'):
            data.update(
                dict(status=self.short_to_url.STATUS_OK)  # just need any subclass of ShortURLBase
            )
        return data


    def convert_urls(self, func, params_list):
        """Take a list of params and apply the provided function to each item in the list.

        Note: the default use case is a *single url* in the params list.
        """
        try:
            data = list(map(func, params_list))[0]  # "unwrap" list to expose data dict
        except cherrypy._cperror.HTTPError as e:
            # Note: use dir() to find all attributes of the HTTPError
            # object to access and create custom error responses
            return self.standardize_error(e)

        return data


    def short_to_original(self, short_url):
        """[GET] Takes a short url and retrieves the original url.

        Returns dictionary
        """
        data = self.convert_urls(
            self.short_to_url.convert_short_url_to_original_url,
            short_url.split()  # need to pass in an list here so split() will do
        )

        return self.standardize_success(data)


    def original_to_short(self, original_url):
        """[POST] Takes a original url and makes it a short url.

        Returns a dictionary
        """
        data = self.convert_urls(
            self.url_to_short.convert_original_url_to_short_url,
            original_url.split()  # need to pass in an list here so split() will do
        )

        return self.standardize_success(data)
