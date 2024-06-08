import logging

from flask import request, g, send_from_directory
from flask_restful import Resource

from config.config import Config
from interceptor.interceptor import login_required
from service.file_service import FileService
from utils.response import Response


class FileController(Resource):
    """
    无需分析的其他文件例如图片等调用此接口进行上传，不做格式检查
    """

    @login_required
    def post(self):
        if 'file' not in request.files:
            return Response.error('请选择要上传的文件')
        logging.debug(f'用户 {g.username} 上传文件 {request.files['file'].filename}')
        return FileService.upload(request.files['file'])

    """
    所有文件的下载接口
    """

    @staticmethod
    def get(filename):
        return send_from_directory(Config.STORE_FOLDER, filename)
