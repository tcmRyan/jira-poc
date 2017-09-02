from urllib.parse import urlencode
from urllib.error import HTTPError
import atlassian_jwt
import requests
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


class AtlassianRequest(object):

    session = None
    responses = None

    def __init__(self, tenant_data):
        self.session = requests.Session()
        self.tenant_data = tenant_data

    def _authorize(self, uri, method):
        jwt_auth = atlassian_jwt.encode_token(
            method,
            uri,
            self.tenant_data.key,
            self.tenant_data.sharedSecret
        )
        return {'Authorization': 'JWT {}'.format(jwt_auth)}

    def request(self, method, rel, **kwargs):
        method = method.upper()
        uri = self.tenant_data.baseUrl + rel
        request_args = {
            'url': uri,
            'method': method
        }
        if kwargs.get('params'):
            uri = uri + urlencode(kwargs.get('params'))

        auth_header = self._authorize(uri, method)
        headers = kwargs.get('headers', {})
        kwargs['headers'] = auth_header if not headers else headers.append(auth_header)

        request_args.update(kwargs)

        return self.session.request(**request_args)

    def reset(self):
        self.session = requests.Session()


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
