from flask_restful import Resource
from server import api
from server.authentication import authenticate


class Test(Resource):
    method_decorators = [authenticate]

    def get(self):
        return 'OK'

api.add_resource(Test, '/hello-world')
