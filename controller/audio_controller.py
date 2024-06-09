from flask import request, send_from_directory, g
from flask_restful import Resource

from config.config import Config
from interceptor.interceptor import login_required
from service.audio_service import AudioService
from utils.response import Response

'''
单条音频操作
'''


class AudioController(Resource):
    @login_required
    def get(self):
        audio_id = request.args.get('audio_id')
        return AudioService.query_by_audio_id(g.username, audio_id)

    @login_required
    def delete(self):
        audio_id = request.args.get('audio_id')
        return AudioService.delete_by_audio_id(g.username, audio_id)


'''
条件查询音频列表
'''


class AudioQuery(Resource):
    @login_required
    def get(self):
        name = request.args.get('name')
        tags = request.args.get('tags')
        return AudioService.query_audios(g.username, name, tags)


'''
此接口上传的是需要分析的音频文件，业务相关，需要在数据库保存记录，所以单独提供接口
也就是说，调用此接口上传文件，就相当于新增一条音频记录
此接口会对文件格式进行检查
'''


class AudioUpload(Resource):
    @login_required
    def post(self):
        # 检查是否存在文件
        if 'file' not in request.files:
            return Response.error('请上传音频文件')
        return AudioService.upload(request.files['file'])


class AudioLabeling(Resource):
    @login_required
    def put(self):
        data = request.json
        if not data or not data.get('audio_id') or not data.get('tags'):
            return Response.error('参数错误')
        audio_id = data['audio_id']
        tags = data['tags']
        return AudioService.labeling(g.username, audio_id, tags)


