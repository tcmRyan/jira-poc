import os
from server import app
from flask import render_template, send_from_directory

site_root = os.path.realpath(os.path.dirname(__file__))
static_path = os.path.join(os.path.join(site_root, "static"))
template_path = os.path.join(os.path.join(site_root, "templates"))


@app.route('/hello-world')
def index():
    # return send_from_directory(template_path, 'hello_world.html')
    return render_template('hello_world.html')

@app.route('/install/<descriptor>')
def install(descriptor):
    """ Return the atlassian json file"""
    return send_from_directory(static_path, descriptor)
