import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False

