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

    MONGO_URI = os.getenv('MONGODB_URI')
    WSGI_AUTH_CREDENTIALS = os.getenv('WSGI_AUTH_CREDENTIALS')


class TestConfig(Config):
    """Test configuration."""

    ENV = 'test'

    DEBUG = True
    TESTING = True

    MONGO_DBNAME = 'dwellingplace_test'
    WSGI_AUTH_CREDENTIALS = None


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'

    DEBUG = True

    MONGO_DBNAME = 'dwellingplace_dev'
    WSGI_AUTH_CREDENTIALS = 'admin:password'


def get_config(name):
    assert name, "no configuration specified"

    for config in Config.__subclasses__():  # pylint: disable=no-member
        if config.ENV == name:
            return config

    assert False, "no matching configuration"
