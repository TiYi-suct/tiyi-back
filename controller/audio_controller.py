from flask import request, send_from_directory
from flask_restful import Resource

from config.config import Config
from interceptor.interceptor import login_required
from service.audio_service import AudioService
from utils.response import Response


class AudioUpload(Resource):
    @login_required
    def post(self):
        # 检查是否存在文件
        if 'file' not in request.files:
            return Response.error('请上传音频文件')
        return AudioService.upload(request.files['file'])


class AudioDownload(Resource):
    @staticmethod
    def get(filename):
        return send_from_directory(Config.AUDIO_UPLOAD_FOLDER, filename)
