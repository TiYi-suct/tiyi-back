from flask import request, g
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.user_service import UserService


class UserController(Resource):
    @login_required
    def get(self):
        return UserService.get_user_by_username(g.username)


'''
用户注册接口
'''


class UserRegister(Resource):
    @staticmethod
    def post():
        return UserService.register(request.json)


'''
用户登录接口
'''


class UserLogin(Resource):
    @staticmethod
    def post():
        return UserService.login(request.json)
