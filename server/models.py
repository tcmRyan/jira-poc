from server import db


class Authentication(db.Model):
    __tablename__ = 'authentications'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    clientKey = db.Column(db.String)
    sharedSecret = db.Column(db.String)
    pluginsVersion = db.Column(db.String)
    baseUrl = db.Column(db.String)
    productType = db.Column(db.String)
    description = db.Column(db.String)
    serviceEntitlementNumber = db.Column(db.String)
    eventType = db.Column(db.String)
    publicKey = db.Column(db.String)
    serverVersion = db.Column(db.String)
    installedBy = db.Column(db.String)

    def __init__(self, install_data):
        self.id = install_data.get('id')
        self.key = install_data.get('key')
        self.clientKey = install_data.get('clientKey')
        self.sharedSecret = install_data.get('sharedSecret')
        self.pluginsVersion = install_data.get('pluginsVersion')
        self.baseUrl = install_data.get('baseUrl')
        self.productType = install_data.get('productType')
        self.serviceEntitlementNumber = install_data.get('service_entitlement_number')
        self.eventType = install_data.get('eventType')
        self.description = install_data.get('description')
        self.publicKey = install_data.get('publicKey')
        self.serverVersion = install_data.get('serverVersion')
        self.installedBy = install_data.get('installedBy')

    def __repr__(self):
        return '<id {}>'.format(self.id)
