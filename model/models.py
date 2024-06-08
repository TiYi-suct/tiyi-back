from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
用户模型
'''


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


'''
音频模型
'''


class Audio(db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    extension = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(1023), unique=True, nullable=False)
    tags = db.Column(db.String(1023), unique=True, nullable=False)
    cover = db.Column(db.String(1023), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
