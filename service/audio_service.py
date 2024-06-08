import os
import uuid

from flask import g

from config.config import Config
from model.models import Audio, db
from utils.response import Response


class AudioService:
    @staticmethod
    def upload(file):
        # 检查文件
        if not file or file.filename == '':
            return Response.error_default('请选择要上传的文件')
        # 生成文件唯一id，作为文件名
        audio_id = uuid.uuid4().hex
        origin_name = file.filename.split('.')[0]
        extension = file.filename.split('.')[-1]
        filename = f'{audio_id}.{extension}'
        filepath = os.path.join(Config.AUDIO_UPLOAD_FOLDER, filename)
        # 将文件保存服务器
        file.save(filepath)
        url = f'{Config.SERVER_URL}/audio/download/{filename}'
        # 将文件记录保存到数据库
        audio = Audio(
            name=origin_name,
            extension=extension,
            path=filepath,
            username=g.username
        )
        db.session.add(audio)
        db.session.commit()
        # 将文件访问地址返回给用户
        return Response.success({
            'audio_id': audio_id,
            'url': url
        })
