from flask_restful import Resource
from server import api
from server.authentication import authenticate, development_only
from flask import request, jsonify
from server.lib import AtLib


class Test(Resource):
    method_decorators = [authenticate]

    def get(self):
        return 'OK'


class Explorer(Resource):
    method_decorators = [development_only]

    def get(self):
        return 'OK'

    def post(self):
        req = AtLib(request.form['baseUrl'])
        resp = req.request(request.form['method'], request.form['rel']).json()
        return jsonify(resp)


api.add_resource(Test, '/hello-world')
api.add_resource(Explorer, '/explore')
