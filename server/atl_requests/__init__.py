from server.models import Authentication
import atlassian_jwt
import requests
from urllib.parse import urlencode
from server.atl_requests.lib import AtLib


class Context:
    def __init__(self, org):
        self.tenant_info = Authentication.query.filter_by(baseUrl=org).first()

    @property
    def base_url(self):
        return self.tenant_info.baseUrl

    @property
    def key(self):
        return self.tenant_info.key

    @property
    def shared_secret(self):
        return self.tenant_info.sharedSecret


class AtlassianRequestor:
    def __init__(self, ctx):
        self.ctx = ctx
        self.session = requests.Session()

    def _generate_auth_header(self, uri, method):
        jwt_auth = atlassian_jwt.encode_token(
            method,
            uri,
            self.ctx.key,
            self.ctx.shared_secret
        )
        return {'Authorization': f'JWT {jwt_auth}'}

    def request(self, method, rel, **kwargs):
        method = method.upper()
        uri = self.ctx.base_url + rel
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
        return self.request('GET', rel, **kwargs)

    def post(self, rel, **kwargs):
        return self.request('POST', rel, **kwargs)

    def put(self, rel, **kwargs):
        return self.request('PUT', rel, **kwargs)

    def delete(self, rel, **kwargs):
        return self.request('DELETE', rel, **kwargs)
