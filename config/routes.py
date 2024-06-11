from flask_restful import Api

from controller.analysis_controller import MelSpectrogram, Spectrogram, BPM, Transposition, MFCC
from controller.analysis_item_controller import AnalysisItemController, AnalysisItemConsumption
from controller.audio_controller import AudioUpload, AudioLabeling, AudioController, AudioQuery
from controller.audio_tags_controller import AudioTagsController
from controller.file_controller import FileController
from controller.pay_controller import GetOrderInfo, PayResultNotify
from controller.recharge_item_controller import RechargeItemController
from controller.user_controller import UserController


def config_routes(app):
    api = Api(app)

    # hello
    # api.add_resource(HelloController, '/hello')

    # 用户相关资源
    api.add_resource(UserController, '/user', '/user/<string:action>')

    # 音频相关资源
    api.add_resource(AudioController, '/audio')
    api.add_resource(AudioQuery, '/audio/list')
    api.add_resource(AudioUpload, '/audio/upload')
    api.add_resource(AudioLabeling, '/audio/labeling')

    # 音频标签相关资源
    api.add_resource(AudioTagsController, '/audio_tags')

    # 分析项目相关资源
    api.add_resource(AnalysisItemController, '/analysis_item')
    api.add_resource(AnalysisItemConsumption, '/analysis_item/consumption')

    # 充值项目相关资源
    api.add_resource(RechargeItemController, '/recharge_item')

    # 支付相关资源
    api.add_resource(GetOrderInfo, '/pay/order_info_str')
    api.add_resource(PayResultNotify, '/pay/notify')

    # 文件相关资源
    api.add_resource(FileController, '/file', '/file/<string:filename>')

    # 音频分析相关资源
    api.add_resource(MelSpectrogram, '/analysis/mel_spectrogram')
    api.add_resource(Spectrogram, '/analysis/spectrogram')
    api.add_resource(BPM, '/analysis/bpm')
    api.add_resource(Transposition, '/analysis/transposition')
    api.add_resource(MFCC, '/analysis/mfcc')
