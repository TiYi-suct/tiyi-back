from flask_restful import Api

from controller.user_controller import UserRegister, UserLogin


def config_routes(app):
    api = Api(app)

    # 用户相关资源
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')
