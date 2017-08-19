import atlassian_jwt


class JWTToken(atlassian_jwt.Authenticator):

    def __init__(self, tenant_info_store):
        super(JWTToken, self).__init__()
        self.tenant_info_store = tenant_info_store

    def get_shared_secret(self, client_key):
        return self.tenant_info_store['sharedSecret']
