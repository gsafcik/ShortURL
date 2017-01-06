import cherrypy
from urllib.parse import urlparse, urljoin

from services import DB, DBSetup, URLShortenerAPIv1
# from services.factories import *


def main():
    """Initialize application."""
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'server.socket_host': '0.0.0.0'
        }
    }
    current_version = '/v1/'
    cherrypy.engine.subscribe('start', DBSetup.setup_database)
    cherrypy.quickstart(URLShortenerAPIv1(), current_version, conf)


if __name__ == '__main__':
    main()
