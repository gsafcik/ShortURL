import cherrypy

from services import SQLite3DBSetup, ShortURLAPIv1


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
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.engine.subscribe('start', SQLite3DBSetup.setup_database)
    cherrypy.quickstart(ShortURLAPIv1(), CURRENT_VERSION, conf)


if __name__ == '__main__':
    main()
