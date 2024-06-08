"""
音频分析相关接口
"""
from flask import request, g
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.analysis_service import AnalysisService


# 梅尔频谱图
class MelSpectrogram(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', -1.0)
        return AnalysisService.mel_spectrogram(g.username, audio_id, float(start_time), float(end_time))
