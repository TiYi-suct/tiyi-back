from flask import request
from flask_restful import Resource

from service.user_service import UserService

'''
用户注册接口
'''


class UserRegister(Resource):
    @staticmethod
    def post():
        return UserService.register(request.get_json())
