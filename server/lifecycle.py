from flask import request, jsonify
from server.desciptor import Descriptor
from server import app
from server.queries import connection
from server.queries.authentications.queries import queries


@app.route('/install/<descriptor>')
def install(descriptor):
    """ Return the atlassian json file, supports multiple descriptors"""
    install_app = {}
    if descriptor == 'pythia':
        install_app = Descriptor(
            key='pythia-addon',
            name='Pythia',
            description='Visualize the current state of the engineering system and identify any engineering constraints',
            vendor_name='Ryan Schaffer',
            vendor_url='https://www.example.com',
            scopes=['read', 'admin']
        )

    return jsonify(install_app.descriptor)


@app.route('/add-on-installed-callback', methods=['POST'])
def installed():
    install_data = request.get_json()
    install_data.update({'installedBy': request.args.get('user_key')})
    with connection() as conn:
        queries.insert_authentication(
            conn,
            key=install_data.get('key'),
            client_key=install_data.get('clientKey'),
            shared_secret=install_data.get('sharedSecret'),
            plugins_version=install_data.get('pluginsVersion'),
            base_url=install_data.get('baseUrl'),
            product_type=install_data.get('productType'),
            description=install_data.get('description'),
            service_entitlement_number=install_data.get('service_entitlement_number'),
            event_type=install_data.get('eventType'),
            public_key=install_data.get('publicKey'),
            server_version=install_data.get('serverVersion'),
            installed_by=install_data.get('installedBy'),
        )
    return 'OK'


@app.route('/add-on-enable', methods=['POST'])
def enabled():
    return 'OK'


@app.route('/uninstall', methods=['POST'])
def uninstalled():
    with connection() as conn:
        queries.delete_authentications_by_client_key(conn, client_key=request.get_json().get('clientKey'))
    return 'OK'
