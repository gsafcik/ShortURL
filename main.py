import cherrypy
from urllib.parse import urlparse, urljoin

from services import DB, DBSetup, URLShortenerAPIv1
# from services.factories import *


def main():
    """Initialize application."""
    API_URI_NAME = 'shorturl'
    VERSION = 'v1'
    CURRENT_VERSION = '/' + '/'.join([API_URI_NAME, VERSION])

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'server.socket_host': '0.0.0.0'
        }
    }

    cherrypy.engine.subscribe('start', DBSetup.setup_database)
    cherrypy.quickstart(URLShortenerAPIv1(), CURRENT_VERSION, conf)


if __name__ == '__main__':
    main()
