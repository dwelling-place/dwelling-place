import logging

from flask import Flask

from . import views
from . import extensions
from . import models


log = logging.getLogger(__name__)


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
