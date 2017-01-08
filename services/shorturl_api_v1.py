import cherrypy
import json
import sys

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

    ACCEPTED_METHODS = ['GET', 'POST']

    def __init__(self):
        """Initialization instantiations."""
        self.shorturl = ShortURL()
        self.check_method()


    def check_method(self):
        """Utility method to make sure that the sent METHOD is an accepted METHOD."""
        if cherrypy.request.method not in self.ACCEPTED_METHODS:
            raise cherrypy.HTTPError(405)


    @cherrypy.tools.accept(media='text/plain')
    @rate_limited(2)
    def GET(self, short_url):
        """Return a set of data based on the original URL.

        successful example:

        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing',
            'created': '2017-01-05 02:57:10.366'
        }


        TODO add simple validation for short_url
        """
        return self.shorturl.short_to_original_json(short_url)


    @rate_limited(2)
    def POST(self, original_url):
        """Return a set of data based on the original URL.

        successful example:

        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing',
            'created': '2017-01-05 02:57:10.366'
        }


        TODO add simple validation for original_url
        """
        return self.shorturl.original_to_short_json(original_url)
