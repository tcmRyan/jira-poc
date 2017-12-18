from server.webhooks import callbacks
from server.webhooks.callbacks import IssueCreationCallback

registered_callbacks = []


def register_view(view):
    callbacks.add_resource(IssueCreationCallback, IssueCreationCallback().url)
    registered_callbacks.append(view)


register_view(IssueCreationCallback)
