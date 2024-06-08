from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
用户模型
"""


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    music_coin = db.Column(db.Integer, default=100)
    avatar = db.Column(db.String(1023), nullable=True)
    signature = db.Column(db.String(1023), default='在签名中展现你的个性吧！')
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())


"""
音频模型
"""


class Audio(db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    audio_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    local_path = db.Column(db.String(1023), unique=True, nullable=False)
    url = db.Column(db.String(1023), unique=True, nullable=False)
    tags = db.Column(db.String(1023), unique=False, nullable=False)
    cover = db.Column(db.String(1023), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def to_dict(self):
        return {
            'audio_id': self.audio_id,
            'name': self.name,
            'extension': self.extension,
            'url': self.url,
            'tags': self.tags.split(',') if self.tags else [],
            'cover': self.cover,
            'username': self.username
        }


"""
用户定义音频标签模型
"""


class AudioTags(db.Model):
    __tablename__ = 'audio_tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.String(1023), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
