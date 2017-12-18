from urllib.error import HTTPError
import atlassian_jwt
from functools import wraps
from flask import request
from server import app
from server.models import Authentication
from urllib.parse import urlparse
import json


def parse_url(url):
    o = urlparse(url)
    return o.scheme + '://' + o.netloc


class Context:
    def __init__(self, url):
        org = parse_url(url)
        self.tenant_info = Authentication.query.filter_by(baseUrl=org).first().__dict__

    @property
    def base_url(self):
        return self.tenant_info['baseUrl']

    @property
    def key(self):
        return self.tenant_info['key']

    @property
    def shared_secret(self):
        return self.tenant_info['sharedSecret']


class SimpleAuthenticator(atlassian_jwt.Authenticator):
    def __init__(self, ctx):
        super(SimpleAuthenticator, self).__init__()
        # tenant_info = Authentication.query.filter_by(baseUrl=domain).first().__dict__
        # tenant_info.pop('_sa_instance_state')
        self.tenant_info_store = ctx.tenant_info

    def get_shared_secret(self, client_key):
        return self.tenant_info_store['sharedSecret']


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = request.args.get('xdm_e')
        if not url:
            # Atlassian decided not do give us anything in the headers
            url = request.get_json()['user']['self']
        ctx = Context(url)
        auth = SimpleAuthenticator(ctx)
        auth.authenticate(request.method, request.url, request.headers)

        return func(*args, **kwargs)
    return wrapper


def development_only(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if app.config['DEVELOPMENT']:
            return func(*args, **kwargs)
        else:
            return HTTPError(args[0], 403, 'Not a valid url for this environment')
    return wrapper
