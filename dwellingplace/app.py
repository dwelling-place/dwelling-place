import logging

from flask import Flask
from flask_login import LoginManager

from . import views
from . import extensions
from . import models
from .models.user import User


log = logging.getLogger(__name__)
login_manager = LoginManager()


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    configure_logging(app)

    register_blueprints(app)
    register_extensions(app)

    with app.app_context():
        models.Metric.create_indexes()

    return app


def configure_logging(app):
    if app.config['DEBUG']:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def register_blueprints(app):
    app.register_blueprint(views.index.blueprint)
    app.register_blueprint(views.api.blueprint)


def register_extensions(app):
    extensions.mongo.init_app(app)
    login_manager.init_app(app)
