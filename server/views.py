import os
from server import app, db
from server.desciptor import Descriptor
from flask import render_template, request, jsonify
from server.models import Authentication
from server.authentication import authenticate, development_only
from server.lib import AtLib

site_root = os.path.realpath(os.path.dirname(__file__))
static_path = os.path.join(os.path.join(site_root, "static"))
template_path = os.path.join(os.path.join(site_root, "templates"))


@app.route('/')
def index():
    return "Welcome"


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
            scopes=['READ', 'ADMIN']
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


@app.route('/welcome')
@authenticate
def welcome():
    atlassian = AtLib(request.args.get('xdm_e'))
    prop = atlassian.projects
    workflows = atlassian.workflows
    return render_template('hello_world.html', properties=prop, workflows=workflows)


@app.route('/explore', methods=['GET', 'POST'])
@development_only
def explore():
    params = {}
    if request.method == 'GET':
        return render_template('api_explorer.html', resp_data={})
    elif request.method == 'POST':
        req = AtLib(request.form['baseUrl'])
        if request.form['expand']:
            params = {'expand': request.form['expand']}
        resp = req.explore_endpoint(request.form['method'], request.form['rel'], params=params)
        return render_template('api_explorer.html', resp_data=resp)
    else:
        return 'Nope!'
