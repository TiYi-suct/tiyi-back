import os

"""
项目配置类
"""


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUDIO_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'files', 'audios')
    SERVER_URL = os.getenv('SERVER_URL')