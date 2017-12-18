from flask import request, jsonify
from server.authentication import Authentication
from server.desciptor import Descriptor
from server import app, db


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
    auth = Authentication(install_data)
    db.session.add(auth)
    db.session.commit()
    return 'OK'


@app.route('/add-on-enable', methods=['POST'])
def enabled():
    return 'OK'


@app.route('/uninstall', methods=['POST'])
def uninstalled():
    Authentication.query.filter_by(clientKey=request.get_json().get('clientKey')).delete()
    db.session.commit()
    return 'OK'
