import os
import uuid

from flask import g
from sqlalchemy import or_

from config.config import Config
from model.models import Audio, db
from utils.response import Response


class AudioService:
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}

    @staticmethod
    def query_by_audio_id(username, audio_id):
        audio = Audio.query.filter_by(audio_id=audio_id).first()
        if not audio:
            return Response.error('音频不存在')
        if not username == audio.username:
            return Response.error(f'非法操作：音频不属于用户：{username}')
        return Response.success(audio.to_dict())

    @staticmethod
    def delete_by_audio_id(username, audio_id):
        audio = Audio.query.filter_by(audio_id=audio_id).first()
        if not audio:
            return Response.error('音频不存在')
        if not username == audio.username:
            return Response.error(f'非法操作：音频不属于用户：{username}')
        db.session.delete(audio)
        db.session.commit()
        return Response.success()

    @staticmethod
    def query_audios(username, name, tags):
        query = Audio.query
        query = query.filter(Audio.username == username)
        if name:
            query = query.filter(Audio.name.like(f'%{name}%'))
        if tags and len(tags) > 0:
            tags_list = tags.split(',')
            tag_filters = [Audio.tags.like(f"%{tag}%") for tag in tags_list]
            query = query.filter(or_(*tag_filters))
        audios = query.order_by(Audio.update_time.desc()).all()
        if not audios:
            return Response.success([])
        result = []
        for audio in audios:
            result.append(audio.to_dict())
        return Response.success(result)

    @staticmethod
    def upload(file):
        # 检查文件
        if not file or file.filename == '':
            return Response.error('请选择要上传的文件')
        # 检查文件格式
        if not AudioService.allowed_file(file.filename):
            return Response.error('不支持的文件格式，仅支持分析wav、mp3、ogg、flac格式')
        extension = file.filename.split('.')[-1]
        # 生成文件唯一id，作为文件名
        audio_id = uuid.uuid4().hex
        origin_name = file.filename.split('.')[0]
        filename = f'{audio_id}.{extension}'
        filepath = os.path.join(Config.STORE_FOLDER, filename)
        # 将文件保存服务器
        file.save(filepath)
        url = f'{Config.SERVER_URL}/file/{filename}'
        # 将文件记录保存到数据库
        audio = Audio(
            audio_id=audio_id,
            name=origin_name,
            extension=extension,
            local_path=filepath,
            url=url,
            username=g.username
        )
        db.session.add(audio)
        db.session.commit()
        # 将文件访问地址返回给用户
        return Response.success({
            'audio_id': audio_id,
            'url': url
        })

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in AudioService.ALLOWED_EXTENSIONS

    @staticmethod
    def labeling(username, audio_id, tags):
        # 给音频打上标签
        audio = Audio.query.filter_by(audio_id=audio_id).first()
        if not audio:
            return Response.error('音频不存在')
        if audio.username != username:
            return Response.error(f'非法操作，音频不属于用户：{username}')
        audio.tags = tags
        db.session.commit()
        return Response.success()
