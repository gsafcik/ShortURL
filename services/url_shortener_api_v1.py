import cherrypy
from services import URLShortener


@cherrypy.expose
class URLShortenerAPIv1(object):
    """Create shortened URLs and convert them back.
    
    REST URIs for v1:
    - [GET]     /v1/<SHORT_URL>      RETURNS data including both URLs, based on short URL.
    - [POST]    /v1/<ORIGINAL_URL>   RETURNS data including both URLs, based on original URL.
    """

    def __init__(self):
        """."""
        self.url_shortener = URLShortener()


    @cherrypy.tools.accept(media='text/plain')
    def GET(self, short_url):
        """Return a set of JSON data based on the original URL.

        If SUCCESS, the response will look like:
        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing'
            'created': '2017-01-05 02:57:10.366',
        }


        TODO add validation for short_url
        """
        return self.url_shortener.convert_short_url_to_original_url(short_url)


    def POST(self, original_url):
        """Return a set of JSON data based on the original URL.

        If SUCCESS, the response will look like:
        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing'
            'created': '2017-01-05 02:57:10.366',
        }


        TODO add validation for original_url
        """
        return self.url_shortener.convert_original_url_to_short_url(original_url)
