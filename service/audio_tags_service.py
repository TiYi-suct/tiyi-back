from model.models import AudioTags, db
from utils.response import Response


class AudioTagsService:
    @staticmethod
    def add_audio_tags(username, tag_name):
        # 查询是否有记录
        audio_tags = AudioTags.query.filter_by(username=username).first()
        if audio_tags:
            # 存在则更新
            existing_audio_tags = audio_tags.tags.split(',') if audio_tags.tags else []
            if tag_name in existing_audio_tags:
                return Response.error(f'重复的标签名：{tag_name}')
            else:
                existing_audio_tags.append(tag_name)
                audio_tags.tags = ','.join(existing_audio_tags)
        else:
            # 不存在则插入
            audio_tags = AudioTags(
                username=username,
                tags=tag_name
            )
            db.session.add(audio_tags)
        db.session.commit()
        return Response.success()

    @staticmethod
    def query_audio_tags(username):
        audio_tags = AudioTags.query.filter_by(username=username).first()
        return Response.success(audio_tags.tags.split(',') if audio_tags and audio_tags.tags else [])

    @staticmethod
    def delete_audio_tags(username, tag_name):
        # 查询是否有记录
        audio_tags = AudioTags.query.filter_by(username=username).first()
        if not audio_tags:
            return Response.error(f'用户 {username} 未定义标签')
        existing_tags = audio_tags.tags.split(',') if audio_tags.tags else []
        if tag_name not in existing_tags:
            return Response.error(f'用户 {username} 未定义标签：{tag_name}')
        # 删除指定标签
        existing_tags.remove(tag_name)
        # 更新记录
        audio_tags.tags = ','.join(existing_tags)
        db.session.commit()
        return Response.success(existing_tags)
