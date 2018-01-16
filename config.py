import os
import requests


def ngrok_url():
    tunnels = requests.get('http://ngrok:4040/api/tunnels').json()['tunnels']
    for tunnel in tunnels:
        if tunnel['proto'] == 'https':
            return tunnel['public_url']
    raise ValueError('No https tunnel available')


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    BASE_URL = ngrok_url()


class StagingConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    BASE_URL = 'https://' + os.environ.get('HEROKU_APP_NAME', '') + '.herokuapp.com'
