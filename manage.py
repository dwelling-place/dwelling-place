#!env/bin/python

import os
import itertools

from werkzeug.wsgi import DispatcherMiddleware
from flask_script import Manager, Server
from wsgi_basic_auth import BasicAuth

from dwellingplace.settings import get_config
from dwellingplace.app import create_app
import red
import red.settings


def find_assets(app):
    """Yield paths for all static files and templates."""
    for name in ['static', 'templates']:
        directory = os.path.join(app.config['PATH'], name)
        for entry in os.scandir(directory):
            if entry.is_file():
                yield entry.path


config = get_config(os.getenv('FLASK_ENV'))
os.environ['WSGI_AUTH_CREDENTIALS'] = config.WSGI_AUTH_CREDENTIALS


app = create_app(config)
redapp = red.create_app(config)
DispatcherMiddleware(app, {
    '/red': redapp
}) 
app.wsgi_app = BasicAuth(DispatcherMiddleware(app, {
    '/red': redapp
}))

server = Server(host='0.0.0.0', extra_files=itertools.chain(find_assets(app), find_assets(redapp)))

manager = Manager(app)
manager.add_command('run', server)


if __name__ == '__main__':
    manager.run()
