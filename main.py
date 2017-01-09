import cherrypy

from services import SQLite3DBSetup, ShortURLAPIv1


@cherrypy.tools.register('before_finalize')
def secureheaders():
    """Copied from the CherryPy doccs and modeled after Google's URL Shortener header values.

    Documentation referenced:
    - https://developers.google.com/url-shortener/v1/getting_started
    - http://cherrypy.readthedocs.io/en/latest/advanced.html?highlight=security#securing-your-server
    - https://www.keycdn.com/blog/x-xss-protection/
    """
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'SAMEORIGIN'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Access-Control-Allow-Origin'] = '*'  # CSRF concern. However, we don't expose any
                                                  # sensitive info nor do we authenticate/authorize
                                                  # users. When those are implemented, we might
                                                  # need to readdress this security concern.


def main():
    """Initialize application."""
    API_URI_NAME = 'shorturl'
    VERSION = 'v1'
    CURRENT_VERSION = '/' + '/'.join([API_URI_NAME, VERSION])

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            # 'tools.sessions.on': True,  # future need?
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')],
            'tools.secureheaders.on': True,
            'tools.json_in.force': False  # "If the 'force' argument is True (the default), then
                                          # entities of other content types will not be allowed;
                                          # '415 Unsupported Media Type' is raised instead." per
                                          # http://svn.cherrypy.org/trunk/cherrypy/lib/jsontools.py.
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.engine.subscribe('start', SQLite3DBSetup.setup_database)
    cherrypy.quickstart(ShortURLAPIv1(), CURRENT_VERSION, conf)


if __name__ == '__main__':
    main()
