from server import db


class Authentication(db.Model):
    __tablename__ = 'authentications'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    client_key = db.Column(db.String)
    shared_secret = db.Column(db.String)
    plugins_version = db.Column(db.String)
    base_url = db.Column(db.String)
    product_type = db.Column(db.String)
    description = db.Column(db.String)
    service_entitlement_number = db.Column(db.String)
    event_type = db.Column(db.String)
    oauth_client_id = db.Column(db.String)
    installed_by = db.Column(db.String)

    def __init__(self, install_data, context):
        self.id = install_data.get('id')
        self.key = install_data.get('key')
        self.client_key = install_data.get('client_key')
        self.shared_secret = install_data.get('shared_secret')
        self.plugins_version = install_data.get('plugins_version')
        self.base_url = install_data.get('base_url')
        self.product_type = install_data.get('product_type')
        self.service_entitlement_number = install_data.get('service_entitlement_number')
        self.event_type = install_data.get('event_type')
        self.oauth_client_id = install_data.get('oauth_client_id')
        self.installed_by = context['user']['userKey']

    def __repr__(self):
        return '<id {}>'.format(self.id)
