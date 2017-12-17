from server import app
from flask import url_for
from server.webhooks import WebHook


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
                'enabled': url_for('enabled'),
                'uninstalled': url_for('uninstalled')
            },
            'scopes': scopes,
            "modules": {
                "generalPages": [
                    {
                        "url": "/welcome",
                        "key": key,
                        "location": "system.top.navigation.bar",
                        "name": {
                            "value": "Greeting"
                        }
                    }
                ]
            },
        }

        self.build_description()

    def build_description(self):
        self.descriptor['modules']['webhooks'] = self.webhooks
        pass

    @property
    def webhooks(self):
        webhooks = []
        for webhook in WebHook:
            webhooks.append(webhook().descriptor)

        return webhooks
