from flask import request, g
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.user_service import UserService
from utils.response import Response


class UserController(Resource):
    @login_required
    def get(self):
        return UserService.get_user_by_username(g.username)

    def post(self, action=None):
        if action == 'login':
            return UserService.login(request.json)
        if action == 'register':
            return UserService.register(request.json)
        return Response.not_exist()

    @login_required
    def put(self, action=None):
        if action == 'avatar':
            avatar = request.files['avatar']
            return UserService.update_avatar(g.username, avatar)
        if action == 'signature':
            signature = request.args.get('signature')
            return UserService.edit_signature(g.username, signature)
        return Response.not_exist()
