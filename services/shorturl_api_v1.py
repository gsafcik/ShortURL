import cherrypy

from ratelimit import *
from services import ShortURL


@cherrypy.expose
class ShortURLAPIv1(object):
    """Create shortened URLs and convert them back.

    REST URIs for v1:
    - [GET]   /shorturl/v1/<SHORT_URL>      RETURNS data including both URLs, based on short URL.
    - [POST]  /shorturl/v1/<ORIGINAL_URL>   RETURNS data including both URLs, based on original URL.

    The REST URIs are rate limited (2 requests per second) using the ratelimit module
    found here: https://pypi.python.org/pypi/ratelimit/1.1.0.

    Motivation for the REST URI architecture came from GOOG.LE URL shortener. The idea is to let
    METHODS tell us what we need to do (and not nest deeply). Thus, the REST URIs are simple and
    return the same data (with just different inputs). The return data could be modified in future
    versions.
    """

    def __init__(self):
        """Initialization instantiations."""
        self.shorturl = ShortURL()


    def retrieve_param(self, identifier, params):
        """Retrieve the specified parameter."""
        try:
            identified_param = params.get(identifier)
            if not identified_param:
                raise cherrypy.HTTPError(400, 'ERROR_INCORRECT_OR_MISSING_PARAM')
        except cherrypy._cperror.HTTPError as e:
            return self.shorturl.standardize_error(e)

        return identified_param


    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    @rate_limited(2)
    def GET(self, **vpath):
        """Return a set of data based on the original URL.

        successful example:

        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing',
            'created': '2017-01-05 02:57:10.366'
        }
        """
        short_url = self.retrieve_param('short_url', vpath)
        try:
            if short_url.get('status'):  # if a dict (not a str), return
                return short_url
        except AttributeError:
            pass

        return self.shorturl.short_to_original(short_url)


    @cherrypy.tools.json_out()
    @rate_limited(2)
    def POST(self, **vpath):
        """Return a set of data based on the original URL.

        successful example:

        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing',
            'created': '2017-01-05 02:57:10.366'
        }
        """
        original_url = self.retrieve_param('original_url', vpath)
        try:
            if original_url.get('status'):  # if a dict (not a str), return
                return original_url
        except AttributeError:
            pass

        return self.shorturl.original_to_short(original_url)
