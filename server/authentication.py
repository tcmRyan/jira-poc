import atlassian_jwt
import requests
from urllib.parse import urlencode


class SimpleAuthenticator(atlassian_jwt.Authenticator):

    def __init__(self, tenant_info_store):
        super(SimpleAuthenticator, self).__init__()
        self.tenant_info_store = tenant_info_store

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
            self.tenant_data['key'],
            self.tenant_data['sharedSecret']
        )
        return {'Authorization': 'JWT {}'.format(jwt_auth)}

    def request(self, uri, method='GET', **kwargs):
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
