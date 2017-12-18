import os
from server import app
from flask import render_template, request
from server.authentication import authenticate, development_only
from server.atl_requests.lib import AtLib

site_root = os.path.realpath(os.path.dirname(__file__))
static_path = os.path.join(os.path.join(site_root, "static"))
template_path = os.path.join(os.path.join(site_root, "templates"))


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
