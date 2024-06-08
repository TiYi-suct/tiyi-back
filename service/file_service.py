import os
import uuid

from config.config import Config
from utils.response import Response


class FileService:
    @staticmethod
    def upload(file):
        if not file or file.filename == '':
            return Response.error('请选择要上传的文件')
        # 生成唯一文件id
        file_id = uuid.uuid4().hex
        if '.' in file.filename:
            filename = f'{file_id}.{file.filename.split('.')[-1]}'
        else:
            filename = file_id
        # 保存到服务器
        filepath = os.path.join(Config.STORE_FOLDER, filename)
        file.save(filepath)
        # 文件远程访问url
        url = f'{Config.SERVER_URL}/file/{filename}'
        return Response.success(url)
