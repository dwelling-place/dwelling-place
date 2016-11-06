from flask import Flask

__all__ = 'create_app',


def create_app(config):
    application = Flask('red', instance_relative_config=True)
    application.config.from_object(config)

    from .routes import blueprint, mongo, api

    application.register_blueprint(blueprint)
    mongo.init_app(application)
    api.init_app(application)

    return application
