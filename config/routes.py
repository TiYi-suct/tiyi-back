from flask_restful import Api

from controller.analysis_item_controller import AnalysisItemController
from controller.audio_controller import AudioUpload, AudioDownload, AudioLabeling, AudioController, AudioQuery
from controller.audio_tags_controller import AudioTagsController
from controller.user_controller import UserRegister, UserLogin, UserController


def config_routes(app):
    api = Api(app)

    # hello
    # api.add_resource(HelloController, '/hello')

    # 用户相关资源
    api.add_resource(UserController, '/user')
    api.add_resource(UserRegister, '/user/register')
    api.add_resource(UserLogin, '/user/login')

    # 音频相关资源
    api.add_resource(AudioController, '/audio')
    api.add_resource(AudioQuery, '/audio/list')
    api.add_resource(AudioUpload, '/audio/upload')
    api.add_resource(AudioDownload, '/audio/download/<filename>')
    api.add_resource(AudioLabeling, '/audio/labeling')

    # 音频标签相关资源
    api.add_resource(AudioTagsController, '/audio_tags')

    # 分析项目相关资源
    api.add_resource(AnalysisItemController, '/analysis_item')
