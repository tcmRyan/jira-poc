from flask import request
from flask_restful import Resource
from server.authentication import authenticate, Context


class IssueCreationCallback(Resource):
    decorators = [authenticate]

    @property
    def url(self):
        return '/callbacks/issue-creation'

    def get(self):
        return {}, 201

    def post(self):
        data = request.get_json()
        ctx = Context(data['issue']['self'])
        print('BaseUrl: {}, Key: {}, SharedSecret: {}'.format(ctx.base_url, ctx.key, ctx.shared_secret))
        return {}, 201

    @property
    def descriptor(self):
        description = {
            "event": "jira:issue_created",
            "url": self.url,
            "excludeBody": False
        }
        return description
