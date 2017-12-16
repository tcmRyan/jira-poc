from urllib.error import HTTPError
import atlassian_jwt
from functools import wraps
from server.models import Authentication
from flask import request
from server import app


class SimpleAuthenticator(atlassian_jwt.Authenticator):
    def __init__(self, domain):
        super(SimpleAuthenticator, self).__init__()
        tenant_info = Authentication.query.filter_by(baseUrl=domain).first().__dict__
        tenant_info.pop('_sa_instance_state')
        self.tenant_info_store = tenant_info

    def get_shared_secret(self, client_key):
        return self.tenant_info_store['sharedSecret']


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        base_url = request.args.get('xdm_e')
        auth = SimpleAuthenticator(base_url)
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
