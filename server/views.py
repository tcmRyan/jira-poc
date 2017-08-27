import os
from server import app, db
from server.desciptor import Descriptor
from flask import render_template, request, jsonify
from server.models import Authentication
from server.authentication import AtlassianRequest

import jwt

site_root = os.path.realpath(os.path.dirname(__file__))
static_path = os.path.join(os.path.join(site_root, "static"))
template_path = os.path.join(os.path.join(site_root, "templates"))


@app.route('/hello-world')
def home():
    # return send_from_directory(template_path, 'hello_world.html')
    tenat_info = Authentication.query.get(10).__dict__
    tenat_info.pop('_sa_instance_state')
    test = jwt.decode(request.args['jwt'], tenat_info['sharedSecret'], algorithms='HS256')
    # url = tenat_info['baseUrl'] + '/rest/atlassian-connect/1/addons/{}'.format(tenat_info['key'])
    url = tenat_info['baseUrl'] + '/rest/api/latest/serverInfo'
    # token = atlassian_jwt.encode_token('GET', url, tenat_info['key'], tenat_info['sharedSecret'])
    # headers = {'Authorization': 'JWT {}'.format(token)}
    #
    # resp = requests.get(url, headers=headers)
    requester = AtlassianRequest(tenat_info)
    resp = requester.request(url)
    print(resp.content)
    return resp.content


@app.route('/install/<descriptor>')
def install(descriptor):
    """ Return the atlassian json file"""
    install_app = {}
    if descriptor == 'pythia':
        install_app = Descriptor(
            key='pythia-addon',
            name='Pythia',
            description='Visualize the current state of the engineering system and identify any engineering constraints',
            vendor_name='Ryan Schaffer',
            vendor_url='https://www.example.com',
            scopes=['READ']
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




