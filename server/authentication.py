import time
from server.models import Authentication
import jwt
from urllib import parse
from collections import OrderedDict
import hashlib


class JWTToken(object):

    header = {
        "typ": "JWT",
        "alg": "HS256"
    }

    def __init__(self):
        self.auth = Authentication.query.get(2)
        self.shared_secret = self.auth.shared_secret
        self.base_url = self.auth.base_url
        self.context_path = '/'
        self.method = 'GET'
        self.api_path = '/rest/atlassian-connect/latest/license'
        self.jwt = None
        self.create_uri_with_jwt()

    def create_uri_with_jwt(self):
        # TODO: Make this real, right now just using the data in the test db

        issued_at = int(time.time())
        expires_at = issued_at + (60 * 3)  # 3 min window
        claim = {
            'iss': self.auth.key,
            'iat': issued_at,
            'exp': expires_at,
            'qsh': self.get_qsh(self.method, self.api_path)
        }

        self.jwt = jwt.encode(claim, self.shared_secret, algorithm='HS256', headers=self.header)

    def get_qsh(self, method, api_path, params={}, data={}):
        method = method.upper()
        canonical_uri = api_path if api_path else '/'
        if method == 'GET':
            params.pop('jwt', None)
            claims_data = self.sort_data(params)
        elif method == 'POST':
            claims_data = self.sort_data(data)
        else:
            claims_data = ''
        canonical_qs = parse.urlencode(claims_data, encoding='utf-8')
        canonical = '&'.join([method, canonical_uri, canonical_qs])
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    def sort_data(self, data_or_params):
        # TODO Atlassian recommends that you sort after encoding, ignoring that requirement for now
        return OrderedDict(sorted(data_or_params.items()))






