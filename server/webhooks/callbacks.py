from flask import request, url_for
from server.webhooks import WebhookContext, WebHook
from server import app


class IssueCreationCallback(WebHook):
    @app.route('/callbacks/issue-creation')
    def callbacks_issue_creation(self):
        data = request.get_json()
        ctx = WebhookContext(data['issue'])
        print('BaseUrl: {}, Key: {}, SharedSecret: {}'.format(ctx.base_url, ctx.key, ctx.shared_secret))
        return 'OK'

    @property
    def descriptor(self):
        description = {
            "event": "jira:issue_created",
            "url": url_for('callbacks_issue_creation'),
            "excludeBody": False,
            "filter": "",
        }
        return description


class IssueCreationCallback2(WebHook):
    @app.route('/callbacks/issue-something-else')
    def callbacks_issue_something_else(self):
        data = request.get_json()
        ctx = WebhookContext(data['issue'])
        print('BaseUrl: {}, Key: {}, SharedSecret: {}'.format(ctx.base_url, ctx.key, ctx.shared_secret))
        return 'OK'

    @property
    def descriptor(self):
        description = {
            "event": "jira:issue_created",
            "url": url_for('callbacks_issue_something_else'),
            "excludeBody": False,
            "filter": "",
        }
        return description
