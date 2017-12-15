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


class AtlassianRequest:
    def __init__(self, session):
        self.session = session

    def _generate_auth_header(self, uri, method):
        jwt_auth = atlassian_jwt.encode_token(
            method,
            uri,
            self.session.tenant_data.key,
            self.session.tenant_data.sharedSecret
        )
        return {f'Authorization': 'JWT {jwt_auth}'}

    def request(self, method, rel, **kwargs):
        method = method.upper()
        uri = self.session.tenant_data.baseUrl + rel
        request_args = {
            'url': uri,
            'method': method
        }
        if kwargs.get('params'):
            uri = uri + '?' + urlencode(kwargs.get('params'))

        auth_header = self._generate_auth_header(uri, method)
        headers = kwargs.get('headers', {})
        kwargs['headers'] = auth_header if not headers else headers.append(auth_header)

        request_args.update(kwargs)

        return self.session.request(**request_args)

    def get(self, rel, **kwargs):
        self.request('GET', rel, **kwargs)

    def post(self, rel, **kwargs):
        self.request('POST', rel, **kwargs)

    def put(self, rel, **kwargs):
        self.request('PUT', rel, **kwargs)

    def delete(self, rel, **kwargs):
        self.request('DELETE', rel, **kwargs)


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
