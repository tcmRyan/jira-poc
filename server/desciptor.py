from server import app
from flask import url_for


class Descriptor(object):

    def __init__(self, key, name, description, vendor_name,
                 vendor_url, scopes, env_prefix='PP_'):

        self.descriptor = {
            'key': key,
            'name': name,
            'description': description,
            'baseUrl': app.config.get('BASE_URL'),
            'vendor': {
                'url': vendor_url,
                'name': vendor_name
            },
            'enableLicensing': False,
            'authentication': {
                'type': 'JWT'
            },
            'apiVersion': 2,
            'lifecycle': {
                'installed': url_for('installed'),
                'enabled': url_for('enabled')
            },
            'scopes': scopes,
            "modules": {
                "generalPages": [
                    {
                        "url": "/hello-world",
                        "key": key,
                        "location": "system.top.navigation.bar",
                        "name": {
                            "value": "Greeting"
                        }
                    }
                ]
            },
        }
