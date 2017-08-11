import time
class JWTToken(object):

    header = {
        "typ": "JWT",
        "alg": "HS256"
    }

    def create_uri_with_jwt(self):
        issuedAt = int(time.time())
        expiresAt = issuedAt + (60 * 3) # 3 min window
        key = "jira-poc"
        sharedSecret =