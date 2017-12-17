from urllib.parse import urlparse
from server.atl_requests import Context
from flask import url_for


class WebhookContext(Context):

    def __init__(self, callback):
        org = self.parse_callback(callback)
        super().__init__(org)

    def parse_callback(self, callback):
        o = urlparse(callback['self'])
        return o.scheme + '://' + o.netloc


class RegisterWebHooks(type):
    def __init__(cls, name, bases, nmspc):
        super(RegisterWebHooks, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = set()
        cls.registry.add(cls)
        cls.registry -= set(bases)

    def __iter__(cls):
        return iter(cls.registry)

    def __str__(cls):
        if cls in cls.registry:
            return cls.__name__
        return cls.__name__ + ": " + ", ".join([sc.__name__ for sc in cls])


class WebHook(object, metaclass=RegisterWebHooks):

    def callback(self):
        """
        The callback url for the webhook.  Needs to be decorated by app.route
        :return: HTTP Response
        """
        pass

    @property
    def descriptor(self):
        """
        Create the descriptor that needs to be registered as part of the main descriptor
        during installation
        :return: Dictionary
        """
        description = {
            "event": "jira:issue_created",
            "url": url_for(self.callback),
            "excludeBody": False,
            "filter": "",
        }
        return description




