from flask import g
from flask_restful import Resource

from interceptor.interceptor import login_required


class HelloController(Resource):
    @login_required
    def get(self):
        print(g.username)
        return "Hello World!"
