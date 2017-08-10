import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('APP_SECRET')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False

