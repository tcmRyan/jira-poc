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
    BASE_URL = os.environ.get('NGROK_URL')


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    BASE_URL = 'https://' + os.environ.get('HEROKU_APP_NAME', '') + '.herokuapp.com'

