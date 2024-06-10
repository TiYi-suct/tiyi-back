"""
音频分析相关接口
"""
from flask import request
from flask_restful import Resource

from interceptor.interceptor import login_required
from service.analysis_service import mel_spectrogram, spectrogram, bpm, transposition, mfcc


# 梅尔频谱图
class MelSpectrogram(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', -1.0)
        return mel_spectrogram(audio_id, float(start_time), float(end_time))


# 频谱图
class Spectrogram(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', -1.0)
        return spectrogram(audio_id, float(start_time), float(end_time))


# BPM
class BPM(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', -1.0)
        return bpm(audio_id, float(start_time), float(end_time))


# 移调
class Transposition(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', -1.0)
        n_steps = request.args.get('n_steps', 2)
        return transposition(audio_id, float(start_time), float(end_time), int(n_steps))


# MFCC
class MFCC(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        start_time = request.args.get('start_time', 0)
        end_time = request.args.get('end_time', -1.0)
        n_mfcc = request.args.get('n_mfcc', 20)
        return mfcc(audio_id, float(start_time), float(end_time), int(n_mfcc))
