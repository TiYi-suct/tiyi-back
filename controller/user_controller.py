from flask import request
from flask_restful import Resource

from service.user_service import UserService

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
