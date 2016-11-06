import os


class Config:
    """Base configuration."""

    ENV = None

    PATH = os.path.abspath(os.path.dirname(__file__))
    ROOT = os.path.dirname(PATH)
    DEBUG = False
    THREADED = False


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'

    SECRET_KEY = os.getenv('SECRET_KEY')
    WSGI_AUTH_CREDENTIALS = os.getenv('WSGI_AUTH_CREDENTIALS')
    MONGO_URI = os.getenv('MONGODB_URI')


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'

    DEBUG = True
    TESTING = True

    SECRET_KEY = 'test'
    WSGI_AUTH_CREDENTIALS = None
    MONGO_DBNAME = 'red_test'


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'

    DEBUG = True

    SECRET_KEY = 'dev'
    WSGI_AUTH_CREDENTIALS = 'admin:password'
    MONGO_DBNAME = 'red_dev'


def get_config(name):
    assert name, "no configuration specified"

    for config in Config.__subclasses__():  # pylint: disable=no-member
        if config.ENV == name:
            return config

    assert False, "no matching configuration"
