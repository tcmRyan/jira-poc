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
    public_key = db.Column(db.String)
    server_version = db.Column(db.String)

    def __init__(self, install_data):
        self.id = install_data.get('id')
        self.key = install_data.get('key')
        self.client_key = install_data.get('clientKey')
        self.shared_secret = install_data.get('sharedSecret')
        self.plugins_version = install_data.get('pluginsVersion')
        self.base_url = install_data.get('baseUrl')
        self.product_type = install_data.get('productType')
        self.service_entitlement_number = install_data.get('service_entitlement_number')
        self.event_type = install_data.get('eventType')
        self.description = install_data.get('description')
        self.public_key = install_data.get('publicKey')
        self.server_version = install_data.get('serverVersion')

    def __repr__(self):
        return '<id {}>'.format(self.id)
