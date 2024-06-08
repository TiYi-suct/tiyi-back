from flask_restful import Api

from controller.audio_controller import AudioUpload, AudioDownload
from controller.audio_tags_controller import AudioTagsController
from controller.user_controller import UserRegister, UserLogin


def config_routes(app):
    api = Api(app)

    # hello
    # api.add_resource(HelloController, '/hello')

    # 用户相关资源
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')

    # 音频相关资源
    api.add_resource(AudioUpload, '/audio/upload')
    api.add_resource(AudioDownload, '/audio/download/<filename>')

    # 音频标签相关资源
    api.add_resource(AudioTagsController, '/audio_tags')