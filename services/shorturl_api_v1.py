import cherrypy
import json

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

    ACCEPTED_CONTENT_TYPES = dict(json='application/json', plain='text/plain')

    def __init__(self):
        """Initialization instantiations."""
        self.shorturl = ShortURL()


    def process_params(self, params):
        """Support AJAX requests that are JSON formatted.

        This method is needed in order to support AJAX requests if a `Content-Type` header is
        declared. I have opted to require AJAX callers declare this because it is more beneficial
        to be explicit. Wait, explicit, go figure ;)
        """
        header_content_type = cherrypy.request.headers.get('Content-Type')
        if not params:
            if header_content_type == self.ACCEPTED_CONTENT_TYPES.get('plain'):
                params = json.loads(cherrypy.request.body.read().decode('utf-8'))
            elif header_content_type == self.ACCEPTED_CONTENT_TYPES.get('json'):
                params = cherrypy.request.json
            else:
                raise cherrypy.HTTPError(400, 'ERROR_INCORRECT_OR_MISSING_PARAM')
        elif params and (header_content_type in self.ACCEPTED_CONTENT_TYPES.values()):
            # supports GETs
            params = json.loads(list(params.keys())[0])

        return params


    def retrieve_param(self, identifier, params):
        """Retrieve the specified parameter."""
        identified_param = params.get(identifier)

        if not identified_param:
            raise cherrypy.HTTPError(400, 'ERROR_INCORRECT_OR_MISSING_PARAM')

        return identified_param


    @rate_limited(2)
    def OPTIONS(self, *args, **kwargs):
        """Accept CORS preflight check if 'Content-Type' header is not standard for AJAX.
    
        The BODY of OPTIONS is not important. Accepts any params (needed).

        per https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS#Overview
        "...the specification mandates that browsers "preflight" the request, soliciting
        supported methods from the server with an HTTP OPTIONS request method..."

        per http://api.jquery.com/jquery.ajax/  (regarding `contentType`)
        "Note: For cross-domain requests, setting the content type to anything other than
        application/x-www-form-urlencoded, multipart/form-data, or text/plain will trigger
        the browser to send a preflight OPTIONS request to the server."

        Important REQEUST HEADERS to look at
        (example per jQuery `contentType: 'application/json'`):
            Request Headers:
              ACCESS-CONTROL-REQUEST-HEADERS: content-type
              ACCESS-CONTROL-REQUEST-METHOD: GET

        See corsheaders() in the main configuration. They "answer" the "preflight" request. 
        """
        return


    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @rate_limited(2)
    def GET(self, **kwargs):
        """Return a set of data based on the original URL.

        successful example:

        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing',
            'created': '2017-01-05 02:57:10.366'
        }
        """
        params = kwargs
        try:
            params = self.process_params(params)
            short_url = self.retrieve_param('short_url', params)
        except cherrypy._cperror.HTTPError as e:
            return self.shorturl.standardize_error(e)

        return self.shorturl.short_to_original(short_url)


    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @rate_limited(2)
    def POST(self, **kwargs):
        """Return a set of data based on the original URL.

        successful example:

        {
            'short_url': 'http://shortu.rl/qM',
            'original_url': 'http://example.com/hello-there/testing',
            'created': '2017-01-05 02:57:10.366'
        }
        """
        params = kwargs
        try:
            params = self.process_params(params)
            original_url = self.retrieve_param('original_url', params)
        except cherrypy._cperror.HTTPError as e:
            return self.shorturl.standardize_error(e)

        return self.shorturl.original_to_short(original_url)
