#!env/bin/python

import os
import itertools

from werkzeug.wsgi import DispatcherMiddleware
from flask_script import Manager, Server
from wsgi_basic_auth import BasicAuth
from wsgi_sslify import sslify

import dwellingplace.settings
import dwellingplace.app
import red


def find_assets(app):
    """Yield paths for all static files and templates."""
    for name in ['static', 'templates']:
        directory = os.path.join(app.config['PATH'], name)
        for entry in os.scandir(directory):
            if entry.is_file():
                yield entry.path


config = dwellingplace.settings.get_config(os.getenv('FLASK_ENV'))
os.environ['WSGI_AUTH_CREDENTIALS'] = config.WSGI_AUTH_CREDENTIALS


dpapp = dwellingplace.app.create_app(config)
redapp = red.create_app(config)

wsgi_app = BasicAuth(DispatcherMiddleware(dpapp.wsgi_app, {
    '/red': redapp.wsgi_app
}))

if dpapp.config['USE_HTTPS']:
    wsgi_app = sslify(wsgi_app)  # pylint: disable=redefined-variable-type

dpapp.wsgi_app = wsgi_app

server = Server(host='0.0.0.0', extra_files=itertools.chain(find_assets(dpapp), find_assets(redapp)))

manager = Manager(dpapp)
manager.add_command('run', server)


if __name__ == '__main__':
    manager.run()
