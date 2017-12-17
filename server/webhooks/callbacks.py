from flask import request, url_for
from server.webhooks import WebhookContext, WebHook
from server import app


class IssueCreationCallback(WebHook):
    @app.route('/callbacks/issue-creation')
    def callback(self):
        data = request.get_json()
        ctx = WebhookContext(data['issue'])
        print('BaseUrl: {}, Key: {}, SharedSecret: {}'.format(ctx.base_url, ctx.key, ctx.shared_secret))
        return 'OK'

    @property
    def descriptor(self):
        description = {
            "event": "jira:issue_created",
            "url": url_for('callback'),
            "excludeBody": False,
            "filter": "",
        }
        return description


