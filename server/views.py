import os
from server import app, db
from flask import render_template, send_from_directory, request
import requests
from server.models import Authentication
import atlassian_jwt

site_root = os.path.realpath(os.path.dirname(__file__))
static_path = os.path.join(os.path.join(site_root, "static"))
template_path = os.path.join(os.path.join(site_root, "templates"))


@app.route('/hello-world')
def home():
    # return send_from_directory(template_path, 'hello_world.html')
    tenat_info = Authentication.query.get(4).__dict__
    tenat_info.pop('_sa_instance_state')
    url = tenat_info['baseUrl'] + '/rest/api/latest/serverInfo'
    token = atlassian_jwt.encode_token('GET', url, **tenat_info)
    headers = {'Authorization': 'JWT {}'.format(token)}

    resp = requests.get(url, headers=headers)
    print(resp.content)
    return resp.content


@app.route('/install/<descriptor>')
def install(descriptor):
    """ Return the atlassian json file"""
    return send_from_directory(static_path, descriptor)


@app.route('/add-on-installed-callback', methods=['POST'])
def install_callback():
    install_data = request.get_json()
    auth = Authentication(install_data)
    db.session.add(auth)
    db.session.commit()
    return 'OK'




