#!/usr/local/bin/python3.5

import cherrypy
from services import URLShortener


@cherrypy.expose
class URLShortenerAPIv1(object):
    """Create shortened URLs and convert them back.
    
    Basic versioning is used here.

    REST URIs:
    [GET]     /v1/<SHORT_URL>      RETURNS original URL from short URL.
    [POST]    /v1/<original_URL>   RETURNS a short URL from a original URL.
    [DELETE]  /v1/<SHORT_URL>      RETURNS "Success" on success or ERROR on error.
    """
    def __init__(self):
        self.url_shortener = URLShortener()


    @cherrypy.tools.accept(media='text/plain')
    def GET(self, short_url):
        return self.url_shortener.convert_short_url_to_original_url(short_url)
 
    
    def POST(self, original_url):
        """RETURN short URL from a original URL.
    
        @login_url must be string.
        TODO add validation for original_url
        """
        return self.url_shortener.convert_original_url_to_short_url(original_url)

    
    def DELETE(self):
        return 'call to DELETE'
