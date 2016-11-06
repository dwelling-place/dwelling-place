#!env/bin/python

import os

from flask_script import Manager, Server
from wsgi_basic_auth import BasicAuth

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

app = create_app(config)
if not os.environ.get('WSGI_AUTH_CREDENTIALS'):
    os.environ['WSGI_AUTH_CREDENTIALS'] = 'foo:bar'
app.wsgi_app = BasicAuth(app.wsgi_app)

server = Server(host='0.0.0.0', extra_files=find_assets())

manager = Manager(app)
manager.add_command('run', server)


if __name__ == '__main__':
    manager.run()
