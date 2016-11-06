#!env/bin/python

import os

from flask_script import Manager, Server
from wsgi_basic_auth import BasicAuth
from wsgi_sslify import sslify

from dwellingplace.settings import get_config
from dwellingplace.app import create_app


def find_assets():
    """Yield paths for all static files and templates."""
    for name in ['static', 'templates']:
        directory = os.path.join(app.config['PATH'], name)
        for entry in os.scandir(directory):
            if entry.is_file():
                yield entry.path


config = get_config(os.getenv('FLASK_ENV'))
os.environ['WSGI_AUTH_CREDENTIALS'] = config.WSGI_AUTH_CREDENTIALS

app = create_app(config)
app.wsgi_app = BasicAuth(app.wsgi_app)
if app.config['USE_HTTPS']:
    app.wsgi_app = sslify(app.wsgi_app)  # pylint: disable=redefined-variable-type

server = Server(host='0.0.0.0', extra_files=find_assets())

manager = Manager(app)
manager.add_command('run', server)


if __name__ == '__main__':
    manager.run()
